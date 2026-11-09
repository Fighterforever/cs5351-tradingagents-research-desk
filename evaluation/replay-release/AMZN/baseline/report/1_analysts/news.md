# News & Macro Research Report — AMZN
**Role: News Researcher (nonbinding role analysis — not a transaction proposal)**
**Analysis date: 2026-07-31 | Ticker: AMZN (Amazon.com, Inc., Consumer Discretionary / Internet Retail)**

## 1. Data availability statement (read first)

Only one of my four tool families returned data. I will not fill the gaps with estimates.

| Tool family | Status |
|---|---|
| `get_news("AMZN", 2026-07-24 → 2026-07-31)` | **Returned data** — but only the frozen official earnings source `src-amzn` (announcement 2026-07-30). No third-party/wire coverage, no analyst notes, no price-action commentary. |
| `get_global_news(2026-07-31, 7d)` | **NO_DATA_AVAILABLE** — not part of the frozen corpus. |
| `get_macro_indicators` (fed_funds_rate, 10y_treasury, cpi, unemployment) | **NO_DATA_AVAILABLE** for all four — not part of the frozen corpus. |
| `get_prediction_markets` ("Fed rate cut", "recession 2026") | **NO_DATA_AVAILABLE** — not part of the frozen corpus. |

**Consequence:** I cannot ground any statement about the Fed path, inflation, Treasury yields, labor market, recession odds, or market-implied probabilities. Every such item below is explicitly marked **UNKNOWN**. Any macro narrative I could write would be fabrication, so I am not writing one.

## 2. The one hard news event: Q2 2026 results (announced 2026-07-30)

This is the dominant, and effectively only, verifiable news input for AMZN this week.

**Top line and profitability**
- Q2 2026 ended June 30 [src-amzn].
- Net sales USD 200.6 billion, up 20% [src-amzn]. (The 20% growth rate is as reported in the source; the prior-year base is not disclosed in my sources, so I cannot independently recompute it.)
- Net income USD 62.6 billion [src-amzn].

**AWS — the core value driver**
- AWS sales USD 42.2 billion, up 37% [src-amzn].
- AWS operating income USD 27.5 billion vs USD 19.2 billion a year earlier [src-amzn].
- Derived: AWS segment operating margin = 27.5 / 42.2 ≈ **65.2%** (calculation from the two `src-amzn` operands, not a sourced figure).
- Derived: AWS YoY operating income growth = (27.5 − 19.2) / 19.2 ≈ **+43.2%** (calculation from `src-amzn` operands).
- Derived: AWS share of consolidated net sales = 42.2 / 200.6 ≈ **21.0%** (calculation from `src-amzn` operands).

**Critical quality-of-earnings flag**
- Net income of USD 62.6 billion "includes substantial investment-related gains"; pre-tax other income of USD 53.4 billion was "primarily from investments in Anthropic" [src-amzn].
- Derived: pre-tax other income as a share of net income = 53.4 / 62.6 ≈ **85.3%** (calculation from `src-amzn` operands). Note this is a pre-tax figure compared against an after-tax net income figure, so it is an approximation of magnitude, not a clean ratio.
- **Interpretation (analyst judgment, not sourced):** the headline USD 62.6 billion net income is overwhelmingly non-operating and non-cash. A trader anchoring on that number — or on any EPS derived from it — would be materially overstating Amazon's recurring earning power. The Anthropic stake is a mark-to-market venture position, so it is a source of *volatility* in reported earnings, not a repeatable earnings stream. Any P/E computed off this quarter's net income is economically meaningless.

**Cash flow — the genuine negative**
- Trailing-twelve-month free cash flow was an **outflow of USD 7.6 billion** [src-amzn].
- **Interpretation (analyst judgment):** this is the single most important line in the release for a risk view. A company growing revenue 20% and AWS 37% while burning USD 7.6 billion of TTM FCF is in a heavy capital-deployment cycle (AI/datacenter/logistics buildout — the specific capex figure is **UNKNOWN** in my sources). It means reported earnings and cash generation have diverged sharply, and it removes buyback/dividend optionality as a support for the equity.

## 3. What I can and cannot say about valuation

- Latest close: **USD 271.5799865722656** on the frozen market CSV as of 2026-07-31 [market-amzn].
- **Trailing P/E: UNKNOWN.** I have no TTM EPS in my sources. Per the grounding rules, a single quarter's net income (especially one 85%+ driven by Anthropic investment gains [src-amzn]) cannot establish a trailing multiple. I will not compute one.
- **Forward P/E, EV/EBITDA, price/sales, price/FCF: UNKNOWN** — no share count, no consensus estimates, no EBITDA, no net debt in my sources.
- **Price reaction to the 2026-07-30 print: UNKNOWN.** I have a single frozen close for 2026-07-31 [market-amzn] but no prior close, so I cannot compute the post-earnings move. The market analyst with the full price series should own that.

## 4. Actionable read-through for traders (labeled as judgment)

1. **Trade the operating story, not the headline EPS.** The defensible bull case is AWS: +37% growth with ~65% segment margin and +43% segment operating income [src-amzn, derived]. That is an acceleration-and-margin-expansion combination, and it is the part of the release that is cash-generative and repeatable.
2. **Discount the USD 62.6 billion net income entirely.** Strip the USD 53.4 billion pre-tax Anthropic-driven other income [src-amzn] and the underlying operating result is a far more modest number. Anyone quoting a P/E off this quarter is wrong.
3. **Treat the −USD 7.6 billion TTM FCF [src-amzn] as the key bear datapoint.** It is the strongest available argument that the AI buildout is consuming more cash than the business throws off, and it is the item most likely to drive multiple compression if it persists.
4. **Do not build a macro overlay from this report.** Fed path, CPI, yields, unemployment and recession odds are all **UNKNOWN** in this corpus. Any position sizing that depends on a rate-cut assumption is currently ungrounded — flag that to the risk analyst rather than assuming a benign backdrop.
5. **Concentration risk to note:** the Anthropic position is now large enough to move Amazon's reported net income by tens of billions [src-amzn]. That introduces a private-AI-valuation beta into AMZN's earnings that did not exist historically — a genuine, if unusual, risk factor.

## 5. Key points summary

| Item | Value / Finding | Source | Status |
|---|---|---|---|
| Ticker / identity | AMZN — Amazon.com, Inc., Consumer Discretionary / Internet Retail | resolved identity | Given |
| Analysis date | 2026-07-31 | — | Given |
| Latest close | USD 271.5799865722656 | market-amzn | Sourced |
| Q2 2026 period end | June 30, 2026 | src-amzn | Sourced |
| Net sales | USD 200.6bn, +20% | src-amzn | Sourced |
| AWS sales | USD 42.2bn, +37% | src-amzn | Sourced |
| AWS operating income | USD 27.5bn vs 19.2bn prior year | src-amzn | Sourced |
| AWS segment margin | ≈65.2% (27.5/42.2) | src-amzn operands | Calculation |
| AWS op. income growth | ≈+