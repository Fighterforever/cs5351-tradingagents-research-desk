"""Deterministic research-report identity contract (ADR-004).

The header is rendered only from the actual ``EvidencePack``. These tests use
two different actual-shaped fixture packs to prove the output is generic (legal
identity and evidence price per pack), that unknown facts stay unavailable, and
that the exported report, replay output, run summary and judge input all share
the same contract without changing raw ``final_state`` text.
"""

from __future__ import annotations

import copy

from research_desk.eval.case_registry import case_for
from research_desk.eval.live import _deterministic_checks
from research_desk.replay import ReplayEngine
from research_desk.report import (
    apply_research_identity_header,
    render_research_identity,
    render_run_report,
)
from test.fixtures.fixture_packs import build_pack, stock_data_csv
from tradingagents.reporting import write_report_tree


def _actual_pack(
    *,
    ticker: str,
    company: str,
    close: float,
    source_id: str,
    analysis_date: str,
    as_of: str,
):
    dates = ["2026-06-01", "2026-06-10"]
    pack = build_pack(
        run_id=f"run-{ticker.lower()}-contract",
        ticker=ticker,
        trade_date=analysis_date,
        signal="Buy",
        final_decision="**Rating**: Buy\n\n**Executive Summary**: Buy modest size.",
        closes=[close - 1.0, close],
        dates=dates,
        with_proposal=False,
    )
    pack.input = pack.input.model_copy(
        update={
            "identity": {
                "company_name": company,
                "sector": "Technology",
                "industry": "Test Industry",
            },
            "available_sources": {
                "identity": {
                    "company_name": company,
                    "sector": "Technology",
                    "industry": "Test Industry",
                },
                "latest_close": close,
                "as_of": as_of,
                "source_id": source_id,
                "market_source_id": f"market-{ticker.lower()}",
                "market": stock_data_csv(ticker, [close - 1.0, close], dates),
                "verified_snapshot": f"last_close: {close:.2f}",
            },
        }
    )
    return pack


def test_identity_header_is_generic_across_two_actual_packs():
    aapl = _actual_pack(
        ticker="AAPL",
        company="Apple Inc.",
        close=308.91,
        source_id="src-aapl",
        analysis_date="2026-07-31",
        as_of="2026-07-31",
    )
    msft = _actual_pack(
        ticker="MSFT",
        company="Microsoft Corporation",
        close=451.10,
        source_id="src-msft",
        analysis_date="2026-07-30",
        as_of="2026-07-30",
    )

    aapl_header = render_research_identity(aapl)
    assert "Apple Inc." in aapl_header
    assert "AAPL" in aapl_header
    assert "2026-07-31" in aapl_header
    assert "308.91" in aapl_header
    assert "market-aapl" in aapl_header
    assert "src-aapl" in aapl_header
    assert "Microsoft Corporation" not in aapl_header
    assert "451.10" not in aapl_header

    msft_header = render_research_identity(msft)
    assert "Microsoft Corporation" in msft_header
    assert "MSFT" in msft_header
    assert "2026-07-30" in msft_header
    assert "451.10" in msft_header
    assert "market-msft" in msft_header
    assert "src-msft" in msft_header
    assert "Apple Inc." not in msft_header
    assert "308.91" not in msft_header


def test_missing_identity_and_price_stay_explicitly_unavailable():
    pack = build_pack(
        run_id="run-missing-contract",
        ticker="AAPL",
        trade_date="2026-07-31",
        signal="Buy",
        final_decision="**Rating**: Buy",
        closes=[99.0, 100.0],
        dates=["2026-06-01", "2026-06-10"],
        with_proposal=False,
    )
    pack.input = pack.input.model_copy(
        update={"identity": {}, "available_sources": {}, "data_snapshot": {}}
    )

    header = render_research_identity(pack)
    assert "- Company (legal identity): unavailable" in header
    assert "- Evidence latest close: unavailable" in header
    assert "- Official earnings source: unavailable" in header
    assert "- Company (legal identity): AAPL" not in header
    assert "market-aapl" not in header


def test_header_does_not_invent_market_id_without_market_corpus():
    pack = build_pack(
        run_id="run-no-corpus-contract",
        ticker="AAPL",
        trade_date="2026-07-31",
        signal="Buy",
        final_decision="**Rating**: Buy",
        closes=[99.0, 100.0],
        dates=["2026-06-01", "2026-06-10"],
        with_proposal=False,
    )
    pack.input = pack.input.model_copy(
        update={
            "identity": {"company_name": "Apple Inc."},
            "available_sources": {"latest_close": 100.0},
        }
    )
    observed = render_research_identity(pack)
    assert "market-aapl" not in observed
    assert "observed get_stock_data tool result" in observed

    pack.input = pack.input.model_copy(
        update={"data_snapshot": {}, "available_sources": {"latest_close": 100.0}}
    )
    metadata = render_research_identity(pack)
    assert "market-aapl" not in metadata
    assert "pack case metadata" in metadata


