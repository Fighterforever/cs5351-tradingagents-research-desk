# NVDA Technical Analysis Report — Role: Market Analyst (nonbinding)

**Ticker:** NVDA | **Analysis date:** 2026-08-27 | **Frozen latest close:** 227.98 USD [market-nvda]

---

## 1. The single most important fact: a post-earnings gap breakout on record volume

The verified snapshot for 2026-08-27 shows NVDA opened at 222.86, traded a range of 220.90–230.47, and closed at 227.98 on volume of 298,909,800 shares [market-nvda]. That is the largest volume print in the entire 82-row window I retrieved (2026-05-01 through 2026-08-27), exceeding the prior peak of 289,410,600 on 2026-05-29 [market-nvda].

Context for the move: the prior session (2026-08-26) closed at 209.66 on 179,900,000 shares [market-nvda], and the official earnings release was dated 2026-08-26 for fiscal Q2 2027 ended July 26, 2026 [src-nvda]. So the 2026-08-27 session is the first full trading session reflecting the report.

**Derived calculation (not a sourced fact):** close-to-close change = (227.98 − 209.66) / 209.66 = +8.74%, using the 2026-08-27 close and 2026-08-26 close, both [market-nvda]. Volume expansion = 298,909,800 / 179,900,000 = 1.66x the prior session, both [market-nvda].

This is a textbook "gap-and-go" confirmation day: price closed in the upper third of the day's range (close 227.98 vs. high 230.47 and low 220.90 [market-nvda]), meaning buyers defended the gap rather than fading it. That is materially more constructive than a gap-up that closes near the low.

**Fundamental backdrop supporting the move** [src-nvda]: revenue of USD 96.2 billion, +18% sequentially and +106% year over year; Data Center revenue of 89.0 billion, +117% year over year; GAAP and non-GAAP gross margins both 75.0%; GAAP EPS 2.46 and non-GAAP EPS 2.22 for the quarter.

**Derived calculation (not a sourced fact):** Data Center share of total revenue = 89.0 / 96.2 = 92.5%, using the two figures above [src-nvda]. This tells you the equity is effectively a single-segment bet on AI infrastructure demand.

**Important valuation caveat:** I have only a single quarter's EPS (GAAP 2.46, non-GAAP 2.22 for fiscal Q2 2027 [src-nvda]). I have no TTM EPS evidence and no share count, so any trailing P/E, forward P/E, or price target multiple is **UNKNOWN** and I will not state one.

---

## 2. Indicator selection and rationale

I selected 8 complementary indicators spanning trend, momentum, volatility, and volume confirmation. Two of my requested indicators returned no data and I will not fabricate them:

- **close_50_sma: NO_DATA_AVAILABLE** — the tool reported it needs 50 rows but only 40 were available at 2026-08-27 [market-nvda].
- **close_200_sma: NO_DATA_AVAILABLE** — needs 200 rows, only 40 available [market-nvda].

This is a genuine analytical limitation, not a minor one: I **cannot** verify a golden cross, a death cross, or whether price sits above or below its long-term trend benchmark. Any claim about the 200-day trend for NVDA would be invented. I flag this explicitly rather than substituting an estimate.

The 8 indicators I did obtain:

| Indicator | Value (2026-08-27) | What it tells us |
|---|---|---|
| close_10_ema | 217.08 | Short-term trend anchor |
| macd | 2.93 | Momentum level |
| macds | 3.60 | Momentum signal line |
| macdh | −0.67 | Momentum gap (negative) |
| rsi | 53.50 | Momentum/overbought gauge |
| atr | 6.51 | Volatility for stops/sizing |
| boll (middle) | 217.21 | 20-SMA basis |
| boll_ub | 231.57 | Upper band |
| boll_lb | 202.85 | Lower band |
| vwma | 209.92 | Volume-weighted trend |

All values [market-nvda].

---

## 3. Trend structure: short-term bullish, medium-term range-bound, long-term UNKNOWN

**Short-term (bullish).** Close 227.98 sits 10.90 above the 10-EMA of 217.08 [market-nvda]. **Derived calculation:** (227.98 − 217.08) / 217.08 = +5.02% premium to the 10-EMA, both operands [market-nvda]. A 5% premium to a 10-period EMA is a stretched but not extreme reading — it signals genuine short-term thrust rather than a slow drift.

**Medium-term (range-bound, now resolving upward).** The Bollinger middle band (20-SMA) is 217.21 and the 10-EMA is 217.08 — essentially identical [market-nvda]. That convergence tells you the prior 20 sessions were a low-directional consolidation, not a trend. The close of 227.98 is 10.77 above the middle band [market-nvda], i.e. **derived:** +4.96% above the 20-SMA.

Critically, the close of 227.98 is **inside** the upper band of 231.57 but well above the middle [market-nvda]. It has not yet closed above the upper band, so this is a strong push into the upper channel rather than a confirmed band breakout. Band width: **derived** (231.57 − 202.85) / 217.21 = 13.2% of the middle band, both operands [market-nvda] — a moderately wide envelope consistent with the elevated volatility of the past three months.

**Long-term: UNKNOWN.** No 200-SMA available [market-nvda]. I will not characterize the primary trend.

**The medium-term range, stated precisely from actual closes** [market-nvda]:
- Range low close in the window: 190.01 on 2026-07-29.
- Range high close before today: 225.30 on 2026-08-13 (with 225.16 on 2026-08-14 and 225.01 on 2026-08-17 forming a triple rejection zone near 225).
- Today's close of 227.98 on 2026-08-27 clears that 225.0–225.3 cluster decisively.

This is the cleanest structural read in the data: NVDA spent mid-August repeatedly failing at ~225, then gapped through it on 1.66x volume. Prior resistance at ~225.0–225.3 [market-nvda] is the level to watch as potential support on any retest.

---

## 4. Momentum: the one genuine warning sign

This is where nuance matters, and where a naive read would mislead.

- **RSI is 53.50** [market-nvda]. That is dead-center neutral. After an +8.74% day (**derived** from 227.98 and 209.66 [market-nvda]), an RSI of only 53.5 is notable — it means the preceding weeks were weak enough that one explosive session only returned momentum to the middle of the range. There is **no overbought condition** and therefore no RSI-based reason to expect mean reversion. RSI has substantial room before the 70 threshold.

- **MACD is 2.93, signal is 3.60, histogram is −0.67** [market-nvda]. The MACD line remains **below** its signal line