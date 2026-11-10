# Research Desk Analysis Report

- Company (legal identity): Meta Platforms, Inc.
- Ticker: META
- Analysis date: 2026-07-30
- Evidence latest close: 539.03 USD [source: market-meta, market CSV as-of 2026-07-30]
- Official earnings source: src-meta
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

## I. Analyst Team Reports

### Market Analyst
**Role: Market Analyst (nonbinding analysis)**

**Ticker META, analysis date 2026-07-30, latest close 539.03 USD [market-meta].**

**Price action.** META closed 539.03 on 2026-07-30 after opening 526.00 (day range 524.49–539.88) on 42.27M shares [market-meta]. Versus the 2026-07-29 close of 585.61 [market-meta], that is a −7.95% move (calc: (539.03−585.61)/585.61), and the open gapped −10.2% below the prior close (calc: (526.00−585.61)/585.61). Volume of 42.27M vs 22.37M on 2026-07-29 [market-meta] is roughly 1.9x (calc) — a high-conviction, news-driven repricing, not drift.

**Context.** The gap follows the 2026-07-29 announcement: Q2 2026 revenue 60.801B, +28%, but operating income 18.775B, −8%, margin 31% vs 43%, with costs of 42.03B including 2.40B legal charges and 1.18B severance, and capex 31.08B [src-meta]. DAP 3.60B, +3% [src-meta]. The market is repricing margin/capex durability, not demand.

**Indicators (all [market-meta]).**
- 10 EMA 600.99 → price sits 10.3% below it (calc). Short-term trend is broken; the EMA is now overhead resistance.
- VWMA 624.00 → price 13.6% below the volume-weighted average (calc), confirming distribution: recent volume transacted far above spot.
- RSI 13.71 → deeply oversold, far below the 30 threshold. In a gap-driven capitulation this flags stretched downside, but oversold is not a reversal signal on its own.
- ATR 24.36 → ~4.5% of spot (calc). Today's 15.39 high-low range (calc) is *inside* ATR, i.e. the gap did the damage, not intraday range expansion.
- 50 SMA, 200 SMA, MACD, MACD signal: NO_DATA_AVAILABLE (insufficient window in the frozen CSV). I will not estimate them; medium/long-term trend and momentum-cross confirmation are UNKNOWN.

**Actionable read.** Structure is bearish-to-capitulative: price below both the 10 EMA and VWMA with a volume surge. Do not treat 524.49 as validated support — it is only today's low [market-meta], with no tested bounce. ATR-based risk framing: a 1×ATR stop from 539.03 implies ~514.67 (calc, assumption, not a sourced level). Practical stance: wait for either (a) a close back above the 10 EMA (600.99) to confirm repair, or (b) a lower-volume retest holding above 524.49 before adding risk. Any entry/stop/position size is an assumption, not a sourced fact.

| Item | Value | Source |
|---|---|---|
| Close / Open / High / Low | 539.03 / 526.00 / 539.88 / 524.49 | market-meta |
| Volume (vs prior day) | 42.27M vs 22.37M | market-meta |
| 1-day change | −7.95% (calc) | market-meta |
| 10 EMA | 600.99 (price −10.3%, calc) | market-meta |
| VWMA | 624.00 (price −13.6%, calc) | market-meta |
| RSI | 13.71 (oversold) | market-meta |
| ATR | 24.36 (~4.5% of spot, calc) | market-meta |
| 50/200 SMA, MACD | NO_DATA_AVAILABLE | market-meta |
| Q2'26 rev / op inc / margin | 60.801B (+28%) / 18.775B (−8%) / 31% vs 43% | src-meta |
| Legal + severance / capex | 2.40B + 1.18B / 31.08B | src-meta |
| DAP | 3.60B (+3%) | src-meta |

### News Analyst
**Role: News Researcher (nonbinding role analysis — not a transaction proposal)**

**Data availability.** Only the frozen official earnings source [src-meta] and the frozen market close [market-meta] are in the corpus. `get_global_news`, `get_macro_indicators` (fed_funds_rate, 10y_treasury) and `get_prediction_markets` all returned NO_DATA_AVAILABLE. I therefore make **no** macro, rate-path, or market-implied-probability claims; those are UNKNOWN for this workflow.

