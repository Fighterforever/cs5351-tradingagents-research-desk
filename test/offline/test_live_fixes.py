"""Review-finding regression tests for the live-ready corrections.

Covers:
- Budget: a real model + structured invocation never starts request 4 at limit 3,
  and ``stop_reason`` distinguishes a genuinely blocked next call from a normal
  completion on the final allowed call (NFR-003).
- Compact delegate: ``_rebuild`` preserves ``AIMessage.tool_calls`` and keeps
  ``ToolMessage`` (and its ``tool_call_id``) instead of turning it into a
  ``SystemMessage``; a tool response required by an assistant tool call is never
  de-duplicated away (review finding #1).
- Frozen provider: real supported indicators are computed from the CSV (including
  comma-separated requests), a full-window indicator that cannot be satisfied is
  reported unavailable rather than relabelled, and company news returns the
  official case notes + source ID (review finding #3).
"""

from __future__ import annotations

import pytest

from research_desk.budget import BudgetExhausted, BudgetTracker
from research_desk.evidence import EvidenceLog, EvidenceRecorder


def test_budget_limit3_never_starts_request4_structured():
    """Through real LangChain callbacks + structured/tool invocation, limit3 -> no 4th."""
    from langchain_core.language_models.chat_models import BaseChatModel
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_core.outputs import ChatGeneration, ChatResult

    class FakeStructuredChatModel(BaseChatModel):  # noqa: D101
        response: str = "ok"

        @property
        def _llm_type(self) -> str:
            return "fake-structured"

        def _generate(self, messages, stop=None, run_manager=None, **kwargs):
            return ChatResult(generations=[ChatGeneration(message=AIMessage(content=self.response))])

        def bind_tools(self, tools, *, tool_choice=None, **kwargs):
            return self

        def with_structured_output(self, schema, *, method=None, include_raw=False, **kwargs):
            return self

    log = EvidenceLog()
    budget = BudgetTracker(max_calls=3)
    recorder = EvidenceRecorder(log, budget)
    llm = FakeStructuredChatModel()
    llm.callbacks = [recorder]

    # Structured/tool-bound invocation routes through the real model callbacks.
    structured = llm.with_structured_output(dict)

    for _ in range(3):
        structured.invoke([HumanMessage(content="hi")])
    assert budget.calls_started == 3

    with pytest.raises(BudgetExhausted):
        structured.invoke([HumanMessage(content="request number 4")])
    assert budget.calls_started == 3  # the 4th never started
    assert budget.stop_reason() == "budget_exhausted"
    requests = [e for e in log.events if e.kind == "llm_request"]
    assert len(requests) == 3


def test_budget_stop_reason_completed_on_final_allowed_call():
    """Reaching the limit on the final allowed call without a 4th attempt = completed."""
    budget = BudgetTracker(max_calls=3)
    for _ in range(3):
        budget.start_call()
    assert budget.calls_started == 3
    assert budget.stop_reason() == "completed"  # nothing was refused


def test_budget_stop_reason_exhausted_when_blocked():
    budget = BudgetTracker(max_calls=3)
    for _ in range(3):
        budget.start_call()
    with pytest.raises(BudgetExhausted):
        budget.start_call()
    assert budget.stop_reason() == "budget_exhausted"


def test_compact_rebuild_preserves_tool_calls_and_tool_message():
    """_rebuild must keep AIMessage.tool_calls and never lose ToolMessage.tool_call_id."""
    from langchain_core.messages import AIMessage, ToolMessage

    from research_desk.eval.compact_delegate import _rebuild

    aim = AIMessage(
        content="",
        tool_calls=[{"name": "get_indicators", "args": {"symbol": "NVDA", "indicator": "rsi"}, "id": "call_1", "type": "tool_call"}],
    )
    rebuilt_aim = _rebuild(aim, aim.content)
    assert rebuilt_aim.tool_calls == aim.tool_calls
    assert rebuilt_aim.tool_calls[0]["id"] == "call_1"

    tool_msg = ToolMessage(content="rsi: 58.0", tool_call_id="call_1")
    rebuilt_tool = _rebuild(tool_msg, "rsi: 58.0")
    assert isinstance(rebuilt_tool, ToolMessage)
    assert rebuilt_tool.tool_call_id == "call_1"


