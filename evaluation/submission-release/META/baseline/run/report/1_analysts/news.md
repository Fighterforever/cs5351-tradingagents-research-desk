# News & Macro Research Report — META (Meta Platforms, Inc.)

**Role:** News Researcher (nonbinding role analysis — not a transaction proposal)
**Analysis date:** 2026-07-30 | **Ticker:** META | **Latest close:** 539.03 USD [market-meta]

---

## 1. Data availability statement (read first)

Of the four tool families available to me, only the company-news feed returned data. Everything else is **unavailable in this frozen corpus**, and I will not estimate or fabricate it:

| Data requested | Result |
|---|---|
| `get_news(META, 2026-07-23 → 2026-07-30)` | Returned — but only the frozen official Q2 2026 earnings release [src-meta]; no third-party/wire coverage |
| `get_global_news(2026-07-30, 7d)` | **NO_DATA_AVAILABLE** |
| `get_macro_indicators` — fed_funds_rate, cpi, 10y_treasury, yield_curve, unemployment | **NO_DATA_AVAILABLE** (all five) |
| `get_prediction_markets` — "Fed rate cut", "recession 2026" | **NO_DATA_AVAILABLE** |

**Consequence for the team:** I cannot ground any macro claim (policy rate level, inflation path, curve shape, labor market, recession odds, rate-cut pricing) in observed data. Any macro narrative in downstream reports must be flagged as an assumption, not evidence. The report below is therefore **entirely company-fundamental**, which is appropriate here because the single most important event for META — the Q2 2026 print — landed one day before the analysis date.

---

## 2. The dominant event: Q2 2026 results (announced 2026-07-29)

This is the whole news week for META. The release is a **growth-vs-margin divergence** story.

**Top line — strong.**
- Revenue **USD 60.801 billion, +28%** [src-meta]. For a company of this scale, ~28% growth is exceptional and indicates the ad franchise is not decelerating on demand.
- Daily active people **3.60 billion, +3%** [src-meta]. Engagement is stable but no longer a growth driver — the revenue growth is coming from monetization per user, not user growth.

**Bottom line — deteriorating.**
- Operating income **18.775 billion, −8%** [src-meta].
- Operating margin **31% vs 43%** a year ago [src-meta] — a **~12 percentage point** compression. Calculation: 31% − 43% = −12 pp (operands both [src-meta]).
- Costs and expenses **42.03 billion** [src-meta].

**Decomposition of the cost base — the key analytical step.**
- Costs and expenses 42.03bn included **2.40bn legal charges** and **1.18bn severance** [src-meta].
- Calculation: 2.40 + 1.18 = **3.58bn** of the 42.03bn is explicitly one-off/non-operating in character [src-meta].
- Calculation: 3.58 / 42.03 = **~8.5%** of total costs [src-meta].
- Calculation (adjusted, my own construction — not a sourced figure): 42.03 − 3.58 = **38.45bn** underlying cost base; 60.801 − 38.45 = **22.35bn** underlying operating income; 22.35 / 60.801 = **~36.8%** underlying margin vs the reported 31% [src-meta].
- **Interpretation:** roughly 6 pp of the 12 pp margin compression is attributable to disclosed legal + severance items. The remaining ~6 pp is structural — and the most likely structural driver is depreciation from the capex ramp (see below). This distinction matters enormously: the one-off portion does not recur, the depreciation portion does.

**Capex — the crux.**
- Capital expenditures **31.08 billion** in the quarter [src-meta].
- Calculation: 31.08 / 60.801 = **~51%** of quarterly revenue going to capex [src-meta]. That is an extraordinary reinvestment ratio and is the single most important number in the release.
- Calculation: 31.08 vs operating income of 18.775 → capex is **~1.66×** operating income [src-meta]. Free cash flow on a reported basis is therefore under heavy pressure; I cannot compute an exact FCF figure because D&A, taxes and working capital are not in the source, so **FCF is UNKNOWN**.
- The mechanism to watch: capex today becomes depreciation over the next several years, so a 31bn/quarter run-rate is a *forward* margin headwind that the 31% print only begins to reflect. This is the bear case's strongest structural argument and it is fully supported by the source.

---

## 3. What is NOT knowable from the sources (explicitly UNKNOWN)

To prevent downstream fabrication, these are all **UNKNOWN** and must not be stated as fact:
- **EPS of any period** — quarterly, annual, or TTM. The release contains no EPS line [src-meta]. Therefore **trailing P/E is UNKNOWN** and cannot be derived.
- **Valuation multiples of any kind** (P/E, EV/EBITDA, P/S, forward multiples) — UNKNOWN. Note that even with the 539.03 close [market-meta] and 60.801bn quarterly revenue [src-meta], a P/S would require a share count and net debt, neither of which is in the sources.
- **Guidance / outlook** for Q3 or FY2026 — not in the source.
- **Segment detail** (Family of Apps vs Reality Labs revenue and operating loss) — not in the source. This is a material gap: we cannot tell whether the margin hit is ad-core or metaverse/AI-related.
- **User monetization (ARPU), ad impressions/pricing, headcount** — not in the source.
- **Consensus expectations / whether this was a beat or miss** — UNKNOWN. The 28% revenue growth and 31% margin cannot be judged against expectations without consensus data.
- **Price reaction** — I have only the frozen close of 539.03 [market-meta]; I have no prior close, so the post-earnings move is **UNKNOWN** to me. The market analyst should supply this.

---

## 4. Actionable read for traders

1. **The report is a "quality of earnings" event, not a demand event.** Revenue +28% [src-meta] says the core ad business is healthy. The −8% operating income and 31% margin [src-meta] say the cost/capex side is the problem. Trades should be framed around *margin durability*, not *growth durability*.
2. **Separate the 3.58bn of legal + severance from the run-rate.** Calculation: 2.40 + 1.18 = 3.58bn [src-meta]. If a trader's thesis is "margins mean-revert," the burden of proof is on the ~6 pp of *non-one-off* compression, which is most plausibly depreciation from the 31.08bn capex quarter [src-meta]. That portion does not mean-revert quickly.
3. **Capex intensity at ~51% of revenue** (calculation: 31.08 / 60.801 [src-meta]) is the number that will drive the multi-quarter narrative. Any incremental disclosure on capex trajectory is the highest-value catalyst; it is currently UNKNOWN.
4. **Do not build a valuation-based view from this dataset.** With EPS and share count absent [src-meta], any P/E or target multiple would be fabricated. Valuation work must wait for a data source that carries the income statement and share count.
5. **Macro overlay is a blank.** Fed path, inflation, curve and recession odds all returned NO_DATA_AVAILABLE. META is a long-duration, high-capex, ad-cyclical asset that is highly sensitive to rates and to ad budgets — so the absence of macro grounding