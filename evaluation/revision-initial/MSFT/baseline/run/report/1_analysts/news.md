# News & Macro Research Report — MSFT
**Role:** News Researcher (nonbinding role analysis — not a transaction proposal)
**Analysis date:** 2026-07-30 | **Instrument:** MSFT (Microsoft Corporation, Technology / Software — Infrastructure)
**Frozen latest close:** 451.10 USD [market-msft]

---

## 1. Data availability audit (read this first)

I ran the full tool suite before writing. Results:

| Source | Status |
|---|---|
| Company news — `get_news(MSFT, 2026-07-23 → 2026-07-30)` | **AVAILABLE** — returned the official fiscal Q4 2026 earnings release [src-msft] |
| Global/macro news — `get_global_news` | **NO_DATA_AVAILABLE** (not in frozen corpus) |
| FRED macro — `fed_funds_rate`, `10y_treasury`, `cpi`, `unemployment`, `yield_curve`, `vix` | **NO_DATA_AVAILABLE** (all six) |
| Prediction markets — "Fed rate cut", "recession 2026", "AI capex Microsoft Azure" | **NO_DATA_AVAILABLE** (all three) |

**Consequence:** I have exactly one substantive information set — the MSFT Q4 FY26 earnings release [src-msft] — plus a single frozen price point [market-msft]. I will **not** estimate, interpolate, or recall-from-memory any rate, inflation print, yield, VIX level, or market-implied probability. Every macro and forward-looking-probability statement below is explicitly marked **UNKNOWN**. Any downstream role that needs a rates path, a discount-rate assumption, or a recession probability must source it elsewhere or treat it as an assumption.

---

## 2. Company-specific news: fiscal Q4 2026 (quarter ended June 30, 2026)

Announcement date 2026-07-29, i.e. **one trading day before this analysis** [src-msft]. This is the dominant news event for MSFT and the only company catalyst in the window.

### 2.1 Headline results
- **Revenue USD 90.0 billion, +18%** [src-msft]
- **Operating income USD 40.6 billion, +18%** [src-msft]
- **GAAP EPS 4.81** vs **non-GAAP EPS 4.74** (both **quarterly**, fiscal Q4 2026) [src-msft]
- **Full fiscal year 2026 revenue USD 331.8 billion** [src-msft]

### 2.2 Derived calculations (arithmetic on sourced operands — not sourced facts)
- **Operating margin** = 40.6 / 90.0 = **45.1%** (operands: operating income 40.6B, revenue 90.0B [src-msft])
- **Prior-year Q4 revenue implied** = 90.0 / 1.18 ≈ **76.3B** (operands: 90.0B revenue, +18% growth [src-msft])
- **Prior-year Q4 operating income implied** = 40.6 / 1.18 ≈ **34.4B** (operands: 40.6B, +18% [src-msft])
- **Q4 as share of FY revenue** = 90.0 / 331.8 = **27.1%** (operands: 90.0B, 331.8B [src-msft])
- **GAAP vs non-GAAP EPS gap** = 4.81 − 4.74 = **+0.07**, i.e. GAAP *above* non-GAAP by ~1.5% (operands: 4.81, 4.74 [src-msft])

### 2.3 The segment signal that matters
- **Microsoft Cloud revenue USD 59.3 billion, +27%** [src-msft]
- **Azure and other cloud revenue +43%** [src-msft]
- **Cloud share of total revenue** = 59.3 / 90.0 = **65.9%** (operands: 59.3B, 90.0B [src-msft])
- **Implied prior-year Cloud revenue** = 59.3 / 1.27 ≈ **46.7B** (operands: 59.3B, +27% [src-msft])

**Interpretation (analyst judgment, not sourced fact):** The critical structural read is the *spread* between Azure at +43% and total company growth at +18% [src-msft]. Azure is growing roughly 2.4x the corporate rate (calculation: 43 / 18), which means the cloud/AI infrastructure line is carrying the consolidated growth rate and the mix is still shifting toward the highest-multiple-of-revenue business. Combined with a 45.1% operating margin *while* absorbing that growth (calculation from [src-msft]), the release is consistent with a company that is not currently in a margin-destroying capex/depreciation cycle — at least not at the operating-income line in this quarter. That is the single most important thing a trader can take from this release.

**Caveat on the EPS quality:** GAAP EPS (4.81) exceeding non-GAAP (4.74) [src-msft] is the *unusual* direction — normally non-GAAP is higher because it strips out costs. GAAP above non-GAAP