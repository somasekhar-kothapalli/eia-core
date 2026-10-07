# Pass 2: 15-minute and 30-minute bars, longer sample (7 Oct 2026)

**Status: illustration only. No edge is visible and none can be ruled out.** About 15 usable events per instrument, one volatile 4–6 month window, simplified fills, no consensus data.

## 1. Corrections found while preparing this run ✅

1. **Holiday-delayed WPSR releases come out on Thursday at 12:00 ET, not 10:30.** EIA schedule: Thu 22 Jan, 19 Feb, 28 May, **10 Sep**, **15 Oct**, 12 Nov 2026 (all 12:00 ET). WNGSR exceptions in 2026: Fri 13 Nov 10:30 ET and Wed 25 Nov 12:00 ET.
2. **The pass-1 crude event "9 Sep" was not a release day.** The release was Thu 10 Sep at 12:00 ET = 16:00 UTC = **9:30 PM IST**. Pass 1 is corrected (below). The crude 5-min file now holds 10 Sep instead of 9 Sep. Event list: `data/events.csv`.
3. **Pass-1 crude, corrected:** 10 Sep gave **no signal** (all closes stayed inside the 9324–9409 range). Five crude trades remain: E1 = E3 = **−2.5** points in total (not +28.5 / +40.5). Hold = +16. Continuation in the reaction direction: 4 of 6 events, mean +43 points. The earlier "5 of 6" and the positive totals were partly the invalid date.

## 2. Data and method

- **Data:** MCX continuous front month, 15-min bars 1 Jun to 7 Oct 2026 (5,232 bars) and 30-min bars from 30 Mar (crude) and 24 Apr (gas). TradingView's bar cap is the limit.
- **Events:** crude on WPSR days (Wednesday, or the Thursday 12:00 ET delay), gas on Thursdays at 10:30 ET. Release time converted to UTC by the US daylight-time rule.
- **Excluded:** any event day, or its previous day, with volume under 50% of the previous 5-day median (contract roll). Crude: 17 Jun, 19 Aug. Gas: 25 Jun, 27 Aug, 24 Sep. Also excluded: events without a full prior history.
- **15-min rules:** opening range = the release bar (15 min). Signal = first 15-min **close** beyond it within the next 75 minutes. Entry = open of the next bar. Stop = midpoint **on touch** (E1…), or on bar **close** (E1c). Time stop = 90 minutes after release. Targets: pivots (E1), or multiples of the stop distance (R1, R1.5, R2). If a bar touches both stop and target, stop first.
- **30-min:** continuation only. Reaction = close of the release bar minus the previous close. Continuation = change over the next 60 minutes. Direction-adjusted = continuation × sign(reaction).
- Results are in **points of the underlying future**. Not option P&L.

## 3. Does price continue in the direction of the early reaction?

| Test | n | Same sign as reaction | Mean continuation, direction-adjusted | SD | t-stat |
|---|---|---|---|---|---|
| Crude 15-min (next 75 min) | 15 | 9 (60%) | +22 pts | 51 | **1.7** |
| Crude 30-min (next 60 min) | 22 | 12 (55%) | +8 pts | 59 | **0.7** |
| Crude 30-min, strong reactions only (≥ median 55 pts) | 11 | 6 | −5 pts | | |
| Gas 15-min | 14 | 9 (64%) | +1.2 pts | 2.5 | **1.8** |
| Gas 30-min | 19 | 11 (58%) | +0.7 pts | 2.3 | **1.3** |
| Gas 30-min, strong reactions only (≥ median 2.2) | 10 | 6 | +0.8 pts | | |

- All four means lean positive (continuation), but **none reaches t = 2**. Sample windows overlap, so the four tests are not independent. At the observed spread, about 20 or more events would show a real effect of this size. We have 14–22.
- The pass-1 "5 of 6" reading was small-sample luck. With more events, continuation is **60% / 55% / 64% / 58%**, close to a coin flip.
- Conclusion: **B1 (continuation) neither confirmed nor rejected. F1 (fade) is not supported either.**

