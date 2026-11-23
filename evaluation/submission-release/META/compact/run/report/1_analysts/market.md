**Role: Market Analyst (nonbinding)**

META, analysis date 2026-07-30, latest close 539.03 [market-meta]. The stock gapped down hard on the Q2 2026 print: open 526.00, low 524.49, close 539.03 on 42.27M shares vs. 22.37M the prior day [market-meta] — a capitulation-volume session. Prior close 585.61 [market-meta], so the drop is roughly -8.0% (calculation: 539.03/585.61 − 1, operands [market-meta]).

Context: META ran from ~563 (2026-06-30) to 681.31 (2026-07-15) [market-meta], then rolled over to 585.61 by 2026-07-29 before the gap. The fundamental trigger is margin compression: revenue +28% to $60.801B but operating income -8% to $18.775B, margin 31% vs 43%, with $2.40B legal and $1.18B severance charges and capex of $31.08B [src-meta]. That is a "growth without earnings leverage" profile — the market is repricing the capex/expense trajectory, not demand.

Indicator selection (8, complementary):
1. **close_10_ema** — fastest read on the gap's damage to short-term momentum.
2. **close_50_sma** — the medium-term trend line now likely broken; key reclaim level.
3. **close_200_sma** — long-term trend check; whether this is a correction or a regime change.
4. **macd** — momentum crossover confirmation of the July top.
5. **macds** — signal-line cross timing.
6. **rsi** — whether the gap produced genuine oversold (potential bounce) or just trend damage.
7. **atr** — essential here: gap-day volatility dictates stop distance and position sizing.
8. **vwma** — volume-weighted confirmation; the 42M-share distribution day is the tell.

Deliberately excluded: boll_ub/boll_lb (bands will be distorted by the gap), macdh (redundant with macd/macds), and stochrsi (redundant with rsi).

Caveats: I have not yet retrieved indicator values, so no exact RSI/MACD/MA levels are asserted here; those must come from get_indicators and be reconciled against the verified snapshot. Valuation multiples and any price targets are UNKNOWN/assumptions, not sourced facts.

| Item | Value / Status | Source |
|---|---|---|
| Ticker / date | META / 2026-07-30 | market-meta |
| Latest close | 539.03 | market-meta |
| Day range | 524.49–539.88 | market-meta |
| Volume | 42.27M (vs 22.37M prior) | market-meta |
| Gap vs prior close | ~-8.0% (calc) | market-meta |
| Q2 rev / op income | $60.801B / $18.775B | src-meta |
| Op margin | 31% vs 43% | src-meta |
| Capex | $31.08B | src-meta |
| Indicators chosen | 10ema, 50sma, 200sma, macd, macds, rsi, atr, vwma | — |
| Valuation / targets | UNKNOWN | — |