def test_exported_complete_report_gets_header_and_keeps_raw_text(tmp_path):
    pack = _actual_pack(
        ticker="AAPL",
        company="Apple Inc.",
        close=308.91,
        source_id="src-aapl",
        analysis_date="2026-07-31",
        as_of="2026-07-31",
    )
    raw_market = pack.final_state["market_report"]
    original_state = copy.deepcopy(pack.final_state)

    out = tmp_path / "report"
    complete = write_report_tree(pack.final_state, pack.manifest.ticker, out)
    apply_research_identity_header(complete, render_research_identity(pack))

    text = complete.read_text(encoding="utf-8")
    assert text.startswith("# Research Desk Analysis Report")
    assert "Apple Inc." in text
    assert "308.91" in text
    assert raw_market in text  # generated model text is unchanged
    assert pack.final_state == original_state

    # Re-applying must replace the header, not duplicate it.
    apply_research_identity_header(complete, render_research_identity(pack))
    assert text.count("# Research Desk Analysis Report") == 1
    assert complete.read_text(encoding="utf-8").count("# Research Desk Analysis Report") == 1


def test_replay_output_uses_same_contract_without_duplicate_header(tmp_path):
    pack = _actual_pack(
        ticker="MSFT",
        company="Microsoft Corporation",
        close=451.10,
        source_id="src-msft",
        analysis_date="2026-07-30",
        as_of="2026-07-30",
    )
    raw_market = pack.final_state["market_report"]
    original_state = copy.deepcopy(pack.final_state)

    out = tmp_path / "replay"
    ReplayEngine().replay(pack, out)
    complete = out / "complete_report.md"
    text = complete.read_text(encoding="utf-8")
    assert text.startswith("# Research Desk Analysis Report")
    assert "Microsoft Corporation" in text
    assert "451.10" in text
    assert raw_market in text
    assert pack.final_state == original_state

    ReplayEngine().replay(pack, out)
    rebuilt = complete.read_text(encoding="utf-8")
    assert rebuilt.count("# Research Desk Analysis Report") == 1


def test_run_summary_and_judge_input_share_the_contract():
    from research_desk.eval.live import _report_text, _report_text_with_identity

    pack = _actual_pack(
        ticker="AAPL",
        company="Apple Inc.",
        close=308.91,
        source_id="src-aapl",
        analysis_date="2026-07-31",
        as_of="2026-07-31",
    )

    summary = render_run_report(pack)
    assert summary.startswith("# Research Desk Analysis Report")
    assert "Apple Inc." in summary
    assert "308.91" in summary

    raw = _report_text(pack.final_state)
    judged = _report_text_with_identity(pack)
    assert judged.startswith("# Research Desk Analysis Report")
    assert "Apple Inc." in judged
    assert "308.91" in judged
    assert raw in judged  # every generated role paragraph is preserved


def _checks_by_name(pack, ticker: str) -> dict[str, dict]:
    return {
        check["check"]: check
        for check in _deterministic_checks(case_for(ticker), pack, ticker)
    }


def test_identity_check_uses_exported_header_when_raw_narrative_omits_name():
    pack = _actual_pack(
        ticker="AAPL",
        company="Apple Inc.",
        close=308.91,
        source_id="src-aapl",
        analysis_date="2026-07-31",
        as_of="2026-07-31",
    )
    assert "Apple Inc." not in pack.final_state["market_report"]

    checks = _checks_by_name(pack, "AAPL")
    assert checks["instrument_identity"]["passed"] is True
    assert checks["analysis_date"]["passed"] is True


def test_identity_check_fails_for_missing_or_wrong_pack_identity():
    pack = _actual_pack(
        ticker="AAPL",
        company="Apple Inc.",
        close=308.91,
        source_id="src-aapl",
        analysis_date="2026-07-31",
        as_of="2026-07-31",
    )
    sources = dict(pack.input.available_sources)
    sources.pop("identity", None)

    missing = pack.model_copy(deep=True)
    missing.input = missing.input.model_copy(
        update={"identity": {}, "available_sources": sources}
    )
    assert _checks_by_name(missing, "AAPL")["instrument_identity"]["passed"] is False

    wrong = pack.model_copy(deep=True)
    wrong_sources = dict(sources)
    wrong_sources["identity"] = {"company_name": "Wrong Corporation"}
    wrong.input = wrong.input.model_copy(
        update={
            "identity": {"company_name": "Wrong Corporation"},
            "available_sources": wrong_sources,
        }
    )
    assert _checks_by_name(wrong, "AAPL")["instrument_identity"]["passed"] is False


def test_judge_rubric_says_header_does_not_excuse_contradictions():
    from research_desk.eval.live import _judge_prompt

    prompt = _judge_prompt(
        {
            "ticker": "AAPL",
            "analysis_date": "2026-07-31",
            "latest_close": 308.91,
            "source_id": "src-aapl",
            "notes": [],
        },
        "report text",
        [],
        available_sources={},
        events=[],
    )
    assert "A correct header does NOT excuse a contradictory price or identity" in prompt
    assert "wrong earnings period or unit" in prompt
