# Pass 1: first simulation on MCX 5-min history (7 Oct 2026)

**Status: illustration only. Not evidence of an edge.** 6 events per instrument, one month, one volatility regime, no consensus data, simplified fills.

> **Correction (7 Oct 2026, see `eia_pass2_results.md`):** the crude event "9 Sep" below was **not a release day**. The WPSR was delayed by Labor Day to **Thu 10 Sep at 12:00 ET (16:00 UTC)**. For 10 Sep there is no signal (all closes inside the range). Corrected crude totals: five trades, E1 = E3 = **−2.5** points, hold = +16. Continuation in the reaction direction: 4 of 6 events, mean +43 points. The crude figures in the tables below that depend on 9 Sep are superseded.

## 1. Data and method

- **Source:** the user's TradingView chart (MCX continuous front month `CRUDEOIL1!` and `NATGASMINI1!`, 5-min). Bars were read from the chart's loaded series. Each symbol loads about **5,350 bars** (24 Aug to 7 Oct 2026, about 6 weeks, 32 trading days). That is the plan's bar cap, so older 5-min history is not reachable from TradingView. The chart was restored to NATGASMINI1! on 5-min afterwards.
- **Events:** WPSR Wednesdays 26 Aug, 2, 9, 16, 23, 30 Sep (crude). WNGSR Thursdays 27 Aug, 3, 10, 17, 24 Sep, 1 Oct (gas). Release = 14:30 UTC = 8:00 PM IST (US daylight time).
- **Rules simulated (common file §3, §6–§11):**
  - Range = the first three 5-min bars from 14:30 UTC. Midpoint = (high + low) / 2.
  - Signal = first 5-min **close** beyond the range after 14:45 UTC. Entry = open of the next bar.
  - Stop = midpoint, **on touch** (S1). If one bar touches both the stop and a target, the stop is assumed first.
  - Targets = floor pivots from the previous trading day's high, low, close. TP1 = nearest level beyond entry, TP2 = the next one.
  - **E1** = all out at TP1. **E3** = hold to TP2. **Time stop** = 16:00 UTC (90 minutes after release), exit at the last close. **Hold** = no stop, no target, exit at the time stop (reference only).
- **Not applied:** the consensus/data filter (no consensus history), breakeven/trailing (E2), option P&L, costs, slippage. Results are **points of the underlying future**.

## 2. Crude (CRUDEOIL1!, Wednesdays)

| Date | Prev-day range | 15-min range | Reaction first 15 min | Signal | Stop distance | E1 | E3 | Hold | Move after 15 min |
|---|---|---|---|---|---|---|---|---|---|
| 26 Aug | 413 | 18 | +13 | Long | 10 | −10 (stop) | −10 | +93 | +101 |
| 2 Sep | 377 | 29 | +13 | Long | 25.5 | +31 (time) | +31 | +31 | +51 |
| 9 Sep | 258 | 22 | +20 | Long | 13 | +31 (TP1) | +43 (no TP2; time) | +43 | +45 |
| 16 Sep | 549 | 69 | −36 | Short | 44.5 | +79 (time) | +79 | +79 | −93 |
| 23 Sep | 479 | 45 | +5 | Short | 60.5 | −60.5 (stop) | −60.5 | −128 | +50 |
| 30 Sep | 465 | 62 | +10 | Long | 42 | −42 (stop) | −42 | −59 | −19 |
| **Total (points)** | | | | | median ≈ 34 | **+28.5** | **+40.5** | +59 | |

## 3. Gas (NATGASMINI1!, Thursdays)

| Date | Prev-day range | 15-min range | Reaction first 15 min | Signal | Stop distance | E1 | E3 | Hold | Move after 15 min |
|---|---|---|---|---|---|---|---|---|---|
| 27 Aug | 12.3 | 3.9 | −3.2 | Short | 2.45 | +1.0 (time) | +1.0 | +1.0 | −1.6 |
| 3 Sep | 4.9 | 3.5 | −2.5 | Short | 2.55 | +0.4 (TP1, 0.4 away) | +3.2 | +4.1 | −5.1 |
| 10 Sep | 7.6 | 2.6 | +1.1 | Long | 1.5 | −1.5 (stop) | −1.5 | +1.2 | +1.4 |
| 17 Sep | 8.0 | 3.4 | −1.4 | Short | 1.8 | −0.1 (time) | −0.1 | −0.1 | −0.2 |
| 24 Sep ⚠️ | 10.0 | 4.5 | +2.1 | Long | 3.55 | +4.77 | +9.73 | +16.3 | +17.6 |
| 1 Oct | 8.4 | 2.0 | −0.1 | Short | 1.8 | −1.8 (stop) | −1.8 | 0.0 | −1.5 |
| **Total excluding 24 Sep** | | | | | median ≈ 1.8 | **−2.0** | **+0.8** | +6.2 | |

