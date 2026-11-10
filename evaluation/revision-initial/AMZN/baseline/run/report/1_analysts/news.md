# News & Macro Research Report — AMZN
**Role:** News Researcher (nonbinding role analysis — not a transaction proposal)
**Analysis date:** 2026-07-31 | **Instrument:** AMZN (Amazon.com, Inc., Consumer Discretionary / Internet Retail)
**Frozen latest close:** 271.5799865722656 USD [market-amzn]

---

## 1. Data availability statement (read first)

This run is executing against a **frozen evaluation corpus**. Of the four tool families available to me, only the company-news source returned data:

| Tool | Status |
|---|---|
| `get_news("AMZN", 2026-07-24 → 2026-07-31)` | **Returned** — official Q2 2026 earnings release [src-amzn] |
| `get_global_news(2026-07-31, 7d)` | **NO_DATA_AVAILABLE** — not part of frozen corpus |
| `get_macro_indicators` (cpi, fed_funds_rate, 10y_treasury, unemployment) | **NO_DATA_AVAILABLE** — all four series unavailable |
| `get_prediction_markets` ("Fed rate cut", "recession 2026") | **NO_DATA_AVAILABLE** — no market-implied probabilities available |

**Consequence for the team:** I cannot ground any macro claim (inflation path, policy rate, curve shape, labor market) or any forward-looking probability (Fed cut odds, recession odds) in observed data. Per the grounding rules I will **not** estimate or fabricate those values. Any macro narrative in downstream bull/bear/trader output that is not traceable to `src-amzn` or `market-amzn` should be treated as unsourced. The only two usable sources are **src-amzn** (earnings) and **market-amzn** (price/technical).

---

## 2. The single hard catalyst: Q2 2026 results (announced 2026-07-30)

Amazon reported Q2 2026, quarter ended June 30, 2026 [src-amzn]. The release landed **one day before** the analysis date, so the frozen close of 271.58 USD [market-amzn] is the first post-announcement mark available to us.

**Reported figures [src-amzn]:**
- Net sales **USD 200.6 billion**, **+20%** year over year.
- **AWS sales 42.2 billion, +37%** year over year.
- **AWS operating income 27.5 billion** vs **19.2 billion** a year earlier.
- **Net income 62.6 billion**, which *includes substantial investment-related gains*.
- **Pre-tax other income 53.4 billion**, *primarily from investments in Anthropic*.
- **Trailing-twelve-month free cash flow: an outflow of 7.6 billion.**

### 2.1 Derived calculations (CALCULATIONS — operands shown, results are not sourced facts)

| Derived metric | Operands (both from src-amzn) | Result |
|---|---|---|
| Prior-year Q2 net sales (implied) | 200.6 ÷ 1.20 | ≈ **167.2 bn** |
| Prior-year Q2 AWS sales (implied) | 42.2 ÷ 1.37 | ≈ **30.8 bn** |
| AWS operating income growth | 27.5 vs 19.2 | **+43.2%** |
| AWS operating margin, Q2 2026 | 27.5 ÷ 42.2 | ≈ **65.2%** |
| AWS operating margin, Q2 2025 (implied) | 19.2 ÷ 30.8 | ≈ **62.3%** |
| AWS share of consolidated net sales | 42.2 ÷ 200.6 | ≈ **21.0%** |
| Pre-tax other income as % of net income | 53.4 ÷ 62.6 | ≈ **85%** |

### 2.2 What these numbers actually say

1. **AWS is the earnings engine and it re-accelerated.** AWS grew 37% [src-amzn] against an implied prior-year base of ~30.8 bn (calculation). AWS operating income grew faster than AWS revenue (+43.2% vs +37%, calculation), i.e. **margin expanded** to roughly 65% (calculation). AWS is only ~21% of revenue (calculation) but is the dominant profit pool — the classic Amazon mix skew.
2. **Top line is healthy at +20%** on a 200.6 bn base [src-amzn]. For a company of this size, 20% is a strong print and implies no visible consumer-demand crack in the reported quarter.
3. **The headline net income of 62.6 bn is NOT an operating number.** Pre-tax other income of 53.4 bn, primarily Anthropic-related investment gains [src-amzn], is ~85% of net income (calculation). This is **mark-to-market / fair-value gain, not cash earnings**. Anyone computing a P/E off 62.6 bn, or annualizing it, is capitalizing a valuation gain. **This is the single biggest trap in this release.**
4. **Free cash flow is negative: TTM outflow of 7.6 bn** [src-amzn]. This is the counterweight to the AWS margin story — heavy capex (consistent with AI/datacenter buildout, though the release does not break out capex, so the driver is **UNKNOWN** from our sources). A company growing 20% with negative TTM FCF is being funded by operating cash flow and/or balance sheet; the release does not give us the split.
5. **Anthropic exposure is now a two-sided risk.** The 53.4 bn pre-tax gain [src-amzn] means a meaningful chunk of reported book earnings is levered to a private AI company's valuation marks. That is a **non-operating, non-cash, and potentially reversible** earnings stream. It cuts both ways: it flattered Q2, and a future down-round or mark-down would hit reported net