# AMZN Technical Analysis Report
**Role: Market Analyst (Technical)** — nonbinding role analysis, not a transaction proposal.
**Ticker:** AMZN | **Analysis date:** 2026-07-31 | **Latest close:** 271.58 USD [market-amzn]

---

## 1. Data Integrity & Scope Notes (read first)

Two important constraints shape this report:

1. **Long moving averages are unavailable.** Both `close_50_sma` and `close_200_sma` returned `NO_DATA_AVAILABLE` — the frozen CSV window at 2026-07-31 contains only 30 rows, while those indicators require 50 and 200 rows respectively [market-amzn]. I will **not** estimate or fabricate these values. Consequently, I cannot make any claim about a golden cross, death cross, or long-term trend regime based on the 50/200 SMA pair. Any such claim would be unsupported.
2. **The verified snapshot is the source of truth for exact price levels.** The snapshot confirms last close 271.58, open 265.00, day high 273.23, day low 262.01, volume 129,054,800 on 2026-07-31 [market-amzn]. The full OHLCV history I retrieved is consistent with this row; no discrepancy to flag.

**Critical context:** 2026-07-31 is the session *immediately following* the Q2 2026 earnings release (announced 2026-07-30) [src-amzn]. The single most important technical fact in this report is that the entire indicator set below is **contaminated by a one-day, event-driven repricing**. Indicators computed "as of 2026-07-31" are largely describing the pre-earnings regime plus one shock bar.

---

## 2. The Price Action: A Violent Regime Break

### 2.1 The earnings-day gap
On 2026-07-30, AMZN closed at 235.50 on volume of 101,839,800 [market-amzn]. On 2026-07-31 it opened at 265.00, traded a range of 262.01–273.23, and closed at 271.58 on volume of 129,054,800 [market-amzn].

Derived calculation (operands cited, result is a calculation not a sourced fact):
- Close-to-close move: (271.58 − 235.50) / 235.50 = **+15.32%** [market-amzn]
- Open-to-close move on 2026-07-31: (271.58 − 265.00) / 265.00 = **+2.48%** [market-amzn]
- Volume expansion vs. the 2026-07-30 session: 129,054,800 / 101,839,800 = **1.27×** [market-amzn]

The interpretation matters: the gap did most of the work, but the stock **kept buying through the session** and closed near the high (271.58 vs. day high 273.23, i.e. within ~0.6% of the high) [market-amzn]. That is a "gap-and-go" structure, not a "gap-and-fade." Gap-and-fade would have shown a close well below the open; it did not.

### 2.2 The preceding downtrend that this breaks
The stock spent roughly two months bleeding lower before the print:
- 2026-05-06 close: 274.99 [market-amzn]
- 2026-06-25 close: 227.01 [market-amzn] — the swing low in the visible window
- 2026-07-22 close: 244.85, then a sharp five-session slide to 226.65 on 2026-07-29 [market-amzn]

Derived: (227.01 − 274.99) / 274.99 = **−17.45%** from the 2026-05-06 close to the 2026-06-25 close [market-amzn]. And (226.65 − 244.85) / 244.85 = **−7.43%** in the five sessions from 2026-07-22 to 2026-07-29 [market-amzn].

So the setup into earnings was a **lower-highs downtrend with a fresh momentum breakdown in the final week** — the stock closed at 226.65 on 2026-07-29, just above the June low of 227.01 [market-amzn]. The 2026-07-31 close of 271.58 is **+19.8% above** that 2026-07-29 close [market-amzn]. This is a textbook failed-breakdown / bear-trap reversal, and it is the dominant technical event of the period.

### 2.3 Where price now sits relative to the visible range
- Highest close in the visible window: 274.99 on 2026-05-06 [market-amzn]
- Current close 271.58 is **−1.24%** below that [market-amzn]
- Highest intraday high in the window: 278.56 on 2026-05-05 [market-amzn]; current close is **−2.51%** below it [market-amzn]

In other words, one session of buying has erased the entire two-month decline and returned AMZN to the top of its visible range. That is a powerful but *unconfirmed* breakout — it has not yet made a new high on a closing basis.

---

## 3. Indicator-by-Indicator Read

### 3.1 Short-term trend: 10 EMA — 242.70 [market-amzn]
Price at 271.58 sits **+11.9% above** the 10 EMA of 242.70 [market-amzn] (calculation: (271.58 − 242.70) / 242.70). This is an extreme extension. For context, the 10 EMA is still anchored to the pre-earnings price cluster in the 230s–240s, so it will take several sessions to "catch up."

**Actionable implication:** Buying at 271.58 means paying ~12% above the short-term mean. Historically, extensions of this magnitude in a single session tend to mean-revert toward the 10 EMA at least partially, *unless* the move is the start of a genuine new trend leg. The correct posture is to let the 10 EMA rise toward price rather than chase.

### 3.2 Momentum: MACD complex — MACD 0.08, Signal −0.84, Histogram +0.91 [market-amzn]
This is the most informative and most *misleading* reading in the set. The MACD line has just crossed **above** its signal line (0.08 > −0.84), producing a positive histogram of +0.91 [market-amzn]. Mechanically that is a bullish crossover.

But note the absolute levels: the MACD line at **0.08** is essentially at zero [market-amzn]. A crossover occurring at the zero line, driven by a single 15% gap, is a **low-quality signal** — it reflects one bar's arithmetic, not a sustained momentum shift. The MACD line has not yet cleared zero decisively, and the histogram's +0.91 is tiny relative to the 9.26 ATR [market-amzn].

**Actionable implication:** Treat this as a *nascent* bullish crossover requiring confirmation. Confirmation = MACD line pushing clearly positive and the histogram expanding over the next 3–5 sessions. If the histogram rolls over within a week, the crossover was a gap artifact.

### 3.3 Momentum: RSI — 64.04 [market-amzn]
RSI at 64.04 is in bullish territory but **below the 70 overbought threshold** [market-amzn]. This is genuinely notable: a +15.3% single-day move that leaves RSI at only 64 tells you the *prior* RSI was deeply depressed (the stock had been sold hard into the print). RSI has room to run before hitting overbought.

**Actionable implication:** Unlike the 10 EMA extension, RSI is *not* screaming "exhaustion." This is a mild positive for continuation. However, RSI computed on a 