⚠️ **27 Aug pivots are contaminated:** the previous day (26 Aug) had only 20,384 contracts of volume (expiring contract) against about 150,000–330,000 on normal days, so TP1/TP2 for that event are unreliable. See `eia_data_plan.md` §2.

⚠️ **24 Sep is contaminated.** Volume before the release was 39–88 contracts per bar and the front-month series drifted +8%. This looks like the expiring contract in the continuous series. The roll rule matters. Treat 24 Sep as unusable until the contract is checked.

## 3a. What the six-plus-six sample hints at (all ❓)

1. **Continuation vs reversal (B1 vs F1):**
   - After the first 15 minutes, price kept moving **in the direction of the early reaction** in 5 of 6 crude events and 5 of 5 clean gas events.
   - Average continuation in the reaction's direction over the next 90 minutes: crude about **+54 points** (individual events +101, +51, +45, +93, +50, −19), against an average 15-min range of about 41 points. Gas about **+2 points** ex-24 Sep (+1.6, +5.1, +1.4, +0.2, +1.5; the 1 Oct reaction was only −0.1, so that one is noise).
   - This leans toward continuation, which fits breakout (B1) more than fade (F1). The sample is tiny and covers one volatile month.
2. **Stops:** the touch stop was **hit and then price recovered** on 26 Aug (crude, hold +93 vs stop −10) and 10 Sep (gas, hold +1.2 vs stop −1.5). It **saved money** on 23 and 30 Sep (crude, stop −60.5 vs −128, and −42 vs −59). That is 2 whipsaws and 2 saves. No conclusion. Test candle-close stops.
3. **Pivot targets:** TP1 was reached only once in crude (9 Sep) and once cleanly in gas (3 Sep, 0.4 away). Pivots are built from yesterday's range and were often far from the day's price (crude prior-day range 258–549 points, 3–6% of price). 9 Sep had no TP2 level above entry. E1 mostly exited at the time stop.
4. **Realistic stop sizes (replaces my 25-pt and 3-pt illustrations):**
   - Crude: 10–60.5 points, median ≈ 34. Price risk per lot at delta ≈ 0.62: about ₹2,100 at the median (4.2% of ₹50,000) and about ₹3,750 at the worst (7.5%).
   - Gas mini: 1.5–2.55 points, median ≈ 1.8–2. Price risk per lot at delta ≈ 0.6 and 250 mmBtu: about ₹270–380 (0.5–0.8%).
5. **Crude is very volatile in this window:** prior-day ranges of 258–549 points are 3–6% of price. A 15-min range of 18–69 points. Our earlier 25-point stop assumption was on the low side for most weeks.
6. **Simulated totals** (points, underlying): crude E1 +28.5, E3 +40.5; gas ex-24 Sep E1 −2.0, E3 +0.8. These are noise-level for 6 events and should not be used for decisions.

## 4. Limits and what extends this

| Limit | Fix |
|---|---|
| Only about 6 weeks of 5-min history per symbol (plan bar cap) | Add 2 events per week by capturing forward; or buy historical 5-min data; or use coarser bars for a longer continuation test |
| No consensus history, so the data filter is untested | Collect 50 weeks of consensus vs actual (Investing.com history) |
| Continuous-contract rolls (24 Sep gas) | Use a defined contract by volume, not `1!` |
| Fills: touch stop, next-bar open, no costs | Re-test with candle-close stop, spread and costs |
| MCX vs NYMEX differences | None needed if we only trade MCX; use NYMEX only as a proxy for long history |

## Change Log
- 2026-10-07: pass 1 run on 6 crude and 6 gas events from the user's TradingView chart.
- 2026-10-07: 27 Aug pivot contamination noted; raw bars saved in data/ (see eia_data_plan.md).
- 2026-10-07: crude 9 Sep corrected to 10 Sep (Labor Day delay); superseded by pass 2.
