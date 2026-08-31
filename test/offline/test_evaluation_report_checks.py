"""Regression tests for the bounded evaluation-report measurement correction.

Two measurement defects were found during the initial AAPL/MSFT development
comparison and repaired in ``src/research_desk/eval/live.py``:

1. ``_report_text`` concatenated stages without titles and repeated the same
   risk-judge/final-decision field twice. It now keeps the authentic upstream
   role titles and includes identical risk/final content exactly once, while
   retaining every different or contrary intermediate opinion.
2. ``_deterministic_checks`` marked ``frozen_price_in_report`` true from
   evidence alone without looking at the report. It now requires both the
   expected close to be supported by evidence/corpus AND stated in the report,
   normalizing ordinary monetary formatting without accepting a different
   number or a substring of a larger number.

These tests use the real ``aapl_pack`` fixture (``model_copy``-based) and the
real ``case_for`` records; no live API call is made.
"""

from __future__ import annotations

import pytest

from research_desk.eval.case_registry import case_for
from research_desk.eval.live import _deterministic_checks, _report_text


def _pack(
    aapl_pack,
    *,
    report_market: str,
    data_snapshot=None,
    available_sources=None,
):
    pack = aapl_pack.model_copy(deep=True)
    final_state = dict(aapl_pack.final_state)
    final_state["market_report"] = report_market
    pack.final_state = final_state
    pack.input = pack.input.model_copy(
        update={
            "data_snapshot": (
                data_snapshot if data_snapshot is not None else pack.input.data_snapshot
            ),
            "available_sources": (
                available_sources
                if available_sources is not None
                else pack.input.available_sources
            ),
        }
    )
    return pack


def _price_check(case: dict, pack) -> dict:
    for check in _deterministic_checks(case, pack, case["ticker"]):
        if check["check"] == "frozen_price_in_report":
            return check
    raise AssertionError("frozen_price_in_report check is missing")


# ---------------------------------------------------------------------------
# _report_text: stage titles, identical-final dedupe, contrary content
# ---------------------------------------------------------------------------


def test_report_text_preserves_stage_titles_and_dedupes_identical_final():
    """Authentic role/stage titles are present and identical risk/final appears once."""
    final_decision = (
        "**Rating**: Buy\n\n**Executive Summary**: Buy AAPL modest size.\n\n"
        "**Investment Thesis**: Supported by analyst evidence."
    )
    fs = {
        "market_report": "Market analyst body text.",
        "news_report": "News analyst body text.",
        "sentiment_report": "Sentiment analyst body text.",
        "fundamentals_report": "Fundamentals analyst body text.",
        "investment_debate_state": {
            "bull_history": "Bull researcher body text.",
            "bear_history": "Bear researcher body text.",
            "judge_decision": "Research manager decision text.",
        },
        "trader_investment_plan": "Trader proposal body text.",
        "risk_debate_state": {
            "aggressive_history": "Aggressive analyst body text.",
            "conservative_history": "Conservative analyst body text.",
            "neutral_history": "Neutral analyst body text.",
            "judge_decision": final_decision,
        },
        "final_trade_decision": final_decision,
    }
    text = _report_text(fs)
    for title in (
        "Market Analyst",
        "News Analyst",
        "Sentiment Analyst",
        "Fundamentals Analyst",
        "Bull Researcher",
        "Bear Researcher",
        "Research Manager",
        "Trader",
        "Aggressive Analyst",
        "Conservative Analyst",
        "Neutral Analyst",
        "Final Portfolio Decision",
    ):
        assert f"## {title}" in text, f"missing stage title {title}"
    assert "## Portfolio Manager" not in text  # identical content included once
    for body in (
        "Market analyst body text.",
        "News analyst body text.",
        "Sentiment analyst body text.",
        "Fundamentals analyst body text.",
        "Bull researcher body text.",
        "Bear researcher body text.",
        "Research manager decision text.",
        "Trader proposal body text.",
        "Aggressive analyst body text.",
        "Conservative analyst body text.",
        "Neutral analyst body text.",
    ):
        assert body in text, f"missing stage content {body}"
    assert text.count(final_decision) == 1


def test_report_text_retains_contrary_intermediate_content():
    """Only the identical risk/final pair is deduped; contrary advice stays."""
    final_decision = "**Rating**: Buy\n\n**Executive Summary**: Buy AAPL."
    fs = {
        "market_report": "Market analyst body text.",
        "investment_debate_state": {
            "bull_history": "Bull: strong product demand.",
            "bear_history": "Bear: margin pressure is material.",
            "judge_decision": "**Recommendation**: Sell\n\n**Rationale**: Valuation stretched.",
        },
        "trader_investment_plan": "**Action**: Sell\n\n**Reasoning**: Reduce exposure now.",
        "risk_debate_state": {
            "aggressive_history": "Aggressive: add aggressively.",
            "conservative_history": "Conservative: keep cash.",
            "judge_decision": final_decision,
        },
        "final_trade_decision": final_decision,
    }
    text = _report_text(fs)
    assert text.count(final_decision) == 1
    assert "Bull: strong product demand." in text
    assert "Bear: margin pressure is material." in text
    assert "**Recommendation**: Sell" in text  # research manager dissent retained
    assert "**Action**: Sell" in text  # trader proposal retained
    assert "Aggressive: add aggressively." in text
    assert "Conservative: keep cash." in text


