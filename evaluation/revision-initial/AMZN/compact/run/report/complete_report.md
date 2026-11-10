# Research Desk Analysis Report

- Company (legal identity): Amazon.com, Inc.
- Ticker: AMZN
- Analysis date: 2026-07-31
- Evidence latest close: 271.58 USD [source: market-amzn, market CSV as-of 2026-07-31]
- Official earnings source: src-amzn
- Contract: identity, date, evidence close and source above are rendered deterministically from the evidence pack; the generated narrative below is unmodified model output.

## I. Analyst Team Reports

### Market Analyst
**Role: Market Analyst — AMZN (nonbinding analysis)**

Ticker AMZN, analysis date 2026-07-31, latest close 271.58 [market-amzn].

**Regime shift.** AMZN closed 271.58 on 2026-07-31 vs 235.50 on 2026-07-30 [market-amzn] — a one-day gain of +15.3% (calc: (271.58−235.50)/235.50). The session opened 265.00, i.e. a +12.5% gap over the prior close (calc), ranged 262.01–273.23, and traded 129,054,800 shares vs 101,839,800 the prior day [market-amzn]. This is an event-driven repricing, not a drift: Q2 2026 net sales USD200.6B, +20%; AWS sales USD42.2B, +37%, with AWS operating income 27.5B vs 19.2B [src-amzn].

**Trend structure.** Price sits 11.9% above the 10 EMA of 242.70 and 12.7% above VWMA of 240.96 [market-amzn] (calcs). Both are volume/price anchors that the gap has left far behind — classic post-gap extension. The 50/200 SMAs returned NO_DATA_AVAILABLE (insufficient window) [market-amzn]; I will not estimate them, so long-term trend confirmation is UNKNOWN.

**Momentum.** RSI 64.04 [market-amzn] — strong but not overbought; note it is computed on a series that includes the gap, so it understates the impulse. MACD 0.08 with histogram 0.91 [market-amzn] implies a signal line near −0.83 (calc). **Discrepancy flag:** a MACD line of only 0.08 after a +15% day is inconsistent with the price move; treat MACD as lagging/unreliable here rather than as confirmation.

**Volatility/risk.** ATR 9.26 [market-amzn] is a pre-gap reading and almost certainly understates current range (the 2026-07-31 bar alone spanned 11.22 points, calc from 273.23−262.01 [market-amzn]). Position sizing off 9.26 would be too aggressive.

**Actionable read.** Constructive but extended. Reference levels (analyst judgment, not sourced): prior close 235.50 and the 2026-07-29 close 226.65 [market-amzn] are the gap-fill zone; the 2026-05-06 close of 274.99 [market-amzn] is the nearest overhead reference, with 2026-07-31 high 273.23 just beneath it. Preferred approach: scale in on a hold above ~262 (2026-07-31 low) rather than chase; a close back under 235.50 would invalidate the gap. Fundamental caveat: TTM free cash flow was an outflow of 7.6B and net income of 62.6B included large Anthropic-related investment gains (pre-tax other income 53.4B) [src-amzn] — headline earnings quality is not operating earnings quality. Valuation multiples are UNKNOWN (no TTM EPS in sources).

| Item | Value | Source |
|---|---|---|
| Close 2026-07-31 | 271.58 | market-amzn |
| Prior close 2026-07-30 | 235.50 | market-amzn |
| 1-day change | +15.3% (calc) | market-amzn |
| Day range | 262.01–273.23 | market-amzn |
| Volume | 129.05M | market-amzn |
| 10 EMA / VWMA | 242.70 / 240.96 | market-amzn |
| RSI | 64.04 | market-amzn |
| MACD / hist | 0.08 / 0.91 (flag: lagging) | market-amzn |
| ATR | 9.26 (pre-gap, understated) | market-amzn |
| 50/200 SMA | NO_DATA_AVAILABLE | market-amzn |
| Q2 sales / AWS | 200.6B +20% / 42.2B +37% | src-amzn |
| TTM FCF | −7.6B | src-amzn |

### News Analyst
**Role: News Researcher (nonbinding analysis — not a transaction proposal)**

