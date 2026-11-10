# AMZN — Technical Analysis Report
**Role: Market Analyst (technical)** | Ticker: AMZN | Analysis date: 2026-07-31 | Latest close: 271.58 USD [market-amzn]

---

## 1. Data Integrity & Scope Notes (read first)

- The frozen market CSV returned **63 rows** for the requested 2025-11-01 → 2026-07-31 window, but the earliest row actually present is **2026-05-01** [market-amzn]. The file is effectively a ~3-month window, not a 9-month window.
- Consequence: **`close_50_sma` and `close_200_sma` are NO_DATA_AVAILABLE** — the tool explicitly reports it needs 50 and 200 rows respectively and only 30 are available at 2026-07-31 [market-amzn]. I will **not** estimate or fabricate these. This is a material limitation: I cannot confirm a golden/death cross, cannot confirm long-term trend structure, and cannot use the 200-SMA as a strategic benchmark. Any claim about "the long-term uptrend" would be unsupported.
- The verified snapshot for 2026-07-31 confirms: open 265.00, high 273.23, low 262.01, close 271.58, volume 129,054,800 [market-amzn]. This matches the last CSV row exactly — **no discrepancy** between the snapshot and the raw data.
- **No valuation ratio, P/E, price target, or EPS figure is asserted anywhere in this report.** The earnings source gives net sales, AWS sales, AWS operating income, net income, pre-tax other income, and TTM FCF — but **no EPS and no share count**, so trailing P/E is **UNKNOWN** [src-amzn]. I flag this explicitly because the Q2 net income of 62.6 billion is heavily distorted by investment gains and must not be annualized into a multiple.

---

## 2. The Dominant Fact: A Violent Single-Session Repricing

The single most important observation in this dataset is the **2026-07-31 session**:

- Close **271.58** vs prior close **235.50** on 2026-07-30 [market-amzn].
- Derived move: (271.58 − 235.50) / 235.50 = **+15.32%** — a calculation from two sourced closes [market-amzn], not a sourced fact.
- Volume **129,054,800** vs **101,839,800** the prior session [market-amzn]. Derived: 129.05M / 101.84M ≈ **1.27×** the already-elevated prior day's volume.
- The 2026-07-30 session was itself an event day: volume 101.8M against a ~30–50M baseline, closing +3.9% (235.50 vs 226.65) [market-amzn]. Derived: (235.50 − 226.65)/226.65 = **+3.90%**.
- The 2026-07-31 range was **262.01 – 273.23**, i.e. the entire session traded **above** the prior day's high of 239.82 [market-amzn]. This is a **full-body gap-up with no overlap** into the prior day's range — the strongest possible form of a breakaway gap.

**Interpretation:** This is a post-earnings repricing, consistent with the announcement date of 2026-07-30 [src-amzn]. The market is reacting to the Q2 2026 print: net sales 200.6B, +20%; AWS sales 42.2B, +37%; AWS operating income 27.5B vs 19.2B a year earlier [src-amzn]. The AWS acceleration (37% growth) and the AWS segment operating income step-up are the plausible drivers of a 15% single-day re-rate — but note the caveat in §6: the headline net income of 62.6B is **not** an operating result.

---

## 3. Trend Structure: A V-Shaped Recovery That Just Broke Out

Reconstructing the path from the available closes [market-amzn]:

| Phase | Dates | Close path | Character |
|---|---|---|---|
| Distribution / lower highs | 2026-05-01 → 2026-05-29 | 268.26 → 270.64, peak 274.99 (05-06) | Choppy, range-bound 259–275 |
| Markdown | 2026-06-01 → 2026-06-25 | 261.26 → 227.01 | Persistent lower highs/lows; −16.1% from 05-06 peak (calc: (227.01−274.99)/274.99) |
| Base / reversal | 2026-06-26 → 2026-07-22 | 232.69 → 244.85 | Higher lows; 06-26 volume spike 248.4M |
| Second leg down | 2026-07-23 → 2026-07-29 | 233.66 → 226.65 | Failed at ~250, retested June low |
| **Breakaway gap** | 2026-07-30 → 2026-07-31 | 235.50 → **271.58** | Gap-and-go, 2.3× normal volume |

Key structural levels derived from actual printed prices [market-amzn]:
- **June low: 225.55 intraday (2026-06-25)**, close low 227.01 — the 2026-07-29 close of 226.65 came within 0.16% of that close low (calc: (226.65−227.01)/227.01 = −0.16%) and **held**. That is a successful retest, and it is the reason the subsequent gap has credibility as a reversal rather than a bounce.
- **Overhead supply: 274.99 (2026-05-06 close) and 278.56 (2026-05-05 intraday high)** [market-amzn]. The 2026-07-31 close of 271.58 sits **just below** this May congestion zone. This is the immediate, concrete resistance the stock must clear.
- The 2026-07-31 high of 273.23 already probed into that zone and closed 1.65 points below the May 6 close [market-amzn].

**Critical nuance:** the stock is back to roughly where it traded on 2026-05-01 (268.26) [market-amzn]. So despite the spectacular single-day move, AMZN has, over the three months in this dataset, gone **sideways-to-nowhere** — it round-tripped a 16% drawdown. The gap recovered the loss; it did not create new highs. Anyone framing this as "breakout to all-time highs" would be overstating the evidence.

---

## 4. Indicator Read-Out (all values as of 2026-07-31, source market-amzn)

**Short-term trend — `close_10_ema` = 242.70** vs close 271.58.
- Derived: price is **+11.90%** above the 10-EMA (calc: (271.58−242.70)/242.70). That is an extreme extension. The 10-EMA is a lagging artifact of the pre-gap price range; it will take several sessions to catch up. **Practical implication: the 10-EMA is useless as a support reference right now** and any "buy the pullback to the 10-EMA" logic would imply a ~29-point, ~10.7% drawdown. Do not use it that way.

**Momentum — MACD complex: `macd` = 0.08, `macds` = −0.84, `macdh` = +0.91** [market-amzn].
- The MACD line has just crossed **above** its signal line (0.08 > −0.84), and the histogram is positive at +0.91. This is a **fresh bullish crossover** — but note the absolute magnitudes are tiny relative to a 271 price. The MACD line at 0