**Company state (Q2 2026, announced 2026-07-29) [src-meta]**
- Revenue USD 60.801B, +28% [src-meta] — top line accelerating.
- Operating income USD 18.775B, **down 8%**; operating margin 31% vs 43% [src-meta]. Calculation: 18.775 / 60.801 = ~30.9%, consistent with the reported 31% (operands both [src-meta]).
- Costs and expenses USD 42.03B, including USD 2.40B legal charges and USD 1.18B severance [src-meta]. Calculation: one-off items = 2.40 + 1.18 = USD 3.58B, ~8.5% of total costs (operands [src-meta]). Ex-one-off cost base ≈ 38.45B (derived).
- Capital expenditures USD 31.08B [src-meta]. Calculation: capex exceeds operating income by 31.08 − 18.775 = USD 12.305B (operands [src-meta]) — the core tension: revenue growth is being bought with capex and legal/severance drag, not margin.
- Daily active people 3.60B, +3% [src-meta] — engagement stable but decelerating relative to 28% revenue growth, implying monetization/ARPU-led growth rather than user growth.

**Trading read (analyst judgment, not sourced fact)**
1. The quarter is a **margin-compression story with a clean-ish core**: strip 3.58B of legal+severance and operating margin would be materially above the reported 31% [src-meta]. Bulls will argue the 8% operating-income decline is largely non-recurring; bears will note capex of 31.08B is recurring and structurally caps free cash flow [src-meta].
2. **Key unknown:** no EPS (quarterly or TTM) and no share count in the corpus, so trailing P/E and FCF-per-share are UNKNOWN — do not price this off a multiple.
3. Price context: latest close USD 539.03, analysis date 2026-07-30 [market-meta]. No volume/technical series was returned, so trend and support levels are UNKNOWN.
4. Actionable: treat post-earnings reaction as a **capex-credibility vote**. Watch for confirmation of whether the 2.40B legal charge is one-time; if it recurs, the 31% margin is the new baseline, not a trough.

**Table**

| Item | Value | Source | Read |
|---|---|---|---|
| Revenue Q2'26 | USD 60.801B, +28% | src-meta | Strong top line |
| Operating income | USD 18.775B, −8% | src-meta | Margin pressure |
| Operating margin | 31% vs 43% | src-meta | −12 pts YoY |
| Costs & expenses | USD 42.03B | src-meta | Includes one-offs |
| Legal charges | USD 2.40B | src-meta | Recurrence = key risk |
| Severance | USD 1.18B | src-meta | Cost reset |
| One-offs (calc) | 3.58B ≈ 8.5% of costs | src-meta | Core margin better |
| Capex | USD 31.08B | src-meta | Exceeds op. income by 12.305B (calc) |
| DAU | 3.60B, +3% | src-meta | Monetization-led growth |
| Latest close | USD 539.03 (2026-07-30) | market-meta | No technicals available |
| Macro / rates / prediction markets | UNKNOWN | — | Data unavailable |
| EPS, TTM P/E, targets | UNKNOWN | — | Not in corpus |

## II. Research Team Decision

### Bull Researcher

Bull Analyst: **Role: Bull Analyst (nonbinding role analysis — not a transaction proposal)**

Ticker META, analysis date 2026-07-30, latest close 539.03 USD [market-meta].

Let me start where the bear will end: the −7.95% one-day drop (calc: (539.03−585.61)/585.61, operands [market-meta]) on 42.27M shares vs 22.37M prior day [market-meta]. That's a sentiment flush, not a demand failure. And the tape is already telling you it's stretched: RSI 13.71 [market-meta] is deep capitulation territory, and today's 15.39 high-low range sits *inside* the 24.36 ATR [market-meta] — the gap did the damage, not sustained intraday selling.

**Growth is accelerating, not decaying.** Revenue hit 60.801B, up 28% [src-meta]. That is the single most important number in the release, and it's the one the bear case has to explain away. DAP of 3.60B, +3% [src-meta], means 3.6 billion people show up daily — that's the moat. The bear will say "+3% users is decelerating." Correct, and irrelevant: the 28% revenue growth on 3% user growth is *monetization leverage*, the highest-quality growth a platform can produce. You don't need new users when ARPU is doing the work.