**Data availability:** Only the frozen official earnings source and market price source are available. `get_global_news`, `get_macro_indicators` (fed_funds_rate, 10y_treasury) and `get_prediction_markets` (Fed rate cut, recession 2026) all returned NO_DATA_AVAILABLE. I will not estimate or fabricate macro, rate, or probability values; those inputs are UNKNOWN for this workflow.

**Company news (only fresh catalyst):** Amazon reported Q2 2026 (ended June 30) on 2026-07-30 [src-amzn].
- Net sales USD200.6B, +20% [src-amzn].
- AWS sales USD42.2B, +37%; AWS operating income USD27.5B vs USD19.2B a year earlier [src-amzn]. Calculation: 27.5 / 42.2 ≈ 65% implied AWS segment operating margin (operands [src-amzn]) — an unusually high level that warrants scrutiny of segment cost allocation, not a sourced figure.
- Net income USD62.6B includes substantial investment-related gains; pre-tax other income USD53.4B came primarily from Anthropic investments [src-amzn]. Calculation: 53.4 / 62.6 ≈ 85% of net income is non-operating (operands [src-amzn]) — headline EPS is NOT a clean read on operating earnings; do not annualize it.
- TTM free cash flow was an outflow of USD7.6B [src-amzn] — the key bear datapoint: 20% revenue growth is being funded with negative FCF.
- AWS share of sales: 42.2 / 200.6 ≈ 21% (calculation, operands [src-amzn]).

**Market context:** AMZN latest close USD271.58, analysis date 2026-07-31 [market-amzn]. No volume/technical series was returned in this workflow, so trend, momentum and post-earnings reaction are UNKNOWN. Any P/E, target, or entry level is UNKNOWN/assumption — no TTM EPS is derivable from the sources (only a single quarter, and that quarter is gain-distorted) [src-amzn].

**Actionable read for traders:** The fundamental signal is bifurcated — accelerating AWS (+37%) with margin expansion [src-amzn] versus negative TTM FCF [src-amzn] and earnings quality heavily dependent on Anthropic mark-ups [src-amzn]. Watch for (a) any reversal in Anthropic valuation hitting other income, and (b) capex-driven FCF trajectory. Macro rate sensitivity of a long-duration growth name cannot be assessed here — macro data unavailable.

| Item | Value | Source / Status |
|---|---|---|
| Ticker / analysis date | AMZN / 2026-07-31 | market-amzn |
| Latest close | USD271.58 | market-amzn |
| Q2 2026 net sales | USD200.6B, +20% | src-amzn |
| AWS sales / growth | USD42.2B, +37% | src-amzn |
| AWS op income | USD27.5B vs 19.2B | src-amzn |
| Net income | USD62.6B (gain-inflated) | src-amzn |
| Pre-tax other income (Anthropic) | USD53.4B | src-amzn |
| TTM free cash flow | −USD7.6B | src-amzn |
| AWS implied op margin | ≈65% (calc) | derived from src-amzn |
| Macro (rates, CPI, yields) | UNKNOWN | tool: NO_DATA_AVAILABLE |
| Global/macro news | UNKNOWN | tool: NO_DATA_AVAILABLE |
| Fed-cut / recession odds | UNKNOWN | tool: NO_DATA_AVAILABLE |
| Valuation multiples, targets | UNKNOWN | not in sources |

## II. Research Team Decision

### Bull Researcher

Bull Analyst: **Role: Bull Analyst — AMZN (nonbinding analysis, not a transaction proposal)**

Ticker AMZN, analysis date 2026-07-31, latest close USD271.58 [market-amzn].

Let me open by conceding the obvious, because the bear will hit it anyway: yes, TTM free cash flow was an outflow of USD7.6B [src-amzn], and yes, USD53.4B of pre-tax other income came from Anthropic marks inside USD62.6B of net income [src-amzn]. I'm not going to pretend that's clean operating earnings. But here's the thing — the market didn't pay up 15.3% (calc: (271.58−235.50)/235.50 [market-amzn]) for the Anthropic line. It paid up for AWS: USD42.2B of sales, +37%, with operating income of USD27.5B versus USD19.2B a year earlier [src-amzn]. That's the engine, and it re-accelerated.

