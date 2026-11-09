# Research Desk Analysis Report

- Company (legal identity): Apple Inc.
- Ticker: AAPL
- Analysis date: 2026-07-31
- Evidence latest close: 308.91 USD [source: market-aapl, market CSV as-of 2026-07-31]
- Official earnings source: src-aapl
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

## I. Analyst Team Reports

### Market Analyst
**Role: Market Analyst (technical) — nonbinding analysis**

**Verified facts:** AAPL last close 308.91 on 2026-07-31, open 304.81, high 310.69, low 300.00, volume 132,489,100 [market-aapl].

**The setup: a post-earnings gap-down into a strong uptrend.** AAPL closed 338.19 on 2026-07-29, then 333.43 on 2026-07-30, then gapped to 308.91 on 2026-07-31 — a one-day decline of 24.52 points from 333.43, i.e. −7.35% (calculation: (308.91−333.43)/333.43; both operands [market-aapl]). Volume 132.5M vs. the ~40–60M typical of July [market-aapl] confirms distribution, not drift. The catalyst is the Q3 FY2026 print (revenue 109.4B, +16% y/y; EPS 2.02, +29%, both including tariff-refund benefit of ~2pp gross margin and 0.11 EPS) [src-aapl] — the market is discounting the *quality* of that beat, since the refund is non-recurring.

**Indicators (all [market-aapl]):**
- 10 EMA 327.24 vs. close 308.91 → price 18.33 below (−5.6%), a decisive short-term breakdown.
- MACD 6.82 below signal 8.14 → bearish crossover, histogram negative; momentum has flipped.
- RSI 45.08 → neutral, not oversold. Room to fall further; no capitulation signal.
- Bollinger upper 344.51; price is far below it, consistent with a band-walk reversal.
- ATR 9.90 → daily range ~3.2% of price; the 24.5-point drop is ~2.5 ATR, an outlier move.
- 50/200 SMA: **NO_DATA_AVAILABLE** (insufficient window). I will not estimate them; medium/long-term trend confirmation is UNKNOWN.

**Actionable read:** The 300.00 intraday low [market-aapl] is the only verified support level — it held on the gap day. A close below 300.00 opens further downside; reclaiming 327.24 (10 EMA) would be the first sign the gap is being repaired. RSI at 45 means don't chase the bounce blindly. Valuation multiples and P/E are UNKNOWN (single-quarter EPS 2.02 cannot establish a trailing P/E) [src-aapl].

| Item | Value | Source |
|---|---|---|
| Close 2026-07-31 | 308.91 | market-aapl |
| Day range | 300.00–310.69 | market-aapl |
| Volume | 132.49M | market-aapl |
| 1-day change | −7.35% (from 333.43) | calc, market-aapl |
| 10 EMA | 327.24 | market-aapl |
| MACD / Signal | 6.82 / 8.14 (bearish) | market-aapl |
| RSI | 45.08 (neutral) | market-aapl |
| Bollinger UB | 344.51 | market-aapl |
| ATR | 9.90 | market-aapl |
| 50/200 SMA | UNKNOWN (no data) | market-aapl |
| Q3 FY26 rev / EPS | 109.4B / 2.02 | src-aapl |
| Key support | 300.00 (verified low) | market-aapl |

### News Analyst
**Role: News Researcher (nonbinding role analysis)**

**Data availability:** Only the official earnings source is in the frozen corpus. Global news, FRED macro series (CPI, fed funds, 10Y), and prediction markets all returned NO_DATA_AVAILABLE. I will not estimate or fabricate those values; macro and event-probability commentary is therefore UNKNOWN.

**Company news (only available source):**
- Apple fiscal Q3 2026 ended June 27; revenue USD109.4bn, +16% y/y [src-aapl].
- Gross margin 50.1%, including ~2pp of tariff-refund benefit [src-aapl].
- Diluted EPS 2.02 (quarterly, FQ3 2026), +29%, including 0.11 of tariff-refund benefit [src-aapl].
- Dividend 0.27/share [src-aapl].