**The margin "collapse" is largely optical.** Operating margin 31% vs 43% [src-meta] looks brutal until you read the cost line: 42.03B includes 2.40B legal and 1.18B severance [src-meta]. Those one-offs total 3.58B (calc: 2.40+1.18, operands [src-meta]) — roughly 8.5% of total costs (calc). Strip them and the core cost base is ~38.45B (derived), and the underlying margin is materially above the reported 31%. The bear's "8% operating income decline" is substantially a legal-and-restructuring artifact, not a structural decay in the ad engine.

**Capex is a bet, not a bleed.** Yes, capex of 31.08B exceeds operating income of 18.775B by 12.305B (calc, operands [src-meta]). The bear calls that a structural FCF cap. I call it the largest discretionary growth investment on the income statement — and discretionary means it can be moderated. Meta is choosing to spend into an infrastructure cycle while revenue compounds at 28%. That's what dominant platforms do at inflection points.

**What the bear cannot say.** There is no EPS, no TTM EPS, no share count in the corpus — so trailing P/E and FCF-per-share are UNKNOWN [src-meta]. The bear cannot call this "expensive." Any multiple-based bear argument is unsourced. Likewise 50/200 SMA and MACD are NO_DATA_AVAILABLE [market-meta], so no one can claim a confirmed long-term downtrend.

**My rebuttal framework:** if the bear argues "margin is the new baseline," demand proof the 2.40B legal charge recurs — that's the actual swing factor, and it's unproven. If the bear argues "capex kills FCF," note that 28% revenue growth [src-meta] is precisely what funds it.

**Honest risk framing (assumption, not sourced fact):** price is 10.3% below the 10 EMA of 600.99 and 13.6% below VWMA of 624.00 [market-meta] — I won't pretend the trend is repaired. But buying dominant franchises at RSI 13.71 after a one-off-driven margin scare is historically the better side of the trade. 524.49 is only today's low [market-meta], not validated support — I'd scale, not lunge.

The growth, the moat, and the one-off-adjusted margin all favor the bull.

### Bear Researcher

Bear Analyst: **Role: Bear Analyst (nonbinding role analysis — not a transaction proposal)**

Ticker META, analysis date 2026-07-30, latest close 539.03 USD [market-meta].

Bull, your whole case rests on one move: strip 3.58B of legal and severance and declare the margin "optical." Let's actually run your own math. Add back 2.40B + 1.18B to operating income of 18.775B and you get 22.355B on 60.801B revenue — a 36.8% margin (calc, operands [src-meta]). Against last year's 43% [src-meta], that's still roughly **6 points of compression that no one-off explains**. Your "artifact" story covers barely half the damage. The other half is structural, and it's the half that compounds.

Now capex. You call 31.08B "discretionary." Discretionary is a word for spending you *haven't* committed to. This is an infrastructure cycle already contracted, and it exceeds operating income by 12.305B (calc, operands [src-meta]). Two consequences you skip: (1) the cash conversion is deteriorating *now*, and (2) the depreciation from that 31.08B lands on future income statements whether or not the AI payoff arrives. You're asking me to underwrite a multi-year spend with no revenue line attached to it in the release [src-meta]. That's not a moat — that's a bet with a bill.

On the 2.40B legal charge: you demand I prove recurrence. Wrong burden. This is a company with persistent regulatory exposure; a charge that size appearing in a *growth* quarter is a warning, not a rounding error. If it recurs, 31% is the baseline — your own framing, and you know it.

Your "sentiment flush" is narrative, not evidence. What the tape shows: price 10.3% below the 10 EMA of 600.99 and 13.6% below VWMA of 624.00 [market-meta], on 42.27M shares vs 22.37M [market-meta]. That's 1.9x volume (calc) transacting *above* spot — distribution, institutions handing stock to you at a discount. RSI 13.71 [market-meta] is not a buy signal; it's what capitulation looks like *before* a retest. And 524.49 is only today's low [market-meta] — you conceded it yourself, then still leaned on it.

DAP +3% [src-meta] against 28% revenue growth [src-meta] means the growth is price and ad-load, not people. That's the most regulator-exposed and engagement-fragile lever you have, and it's the one carrying the entire thesis.

I won't call META expensive — EPS and TTM P/E are UNKNOWN [src-meta], and I won't fake a multiple. I don't need one. The cash math is the argument: margins down double digits, capex above operating income, one-offs of unknown recurrence, and a broken tape with no tested support. ATR of 24.36 is ~4.5% of spot (calc) [market-meta] — you're scaling into that with no confirmation.

