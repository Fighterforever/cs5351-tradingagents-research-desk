"""Live evaluation entry points: ``evaluate-case``, ``judge-case``, ``aggregate``.

These are the real runnable application boundary for the frozen six-case
comparison (AT-07 / FR-003 / QUALITY-001..003 / COST-001 / PERF-001):

- ``run_evaluate_case`` runs ``ResearchRunner`` against the real
  ``TradingAgentsGraph`` with real DeepSeek clients on the frozen CSV + case
  notes for one case in one context mode (baseline/compact). It saves the exact
  config, the full evidence pack (raw prompts/responses/tools/usage/events,
  final state, reports), the measured wall time and the outcome.
- ``run_judge_case`` uses the real DeepSeek client as an *isolated evaluator*
  (separate role, fixed evidence and rubric, no baseline/compact identity) to
  score a completed run's report, plus deterministic identity/date/price/state
  and source-ID checks. Raw judge response and usage are recorded separately.
- ``run_aggregate`` reads existing output directories and computes six paired
  (baseline vs compact) metrics without calling any model again.

Only host credentials are used: ``DEEPSEEK_API_KEY`` and optional
``DEEPSEEK_BASE_URL`` (default ``https://api.aiohub.org/v1``). Each run uses an
isolated home directory. A completed or
failed outcome means the actual graph outcome; a failed setup is never reported
as completed.
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, model_validator

from ..config import DEFAULT_BASE_URL, DEFAULT_MODEL, DEFAULT_PROVIDER
from .case_registry import case_for
from .frozen_provider import FrozenMarketProvider

logger = logging.getLogger(__name__)

MODEL = DEFAULT_MODEL
PROVIDER = DEFAULT_PROVIDER
OUTPUT_CAP = 1800  # provider max_tokens cap, identical for both arms
PROVENANCE_FILENAME = "provenance.json"


def _base_url() -> str:
    """Host-supplied endpoint override, otherwise the authoritative default."""
    return os.environ.get("DEEPSEEK_BASE_URL") or DEFAULT_BASE_URL


def _project_root() -> Path:
    """Repository root (this module lives in ``src/research_desk/eval``)."""
    return Path(__file__).resolve().parents[3]


def _current_source_fingerprint(root: Path) -> str:
    """Current runtime source fingerprint from the release-quality contract."""
    from .quality import source_fingerprint

    return source_fingerprint(root)


def _provenance_payload(
    fingerprint: str, cfg: dict[str, Any], base_url: str
) -> dict[str, Any]:
    """Provenance record bound to the actual model/provider/endpoint/config."""
    return {
        "source_fingerprint": fingerprint,
        "model": cfg.get("quick_think_llm") or MODEL,
        "provider": cfg.get("llm_provider") or PROVIDER,
        "endpoint": base_url,
        "deep_think_llm": cfg.get("deep_think_llm") or MODEL,
        "max_tokens": cfg.get("max_tokens"),
        "temperature": cfg.get("temperature"),
    }


def _read_source_fingerprint(path: Path) -> str | None:
    """Read a saved provenance source fingerprint, or None if absent/invalid."""
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(data, dict):
        return None
    value = data.get("source_fingerprint")
    return value if isinstance(value, str) else None


# Verified AioHub deepseek-flash endpoint contract: ``thinking={"type":
# "disabled"}`` alone is ignored and the model still emits reasoning, while
# adding ``reasoning_effort="none"`` yields zero reasoning. Both keys travel as
# ``extra_body`` (never top-level) because the upstream factory filters a
# top-level ``reasoning_effort`` for DeepSeek; this gives the graph models and
# the isolated judge the same effective non-thinking setting.
THINKING_DISABLED_EXTRA_BODY = {
    "thinking": {"type": "disabled"},
    "reasoning_effort": "none",
}


def _graph_config(home: Path, base_url: str | None) -> dict[str, Any]:
    """Build the evaluation graph config from the real DEFAULT_CONFIG.

    The upstream graph treats the supplied dict as complete, so we start from a
    deep copy of ``DEFAULT_CONFIG`` (which declares ``data_cache_dir``,
    ``results_dir`` and ``memory_log_path``) and then override the explicit
    model/settings. The path fields are pointed inside the arm's isolated home
    so both arms' effective settings are identical and each run stays isolated.
    """
    from copy import deepcopy

    from tradingagents.default_config import DEFAULT_CONFIG

    cfg = deepcopy(DEFAULT_CONFIG)
    cfg.update(
        {
            "llm_provider": PROVIDER,
            "quick_think_llm": MODEL,
            "deep_think_llm": MODEL,
            "max_tokens": OUTPUT_CAP,
            "temperature": 0,
            "llm_max_retries": 2,
            "max_debate_rounds": 1,
            "max_risk_discuss_rounds": 1,
            "extra_body": THINKING_DISABLED_EXTRA_BODY,
            "checkpoint_enabled": False,
            "results_dir": str(home / "logs"),
            "data_cache_dir": str(home / "cache"),
            "memory_log_path": str(home / "memory" / "trading_memory.md"),
        }
    )
    cfg["backend_url"] = base_url or DEFAULT_BASE_URL
    return cfg


def _desk_settings(home: Path, max_calls: int | None):
    from research_desk.config import ResearchDeskSettings

    s = ResearchDeskSettings(home=str(home))
    s.analysts = ("market", "news")
    s.max_calls = max_calls
    s.ensure_dirs()
    return s


def _dump_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")


def run_evaluate_case(
    ticker: str,
    context_mode: str,
    out_dir: str | Path,
    max_calls: int | None = None,
) -> dict[str, Any]:
    """Run one frozen case in one mode; write config/evidence/summary/report."""
    from research_desk.graph_adapter import ResearchRunner
    from research_desk.report import render_run_report

    ticker = ticker.upper()
    if context_mode not in ("baseline", "compact"):
        raise ValueError(f"mode must be baseline|compact, got {context_mode!r}")
    case = case_for(ticker)
    out = Path(out_dir)
    arm_dir = out / ticker / context_mode
    arm_dir.mkdir(parents=True, exist_ok=True)

    base_url = _base_url()
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError(
            "DEEPSEEK_API_KEY is not set. Supply it as a host environment variable."
        )

    provider = FrozenMarketProvider(ticker)
    # Isolated home for this run; the evidence pack is exported under it and all
    # graph paths (cache/results/memory) are pointed inside it.
    home = arm_dir / ".home"
    cfg = _graph_config(home, base_url)
    settings = _desk_settings(home, max_calls)

    _dump_json(arm_dir / "config.json", cfg)
    _dump_json(arm_dir / "case.json", case)

    runner = ResearchRunner(
        settings,
        context_mode=context_mode,
        data_mode="frozen",
        frozen_provider=provider,
        graph_config=cfg,
    )

    root = _project_root()
    source_before = _current_source_fingerprint(root)
    _dump_json(
        arm_dir / PROVENANCE_FILENAME,
        _provenance_payload(source_before, cfg, base_url),
    )

    start = time.time()
    result = runner.run(ticker, case["analysis_date"])
    wall_seconds = time.time() - start
    source_after = _current_source_fingerprint(root)
    source_changed = source_after != source_before

    # The pack is exported by the runner under the isolated home; relocate the
    # whole run directory into the arm dir for stable aggregate/export paths.
    run_dir = Path(result.pack_path) if result.pack_path else None
    dest = arm_dir / "run"
    if run_dir is not None and run_dir.exists():
        _replace_dir(run_dir, dest)

    pack = None
    from research_desk.evidence import EvidencePackIO

    try:
        pack = EvidencePackIO().import_pack(dest)
    except Exception as exc:  # noqa: BLE001 - record import failure, keep going
        logger.warning("failed to import relocated pack %s: %s", dest, exc)

    summary = {
        "ticker": ticker,
        "analysis_date": case["analysis_date"],
        "context_mode": context_mode,
        "outcome": result.outcome,
        "signal": result.signal,
        "stop_reason": result.stop_reason,
        "calls": result.usage.calls,
        "input_tokens": result.usage.input_tokens,
        "output_tokens": result.usage.output_tokens,
        "total_tokens": result.usage.total_tokens,
        "wall_seconds": round(wall_seconds, 3),
        "error": result.error,
        "pack_complete": pack.complete if pack is not None else False,
        "run_dir": str(dest),
    }
    if source_changed:
        summary["source_changed"] = True
        summary["error"] = (
            "source changed during run; refusing to certify evidence "
            f"({source_before} != {source_after})"
        )
    _dump_json(arm_dir / "summary.json", summary)
    if pack is not None:
        (arm_dir / "report.md").write_text(render_run_report(pack), encoding="utf-8")
    if source_changed:
        raise RuntimeError(summary["error"])
    return summary


def _replace_dir(src: Path, dest: Path) -> None:
    """Move ``src`` to ``dest`` (overwriting any previous dest)."""
    import shutil

    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dest))


# ---------------------------------------------------------------------------
# judge
# ---------------------------------------------------------------------------


# A monetary number token in ordinary report formatting: optional ``$``/spaces,
# an explicit sign, US thousands separators, and a decimal fraction. Ungrouped
# integers of any length match, correctly grouped comma amounts match, and the
# sign stays part of the numeric value so ``-451.10`` is never read as
# ``451.10``. The boundaries reject a digit/comma/dot directly before and a
# digit directly after, so the match is never a substring of a larger number
# like ``1451.10`` for an expected ``451.10``.
_PRICE_TOKEN_RE = re.compile(
    r"(?<![\d.,])\$?\s*[+-]?\s*(?:\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)(?!\d)"
)


def _normalize_number_token(token: str) -> Decimal | None:
    """Parse a matched number token (``$``/commas removed, sign kept) into a Decimal."""
    cleaned = token.replace(",", "").replace("$", "").strip()
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


def _contains_price(text: str, expected_close: float) -> bool:
    """True when ``text`` states the expected close as its own number token.

    Ordinary formatting is normalized ($451.10, 451.1, comma thousands, trailing
    zeros), so the check accepts exactly the expected numerical value and never
    a different number or a substring of a larger number.
    """
    expected = Decimal(f"{expected_close:.2f}")
    for match in _PRICE_TOKEN_RE.finditer(text):
        value = _normalize_number_token(match.group(0))
        if value is not None and value == expected:
            return True
    return False


def _report_text(final_state: dict[str, Any]) -> str:
    """Assemble the material report text a run actually produced.

    Stages keep their authentic upstream role titles (``reporting.py``) so the
    independent judge can distinguish intermediate proposals (bull/bear, research
    manager, trader, risk analysts) from the final portfolio decision. The
    Portfolio Manager node writes the same string to both
    ``risk_debate_state.judge_decision`` and ``final_trade_decision``; when they
    are exactly equal after whitespace stripping, the identical content is
    included once as the final decision. Raw model text is preserved; no
    different or contrary stage is removed.
    """
    parts: list[str] = []

    def _add(title: str, value: Any) -> None:
        if isinstance(value, str) and value.strip():
            parts.append(f"## {title}\n{value.strip()}")

    for key, title in (
        ("market_report", "Market Analyst"),
        ("news_report", "News Analyst"),
        ("sentiment_report", "Sentiment Analyst"),
        ("fundamentals_report", "Fundamentals Analyst"),
    ):
        _add(title, final_state.get(key))

    debate = final_state.get("investment_debate_state")
    if isinstance(debate, dict):
        _add("Bull Researcher", debate.get("bull_history"))
        _add("Bear Researcher", debate.get("bear_history"))
        _add("Research Manager", debate.get("judge_decision"))

    _add("Trader", final_state.get("trader_investment_plan"))

    risk_judge: str | None = None
    risk = final_state.get("risk_debate_state")
    if isinstance(risk, dict):
        _add("Aggressive Analyst", risk.get("aggressive_history"))
        _add("Conservative Analyst", risk.get("conservative_history"))
        _add("Neutral Analyst", risk.get("neutral_history"))
        judge = risk.get("judge_decision")
        if isinstance(judge, str) and judge.strip():
            risk_judge = judge.strip()

    final = final_state.get("final_trade_decision")
    final = final.strip() if isinstance(final, str) and final.strip() else None

    if risk_judge is not None and final is not None and risk_judge == final:
        _add("Final Portfolio Decision", final)
    else:
        _add("Portfolio Manager", risk_judge)
        _add("Final Portfolio Decision", final)

    return "\n\n".join(parts)


def _report_text_with_identity(pack) -> str:
    """The judge input: the shared deterministic header plus raw generated text."""
    from research_desk.report import render_research_identity

    return render_research_identity(pack) + "\n\n" + _report_text(pack.final_state)


def _deterministic_checks(case: dict, pack, ticker: str) -> list[dict[str, Any]]:
    """Deterministic identity/date/price/state and source-ID checks (QUALITY-001)."""
    checks: list[dict[str, Any]] = []
    fs = pack.final_state if pack is not None else {}
    text = _report_text(fs)

    from research_desk.report import render_research_identity

    # Identity/date are presentation-contract checks over the same deterministic
    # header the user-visible report and judge input carry. The raw narrative
    # price check below stays independent and stronger.
    contract_text = render_research_identity(pack) if pack is not None else ""

    def check(name: str, passed: bool, detail: str) -> None:
        checks.append({"check": name, "passed": passed, "detail": detail})

    expected_company = case.get("identity", {}).get("company_name", "")
    check(
        "instrument_identity",
        bool(expected_company) and expected_company.lower() in contract_text.lower(),
        f"report contract references company '{expected_company}'",
    )
    check(
        "analysis_date",
        case["analysis_date"] in contract_text,
        f"report contract references analysis date {case['analysis_date']}",
    )
    check("final_decision_present", bool(fs.get("final_trade_decision")),
          "final trade decision is present in the final state")
    # Price must be supported by evidence (observed tool result or the factual
    # available corpus), never fabricated, AND the report itself must state the
    # expected close. Case metadata alone is not output evidence.
    expected_close = case["latest_close"]
    evidence_supports_price = False
    if pack is not None:
        for bucket in pack.input.data_snapshot.values():
            for res in bucket.values():
                if isinstance(res, str) and _contains_price(res, expected_close):
                    evidence_supports_price = True
        avail = pack.input.available_sources or {}
        for source in (avail.get("market"), avail.get("verified_snapshot")):
            if isinstance(source, str) and _contains_price(source, expected_close):
                evidence_supports_price = True
    reported_price = _contains_price(text, expected_close)
    check(
        "frozen_price_in_report",
        evidence_supports_price and reported_price,
        f"frozen latest close {expected_close:.2f} is supported by evidence and stated in the report",
    )
    source_id = case.get("source_id", "")
    check("source_id_referenced", bool(source_id) and source_id in text,
          f"report references source_id '{source_id}'")
    return checks


def run_judge_case(
    ticker: str,
    out_dir: str | Path,
    max_calls: int | None = None,
) -> dict[str, Any]:
    """Judge a completed run's report with a real isolated DeepSeek evaluator.

    Deterministic checks are computed first. Then the real DeepSeek client
    (same model, separate role, fixed evidence and rubric) scores support,
    relevance and citations with a structured rationale. Raw response and usage
    are recorded separately. A score is never auto-assigned for nonempty text.
    """
    from research_desk.evidence import EvidencePackIO

    ticker = ticker.upper()
    if not os.environ.get("DEEPSEEK_API_KEY"):
        raise RuntimeError(
            "DEEPSEEK_API_KEY is not set. Supply it as a host environment variable."
        )
    case = case_for(ticker)
    out = Path(out_dir)
    root = _project_root()
    judged: dict[str, Any] = {"ticker": ticker, "arms": {}}
    source_failure = False
    for mode in ("baseline", "compact"):
        run_dir = out / ticker / mode / "run"
        if not run_dir.exists():
            continue
        current = _current_source_fingerprint(root)
        run_fingerprint = _read_source_fingerprint(
            out / ticker / mode / PROVENANCE_FILENAME
        )
        if run_fingerprint is None:
            judged["arms"][mode] = {
                "error": "run provenance missing; refusing to judge",
            }
            source_failure = True
            continue
        if run_fingerprint != current:
            judged["arms"][mode] = {
                "error": "run provenance is stale; refusing to judge",
                "run_source_fingerprint": run_fingerprint,
                "current_source_fingerprint": current,
            }
            source_failure = True
            continue
        try:
            pack = EvidencePackIO().import_pack(run_dir)
        except Exception as exc:  # noqa: BLE001
            logger.warning("cannot import run for %s/%s: %s", ticker, mode, exc)
            judged["arms"][mode] = {"error": str(exc)}
            continue
        if pack.manifest.outcome != "completed" or not pack.final_state:
            judged["arms"][mode] = {
                "outcome": pack.manifest.outcome,
                "note": "skipped judge: run not completed",
            }
            continue
        report_text = _report_text_with_identity(pack)
        deterministic = _deterministic_checks(case, pack, ticker)
        judge_cfg = {
            "llm_provider": PROVIDER,
            "quick_think_llm": MODEL,
            "deep_think_llm": MODEL,
            "max_tokens": OUTPUT_CAP,
            "temperature": 0,
        }
        arm_judge_dir = out / "judge" / ticker / mode
        arm_judge_dir.mkdir(parents=True, exist_ok=True)
        _dump_json(
            arm_judge_dir / PROVENANCE_FILENAME,
            _provenance_payload(current, judge_cfg, _base_url()),
        )
        raw, score = _llm_judge(
            case,
            report_text,
            deterministic,
            available_sources=pack.input.available_sources or {},
            events=pack.events,
        )
        source_after = _current_source_fingerprint(root)
        if source_after != current:
            judged["arms"][mode] = {
                "error": "source changed during judge; refusing to certify",
                "judge_source_fingerprint": current,
                "current_source_fingerprint": source_after,
            }
            source_failure = True
            continue
        _dump_json(arm_judge_dir / "raw.json", raw)
        _dump_json(arm_judge_dir / "judge.json", score)
        judged["arms"][mode] = score
    _dump_json(out / "judge" / ticker / "summary.json", judged)
    if source_failure:
        raise RuntimeError(
            "source provenance missing or changed; refusing to certify judge results"
        )
    return judged


def _observed_tools_text(events) -> str:
    """Every actual ``tool_result`` payload in the event log, in event order.

    ``input.data_snapshot`` is a lossy fallback projection keyed by tool
    arguments and keeps only the last output for a repeated tool name, so the
    judge reads the authoritative event log instead. Each output keeps its
    tool/source name and event sequence; an exact duplicate (same tool, same
    result) is not repeated, but different results from the same tool survive.
    """
    lines: list[str] = []
    seen: set[tuple[str, str]] = set()
    for ev in events:
        if getattr(ev, "kind", None) != "tool_result":
            continue
        payload = getattr(ev, "payload", None) or {}
        name = payload.get("name") or "unknown"
        result = payload.get("result")
        if not isinstance(result, str) or not result.strip():
            continue
        if (name, result) in seen:
            continue
        seen.add((name, result))
        lines.append(f"## observed tool output: {name} (event {getattr(ev, 'seq', '?')})")
        lines.append(result)
    return "\n".join(lines)


def _judge_prompt(
    case: dict,
    report_text: str,
    deterministic: list[dict],
    available_sources: dict[str, Any],
    events,
) -> str:
    """Build the judge prompt from the *actual* frozen evidence captured in this pack.

    Supplies the official earnings notes, the fixed ticker/date/identity and
    source IDs, plus the real market evidence (market CSV, verified snapshot and
    official news) and every observed tool result recorded in the event log — so
    the judge can validate technical/history claims in the report. No
    baseline/compact identity is revealed.
    """
    identity = available_sources.get("identity") or case.get("identity", {})
    notes = "\n".join(f"- {n}" for n in case.get("notes", []))
    facts = "\n".join(
        f"- {c['check']}: {'PASS' if c['passed'] else 'FAIL'} ({c['detail']})"
        for c in deterministic
    )
    market_evidence = str(available_sources.get("market", "")).strip()
    verified = str(available_sources.get("verified_snapshot", "")).strip()
    news = str(available_sources.get("news", "")).strip()
    observed = _observed_tools_text(events).strip()

    return f"""You are an independent equity-research evaluator (a separate role from the analyst). You are judging a single research report for a single equity case. You have no knowledge of which context configuration produced it.

