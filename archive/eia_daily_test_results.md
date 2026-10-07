# Daily-horizon test on free EIA history (7 Oct 2026)

**Question:** without consensus data, does a de-seasonalised inventory shock predict WTI / Henry Hub spot returns around the release? This is the idea taken from the Cushing repo (common file §17), run with parameters fixed in advance.
**Answer in one line: the free-data proxy does not measure the surprise well, so this test cannot settle our question.**

## 1. Downloaded files (user approved, from eia.gov, 7 Oct 2026; saved in `data/eia/`)

| File | Content | Coverage | Size |
|---|---|---|---|
| `RWTCd.xls` | WTI Cushing spot, daily, $/bbl | 2 Jan 1986 to 29 Sep 2026 | 471 KB |
| `RNGWHHDd.xls` | Henry Hub spot, daily, $/mmBtu | 7 Jan 1997 to 29 Sep 2026 | 295 KB |
| `WCESTUS1w.xls` | US commercial crude stocks excl. SPR, weekly, kb | 20 Aug 1982 to 25 Sep 2026 | 130 KB |
| `W_EPC0_SAX_YCUOK_MBBLw.xls` | Cushing crude stocks, weekly, kb | 16 Apr 2004 to 25 Sep 2026 | 76 KB |
| `WGTSTUS1w.xls` | US total gasoline stocks, weekly, kb | 5 Jan 1990 to 25 Sep 2026 | 113 KB |
| `WDISTUS1w.xls` | US distillate stocks, weekly, kb | 20 Aug 1982 to 25 Sep 2026 | 130 KB |
| `NW2_EPG0_SWO_R48_BCFw.xls` | Lower 48 working gas, weekly, Bcf | 1 Jan 2010 to 25 Sep 2026 | 66 KB |

- ✅ Latest values match the EIA figures we verified: commercial crude 427,320 kb, Cushing 24,301 kb, working gas 3,415 Bcf.
- Script and outputs: `data/eia/daily_horizon_test.py`, `daily_horizon_output.txt`, `*_z_returns.csv`. Gasoline and distillate files are saved but not used yet.

## 2. Method (fixed before looking)

- Weekly change = this week's stock − last week's. Expected change = mean of the same-week change over the previous 5 years. **Proxy surprise = change − expected**, then z = surprise ÷ SD of the previous 260 weekly surprises (past data only).
- Release day = Wednesday (crude) or Thursday (gas) after the week ending, shifted one day when a federal holiday falls early in the week (approximate).
- Returns in %, log: **R0** = release day vs previous day, **R1** = next day, **R2** = two days later (from the release-day close).
- "Strong" = |z| ≥ 0.8 (the repo's threshold). **Aligned** return = in the direction of the bias (negative z is bullish).
- Sub-periods fixed in advance.

## 3. Results

| Series | n | corr(z, R0) | corr(z, R1) | corr(z, R2) |
|---|---|---|---|---|
| **Crude** 2000–2026 | 1,377 | **−0.089** (t −3.3) | +0.056 (t +2.1) | +0.027 (+1.0) |
| Crude 2000–2014 | 767 | **−0.147** (t −4.1) | +0.011 (+0.3) | −0.042 (−1.2) |
| Crude 2015–2026 | 610 | −0.032 (t −0.8) | **+0.100** (t +2.5) | **+0.097** (t +2.4) |
| Cushing 2012–2026 | 759 | +0.060 (t +1.7) | +0.042 (+1.2) | +0.027 (+0.8) |
| **Gas** 2016–2026 | 551 | **+0.127** (t +3.0) | −0.069 (t −1.6) | +0.012 (+0.3) |

Strong signals (|z| ≥ 0.8), average return **in the direction of the bias**:

| Series | n | Release day (R0) | Next day (R1) | Two days (R2) |
|---|---|---|---|---|
| Crude 2000–2014 | 299 | **+0.54%** (t +3.3) | +0.04% | +0.27% |
| Crude 2015–2026 | 267 | +0.18% (t +0.7) | **−0.53%** (t −2.6, win 46%) | **−0.63%** (t −2.3, win 43%) |
| Cushing 2012–2026 | 299 | −0.23% | −0.22% | −0.13% |
| Gas 2016–2026 | 155 | −1.92% (t −1.8) | +1.71% (t +1.4) | −0.35% |

## 4. What this means

1. **Sanity check on the proxy.** A real surprise should move the price the right way on the release day: negative z (draw) should give a higher price, so corr(z, R0) should be negative.
   - **Crude passes in 2000–2014** (−0.15, t −4.1) but **fades to nothing in 2015–2026** (−0.03).
   - **Cushing fails** (+0.06, wrong sign).
   - **Gas fails clearly** (+0.13, t +3.0, wrong sign).
   - Reason ❓: the market reacts to the surprise against the *consensus*. A gap from a 5-year seasonal average is mostly predictable (weather, production trends), so it is already priced in. For gas it can even carry the opposite sign.
2. **The one eye-catching result is a crude reversal in 2015–2026** (fading the bias after the release-day close made about +0.5% over 1 day and +0.6% over 2 days, t −2.6 and −2.3, 54–57% wins). Do not trust it:
   - About 20 numbers were examined; at that count a t of 2.5 is expected by chance a few times (adjusted, p is about 0.15).
   - The proxy barely moved the price on the release day in that period (R0 not significant), so it is not clearly a "surprise" test.
   - It is absent in 2000–2014.
   - It is a close-to-close daily effect on spot, not an intraday or option result.
3. **Consistent with the literature:** no strong next-day continuation. If anything, mild reversal.
4. **Consensus is needed.** The test supports the plan to collect true consensus-versus-actual history (Investing.com). The free proxy is not a substitute for crude after 2015 or for gas at all.
5. **Gas needs weather/forecast information** (or consensus) to separate expected from unexpected storage changes.

## 5. Limits
- Spot, not futures, and daily; no intraday timing; release-day alignment approximate; no costs.
- 2020 negative prices removed for WTI (price filter > $5).
- Overlapping windows are not independent; t-stats are indicative.

## Change Log
- 2026-10-07: created. Free EIA history downloaded; daily-horizon proxy test run for crude, Cushing and gas.