**Analytical read (calculations, not sourced facts):**
- Ex-refund EPS ≈ 2.02 − 0.11 = 1.91; ex-refund growth ≈ 1.91/1.58 − 1 ≈ +21% (implied prior-year base 2.02/1.29 ≈ 1.57). Operands: 2.02, +29%, 0.11 [src-aapl]. So ~38% of the EPS growth rate is refund-driven — quality of beat is lower than headline.
- Ex-refund gross margin ≈ 48.1% (50.1% − ~2pp) [src-aapl] — still strong, but the tariff refund is non-recurring.
- Trailing P/E: UNKNOWN. Only a single-quarter EPS (2.02) is available; no TTM EPS evidence exists in the corpus, so no trailing multiple can be computed against the 308.91 close [market-aapl].
- Price context: latest close 308.91 USD, analysis date 2026-07-31 [market-aapl]. No volume/technical data was returned, so trend signals are UNKNOWN.

**Actionable insights:**
1. Treat the 16% revenue growth and 29% EPS growth as partly one-off; model FQ4 on ex-refund margin (~48%) and ex-refund EPS (~1.91) to avoid over-extrapolating [src-aapl].
2. Watch for tariff-refund reversal risk in future quarters — a ~2pp margin headwind is embedded in the base [src-aapl].
3. Macro rates, inflation, and Fed-cut odds are unavailable in this corpus; do not assume a rate path. Any valuation or target must be labeled an assumption, not a sourced fact.

| Item | Value | Source / Status |
|---|---|---|
| Ticker / date / close | AAPL / 2026-07-31 / 308.91 USD | market-aapl |
| FQ3 2026 revenue | 109.4bn, +16% y/y | src-aapl |
| FQ3 2026 diluted EPS | 2.02, +29% (quarterly) | src-aapl |
| Tariff-refund benefit | ~2pp GM; 0.11 EPS | src-aapl |
| Ex-refund EPS (calc) | ~1.91, ~+21% y/y | calc from src-aapl |
| Ex-refund GM (calc) | ~48.1% | calc from src-aapl |
| Dividend | 0.27/share | src-aapl |
| Trailing P/E | UNKNOWN (no TTM EPS) | — |
| CPI / Fed funds / 10Y | UNKNOWN | NO_DATA_AVAILABLE |
| Fed-cut & recession odds | UNKNOWN | NO_DATA_AVAILABLE |

## II. Research Team Decision

### Bull Researcher

Bull Analyst: **Role: Bull Researcher — nonbinding analysis**

Let me open by conceding what's true, then show why the bear case is weaker than it looks.

**The growth story is real, even stripped of the refund.** Yes, the tariff refund is non-recurring — ~2pp of gross margin and 0.11 of EPS [src-aapl]. But do the math the bears want you to do: ex-refund EPS ≈ 1.91, still ~+21% y/y (calc: 2.02−0.11=1.91; implied base 2.02/1.29≈1.57; 1.91/1.57−1≈+21%) [src-aapl]. Ex-refund gross margin ≈48.1% [src-aapl]. A company growing EPS 21% and holding ~48% margins *after* removing the one-off is not a deteriorating business — that's a franchise. Revenue +16% to 109.4B [src-aapl] is the headline the bear keeps skipping past.

**The selloff is a sentiment event, not a fundamentals event.** The −7.35% gap (333.43→308.91) [market-aapl] is ~2.5 ATR on 132.5M volume [market-aapl] — that's forced distribution and de-risking, not a repricing of the earnings power I just laid out. Critically, the 300.00 low *held* on the gap day [market-aapl]. Buyers defended it. RSI 45.08 is neutral, not broken [market-aapl] — the market hasn't capitulated, which means the panic is contained, not terminal.

**Countering the bear's likely points before they land:**
- *"The beat was low quality."* Partly true, and I've already haircut it. But 21% ex-refund EPS growth and 48% ex-refund margins [src-aapl] still beat most large-cap tech. Quality concern ≠ value destruction.
- *"Momentum flipped — MACD bearish, price below 10 EMA."* Correct [market-aapl], but these are lagging, short-horizon signals after a one-day shock. The 50/200 SMA are UNKNOWN (no data) [market-aapl] — the bear cannot claim a broken long-term trend, because that evidence doesn't exist. Absence of confirmation cuts both ways; don't let the bear weaponize it one direction.
- *"Valuation is stretched."* Trailing P/E is UNKNOWN — no TTM EPS in the corpus [src-aapl]. Any "expensive" claim is an assumption, not a fact. I won't assert cheap either; I'll assert the bear can't prove expensive.

**What I'm watching, honestly:** reclaiming the 10 EMA at 327.24 would confirm gap repair [market-aapl]; a close below 300.00 would invalidate my support thesis [market-aapl]. That's my risk line, labeled as judgment, not fact.