**On the FCF bear case.** Negative FCF at Amazon has historically been a *choice*, not a constraint — it's capex into capacity that shows up as future AWS revenue. The bear will call it "growth funded with negative cash flow." I'd call it the cheapest customer-acquisition cost in tech: you build the datacenter, and the AI workload rents it for years. And note the offset — AWS operating income rose USD8.3B year over year (calc: 27.5−19.2 [src-amzn]) while total sales grew 20% to USD200.6B [src-amzn]. That is operating leverage, not a company burning cash to stand still.

**On earnings quality.** Fair hit, but it cuts both ways. Strip the gains and you still have a business compounding revenue at 20% on a USD200.6B quarterly base [src-amzn]. The Anthropic stake isn't a liability — it's a mark-to-market option on the AI cycle sitting inside the P&L. If Anthropic's valuation reverses, that's a headline problem, not an operating one.

**On the chart.** The bear will say "extended." Price is 11.9% above the 10 EMA of 242.70 and 12.7% above VWMA of 240.96 [market-amzn] — true, and I won't chase it. But RSI at 64.04 [market-amzn] is strong, not blown out, and the 2026-07-31 high of 273.23 sits just under the 2026-05-06 close of 274.99 [market-amzn]. A push through that level opens air. Volume of 129.05M versus 101.84M the prior day [market-amzn] says institutions, not retail froth.

**Where I'll give ground honestly:** 50/200 SMAs are NO_DATA_AVAILABLE [market-amzn], so long-term trend confirmation is UNKNOWN. ATR of 9.26 [market-amzn] is pre-gap and understated — the day's own range was 11.22 points (calc: 273.23−262.01 [market-amzn]). Valuation multiples are UNKNOWN; no TTM EPS is derivable from a single gain-distorted quarter [src-amzn]. So I'm not going to hand you a P/E.

**My stance (analyst judgment, not sourced fact):** constructive, scaled entry above ~262 (the 2026-07-31 low [market-amzn]), invalidation on a close under 235.50 [market-amzn]. The bear can own the accounting debate; I'll own the AWS re-acceleration.

### Bear Researcher

Bear Analyst: **Role: Bear Analyst — AMZN (nonbinding analysis, not a transaction proposal)**

Ticker AMZN, analysis date 2026-07-31, latest close USD271.58 [market-amzn].

Bull, you conceded the accounting and then asked me to look past it. I won't, because the tape says the market *did* pay for the headline. Net income was USD62.6B with USD53.4B of pre-tax other income from Anthropic marks [src-amzn] — that's ~85% of net income non-operating (calc: 53.4/62.6 [src-amzn]). A +15.3% gap (calc: (271.58−235.50)/235.50 [market-amzn]) landed on a quarter whose bottom line was mostly a mark-up on a private AI stake. You call that stake "an option." Options have two directions, and a reversal hits reported EPS, not just a footnote.

**Your FCF defense is an assertion, not evidence.** You say negative FCF is "capex into capacity." The sources give me TTM FCF of −USD7.6B [src-amzn] and *no* capex line. The mechanism you're describing is UNKNOWN in this dataset. You're filling a data hole with a narrative.

**AWS is 21% of sales** (calc: 42.2/200.6 [src-amzn]). The other ~79% is the low-margin base you're implicitly asking me to ignore. And that implied ~65% AWS operating margin (calc: 27.5/42.2 [src-amzn]) is the number I'd audit first — margins that extreme usually reflect cost allocation, not durable pricing power. If it normalizes, your "operating leverage" evaporates.

**The chart is worse than you admit.** Price is 11.9% above the 10 EMA of 242.70 and 12.7% above VWMA of 240.96 [market-amzn]. The 2026-07-31 high of 273.23 stalled under the 2026-05-06 close of 274.99 [market-amzn] — that's a rejection at resistance, not "air." MACD at 0.08 after a +15% day is internally inconsistent [market-amzn]; you can't claim momentum confirmation from a lagging, flagged indicator. 50/200 SMAs are NO_DATA_AVAILABLE [market-amzn] — no long-term trend evidence exists. ATR 9.26 is pre-gap while the bar itself spanned 11.22 points (calc: 273.23−262.01 [market-amzn]).

