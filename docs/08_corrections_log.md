# 08 Corrections Log (every source claim checked)

Consolidated from the earlier per-file logs (74 rows, de-duplicated and grouped by topic; some rows combine several related claims). **Verdicts:** ✅ correct · ⚠️ wrong, misleading or inconsistent (fixed in the spec) · ❓ unverified. "Source" = the user's research pastes, or the reference named.

## A. Timing and schedule

| Claim | Verdict |
|---|---|
| Release at 8:00 PM IST all year | ⚠️ Only in US daylight time. 9:00 PM IST from 4/5 Nov 2026 |
| WPSR is always Wednesday 10:30 ET | ⚠️ **Holiday delays are Thursday 12:00 ET** (22 Jan, 19 Feb, 28 May, 10 Sep, 15 Oct, 12 Nov 2026) |
| Two sources write "EST" for the release time (ACY, CFI) | ⚠️ It is EDT in summer |
| 1 hour vs 1.5 hours vs no time stop | ⚠️ Inconsistent. Spec: 90 minutes from release |
| MCX hours 9:00 to 11:30 PM, 11:55 PM in US standard time | ✅ (rule from 9 Mar 2026) |

## B. Report tables and data

| Claim | Verdict |
|---|---|
| Table 1 = "U.S. Petroleum Balance Sheet" | ✅ |
| Cushing is in Table 1 | ⚠️ Wrong: Table 4 (and 9) |
| Refinery utilization is in Table 1 | ⚠️ Wrong: Table 2 (and 9) |
| Column "week-on-week change" in Table 1 | ⚠️ Table 1 says "Difference". The label is from the landing-page box |
| "PADD 2 Stocks at Cushing" | ⚠️ Not an EIA label; the row is "Cushing" |
| "4 core data points" / "4 pillars" | ⚠️ Incomplete (crude); for gas only net change is a trigger and consensus was missing from the list |
| 922 = a 922,000-barrel build | ✅ |
| Gas: read the "Working Gas in Underground Storage, Lower 48 States" table; Summary/CSV/JSON | ✅ |
| "Implied Weather Delta" as a data point | ⚠️ No such item; "implied flow" is a different column; no weather on the WNGSR page |
| HDD/CDD from the EIA storage dashboard | ❓ Partly supported (regional temperatures); HDD/CDD not confirmed; realized data is backward-looking |
| Ignore regional data, "zero impact" | ❓ Opinion; Salt kept as a conflict flag |
| Skip data "to protect execution speed" | ⚠️ Moot: entry waits for the 15-minute range |
| Ignore base gas / peak capacity | ✅ Not in the main table |
| PDFs available at 10:30 | ⚠️ Most per-table PDFs appear at 1:00 p.m. ET; use CSV/XLS/TXT |

## C. Signal and consensus

| Claim | Verdict |
|---|---|
| Surprise = actual − consensus; negative = bullish | ✅ (ACY, gas matrix: all four rows correct) |
| "Draw = bullish" on its own | ⚠️ Only versus consensus |
| "Positive surprise" | ⚠️ Ambiguous; use bullish/bearish |
| "Gas Deviation Alpha" | ⚠️ It is the surprise, not alpha |
| Matrix magnitudes 20–30 Bcf as "strong" | ❓ No threshold; typical miss unknown; floor is EIA sampling error about 2 Bcf |
| Matrix: data alone gives buy call / put with delta 0.70 | ⚠️ Skips breakout confirmation and the chain-based strike pick |
| Consensus source not named | ⚠️ Fixed: Investing.com primary, Trading Economics cross-check |
| Trading Economics link for Cushing | ⚠️ That page is commercial crude; Cushing has no consensus on either site |
| Trading Economics gas consensus = actual | ❓ Possibly overwritten after release |
| Sources in the gas paste, including an unrelated sports-REIT domain | ⚠️ Use EIA primary pages |

## D. Levels, pivots, timeframe

| Claim | Verdict |
|---|---|
| Pivot formulas (P, R1, S1, R2, S2) | ✅ |
| Midpoint = (High + Low) / 2 | ✅ |
| Camarilla R3/R4/S3/S4 formulas | ✅. "Camarilla P" is not part of the set (⚠️) |
| Crude respects floor pivots, gas respects Camarilla | ❓ No evidence |
| R3/S3 as profit targets | ⚠️ Normally reversal levels; design choice |
| A separate 15-minute chart is needed | ⚠️ Redundant (build the range from execution candles) |
| 3-minute chart because 5-minute is too slow | ❓ Opinion; kept as a test variant |
| "Falling back through the midpoint = momentum failed" | ❓ Heuristic |
| "No pivot resistance past R2" | ⚠️ R3/S3 exist |
| "News breakouts systematically reach pivots" | ❓ No evidence (our test: pivot TP1 almost never reached in 90 minutes) |
| Targets are "volatility-adjusted" | ⚠️ Pivots use yesterday's range |

## E. Options, Greeks, IV