FIXED CASE (identity, do not contest):
- ticker: {case['ticker']}
- company: {identity.get('company_name', '')}
- analysis date: {case['analysis_date']}
- source_id: {case.get('source_id', 'n/a')}
- official source URL: {case.get('source_url', 'n/a')}

Official earnings notes (frozen source):
{notes}

Frozen latest close (from the actual market CSV): {case['latest_close']:.2f}

Market evidence captured in this pack (actual frozen market data this run had available):
{market_evidence or '(none present)'}

Verified market snapshot captured in this pack:
{verified or '(none present)'}

Company news captured in this pack (official source):
{news or '(none present)'}

Observed tool outputs this report's run actually retrieved:
{observed or '(none present)'}

Deterministic checks already computed against the report:
{facts}

Judge the report below. Score support and relevance on 0-1 using the rubric:
- support 1.0 = every key conclusion has direct support from the evidence; 0.8 = main conclusions supported with no key fabrication; 0.5 = important evidence gaps; 0 = key factual fabrication.
- relevance 1.0 = fully focused on the requested ticker/date/task; 0.8 = core complete with minor redundancy; 0.5 = missing key parts; 0 = off task.

Citation accounting (count factual claims that carry a source citation):
- cited_claim_count = number of factual claims that cite a source ID.
- supported_cited_claim_count = number of those cited claims whose cited source ID is present AND actually supports that particular claim. A source ID merely existing is NOT support; it must back the specific claim.
- invalid_citation_explanations = for each cited claim whose citation does not support it, explain why.
- uncited_factual_claims = factual claims (numbers/dates/identity/price) made with no supporting source ID.
Do NOT give 1.0 just because the report is nonempty.

