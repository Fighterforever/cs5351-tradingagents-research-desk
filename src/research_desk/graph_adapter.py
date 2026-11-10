"""Clean integration seam with the real ``TradingAgentsGraph``.

Live runs use the actual upstream graph — its real analysts, bull/bear
researchers, research manager, trader, risk debators and portfolio manager —
with two narrow extension points owned by the subclass:

- ``resolve_instrument_context`` is overridden to *record* the direct
  ticker-identity data path (callbacks cannot see it) and to substitute a
  frozen identity on controlled reruns.
- ``_fetch_returns`` is overridden to record the direct realized-returns read
  and to skip network resolution on frozen reruns.
- ``_create_tool_nodes`` is overridden so a controlled rerun feeds the exact
  frozen evidence back into the same ToolNodes the live graph uses. The graph
  topology and every agent are untouched.

There is no monkeypatching of global state, no replacement of upstream agents
and no toy pipeline: the frozen-tool variant is the same compiled graph with
the same nodes, only its data source is frozen.

``ResearchRunner`` orchestrates one run: assemble context (baseline/compact),
stream the graph with the evidence recorder + budget, capture the final state,
derive the signal deterministically, write reports, and create a PENDING_REVIEW
proposal when the signal is tradeable.
"""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Callable
from pathlib import Path
from typing import Any

from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode

from tradingagents.agents.utils.agent_utils import (
    build_instrument_context,
    resolve_instrument_identity,
)
from tradingagents.agents.utils.rating import is_review
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.reporting import write_report_tree

from .budget import BudgetExhausted, BudgetTracker, ContextBudgetExceeded
from .config import ResearchDeskSettings
from .context import ContextAssembler, StandingConstraints, build_common_grounding
from .evidence import EvidenceLog, EvidencePackIO, record_data_read
from .models import (
    InputSnapshot,
    ProposalRecord,
    RunManifest,
    RunOutcome,
    RunResult,
    utcnow_iso,
)
from .report import apply_research_identity_header, render_research_identity
from .review import ReviewError, create_proposal

logger = logging.getLogger(__name__)


