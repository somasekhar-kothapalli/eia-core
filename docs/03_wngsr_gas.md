# 03 WNGSR (Natural Gas): Report, Data, Consensus and Option Chain

**Catalyst:** EIA Weekly Natural Gas Storage Report. **Price driver:** NYMEX Henry Hub. **Traded:** MCX NATGASMINI (250 mmBtu) options. Rules are in `01_strategy_spec.md`.
**Last revised:** 7 Oct 2026. Tags: ✅ verified · 🔧 decided · ❓ open.

## 1. Report mechanics ✅

| Item | Value |
|---|---|
| Release | **Thursday** 10:30 AM ET (= 8:00 PM IST in daylight time, 9:00 PM IST in standard time). Exceptions 2026: Fri 13 Nov 10:30 ET and Wed 25 Nov 12:00 ET |
| Data period | Week ending the previous Friday (release Thu 1 Oct = week ending Fri 25 Sep). Next: Thu 8 Oct |
| Downloads at 10:30 ET | Summary text, CSV, JSON |
| Units and signs | **Bcf**. Injection positive, withdrawal negative. Injection season roughly Apr–Oct, withdrawal season roughly Nov–Mar. The signal rule works in both seasons |
| Main table | "Working gas in underground storage, Lower 48 states". Columns: stocks (current, prior week), **net change**, **implied flow**, year-ago stocks (% change), 5-year average 2021–25 (% change). Rows: East, Midwest, Mountain, Pacific, South Central (with Salt and Nonsalt) and the **Lower 48 total** |
| Second table | Sampling variability: coefficient of variation of stocks and **standard error of net change** by region |
| Not on the page | **No weather data** (heating/cooling degree days). Another reference says EIA's Natural Gas Storage Dashboard shows daily regional temperatures and deviation from normal; HDD/CDD not confirmed ❓ |

## 2. Reference print: week ending 25 Sep 2026 (released Thu 1 Oct) ✅

| Item | Value |
|---|---|
| Stocks 25 Sep / 18 Sep | 3,415 / 3,351 Bcf |
| Net change | **+64 Bcf** (3,415 − 3,351 ✅). Implied flow +64 (same this week) |
| Year ago | 3,553 Bcf, −3.9% (−138 Bcf) |
| 5-year average (2021–25) | 3,336 Bcf; stocks +2.4% above (+79 Bcf) |
| EIA standard error of net change | 0.7 Bcf. Coefficient of variation of stocks 0.4% |

| Region | Stocks | Net change | vs 5-yr avg |
|---|---|---|---|
| East | 840 | +25 | +4.6% |
| Midwest | 984 | +25 | +2.9% |
| Mountain | 248 | +4 | +6.4% |
| Pacific | 295 | +3 | +8.9% |
| South Central | 1,048 | +7 | −2.4% |
| of which Salt | 213 | **−4** | **−15.5%** |
| of which Nonsalt | 834 | +9 | +1.5% |

Regions sum to 3,415 and net changes to +64 ✅. Salt storage withdrew 4 Bcf while the total injected 64. Whether Salt has any price effect at 10:30 ET is untested ❓ (kept as a conflict flag only).

## 3. What is used from the report

| Item | Role |
|---|---|
| Net change, Lower 48 total | **The only trigger**, compared with consensus |
| Stocks vs 5-year average and vs year ago | Context only, not an intraday trigger ❓ |
| Implied flow | Check it equals net change; a gap hints at a revision or reclassification ❓ (EIA definition not on the page) |
| South Central Salt | Conflict flag ❓ |
| Standard error (0.7 Bcf on 25 Sep) | Noise reference |

- **Threshold X:** EIA's own sampling error averages about **2 Bcf** (Lower 48), 2.2–5.5 Bcf in 2016 weeks with withdrawals above 100 Bcf ✅. A surprise below about 2 Bcf is inside measurement noise: our 1 Oct miss (+1 Bcf) is noise. **Measured misses (Investing.com, 98 releases Nov 2024 to Oct 2026): SD 9.39 Bcf, median |miss| 5.0 Bcf, 90th percentile 13.6, largest 47; actuals exceeded consensus on average by +1.2 Bcf (54% of weeks).** The earlier guess of "a few Bcf" was wrong and the 13 Bcf summary was roughly right.
- From the literature: gas moves about **1.16% per 1 SD of surprise** (about 3.6 points at ₹306), much more than crude, and most of it within 5–7 minutes (`05_evidence.md`).

## 4. Consensus sources (chosen by the user; pages read 7 Oct 2026)