Wait for a close above 600.99 or a lower-volume hold of 524.49. Until then, the bull case is a hope, not a setup.

### Research Manager
**Recommendation**: Underweight

**Rationale**: Ticker META, analysis date 2026-07-30, latest close 539.03 USD [market-meta]. The bear won the decisive exchange, and it won it on the bull's own arithmetic. Adding back the 2.40B legal and 1.18B severance charges to operating income of 18.775B gives 22.355B on 60.801B revenue — a 36.8% margin (calc, operands [src-meta]) versus 43% a year ago [src-meta]. So roughly six points of compression survive the "one-off" defense; the bull's artifact story explains barely half the damage, and the residual is the part that compounds. The capex point is equally hard to dismiss: 31.08B of capital expenditures against 18.775B of operating income, a 12.305B shortfall (calc, operands [src-meta]), with depreciation landing on future income statements regardless of AI payoff and no revenue line attached to that spend in the release [src-meta]. The bull's "discretionary" label is assertion, not evidence. The bull's genuine wins: revenue +28% [src-meta] on DAP 3.60B, +3% [src-meta] is real monetization leverage, and RSI 13.71 [market-meta] is extreme. But the tape is unambiguously broken — price 10.3% below the 10 EMA of 600.99 and 13.6% below VWMA of 624.00 [market-meta] on 42.27M shares vs 22.37M prior [market-meta], i.e. ~1.9x volume (calc) — and 524.49 is only today's low, not validated support [market-meta]. Neither side can source a multiple: EPS, TTM EPS and trailing P/E are UNKNOWN [src-meta], and 50/200 SMA and MACD are NO_DATA_AVAILABLE [market-meta]. With ATR 24.36 at ~4.5% of spot (calc) [market-meta], scaling in without confirmation is paying full volatility for an unproven thesis. Growth quality keeps this from a Sell; the cash math and broken trend keep it from a Hold.

**Strategic Actions**: 1) Trim META to a below-benchmark weight — reduce the existing position by roughly one-third, executed in tranches rather than one block given ATR 24.36 (~4.5% of spot) [market-meta]. 2) No new or added exposure until one of two confirmations: a daily close above the 10 EMA of 600.99, or a lower-volume retest that holds 524.49 [market-meta]. 3) Risk control (assumption, not sourced fact): place a protective stop near 505, roughly 2 ATR below the 524.49 low, sized so total loss on the residual position is under 1% of portfolio value. 4) Re-underwrite on the next release: the swing factors are whether the 2.40B legal charge recurs and whether capex growth decelerates relative to the 28% revenue growth [src-meta]. 5) Do not build any valuation-based target — EPS, TTM EPS and trailing P/E are UNKNOWN [src-meta]; any price objective is an analyst assumption and must be labeled as such.

## III. Trading Team Plan

### Trader
**Action**: Sell

**Reasoning**: The plan's Underweight call is supported by the tape and the arithmetic: META closed 539.03, 10.3% below the 10 EMA of 600.99 and 13.6% below VWMA of 624.00 on 42.27M shares vs 22.37M prior (~1.9x volume), a distribution-grade repricing rather than drift, and 524.49 is only today's low with no tested bounce. Even adding back the 2.40B legal and 1.18B severance charges, operating margin is ~36.8% versus 43% a year ago, so roughly six points of compression survive the "one-off" defense, while capex of 31.08B exceeds operating income of 18.775B by 12.305B with depreciation still to come. RSI 13.71 and revenue +28% on DAP 3.60B (+3%) argue against a full exit, so I trim rather than liquidate, and I will not add until either a daily close above 600.99 or a lower-volume retest holding 524.49. All stop and sizing levels are analyst assumptions, not sourced facts; 50/200 SMA, MACD, EPS and trailing P/E are unavailable, so no valuation target is set.

**Entry Price**: 539.03

**Stop Loss**: 505.0

**Position Sizing**: Trim existing META position by roughly one-third, executed in tranches given ATR 24.36 (~4.5% of spot); hold the residual at a below-benchmark weight with a protective stop near 505 (~2 ATR below the 524.49 low), sized so total loss on the residual is under 1% of portfolio value. No new or added exposure until confirmation.

FINAL TRANSACTION PROPOSAL: **SELL**

## IV. Risk Management Team Decision

### Aggressive Analyst