def test_compact_keeps_tool_response_needed_by_assistant_call():
    """A ToolMessage answering an assistant tool call is never de-duplicated away."""
    from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage

    from research_desk.eval.compact_delegate import compact_transform

    assistant = AIMessage(
        content="",
        tool_calls=[{"name": "get_indicators", "args": {"symbol": "NVDA"}, "id": "c1", "type": "tool_call"}],
    )
    tool_result = ToolMessage(content="rsi: 58.0", tool_call_id="c1")
    dup_tool_result = ToolMessage(content="rsi: 58.0", tool_call_id="c1")
    prompt = [SystemMessage(content="You are an analyst."), HumanMessage(content="Analyze NVDA."), assistant, tool_result, dup_tool_result]

    out = compact_transform(prompt, max_output_tokens=600)
    tool_msgs = [m for m in out if isinstance(m, ToolMessage)]
    # Both tool responses survive (identical content but each answers the call);
    # the assistant tool-call message survives too.
    assert len(tool_msgs) == 2
    assert all(m.tool_call_id == "c1" for m in tool_msgs)
    assert any(isinstance(m, AIMessage) and m.tool_calls for m in out)


def test_frozen_provider_indicators_from_csv():
    from research_desk.eval.frozen_provider import FrozenMarketProvider

    provider = FrozenMarketProvider("NVDA")
    out = provider.get_indicators("NVDA", "rsi", "2026-08-27", look_back_days=60)
    assert "rsi:" in out and "NO_DATA_AVAILABLE" not in out

    # Comma-separated request handled.
    multi = provider.get_indicators("NVDA", "rsi,macd,close_50_sma", "2026-08-27", look_back_days=60)
    assert "rsi:" in multi and "macd:" in multi and "close_50_sma:" in multi


def test_frozen_provider_full_window_unavailable_not_relabelled():
    """SMA200 over a short window must be unavailable, not a short-window SMA."""
    from research_desk.eval.frozen_provider import FrozenMarketProvider

    provider = FrozenMarketProvider("NVDA")
    # NVDA has 82 rows; a 200-window SMA cannot be satisfied.
    out = provider.get_indicators("NVDA", "close_200_sma", "2026-08-27", look_back_days=82)
    assert "NO_DATA_AVAILABLE" in out
    assert "window is unavailable" in out
    # RSI (14) over 30 rows is fine.
    assert "NO_DATA_AVAILABLE" not in provider.get_indicators("NVDA", "rsi", "2026-08-27", look_back_days=30)


def test_frozen_provider_unknown_indicator_unavailable():
    from research_desk.eval.frozen_provider import FrozenMarketProvider

    provider = FrozenMarketProvider("NVDA")
    out = provider.get_indicators("NVDA", "bogus_indicator", "2026-08-27", look_back_days=30)
    assert "NO_DATA_AVAILABLE" in out  # never fabricate a value for an unsupported name


def test_frozen_provider_news_returns_case_notes():
    from research_desk.eval.frozen_provider import FrozenMarketProvider

    provider = FrozenMarketProvider("NVDA")
    out = provider.get_news("NVDA")
    assert "source_id: src-nvda" in out
    assert "Revenue USD96.2 billion" in out  # official case note

    # A ticker outside the corpus stays NO_DATA.
    other = FrozenMarketProvider("NVDA")
    assert "NO_DATA_AVAILABLE" in other.get_news("TSLA")


def test_frozen_provider_symbol_date_correspondence():
    from research_desk.eval.frozen_provider import FrozenMarketProvider

    provider = FrozenMarketProvider("NVDA")
    # Wrong symbol -> unavailable, never fabricate.
    assert "NO_DATA_AVAILABLE" in provider.get_stock_data("TSLA", "2026-08-01", "2026-08-27")
    assert "NO_DATA_AVAILABLE" in provider.get_indicators("AAPL", "rsi", "2026-08-27", look_back_days=30)