**Bottom line:** A 16%-revenue, 21%-ex-refund-EPS grower with ~48% margins [src-aapl], sold off on a one-off-quality scare into verified support that held [market-aapl], is an opportunity — not a warning. The bear is pricing the refund; I'm pricing the franchise.

### Bear Researcher

Bear Analyst: **Role: Bear Researcher — nonbinding analysis**

Bull, you keep calling this a "sentiment event." The tape disagrees. A −7.35% gap (333.43→308.91) on 132.5M volume versus ~40–60M typical July volume [market-aapl] is *institutional distribution* — the people with the most information chose to exit at these prices. You call that "forced de-risking"; I call it a verdict on the print.

**On "21% ex-refund growth is a franchise":** You did the haircut, then spent it. ~38% of the headline 29% EPS growth was refund-driven (calc: 0.11/2.02 of the beat; operands [src-aapl]). And here's what you skip: the refund is *non-recurring*, so next quarter's base carries a ~2pp margin headwind with no offset [src-aapl]. You're extrapolating a growth rate that structurally decelerates. That's not a franchise — that's a comp problem waiting to print.

**On "300 held, buyers defended it":** One intraday low is not support — it's a single data point. Price closed at 308.91, just 2.9% above it [market-aapl]. RSI 45.08 is *neutral*, which is your own problem: there's no capitulation, no washout, no oversold bounce fuel. Momentum has room to bleed. MACD 6.82 vs. signal 8.14 is a confirmed bearish crossover [market-aapl] — you dismiss it as "lagging," but lagging indicators are exactly what confirm a trend *after* a shock. Price sits 18.33 below the 10 EMA (−5.6%) [market-aapl]. That's not contained panic; that's a broken short-term structure.

**On the 50/200 SMA:** You're right they're UNKNOWN [market-aapl] — and you're weaponizing that absence. Fine. But the *verified* evidence I do have all points one direction: below 10 EMA, bearish MACD, distribution volume, no oversold relief. I don't need the long-term trend to make the near-term case. You need it to rescue yours.

**On valuation:** Agreed, trailing P/E is UNKNOWN — no TTM EPS [src-aapl]. But you've inverted the burden. I'm not claiming "expensive"; I'm claiming *you cannot underwrite a 308.91 entry* [market-aapl] without a multiple, and you don't have one. That's not a bull case — that's a hope.

**The asymmetry you're ignoring:** Downside is defined and close — a close below 300.00 opens air, with no verified support beneath it [market-aapl]. Upside requires reclaiming 327.24 just to *repair* the gap [market-aapl] — a 5.9% climb before the thesis even starts working. You're asking investors to buy a falling knife with a one-off-inflated beat, a decelerating comp, and a 6% hole to climb out of.

**Bottom line:** AAPL, analysis date 2026-07-31, latest close 308.91 [market-aapl]. The market repriced the *quality* of this beat and it was right to. Wait for 300 to break or 327 to reclaim — don't buy the middle.

### Research Manager
**Recommendation**: Hold

**Rationale**: Both sides landed real blows, and neither closed the argument. The bull's strongest point is that the fundamentals survive the haircut: revenue +16% to 109.4B, and ex-refund EPS ≈1.91 still implies roughly +21% y/y growth with ex-refund gross margin ≈48.1% (calc: 2.02−0.11=1.91; base 2.02/1.29≈1.57; 1.91/1.57−1≈+21%) [src-aapl]. That is not a deteriorating franchise, and the bear never disproved it — the bear only argued the growth rate decelerates because the ~2pp refund benefit doesn't repeat [src-aapl]. That's a comp headwind, not evidence of value destruction.

The bear's strongest point is procedural and it wins on the tape: a −7.35% gap (333.43→308.91) on 132.5M volume [market-aapl] is distribution, MACD 6.82 vs signal 8.14 is a confirmed bearish crossover, and price sits 18.33 (−5.6%) below the 10 EMA at 327.24 [market-aapl]. RSI 45.08 is neutral [market-aapl], so there is no washout to buy. The bull's "300 held" is one intraday low with the close only 2.9% above it [market-aapl] — thin evidence for support.

Where the bear overreaches: the 50/200 SMA are UNKNOWN [market-aapl], so no broken long-term trend is established, and trailing P/E is UNKNOWN because there is no TTM EPS in the corpus [src-aapl] — so "expensive" is unproven. But the bull equally cannot underwrite a 308.91 entry [market-aapl] without a multiple. Both valuation claims are assumptions, and they cancel.

