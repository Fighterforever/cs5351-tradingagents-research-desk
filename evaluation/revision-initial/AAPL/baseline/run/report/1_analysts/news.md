# News & Macro Research Report — AAPL (Apple Inc.)
**Role:** News Researcher (nonbinding role analysis — not a transaction proposal)
**Analysis date:** 2026-07-31 | **Instrument:** AAPL | **Latest close:** 308.91 USD [market-aapl]

---

## 1. Data availability statement (read first)

Of the four tool families available to me, only the company-news source returned data. Every macro and prediction-market query returned an explicit unavailability notice, and I will not estimate or fabricate substitutes:

| Tool | Query | Result |
|---|---|---|
| `get_news` (AAPL, 2026-07-24 → 2026-07-31) | company news | **Returned** — official earnings release only [src-aapl] |
| `get_global_news` (2026-07-31, 7d) | global macro news | **NO_DATA_AVAILABLE** — not in frozen corpus |
| `get_macro_indicators` | cpi, fed_funds_rate, 10y_treasury, yield_curve, unemployment | **NO_DATA_AVAILABLE** (all five) |
| `get_prediction_markets` | "Fed rate cut", "recession 2026" | **NO_DATA_AVAILABLE** (both) |

**Consequence for the desk:** I cannot ground any claim about inflation, policy rates, the curve, labor conditions, or market-implied probabilities of Fed action/recession. Any such statement in downstream reports would be unsourced. The macro backdrop is **UNKNOWN** as of 2026-07-31 in this corpus. The only two usable evidence streams are (a) the official Apple earnings release [src-aapl] and (b) the frozen market close [market-aapl].

---

## 2. The single hard catalyst: fiscal Q3 2026 results (announced 2026-07-30)

Apple's fiscal Q3 2026 ended June 27 [src-aapl]. The release is one day old relative to the analysis date, so the market's reaction window is essentially a single session — the frozen close of 308.91 USD [market-aapl] is the post-announcement print available to us.

**Headline figures [src-aapl]:**
- Revenue: **USD 109.4 billion**, up **16% year over year** [src-aapl]
- Gross margin: **50.1%**, including **~2 percentage points of tariff-refund benefit** [src-aapl]
- Diluted EPS: **2.02** (quarterly, fiscal Q3 2026), up **29%**, including **0.11 of tariff-refund benefit** [src-aapl]
- Dividend: **0.27 per share** [src-aapl]

### 2.1 Derived calculations (arithmetic on sourced operands — not sourced facts)

| Derived metric | Operands (both [src-aapl]) | Result |
|---|---|---|
| Prior-year Q3 revenue (implied) | 109.4 ÷ 1.16 | ≈ **94.3 bn** |
| Prior-year Q3 diluted EPS (implied) | 2.02 ÷ 1.29 | ≈ **1.57** |
| EPS excluding tariff-refund benefit | 2.02 − 0.11 | ≈ **1.91** |
| YoY EPS growth ex-refund | 1.91 ÷ 1.57 − 1 | ≈ **+22%** |
| Gross margin ex-refund | 50.1% − ~2.0pp | ≈ **48.1%** |
| Refund share of quarterly EPS | 0.11 ÷ 2.02 | ≈ **5.4%** |
| Implied annualized dividend | 0.27 × 4 | ≈ **1.08 / share** |

**Interpretation:** the quality of the beat matters more than the headline. Roughly 5.4% of quarterly EPS and ~2pp of gross margin are a **one-time tariff-refund item**, not operating momentum [src-aapl]. Even stripping it out, EPS growth of ~22% on revenue growth of 16% implies operating leverage — but the *reported* 29% and 50.1% margin overstate the run-rate. Traders should model the ex-refund ~48.1% margin and ~1.91 EPS as the cleaner base.

### 2.2 What the release does NOT tell us
- **No TTM or annual EPS** is provided [src-aapl]. A single quarter's 2.02 cannot establish a trailing P/E. **Trailing P/E for AAPL is UNKNOWN** in this corpus. Any P/E, forward P/E, EV/EBITDA, or price target quoted downstream would be fabricated.
- **No revenue mix** (iPhone / Services / Mac / Wearables), **no Greater China figure**, **no guidance**, **no buyback authorization**, **no cash/balance-sheet data**, and **no installed-base or AI-related commentary** [src-aapl]. Segment-level rotation calls are therefore unsupported.
- **No volume or technical indicator data** was returned to me; I can cite the close level [market-aapl] but not RSI, moving averages, or relative volume.

---

## 3. Actionable read for the desk

1. **Treat the beat as "good but partly non-recurring."** The tariff-refund contribution (0.11 of 2.02 EPS; ~2pp of margin) [src-aapl] is the key adjustment. A trader anchoring on 50.1% gross margin or 29% EPS growth is anchoring on a number that will not repeat. Use ~48.1% / ~1.91 as the normalized base (derived above from [src-aapl]).
2. **The 16% revenue growth is the strongest signal in the release** [src-aapl] — it is a top-line figure and is not flagged as refund-affected. That is the cleanest evidence of demand strength available.
3. **Do not build a valuation case.** With no TTM EPS [src-aapl] and only a price level of 308.91 USD [market-aapl], no multiple can be computed. Valuation must be left **UNKNOWN** pending a TTM EPS source.
4. **Do not build a macro overlay.** CPI, policy rate, 10Y, curve, unemployment, Fed-cut odds and recession odds are all unavailable. Position sizing and rate-sensitivity arguments cannot be evidenced today; flag them as assumptions if used.
5. **Event-risk framing:** the announcement is 2026-07-30 and the analysis date is 2026-07-31 [src-aapl], so post-earnings drift/analyst-revision flow is still ahead. The absence of any follow-up news in the corpus means I cannot confirm sell-side reaction, guidance commentary, or supply-chain/tariff policy developments.

---

## 4. Key points summary

| Category | Item | Value / Status | Source |
|---|---|---|---|
| Identity | Company / sector | Apple Inc. — Technology / Consumer Electronics | resolved identity |
| Market | Latest close (frozen) | 308.91 USD | [market-aapl] |
| Event | Fiscal Q3 2026 period end | June 27, 2026; announced 2026-07-30 | [src-aapl] |
| Earnings | Revenue | USD 109.4 bn