I now have all the data I need. Let me compile my analysis as a trading assistant (market analyst role).

Let me analyze the data:

**Verified snapshot (2026-07-30):**
- Last close: $539.03
- Open: $526.00, High: $539.88, Low: $524.49
- Volume: 42,271,500 (extremely elevated)

**Key observations from price data:**
- The stock was trading around $608-635 in late May
- It declined through June to a low around $540-550
- It spiked to $681 on July 15, then declined sharply
- On July 29-30, there was a massive selloff: from $585.61 (July 29 close) to $539.03 (July 30 close), a drop of ~8%
- July 30 opened at $526, hit a low of $524.49, closed at $539.03
- Volume on July 30 was 42.27M shares, the highest in the dataset (vs ~10-20M typical)

**Indicators:**
- 10 EMA: $597.37 (price well below)
- MACD: -3.14, Signal: +8.98, Histogram: -12.12 (bearish crossover, negative momentum)
- RSI: 13.71 (deeply oversold, below 30)
- Bollinger Middle: $622.11, Upper: $694.96, Lower: $549.26 (price below lower band)
- ATR: $24.36 (elevated volatility)
- VWMA: $603.43 (price well below volume-weighted average)
- 50 SMA and 200 SMA: NO_DATA_AVAILABLE (insufficient window)

This aligns with the earnings announcement on 2026-07-29. The earnings showed revenue up 28% but operating income DOWN 8% and operating margin down from 43% to 31%, with $2.40B legal charges and $1.18B severance. The market reacted very negatively.

Let me write my detailed report.

---

# META Technical Analysis Report — Trading Assistant (Market Analyst)

**Ticker:** META | **Analysis date:** 2026-07-30 | **Latest close:** $539.03 [market-meta]

## Market Context & Verified Snapshot

The verified market snapshot for META as of 2026-07-30 confirms a severe one-day breakdown [market-meta]:
- **Last close:** $539.03
- **Open:** $526.00 (gapped down sharply)
- **Day high:** $539.88 | **Day low:** $524.49
- **Volume:** 42,271,500 shares — the highest single-day volume in the entire observed dataset (typical daily volume ranged ~10–20M shares) [market-meta]

This collapse follows the Q2 2026 earnings announcement on 2026-07-29 [src-meta]. While revenue grew 28% to $60.801B, operating income **fell 8%** to $18.775B and operating margin compressed from 43% to 31%, burdened by $2.40B in legal charges and $1.18B in severance [src-meta]. The market's reaction was decisively negative.

## Price Action Timeline (May–July 2026)

The price data reveals a clear three-phase structure [market-meta]:

1. **Late-May consolidation (~$600–635):** META traded in a tight band, peaking at $635.29 on May 28 before drifting lower.

2. **June downtrend (~$540–630):** A persistent decline from ~$635 to a June 25 low of $542.87, with a sharp June 5 drop (from $627.57 to $593.00) and continued weakness through late June.

3. **July spike-and-crash:** A powerful rally from $563.29 (June 30) to an intraday high of $686.08 on July 15 (closing at $681.31), followed by a steady decline into the earnings event. The stock fell from $681.31 (July 15) to $585.61 (July 29), then collapsed to $539.03 on July 30 — a **~8% single-day drop** on record volume.

## Technical Indicator Analysis

### Moving Averages
- **10 EMA: $597.37** [market-meta] — Price ($539.03) is trading **~9.8% below** the 10 EMA, indicating extreme short-term bearish momentum. The price has decisively broken below this fast average.
- **50 SMA & 200 SMA:** NO_DATA_AVAILABLE — insufficient calculation window (needs 50/200 rows, only 30 available) [market-meta]. I will not fabricate these values. Note: the price has fallen well below the Bollinger middle (20 SMA) of $622.11, suggesting it is also below the 50-day trend benchmark.

### MACD (Momentum)
- **MACD line: -3.14** | **Signal: +8.98** | **Histogram: -12.12** [market-meta]
- The MACD line has crossed decisively below the signal line, and the histogram is deeply negative (-12.12). This is a **strong bearish crossover** confirming accelerating downside momentum. The negative histogram magnitude indicates the bearish momentum is intensifying, not stabilizing.

### RSI (Momentum / Overbought-Oversold)
- **RSI: 13.71** [market-meta] — Deeply oversold, far below the 30 threshold. This signals an extreme short-term oversold condition. However, in strong downtrends RSI can remain in oversold territory for extended periods, so this alone is not a buy signal — it flags that a technical bounce is possible but the trend remains down.

### Bollinger Bands (Volatility)
- **Middle (20 SMA): $622.11** | **Upper: $694.96** | **Lower: $549.26** [market-meta]
- Price ($539.03) is trading **below the lower band** ($549.26). This is a classic "band walk" / breakdown condition indicating extreme volatility and a strong downward move. The bands are very wide (upper-lower spread of ~$145.70), reflecting the elevated volatility regime.