**Your volume inference is unsupported.** 129.05M vs 101.84M [market-amzn] tells you size, not buyer identity. "Institutions, not retail" is a story, not a datapoint.

**And the asymmetry kills your own plan.** Entry above ~262 with invalidation at 235.50 [market-amzn] is ~10% risk (calc: (262−235.50)/262) for ~5% to your own 274.99 reference (calc: (274.99−262)/262). You're risking two to make one, at 12% extension, on gain-distorted earnings, with valuation multiples UNKNOWN [src-amzn]. That's not conviction — that's chasing.

I'd want a gap-fill toward 235.50 before I'd underwrite this.

### Research Manager
**Recommendation**: Overweight

**Rationale**: Ticker AMZN, analysis date 2026-07-31, latest close USD271.58 [market-amzn]. Both sides fought well, but the bull won the argument that matters and the bear won the argument about timing — which is why this is Overweight, not Buy.

What the bull carried: the operating engine is real and re-accelerated. AWS sales of USD42.2B, +37%, with operating income of USD27.5B versus USD19.2B a year earlier [src-amzn], on total net sales of USD200.6B, +20% [src-amzn]. That is a USD8.3B year-over-year step-up in AWS operating income (calc: 27.5−19.2 [src-amzn]) alongside 20% top-line growth — the strongest single datapoint in this debate, and it is operating, not mark-to-market.

What the bear carried: earnings quality and entry risk. USD53.4B of pre-tax other income, primarily Anthropic marks, inside USD62.6B of net income [src-amzn] is ~85% of the bottom line non-operating (calc: 53.4/62.6 [src-amzn]); TTM FCF was an outflow of USD7.6B [src-amzn] with no capex line in the sources, so the "capex into capacity" mechanism is UNKNOWN, not proven. The bear is also right that the tape is stretched: price is 11.9% above the 10 EMA of 242.70 and 12.7% above VWMA of 240.96 [market-amzn], the 2026-07-31 high of 273.23 stalled under the 2026-05-06 close of 274.99 [market-amzn], MACD at 0.08 is internally inconsistent [market-amzn], and 50/200 SMAs are NO_DATA_AVAILABLE [market-amzn] — long-term trend is UNKNOWN. The bull's "institutions, not retail" read on 129.05M vs 101.84M volume [market-amzn] is unsupported inference, and I discount it.

Where I overrule the bear: the bear's own implied ~65% AWS operating margin (calc: 27.5/42.2 [src-amzn]) critique is speculation about cost allocation with no source support, and "wait for a gap-fill to 235.50" is a wish, not a thesis. Valuation multiples and TTM EPS remain UNKNOWN [src-amzn] — no trailing P/E is derivable from a single gain-distorted quarter — so neither side can claim a valuation edge. Net: own the AWS re-acceleration, but do not pay the full 12% extension in one clip.

**Strategic Actions**: 1) Build exposure in tranches, not at once. Start with roughly one-third of the intended AMZN position at market near the frozen close of USD271.58 [market-amzn]. 2) Add a second tranche on a pullback into the USD262 area (the 2026-07-31 low [market-amzn]) and a third on a close back toward the 10 EMA of 242.70 [market-amzn]. 3) Do not add on a breakout above 274.99 [market-amzn] unless volume expands beyond the 129.05M seen on 2026-07-31 [market-amzn]; treat that level as resistance until proven otherwise. 4) Risk control (analyst judgment, not sourced fact): hard invalidation on a daily close below USD235.50 [market-amzn]; size the full position so that a stop there costs no more than ~1.5% of portfolio value, which implies a modest single-name weight given the ~13% distance from current price. 5) Cap total AMZN weight at a level consistent with Overweight — above benchmark, below a full-conviction Buy. 6) Re-underwrite on the next earnings release: specifically whether AWS operating income holds near the USD27.5B level [src-amzn] and whether TTM FCF moves off the −USD7.6B outflow [src-amzn]. 7) Treat any large negative Anthropic revaluation as a thesis-review trigger, not an automatic exit — it hits reported EPS, not AWS operations [src-amzn]. 8) Note explicitly: valuation multiples, TTM EPS and long-term trend (50/200 SMA) are UNKNOWN [src-amzn][market-amzn]; do not present any target multiple or price objective as sourced fact.