| Claim | Verdict |
|---|---|
| IV crush is real | ✅. But IV usually peaks before the print; "spike at release then collapse" is loose |
| ITM options insulate from vega | ⚠️ Only a smaller percentage loss; vega is highest ATM |
| ITM options have maximum gamma | ⚠️ ATM has maximum gamma; on our chains gamma is negligible |
| 1–2 (or 2–3) strikes ITM ≈ delta 0.60 (0.70) | ⚠️ Select by delta from the live chain |
| Delta 0.65–0.75 **and** extrinsic < 20% | ⚠️ Inconsistent (confirmed on the gas chain: delta 0.74 = 23% extrinsic) |
| Delta 0.70 "behaves like a synthetic future" | ⚠️ Wrong: a 0.70 delta passes through about 70% of the move |
| Pre-report IV above 100–120%, collapsing to 60–70% | ❓ Not seen: chains show about 52–58% ATM a day before |
| Delta "cushions" a 20-point fall to about 12 | ⚠️ Arithmetic right (0.60 × 20), but it is pass-through, not protection |
| "Deep ITM" is best for gas | ⚠️ Depends on the move size |
| Mid-market limit orders for gas | Parked (execution) |
| Naked buying wins only 30–40% of the time | ❓ Unsupported |
| "Naked options are melting ice cubes" via theta in 30–45 minutes | ⚠️ Theta over 45 minutes is about 0.1% of premium |

## F. Entry, stop, targets, trailing, time stop

| Claim | Verdict |
|---|---|
| "Close above" vs "body fully outside" the range | ⚠️ Inconsistent; spec uses close beyond |
| Entry "on the open" of the next candle | ⚠️ Not exactly achievable in practice (execution parked); spec defines it on the underlying |
| Stop on the underlying chart translated with delta | ✅ Same principle (`(entry − stop) × delta`) |
| Midpoint stop on touch although the source says gas has stop-hunt wicks | ⚠️ Contradiction; test touch vs close |
| "Institutional order flow failed" at the midpoint | ❓ Narrative |
| Stop "never as a % of premium" and "cap 20–30% of premium" | ⚠️ Contradicts itself; also never binds for ITM options |
| Stops as market orders on the option from a future-price level | ⚠️ Not native on MCX options (parked) |
| Profit target 40–60% of premium | ⚠️ Needs 264 crude points or 13–15 gas points |
| 60/40 scaling; "50% rule" | ⚠️ Needs at least 2–5 lots; we trade 1 lot |
| TP1 "locks profitability"; breakeven = "zero risk" | ⚠️ False for options, and with 1 lot nothing is locked |
| 1:2 or 1:3 reward-to-risk | ❓ No evidence; break-even win rate 33% at 1:2 |
| "A 50% loss makes recovery impossible" | ⚠️ Needs +100%; hard, not impossible |
| "Swing low" vs "low of the previous candle" | ⚠️ Inconsistent; spec uses the previous closed candle |
| Trail formula | ⚠️ Missing the never-loosen rule |
| "Trailing take profit" with ATR 14 × 2.0 "institutional" | ⚠️ It is a trailing stop; classic Chandelier is 22 × 3.0 |
| Candle trail and ATR trail on one position | ⚠️ No priority rule; use one |
| Close 100% at TP2, then "trail past TP2" | ⚠️ Contradiction |
| Trail buffers "2 points" (crude) and "1.5 points" (gas) | ⚠️ Scale-dependent; use ticks or ATR |
| "35–45 point" crude target capture | ❓ Unsupported |
| Time stop "30–45 minutes after entry" | ❓ Plausible; kept as variant T2 |
| ACY pullback strategy (50 EMA, RSI 40–50, Bollinger) | ❓ A different strategy with no evidence; variant P1 |
| "Institutional" framing; "overall edge" | ⚠️ Retail rule sets. The label is not evidence; no source gave a backtest |

## G. My own errors (corrected)

1. Said refinery utilization was in Table 1 (it is in Table 2) and Cushing only "probably" in Table 4 (now verified).
2. Ran the crude "9 Sep" event in pass 1; the WPSR was Thu 10 Sep at 12:00 ET. Corrected; earlier crude totals and the "5 of 6 continuation" reading were wrong.
3. Gas daily-test bug: filtered out all Henry Hub prices under $5. Fixed.
4. Guessed weekly gas misses were "a few Bcf". Wrong: measured over 98 weeks the median miss is 5.0 Bcf and the SD 9.4 Bcf (crude: median 3.0 mb, SD 4.8 mb).
5. Used 25-point (crude) and 3-point (gas) illustrative stops; measured medians are 43 and 2.2 (crude risk is about 5% of the account, not 3%).
6. Wrote "WPSR Wed 14 Oct". The release is Thu 15 Oct at 12:00 ET, the same day the crude options expire.
7. Quoted a 58% break-even win rate and a "continuation 5 of 6" reading from the old 60/40 scheme and the invalid pass-1 date. Both superseded (break-even is now `R / (R + A)` for a single exit; continuation is 55–64%).