Net: a genuinely good ex-refund business, priced off a one-off-inflated beat, in a confirmed short-term downtrend with no oversold relief and no valuation anchor. That is balanced evidence, not a conviction call in either direction. Hold — do not add into the gap, do not exit a franchise on a sentiment print.

**Strategic Actions**: Maintain the existing AAPL position at current size; no new capital deployed at 308.91 [market-aapl]. Set two judgment-based (ASSUMPTION, not sourced fact) triggers: (1) add on a close above 327.24, the 10 EMA, which would confirm gap repair [market-aapl] — scale in roughly one-third of intended add per confirming close; (2) trim toward the low end of the target band on a close below 300.00, where no verified support exists beneath [market-aapl]. Between those levels, do nothing. Cap total AAPL exposure at the current allocation until a trailing P/E can be computed from actual TTM EPS — that input is UNKNOWN [src-aapl] and must be sourced before any size increase. Position sizes and trigger levels are analyst judgment, not sourced facts.

## III. Trading Team Plan

### Trader
**Action**: Hold

**Reasoning**: The tape and the fundamentals genuinely cancel: a −7.35% gap (333.43→308.91) on 132.5M volume with MACD 6.82 below signal 8.14 and price 18.33 (−5.6%) under the 10 EMA at 327.24 is confirmed short-term distribution, while the ex-refund business (EPS ≈1.91, ≈+21% y/y, gross margin ≈48.1%) shows no franchise damage. RSI 45.08 is neutral, so there is no washout to buy, and with 50/200 SMA and trailing P/E both UNKNOWN there is no trend or valuation anchor to justify either adding at 308.91 or exiting. Hold at current size, do nothing between 300.00 and 327.24, and let the verified levels decide.

**Entry Price**: 308.91

**Stop Loss**: 300.0

**Position Sizing**: Maintain existing AAPL allocation; no new capital at 308.91. Cap total exposure at current size until a trailing P/E can be computed from actual TTM EPS (UNKNOWN). On a close above 327.24 (10 EMA), scale in ~1/3 of intended add per confirming close; on a close below 300.00, trim toward the low end of the target band. ATR 9.90 (~3.2% of price) implies roughly 1 ATR of noise around the 300.00 support — treat 300.00 as a close-based trigger, not an intraday touch.

FINAL TRANSACTION PROPOSAL: **HOLD**

## IV. Risk Management Team Decision

### Aggressive Analyst

Aggressive Analyst: I'm the Aggressive Risk Analyst, and I'll say this plainly: the trader's HOLD is the right call, but not for the timid reasons the cautious camp will reach for. Let me preempt and dismantle those arguments before they're even made.

To the conservative analyst's inevitable "the beat was fake, the refund is non-recurring, get out": you're half right and fully wrong on the conclusion. Yes, ex-refund EPS is ~1.91 and ex-refund gross margin ~48.1% (calc: 2.02−0.11; 50.1%−~2pp) [src-aapl]. But 48% gross margin and +21% ex-refund EPS growth is a franchise still compounding at a rate most mega-caps would kill for. You're treating a one-off tax benefit as if it were a deterioration. It isn't — it's a normalization. The market already discounted it in the −7.35% gap (333.43→308.91) [market-aapl]. Selling into that discount is selling the news after the news is priced.

To the neutral analyst's "RSI 45, no washout, no anchor, do nothing": that's not a strategy, that's paralysis dressed as discipline. You correctly note 50/200 SMA and trailing P/E are UNKNOWN [market-aapl]. But UNKNOWN is not bearish — it's simply unmeasured. The verified support at 300.00 held on the gap day [market-aapl], and ATR 9.90 means the 24.5-point drop was ~2.5 ATR — an outlier, not a trend [market-aapl]. Outliers mean-revert. That's the asymmetry the cautious crowd keeps missing: downside to 300.00 is ~2.9% (calc: (308.91−300)/308.91), while a repair to the 10 EMA at 327.24 is ~+5.9% (calc: (327.24−308.91)/308.91) [market-aapl]. The reward-to-risk on the *trigger* is roughly 2:1 in favor of the upside — and that's before any re-rating.

