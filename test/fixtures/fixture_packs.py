"""Deterministic evidence-pack fixtures for the offline slice tests.

Fixtures are hand-built evidence packs that look exactly like the output of a
real ``ResearchRunner`` run — manifest, input snapshot, event log, final state,
usage, calls, optional proposal. They are used only by offline tests; nothing
here performs a network call or starts an LLM request.

Run ``python -m test.fixtures.fixture_packs`` from the repo root to (re)generate
the committed JSON files under ``test/fixtures/packs/``.
"""

from __future__ import annotations

import json
from pathlib import Path

from research_desk.evidence import EvidencePackIO
from research_desk.models import (
    EvidenceEvent,
    EvidencePack,
    InputSnapshot,
    RunManifest,
    UsageSummary,
    utcnow_iso,
)

PACKS_DIR = Path(__file__).parent / "packs"

FINAL_STATE_COMMON = {
    "company_of_interest": "AAPL",
    "trade_date": "2026-06-10",
    "instrument_context": "The instrument to analyze is `AAPL`.",
    "past_context": "",
    "market_report": (
        "**Market Analysis of AAPL**\n\nAAPL trends higher with strong volume. "
        "The last close is 100.00. RSI is 58 (neutral-to-bullish)."
    ),
    "news_report": (
        "**News Analysis of AAPL**\n\nNo negative regulatory headlines; product "
        "cycle momentum continues."
    ),
    "investment_debate_state": {
        "bull_history": "Bull: AAPL fundamentals are solid.",
        "bear_history": "Bear: valuation is stretched.",
        "history": "Debate complete.",
        "current_response": "",
        "judge_decision": "**Recommendation**: Buy\n\n**Rationale**: Fundamentals.",
        "count": 1,
    },
    "trader_investment_plan": (
        "**Action**: Buy\n\n**Reasoning**: Momentum confirms the research plan.\n\n"
        "FINAL TRANSACTION PROPOSAL: **BUY**"
    ),
    "risk_debate_state": {
        "aggressive_history": "Aggressive: size it up.",
        "conservative_history": "Conservative: keep it modest.",
        "neutral_history": "Neutral: balanced.",
        "history": "Risk debate complete.",
        "latest_speaker": "Portfolio Manager",
        "current_aggressive_response": "",
        "current_conservative_response": "",
        "current_neutral_response": "",
        "judge_decision": (
            "**Rating**: Buy\n\n**Executive Summary**: Buy modest size.\n\n"
            "**Investment Thesis**: Supported by evidence."
        ),
        "count": 1,
    },
    "final_trade_decision": (
        "**Rating**: Buy\n\n**Executive Summary**: Buy AAPL modest size.\n\n"
        "**Investment Thesis**: Supported by analyst evidence."
    ),
}


def stock_data_csv(symbol: str, closes: list[float], dates: list[str]) -> str:
    """Build a get_stock_data result string in the upstream CSV shape."""
    assert len(closes) == len(dates)
    header = f"# Stock data for {symbol} from {dates[0]} to {dates[-1]}\n"
    header += f"# Total records: {len(closes)}\n"
    header += f"# Data retrieved on: {dates[-1]} 00:00:00\n\n"
    header += "Date,Open,High,Low,Close,Adj Close,Volume\n"
    for d, c in zip(dates, closes, strict=True):
        header += f"{d},{c:.2f},{c + 1:.2f},{c - 1:.2f},{c:.2f},{c:.2f},1000000\n"
    return header


def news_result(ticker: str) -> str:
    return (
        f"# News for {ticker}\n\n"
        f"2026-06-09: {ticker} reports steady product demand.\n"
        f"2026-06-08: No material regulatory filings.\n"
    )


