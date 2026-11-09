# News & Macro Research Report — AAPL (Apple Inc.)
**Role:** News Researcher (nonbinding role analysis — not a transaction proposal)
**Analysis date:** 2026-07-31 | **Ticker:** AAPL | **Latest close:** 308.91 USD [market-aapl]

---

## 1. Data Availability Statement (read first)

This analysis runs against a **frozen evaluation corpus**. Only two sources are live:

- **src-aapl** — Apple's official fiscal Q3 2026 earnings release (announcement 2026-07-30).
- **market-aapl** — frozen market price/volume and technical computations (close as-of 2026-07-31).

The following tool calls were attempted and returned **NO_DATA_AVAILABLE** — this data is *not* part of the corpus, and I will not estimate or fabricate it:

| Tool | Requested | Result |
|---|---|---|
| get_global_news | 7-day lookback to 2026-07-31 | NO_DATA_AVAILABLE |
| get_macro_indicators | cpi | NO_DATA_AVAILABLE |
| get_macro_indicators | core_pce | NO_DATA_AVAILABLE |
| get_macro_indicators | fed_funds_rate | NO_DATA_AVAILABLE |
| get_macro_indicators | 10y_treasury | NO_DATA_AVAILABLE |
| get_macro_indicators | yield_curve | NO_DATA_AVAILABLE |
| get_macro_indicators | unemployment | NO_DATA_AVAILABLE |
| get_macro_indicators | vix | NO_DATA_AVAILABLE |
| get_prediction_markets | Fed rate cut | NO_DATA_AVAILABLE |
| get_prediction_markets | recession 2026 | NO_DATA_AVAILABLE |
| get_prediction_markets | tariffs | NO_DATA_AVAILABLE |

**Consequence for the team:** there is **no observable macro backdrop, no rate path, no inflation print, no market-implied probability set, and no non-earnings company news** in this corpus. Any macro narrative (e.g. "Fed cutting," "tariffs escalating," "VIX elevated") would be invention. Downstream roles must treat all macro/rate/positioning inputs as **UNKNOWN** and confine themselves to the earnings release and the frozen price series.

---

## 2. The One Hard Catalyst: Fiscal Q3 2026 Results (announced 2026-07-30)

Apple's fiscal Q3 2026 ended June 27 [src-aapl]. The release is the sole fundamental input available.

**Headline figures [src-aapl]:**
- Revenue: **USD 109.4 billion**, **+16% year over year** [src-aapl]
- Gross margin: **50.1%**, including **~2 percentage points of tariff-refund benefit** [src-aapl]
- Diluted EPS: **2.02** (Q3 FY2026 quarter only), **+29%**, including **0.11 of tariff-refund benefit** [src-aapl]
- Dividend: **0.27 per share** [src-aapl]

### 2.1 The critical analytical point: earnings quality

The reported numbers are strong, but a material slice is **non-recurring tariff-refund benefit**, not operating momentum:

- Gross margin ex-refund: 50.1% − ~2.0pp = **~48.1%** — a *calculation* from 50.1% and the ~2pp refund disclosure [src-aapl]. The refund contributed roughly **4% of the gross-margin rate** (2.0 / 50.1 ≈ 4.0%) — calculation from the same operands [src-aapl].
- EPS ex-refund: 2.02 − 0.11 = **1.91** — a *calculation* from the two disclosed operands [src-aapl]. The refund is therefore **~5.4% of reported diluted EPS** (0.11 / 2.02 ≈ 5.4%) — calculation [src-aapl].
- Growth ex-refund: reported EPS growth of +29% [src-aapl] is flattered by the refund. The **underlying growth rate cannot be computed** because prior-year Q3 FY2025 diluted EPS is not in the corpus — that figure is **UNKNOWN**. Do not assume the +29% is organic.

**Trading implication:** the "beat" is partly a one-time tariff-refund accounting benefit. A trader anchoring on 50.1% gross margin or 2.02 EPS as the run-rate is overstating normalized profitability by ~2pp of margin and ~0.11 of quarterly EPS [src-aapl]. The correct normalized read is **~48% gross margin and ~1.91 quarterly EPS** — both calculations, not sourced facts.

### 2.2 What the release does NOT tell us

- **No revenue by segment/geography** (iPhone, Services, Greater China) — UNKNOWN.
- **No guidance** for fiscal Q4 2026 — UNKNOWN.
- **No cash flow, buyback, or net-cash figures** — UNKNOWN.
- **No TTM EPS.** Only a single quarter (2.02) is disclosed [src-aapl]. Per grounding rule 4, a **trailing P/E cannot be computed** from one quarter. Trailing P/E for AAPL is **UNKNOWN**. Any P/E quoted downstream must be labeled UNKNOWN or built from actual TTM evidence that does not exist here.
- **No forward EPS, no price target, no multiple** — all UNKNOWN.

### 2.3 Dividend math (calculation, not sourced fact)

Annualized dividend = 0.27 × 4 = **1.08 per share** — calculation from the disclosed quarterly 0.27 [src-aapl]. Against the frozen close of 308.91 [market-aapl], implied yield = 1.08 / 308.91 ≈ **0.35%** — a calculation using operands from src-aapl and market-aapl. This is a derived ratio, not a sourced fact, and it is thin relative to any plausible cash-yield alternative (the alternative's yield is UNKNOWN here).

---

## 3. Price Context

- Frozen latest close: **308.91 USD** as of 2026-07-31 [market-aapl], i.e. the first session after the 2026-07-30 release [src-aapl].
- **The corpus contains no pre-earnings close, no volume data, and no technical indicator values in this report's tool output.** Therefore the **post-earnings price reaction, gap size, and volume confirmation are UNKNOWN** to me. I cannot state whether the market rewarded or punished the print. The market analyst role, which has the market CSV, must supply the reaction and trend structure.
- Because trailing EPS is UNKNOWN, **no valuation multiple can be attached to 308.91** [market-aapl]. The stock's cheapness/richness is **UNKNOWN** on the evidence available.

---

## 4. Actionable Insights for the Desk

1. **Normalize before you model.** Use ~48.1% gross margin and ~1.91 quarterly EPS as the clean run-rate, not 50.1% / 2.02 [src-aapl]. The ~2pp margin and 0.11 EPS tariff-refund benefit is explicitly non-operating in nature [src-aapl].
2. **Treat the +29% EPS growth as an upper bound, not a trend.** Prior-year comparables are absent, so the organic growth rate is UNKNOWN [src-aapl]. Do not extrapolate +29% into forward estimates.
3. **Tariff-refund is a policy-dependent item.** Its presence in the quarter [src-aapl] means the *absence* of a similar refund in future quarters is a mechanical headwind to reported margin and EPS. The size and timing of any future refund is UNKNOWN — no tariff policy data is available in this corpus (prediction-market query returned NO_DATA_AVAILABLE).
4. **Do not build a macro overlay.** With CPI, core PCE, fed funds, 10Y, curve, unemployment, VIX, and all prediction markets unavailable, any rate-cut or recession probability quoted to the desk would be fabricated. Flag