Semantic validity (dedicated condition):
- semantic_valid = true only when every earnings-period and unit statement is correct. A quarterly EPS is never described as trailing-twelve-month (TTM) or annual EPS, and a trailing P/E or other trailing ratio is computed only from actual TTM EPS evidence.
- Set semantic_valid = false if the report converts or relabels a single-quarter figure as TTM/annual, computes a trailing P/E from quarterly EPS, or makes a key numerical valuation assertion unsupported by the evidence. Valid citation IDs do NOT rescue a wrong period/unit or an unsupported numerical claim.
- semantic_errors = concise explanations of each period/unit error or unsupported numerical valuation claim. Any non-empty semantic_errors list must accompany semantic_valid = false.

Presentation contract:
- The first section is a deterministic identity/date/evidence-price header rendered from the evidence pack. It is a presentation contract, not model reasoning.
- A correct header does NOT excuse a contradictory price or identity in the raw reasoning, nor a wrong earnings period or unit. Judge the generated narrative independently.

REPORT:
{report_text}
"""


def _valid_citation_rate(cited: int, supported: int) -> float | None:
    """Supported-cited fraction; a zero denominator is NOT an automatic pass."""
    if cited <= 0:
        return None
    return round(supported / cited, 4)


class JudgeScore(BaseModel):
    """Structured judge output, including the dedicated semantic validity gate.

    ``semantic_valid`` defaults to ``False`` when a legacy or incomplete judge
    response omits it, so absence can never be read as a pass. Any recorded
    semantic error also forces it to ``False`` regardless of citation counts.
    """

    support: float = Field(..., ge=0, le=1)
    relevance: float = Field(..., ge=0, le=1)
    cited_claim_count: int = Field(..., ge=0)
    supported_cited_claim_count: int = Field(..., ge=0)
    invalid_citation_explanations: list[str] = Field(default_factory=list)
    uncited_factual_claims: list[str] = Field(default_factory=list)
    semantic_valid: bool = Field(
        default=False,
        description=(
            "True only when earnings periods/units are correct and no key numerical "
            "valuation assertion is unsupported by the evidence."
        ),
    )
    semantic_errors: list[str] = Field(default_factory=list)
    rationale: str = ""

    @model_validator(mode="after")
    def _supported_within_cited(self):
        if self.supported_cited_claim_count > self.cited_claim_count:
            raise ValueError(
                "supported_cited_claim_count cannot exceed cited_claim_count"
            )
        return self

    @model_validator(mode="after")
    def _semantic_errors_invalidate(self):
        if self.semantic_errors:
            self.semantic_valid = False
        return self


def _llm_judge(
    case: dict,
    report_text: str,
    deterministic: list[dict],
    *,
    available_sources: dict[str, Any],
    events,
):
    """Run the real DeepSeek evaluator; returns (raw, score) without fabrication."""
    from tradingagents.llm_clients import create_llm_client

    client = create_llm_client(
        PROVIDER,
        MODEL,
        base_url=_base_url(),
        max_tokens=OUTPUT_CAP,
        temperature=0,
    )
    llm = client.get_llm()
    if hasattr(llm, "extra_body"):
        llm.extra_body = dict(THINKING_DISABLED_EXTRA_BODY)

    prompt = _judge_prompt(case, report_text, deterministic, available_sources, events)
    structured = llm.with_structured_output(JudgeScore, include_raw=True)
    try:
        raw_out = structured.invoke(prompt)
    except Exception as exc:  # noqa: BLE001 - surface judge failures visibly
        raw_failed: dict[str, Any] = {"prompt": prompt, "invoke_error": str(exc), "usage": {}}
        score: dict[str, Any] = {
            "support": None,
            "relevance": None,
            "cited_claim_count": 0,
            "supported_cited_claim_count": 0,
            "valid_citation_rate": None,
            "invalid_citation_explanations": [],
            "uncited_factual_claims": [],
            "semantic_valid": False,
            "semantic_errors": [],
            "rationale": f"judge invoke failed: {exc}",
            "error": True,
            "deterministic_checks": deterministic,
        }
        return raw_failed, score

    raw_resp = raw_out.get("raw", None)
    parsed = raw_out.get("parsed", None)
    parsing_error = raw_out.get("parsing_error", None)
    usage: dict[str, Any] = {}
    if hasattr(raw_resp, "usage_metadata"):
        usage = dict(raw_resp.usage_metadata or {}) if raw_resp.usage_metadata else {}

    # Full raw message: tool-call responses often carry content='' with the
    # answer in tool_calls, so persist the complete message, not just text.
    raw_msg_json: Any = None
    if raw_resp is not None:
        try:
            raw_msg_json = raw_resp.model_dump()
        except Exception:  # noqa: BLE001
            raw_msg_json = {"content": getattr(raw_resp, "content", None)}

    if parsed is None:
        score = {
            "support": None,
            "relevance": None,
            "cited_claim_count": 0,
            "supported_cited_claim_count": 0,
            "valid_citation_rate": None,
            "invalid_citation_explanations": [],
            "uncited_factual_claims": [],
            "semantic_valid": False,
            "semantic_errors": [],
            "rationale": (
                "judge returned no parseable structured score"
                + (f": {parsing_error}" if parsing_error else "")
            ),
            "error": True,
            "parse_error": str(parsing_error) if parsing_error else None,
            "deterministic_checks": deterministic,
        }
    else:
        cited = int(parsed.cited_claim_count)
        supported = int(parsed.supported_cited_claim_count)
        valid_citation_rate = _valid_citation_rate(cited, supported)
        semantic_errors = list(getattr(parsed, "semantic_errors", []) or [])
        semantic_valid = bool(getattr(parsed, "semantic_valid", False))
        if semantic_errors:
            semantic_valid = False  # a recorded semantic defect cannot pass
        score = {
            "support": float(parsed.support),
            "relevance": float(parsed.relevance),
            "cited_claim_count": cited,
            "supported_cited_claim_count": supported,
            "valid_citation_rate": valid_citation_rate,
            "invalid_citation_explanations": list(parsed.invalid_citation_explanations),
            "uncited_factual_claims": list(parsed.uncited_factual_claims),
            "semantic_valid": semantic_valid,
            "semantic_errors": semantic_errors,
            "rationale": parsed.rationale,
            "error": False,
            "deterministic_checks": deterministic,
        }
    raw: dict[str, Any] = {
        "prompt": prompt,
        "raw_message": raw_msg_json,
        "response_text": getattr(raw_resp, "content", None) if raw_resp is not None else None,
        "usage": usage,
        "parse_error": str(parsing_error) if parsing_error else None,
    }
    return raw, score


# ---------------------------------------------------------------------------
# aggregate
# ---------------------------------------------------------------------------


def run_aggregate(root: str | Path) -> dict[str, Any]:
    """Compute six paired baseline/compact metrics from existing run dirs.

    No model is called. Completed arms are included; a missing or non-completed
    arm is recorded as such. Judge scores, when present, are attached separately.
    """
    root = Path(root)
    cases = [c for c in (root.iterdir() if root.exists() else []) if c.is_dir()]
    paired: list[dict[str, Any]] = []
    for case_dir in sorted(cases):
        ticker = case_dir.name
        arms = {}
        for mode in ("baseline", "compact"):
            summary = case_dir / mode / "summary.json"
            if not summary.exists():
                arms[mode] = {"present": False}
                continue
            data = json.loads(summary.read_text(encoding="utf-8"))
            data["present"] = True
            judge_file = root / "judge" / ticker / mode / "judge.json"
            if judge_file.exists():
                data["judge"] = json.loads(judge_file.read_text(encoding="utf-8"))
            arms[mode] = data
        if not arms.get("baseline", {}).get("present") and not arms.get("compact", {}).get("present"):
            continue
        paired.append({"ticker": ticker, "baseline": arms.get("baseline"), "compact": arms.get("compact")})
    report = _aggregate_report(paired)
    _dump_json(root / "aggregate" / "summary.json", {"paired": paired})
    (root / "aggregate" / "report.md").write_text(report, encoding="utf-8")
    return {"paired": paired, "report": report}


def _arm_value(arm: dict | None, key: str, default=None):
    if arm is None or not arm.get("present"):
        return default
    return arm.get(key, default)


def _aggregate_report(paired: list[dict]) -> str:
    lines = [
        "# Baseline / Compact Aggregate (six paired metrics)",
        "",
        "Read from existing run outputs; no model calls. Judge scores are attached when present.",
        "",
        "| ticker | metric | baseline | compact | delta |",
        "|---|---|---|---|---|",
    ]
    metrics = [
        ("calls", "{:.0f}"),
        ("input_tokens", "{:.0f}"),
        ("output_tokens", "{:.0f}"),
        ("total_tokens", "{:.0f}"),
        ("wall_seconds", "{:.1f}"),
        ("outcome", "{!s}"),
    ]
    for p in paired:
        t = p["ticker"]
        for key, fmt in metrics:
            b = _arm_value(p.get("baseline"), key)
            c = _arm_value(p.get("compact"), key)
            b_s = "n/a" if b is None else fmt.format(b)
            c_s = "n/a" if c is None else fmt.format(c)
            delta = "—"
            if isinstance(b, (int, float)) and isinstance(c, (int, float)):
                delta = _pct(b, c)
            lines.append(f"| {t} | {key} | {b_s} | {c_s} | {delta} |")
    for p in paired:
        for mode in ("baseline", "compact"):
            judge = _arm_value(p.get(mode), "judge")
            if isinstance(judge, dict) and not judge.get("error") and judge.get("support") is not None:
                lines.append(
                    f"| {p['ticker']} | {mode} judge support | {judge['support']:.2f} | — | — |"
                )
                lines.append(
                    f"| {p['ticker']} | {mode} judge relevance | {judge['relevance']:.2f} | — | — |"
                )
    return "\n".join(lines)


def _pct(b: float, c: float) -> str:
    if b == 0:
        return "—"
    return f"{(c - b) / b * 100:+.1f}%"
