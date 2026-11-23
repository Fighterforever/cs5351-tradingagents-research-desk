# META — Technical Analysis Report
**Role: Market Analyst (technical)** | Ticker: META | Analysis date: 2026-07-30 | Latest close: 539.03 USD [market-meta]

---

## 1. Data Integrity & Scope Notes (read first)

- The frozen market CSV returned **62 rows spanning 2026-05-01 → 2026-07-30** [market-meta]. The requested start date of 2025-11-01 was not honored by the vendor; the effective history is ~3 months.
- Consequently, **close_50_sma and close_200_sma are NO_DATA_AVAILABLE** — the tool explicitly refused to compute them (needs 50 / 200 rows, only 30 available at 2026-07-30) [market-meta]. I will **not** estimate or fabricate these. This is a material limitation: I cannot confirm a golden/death cross, and I cannot state whether price is above or below the 200-day benchmark.
- The verified snapshot confirms: last_close 539.03, last_open 526.00, day_high 539.88, day_low 524.49, volume 42,271,500 [market-meta]. This matches the final CSV row exactly — **no discrepancy** between tools.
- All indicator values below are computed from the frozen CSV and carry source_id market-meta.

---

## 2. The Dominant Fact: A Post-Earnings Gap-Down of Historic Proportions

The single most important observation is the **2026-07-30 session**:

- Open 526.00, high 539.88, low 524.49, close 539.03, volume 42,271,500 [market-meta].
- Prior close (2026-07-29) was 585.61 [market-meta].
- **Calculation:** (539.03 − 585.61) / 585.61 = **−7.95%** on the day. Operands: 539.03 and 585.61 [market-meta]. This is a derived figure, not a sourced fact.
- **Calculation:** volume 42,271,500 vs. the 2026-07-29 volume of 22,371,100 = **1.89×** prior-day volume. Operands both [market-meta]. This is the highest volume in the entire 62-row window — higher even than the 2026-07-10 volume of 40,608,900 [market-meta].

Critically, the stock **opened at 526.00 and closed at 539.03**, i.e. it closed in the upper portion of the day's range (524.49–539.88) [market-meta]. **Calculation:** (539.03 − 524.49) / (539.88 − 524.49) = 14.54/15.39 ≈ **94% of the daily range captured to the upside** — operands [market-meta]. That is a genuine intraday reversal/buyer-absorption signature, not a close-on-the-lows capitulation. This nuance matters enormously for the trade construction below.

**Fundamental driver (context, not technical):** Q2 2026 revenue was USD 60.801bn, +28% [src-meta], but operating income fell 8% to 18.775bn with operating margin compressing to 31% from 43% [src-meta]. Costs included 2.40bn of legal charges and 1.18bn of severance [src-meta], and capex was 31.08bn [src-meta]. The market is repricing the margin/capex trajectory, not the top line. Daily active people rose 3% to 3.60bn [src-meta] — engagement is intact.

---

## 3. Trend Structure: Broken Short-Term Uptrend, Now Deeply Oversold

### 3.1 The July rally and its failure
META staged a powerful advance in early-to-mid July:
- 2026-07-01 close 612.91 on 45,536,300 volume [market-meta]
- 2026-07-10 close 669.21 on 40,608,900 volume [market-meta]
- 2026-07-15 close 681.31 — the **highest close in the window** [market-meta]

From there it rolled over: 2026-07-17 close 646.01, 2026-07-22 close 627.17, 2026-07-23 close 606.10, 2026-07-29 close 585.61, then the 2026-07-30 gap to 539.03 [market-meta].

**Calculation:** drawdown from the 2026-07-15 peak close of 681.31 to 539.03 = (539.03 − 681.31)/681.31 = **−20.88%**. Operands [market-meta]. In eleven trading sessions the stock has entered technical bear-market territory. This is a *derived* figure.

### 3.2 Moving averages — all signals point down
- **close_10_ema = 597.37** vs. last close 539.03 [market-meta]. **Calculation:** price is 539.03/597.37 − 1 = **−9.8% below** the 10-EMA. Operands [market-meta]. The short-term average is far overhead and falling; price is not merely below it, it is *dislocated* from it.
- **vwma = 603.43** vs. last close 539.03 [market-meta]. **Calculation:** −10.7% below the volume-weighted average. Operands [market-meta]. This is the more damning of the two: the volume-weighted average price of recent participation sits ~64 points above spot, meaning **the recent volume-weighted cohort is underwater**. Heavy-volume buyers from the July run are trapped, which creates overhead supply on any bounce.
- 50-SMA and 200-SMA: **UNKNOWN / NO_DATA_AVAILABLE** [market-meta]. I explicitly decline to infer them.

### 3.3 MACD — bearish crossover, momentum accelerating negative
- **macd = −3.14**, **macds (signal) = 8.98**, **macdh = −12.12** [market-meta].
- The MACD line has crossed **below** its signal line and both the line and histogram are negative. **Calculation:** macd − macds = −3.14 − 8.98 = −12.12, which reconciles exactly with the reported histogram [market-meta] — internally consistent.
- Interpretation: the crossover is fresh and the histogram is deeply negative, indicating downside momentum is *expanding*, not exhausting. Note the MACD line at −3.14 is only modestly negative while the signal at +8.98 is still positive — this is the classic **early-stage bearish crossover** profile, where the signal line has not yet caught down. Historically that configuration implies further downside follow-through before a base forms. (This is analytical judgment, not a sourced fact.)

### 3.4 RSI — extreme oversold, the loudest signal in the dataset
- **rsi = 13.71** [market-meta]. This is far below the conventional 30 oversold threshold and is an extreme reading.
- Nuance: in a genuine trend break, RSI can stay pinned low, so oversold is **not** a buy signal by itself. However, an RSI in the low teens combined with a close at ~94% of the daily range [market-meta] is a **capitulation-plus-absorption** combination that historically precedes at least a violent reflex bounce. I treat it as a *tactical* signal, not a *strategic* one.

### 3.5 Bollinger Bands — price has broken clean through the lower band
- **boll (middle, 20-SMA) = 622.11**, **boll_ub = 694.96**, **boll_lb = 549.26** [market-meta].
- Last close 539.03 is **below the lower band of 549.26** [market-meta]. **Calculation:** 539.03 − 549.26 =