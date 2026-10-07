# EIA WNGSR → Henry Hub Natural Gas: MCX Execution Strategy

File: `eia_wngsr_mcx_natgas.md`. Companion to `eia_wpsr_mcx_crude.md`. Entry, exit, trailing, order and risk rules are the same for both assets and live in `eia_common_execution.md`.

**Scope:** WNGSR is the catalyst. NYMEX Henry Hub (NG) is the price driver. Execution is on the **MCX Natural Gas current-month future and its options** (INR).

**Tags:** ✅ verified (EIA pages, or exact arithmetic) · ⚠️ corrected from source · 🔧 rule added or tightened in review · ❓ unverified, needs backtest or contract-spec check

---

## 1. Report Mechanics

| Item | Value | Tag |
|------|-------|-----|
| Report | Weekly Natural Gas Storage Report (WNGSR) | ✅ |
| Release | **Thursday** 10:30 AM ET (the crude report is Wednesday). Holiday weeks shift the day/time. Check the EIA schedule weekly | ✅ |
| Data period | Week ending the previous Friday (release Thu 1 Oct 2026 = week ending Fri 25 Sep) | ✅ |
| IST during US daylight time (EDT) | **8:00 PM IST** | ✅ |
| IST during US standard time (EST) | **9:00 PM IST** (releases from Thu 5 Nov 2026) | ✅ |
| Next release | Thu 8 Oct 2026 (8:00 PM IST) | ✅ |
| Units | **Bcf** (billion cubic feet) | ✅ |
| Layout | 5 regions (East, Midwest, Mountain, Pacific, South Central). Columns: current stocks, previous week, **net change**, **implied flow**, year-ago and five-year-average comparisons | ✅ |

Rule 🔧: derive the window start as **10:30 ET converted to IST**. Never hardcode 8:00 PM.

**Reference print: week ending 25 Sep 2026** ✅ (ir.eia.gov/ngs/ngs.html, Lower 48 total)

| Item | Value |
|---|---|
| Stocks 25 Sep / 18 Sep | 3,415 / 3,351 Bcf |
| Net change | **+64 Bcf** (3,415 − 3,351 ✅) |
| Implied flow | +64 Bcf (equals net change this week) |
| Year ago (25 Sep 2025) | 3,553 Bcf, −3.9% |
| 5-year average (2021–25) | 3,336 Bcf, stocks +2.4% above (+79 Bcf) |
| Standard error of net change | 0.7 Bcf |
| Coefficient of variation of stocks | 0.4% |

Regional rows, same print ✅ (stocks Bcf; regions sum to 3,415 and net changes to +64):

| Region | Stocks | Net change | vs 5-yr avg |
|---|---|---|---|
| East | 840 | +25 | +4.6% |
| Midwest | 984 | +25 | +2.9% |
| Mountain | 248 | +4 | +6.4% |
| Pacific | 295 | +3 | +8.9% |
| South Central | 1,048 | +7 | −2.4% |
| of which Salt | 213 | **−4** | **−15.5%** |
| of which Nonsalt | 834 | +9 | +1.5% |

- Salt storage withdrew 4 Bcf while the total injected 64 Bcf. Salt is 15.5% below its 5-year average. ❓ Whether this subcategory has any price effect at 10:30 ET is untested. Kept as a conflict flag.

- Bias (consensus from Investing.com, see §2.4): surprise = 64 − 63 = **+1 Bcf**, slightly bearish and tiny. ✅ arithmetic. With Trading Economics' consensus (64) the surprise is 0.

**Season** ✅: injection season (stocks rise, net change positive) runs roughly Apr–Oct. Withdrawal season (net change negative) runs roughly Nov–Mar. The signal rule below works in both, as long as the sign convention is kept (injection +, withdrawal −).

## 2. Data Map and Signal Definition

**2.1 Where to read** ✅ (ir.eia.gov/ngs/ngs.html, 25 Sep 2026 release)
- Main table: **"Working gas in underground storage, Lower 48 states"**. Columns: stocks (current and prior week), **net change**, **implied flow**, year-ago stocks with % change, 5-year average (2021–25) with % change.
- Rows: East, Midwest, Mountain, Pacific, South Central (with Salt and Nonsalt) and the **Lower 48 total**.
- Download formats at 10:30 ET: **Summary text, CSV, JSON** ✅.
- Second table: sampling variability (coefficient of variation of stocks, standard error of net change, by region) ✅.
- ⚠️ **No weather data (heating / cooling degree days) is on this page.**