def test_report_text_distinct_risk_and_final_both_retained():
    """When risk judge and final decision differ, both are reported under titles."""
    fs = {
        "risk_debate_state": {"judge_decision": "Portfolio manager draft."},
        "final_trade_decision": "Final decision text.",
    }
    text = _report_text(fs)
    assert "## Portfolio Manager\nPortfolio manager draft." in text
    assert "## Final Portfolio Decision\nFinal decision text." in text


# ---------------------------------------------------------------------------
# frozen_price_in_report: accepted formats
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "ticker,report_price",
    [
        ("AAPL", "$308.91"),
        ("AAPL", "308.91"),
        ("AAPL", "308.910"),
        ("AAPL", "last close of 308.91 USD"),
        ("MSFT", "$451.10"),
        ("MSFT", "451.1"),
        ("MSFT", "451.10"),
    ],
)
def test_frozen_price_in_report_accepts_normal_formatting(aapl_pack, ticker, report_price):
    """Correct price stated with ordinary monetary formatting passes."""
    case = case_for(ticker)
    close = f"{case['latest_close']:.2f}"
    pack = _pack(
        aapl_pack,
        report_market=f"The closing price was {report_price}.",
        available_sources={"verified_snapshot": f"last_close: {close}"},
    )
    assert _price_check(case, pack)["passed"] is True


@pytest.mark.parametrize(
    "report_price",
    [
        "$308.92",  # different number
        "308.9",  # different number
        "308.9100036621094",  # more precise, not the expected close
        "1308.91",  # substring of a larger number
        "2451.10",  # substring of a larger number
    ],
)
def test_frozen_price_in_report_rejects_different_or_substring_numbers(
    aapl_pack, report_price
):
    """A different number or a substring of a larger number never passes."""
    case = case_for("AAPL")
    pack = _pack(
        aapl_pack,
        report_market=f"The closing price was {report_price}.",
        available_sources={"verified_snapshot": "last_close: 308.91"},
    )
    assert _price_check(case, pack)["passed"] is False


def test_price_token_normalizes_comma_thousands():
    """Comma thousands are ordinary formatting of the same number."""
    from research_desk.eval.live import _contains_price

    assert _contains_price("Priced at $1,234.56 per share.", 1234.56) is True
    assert _contains_price("Priced at $12,345.67.", 2345.67) is False


@pytest.mark.parametrize(
    "text,expected_close,should_match",
    [
        ("The close was 1234.50.", 1234.5, True),  # ungrouped integer of any length
        ("The close was $1,234.50.", 1234.5, True),  # correctly grouped comma amount
        ("The close was -451.10.", 451.1, False),  # sign is part of the value
        ("The close was 1451.10.", 451.1, False),  # substring of a larger number
    ],
)
def test_price_token_sign_and_grouping(text, expected_close, should_match):
    from research_desk.eval.live import _contains_price

    assert _contains_price(text, expected_close) is should_match


# ---------------------------------------------------------------------------
# frozen_price_in_report: both evidence and report are required
# ---------------------------------------------------------------------------


def test_frozen_price_fails_when_report_omits_price_despite_correct_input(aapl_pack):
    """Correct evidence alone no longer passes the check."""
    case = case_for("AAPL")
    pack = _pack(
        aapl_pack,
        report_market="AAPL trends higher with strong volume.",
        available_sources={"verified_snapshot": "last_close: 308.91"},
    )
    assert _price_check(case, pack)["passed"] is False


def test_frozen_price_fails_when_report_states_wrong_price(aapl_pack):
    """Correct evidence plus a wrong stated price fails."""
    case = case_for("AAPL")
    pack = _pack(
        aapl_pack,
        report_market="The last close was $308.92.",
        available_sources={"verified_snapshot": "last_close: 308.91"},
    )
    assert _price_check(case, pack)["passed"] is False


def test_frozen_price_fails_without_evidence_support(aapl_pack):
    """Correct report price without input support fails."""
    case = case_for("AAPL")
    pack = _pack(
        aapl_pack,
        report_market="The last close was 308.91.",
        available_sources={},
    )
    # The aapl fixture snapshot only holds the synthetic 95..100 closes.
    assert _price_check(case, pack)["passed"] is False


def test_frozen_price_evidence_support_from_observed_tool_result(aapl_pack):
    """Observed tool output (not corpus metadata) can supply the evidence side."""
    case = case_for("AAPL")
    pack = _pack(
        aapl_pack,
        report_market="The last close was 308.91.",
        data_snapshot={
            "get_verified_market_snapshot": {"{}": "last_close: 308.91"}
        },
        available_sources={},
    )
    assert _price_check(case, pack)["passed"] is True