Here's where I push the trader to be bolder than "do nothing." The plan's scale-in on a close above 327.24 is correct but too passive. I'd argue for pre-positioning a starter tranche near 300–305, because the 300.00 low is a *verified* floor [market-aapl] and the fundamentals show no franchise damage [src-aapl]. Waiting for 327.24 confirmation means surrendering ~6% of upside to buy comfort. That's a conservative tax, not risk management.

The honest caveat I'll own: trailing P/E is genuinely UNKNOWN — no TTM EPS exists in the corpus [src-aapl], so I won't fabricate a valuation anchor. And macro is NO_DATA_AVAILABLE. That's exactly why the trader's close-based 300.00 stop (not intraday) is smart — it respects ATR noise while capping downside.

Bottom line: HOLD is correct, but frame it as a coiled spring, not a bunker. The cautious analysts will call this distribution; I call it a discounted entry into a 48%-margin compounder. Ticker AAPL, analysis date 2026-07-31, latest close 308.91 [market-aapl]. Nonbinding role analysis.

### Conservative Analyst

Conservative Analyst: I'm the Conservative Risk Analyst. Let me be direct with the Aggressive Analyst, because his case rests on a word he keeps using loosely: "verified."

He calls 300.00 a "verified floor." It is not a floor. It is a single intraday low from one session [market-aapl]. One touch is a data point, not a support structure. He then builds a 2:1 reward-to-risk ratio on top of it — but that ratio is an assumption dressed as arithmetic. The downside to 300.00 is ~2.9% only if 300.00 holds; if it breaks, the next verified level is UNKNOWN, because 50/200 SMA returned NO_DATA_AVAILABLE [market-aapl]. So his "2.9% downside" has no defined floor beneath it. That is precisely the kind of unbounded tail a conservative mandate exists to avoid.

His "outliers mean-revert" claim is the most dangerous line in the debate. A −7.35% gap on 132.5M volume versus ~40–60M typical [market-aapl] is not noise — it is distribution on conviction volume. MACD 6.82 below signal 8.14 confirms momentum has flipped [market-aapl]. RSI 45.08 is neutral, not oversold [market-aapl] — meaning there is no exhaustion signal, no capitulation, no reason to believe the selling is finished. Mean reversion is a hope, not a measured fact.

And his "the market already priced the refund" assertion is unverifiable. We have no TTM EPS, so trailing P/E is UNKNOWN [src-aapl]. Without a valuation anchor, nobody — including him — can claim the gap fully discounted anything. He admits this, then proceeds as if it were settled.

His proposal to pre-position a starter tranche at 300–305 is the real problem. That adds capital into a confirmed short-term breakdown, ahead of any confirmation, with no valuation anchor and no macro data (NO_DATA_AVAILABLE). He calls waiting for 327.24 a "conservative tax" of ~6%. I call it the price of not buying into a falling knife. The firm's assets are better served by forgoing uncertain upside than by funding an unhedged entry on a one-touch low.

To the Neutral Analyst, who hasn't spoken: silence in the face of a 2.5-ATR distribution day is itself a position. "Do nothing" is fine only if paired with a hard, close-based risk trigger — which the trader has, at 300.00. I endorse that discipline and would tighten it: no new capital, cap exposure at current size, and treat any close below 300.00 as a trim signal, not a buying opportunity.

The Aggressive Analyst wants a coiled spring. I see a stock that gapped down 7.35% on heavy volume, sits 5.6% under its 10 EMA, has neutral RSI with room to fall, and offers no valuation or trend anchor. HOLD at current size is correct — but as a bunker, not a spring. Ticker AAPL, analysis date 2026-07-31, latest close 308.91 [market-aapl]. Nonbinding role analysis.

### Neutral Analyst

Neutral Analyst: I'm the Neutral Risk Analyst. Both of you are building confident structures on a single session's data, and each of you is overreaching in a mirror-image way.

Aggressive, your "verified floor" is the weakest link, and the Conservative is right to hit it. 300.00 is one intraday low [market-aapl], not a support structure. But your 2:1 ratio isn't pure fiction either — it's a conditional calculation: (308.91−300)/308.91 ≈ 2.9% vs (327.24−308.91)/308.91 ≈ 5.9% [market-aapl]. The honest framing is that it's a ratio *if* 300 holds, and you presented it as if it were settled. That's the overreach. Your "outliers mean-revert" is also a hope, not a measured fact — a 2.5-ATR move on 132.5M volume [market-aapl] is a distribution signal, and RSI 45.08 [market-aapl] gives no exhaustion evidence. Pre-positioning at 300–305 ahead of confirmation adds capital into a confirmed breakdown with no valuation anchor. That's not boldness; it's paying full price for an unmeasured tail.