| Source | Week ending 25 Sep 2026 (released 1 Oct) |
|---|---|
| [Investing.com natural gas storage](https://in.investing.com/economic-calendar/natural-gas-storage-386) (**primary**) | Actual 64, forecast **63**, previous 53. History table of actual/forecast/previous |
| [Trading Economics natural gas stocks change](https://tradingeconomics.com/united-states/natural-gas-stocks-change) (cross-check) | Actual 64, previous 53, consensus **64** |

- Surprise vs Investing = 64 − 63 = **+1 Bcf** (bearish, tiny). vs Trading Economics = 0. The signs disagree, so the sign rule gives **no trade** for that week.
- A consensus equal to the actual looks overwritten after release ❓. Both sites list 14:30 GMT = 10:30 ET (daylight).
- Only one gas number needs a consensus (net change). History depth for a backtest: not checked; copy by hand, no scraping ❓.

## 5. NATGASMINI option chain (snapshot 7 Oct 2026, before the release; Fut 306.00, ATM 305, step 5, expiry 23 Oct 2026; Greeks as shown by the chart tool ❓)

Same method as the crude doc. `BE move` is for a 3-pt IV drop. Cost per lot = LTP × 250.

Calls:

| Strike | Delta | LTP | Vega% | Theta%/day | BE move | Volume | Cost per lot |
|---|---|---|---|---|---|---|---|
| 285 | 0.75 | 26.65 | 0.79% | 1.28% | 0.84 | 234 | ₹6,663 |
| **290** | 0.69 | 23.65 | 0.97% | 1.65% | 1.00 | 1,538 | ₹5,913 |
| **295** | 0.64 | 20.80 | 1.15% | 2.02% | 1.13 | 2,123 | ₹5,200 |
| 300 | 0.59 | 17.95 | 1.39% | 2.45% | 1.27 | 6,510 | ₹4,488 |
| 305 (ATM) | 0.53 | 15.65 | 1.66% | 2.94% | 1.47 | 7,018 | ₹3,913 |

Puts (volume column cut off at the screenshot edge, so volumes are minimums):

| Strike | Delta | LTP | Vega% | BE move | Volume (≥) | Cost per lot |
|---|---|---|---|---|---|---|
| 310 | −0.51 | 17.45 | 1.49% | 1.53 | 1,703 | ₹4,363 |
| **315** | −0.56 | 20.60 | 1.21% | 1.34 | 941 | ₹5,150 |
| **320** | −0.61 | 23.95 | 1.04% | 1.23 | 551 | ₹5,988 |
| 325 | −0.65 | 27.55 | 0.87% | 1.11 | 25 | ₹6,888 |

Findings:
- ✅ The mini chain **matches the standard NATURALGAS chain** (snapshot of the same time: unit premiums within about ₹0.3; IV 51–62% near the money; call volume 2,123–7,018 at strikes 295–305). Mini liquidity is not worse in this snapshot.
- ✅ **Delta 0.65–0.75 and extrinsic < 20% cannot both hold**: delta 0.74 had 23% extrinsic and 0.69 had 33% (standard chain). Under 20% needs delta ≥ 0.78.
- ✅ **IV about 58% ATM** one day before the release. The claim of 100–120% pre-report IV is not seen here ❓ (IV could still rise into Thursday).
- Put IV rises with strike (56.7% at 270, 60.5% at 320), so ITM puts cost more IV than ITM calls. Far puts (335, 340, 345) show stale last prints (IV 71–95%): ignore.
- Near-ATM wins on % return for a plausible 6-pt move (15.7% vs 13.5% for the 280 call); ITM wins on breakeven move and theta. The gas result depends on move size ❓; crude's did not.
- **Working zone: calls 290–295 (delta 0.64–0.69), puts 315–320 (delta −0.56 to −0.61).** Premium per lot ₹4,500–6,000 (9–12% of ₹50,000), which is the maximum loss.
- ⚠️ **Gas expiry:** these options expire **Fri 23 Oct**. The WNGSR of **Thu 22 Oct** is one day before expiry; use the next-month chain then (spec §7).

## 6. Sources

| Source | Status | Use |
|---|---|---|
| [EIA WNGSR](https://ir.eia.gov/ngs/ngs.html) and [schedule](https://ir.eia.gov/ngs/schedule.html) | ✅ read | Primary: every table value above; 2026 exceptions |
| [EIA Today in Energy: sampling variability](https://www.eia.gov/todayinenergy/detail.php?id=29712) | ✅ read | Standard error about 2 Bcf |
| [energyby5.com](https://www.energyby5.com/blogs/natural-gas-storage-how-to-read-the-tea-leaves) | ✅ read | Thursday 10:30 ET; analysts focus on projected storage. Capacity "about 4,250 Bcf" ❓ |
| [met.com](https://met.com/en/media/energy-insight/natural-gas-report/) | ✅ read | Thursday 10:30 ET; storage dashboard shows regional temperatures |
| [corporatefinanceinstitute.com](https://corporatefinanceinstitute.com/resources/valuation/natural-gas-storage-indicator-eia-report/) | ✅ read | Generic; writes "EST" for a time that is EDT in summer |
| [kilowattlogic.com](https://kilowattlogic.com/natural-gas/eia-weekly-storage-report) | ✅ read | Its 25 Sep numbers match EIA ✅ |
| [materials-risk.com](https://materials-risk.com/natural-gas-storage-how-to-read-eia-report) | ✅ read | Methodology only; asserts the 5-year comparison is more informative than the headline ❓ |
| [marketplace.reitsport.ch](https://marketplace.reitsport.ch/sport-reits/natural-gas-storage-report-live-updates-and-analysis-1767647855) | ❌ not read | Connection refused; a sports-REIT marketplace, not an energy source: dropped |

None gives consensus handling, typical surprise size, price move per Bcf, option behavior or a backtest. See `08_corrections_log.md`.
