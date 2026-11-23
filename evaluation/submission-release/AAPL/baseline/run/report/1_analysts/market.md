# AAPL Technical Analysis Report
**Role: Market Analyst (Technical)** — nonbinding role analysis, not a transaction proposal.
Ticker AAPL, analysis date 2026-07-31, latest close 308.91 [market-aapl].

---

## 1. Data Availability Caveats (read first)

Two of the eight requested indicators could not be computed on the frozen corpus:

- `close_50_sma`: **NO_DATA_AVAILABLE** — needs 50 rows, only 30 available at 2026-07-31 [market-aapl].
- `close_200_sma`: **NO_DATA_AVAILABLE** — needs 200 rows, only 30 available [market-aapl].

I will **not** estimate or fabricate these. This is a material limitation: the medium- and long-term trend benchmarks are unknown, so any claim about a "golden cross," "death cross," or price relative to the 200-day is **UNKNOWN** and is excluded from this report. The raw price history I do have (2026-05-01 through 2026-07-31, 63 rows) is sufficient to reason about the trend qualitatively, but not to produce those two averages.

All exact price/indicator values below come from the verified snapshot and the indicator tool, both sourced to `market-aapl`.

---

## 2. The Dominant Fact: A Violent Post-Earnings Repricing

The single most important observation is the 2026-07-31 session:

- Open 304.81, High 310.69, Low 300.00, Close 308.91, Volume 132,489,100 [market-aapl].
- Prior close (2026-07-30): 333.43 [market-aapl].

Derived move: (308.91 − 333.43) / 333.43 = **−7.36%** on the day. Calculation operands: 308.91 and 333.43, both [market-aapl]. This is a calculation, not a sourced fact.

Derived gap: open 304.81 vs prior close 333.43 = **−8.58%** opening gap down [market-aapl operands]. The stock then recovered ~4.1 points off the 300.00 low to close at 308.91 — i.e., the session closed in the upper third of its range, but still deep in the red.

Volume context: 132.49M shares vs the 2026-07-30 volume of 74.82M [market-aapl] — roughly **1.77×** the prior session (calculation from those two operands). Compare to the ~40–60M typical sessions in June–July 2026 [market-aapl]. This is a genuine distribution/capitulation day, not noise.

**The fundamental trigger is visible in the earnings release** [src-aapl]: fiscal Q3 2026 (ended June 27) revenue was USD109.4B, +16% y/y, gross margin 50.1%, diluted EPS 2.02 (+29%), dividend 0.27. On the face of it that is a strong quarter. The critical nuance: **gross margin included approximately 2 percentage points of tariff-refund benefit, and EPS included 0.11 of tariff-refund benefit** [src-aapl].

Derived quality-of-earnings math: 0.11 / 2.02 = **~5.4% of reported quarterly EPS was a one-time tariff refund** [src-aapl operands]. Similarly, ~2 of the 50.1 points of gross margin were refund-driven [src-aapl]. So the "clean" gross margin is closer to ~48.1% and clean EPS closer to ~1.91 (calculation from src-aapl operands). The market's −7.4% reaction is consistent with investors annualizing/forward-looking past a non-recurring benefit — but I want to be explicit: **the sources do not state why the stock fell.** The causal link between the tariff-refund disclosure and the selloff is my inference, not a sourced fact.

Note also: I cannot compute a trailing P/E. Only a single-quarter EPS (2.02, fiscal Q3 2026) is available [src-aapl]; no TTM EPS evidence exists in the sources. **Trailing P/E is UNKNOWN.** Any valuation multiple, price target, or fair value is likewise UNKNOWN.

---

## 3. Trend Structure: Uptrend Intact on Paper, Broken on the Tape

Reconstructing the path from the raw closes [market-aapl]:

- **May 2026:** 280.14 (May 1) → 312.06 (May 29). Steady, orderly advance.
- **June 2026:** Choppy consolidation, 306.31 (Jun 1) → 289.36 (Jun 30), with a sharp air-pocket on 2026-06-25 (close 275.15, volume 107.0M) and a huge-volume reversal day on 2026-06-26 (close 283.78, volume **261.8M** — the largest volume in the entire dataset) [market-aapl].
- **July 2026:** Strong recovery and breakout. 294.38 (Jul 1) → 340.08 (Jul 28), a new local high. Then 338.19 (Jul 29), 333.43 (Jul 30), and the 308.91 collapse (Jul 31) [market-aapl].

Derived: the July run from the 2026-06-30 close of 289.36 to the 2026-07-28 close of 340.08 is **+17.5%** in under a month [market-aapl operands]. The 2026-07-31 close of 308.91 gives back a large chunk of that: from the 340.08 peak, the drawdown is **−9.17%** (calculation from 340.08 and 308.91 [market-aapl]).

So the structural read: the intermediate uptrend that began in late June is **damaged but not invalidated**. Price is still above the June 30 close (289.36) and well above the June 25 low close (275.15) [market-aapl]. But the July breakout has been rejected.

---

## 4. Indicator-by-Indicator Read

**10 EMA = 327.24 vs close 308.91** [market-aapl]. Price is **18.33 points / ~5.6% below** the short-term average (calculation from those operands). This is the cleanest signal in the set: the fast trend measure has flipped from support to overhead resistance. A close back above 327.24 would be the first evidence of repair; until then, rallies are suspect.

**MACD = 6.82, Signal = 8.14, Histogram = −1.32** [market-aapl]. The MACD line remains positive (6.82) — momentum is still net positive on this window — but it sits **below** its signal line, and the histogram is negative. That is a **bearish crossover in progress**: momentum is decelerating from a positive base. The histogram at −1.32 is not yet deeply negative, which is consistent with a one-day shock rather than a fully established downtrend. Watch for the histogram to expand negatively (confirmation) or curl back toward zero (failed signal).

**RSI = 45.08** [market-aapl]. Neutral-to-weak. Critically, RSI is **not oversold** (nowhere near 30) despite a −7.4% day. That means the selloff has not yet produced a classic mean-reversion setup, and it also means there is room to fall further before RSI flags capitulation. In a strong uptrend RSI can stay elevated; here it has simply reset to the middle of the range, which is the signature of a trend that has lost its bid rather than one that is washed out.

**Bollinger Middle = 324.37, Upper = 344.51, Lower = 304.22** [market-aapl]. Close 308.91 sits **between the middle and lower band**, roughly 4.7 points above the lower band (calculation from 308