Conservative, your discipline is sound but your framing is too absolute. You correctly note the next level below 300 is UNKNOWN [market-aapl] — but that cuts both ways. You can't call the downside "unbounded" and simultaneously refuse to size against it; the trader's close-based 300 trigger is exactly the mechanism that bounds it. And your "distribution on conviction volume" is a reasonable read, not a proven one — one heavy day after a non-recurring-refund print [src-aapl] is equally consistent with a repricing that completes, not a trend that continues. Treating it as certain is the same error you accuse the Aggressive of. Your "bunker" also risks anchoring to fear when the ex-refund franchise still shows ~48.1% gross margin and ~+21% EPS growth [src-aapl, calc].

Here's the moderate synthesis. The trader's HOLD is correct, and the close-based 300.00 trigger is the right instrument — but it should be symmetric, not one-directional. I'd add a defined re-entry ladder rather than the Aggressive's blind pre-positioning: no new capital at 308.91, but authorize a small starter tranche only on a *close* that stabilizes above 300.00 with volume normalizing below the 132.5M gap-day print [market-aapl] — that's confirmation, not a guess. On the upside, keep the 327.24 (10 EMA) scale-in [market-aapl] as the trader wrote. Cap total exposure at current size until a trailing P/E can be computed from actual TTM EPS, which remains UNKNOWN [src-aapl]. And explicitly label the 300.00 and 327.24 levels as assumptions/judgment, not sourced facts.

That gives you the Aggressive's participation if the gap repairs, the Conservative's hard floor if it doesn't, and neither camp's overconfidence. Ticker AAPL, analysis date 2026-07-31, latest close 308.91 [market-aapl]. Nonbinding role analysis.

## V. Portfolio Manager Decision

### Portfolio Manager
**Rating**: Hold

**Executive Summary**: Maintain the existing AAPL position at current size; deploy no new capital at 308.91 [market-aapl]. Treat 300.00 as a close-based trim trigger and 327.24 (10 EMA) as the scale-in confirmation level — both are analyst judgment (ASSUMPTION), not sourced facts [market-aapl]. Cap total exposure at current size until a trailing P/E can be computed from actual TTM EPS, which is UNKNOWN [src-aapl]. Horizon: 3-6 months, letting verified levels decide.

**Investment Thesis**: The debate resolves to a genuine standoff, and the Neutral Analyst's synthesis is the most defensible read. Bull case: the ex-refund franchise is intact — revenue 109.4B, +16% y/y, ex-refund EPS ≈1.91 (2.02−0.11) implying ≈+21% y/y, ex-refund gross margin ≈48.1% (50.1%−~2pp) [src-aapl, calc]. That is normalization, not deterioration, and the Conservative never disproved it. Bear case wins on the tape: a −7.35% gap (333.43→308.91) on 132.5M volume, MACD 6.82 below signal 8.14, price 18.33 (−5.6%) under the 10 EMA at 327.24, RSI 45.08 neutral with no washout [market-aapl]. That is distribution, not exhaustion.

Both extremes overreach. The Aggressive's "verified floor" at 300.00 is one intraday low, and his 2:1 ratio is conditional, not settled — pre-positioning at 300–305 funds an unmeasured tail with no valuation anchor. The Conservative's "unbounded downside" is equally overstated: the close-based 300.00 trigger is precisely the mechanism that bounds it, and 50/200 SMA are UNKNOWN [market-aapl], so no broken long-term trend is established. Trailing P/E is UNKNOWN because no TTM EPS exists in the corpus [src-aapl] — so "expensive" and "already discounted" are both unproven and cancel.

I adopt the Neutral's symmetric structure: no capital at 308.91; a small starter tranche only on a close stabilizing above 300.00 with volume normalizing below the 132.5M gap-day print; scale in ~1/3 of intended add per confirming close above 327.24; trim toward the low end of the band on a close below 300.00. ATR 9.90 (~3.2% of price) means 300.00 must be close-based, not intraday [market-aapl]. Good business, one-off-inflated beat, confirmed short-term downtrend, no valuation anchor — balanced evidence, no conviction either way. Ticker AAPL, analysis date 2026-07-31, latest close 308.91 [market-aapl].

**Time Horizon**: 3-6 months
