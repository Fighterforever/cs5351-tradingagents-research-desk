# MSFT Technical Analysis Report
**Role: Market Analyst (technical)** — nonbinding role analysis, not a transaction proposal.
Ticker MSFT, analysis date 2026-07-30, latest close 451.10 USD [market-msft].

---

## 1. Data integrity and indicator availability (read this first)

Two of my preferred indicators could not be computed, and I will not fabricate them:

- **close_50_sma: NO_DATA_AVAILABLE** — the tool reports the 50-row window is unavailable (only 30 rows available at 2026-07-30) [market-msft].
- **close_200_sma: NO_DATA_AVAILABLE** — same constraint, 200 rows required [market-msft].

This is a real limitation, not a rounding issue. The frozen CSV I retrieved spans 2026-05-01 to 2026-07-30 and contains 62 records, but the indicator vendor only exposes a 30-row window at the current date. **Consequence: I cannot verify a golden-cross/death-cross state, cannot verify whether price is above or below the 200-day, and cannot state long-term trend structure as a sourced fact.** Any claim about the 200-day would be an invention. I flag this explicitly rather than substituting an estimate.

The verified snapshot confirms the exact OHLCV for the current bar: open 437.90, high 458.69, low 432.44, close 451.10, volume 110,160,700 [market-msft]. This matches the final row of the price CSV — no discrepancy between tools.

---

## 2. The dominant fact: a post-earnings gap of extraordinary size

The single most important observation is the 2026-07-30 session. MSFT closed 2026-07-29 at 390.54 [market-msft] and closed 2026-07-30 at 451.10 [market-msft].

- Point change: 451.10 − 390.54 = **+60.56** (calculation from the two closes above [market-msft]).
- Percentage change: 60.56 / 390.54 = **+15.51%** (calculation, operands [market-msft]).
- Volume: 110,160,700 on 2026-07-30 versus 47,209,000 on 2026-07-29 [market-msft] — roughly 2.33× the prior session (calculation from those two volume figures [market-msft]).

This is a genuine gap, not an intraday drift: the open of 437.90 was already 47.36 above the prior close (calculation, operands [market-msft]), i.e. the market repriced MSFT by ~12.1% before the first trade. The day then extended to a high of 458.69 and closed at 451.10, in the upper half of the 432.44–458.69 range [market-msft]. Closing 13.20 below the high but 18.66 above the open (calculations, operands [market-msft]) describes a session that gapped, probed higher, and held most of the gain — constructive, but with a visible intraday fade from the high.

**Fundamental trigger (the only earnings source):** fiscal Q4 2026 (ended June 30) revenue USD 90.0 billion, +18%; operating income 40.6 billion, +18%; GAAP EPS 4.81 vs non-GAAP 4.74; Microsoft Cloud revenue 59.3 billion, +27%; Azure and other cloud revenue +43%; full-year revenue 331.8 billion [src-msft]. The Azure +43% figure is the line that plausibly explains a 15% single-day repricing, but I note that as interpretation, not sourced fact — the source does not attribute the price move.

**EPS discipline:** 4.81 is a **single-quarter** GAAP figure [src-msft]. It is not a TTM number. I have no TTM EPS in the sources, therefore **trailing P/E is UNKNOWN** and I will not compute or imply one. Any valuation multiple, price target, or forward estimate is likewise UNKNOWN from the observed sources.

---

## 3. Trend structure: short-term strongly up, medium-term recovering from a deep drawdown

Reconstructing the path from the CSV [market-msft]:

- **May 2026: base-building.** The month opened at 414.44 (2026-05-01) and chopped in a 400–430 band, with a low close of 405.21 on 2026-05-13 [market-msft].
- **Late-May/early-June spike and failure.** A sharp two-day surge took MSFT from 412.67 (2026-05-27) to 426.99 (2026-05-28) to 450.24 (2026-05-29) on 79.65M volume, then to a **local peak close of 460.52 on 2026-06-01** [market-msft]. That peak did not hold.
- **June 2026: sustained distribution.** From 460.52 (2026-06-01) the stock fell to a **trough close of 352.83 on 2026-06-25** [market-msft]. Decline: 460.52 − 352.83 = 107.69, or **−23.4%** (calculation, operands [market-msft]). Note 2026-06-26 printed 186,201,600 volume — the largest in the dataset — on a day that closed up at 372.97 from 352.83 [market-msft], consistent with capitulation-style volume, though I cannot assert the causal mechanism from price data alone.
- **July 2026: repair.** From the 352.83 low, MSFT ground back through 384.28 (2026-07-01), 401.10 (2026-07-16), and 393.35 (2026-07-28) before the earnings gap to 451.10 [market-msft].

**Net position:** the 2026-07-30 close of 451.10 [market-msft] is still **below** the 2026-06-01 peak close of 460.52 [market-msft] — by 9.42, or −2.0% (calculation, operands [market-msft]). So the gap recovered the entire June drawdown but has *not* yet made a new high on a closing basis. That is a materially different picture from "breakout to new highs," and it matters for how aggressively one should chase.

---

## 4. Moving averages: price is stretched far above every available average

- **close_10_ema = 401.04** [market-msft]. Close 451.10 is **50.06 above** it, or **+12.5%** (calculation, operands [market-msft]). This is an extreme short-term extension. The 10-EMA is a lagging, responsive average and a one-day 15% gap mechanically detaches price from it; mean-reversion pressure toward this average is a live risk.
- **boll (20-SMA) = 393.15** [market-msft]. Close is **57.95 above**, or **+14.7%** (calculation, operands [market-msft]).
- **vwma = 386.48** [market-msft]. Close is **64.62 above**, or **+16.7%** (calculation, operands [market-msft]). The volume-weighted average sitting *below* the simple 20-SMA tells us the heavy-volume days of the last month clustered at lower prices — i.e. the volume-weighted holder base is underwater-to-flat and now deeply in profit. That is supportive of holding, but it also means the marginal buyer is paying a large premium to the recent volume-weighted cost basis.

**Interpretation:** every computable average is far below price. This is the signature of a gap-driven repricing, not a gradual trend. Trend-following entries here are entries at a 12–17% premium to short-term fair-value anchors.

---