Aggressive Analyst: I'm the Aggressive Risk Analyst, and I'm here to say the trader's SELL is the boldest, highest-reward call on the table — and I'll preemptively dismantle the two objections I know are coming.

First, the facts. META, analysis date 2026-07-30, latest close 539.03 USD [market-meta]. Price sits 10.3% below the 10 EMA of 600.99 and 13.6% below VWMA of 624.00 on 42.27M shares versus 22.37M prior, roughly 1.9x [market-meta]. That is not noise; that is institutions handing risk to whoever will take it.

To the conservative analyst, who will surely say "hold, the legal and severance charges are one-off, the core is fine": run the arithmetic. Costs of 42.03B include 2.40B legal and 1.18B severance [src-meta]. Add both back and margin is still roughly 36.8% against 43% a year ago — six points of compression survive the excuse. And capex of 31.08B exceeds operating income of 18.775B by 12.305B [src-meta]. Capex is recurring. You cannot add that back. The conservative case requires believing a 12-point margin drop is a rounding error; the tape already voted no.

To the neutral analyst, who will say "wait for confirmation, 50/200 SMA and MACD are unavailable": unavailable data is not a reason to stay fully weighted — it's a reason to stop pretending you have a trend signal at all. And 524.49 is only today's low, not tested support [market-meta]. RSI 13.71 is not a buy ticket; in gap capitulation it can stay pinned for weeks while the 10 EMA grinds down as overhead resistance. "Wait and see" while holding full size is itself an aggressive, unhedged bet — just a badly priced one.

Here's the aggressive logic the cautious crowd keeps missing: trimming a third isn't retreat, it's reloading. The high-reward play is to be liquid and ruthless now so that when the real capitulation prints — a lower-volume retest holding 524.49, or a close back above 600.99 — you can take size at a genuine discount instead of averaging down into a falling knife with no dry powder. Sitting at benchmark weight through a distribution-grade repricing is how you miss the next entry entirely.

The stop near 505 and the one-third tranche sizing are analyst assumptions, not sourced facts, and ATR of 24.36 (~4.5% of spot) [market-meta] justifies tranching rather than dumping. EPS, TTM P/E and any valuation floor are UNKNOWN, so there is no multiple to hide behind — only price, volume, and the capex arithmetic.

Sell the third. Keep the ammunition. That's the aggressive trade.

### Conservative Analyst

Conservative Analyst: I'm the Conservative Risk Analyst. I support the direction of the trader's SELL but not its residual risk budget — and the aggressive analyst's "reloading" framing is precisely the optimism that turns a manageable drawdown into a permanent loss.

Ticker META, analysis date 2026-07-30, latest close 539.03 USD [market-meta].

To the aggressive analyst: we agree on the arithmetic — operating margin 31% vs 43% [src-meta], and capex of 31.08B exceeding operating income of 18.775B by 12.305B [src-meta]. But if that is your conviction, a one-third trim is under-hedged, not bold. You cannot call the margin damage structural and leave two-thirds exposed. And "keep the ammunition" is not risk management — it is a pre-committed re-entry with no valuation anchor. EPS, TTM P/E and any valuation floor are UNKNOWN, so there is no price at which you can prove a discount is genuine. Reloading is a new bet, not a hedge.

The deeper flaw is the stop. A 505 stop assumes continuous trading. This name opened 526.00 against a prior close of 585.61 — a −10.2% gap [market-meta]. Stops do not fill at 505 in a gap; they fill where the market is. So the claim that total loss on the residual stays under 1% of portfolio is unenforceable — an assumption dressed as a control. With ATR 24.36, roughly 4.5% of spot [market-meta], and 50/200 SMA and MACD unavailable [market-meta], medium-term trend is UNKNOWN; we cannot assert the drawdown is contained.

To the neutral seat, which has not spoken: "wait for confirmation" while holding benchmark weight is the same unhedged bet the aggressive analyst rightly criticizes.

My adjustment: reduce more than a third — target roughly two-thirds out, leaving a token residual — and replace the resting stop with a rule: any close below 524.49 [market-meta] exits the remainder, and no re-entry until a close above 600.99 [market-meta]. Also flag recurrence risk: if the 2.40B legal charge [src-meta] repeats, 31% is the new baseline, not a trough. All levels and sizing are analyst assumptions, not sourced facts. Capital preservation first; upside can be repurchased with evidence.