## III. Trading Team Plan

### Trader
**Action**: Buy

**Reasoning**: The research plan is Overweight and the bull's case rests on operating evidence, not sentiment: AWS sales of USD42.2B, +37%, with operating income of USD27.5B versus USD19.2B a year earlier [src-amzn] — a USD8.3B operating step-up on 20% total net sales growth of USD200.6B [src-amzn]. The bear's valid points are about entry price and earnings quality (USD53.4B of pre-tax other income inside USD62.6B net income, TTM FCF of −USD7.6B [src-amzn]), not about the business, so the correct expression is a scaled Buy rather than a full-conviction chase: price is 11.9% above the 10 EMA of 242.70 and 12.7% above VWMA of 240.96, and the 2026-07-31 high of 273.23 stalled under the 2026-05-06 close of 274.99 [market-amzn]. I therefore take only the first tranche near the 271.58 close, reserve adds for 262 (2026-07-31 low) and 242.70 (10 EMA), and treat a daily close below 235.50 as full invalidation of the gap. Note explicitly that 50/200 SMAs, TTM EPS and valuation multiples are UNKNOWN [market-amzn][src-amzn], and ATR of 9.26 is a pre-gap reading that understates the current 11.22-point daily range, so sizing must not be derived from it.

**Entry Price**: 271.58

**Stop Loss**: 235.5

**Position Sizing**: Tranche 1: ~4% of portfolio at market near 271.58 (one-third of intended position). Tranche 2: ~3.5% on a pullback into ~262.00 (2026-07-31 low). Tranche 3: ~3.5% on a close back toward the 10 EMA of 242.70. Full position cap ~11% of portfolio (Overweight: above benchmark, below full-conviction Buy). Stop is a daily close below 235.50 (~13.3% below the first entry), sized so total loss at that stop is ~1.5% of portfolio value; do not add on a breakout above 274.99 unless volume exceeds the 129.05M seen on 2026-07-31.

FINAL TRANSACTION PROPOSAL: **BUY**

## IV. Risk Management Team Decision

### Aggressive Analyst

Aggressive Analyst: I'm the Aggressive Risk Analyst, and I'll say it plainly: the trader's scaled Buy is the right expression, and both the cautious and the neutral seats are about to argue themselves out of the best operating print this name has produced.

Start with what the conservative will attack first — extension. Yes, AMZN at 271.58 on 2026-07-31 sits 11.9% above the 10 EMA of 242.70 and 12.7% above VWMA of 240.96 [market-amzn]. That is not a warning; that is what a repricing looks like. The move came on 129.05M shares versus 101.84M the prior day [market-amzn] — that is institutional repositioning, not retail froth. RSI 64.04 [market-amzn] is strong, not overbought. Demanding a pullback to 242.70 means demanding the market surrender the entire catalyst before you'll own a share. That isn't risk control, it's a hope.

On earnings quality: the conservative will wave the 53.4B pre-tax other income and the −7.6B TTM FCF [src-amzn] as reasons to stand aside. But you cannot dismiss the Anthropic gain as "low quality" while ignoring that it reflects a real, appreciating asset on the balance sheet. And negative FCF alongside 20% sales growth to 200.6B [src-amzn] is investment intensity, not deterioration. Meanwhile the actual operating engine: AWS 42.2B, +37%, operating income 27.5B versus 19.2B — an 8.3B step-up (calc from src-amzn). That is cash-generating, not mark-to-market.

To the neutral: hiding behind UNKNOWN valuation multiples and NO_DATA_AVAILABLE 50/200 SMAs [market-amzn] is not analysis, it's paralysis. Waiting for data that doesn't exist is not risk management. And your "scale in on a hold above 262" is already inside this plan — tranche 2 at 262, tranche 3 at 242.70. The only real disagreement is whether you own anything at 271.58. You should, because if AWS compounds at 37%, this is the cheapest tranche you'll get.

The asymmetry is the argument: 4% now, cap 11%, stop at 235.50 — roughly 1.5% of portfolio at risk — against a clear overhead reference at 274.99 [market-amzn] and open air beyond it. The trader even refuses to add above 274.99 without volume exceeding 129.05M. That's discipline, not timidity.

