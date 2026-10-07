# 05 Evidence: What We Know and What We Do Not

**Last revised:** 7 Oct 2026. "Read" = I opened the source. "Snippet" = only a search-result summary (treat as ❓).
**Bottom line: no edge is visible in our data, and none is ruled out. The literature says the reaction to an EIA surprise completes within minutes, so a 15-minute breakout entry is late.**

## 1. Literature and external sources

| # | Finding | Source | Status |
|---|---|---|---|
| R1 | Futures react to EIA inventory surprises **within about 5–7 minutes** and the response **did not revert** by the study's later reference point (about 100 minutes). Sample 16 Jul 2003 to 30 Jun 2017, front-month NYMEX; surprise = actual − Bloomberg median forecast, scaled by its SD | [Linn et al., EIA presentation, 2017](https://www.eia.gov/finance/markets/reports_presentations/2017/linn.pdf) (citing Halova et al. 2014) | ✅ read |
| R2 | A different study: the reaction lasts about **25 minutes** and **the price reverts quickly** afterwards; larger reaction when analysts disagree more | Rousse et al., Energy Journal 40(2) (IAEE summary) | ❓ snippet |
| R3 | Response per **1 SD of surprise**: crude −0.429 (before June 2006) → **−0.271** after; gas −0.708 → **−1.163**. Units assumed to be % log price change. No difference between positive and negative surprises | Linn et al. | ✅ read; units ❓ |
| R4 | **No relation between surprises and price changes on the two days after the release** | Linn et al. | ✅ read |
| R5 | Average absolute return rises with the **absolute size of the surprise** (a bigger miss gives a bigger early range) | Linn et al. | ✅ read |
| R6 | Crude, gasoline and distillate surprises each move crude **in the same direction**; gas responds most to its own surprise (−1.005 per SD) | Linn et al. | ✅ read |
| R7 | EIA's own **sampling standard error** for gas net change: about **2 Bcf** (Lower 48), about 1 Bcf per region; 2.2–5.5 Bcf in 2016 weeks with withdrawals above 100 Bcf; 1.0–3.2 Bcf in other weeks | [EIA Today in Energy](https://www.eia.gov/todayinenergy/detail.php?id=29712) | ✅ read |
| R8 | Analyst gas forecasts averaged about **13.2 Bcf** absolute error per week since 2002. Bloomberg median crude forecasts are "considerably less accurate" and underestimate the change | Search snippets (Ederington et al., Energy Journal 40(5)) | ❓ snippet |
| R9 | **IV drifts up before scheduled releases and drops after**; realized volatility rises on release days | Search snippets | ❓ size unknown |
| R10 | Public academic tests of **floor/Camarilla pivots on energy futures are scarce** | Search summary | ✅ finding |
| R11 | Published support/resistance levels did predict **intraday trend interruptions** (FX, six firms, 1996–98), not floor pivots, not energy | [Osler, NY Fed 2000](https://resources.newyorkfed.org/medialibrary/media/research/epr/00v06n2/0007osle.pdf) | ❓ snippet |
| R12 | **No comparative evidence** for a range-midpoint stop vs an opposite-edge stop; only retail ORB backtests on ES | TradingView / edgeful pages | ✅ finding |
| R13 | Trade-press gas examples show **partial retracement within 15 minutes** after a surprise | NGI articles | ❓ anecdote |

**The Cushing inventory repo** ([codingshujaa/Cushing-Inventory-WTI-trading-model](https://github.com/codingshujaa/Cushing-Inventory-WTI-trading-model); README and `.qmd` read via a summariser, figures ❓):
- Signal: z-score of the weekly **Cushing change** (training mean/SD, ±0.8 SD thresholds from a grid search). **No consensus.**
- Rule: big build while the 4-week MA is above the 13-week MA → short; big draw while below → long (with the data bias, against the trend). The README calls it "mean reversion", which is misleading.
- Entry at the daily close on release day; target $1.20, stop $0.80, at most 2 days; **no costs**. Train 2010–2023: 87 trades, win rate about 59%, about +$32. **Test 2024+: 16 trades, win rate about 44%, about +$1.9.**
- Assessment: break-even win rate is 0.80/(0.80+1.20) = 40%, so 44% is barely above it before costs. Thresholds were tuned on the training data; seasonality is ignored; not comparable to our intraday options setup. Ideas taken: standardise in SD units, a trend-relation filter, fix parameters in advance, judge in risk multiples.

## 2. Our tests

**Common method:** MCX continuous front month read from the user's TradingView chart (bar cap about 5,350 bars per symbol). Release time converted to UTC with the correct holiday exceptions (`data/events.csv`). Days or previous days with volume under 50% of the previous 5-day median are excluded (contract roll). Results are in **points of the underlying**, no costs, no option Greeks, no consensus filter. A bar that touches both stop and target counts as stopped first.

### 2.1 Pass 1: 5-minute bars, 6 + 6 events (24 Aug to 1 Oct), corrected

- ⚠️ The first run used crude "9 Sep" as a release day; the WPSR was actually **Thu 10 Sep at 12:00 ET** (no signal that day). **Corrected:** five crude trades, E1 = E3 = **−2.5** points, hold to the time stop **+16**; continuation in the reaction direction **4 of 6** events (mean +43). Gas (five clean events; 24 Sep is the expiring contract): E1 −2.0, E3 +0.8, hold +6.2; **5 of 5** same direction (mean about +2). 27 Aug gas pivots came from a thin expiring-contract day.
- Stops measured: crude median 42 (n = 5), gas 1.8. TP1 pivots were reached once in crude (on the invalid date) and once trivially in gas.

### 2.2 Pass 2: 15-minute and 30-minute bars, about 15–22 events

Does price continue in the direction of the first reaction? (direction-adjusted mean continuation after the reaction; SD and t-statistic)

| Test | n | Same sign as reaction | Mean continuation | SD | t |
|---|---|---|---|---|---|
| Crude 15-min (next 75 min) | 15 | 9 (60%) | +22 pts | 51 | 1.7 |
| Crude 30-min (next 60 min) | 22 | 12 (55%) | +8 pts | 59 | 0.7 |
| Gas 15-min | 14 | 9 (64%) | +1.2 pts | 2.5 | 1.8 |
| Gas 30-min | 19 | 11 (58%) | +0.7 pts | 2.3 | 1.3 |

Strong reactions only (≥ median) are no better (crude 6 of 11, gas 6 of 10 same sign). All four means lean positive, none reaches t = 2, the windows overlap. About 20 or more events would show a real effect of this size.

Simulated trades, 15-minute opening range (points; crude 13 trades, gas 11):

| Exit design | Crude total | Gas total |
|---|---|---|
| E1 (touch stop, nearest-pivot TP1) | **−6.5** (6 of 13 positive; TP1 never reached) | **+1.0** |
| E1c (stop on bar close) | −58 | +1.0 |
| Target 1× stop | −19 | +1.6 |
| Target 1.5× stop | −61.5 | +1.3 |
| Target 2× stop | −44.5 | +1.3 |
| Hold to time stop, no stop | **+19** | +3.5 |

Every design is within noise of zero. Pivot TP1 median distance in crude was about 118 points, about 2.7 times the stop. Prior-day ranges were 3–6% of price in this window, so yesterday's pivots sit far from the day's price. **Measured stops: crude median 43 points (range 14–91.5); gas median 2.2 (range 1.4–7.05).** Touch vs close stop: one clear crude whipsaw (5 Aug), one clear crude gap-through (23 Sep, closed-bar stop −121). The crude window was very volatile (futures between about 6,000 and 9,900 within months).

### 2.3 Daily-horizon test on free EIA history (consensus-free proxy)

Weekly change minus the 5-year same-week mean, divided by its recent SD (z); returns on WTI/Henry Hub **spot** around the release day (R0 release day, R1 next day, R2 two days). Parameters fixed in advance; script in `data/eia/daily_horizon_test.py`.

| Series | n | corr(z, R0) | corr(z, R1) | corr(z, R2) |
|---|---|---|---|---|
| Crude 2000–2026 | 1,377 | −0.089 (t −3.3) | +0.056 (+2.1) | +0.027 |
| Crude 2000–2014 | 767 | **−0.147** (t −4.1) | +0.011 | −0.042 |
| Crude 2015–2026 | 610 | −0.032 (t −0.8) | **+0.100** (t +2.5) | **+0.097** (t +2.4) |
| Cushing 2012–2026 | 759 | +0.060 | +0.042 | +0.027 |
| Gas 2016–2026 | 551 | **+0.127** (t +3.0) | −0.069 | +0.012 |

- A real surprise should lift the price on release day after a draw, so corr(z, R0) should be **negative**. **The proxy passes this only for crude before 2015, fails for Cushing and fails clearly for gas** (wrong sign). Likely reason: a gap from a seasonal average is largely predictable and already priced; the market reacts to the surprise versus **consensus**.
- The crude reversal since 2015 (fading the bias after release-day close earned about +0.5% over 1 day and +0.6% over 2 days, t −2.6 and −2.3, 54–57% wins) is **not trusted**: about 20 numbers were examined, the proxy barely moved the price on release day in that period, and it is absent in 2000–2014. Not an intraday or option result.

### 2.4 True consensus surprises on the daily horizon (about 2 years)

Source: Investing.com history (99 weeks, fetched with `scripts/fetch_investing_playwright.py`) joined to EIA daily spot prices. Surprise = actual − consensus, in SD units (crude SD 4.82 mb, gas SD 9.39 Bcf). Returns are % log changes of WTI / Henry Hub spot: R0 release day, R1 next day, R2 two days later.

| Series | n | corr(z, R0) | corr(z, R1) | corr(z, R2) | Slope on release day |
|---|---|---|---|---|---|
| Crude | 98 | −0.082 (t −0.8) | −0.056 (t −0.5) | +0.069 (t +0.7) | −0.25% per 1 SD |
| Gas | 97 | **−0.350** (t −3.6) | **−0.296** (t −3.0) | **−0.262** (t −2.6) | −2.9% per 1 SD |

- ✅ **The sign is right for both** (a draw lifts the price), unlike the free proxy. The crude slope of −0.25% per SD is close to the literature's −0.27% (R3) but **not significant at n = 98**.
- **Gas reacts strongly and the effect continues on days 1 and 2** (t −3.0 and −2.6; Bonferroni threshold for 6 tests is about t 2.7, so the day-1 result passes and day 2 is borderline). Caveats ❓: weather news is persistent and drives both the storage number and the following price moves; and the EIA daily spot series may be timed a day behind futures. Needs a futures-based check.
- Crude shows **no drift on days 1–2**, consistent with R4. These are daily results; the intraday MCX evidence (2.2) is still small.

### 2.5 True consensus surprises on 15 years (rerun of 2.4)

Source: `data/releases_crude.csv` / `releases_gas.csv` (usable rows, 2011 on, forecast present: crude 780 weeks, gas 767 usable with spot prices). z = surprise ÷ SD of **earlier** surprises only. Same spot returns as 2.4. Script `scripts/surprise_test_15y.py`, results `data/surprise_test_15y.csv`; parameters and periods fixed before running.

| Series | Sample | n | corr(z, R0) | corr(z, R1) | corr(z, R2) | Slope R0 (% per SD) |
|---|---|---|---|---|---|---|
| Crude | 2011–2026 | 780 | **−0.116** (t −3.3) | +0.041 | +0.035 | −0.31 |
| Crude | 2011–2018 | 383 | −0.236 (t −4.7) | 0.00 | −0.01 | −0.51 |
| Crude | 2019–2026 | 397 | −0.055 (t −1.1) | +0.062 | +0.064 | −0.17 |
| Crude | \|z\| ≥ 1 | 278 | −0.243 (t −4.2) | +0.075 | +0.034 | −0.34 |
| Gas | 2011–2026 | 767 | −0.072 (t −2.0) | **−0.160** (t −4.5) | +0.031 | −0.42 |
| Gas | 2011–2018 | 371 | −0.021 | −0.272 (t −5.4) | −0.076 | −0.08 |
| Gas | 2019–2026 | 396 | −0.087 | −0.142 (t −2.8) | +0.063 | −0.57 |

- ✅ **Crude:** the sign is right and the slope on release day is **−0.31% per SD**, matching the literature's −0.27% (R3). No drift on days 1–2 (R4 confirmed on 15 years). **The effect has faded: −0.24 correlation in 2011–2018, −0.06 (not significant) in 2019–2026.** Large surprises (|z| ≥ 1) carry most of it.
- ✅ **Gas:** the reaction shows on **day 1, not on the release day** (R1 −0.16, t −4.5; R0 only −0.07), and **nothing on day 2**. So the "continuation on days 1–2" in 2.4 was mostly a timing artifact: the EIA daily Henry Hub spot is struck before 10:30 ET, so day 1 holds the reaction. Exploratory (not pre-registered) R0+R1 slope: **−1.8% per SD** (literature −1.16%), 2011–2018 −1.4, 2019–2026 −2.0.
- ❓ The last-2-year gas numbers (slope −3.5 on R0, −9.7 on R0+R1) are far above the 15-year level: **a thin, unstable sample, not a better estimate.**
- **What this does not show:** these are daily spot returns. It confirms the direction and size of the surprise effect, **not** that a 15-minute breakout entry after the move has an edge (the reaction is complete within minutes, R1).

## 3. What we know and do not know

| Known (✅) | Not known (❓) |
|---|---|
| The main reaction completes in minutes (R1); no next-day drift (R4) | Whether price continues after the first 15 minutes (B1) or fades (F1): sources conflict, our samples (n 14–22) are inconclusive |
| A bigger surprise gives a bigger range and bigger risk (R5) | Whether the consensus surprise predicts the next 60–75 minutes (needs consensus history) |
| Products move crude in the same direction (R6) | The conflict-flag rule |
| Gas sampling noise is about 2 Bcf (R7). **Typical misses: crude SD 4.82 mb (median 3.0), gas SD 9.39 Bcf (median 5.0)** | Whether the 2-year miss distribution holds going forward |
| Pivots from yesterday's range are far from the 90-minute action; stops are about 43 (crude) and 2.2 (gas) points | Whether targets as multiples of the stop beat pivots (not distinguishable at n ≈ 13) |
| The free-data proxy cannot stand in for consensus | The real IV change around the release (needs chain snapshots at T − 5 and T + 15) |

## 4. Implications for the spec

1. Treat **B1 vs F1** as an open test; do not assume continuation.
2. Prefer **targets as multiples of the stop** over pivots as the default to test next.
3. Express the surprise threshold in **SD units** once we have consensus history; for gas it must exceed about 2 Bcf.
4. Record risk per trade (crude about 5% of the account at the median stop) and judge results in risk multiples, not "cumulative return".
5. Use forward capture from 7 Oct 2026 as the clean out-of-sample set; do not tune on it.