### ATR (Volatility)
- **ATR: $24.36** [market-meta] — Elevated volatility. This represents roughly 4.5% of the current price, meaning daily swings of ±$24 are normal. This is critical for position sizing and stop-loss placement.

### VWMA (Volume-Weighted Average)
- **VWMA: $603.43** [market-meta] — Price is trading **~10.7% below** the volume-weighted average, confirming that the recent selling has been heavy-volume-driven. The gap between price and VWMA underscores that distribution (selling) has dominated.

## Indicator Selection Rationale

I selected the following 8 indicators for complementary, non-redundant coverage:
1. **close_10_ema** — Fast trend gauge to capture the immediate breakdown.
2. **macd / macds / macdh** — Momentum crossover system to confirm trend direction and intensity.
3. **rsi** — Overbought/oversold oscillator to flag extreme conditions.
4. **boll / boll_ub / boll_lb** — Volatility bands to identify the breakdown below the lower band.
5. **atr** — Volatility measure for risk management and stop placement.
6. **vwma** — Volume-weighted price to confirm the selling is volume-backed.

I deliberately excluded the 50/200 SMA (data unavailable) and avoided redundant oscillators (e.g., stochastic RSI) since RSI already covers momentum extremes.

## Actionable Insights

1. **Trend is firmly bearish short-term.** Price is below the 10 EMA, below the Bollinger lower band, below VWMA, with a bearish MACD crossover and deeply negative histogram. All momentum and trend signals align to the downside [market-meta].

2. **Extreme oversold condition (RSI 13.71) suggests a technical bounce is possible** in the near term, but this is a counter-trend signal, not a reversal signal. Traders should not interpret oversold RSI as a buy trigger in a confirmed downtrend without additional confirmation (e.g., a bullish MACD crossover or reclaim of the 10 EMA).

3. **Key resistance levels to watch:** The Bollinger lower band ($549.26) now acts as near-term resistance (price must reclaim it to stabilize). Above that, the 10 EMA ($597.37) and VWMA ($603.43) represent stronger resistance zones where sellers previously dominated [market-meta].

4. **Support:** The July 30 intraday low of $524.49 is the immediate support reference. A break below this would open the door to further downside [market-meta].

5. **Volatility management:** With ATR at $24.36, any stop-loss should be sized to accommodate ~1.5–2× ATR (≈$37–49) to avoid being stopped out by normal noise. Position sizes should be reduced given the elevated volatility [market-meta].

6. **Volume confirms distribution:** The 42.27M-share volume on July 30 (vs. ~10–20M typical) confirms institutional selling pressure. Heavy-volume breakdowns often require time to base before stabilizing [market-meta].

## Key Points Summary

| Metric | Value | Signal | Source |
|--------|-------|--------|--------|
| Last Close | $539.03 | — | market-meta |
| Day Range | $524.49 – $539.88 | Wide, bearish | market-meta |
| Volume | 42,271,500 | Record high, distribution | market-meta |
| 10 EMA | $597.37 | Price ~9.8% below (bearish) | market-meta |
| MACD / Signal / Hist | -3.14 / +8.98 / -12.12 | Bearish crossover, intensifying | market-meta |
| RSI | 13.71 | Deeply oversold (<30) | market-meta |
| Bollinger Mid/Up/Low | 622.11 / 694.96 / 549.26 | Price below lower band | market-meta |
| ATR | $24.36 | Elevated volatility | market-meta |
| VWMA | $603.43 | Price ~10.7% below (bearish) | market-meta |
| 50/200 SMA | N/A | Insufficient data | market-meta |
| Q2 Revenue | $60.801B (+28%) | Strong top-line | src-meta |
| Q2 Op Income | $18.775B (-8%) | Margin compression | src-meta |
| Q2 Op Margin | 31% (vs 43%) | Significant decline | src-meta |
| Legal/Severance | $2.40B / $1.18B | Earnings drag | src-meta |

## Conclusion

META is in a **confirmed short-term downtrend** following a sharply negative earnings reaction. All momentum, trend, and volume indicators align bearishly, with the stock trading below its 10 EMA, Bollinger lower band, and VWMA, accompanied by a bearish MACD crossover and record distribution volume. The RSI at 13.71 flags an extreme oversold condition that could produce a technical bounce, but the prevailing trend remains down. Traders should treat any bounce as counter-trend until price reclaims the Bollinger lower band ($549.26) and ideally the 10 EMA ($597.37). Risk management is paramount given ATR of $24.36.

**Note:** This is nonbinding role analysis from the market analyst. The 50/200 SMA values could not be computed due to insufficient data window and were not estimated.