Ticker AMZN, analysis date 2026-07-31, latest close 271.58 [market-amzn]. Buy the first tranche.

### Conservative Analyst

Conservative Analyst: I'm the Conservative Risk Analyst. Ticker AMZN, analysis date 2026-07-31, latest close 271.58 [market-amzn].

Aggressive, you called the extension "what a repricing looks like." A repricing is also what a gap is — and gaps fill. AMZN closed 235.50 on 2026-07-30 and opened 265.00 the next morning [market-amzn]. That is a 12.5% overnight repricing on information, not on accumulated demand. The 129.05M shares you cite as institutional conviction is one session of event flow; it tells us nothing about who holds the stock at 271.58 tomorrow. And you cannot claim RSI 64.04 is "strong, not overbought" while the market analyst flags that the same series understates the impulse — you're using a lagging indicator as comfort.

Your asymmetry math is where I object hardest. You say 4% now, stop 235.50, "roughly 1.5% of portfolio at risk." That assumes the stop fills at 235.50. This name just demonstrated it can move 12.5% between closes [market-amzn]. A close-based stop on a gap-prone instrument is not a 13.3% risk; it is an unknown risk, and ATR of 9.26 is explicitly a pre-gap reading that understates the 11.22-point bar [market-amzn]. Sizing off a number we know is wrong is not discipline.

On quality: 53.4B of pre-tax other income inside 62.6B of net income is roughly 85% non-operating (calc from src-amzn). You call the Anthropic stake "a real, appreciating asset." It is a mark. Marks reverse without any operating change, and we have no visibility into the next one. Meanwhile TTM free cash flow is an outflow of 7.6B [src-amzn] — that is not "investment intensity" you can wave away; it means the growth is externally funded, and rates are UNKNOWN in this workflow. You are asking the firm to underwrite duration risk you cannot price.

To the neutral seat: your "hold above 262" is the right instinct but it is not inside this plan — tranche 2 at 262 and tranche 3 at 242.70 are triggered by weakness, not by a hold. That is averaging down into a gap fill, and it deploys the full 11% precisely when the thesis is being invalidated. That is the flaw neither of you named.

My adjustment: cut tranche 1 to ~2% of portfolio, not 4%. Make 262.00 — the 2026-07-31 low [market-amzn] — the confirmation trigger, not a buy level: add only on a close that holds above it with volume. Cap the position at ~7%, not 11%. And move invalidation from 235.50 to a close below 262.00, which cuts per-share risk from 13.3% to roughly 3.5% (calc from market-amzn) while keeping the AWS operating step-up — 27.5B versus 19.2B [src-amzn] — as the reason to own it at all. The 274.99 reference you lean on is a 2026-05-06 close [market-amzn], nearly three months stale; "open air beyond it" is absence of evidence, not a target.

Buy less, later, with a tighter invalidation. That is how we keep the operating story without donating the firm's capital to a gap.

### Neutral Analyst

Neutral Analyst: I'm the Neutral Risk Analyst. Ticker AMZN, analysis date 2026-07-31, latest close 271.58 [market-amzn].

Aggressive, two of your pillars don't hold. "This is the cheapest tranche you'll get" is a forecast, and with no TTM EPS in the sources every valuation multiple is UNKNOWN [src-amzn] — you can't call anything cheap. "Open air beyond 274.99" is worse: that's a 2026-05-06 close [market-amzn], nearly three months stale, and absence of resistance is not a target. And your 1.5%-at-risk figure assumes the stop fills at 235.50 on a name that just moved 12.5% between closes [market-amzn]; that's a modeled loss, not a bounded one. Calling the Anthropic mark "a real, appreciating asset" is fine as balance-sheet fact, but 53.4B of 62.6B net income is roughly 85% non-operating (calc from src-amzn) — it cannot carry the underwriting case.

Conservative, your turn. A close below 262.00 as invalidation is too tight to be meaningful: 262.01 was simply the 2026-07-31 low, and that single bar spanned 11.22 points [market-amzn]. A ~3.5% stop on an instrument with that realized range is noise-level — you'd be shaken out by ordinary post-gap digestion and then watch the operating story from the sidelines. You also misread the plan: tranche 2 at 262 and tranche 3 at 242.70 aren't "averaging down into invalidation" if they're conditioned on stabilization — but you're right that as written they trigger on price touch alone, which is a real flaw. And capping at 7% underweights the one hard number here: AWS operating income 27.5B versus 19.2B, an 8.3B step-up (calc from src-amzn).

