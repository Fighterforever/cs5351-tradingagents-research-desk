# News & Macro Research Report — MSFT
**Role: News Researcher (nonbinding role analysis — not a transaction proposal)**
**Analysis date: 2026-07-30 | Ticker: MSFT (Microsoft Corporation, Technology / Software — Infrastructure)**

---

## 1. Data availability — read this first

I must be explicit about what I could and could not verify, because the difference materially limits this report.

| Data source requested | Result |
|---|---|
| Company news for MSFT, 2026-07-23 → 2026-07-30 | **Available** — returned the frozen official earnings source (`src-msft`) |
| Global/macroeconomic news (`get_global_news`) | **NO_DATA_AVAILABLE** — not part of the frozen evaluation corpus |
| FRED macro: `fed_funds_rate`, `10y_treasury`, `cpi`, `yield_curve`, `unemployment` | **NO_DATA_AVAILABLE** for all five |
| Prediction markets: "Fed rate cut", "recession 2026" | **NO_DATA_AVAILABLE** for both |

**Consequence:** I have **no verified macro data, no policy-rate data, no inflation data, no yield data, and no market-implied probabilities** for this analysis date. Per the grounding rules, I will not estimate, interpolate, or fabricate any of these. Every macro statement below is therefore either (a) explicitly labeled UNKNOWN, or (b) framed as a question the trader must resolve with another data source. The only hard evidence in this report is the MSFT earnings release and the frozen market close.

---

## 2. The one substantive news event: MSFT fiscal Q4 2026 (announced 2026-07-29)

This is the dominant, and effectively only, verified news item in the window. It landed **one day before** the analysis date, so the market has had exactly one session to price it.

**Headline results (fiscal Q4 2026, quarter ended June 30, 2026):**
- Revenue **USD 90.0 billion, +18%** [src-msft]
- Operating income **USD 40.6 billion, +18%** [src-msft]
- **GAAP EPS 4.81** vs **non-GAAP EPS 4.74** — note GAAP is *above* non-GAAP [src-msft]
- **Microsoft Cloud revenue 59.3 billion, +27%** [src-msft]
- **Azure and other cloud revenue +43%** [src-msft]
- **Full fiscal year 2026 revenue 331.8 billion** [src-msft]

**Derived calculations (my arithmetic on sourced operands, not sourced facts):**
- Operating margin = 40.6 / 90.0 = **~45.1%** (operands: operating income 40.6bn [src-msft]; revenue 90.0bn [src-msft])
- Cloud mix = 59.3 / 90.0 = **~65.9%** of quarterly revenue (operands: Microsoft Cloud 59.3bn [src-msft]; revenue 90.0bn [src-msft])
- Q4 revenue as share of FY = 90.0 / 331.8 = **~27.1%** (operands: Q4 revenue 90.0bn [src-msft]; FY revenue 331.8bn [src-msft])
- GAAP-minus-non-GAAP EPS spread = 4.81 − 4.74 = **+0.07** (operands: both EPS figures [src-msft])

**What is genuinely notable here, in analytical terms:**

1. **Revenue and operating income grew at identical 18%** [src-msft]. That is an unusual and important signal: it implies operating leverage was *flat* year-over-year — margin held, it did not expand. For a company scaling a 43%-growth cloud business [src-msft], flat margin suggests heavy cost absorption (almost certainly AI/datacenter capacity and depreciation), not deterioration. But traders should not read this print as a margin-expansion story; it is a growth story with margin held constant.

2. **Azure at +43%** [src-msft] is the single most important number in the release. It is the demand read-through for the entire AI-infrastructure complex. A 43% growth rate at Microsoft's scale is a strong absolute signal, though I have **no prior-quarter Azure growth figure in the corpus**, so I cannot state whether 43% represents acceleration or deceleration. **That comparison is UNKNOWN** and is the first thing a trader should source independently — the direction of the *second derivative* on Azure is what typically drives the stock reaction, not the level.

3. **GAAP EPS (4.81) exceeding non-GAAP (4.74)** [src-msft] is a favorable-quality tell. Non-GAAP usually strips out costs, so GAAP > non-GAAP implies net *gains* in the GAAP line (e.g., investment marks) rather than net charges. Caveat: I have no reconciliation detail in the corpus, so the composition of that 0.07 gap is **UNKNOWN** — it may be non-operating and non-recurring, in which case the "clean" earnings power is closer to the non-GAAP 4.74.

4. **Cloud is now roughly two-thirds of revenue** (~65.9% derived) [src-msft]. MSFT's equity story is now overwhelmingly a cloud/AI-infrastructure story; legacy software is a minority of the top line. This raises the stock's sensitivity to cloud capex sentiment and rates.

---

## 3. Valuation — deliberately left UNKNOWN

I want to be precise here because it is a common failure point.

- The corpus gives me **quarterly** EPS only: GAAP 4.81 and non-GAAP 4.74 for fiscal Q4 2026 [src-msft].
- I have **no TTM EPS** and **no annual EPS per share** (FY revenue of 331.8bn [src-msft] is revenue, not EPS, and I have no share count).
- Therefore **trailing P/E is UNKNOWN**. A single quarter's EPS cannot establish a trailing multiple, and I will not annualize 4.81 × 4 — that would be a fabricated figure, not a sourced one.
- **Forward P/E, EV/EBITDA, price/sales, and any price target are UNKNOWN** — none appear in the observed sources.

The only price anchor I have is the frozen close: **USD 451.10** as of 2026-07-30 [market-msft]. Any multiple built on that price requires an EPS or earnings figure I do not possess.

---

## 4. Macro backdrop — UNKNOWN, and that is the report's biggest gap

I cannot responsibly characterize the macro environment for 2026-07-30. Specifically **UNKNOWN**:
- Fed policy rate and the direction/timing of any cuts
- CPI / core PCE inflation trajectory
- 10-year Treasury yield and curve shape
- Unemployment rate
- Market-implied recession probability
- Market-implied Fed-decision odds

**Why this matters disproportionately for MSFT:** a ~45%-operating-margin, ~66%-cloud-mix business trading at USD 451.10 [market-msft] is a long-duration asset. Its valuation is mechanically sensitive to the discount rate, and its capex-heavy AI buildout is sensitive to financing costs. Without the 10-year yield and the policy path, I cannot assess whether the rate backdrop is a tailwind or a headwind for the multiple. **Any trader acting on this report must independently source rates and inflation data before sizing a position.**

---

## 5. Actionable insights for the trading desk

Framed as judgments/assumptions, not sourced facts:

1. **The event is one session old.** Earnings dropped 2026-07-29 [src-msft]; the frozen close of 451.10 is dated 2026-07-30 [market-msft]. Post-earnings drift is typically most violent in the first 1–3 sessions. Confirm whether 451.10 already reflects the print or precedes it before treating it as a post-earnings price