**2.2 What each item is used for**

| Item | Role | Tag |
|---|---|---|
| Net change, Lower 48 total (Bcf) | **The only trigger.** Compared with consensus | ✅ |
| Stocks vs 5-year average (Bcf and %) | Context only (structural tone). Not an intraday trigger | ❓ |
| Stocks vs year ago | Context only | ❓ |
| Implied flow | Check it equals net change. A gap hints at a revision or reclassification | ❓ (EIA's exact definition not on the page) |
| South Central Salt / Nonsalt | Conflict flag only | ❓ |
| Standard error of net change (0.7 Bcf on 25 Sep) | Noise reference. The measurement is tight; the miss is mostly forecast error | ✅ |

**2.3 Signal rule**
- `Surprise = actual net change − consensus` (Bcf). Sign convention: injection +, withdrawal −.
- **Negative surprise = bullish** (smaller injection, or larger withdrawal). **Positive surprise = bearish.** ✅ Works in both seasons.
- ✅ All four rows of the source's seasonal matrix have the correct direction (−120 vs −90 bullish; −60 vs −90 bearish; +40 vs +65 bullish; +85 vs +65 bearish).
- ⚠️ The source calls the formula "Gas Deviation Alpha". It is the **surprise**, not alpha. Formula ✅.
- 🔧 Consensus: use **one** source every week and record it ❓ (Reuters, Bloomberg, WSJ poll, etc.). ❓ Whether the distance outside the poll range adds information.
- 🔧 Threshold: `|surprise| ≥ X`. X is ❓ from backtest, preferably in **SD units** (see common file §16 and the SD note there). The source labels moves of 20–30 Bcf "strong" but gives no threshold.
- ✅ **Floor for X:** EIA's own sampling standard error for net change averages about **2 Bcf** (Lower 48), rising to 2.2–5.5 Bcf in weeks with withdrawals above 100 Bcf (EIA Today in Energy). A surprise below about 2 Bcf is inside the measurement noise. Our 1 Oct miss (+1 Bcf; 0.7 Bcf standard error that week) is noise.
- ❓ **Typical miss size is unknown.** One search summary says the average analyst error is about 13 Bcf per week (unverified). Trade-press examples show misses of 8–13 Bcf. My earlier "a few Bcf" was a guess and is withdrawn. Measure it from our own history.
- ✅ Research (common file §16): the gas response per 1 SD of surprise is about 1.16% (about 3.6 points at ₹306), larger than crude's 0.27%. Most of the move occurs in the first 5–7 minutes (✅ Linn et al., 2003–2017 NYMEX).
- 🔧 Conflict rule: data bias and breakout direction disagree = **no trade**. The source's matrix ends in "buy call / buy put" from the data alone. ⚠️ That skips the price-breakout confirmation (common file §6).
- ⚠️ The matrix fixes "delta 0.70". Pick the strike by chain method (common file §4).

**2.4 Consensus sources (chosen by the user; pages read 7 Oct 2026)**

| Source | Latest (week ending 25 Sep 2026, released 1 Oct) |
|---|---|
| [Investing.com natural gas storage](https://in.investing.com/economic-calendar/natural-gas-storage-386) | Actual 64, forecast 63, previous 53 (Bcf). Shows a history table of actual / forecast / previous |
| [Trading Economics natural gas stocks change](https://tradingeconomics.com/united-states/natural-gas-stocks-change) | Actual 64, previous 53, consensus **64** |

- ✅ Both agree on the actual (64) and previous (53). Both list release time 14:30 GMT = 10:30 ET (EDT) = 8:00 PM IST; 15:30 GMT in winter.
- ⚠️ The consensus differs: 63 vs 64. A consensus equal to the actual looks suspicious, as if overwritten after release ❓. 🔧 Primary source = **Investing.com** (forecast kept in the history table), confirmed by the user 7 Oct 2026. Trading Economics is the cross-check. Capture template: `eia_snapshot_log.md`.
- Only this one number is needed (net change, Bcf). No other gas data point needs a consensus.
- ❓ History depth for a 50-week backtest: not checked. Do not scrape; check whether older rows load, or copy by hand.
- First data point on miss size: +1 Bcf, inside EIA's sampling noise. One week is not evidence ❓.

## 3. Level Construction

Moved to `eia_common_execution.md` §3. Same opening range and midpoint; floor pivots by default. The Camarilla set from the gas source is kept there as a **test variant** (§3.4).

## 4. Instrument Selection (options)

| Source claim | Verdict |
|---|---|
| Pre-report IV can exceed 100–120%, collapsing to 60–70% within minutes | ❓ Unverified numbers. Measure from MCX natgas chain history. IV crush itself is real ✅ |
| Deep ITM, delta 0.65–0.75, "2–3 intervals ITM" | ⚠️ Delta is the right selector. Interval counts depend on strike gap, IV and days to expiry. **Select by delta from the live chain.** |
| Extrinsic value < 20% of premium **and** delta 0.65–0.75 | ⚠️ **Inconsistent.** On your crude chain a 0.72-delta call had ≈ 25% extrinsic (8250 call: LTP 524.7, intrinsic ≈ 393). Extrinsic < 20% needs a deeper strike, usually delta ≥ 0.8. Natgas IV is higher, so the gap is likely larger ❓. **Pick one criterion.** |
| Delta 0.70 "behaves like a synthetic future" | ⚠️ **Wrong.** A synthetic future has delta ≈ 1. At 0.70 you capture ~70% of the move. |
| ITM "shields" from vega | ⚠️ Overstated (same as #11 in the crude file). Vega is lower but not zero. The real gain is a smaller **percentage** loss on a larger premium. |
| Use limit orders at mid-market | Parked (execution is out of scope for now) |
| Gas options have wider spreads and lower liquidity than crude | ❓ Plausible. Check bid-ask and volume on the live chain. |

**Live chain snapshot analysis** (MCX NATURALGAS: Fut 305.70, ATM 305, step 5, expiry 23 Oct 2026, so 16 days from 7 Oct; Greeks as shown by the chart tool; screenshot taken 7 Oct 2026, **before** the WPSR release and about a day before the WNGSR)

Method as in the crude file §6. `Vega%` = vega ÷ LTP. `BE move` = futures points needed to offset a 3-pt IV drop = vega × 3 ÷ delta. `Net` = delta × move − vega × 3 for an **illustrative +6 pt move** (≈ 2% of 305.7) ❓ and IV −3 pts ❓. Cost per lot = LTP × 1,250.

Calls:

| Strike | Delta | LTP | Extrinsic % | Vega% | Theta% /day | BE move (pts) | Net ₹ (% of premium) | Volume | Cost per lot |
|---|---|---|---|---|---|---|---|---|---|
| 280 | 0.78 | 30.35 | 15% | 0.63% | 1.05% | 0.73 | 4.11 (13.5%) | 166 | ₹37,938 |
| 285 | 0.74 | 26.80 | 23% | 0.78% | 1.34% | 0.85 | 3.81 (14.2%) | 258 | ₹33,500 |
| **290** | 0.69 | 23.40 | 33% | 0.98% | 1.67% | 1.00 | 3.45 (14.7%) | 1,035 | ₹29,250 |
| **295** | 0.64 | 20.35 | 47% | 1.18% | 2.01% | 1.13 | 3.12 (15.3%) | 2,154 | ₹25,438 |
| 300 | 0.58 | 17.70 | 68% | 1.41% | 2.49% | 1.29 | 2.73 (15.4%) | 6,355 | ₹22,125 |
| 305 (ATM) | 0.53 | 15.25 | 95% | 1.70% | 2.95% | 1.47 | 2.40 (15.7%) | 4,788 | ₹19,063 |

Puts (volume column cut off at the screenshot edge, so volumes are minimums):

| Strike | Delta | LTP | Extrinsic % | Vega% | BE move (pts) | Net ₹ (% of premium) | Volume (≥) | Cost per lot |
|---|---|---|---|---|---|---|---|---|
| 330 | −0.70 | 31.15 | 22% | 0.71% | 0.94 | 3.54 (11.4%) | 44 | ₹38,938 |
| 325 | −0.65 | 27.85 | 31% | 0.86% | 1.11 | 3.18 (11.4%) | 17 | ₹34,813 |
| **320** | −0.61 | 24.10 | 41% | 1.04% | 1.23 | 2.91 (12.1%) | 271 | ₹30,125 |
| **315** | −0.57 | 20.70 | 55% | 1.21% | 1.32 | 2.67 (12.9%) | 315 | ₹25,875 |
| 310 | −0.52 | 17.50 | 75% | 1.49% | 1.50 | 2.34 (13.4%) | 169 | ₹21,875 |
| 305 (ATM) | −0.47 | 14.70 | 100% | 1.77% | 1.66 | 2.04 (13.9%) | 291 | ₹18,375 |

Findings:
- ✅ **Strike interval is ₹5** (from the chain header). Option expiry 23 Oct 2026. Futures price scale ≈ ₹305, so 1 point = 0.33% of the future.
- ✅ **The source's "delta 0.65–0.75 and extrinsic < 20%" cannot both hold.** Call delta 0.74 has 23% extrinsic; delta 0.69 has 33%. Under 20% extrinsic needs delta ≥ 0.78 (280 call: 15%). Put 330 (delta −0.70) is 22%. Pick one criterion.
- ✅ **IV on this chain is 51–63%**, ATM about 58%. The source's "100–120% before the report" is not what this snapshot shows ❓ (taken about a day before the WNGSR release, so IV could still rise into Thursday ❓). The source's "collapse to 60–70%" would be above the level seen here.
- ⚠️ **Skew:** put IV rises with strike (56.7% at 270 to 60.5% at 320), so ITM puts cost more IV than ITM calls (calls ITM 51–57%). ❓ Whether this persists.
- ⚠️ **Stale prints:** the 335 and 345 puts show IV 80.1% and 78.2% with LTP equal to the 340 put (39.30). Ignore them. Do not rely on any strike with a stale last price.
- On gas, IV drag is small against a plausible move (vega × 3 = 0.78 at ATM vs delta × 6 = 3.2). A larger move favors near-ATM on **percentage** return (15.7% vs 13.5%). ITM wins on **breakeven move**, **theta**, and absolute rupees. This is the opposite of crude, where ITM won on both. The result depends on the assumed move size ❓.
- ✅ Gamma adds ≈ ₹0.2 on a 6-pt move, about 5% of the gain. Small, not zero.
- **Liquidity:** call volume is concentrated at 295–310 (2,154–6,355). Calls at 285 or deeper have under 300 contracts. Put volumes are low everywhere in the ITM range. Bid-ask is not shown. ❓ Check it live.
- 🔧 Working rule for this chain: **calls ≈ 290–295 (delta 0.64–0.69), puts ≈ 315–320 (delta −0.57 to −0.61)**, re-picked each Thursday from the live chain by the same table. Skip any strike with a wide spread or stale price.
- 🔧 Risk per lot (price part, 3-pt stop): 290 call 0.69 × 3 × 1,250 = ₹2,588; 295 call ₹2,400; 315 put ₹2,138; 320 put ₹2,288. At a 1% cap that needs about ₹2.1–2.6 lakh equity. Maximum loss = premium: ₹25,438 for the 295 call.

**NATGASMINI chain snapshot (the contract we will trade)** (Fut 306.00, ATM 305, step 5, expiry 23 Oct 2026, taken 7 Oct 2026 before the release; same method and assumptions as above)

Calls:

| Strike | Delta | LTP | Vega% | Theta% /day | BE move (pts) | Volume | Cost per lot (×250) |
|---|---|---|---|---|---|---|---|
| 285 | 0.75 | 26.65 | 0.79% | 1.28% | 0.84 | 234 | ₹6,663 |
| **290** | 0.69 | 23.65 | 0.97% | 1.65% | 1.00 | 1,538 | ₹5,913 |
| **295** | 0.64 | 20.80 | 1.15% | 2.02% | 1.13 | 2,123 | ₹5,200 |
| 300 | 0.59 | 17.95 | 1.39% | 2.45% | 1.27 | 6,510 | ₹4,488 |
| 305 (ATM) | 0.53 | 15.65 | 1.66% | 2.94% | 1.47 | 7,018 | ₹3,913 |

Puts (volume column cut off, so volumes are minimums):

| Strike | Delta | LTP | Vega% | BE move (pts) | Volume (≥) | Cost per lot (×250) |
|---|---|---|---|---|---|---|
| 310 | −0.51 | 17.45 | 1.49% | 1.53 | 1,703 | ₹4,363 |
| **315** | −0.56 | 20.60 | 1.21% | 1.34 | 941 | ₹5,150 |
| **320** | −0.61 | 23.95 | 1.04% | 1.23 | 551 | ₹5,988 |
| 325 | −0.65 | 27.55 | 0.87% | 1.11 | 25 | ₹6,888 |

- ✅ **The mini chain looks like the standard chain**: same expiry (23 Oct), same ₹5 step, unit premiums within about ₹0.3 (the future is 306.00 vs 305.70), Greeks and IV (51–62% near the money) nearly identical.
- ✅ **Mini liquidity is not worse here**: calls 295–305 show 2,123–7,018 contracts, similar to the standard chain. Mini put volumes (941 at 315, 551 at 320, cut off) look better than the standard chain's.
- ⚠️ Stale prints again at the far puts (335: IV 71.6, 340: 73.7, 345: 94.9). Ignore them.
- ✅ Same working zone: **calls 290–295, puts 315–320**.
- 🔧 Premium per lot is ₹5,000–6,000 (10–12% of a ₹50,000 account). Risk at a 3-pt stop is ₹420–520, about 0.8–1.0% of the account (common file §11).

- 🔧 Use the **same chain method as the crude file §6**: compare candidates by **vega ÷ premium**, **breakeven move**, **bid-ask spread** and volume. Paste a MCX NATURALGAS chain screenshot to do this with real numbers.
- ✅ Contract specs are in the common file §1: lot 1,250 mmBtu (mini 250), futures tick ₹0.10, strike step ₹5, option tick ₹0.05, option expiry two business days before futures expiry (gas options 23 Oct 2026). Official MCX page not yet checked ❓.

## 5. Execution Rules

Identical to crude. See `eia_common_execution.md` §6–§12 (entry, stop, targets, breakeven, trailing, time stop, order mechanics). Gas-specific notes only:
- Gas source used a 3-min chart and Camarilla R3/R4 targets. Both are **test variants** of the common rules.
- Gas source contradictions (touch-stop despite "stop-hunt wicks", TP2 then trail, 1.5-point buffer, no time stop) are resolved in the common file.
- Mid-price limit entries may not fill in a fast gas move: time-limit rule is in the common file §6.

## 6. Risk Management

**Contract: NATGASMINI (250 mmBtu). Account: ₹50,000. Phase 1** (no %-cap filter; see `eia_common_execution.md` §11). 1 lot, 1 trade per report.
- ₹250 per 1-pt move of the future per lot. Premium per lot ₹4,500–6,000 (9–12% of the account) = maximum loss.
- Risk at a 3-pt stop (illustrative ❓): ₹420–520, about 0.8–1.0% of the account. A wider stop raises it in proportion. It is recorded, not filtered.
- Phase 2: a 2% cap fits at about ₹21,000–26,000 and a 1% cap at about ₹42,000–52,000 (3-pt stop). This contract is already near the 1% level.

## 7. Corrections Log

| # | Source claim | Verdict |
|---|---|---|
| 1 | 8:00 PM IST release time | ⚠️ Only during US daylight time. 9:00 PM IST from 5 Nov 2026. |
| 2 | Surprise = net change below forecast is bullish | ✅ |
| 3 | No consensus source or threshold given | ⚠️ Added. |
| 4 | Camarilla R3/R4/S3/S4 formulas | ✅ |
| 5 | Camarilla "P" level | ⚠️ Not part of Camarilla. |
| 6 | Crude = floor pivots, gas = Camarilla | ❓ No evidence. |
| 7 | R3 as profit target | ⚠️ R3/S3 are normally reversal levels. Design choice, needs backtest. |
| 8 | IV 100–120% → 60–70% | ❓ Unverified numbers. |
| 9 | Delta 0.65–0.75 **and** extrinsic < 20% | ⚠️ Inconsistent. Pick one. |
| 10 | Delta 0.70 = synthetic future | ⚠️ Wrong. |
| 11 | ITM shields from vega | ⚠️ Overstated. |
| 12 | Mid-market limit orders | Parked (execution is out of scope for now) |
| 13 | 15-min macro chart | ⚠️ Redundant (five 3-min candles). |
| 14 | Midpoint stop on touch despite "stop-hunt wicks" | ⚠️ Contradiction. |
| 15 | "Body closes outside" vs "closes above" | ⚠️ Inconsistent. |
| 16 | Close 100% at TP2, then trail past TP2 | ⚠️ Contradiction. |
| 17 | Trail buffer "1.5 points" | ⚠️ Scale-dependent. Use ticks/ATR. |
| 18 | "Zero risk" after breakeven | ⚠️ False for options. |
| 19 | No time stop | ⚠️ Added (proposed 90 min). |
| 20 | "Institutional" framing | ⚠️ A retail breakout rule set. Not evidence of edge. |
| 21 | Overall edge | ❓ Needs backtest. |
| 22 | Read table "Working Gas in Underground Storage, Lower 48 States" | ✅ (page title: "Working gas in underground storage, Lower 48 states") |
| 23 | Data via Summary text, CSV, JSON | ✅ |
| 24 | Bullish = larger withdrawal / smaller injection than forecast | ✅ |
| 25 | Seasonal matrix directions (4 rows) | ✅ |
| 26 | Matrix magnitudes 20–30 Bcf as "strong" | ❓ No threshold. Typical miss size unknown (one unverified source says ~13 Bcf average analyst error). Floor: EIA sampling error ≈ 2 Bcf. |
| 27 | Matrix gives "buy call/put" from data alone with delta 0.70 | ⚠️ Missing breakout confirmation and chain-based strike pick. |
| 28 | "Gas Deviation Alpha" | ⚠️ Misnamed. It is the surprise. |
| 29 | "Implied Weather Delta" as a core data point | ⚠️ No such item. "Implied flow" is a different column. Weather is not on the WNGSR page. |
| 30 | HDD/CDD from an "adjacent EIA Storage Dashboard" | ❓ Partly supported. One reference says the EIA Natural Gas Storage Dashboard has daily regional average temperatures and deviation from normal. HDD/CDD not confirmed. Not on the WNGSR page. Realized data is backward-looking. |
| 31 | "4 core data points" | ⚠️ Only net change is a trigger. 5-year and year-ago comparisons are context. Consensus is missing from the list. |
| 32 | Ignore regional data, "zero immediate impact" | ❓ Opinion. Kept as a conflict flag. |
| 33 | Skip data "to protect execution speed" | ⚠️ Moot. Entry waits for the 15-min range, so reading time is not binding. |
| 34 | Ignore base gas and peak capacity | ✅ Not in the main table; no intraday use. |
| 35 | Cited sources | ⚠️ Includes unrelated domains. Use EIA primary pages. |
| 36 | "3-minute execution window" | ⚠️ Common default is 5-min. 3-min is a test variant. |
| 37 | Delta 0.65–0.75 with extrinsic < 20% | ✅ Inconsistent. Confirmed on the live gas chain (delta 0.74 = 23% extrinsic). |
| 38 | IV 100–120% before the report | ❓ Not seen about a day before the release: chain shows 51–63%. Re-check at T − 5 on Thursday. |
| 39 | "Deep ITM" is best for gas options | ⚠️ Depends on move size. On this chain near-ATM wins on % return; ITM wins on breakeven and theta. |

## 8. Open Questions / To Validate

- A second **NATGASMINI** chain snapshot (before and after a release) to measure the real IV drop; bid-ask spreads for the chosen strikes; a Thursday T − 5 and T + 15 pair (this snapshot was taken ~1 day before the release).
- Consensus source and timing; surprise threshold X (Bcf). Typical miss size and its SD from history.
- EIA definition of implied flow and how reclassifications appear on the page.
- Where to get HDD/CDD or weather forecasts, and whether they add edge at 10:30 ET.
- Official MCX confirmation of the natgas specs (common file §1).
- Backtest ≥ 50 Thursdays. No MCX history: proxy = NYMEX NG 5/3-min around the release, then forward-test small. ❓ The proxy ignores USD/INR and MCX spreads.
- Test: 3-min vs 5-min; touch vs close stop; TP design A/B/C; trail buffer; time stop; Camarilla vs classic pivots.

## 9. References (gas)

Checked 6 Oct 2026. Primary source first.

| Source | Status | What it gives us |
|---|---|---|
| [EIA WNGSR (ir.eia.gov/ngs/ngs.html)](https://ir.eia.gov/ngs/ngs.html) | ✅ read | All table values above. Use this public URL. |
| [energyby5.com: how to read the tea leaves](https://www.energyby5.com/blogs/natural-gas-storage-how-to-read-the-tea-leaves) | ✅ read | Thursday 10:30 ET ✅. Analysts focus on where storage was **projected** to be, not the headline. Capacity "about 4,250 Bcf" and loose spring/summer ranges: ❓ unverified. |
| [met.com: natural gas report](https://met.com/en/media/energy-insight/natural-gas-report/) | ✅ read | Thursday 10:30 ET ✅. Older example (2,097 Bcf, +73). Says the EIA Natural Gas Storage Dashboard shows daily regional temperatures and deviation from normal. |
| [corporatefinanceinstitute.com: storage indicator](https://corporatefinanceinstitute.com/resources/valuation/natural-gas-storage-indicator-eia-report/) | ✅ read | Generic. Says "10:30 a.m. EST" ⚠️ (EDT in summer). Working gas = total − base gas ✅. Direction logic matches ours ✅. |
| [kilowattlogic.com: EIA weekly storage report](https://kilowattlogic.com/natural-gas/eia-weekly-storage-report) | ✅ read | Its 25 Sep 2026 numbers match EIA ✅ (total, net change, vs 5-yr, year-ago, Salt 213 Bcf −15.5%). A forecast "revised down 119 Bcf" has no stated source ❓. |
| [materials-risk.com: how to read the EIA report](https://materials-risk.com/natural-gas-storage-how-to-read-eia-report) | ✅ read | Methodology only. No timing, no numbers. Asserts that comparison to the 5-year average is "more informative than the headline" ❓. For our intraday trigger, the miss vs consensus is what we test. |
| [marketplace.reitsport.ch](https://marketplace.reitsport.ch/sport-reits/natural-gas-storage-report-live-updates-and-analysis-1767647855) | ❌ not read | Connection refused. Domain is a sports-REIT marketplace, not an energy source. Drop it. |

**What none of them provide:** the consensus source, typical surprise size, price move per Bcf of surprise, option behavior, or any backtest. The surprise thresholds, move sizes and option rules therefore remain ❓ for gas.

## Change Log
- 2026-10-06: file created from the first WNGSR research batch; report facts verified on ir.eia.gov (release 1 Oct 2026, 3,415 Bcf, net +64).
- 2026-10-06: sections 3, 5, 6 now point to eia_common_execution.md. Lot sizes added (1,250 / 250).
- 2026-10-06: data and signal batch evaluated; verified main table, columns, formats, Lower 48 values and standard error on ir.eia.gov; corrections #22-36 added.
- 2026-10-06: added regional table (sums verified) and gas references; #30 updated (dashboard has regional temperatures); reitsport source dropped.
- 2026-10-06: full links added to the references table.
- 2026-10-07: consensus sources added (§2.4); 1 Oct surprise computed (+1 Bcf).
- 2026-10-07: NATURALGAS chain analysed (strike table, extrinsic vs delta, IV level, liquidity); corrections #37-39.
- 2026-10-07: chain snapshot timing recorded (about a day before WNGSR).
- 2026-10-07: broker execution parked.
- 2026-10-07: MCX specs resolved via common file §1; next WNGSR (22 Oct) falls one day before the 23 Oct options expiry.
- 2026-10-07: contract chosen: NATGASMINI. Risk section rewritten; a NATGASMINI chain is now needed.
- 2026-10-07: NATGASMINI chain analysed (matches the standard chain). Account ₹50,000: risk section rewritten.
- 2026-10-07: risk section moved to Phase 1 (no cap filter at ₹50,000).
- 2026-10-07: gas contract final: NATGASMINI, Thursdays only, one trade per report.
- 2026-10-07: independent research applied: threshold floor ≈ 2 Bcf (EIA sampling error), SD units, response per SD, earlier 'few Bcf' guess withdrawn.