def _events(
    ticker: str, dates: list[str], closes: list[float], price: float,
) -> list[EvidenceEvent]:
    return [
        EvidenceEvent(seq=1, kind="run_start", ts=utcnow_iso(), payload={"ticker": ticker}),
        EvidenceEvent(seq=2, kind="context_assembled", ts=utcnow_iso(), payload={"mode": "baseline", "chars": 512}),
        EvidenceEvent(seq=3, kind="tool_call", ts=utcnow_iso(), payload={
            "name": "get_stock_data",
            "args": {"symbol": ticker, "start_date": dates[0], "end_date": dates[-1]},
        }),
        EvidenceEvent(seq=4, kind="tool_result", ts=utcnow_iso(), payload={
            "name": "get_stock_data",
            "result": stock_data_csv(ticker, closes, dates),
        }),
        EvidenceEvent(seq=5, kind="tool_call", ts=utcnow_iso(), payload={
            "name": "get_news",
            "args": {"ticker": ticker, "start_date": dates[0], "end_date": dates[-1]},
        }),
        EvidenceEvent(seq=6, kind="tool_result", ts=utcnow_iso(), payload={
            "name": "get_news",
            "result": news_result(ticker),
        }),
        EvidenceEvent(seq=7, kind="llm_request", ts=utcnow_iso(), payload={"model": "deepseek-chat"}),
        EvidenceEvent(seq=8, kind="llm_response", ts=utcnow_iso(), payload={
            "input_tokens": 1200, "output_tokens": 300, "response": "..."}),
        EvidenceEvent(seq=9, kind="run_end", ts=utcnow_iso(), payload={"outcome": "completed"}),
    ]


def build_pack(
    *,
    run_id: str,
    ticker: str,
    trade_date: str,
    signal: str,
    final_decision: str,
    closes: list[float],
    dates: list[str],
    outcome: str = "completed",
    data_mode: str = "live",
    context_mode: str = "baseline",
    memory_used: list[dict] | None = None,
    price: float | None = None,
    with_proposal: bool = True,
    prompt_version: str = "research-desk-0.1.0",
) -> EvidencePack:
    snapshot = {
        "get_stock_data": {
            json.dumps(
                {"symbol": ticker, "start_date": dates[0], "end_date": dates[-1]},
                sort_keys=True,
            ): stock_data_csv(ticker, closes, dates)
        },
        "get_news": {
            json.dumps(
                {"ticker": ticker, "start_date": dates[0], "end_date": dates[-1]},
                sort_keys=True,
            ): news_result(ticker)
        },
    }
    final_state = dict(FINAL_STATE_COMMON)
    final_state["company_of_interest"] = ticker
    final_state["trade_date"] = trade_date
    final_state["final_trade_decision"] = final_decision
    manifest = RunManifest(
        run_id=run_id,
        ticker=ticker,
        trade_date=trade_date,
        asset_type="stock",
        analysts=["market", "news"],
        context_mode=context_mode,
        data_mode=data_mode,
        outcome=outcome,
        signal=signal,
        prompt_version=prompt_version,
        created_at=utcnow_iso(),
        operator="research-desk",
        model_quick="deepseek-chat",
        model_deep="deepseek-reasoner",
    )
    input_snapshot = InputSnapshot(
        instrument_context=f"The instrument to analyze is `{ticker}`.",
        past_context="",
        initial_state={"company_of_interest": ticker, "trade_date": trade_date},
        identity={"company_name": ticker, "sector": "Technology"},
        data_snapshot=snapshot,
        memory_used=memory_used or [],
        memory_sources=["test/fixtures"],
    )
    proposal = None
    if with_proposal and price is not None:
        from research_desk.review import create_proposal

        proposal = create_proposal(
            run_id=run_id, ticker=ticker, trade_date=trade_date,
            signal=signal, rating=signal, price=price,
            proposal_id=f"prop-{run_id[-6:]}",
        )
    return EvidencePack(
        manifest=manifest,
        input=input_snapshot,
        events=_events(ticker, dates, closes, price or 0.0),
        final_state=final_state,
        usage=UsageSummary(calls=2, input_tokens=2400, output_tokens=600, total_tokens=3000, stop_reason="completed"),
        calls=[],
        proposal=proposal,
        complete=False,
    )


DATES = ["2026-06-01", "2026-06-02", "2026-06-03", "2026-06-04", "2026-06-05", "2026-06-08", "2026-06-09", "2026-06-10"]