## 4. Simulated trades, 15-min opening range (points of the underlying)

**Crude, 13 trades** (15 events, 2 with no signal):

| Exit design | Total | Note |
|---|---|---|
| E1: stop on touch, TP1 = nearest pivot | **−6.5** | 6 of 13 positive. **TP1 never reached** |
| E1c: stop on bar close | **−58** | gaps through the stop (e.g. −121 on 23 Sep) |
| R1: target at 1× stop | −19 | |
| R1.5: target at 1.5× stop | −61.5 | |
| R2: target at 2× stop | −44.5 | |
| Hold to the time stop, no stop | **+19** | one big win (+89, 26 Aug) and one big loss (−121) |

**Gas, 11 trades** (14 events, 3 with no signal):

| Exit design | Total |
|---|---|
| E1 (touch stop, pivot TP1) | **+1.0** (≈ +₹257 per mini lot) |
| E1c (close stop) | +1.0 |
| R1 / R1.5 / R2 | +1.6 / +1.3 / +1.3 |
| Hold to the time stop | +3.5 |

- **Every design is within noise of zero.** Across 13 crude trades the best (hold) is +19 points and the worst (E1c) is −58, against a median stop of 43 points. Across 11 gas trades the range is +1 to +3.5 points against a median stop of 2.2.
- **Pivot targets are too far for a 90-minute window.** Crude TP1 median distance about 118 points (about 2.7 times the stop), reached **0 of 13** times. Gas TP1 reached about 1 of 11. Yesterday's range sets the pivots, and it is 3–6% of price in this sample.
- **Touch vs close stops:** crude closed-bar stops were worse (−58 vs −6.5) because price gapped through the midpoint. Gas was identical. One crude whipsaw (5 Aug: touch stop −21.5, price then recovered to +40). No clear winner.

## 5. Stop sizes and risk on ₹50,000 (replaces earlier illustrations)

| | Median stop | Range | Price risk per lot at delta ≈ 0.62 / 0.6 | % of ₹50,000 |
|---|---|---|---|---|
| CRUDEOIL (100 bbl) | **43 pts** | 14–91.5 | ₹2,666 median; ₹5,673 worst | **5.3%** median; **11%** worst |
| NATGASMINI (250 mmBtu) | **2.2 pts** | 1.4–7.05 | ₹330 median; ₹1,058 worst | **0.7%** median; **2.1%** worst |

- ⚠️ **Crude risk per trade is 5% of the account at the median and 11% at the worst, much larger than the 3% I estimated.** One crude lot is also 79–94% of the account in premium. This is the user's accepted Phase 1 choice, but the numbers are now explicit.
- Gas mini is comfortable: 0.7% median.
- Gas opening ranges: median ≈ 3 points. Crude: median ≈ 44 points (0.5% of price).

## 6. What we learned

1. The strategy as written shows **no measurable edge in about 4–6 months of MCX data**, and no clear harm either. The literature said the reaction completes in about 5–7 minutes, and a 15-minute breakout entry is late.
2. **Pivots from the prior day are poor targets** when the prior-day range is 3–6% of price.
3. **Contract rolls matter** (5 flagged event days). The roll rule is needed.
4. **Calendar exceptions matter**: 10 Sep (crude 12:00 ET) and next week's **Thu 15 Oct** (WPSR at 12:00 ET = 9:30 PM IST, and the crude options expire that day).
5. The honest next step is more events, and a **simpler hypothesis test**: does the data surprise, not only price, predict the next 60–75 minutes? That needs consensus history.

## 7. Limits

- n ≈ 15 per instrument; windows overlap; a volatile regime (crude moved between 6,000 and 9,900 in this window).
- Touch stops assumed to fill at the midpoint; no costs, slippage, option Greeks, or IV.
- MCX continuous-contract artifacts despite the volume filter.
- No consensus filter, no E2 breakeven/trailing, no 3-min test.

## Change Log
- 2026-10-07: created. Corrects pass 1 (crude 9 Sep → 10 Sep).
