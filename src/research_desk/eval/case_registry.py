"""The six frozen evaluation cases and their evidence notes.

The corpus is imported from ``../orchestration/project-market-sources/`` (real
market CSVs) and ``../orchestration/project-evaluation-sources.md`` (factual
source notes). Prices and notes are preserved verbatim; nothing here is
model-generated or fabricated. Two cases (AAPL, MSFT) are development cases for
calibrating the harness; the other four (NVDA, AMZN, META, GOOGL) are held out
and only ever scored by the live judge, never tuned against.

Every case records:
- the analysis day (the day after the earnings announcement, so the after-
  market release does not leak into that day's earlier close),
- the announcement date and the public source URL (source identity),
- the real market CSV and its as-of date / latest close from the retrieval
  manifest,
- the factual source notes the judge compares final reports against.

``source_id`` is the concise ID embedded in final reports for grounding.
"""

from __future__ import annotations

import json
from pathlib import Path

MARKET_DIR = Path(__file__).resolve().parents[3] / "test" / "fixtures" / "market"

# retrieved_at / as_of / latest_close from orchestration/project-market-sources/manifest.json
_MARKET_META = {
    "AAPL": {"as_of": "2026-07-31", "latest_close": 308.9100036621094},
    "MSFT": {"as_of": "2026-07-30", "latest_close": 451.1000061035156},
    "NVDA": {"as_of": "2026-08-27", "latest_close": 227.97999572753906},
    "AMZN": {"as_of": "2026-07-31", "latest_close": 271.5799865722656},
    "META": {"as_of": "2026-07-30", "latest_close": 539.030029296875},
    "GOOGL": {"as_of": "2026-07-23", "latest_close": 317.69000244140625},
}

# Evidence notes preserved from ../orchestration/project-evaluation-sources.md.
# Each is a concise factual statement from the official announcement; the final
# ``balance`` string is the rubric guidance the judge uses to weigh a balanced
# conclusion (it is also part of the evidence, not a grade).
_CASE_NOTES = {
    "AAPL": {
        "notes": [
            "Apple fiscal Q3 2026 ended June 27.",
            "Revenue was USD109.4 billion, up 16% year over year.",
            "Gross margin 50.1% included approximately 2 percentage points of tariff-refund benefit.",
            "Diluted EPS 2.02, up 29%, included 0.11 of tariff-refund benefit.",
            "Dividend 0.27 per share.",
        ],
        "balance": "Distinguish the one-off tariff-refund benefit from underlying operating growth.",
    },
    "MSFT": {
        "notes": [
            "Microsoft fiscal Q4 2026 ended June 30.",
            "Revenue USD90.0 billion increased 18%; operating income 40.6 billion increased 18%.",
            "GAAP EPS 4.81 compared with non-GAAP 4.74.",
            "Microsoft Cloud revenue 59.3 billion increased 27%; Azure and other cloud revenue increased 43%.",
            "Full fiscal year revenue 331.8 billion.",
        ],
        "balance": "Investment gains affected reported income and EPS; do not equate all GAAP growth with operating growth.",
    },
    "NVDA": {
        "notes": [
            "NVIDIA fiscal Q2 2027 ended July 26, 2026.",
            "Revenue USD96.2 billion increased 18% sequentially and 106% year over year.",
            "Data Center revenue 89.0 billion increased 117% year over year.",
            "GAAP and non-GAAP gross margins were both 75.0%.",
            "GAAP EPS 2.46; non-GAAP EPS 2.22.",
        ],
        "balance": "These are quarterly results, not a guarantee of subsequent share performance.",
    },
    "AMZN": {
        "notes": [
            "Amazon Q2 2026 ended June 30.",
            "Net sales USD200.6 billion increased 20%.",
            "AWS sales 42.2 billion increased 37%; operating income 27.5 billion compared with 19.2 billion a year earlier.",
            "Net income 62.6 billion includes substantial investment-related gains; pre-tax other income 53.4 billion was primarily from investments in Anthropic.",
            "Trailing-twelve-month free cash flow was an outflow 7.6 billion.",
        ],
        "balance": "Distinguish operating improvement from investment gains and capital expenditure pressure.",
    },
    "META": {
        "notes": [
            "Meta Q2 2026 revenue USD60.801 billion increased 28%.",
            "Operating income 18.775 billion decreased 8%, and operating margin 31% compared with 43%.",
            "Costs and expenses 42.03 billion included 2.40 billion legal charges and 1.18 billion severance.",
            "Daily active people 3.60 billion increased 3%.",
            "Capital expenditures 31.08 billion.",
        ],
        "balance": "Revenue growth and margin compression coexist; neither should be omitted from a balanced conclusion.",
    },
    "GOOGL": {
        "notes": [
            "Alphabet Q2 2026 revenue USD119.796 billion increased 24%.",
            "Google Cloud revenue 24.768 billion increased 82%.",
            "Operating income 40.770 billion and operating margin 34%.",
            "Net income 112.107 billion and EPS 9.11 were affected by 97.983 billion other income, primarily unrealized equity investment gains.",
        ],
        "balance": "The evidence supports strong cloud growth but does not support treating the full net-income increase as recurring operating performance.",
    },
}