def test_build_graph_no_global_patch_and_config_builds(monkeypatch):
    """Finding #2/config fix: no global ``_tg.create_llm_client`` mutation, and the
    evaluation config (built from DEFAULT_CONFIG) constructs the real graph without
    a ``KeyError: data_cache_dir``. Uses a fake non-secret token; no provider request.
    """

    from pathlib import Path

    from research_desk.eval import case_registry
    from research_desk.eval.frozen_provider import FrozenMarketProvider
    from research_desk.eval.live import _desk_settings, _graph_config
    from research_desk.graph_adapter import ResearchRunner

    monkeypatch.setenv("DEEPSEEK_API_KEY", "sk-fake-non-secret-token")
    home = Path("/tmp/rd-graph-smoke-home")

    cfg = _graph_config(home, None)
    # The config must declare the fields the upstream graph reads directly.
    assert "data_cache_dir" in cfg and "results_dir" in cfg and "memory_log_path" in cfg
    assert home / "cache" == Path(cfg["data_cache_dir"])
    assert home / "memory" / "trading_memory.md" == Path(cfg["memory_log_path"])

    # Constructing the real graph must succeed (no KeyError) with a frozen
    # provider and a fake key — no network is touched at construction.
    import tradingagents.graph.trading_graph as _tg

    orig = _tg.create_llm_client
    from research_desk.budget import BudgetTracker
    from research_desk.evidence import EvidenceLog, EvidenceRecorder

    provider = FrozenMarketProvider("NVDA", case_registry.MARKET_DIR / "NVDA.csv")
    settings = _desk_settings(home, None)
    runner = ResearchRunner(
        settings,
        context_mode="baseline",
        data_mode="frozen",
        frozen_provider=provider,
        graph_config=cfg,
    )
    recorder = EvidenceRecorder(EvidenceLog(), BudgetTracker(max_calls=None))
    graph = runner._build_graph(cfg, recorder, None, frozen_snapshot={}, frozen_identity=provider.identity)

    assert _tg.create_llm_client is orig  # no global monkeypatch
    assert graph.graph is not None  # the real compiled graph
    assert Path(cfg["data_cache_dir"]).exists()  # created by the graph __init__

def test_price_from_available_sources_no_stock_data():
    """Finding #2: price remains derivable even when no get_stock_data was called."""
    from research_desk.eval import case_registry
    from research_desk.eval.frozen_provider import FrozenMarketProvider
    from research_desk.graph_adapter import _available_sources_from_provider, price_from_evidence

    provider = FrozenMarketProvider("AAPL", case_registry.MARKET_DIR / "AAPL.csv")
    case = provider.case
    trade_date = case["analysis_date"]
    available = _available_sources_from_provider(provider, "AAPL", trade_date)
    # No observed tool results at all.
    assert price_from_evidence({}, "AAPL", available_sources=available) is not None
    # The available corpus price equals the case latest close (from the real CSV).
    observed_price = price_from_evidence(
        {"get_verified_market_snapshot": {"v": f"# Verified market snapshot\nlast_close: {case['latest_close']:.2f}\n"}},
        "AAPL",
    )
    assert observed_price is not None
    assert round(observed_price, 2) == round(float(case["latest_close"]), 2)


def test_decide_proposal_uses_available_corpus_price():
    """A completed Buy with no get_stock_data still yields a proposal via the corpus."""
    from research_desk.eval import case_registry
    from research_desk.eval.frozen_provider import FrozenMarketProvider
    from research_desk.graph_adapter import _available_sources_from_provider, decide_proposal

    provider = FrozenMarketProvider("AAPL", case_registry.MARKET_DIR / "AAPL.csv")
    case = provider.case
    trade_date = case["analysis_date"]
    available = _available_sources_from_provider(provider, "AAPL", trade_date)
    p = decide_proposal(
        outcome="completed", signal="Buy", run_id="r", ticker="AAPL",
        trade_date=trade_date, snapshot={}, available_sources=available,
    )
    assert p is not None and p.price is not None