Where I land, between you: keep the first tranche but at ~3%, not 4% and not 2% — the operating evidence justifies owning something at 271.58, the extension justifies owning less. Make tranche 2 conditional, not mechanical: add only after a session that tests toward 262 and closes back above it, so you're buying a hold, not a touch. Keep 235.50 as the invalidation line because it's the pre-gap close and the structural level, but size off the observed 11.22-point bar rather than ATR 9.26, which the market analyst flags as pre-gap and understated [market-amzn]. Cap the whole position near 9% — above benchmark, below the 11% full-conviction figure. And hold the trader's volume condition on any add above 274.99: 129.05M shares [market-amzn] is the bar to beat.

That gives you the AWS step-up and the 20% sales growth to 200.6B [src-amzn] with real participation, while refusing to pretend a gap-prone, negative-FCF name (TTM outflow 7.6B [src-amzn]) with UNKNOWN macro and UNKNOWN multiples deserves either a chase or a token 2% gesture. Moderate sizing, conditional adds, structural invalidation — that's the version that survives both a gap fill and a continuation.

## V. Portfolio Manager Decision

### Portfolio Manager
**Rating**: Overweight

**Executive Summary**: Ticker AMZN, analysis date 2026-07-31, latest close USD271.58 [market-amzn]. Own the AWS re-acceleration but do not pay the full ~12% extension in one clip: initiate ~3% of portfolio at market, add only on a session that tests toward 262.00 and closes back above it, and reserve a final tranche near the 10 EMA of 242.70 [market-amzn]. Cap total weight at ~9% — the trader's 11% breaches the 10% max-single-position constraint — with invalidation on a daily close below 235.50 [market-amzn], sized off the observed 11.22-point bar rather than the pre-gap ATR of 9.26 [market-amzn]. Horizon 6-12 months, re-underwritten at the next earnings release.

**Investment Thesis**: The operating evidence is the only hard, non-mark-to-market datapoint in this debate and it belongs to the bull: AWS sales of USD42.2B, +37%, with operating income of USD27.5B versus USD19.2B a year earlier [src-amzn] — a USD8.3B step-up (calc: 27.5−19.2 [src-amzn]) on total net sales of USD200.6B, +20% [src-amzn]. That justifies owning the name; it does not justify chasing it.

The conservative and neutral seats win the sizing and entry argument. USD53.4B of pre-tax other income inside USD62.6B of net income is ~85% non-operating (calc: 53.4/62.6 [src-amzn]), so the bottom line cannot carry the underwriting case, and TTM free cash flow was an outflow of USD7.6B [src-amzn] with no capex line in the sources — the funding mechanism is UNKNOWN, not proven. The tape is stretched: price is 11.9% above the 10 EMA of 242.70 and 12.7% above VWMA of 240.96, the 2026-07-31 high of 273.23 stalled under the 2026-05-06 close of 274.99, and 50/200 SMAs are NO_DATA_AVAILABLE [market-amzn]. The 2026-07-30 close of 235.50 to a 2026-07-31 open of 265.00 [market-amzn] proves this instrument gaps, so a close-based stop is a modeled loss, not a bounded one — hence modest initial size.

I adopt the neutral seat's compromise over both extremes: ~3% first tranche (not the aggressive 4% chase, not the conservative 2% token), tranche 2 made conditional on a hold above 262.00 rather than a mechanical touch, and 235.50 retained as structural invalidation because it is the pre-gap close. I reject the conservative's 262.00 invalidation as noise-level on an 11.22-point bar [market-amzn], and I reject the aggressive's "cheapest tranche" and "open air beyond 274.99" as unsupported — with no TTM EPS in the sources, every valuation multiple is UNKNOWN [src-amzn], so no price target is stated. Adds above 274.99 require volume exceeding the 129.05M seen on 2026-07-31 [market-amzn].

**Time Horizon**: 6-12 months