### Neutral Analyst

Neutral Analyst: I'm the Neutral Risk Analyst. Ticker META, analysis date 2026-07-30, latest close 539.03 USD [market-meta]. I support reducing risk, but neither the aggressive "reload" nor the conservative "token residual" is the most sustainable adjustment.

Aggressive, you're right that the tape is distribution-grade: 539.03 is 10.3% below the 10 EMA of 600.99 and 13.6% below VWMA of 624.00 on 42.27M versus 22.37M shares [market-meta]. But "institutions handing risk" is interpretation, not data. Your one-third trim is too light if you truly believe capex of 31.08B exceeds operating income of 18.775B by 12.305B [src-meta] and margin is 31% versus 43% [src-meta]. And "reloading" is a new bet: EPS, TTM P/E and any valuation floor are UNKNOWN, so no discount is provable. A 505 stop is also gap-exposed; META opened 526.00 against a prior close of 585.61 [market-meta], so the under-1% residual-loss claim is an assumption, not a control.

Conservative, your gap critique is correct, and recurrence risk on the 2.40B legal charge [src-meta] is real. But two-thirds out plus a token residual overreacts to one quarter. Revenue rose 28% to 60.801B and DAP is 3.60B, up 3% [src-meta]; adding back 2.40B legal and 1.18B severance gives roughly 36.8% margin (calc: (18.775+3.58)/60.801; operands [src-meta]), still compressed but not a broken franchise. A hard no-re-entry until 600.99 [market-meta] may also be too rigid; repair can begin before the old EMA.

Moderate adjustment: trim roughly half now, in tranches, not one-third and not two-thirds. Add a conditional second tranche only on a daily close below 524.49 [market-meta], and do not rely on a resting 505 stop as the primary control. Size the residual for a gap scenario, not a continuous-market stop. Re-entry should be staged: either a close above 600.99 [market-meta] or a lower-volume ret

## V. Portfolio Manager Decision

### Portfolio Manager
**Rating**: Underweight

**Executive Summary**: META (analysis date 2026-07-30, latest close 539.03 USD [market-meta]): trim roughly half of the existing position in tranches, not the trader's one-third and not the conservative's two-thirds. Do not rely on a resting 505 stop as the primary control — META gapped from a 585.61 prior close to a 526.00 open [market-meta], so gap risk makes any continuous-market stop unenforceable. Exit the remainder on a daily close below 524.49 [market-meta]; no new exposure until a close above the 10 EMA of 600.99 or a lower-volume retest that holds 524.49 [market-meta]. All levels and sizing are analyst assumptions, not sourced facts.

**Investment Thesis**: The bear arithmetic survives the bull's own defense. Operating margin is 31% versus 43% [src-meta]; adding back the 2.40B legal and 1.18B severance charges to operating income of 18.775B on 60.801B revenue still yields only ~36.8% (calc, operands [src-meta]) — roughly six points of compression that are not one-off. Capex of 31.08B exceeds operating income of 18.775B by 12.305B (calc, operands [src-meta]), and depreciation lands on future income statements with no revenue line attached in the release [src-meta]. The tape confirms distribution: 539.03 sits 10.3% below the 10 EMA of 600.99 and 13.6% below VWMA of 624.00 on 42.27M shares versus 22.37M prior, ~1.9x (calc) [market-meta], and 524.49 is only today's low, not validated support [market-meta]. I side with the neutral analyst on sizing: the aggressive one-third trim is under-hedged given the capex math, while the conservative two-thirds-plus-token-residual overreacts to a single quarter in which revenue rose 28% to 60.801B and DAP reached 3.60B, +3% [src-meta]. The conservative analyst's gap critique is decisive on mechanics — a 505 stop is an assumption, not a control — so the exit rule becomes a close below 524.49 rather than a resting order. The aggressive analyst's "reloading" is a new bet, not a hedge: EPS, TTM EPS and trailing P/E are UNKNOWN [src-meta], and 50/200 SMA and MACD are NO_DATA_AVAILABLE [market-meta], so no valuation floor or discount is provable and no price target is set. Recurrence of the 2.40B legal charge [src-meta] would make 31% the baseline, which is why the residual stays below benchmark weight and re-entry is staged on evidence, not on RSI 13.71 [market-meta].

**Time Horizon**: 3-6 months