def test_frozen_provider_identity_no_online_fallback(monkeypatch):
    """Finding #1: frozen resolve uses the provider identity, never online resolve."""
    from research_desk.eval import case_registry
    from research_desk.eval.frozen_provider import FrozenMarketProvider
    from research_desk.graph_adapter import EvidenceTradingGraph

    called = {"online": False}
    provider = FrozenMarketProvider("MSFT", case_registry.MARKET_DIR / "MSFT.csv")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-fake-non-secret")  # construct graph offline

    def fake_resolve_identity(_ticker):
        called["online"] = True
        return {"company_name": "ONLINE-ONLY"}

    monkeypatch.setattr("research_desk.graph_adapter.resolve_instrument_identity", fake_resolve_identity)
    from tradingagents.default_config import DEFAULT_CONFIG

    cfg = DEFAULT_CONFIG.copy()
    cfg["data_cache_dir"] = "/tmp/rd-identity-cache"
    cfg["results_dir"] = "/tmp/rd-identity-results"
    graph = EvidenceTradingGraph(
        selected_analysts=("market",),
        config=cfg,
        data_mode="frozen",
        frozen_identity=None,  # not supplied -> must fall back to provider identity
        frozen_provider=provider,
    )
    ctx = graph.resolve_instrument_context("MSFT", "stock")
    assert called["online"] is False  # no hidden online identity request
    assert "Microsoft Corporation" in ctx


def test_valid_citation_rate_zero_denominator_not_pass():
    from research_desk.eval.live import _valid_citation_rate

    assert _valid_citation_rate(0, 0) is None  # denominator 0 is not an auto pass
    assert _valid_citation_rate(4, 3) == 0.75
    assert _valid_citation_rate(4, 4) == 1.0


def test_judge_raw_persists_tool_call_message(monkeypatch):
    """Finding #5: raw judge output keeps the full AIMessage incl. tool_calls."""
    from langchain_core.messages import AIMessage

    from research_desk.eval.live import _llm_judge

    class _Parsed:
        support = 0.8
        relevance = 0.9
        cited_claim_count = 4
        supported_cited_claim_count = 3
        invalid_citation_explanations = ["src-aapl does not back claim X"]
        uncited_factual_claims = ["Revenue grew 10%"]
        rationale = "solid"

    class _FakeLLM:
        def __init__(self):
            self.extra_body = None

        def with_structured_output(self, schema, include_raw=False):
            def invoke(_prompt):
                msg = AIMessage(
                    content="",
                    tool_calls=[
                        {"name": "the_tool", "args": {"support": 0.8}, "id": "c1", "type": "tool_call"}
                    ],
                )
                msg.usage_metadata = {"input_tokens": 100, "output_tokens": 20, "total_tokens": 120}
                return {"raw": msg, "parsed": _Parsed(), "parsing_error": None}
            return type("SO", (), {"invoke": staticmethod(invoke)})()

    class _FakeClient:
        def get_llm(self):
            return _FakeLLM()

    monkeypatch.setattr("tradingagents.llm_clients.create_llm_client", lambda *a, **k: _FakeClient())

    raw, score = _llm_judge(
        {"ticker": "AAPL", "analysis_date": "2026-07-31", "latest_close": 308.91, "source_id": "src-aapl", "notes": ["n"]},
        "report text", [{"check": "x", "passed": True, "detail": "d"}],
        available_sources={}, data_snapshot={},
    )
    # Full raw message with tool_calls preserved (content may be empty).
    assert raw["raw_message"]["tool_calls"][0]["name"] == "the_tool"
    assert raw["usage"]["input_tokens"] == 100
    assert score["valid_citation_rate"] == 0.75
    assert score["error"] is False
    assert score["deterministic_checks"][0]["check"] == "x"