def _aapl_buy() -> EvidencePack:
    # Last close 100.00 -> price from evidence is exactly 100 (AT-03 boundary).
    return build_pack(
        run_id="fixture-aapl-buy",
        ticker="AAPL",
        trade_date="2026-06-10",
        signal="Buy",
        final_decision=FINAL_STATE_COMMON["final_trade_decision"],
        closes=[95, 96, 97, 98, 99, 99.5, 99.8, 100.0],
        dates=DATES,
        price=100.0,
    )


def _msft_review() -> EvidencePack:
    # No parseable rating -> REVIEW signal, not tradeable.
    return build_pack(
        run_id="fixture-msft-review",
        ticker="MSFT",
        trade_date="2026-06-10",
        signal="REVIEW",
        final_decision="The analysis is ambiguous; no clear rating could be established.",
        closes=[400, 401, 402, 403, 404, 405, 406, 407],
        dates=DATES,
        with_proposal=False,
        price=None,
    )


def _tsla_hold() -> EvidencePack:
    return build_pack(
        run_id="fixture-tsla-hold",
        ticker="TSLA",
        trade_date="2026-06-10",
        signal="Hold",
        final_decision="**Rating**: Hold\n\n**Executive Summary**: Balanced evidence.",
        closes=[250, 251, 252, 253, 254, 255, 256, 257],
        dates=DATES,
        with_proposal=False,
        price=None,
    )


def _nvda_compact_memory() -> EvidencePack:
    # Long history with a repeated report body, used by the AT-06 context test.
    # ``reflection`` is stored WITHOUT the "REFLECTION:" header, matching the
    # shape TradingMemoryLog._parse_entry returns.
    repeated = "Momentum signals worked well; keep the same discipline."
    memory_used = [
        {
            "date": "2026-05-20",
            "ticker": "NVDA",
            "rating": "Buy",
            "decision": "DECISION:\nBuy on strength.",
            "reflection": repeated,
            "resolved": "2026-06-01",
        },
        {
            "date": "2026-04-15",
            "ticker": "NVDA",
            "rating": "Overweight",
            "decision": "DECISION:\nOverweight on data-center demand.",
            "reflection": repeated,
            "resolved": "2026-04-30",
        },
        {
            "date": "2026-03-01",
            "ticker": "NVDA",
            "rating": "Hold",
            "decision": "DECISION:\nHold; valuation elevated.",
            "reflection": repeated,
            "resolved": "2026-03-15",
        },
        # An exact duplicate of the 2026-04-15 entry, so whole-block dedup fires.
        {
            "date": "2026-02-10",
            "ticker": "NVDA",
            "rating": "Overweight",
            "decision": "DECISION:\nOverweight on data-center demand.",
            "reflection": repeated,
            "resolved": "2026-02-25",
        },
    ]
    return build_pack(
        run_id="fixture-nvda-compact-memory",
        ticker="NVDA",
        trade_date="2026-06-10",
        signal="Buy",
        final_decision="**Rating**: Buy\n\n**Executive Summary**: Buy NVDA.",
        closes=[130, 131, 132, 133, 134, 135, 136, 137],
        dates=DATES,
        memory_used=memory_used,
        price=137.0,
    )


def build_all() -> dict[str, EvidencePack]:
    return {
        "aapl_buy_complete": _aapl_buy(),
        "msft_review": _msft_review(),
        "tsla_hold": _tsla_hold(),
        "nvda_compact_memory": _nvda_compact_memory(),
    }


def generate() -> list[Path]:
    io = EvidencePackIO()
    written = []
    for name, pack in build_all().items():
        target = PACKS_DIR / name
        io.export(pack, target)
        (target / "manifest.json").write_text(
            json.dumps(pack.manifest.model_dump(), indent=2), encoding="utf-8"
        )
        (target / "meta.json").write_text(
            json.dumps({"fixture": name, "complete": True}, indent=2), encoding="utf-8"
        )
        written.append(target)
    return written


if __name__ == "__main__":
    for path in generate():
        print(f"wrote {path}")
