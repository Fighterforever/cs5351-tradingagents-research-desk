# META — Technical Analysis Report
**Role: Market Analyst (technical)** | Ticker: META | Analysis date: 2026-07-30 | Latest close: 539.03 USD [market-meta]

---

## 1. Data Integrity & Scope Notes (read first)

- The frozen market CSV supplied to me contains **62 rows spanning 2026-05-01 to 2026-07-30** [market-meta]. My requested window began 2025-11-01, but no rows before 2026-05-01 were returned.
- Consequently, **`close_50_sma` and `close_200_sma` returned `NO_DATA_AVAILABLE`** — the tool explicitly states it needs 50 and 200 rows respectively and only 30 were available at 2026-07-30 [market-meta]. **I will not estimate or fabricate these values.** This is a material limitation: I cannot confirm a golden/death cross, cannot state whether price is above or below the 200-day, and cannot use the 50-day as dynamic support. Any claim about the long-term trend structure must therefore be built from price action and the shorter averages only.
- The verified snapshot confirms: last close **539.03**, open **526.00**, day high **539.88**, day low **524.49**, volume **42,271,500** [market-meta]. This matches the final CSV row exactly — no discrepancy between tools.
- **No valuation ratio, P/E, EPS, or price target is available in my sources.** Per grounding rules, all such figures are **UNKNOWN** and are not asserted here. I have no TTM EPS evidence, so no trailing P/E is computed.

---

## 2. The Dominant Fact: A Violent Post-Earnings Gap Down

The single most important observation is the **2026-07-30 session**: price opened at **526.00** versus the prior close of **585.61** on 2026-07-29, and closed at **539.03** on volume of **42.27 million** [market-meta].

Derived calculation (operands cited, result is arithmetic, not a sourced fact):
- Gap from prior close to open: (526.00 − 585.61) / 585.61 = **−10.18%** [market-meta]
- Close-to-close change: (539.03 − 585.61) / 585.61 = **−7.95%** [market-meta]
- Volume vs. the 2026-07-29 session (22.37M): 42.27M / 22.37M = **1.89×** [market-meta]

This is a **high-volume, gap-down repricing event**, and it is directly attributable to the Q2 2026 earnings release dated 2026-07-29 [src-meta]. The fundamental trigger is legible in the official numbers:

- Revenue **USD 60.801B, +28%** [src-meta] — top line was strong.
- Operating income **18.775B, −8%**, operating margin **31% vs. 43%** [src-meta] — a **12-percentage-point margin collapse** (derived: 31% − 43% = −12pp, both operands [src-meta]).
- Costs and expenses **42.03B**, *including* **2.40B legal charges** and **1.18B severance** [src-meta].
- Capital expenditures **31.08B** [src-meta] — a very large absolute capex figure against 60.8B revenue (derived ratio: 31.08 / 60.801 = **51.1%** of quarterly revenue, both operands [src-meta]).
- Daily active people **3.60B, +3%** [src-meta] — engagement growth is decelerating relative to the 28% revenue growth.

**Interpretation:** The market is not punishing the revenue line; it is punishing the **margin and cost structure**. A 28% revenue grower that simultaneously prints an 8% operating-income decline, a 12pp margin compression, 3.58B of one-off legal/severance drag (derived: 2.40 + 1.18 = 3.58B, both operands [src-meta]), and 31.08B of quarterly capex is being re-rated from "growth compounder" toward "capex-heavy, margin-constrained" — hence the gap. Note the one-offs are *inside* the 42.03B cost base, so a portion of the margin hit is non-recurring; the market's reaction suggests it is discounting the recurring capex/depreciation trajectory more than the one-offs.

---

## 3. Trend Structure: Broken Short-Term, Medium-Term Topping, Long-Term Unknown

### 3.1 Price path reconstruction [market-meta]
- **May 2026:** a tight, upward-drifting range roughly **598–643**, with a breakout on 2026-05-27 (close 635.26 on 23.14M volume) and a peak close of **635.29** on 2026-05-28.
- **June 2026:** a persistent **lower-highs sequence** — 627.57 (06-04) → 600.21 (06-16) → 577.22 (06-18) → 563.29 (06-30), with a June low close of **542.87** on 2026-06-25.
- **Early July 2026:** a sharp **recovery impulse** — 2026-07-01 closed **612.91** on **45.54M** volume (the largest volume in the sample until today), then a run to **681.31** on 2026-07-15, the **highest close in the dataset**.
- **Mid-to-late July 2026:** a **rollover** — 664.54 (07-16) → 646.01 (07-17) → 627.17 (07-22) → 606.10 (07-23) → 595.19 (07-24) → 593.41 (07-28) → 585.61 (07-29) → **539.03 (07-30)**.

So the sequence is: **June downtrend → July V-shaped recovery to a new high → immediate failure and a much deeper breakdown.** The 2026-07-15 high of 681.31 was never consolidated; the entire July advance has been fully retraced and then some.

### 3.2 Moving averages — what I *can* say
- **10 EMA = 597.37** vs. last close **539.03** [market-meta]. Price is **58.34 points below** the 10 EMA (derived: 539.03 − 597.37 = −58.34, both operands [market-meta]), i.e. **−9.8%** below it (derived: −58.34 / 597.37). The short-term average is now **overhead resistance**, not support. This is the classic signature of a momentum break: the fastest average has flipped from floor to ceiling.
- **50 SMA and 200 SMA: UNKNOWN** [market-meta, NO_DATA_AVAILABLE]. I explicitly flag that I cannot verify whether the 50-day has crossed the 200-day, nor where the long-term trend line sits. Given the July high of 681.31 and today's 539.03, it is *plausible* price has lost the 50-day, but **I will not assert it** — the data is not in my sources.

### 3.3 Bollinger structure — a genuine outlier reading
- Bollinger middle (20 SMA) = **622.11** [market-meta]
- Upper band = **694.96** [market-meta]
- Lower band = **549.26** [market-meta]
- Last close = **539.03** [market-meta]

**Price is trading BELOW the lower Bollinger band.** Derived: 539.03 − 549.26 = **−10.23 points** below the lower band [market-meta]. Band width (derived): 694.96 −