_CASES = [
    {
        "ticker": "AAPL",
        "analysis_date": "2026-07-31",
        "announcement_date": "2026-07-30",
        "split": "development",
        "company_name": "Apple Inc.",
        "sector": "Technology",
        "industry": "Consumer Electronics",
        "source_url": "https://www.apple.com/newsroom/2026/07/apple-reports-third-quarter-results/",
    },
    {
        "ticker": "MSFT",
        "analysis_date": "2026-07-30",
        "announcement_date": "2026-07-29",
        "split": "development",
        "company_name": "Microsoft Corporation",
        "sector": "Technology",
        "industry": "Software — Infrastructure",
        "source_url": "https://www.microsoft.com/en-us/investor/earnings/fy-2026-q4/press-release-webcast",
    },
    {
        "ticker": "NVDA",
        "analysis_date": "2026-08-27",
        "announcement_date": "2026-08-26",
        "split": "held_out",
        "company_name": "NVIDIA Corporation",
        "sector": "Technology",
        "industry": "Semiconductors",
        "source_url": "https://investor.nvidia.com/news/press-release-details/2026/NVIDIA-Announces-Financial-Results-for-Second-Quarter-Fiscal-2027/default.aspx",
    },
    {
        "ticker": "AMZN",
        "analysis_date": "2026-07-31",
        "announcement_date": "2026-07-30",
        "split": "held_out",
        "company_name": "Amazon.com, Inc.",
        "sector": "Consumer Discretionary",
        "industry": "Internet Retail",
        "source_url": "https://ir.aboutamazon.com/news-release/news-release-details/2026/Amazon-com-Announces-Second-Quarter-Results/default.aspx",
    },
    {
        "ticker": "META",
        "analysis_date": "2026-07-30",
        "announcement_date": "2026-07-29",
        "split": "held_out",
        "company_name": "Meta Platforms, Inc.",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "source_url": "https://investor.atmeta.com/investor-news/press-release-details/2026/Meta-Reports-Second-Quarter-2026-Results/default.aspx",
    },
    {
        "ticker": "GOOGL",
        "analysis_date": "2026-07-23",
        "announcement_date": "2026-07-22",
        "split": "held_out",
        "company_name": "Alphabet Inc.",
        "sector": "Communication Services",
        "industry": "Internet Content & Information",
        "source_url": "https://s206.q4cdn.com/479360582/files/doc_financials/2026/q2/2026q2-alphabet-earnings-release.pdf",
    },
]


def all_cases() -> list[dict]:
    """The six evaluation cases, each fully resolved with evidence notes."""
    out = []
    for case in _CASES:
        meta = _MARKET_META[case["ticker"]]
        notes = _CASE_NOTES[case["ticker"]]
        out.append(
            {
                **case,
                "source_id": f"src-{case['ticker'].lower()}",
                "csv": f"{case['ticker']}.csv",
                "csv_path": str(MARKET_DIR / f"{case['ticker']}.csv"),
                "as_of": meta["as_of"],
                "latest_close": meta["latest_close"],
                "identity": {
                    "company_name": case["company_name"],
                    "sector": case["sector"],
                    "industry": case["industry"],
                },
                "notes": notes["notes"],
                "balance": notes["balance"],
            }
        )
    return out


def case_for(ticker: str) -> dict:
    for case in all_cases():
        if case["ticker"].upper() == ticker.upper():
            return case
    raise KeyError(f"unknown evaluation case: {ticker!r}")


def development_cases() -> list[dict]:
    return [c for c in all_cases() if c["split"] == "development"]


def held_out_cases() -> list[dict]:
    return [c for c in all_cases() if c["split"] == "held_out"]


def load_market_manifest() -> dict:
    """Read the frozen retrieval manifest that documents provenance."""
    p = MARKET_DIR / "orchestration-manifest.json"
    return json.loads(p.read_text(encoding="utf-8"))