def _provider_tools(provider: Any) -> dict[str, Any]:
    """Build frozen tools bound to a concrete ``FrozenMarketProvider``.

    Each tool computes its result from the fixed CSV via the provider, so a
    frozen run answers whichever tool arguments the (compact) model selects
    instead of failing an exact-args transcript lookup.
    """

    @tool("get_stock_data")
    def get_stock_data(
        symbol: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """Frozen-evidence get_stock_data (same schema), computed from the fixed CSV."""
        return provider.get_stock_data(symbol, start_date, end_date)

    @tool("get_indicators")
    def get_indicators(
        symbol: str,
        indicator: str,
        curr_date: str,
        look_back_days: int = 30,
    ) -> str:
        """Frozen-evidence get_indicators, computed from the fixed CSV."""
        return provider.get_indicators(symbol, indicator, curr_date, look_back_days)

    @tool("get_verified_market_snapshot")
    def get_verified_market_snapshot(
        symbol: str,
        curr_date: str,
        look_back_days: int = 30,
    ) -> str:
        """Frozen-evidence get_verified_market_snapshot, computed from the fixed CSV."""
        return provider.get_verified_market_snapshot(symbol, curr_date, look_back_days)

    @tool("get_news")
    def get_news(
        ticker: str,
        start_date: str,
        end_date: str,
    ) -> str:
        """Frozen-evidence get_news (honest unavailable; news is supplied as evidence notes)."""
        return provider.get_news(ticker, start_date, end_date)

    @tool("get_global_news")
    def get_global_news(
        curr_date: str,
        look_back_days: int | None = None,
        limit: int | None = None,
    ) -> str:
        """Frozen-evidence get_global_news (unsupported)."""
        return provider.get_global_news(curr_date, look_back_days, limit)

    @tool("get_insider_transactions")
    def get_insider_transactions(ticker: str) -> str:
        """Frozen-evidence get_insider_transactions (unsupported)."""
        return provider.get_insider_transactions(ticker)

    @tool("get_macro_indicators")
    def get_macro_indicators(
        indicator: str,
        curr_date: str,
        look_back_days: int | None = None,
    ) -> str:
        """Frozen-evidence get_macro_indicators (unsupported, honest sentinel)."""
        return provider.get_macro_indicators(indicator, curr_date, look_back_days)

    @tool("get_prediction_markets")
    def get_prediction_markets(
        topic: str,
        limit: int | None = None,
    ) -> str:
        """Frozen-evidence get_prediction_markets (unsupported, honest sentinel)."""
        return provider.get_prediction_markets(topic, limit)

    return {
        "get_stock_data": get_stock_data,
        "get_indicators": get_indicators,
        "get_verified_market_snapshot": get_verified_market_snapshot,
        "get_news": get_news,
        "get_global_news": get_global_news,
        "get_insider_transactions": get_insider_transactions,
        "get_macro_indicators": get_macro_indicators,
        "get_prediction_markets": get_prediction_markets,
    }


class EvidenceTradingGraph(TradingAgentsGraph):
    """TradingAgentsGraph subclass that records direct data paths and can freeze evidence."""

    def __init__(
        self,
        selected_analysts=("market", "news"),
        debug=False,
        config: dict[str, Any] | None = None,
        callbacks: list | None = None,
        *,
        data_mode: str = "live",
        evidence_log: EvidenceLog | None = None,
        data_snapshot: dict[str, dict[str, str]] | None = None,
        frozen_identity: dict[str, Any] | None = None,
        frozen_provider: Any = None,
    ):
        self.data_mode = data_mode
        self.evidence_log = evidence_log
        self.data_snapshot = data_snapshot or {}
        self._frozen_identity = frozen_identity
        self._frozen_provider = frozen_provider
        self.last_identity: dict[str, Any] = {}
        # In frozen mode the provider carries the fixed case identity; never fall
        # back to an online identity lookup (no hidden identity request).
        if (
            self.data_mode == "frozen"
            and self._frozen_identity is None
            and self._frozen_provider is not None
        ):
            self._frozen_identity = dict(
                getattr(self._frozen_provider, "identity", None) or {}
            )
        super().__init__(selected_analysts=selected_analysts, debug=debug, config=config, callbacks=callbacks)

    def _create_tool_nodes(self) -> dict[str, ToolNode]:
        if self.data_mode != "frozen":
            return super()._create_tool_nodes()
        tools = _provider_tools(self._frozen_provider)
        return {
            "market": ToolNode(
                [
                    tools["get_stock_data"],
                    tools["get_indicators"],
                    tools["get_verified_market_snapshot"],
                ]
            ),
            "social": ToolNode([tools["get_news"]]),
            "news": ToolNode(
                [
                    tools["get_news"],
                    tools["get_global_news"],
                    tools["get_insider_transactions"],
                    tools["get_macro_indicators"],
                    tools["get_prediction_markets"],
                ]
            ),
            "fundamentals": ToolNode([]),
        }

    def resolve_instrument_context(self, ticker: str, asset_type: str = "stock") -> str:
        """Resolve identity (live lookup or frozen), record it, build the context string."""
        if self.data_mode == "frozen":
            if self._frozen_identity is None:
                raise ValueError(
                    f"frozen run for {ticker} has no frozen identity; "
                    "a fixed case identity must be supplied (no hidden online lookup)"
                )
            identity = dict(self._frozen_identity)
        else:
            identity = resolve_instrument_identity(ticker)
        self.last_identity = identity
        if self.evidence_log is not None:
            record_data_read(
                self.evidence_log,
                "instrument_identity",
                ticker,
                identity,
                node="graph.resolve_instrument_context",
            )
        return build_instrument_context(ticker, asset_type, identity)

    def _fetch_returns(
        self, ticker: str, trade_date: str, holding_days: int = 5, benchmark: str = "SPY",
    ) -> tuple[float | None, float | None, int | None, str | None]:
        """Record the realized-returns read; skip network resolution on frozen reruns."""
        if self.data_mode == "frozen":
            if self.evidence_log is not None:
                record_data_read(
                    self.evidence_log,
                    "realized_returns",
                    ticker,
                    {"mode": "frozen", "skipped": True, "trade_date": trade_date},
                    node="graph.resolve_pending_entries",
                )
            return None, None, None, None
        result = super()._fetch_returns(ticker, trade_date, holding_days, benchmark)
        if self.evidence_log is not None:
            record_data_read(
                self.evidence_log,
                "realized_returns",
                ticker,
                {
                    "trade_date": trade_date,
                    "holding_days": holding_days,
                    "raw_return": result[0],
                    "alpha_return": result[1],
                    "resolution_date": result[3],
                },
                node="graph.resolve_pending_entries",
            )
        return result


def _available_sources_from_provider(provider: Any, ticker: str, trade_date: str) -> dict[str, Any]:
    """The factual available corpus for a frozen case, independent of tool calls.

    This is real CSV + case metadata (never fabricated or fake tool calls), kept
    separate from the tools actually invoked so the evidence-derived price stays
    available for proposal/replay even when a model path did not ask a data tool.
    """
    case = dict(getattr(provider, "case", None) or {})
    market = ""
    verified = ""
    news = ""
    if hasattr(provider, "get_stock_data"):
        market = provider.get_stock_data(ticker, "", trade_date)
    if hasattr(provider, "get_verified_market_snapshot"):
        verified = provider.get_verified_market_snapshot(ticker, trade_date, look_back_days=30)
    if hasattr(provider, "get_news"):
        news = provider.get_news(ticker)
    from .context import market_source_id

    return {
        "identity": dict(getattr(provider, "identity", None) or {}),
        "market": market,
        "verified_snapshot": verified,
        "news": news,
        "as_of": case.get("as_of", ""),
        "latest_close": case.get("latest_close"),
        "source_id": case.get("source_id", ""),
        "market_source_id": market_source_id(ticker),
        "announcement_date": case.get("announcement_date", ""),
        "analysis_date": case.get("analysis_date", ""),
    }


def _parse_stock_data_price(table: dict[str, str]) -> float | None:
    import csv
    import io

    best: float | None = None
    for result in table.values():
        if not result.startswith("# Stock data for"):
            continue
        csv_lines = [ln for ln in result.splitlines() if ln and not ln.startswith("#")]
        if not csv_lines:
            continue
        try:
            rows = list(csv.DictReader(io.StringIO("\n".join(csv_lines))))
        except Exception:
            continue
        for row in reversed(rows):
            close = row.get("Close")
            if close:
                try:
                    best = float(close)
                except (TypeError, ValueError):
                    continue
                break
    return best


def _parse_verified_snapshot_price(table: dict[str, str]) -> float | None:
    for result in table.values():
        for line in result.splitlines():
            if line.lower().startswith("last_close:"):
                try:
                    return float(line.split(":", 1)[1].strip())
                except (TypeError, ValueError):
                    return None
    return None


def price_from_evidence(
    snapshot: dict[str, dict[str, str]],
    ticker: str,
    available_sources: dict[str, Any] | None = None,
) -> float | None:
    """Extract the latest close for ``ticker`` from evidence.

    Checks, in order: observed ``get_stock_data`` results, observed
    ``get_verified_market_snapshot`` results, then the factual available corpus
    (the real market CSV / verified snapshot) when no tool path produced a price.
    This is the only price source for proposals — the operator never types a
    price. Returns ``None`` when no price evidence exists.
    """
    best = _parse_stock_data_price(snapshot.get("get_stock_data", {}))
    if best is None:
        best = _parse_verified_snapshot_price(snapshot.get("get_verified_market_snapshot", {}))
    if best is None and available_sources:
        best = _parse_stock_data_price({"available": str(available_sources.get("market", ""))})
        if best is None:
            best = _parse_verified_snapshot_price(
                {"available": str(available_sources.get("verified_snapshot", ""))}
            )
    return best


def merge_trace(trace: list[dict[str, Any]]) -> dict[str, Any]:
    final_state: dict[str, Any] = {}
    for chunk in trace:
        final_state.update(chunk)
    return final_state


def decide_proposal(
    *,
    outcome: str,
    signal: str | None,
    run_id: str,
    ticker: str,
    trade_date: str,
    snapshot: dict[str, dict[str, str]],
    evidence_id: str | None = None,
    available_sources: dict[str, Any] | None = None,
) -> ProposalRecord | None:
    """Decide whether a run yields a PENDING_REVIEW proposal.

    The single place that enforces "a budget-stopped or failed run is never
    approvable, and Hold/REVIEW do not trade". Tradeable signals are the Buy
    family (buy) and Sell family (sell, validated against owned shares at
    execution); the price must come from evidence (observed tool result or the
    factual available corpus).
    """
    if outcome != RunOutcome.COMPLETED.value:
        return None  # budget-stopped / failed runs never become approvable (NFR-003)
    if not signal or is_review(signal):
        return None
    from .review import BUY_SIGNALS, SELL_SIGNALS, ReviewError

    if signal not in BUY_SIGNALS and signal not in SELL_SIGNALS:
        return None
    price = price_from_evidence(snapshot, ticker, available_sources=available_sources)
    if price is None:
        return None  # price must come from evidence; no price -> nothing to review
    try:
        return create_proposal(
            run_id=run_id,
            ticker=ticker,
            trade_date=trade_date,
            signal=signal,
            rating=signal,
            price=price,
            evidence_id=evidence_id,
        )
    except ReviewError:
        return None


class ResearchRunner:
    """Runs one research session against the real graph and produces evidence + proposal."""

    def __init__(
        self,
        settings: ResearchDeskSettings,
        *,
        context_mode: str = "baseline",
        data_mode: str = "live",
        source_pack: Any = None,
        graph_config: dict[str, Any] | None = None,
        llm_factory: Callable[..., tuple[Any, Any]] | None = None,
        frozen_provider: Any = None,
        evidence_id: str | None = None,
    ):
        self.settings = settings
        self.context_mode = context_mode
        self.data_mode = data_mode
        self.source_pack = source_pack
        self.graph_config = graph_config or {}
        self.llm_factory = llm_factory
        self.frozen_provider = frozen_provider
        self.evidence_id = evidence_id
        self.io = EvidencePackIO()

    # ------------------------------------------------------------------
    # Memory / context source
    # ------------------------------------------------------------------

    def _memory_entries(self, ticker: str, trade_date: str) -> list[dict[str, Any]]:
        if self.data_mode == "frozen" and self.source_pack is not None:
            return self.source_pack.input.memory_used
        from tradingagents.agents.utils.memory import TradingMemoryLog

        log = TradingMemoryLog(self.graph_config)
        return [e for e in log.load_entries() if e.get("ticker") == ticker]

    def _assemble_context(self, ticker: str, trade_date: str, identity: dict[str, Any]) -> Any:
        prices: dict[str, float] = {}
        if self.frozen_provider is not None:
            price = self._price_from_provider(ticker, trade_date)
            if price is not None:
                prices["last_close"] = price
        elif self.data_mode == "frozen" and self.source_pack is not None:
            price = price_from_evidence(self.source_pack.input.data_snapshot, ticker)
            if price is not None:
                prices["last_close"] = price
        constraints = StandingConstraints(
            ticker=ticker,
            trade_date=trade_date,
            identity=identity,
            prices=prices,
            policy={
                "initial_cash": "USD 100000",
                "max_single_position": "10% of equity",
                "integer_shares": "yes",
                "no_shorting": "yes",
            },
            current_task=(
                f"Produce the research-desk analysis of {ticker} on {trade_date} "
                "for US equities (market + news analysts)."
            ),
        )
        assembler = ContextAssembler(constraints)
        entries = self._memory_entries(ticker, trade_date)
        return assembler.assemble_from_entries(entries, self.context_mode)

    def _build_graph(
        self,
        config,
        recorder,
        evidence_log,
        *,
        frozen_snapshot,
        frozen_identity,
        ticker=None,
        trade_date=None,
    ):
        """Construct the real graph and install the COMMON grounding layer.

        No global factory patch and no dynamic ``__class__`` mutation. The graph
        is built normally with the real ``create_llm_client`` (its no-monkeypatch
        contract). For BOTH arms we then wrap the graph's *actual* quick/deep
        model attributes with a small declared delegate that injects the common
        grounding layer into every request, and rebuild the ``GraphSetup`` with
        the original memory objects, tool nodes, conditional logic and selected
        analysts, then recompile. Baseline keeps the substantive history
        uncompressed; compact also trims/de-duplicates and adds the concise
        output instruction.
        """
        graph = EvidenceTradingGraph(
            self.settings.analysts,
            debug=False,
            config=config,
            callbacks=[recorder],
            data_mode=self.data_mode,
            evidence_log=evidence_log,
            data_snapshot=frozen_snapshot,
            frozen_identity=frozen_identity,
            frozen_provider=self.frozen_provider,
        )

        # Forward an ``extra_body`` (e.g. DeepSeek ``thinking={"type":"disabled"}``)
        # onto the actual model attributes so it reaches the provider request.
        # ``ChatOpenAI.extra_body`` flows into the request payload (see
        # ``_default_params``); it is not part of the client factory's passthrough
        # keys, so we set it on the constructed models directly.
        extra_body = config.get("extra_body")
        if isinstance(extra_body, dict) and extra_body:
            for llm in (graph.quick_thinking_llm, graph.deep_thinking_llm):
                if hasattr(llm, "extra_body"):
                    llm.extra_body = dict(extra_body)

        from tradingagents.graph.reflection import Reflector
        from tradingagents.graph.setup import GraphSetup
        from tradingagents.graph.signal_processing import SignalProcessor

        from .eval.compact_delegate import BudgetObservation, wrap_for_mode

        # The one COMMON grounding layer, derived from the real per-case
        # provider/available_sources, identical for both arms.
        available_sources = self._available_sources(
            ticker or "", trade_date or "", frozen_identity
        )
        common_grounding = build_common_grounding(
            ticker or "", trade_date or "", available_sources
        )

        def _observe_budget(observation: BudgetObservation) -> None:
            if evidence_log is not None:
                evidence_log.record("context_budget", **observation)

        graph.quick_thinking_llm = wrap_for_mode(
            graph.quick_thinking_llm,
            self.context_mode,
            common_grounding=common_grounding,
            context_max_tokens=self.settings.context_max_tokens,
            context_trigger_tokens=self.settings.context_trigger_tokens,
            budget_observer=_observe_budget,
        )
        graph.deep_thinking_llm = wrap_for_mode(
            graph.deep_thinking_llm,
            self.context_mode,
            common_grounding=common_grounding,
            context_max_tokens=self.settings.context_max_tokens,
            context_trigger_tokens=self.settings.context_trigger_tokens,
            budget_observer=_observe_budget,
        )

        # Rebuild the setup with the wrapped models but the *original* memory
        # objects, tool nodes and conditional logic, plus the selected analysts.
        graph.graph_setup = GraphSetup(
            graph.quick_thinking_llm,
            graph.deep_thinking_llm,
            graph.tool_nodes,
            graph.conditional_logic,
        )
        graph.reflector = Reflector(graph.quick_thinking_llm)
        graph.signal_processor = SignalProcessor(graph.quick_thinking_llm)
        graph.workflow = graph.graph_setup.setup_graph(self.settings.analysts)
        graph.graph = graph.workflow.compile()
        return graph

    def _price_from_provider(self, ticker: str, trade_date: str) -> float | None:
        """Latest close for ``ticker`` at or before ``trade_date`` from the fixed CSV."""
        frame = self.frozen_provider.frame
        df = frame if not trade_date else frame[frame["Date"] <= trade_date]
        if df.empty:
            return None
        return float(df.iloc[-1]["Close"])

    # ------------------------------------------------------------------
    # Main run
    # ------------------------------------------------------------------

    def run(self, ticker: str, trade_date: str, asset_type: str = "stock") -> RunResult:
        run_id = f"run-{uuid.uuid4().hex[:12]}"
        evidence_log = EvidenceLog()
        budget = BudgetTracker(max_calls=self.settings.max_calls)

        from .evidence import EvidenceRecorder

        recorder = EvidenceRecorder(evidence_log, budget)
        evidence_log.record(
            "run_start",
            run_id=run_id,
            ticker=ticker,
            trade_date=trade_date,
            context_mode=self.context_mode,
            data_mode=self.data_mode,
            budget_max_calls=self.settings.max_calls,
        )

        config = dict(self.graph_config)
        config.setdefault("checkpoint_enabled", False)
        config.setdefault("results_dir", str(self.settings.home_path / "logs"))

        frozen_snapshot: dict[str, dict[str, str]] = {}
        frozen_identity: dict[str, Any] | None = None
        if self.frozen_provider is not None:
            frozen_identity = getattr(self.frozen_provider, "identity", None) or {}
        elif self.data_mode == "frozen" and self.source_pack is not None:
            frozen_snapshot = self.source_pack.input.data_snapshot
            frozen_identity = self.source_pack.input.identity

        self._run_events = evidence_log.events
        graph = self._build_graph(
            config, recorder, evidence_log,
            frozen_snapshot=frozen_snapshot, frozen_identity=frozen_identity,
            ticker=ticker, trade_date=trade_date,
        )

        # Identity: recorded by the graph override; needed for context constraints.
        instrument_context = graph.resolve_instrument_context(ticker, asset_type)
        identity = graph.last_identity

        assembly = self._assemble_context(ticker, trade_date, identity)
        evidence_log.record(
            "context_assembled",
            mode=assembly.mode,
            chars=assembly.chars,
            blocks=assembly.blocks,
            deduplicated=assembly.deduplicated,
            truncated=assembly.truncated,
            token_heuristic=assembly.token_heuristic,
        )

        init_state = graph.propagator.create_initial_state(
            ticker,
            trade_date,
            asset_type=asset_type,
            past_context=assembly.text,
            instrument_context=instrument_context,
        )
        args = graph.propagator.get_graph_args(callbacks=[recorder])

        trace: list[dict[str, Any]] = []
        start = time.time()
        outcome = RunOutcome.COMPLETED
        error: str | None = None
        context_stopped = False
        try:
            for chunk in graph.graph.stream(init_state, **args):
                trace.append(chunk)
        except ContextBudgetExceeded as exc:
            outcome = RunOutcome.BUDGET_STOPPED
            context_stopped = True
            evidence_log.record(
                "budget_stop",
                reason=exc.stop_reason,
                estimated_tokens=exc.estimated_tokens,
                limit=exc.limit,
            )
        except BudgetExhausted as exc:
            outcome = RunOutcome.BUDGET_STOPPED
            evidence_log.record("budget_stop", limit=exc.limit)
        except Exception as exc:  # noqa: BLE001 - surface any graph failure
            logger.exception("graph run failed for %s on %s", ticker, trade_date)
            outcome = RunOutcome.FAILED
            error = f"{type(exc).__name__}: {exc}"
            evidence_log.record("run_error", error=error)
        wall_seconds = time.time() - start

        final_state = merge_trace(trace)
        usage = budget.summary()
        usage.stop_reason = (
            ContextBudgetExceeded.stop_reason if context_stopped else budget.stop_reason()
        )

        signal = None
        if outcome == RunOutcome.COMPLETED and "final_trade_decision" in final_state:
            signal = graph.process_signal(final_state["final_trade_decision"])
            evidence_log.record("run_end", outcome="completed", signal=signal, wall_seconds=round(wall_seconds, 3))
        elif outcome == RunOutcome.BUDGET_STOPPED:
            evidence_log.record(
                "run_end",
                outcome="budget_stopped",
                note="incomplete research returned; no approvable recommendation",
            )
        else:
            evidence_log.record("run_end", outcome="failed")

        # Reports (deterministic rebuild from the final state).
        report_dir = self.settings.runs_dir / run_id / "report"
        report_files: list[str] = []
        complete_report_path: Path | None = None
        if final_state:
            try:
                complete = write_report_tree(final_state, ticker, report_dir)
                complete_report_path = complete
                report_files = [str(p) for p in report_dir.iterdir() if p.is_file()]
                report_files.append(str(complete))
            except Exception as exc:  # noqa: BLE001 - reports are best-effort
                logger.warning("report write failed: %s", exc)

        # Proposal (only a completed, tradeable signal with evidence price).
        proposal = None
        proposal_error: str | None = None
        snapshot = self._data_snapshot_from_run(final_state, frozen_snapshot)
        available_sources = self._available_sources(ticker, trade_date, frozen_identity)
        try:
            proposal = decide_proposal(
                outcome=outcome.value,
                signal=signal,
                run_id=run_id,
                ticker=ticker,
                trade_date=trade_date,
                snapshot=snapshot,
                available_sources=available_sources,
            )
        except ReviewError as exc:
            proposal_error = str(exc)
        if outcome == RunOutcome.BUDGET_STOPPED:
            proposal = None  # incomplete research must not be approvable (NFR-003)

        input_snapshot = InputSnapshot(
            instrument_context=instrument_context,
            past_context=assembly.text,
            initial_state=_trim_state(init_state),
            identity=identity,
            data_snapshot=self._data_snapshot_from_run(final_state, frozen_snapshot),
            memory_used=self._memory_entries(ticker, trade_date),
            memory_sources=["tradingagents.memory_log" if self.data_mode == "live" else "frozen-pack"],
            available_sources=available_sources,
        )

        manifest = RunManifest(
            run_id=run_id,
            ticker=ticker,
            trade_date=trade_date,
            asset_type=asset_type,
            analysts=list(self.settings.analysts),
            context_mode=self.context_mode,
            data_mode=self.data_mode,
            outcome=outcome.value,
            signal=signal,
            prompt_version=self.settings.prompt_version,
            created_at=utcnow_iso(),
            operator="research-desk",
            model_quick=self.graph_config.get("quick_think_llm"),
            model_deep=self.graph_config.get("deep_think_llm"),
            budget_max_calls=self.settings.max_calls,
            source_pack=self.source_pack.manifest.run_id if self.source_pack is not None else None,
            reason=proposal_error,
        )

        from .evidence import build_pack

        pack = build_pack(
            manifest=manifest,
            input_snapshot=input_snapshot,
            events=evidence_log.events,
            final_state=final_state,
            usage=usage,
            proposal=proposal,
            reports_written=report_files,
        )
        if complete_report_path is not None:
            apply_research_identity_header(
                complete_report_path, render_research_identity(pack)
            )
        run_dir = self.settings.runs_dir / run_id
        self.io.export(pack, run_dir)
        pack_path = str(run_dir)

        return RunResult(
            run_id=run_id,
            ticker=ticker,
            trade_date=trade_date,
            outcome=outcome.value,
            signal=signal,
            usage=usage,
            events=evidence_log.events,
            final_state=final_state,
            proposal=proposal,
            pack_path=pack_path,
            error=error,
            stop_reason=usage.stop_reason,
        )

    def _data_snapshot_from_run(
        self, final_state: dict[str, Any], frozen_snapshot: dict[str, dict[str, str]]
    ) -> dict[str, dict[str, str]]:
        """The tool-data snapshot a run consumed: frozen input plus live tool results.

        For live runs the snapshot is rebuilt from the recorded tool events so
        the evidence pack is self-contained. For frozen reruns the frozen
        snapshot is authoritative; when a fixed-CSV provider backs the run, the
        tool-data snapshot is rebuilt from the recorded tool events so the pack
        remains self-contained without an exact-args fixture.
        """
        if self.data_mode == "frozen" and self.frozen_provider is None:
            return frozen_snapshot
        from .evidence import _data_snapshot_from_events

        return _data_snapshot_from_events(getattr(self, "_run_events", []))

    def _available_sources(
        self, ticker: str, trade_date: str, frozen_identity: dict[str, Any] | None
    ) -> dict[str, Any]:
        """The factual available corpus for a frozen case, or an empty dict live."""
        if self.frozen_provider is not None:
            return _available_sources_from_provider(self.frozen_provider, ticker, trade_date)
        if self.data_mode == "frozen" and self.source_pack is not None:
            return dict(getattr(self.source_pack.input, "available_sources", None) or {})
        return {}


# Bound the initial-state copy stored in evidence: LangChain message objects are
# not JSON-serialisable, so keep the scalar fields that matter for provenance.
_SERIALISABLE_STATE_FIELDS = (
    "company_of_interest",
    "asset_type",
    "instrument_context",
    "trade_date",
    "past_context",
)


def _trim_state(state: dict[str, Any]) -> dict[str, Any]:
    return {k: state[k] for k in _SERIALISABLE_STATE_FIELDS if k in state}
