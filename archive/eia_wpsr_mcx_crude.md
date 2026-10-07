# EIA WPSR → WTI Crude: MCX Execution Strategy

File: `eia_wpsr_mcx_crude.md`. Shared entry/exit/risk rules are in `eia_common_execution.md`.

**Scope:** WPSR is the catalyst. NYMEX WTI (CL) is the price driver. Execution is on the **MCX Crude Oil current-month future and its options** (INR).

**Tags:** ✅ verified (EIA pages/tables, or exact arithmetic) · ⚠️ corrected from source · 🔧 rule added or tightened in review (not in original research) · ❓ unverified, needs backtest or contract-spec check

---

## 1. Report Mechanics

| Item | Value | Tag |
|------|-------|-----|
| Report | Weekly Petroleum Status Report (WPSR) | ✅ |
| Release | Wednesday 10:30 AM ET. Holiday weeks can shift the day and/or time. Check the EIA schedule weekly | ✅ |
| Data period | Week ending the previous Friday (e.g. release Wed 30 Sep 2026 = week ending Fri 25 Sep) | ✅ |
| IST during US daylight time (EDT) | **8:00 PM IST** | ✅ |
| IST during US standard time (EST) | **9:00 PM IST** | ⚠️ source assumed 8:00 PM year-round |
| 2026 EDT → EST switch | Sun 1 Nov 2026. Releases from Wed 4 Nov are at 9:00 PM IST | ✅ |
| Next release | Wed 7 Oct 2026 (EDT, so 8:00 PM IST) | ✅ |

Rule 🔧: derive the window start as **10:30 ET converted to IST**. Never hardcode 8:00 PM.

**Release formats (from the EIA report page)** ✅
- At **10:30 a.m. ET:** Summary TXT, all CSV/XLS tables, and the combined "Data Overview" PDF (Tables 1 + 9).
- At **1:00 p.m. ET:** most per-table PDFs. Do not wait for them. Read the headline box, the Summary TXT or the CSV/XLS.

**Units and signs** ✅
- Landing-page headline box: **thousand barrels** (e.g. 427,320). Tables 1, 2 and 4 show stocks in **million barrels, 1 decimal** (e.g. 427.3). Rounding in the tables hides small moves, so use the thousand-barrel figure for trading.
- Flows (production, inputs, products supplied) are in **thousand barrels per day**.
- Sign: **positive = build, negative = draw.** Example: commercial crude 427,320 vs 426,398 = **+922 kb** (a 0.922 mb build). PADD changes sum to the same 922.
- Headline "Commercial Crude Oil Stocks" **excludes SPR** ✅.

## 2. Data Map: Which Table Holds What

Verified by opening the 25 Sep 2026 tables on eia.gov. ✅

| Table | Name | Use it for |
|-------|------|-----------|
| **1** | U.S. Petroleum Balance Sheet | Stocks (crude total, commercial, SPR, gasoline, jet, distillate, resid, propane); crude supply lines (production, imports, exports, net imports); crude input to refineries; **products supplied** (implied demand: total, gasoline, jet, distillate); net imports |
| **2** | U.S. Inputs and Production by PAD District | **Refinery utilization %**, gross inputs, operable capacity, crude inputs by PADD |
| **4** | Stocks of Crude Oil by PAD District, and Stocks of Petroleum Products | **Cushing, OK stocks** and crude by PADD |
| **9** | U.S. and PAD District Weekly Estimates | Combined view of the above (includes Cushing and utilization) |
| 3, 5, 5A, 6, 7, 8 | Refiner net production; gasoline stocks; distillate/jet/resid/propane stocks; imports/exports; crude imports by country | Detail only |

**Corrections to the source:**
- ⚠️ **Cushing is NOT in Table 1.** It is in Table 4 (and Table 9). Verified: no "Cushing" row in Table 1.
- ⚠️ **Refinery utilization is NOT in Table 1.** It is in Table 2 (and Table 9). Table 1 only has "Crude Oil Input to Refineries" in kb/d.
- ⚠️ The "week-on-week change" label belongs to the landing-page box. Table 1 labels the column **"Difference"** (week ago and year ago), plus "Percent Change".
- ⚠️ "Open Table 1 for all 4 pillars" is wrong. Crude and gasoline stocks and crude input are in Table 1. **Cushing = Table 4, utilization % = Table 2.** The fastest single source is the Data Overview PDF (Tables 1 + 9) or the Table 9 CSV.
- ⚠️ "4 pillars" is incomplete. Also watch **distillate stocks, products supplied (implied demand), crude imports/exports, production**.
- ⚠️ "PADD 2 Stocks at Cushing" is not an EIA label. The row is **"Cushing"** under Midwest (PADD 2).

## 3. Reference Print: Week Ending 25 Sep 2026 (released Wed 30 Sep 2026)

| Metric | Current | Prior | Change | Source |
|--------|---------|-------|--------|--------|
| Commercial crude (kb) | 427,320 | 426,398 | **+922** (build) | headline box ✅ |
| Total crude incl. SPR (mb) | 711.1 | 711.0 | +0.1 | Table 1 ✅ |
| SPR (mb) | 283.8 | 284.6 | −0.8 | Table 1 ✅ |
| Cushing (mb) | 24.3 | 23.7 | ≈ +0.6 | Table 4 (calculated from rounded values) ✅ |
| Refinery utilization | ≈ 92.5% | ≈ 94.0% | ≈ −1.5 pt | Table 2 (gross inputs ÷ operable capacity: 16,670 ÷ 18,027) ✅ |
| Crude input to refineries (kb/d) | 16,257 | 16,811 | −554 | Table 1 ✅ |

- Bias (consensus from Investing.com, see §4.1): surprise = +0.922 − (−0.700) = **+1.622 mb**, a larger build than the expected draw, so **bearish** ✅ arithmetic. With Trading Economics' consensus (−0.3) it is +1.222 mb, also bearish.
- The PDF text extraction was messy; figures above were cross-checked with arithmetic. Re-check against the CSV before reusing them.

## 4. Signal Definition

- **Bullish for crude:** crude stocks draw larger than consensus, or build smaller than consensus.
- **Bearish for crude:** crude stocks build larger than consensus, or draw smaller than consensus. ✅
- ⚠️ "Draw = bullish" is wrong on its own. Surprise = **actual − consensus** (and compare with the API figure released Tuesday).
- ⚠️ "Positive surprise" in the source is ambiguous. Use **bullish surprise** / **bearish surprise**.
- 🔧 Primary metric: commercial crude stock change (kb) vs consensus.
- 🔧 Threshold: define "significant" as `|actual − consensus| ≥ X kb`. X = ❓ from backtest.
- 🔧 Secondary metrics (conflict flags only): Cushing, gasoline and distillate stocks, refinery utilization, products supplied, crude imports/exports.
- 🔧 Conflict rule: if the data bias and the breakout direction disagree, **no trade**.
- ❓ The data filter may duplicate the price breakout, since price already reflects the print. Backtest whether it adds edge.

**4.1 Consensus sources (chosen by the user; pages read 7 Oct 2026)**

| Data point | Unit | Source | Consensus shown? |
|---|---|---|---|
| Commercial crude stocks change | mb | [Investing.com EIA Crude Oil Inventories](https://www.investing.com/economic-calendar/eia-crude-oil-inventories-75); [Trading Economics](https://tradingeconomics.com/united-states/crude-oil-stocks-change) | Yes, both. They differ for 30 Sep: −0.700 vs −0.3 ⚠️ |
| API crude stocks change | mb | [Trading Economics](https://tradingeconomics.com/united-states/api-crude-oil-stock-change) | Yes. Latest (week ending 2 Oct): actual −2.09, consensus −1.9 ❓ re-check on the page |
| Gasoline stocks change | mb | [Investing.com](https://www.investing.com/economic-calendar/gasoline-inventories-485); [Trading Economics](https://tradingeconomics.com/united-states/gasoline-stocks-change) | Yes. 30 Sep: −1.684 vs −0.5 (same on both) |
| Distillate stocks change | mb | [Investing.com](https://www.investing.com/economic-calendar/eia-weekly-distillates-stocks-917); [Trading Economics](https://tradingeconomics.com/united-states/distillate-stocks) | Yes. 30 Sep: −2.251 vs −0.2 (same on both) |
| Refinery utilization change | % pts | [Investing.com](https://in.investing.com/economic-calendar/eia-weekly-refinery-utilization-rates-1961) | **No forecast shown.** Actual −1.5, previous −2.8 |
| Cushing stocks change | mb | [Investing.com](https://in.investing.com/economic-calendar/eia-weekly-cushing-oil-inventories-1657) | **No forecast shown.** Actual +0.553, previous +2.266 |
| SPR | kb (level) | [Trading Economics](https://tradingeconomics.com/united-states/strategic-petroleum-reserve-crude-oil-stocks) | No. Level only: 283,767 vs 284,552 = −785 kb ✅ matches Table 1. Not needed for the signal |

- ⚠️ **The Trading Economics link you gave for Cushing is the commercial crude series**, not Cushing. It shows the Cushing figure (+0.553) only as a side metric. The TE `cushing-crude-oil-stocks` page is the level series. Cushing has no consensus on either site.
- ✅ Investing.com's refinery change (−1.5) matches our calculation from Table 2 (92.5% vs 94.0%).
- ✅ Both sites list release time 14:30 GMT = 10:30 ET (EDT) = 8:00 PM IST. It becomes 15:30 GMT in winter.
- ⚠️ **Single-source rule:** the same data point can carry different consensus values. 🔧 Primary source = **Investing.com** (its table shows actual, forecast and previous per release), confirmed by the user 7 Oct 2026. Trading Economics is the cross-check and the only source for API. Capture template: `eia_snapshot_log.md`.
- ❓ **History depth:** Investing pages show only recent weeks by default. A 50-week backtest needs older rows. Do not scrape the site. Check if older rows load, or copy the table by hand.
- Page quirk: the page header can show the next release date next to the last actual. Use completed rows only.

**30 Sep 2026 worked example (Investing.com consensus)** ✅ arithmetic

| Item | Actual | Forecast | Surprise | Read |
|---|---|---|---|---|
| Crude (mb) | +0.922 | −0.700 | **+1.622** | bearish |
| Gasoline (mb) | −1.684 | −0.5 | −1.184 | bullish |
| Distillate (mb) | −2.251 | −0.2 | −2.051 | bullish |
| Refinery utilization (pts) | −1.5 | n/a | n/a | n/a |
| Cushing (mb) | +0.553 | n/a | n/a | n/a |

- The primary trigger (crude) was bearish while both products were bullish. This is why the secondary flags need a written rule ❓ (for example: count of agreeing flags). Not defined yet.

**4.2 Research notes applied (independent research, common file §16)**
- ✅ **Companion-product surprises matter.** In the study (Linn et al., 2003–2017), crude, gasoline and distillate surprises each moved crude in the same direction (a bigger-than-expected product draw is bullish). That gives our conflict flags an evidence basis. On 30 Sep crude was bearish (+1.622 mb) while gasoline (−1.184) and distillate (−2.051) were bullish: a mixed print, so the net read is unclear. 🔧 Flag rule still to be written ❓.
- ✅ **Move size per 1 SD of crude surprise ≈ 0.27%** (post-2006 estimate, % assumed): about **23 points** on MCX crude at 8,643. Our illustrative 25-point stop is about one SD move ❓ (sample ends 2017, NYMEX).
- ✅ **Timing:** most of the reaction occurs within about 5–7 minutes of the release, before our 15-minute range closes. Continuation after that is unproven (conflicting studies). See B1 vs F1 in the common file §13.
- 🔧 Threshold X for crude in **SD units** ❓ from our own history of consensus misses. The Bloomberg-type median is described as less accurate than expected in the literature (snippet ❓).
- ❓ IV: if the release-driven drop happens in the first minutes, entering at T + 15 buys after much of it. Tonight's chain at T − 5 and T + 15 tests this.

## 5. Level Construction

Moved to `eia_common_execution.md` §3 (opening range, midpoint, floor pivots; identical for both assets). Crude uses the 5-min execution chart and floor pivots from the previous MCX day.

## 6. Instrument Selection (options)

**Volatility crush** ✅ is a real risk. ⚠️ Mechanism correction: IV is usually bid up *into* the event and falls *after* the print. It does not typically "spike at release, then collapse". The size of the drop for MCX crude weekly events is ❓. Measure it from option-chain history.

| Source claim | Verdict |
|---|---|
| Slightly ITM, delta 0.55–0.65 | ⚠️ Reasonable choice, but not "vega protection". See below. |
| ITM insulates from vega | ⚠️ **Wrong as stated.** Vega is highest ATM. A 0.60-delta option has almost the same absolute vega as ATM. The only benefit is a higher premium, so the *percentage* loss from an IV drop is smaller. |
| ITM = "high gamma, maximizes acceleration" | ⚠️ **Wrong.** Gamma peaks ATM and falls as you go ITM. |
| "1–2 strikes ITM" ≈ delta 0.60 | ⚠️ Not reliable. Strike gap, IV and days to expiry decide the delta. **Select by delta from the live chain**, not by strike count. |
| OTM/ATM premium is all extrinsic | ✅ |

**Which Greek does what (use for strike selection)** ✅
| Greek | Want | Where it is best |
|---|---|---|
| Delta | high (direction pays) | deeper ITM |
| Vega ÷ premium | **low** (small % loss when IV falls) | deeper ITM |
| Theta ÷ premium | low (small % decay) | deeper ITM |
| Gamma | high (delta speeds up) | ATM (conflicts with the rows above) |

**Live chain snapshot analysis** (MCX CRUDEOIL, Fut 8643, ATM 8650, step 50, expiry 15 Oct 2026; screenshot taken 6 Oct 2026, Greeks as shown by the chart tool) ✅ arithmetic / ❓ vendor Greeks

Calls (buy on a bullish break). `Vega%` = vega ÷ LTP. `BE move` = futures points needed to offset an assumed 3-pt IV drop = vega × 3 ÷ delta.

| Strike | Delta | LTP | Vega% | Theta% /day | BE move (pts) | Net ₹ if fut +40, IV −3 |
|---|---|---|---|---|---|---|
| 8250 | 0.72 | 524.7 | 0.87% | 2.6% | 19 | +15.2 |
| 8350 | 0.67 | 458.9 | 1.07% | 3.2% | 22 | +12.1 |
| **8400** | 0.65 | 428.7 | 1.18% | 3.6% | 23 | +10.9 |
| **8450** | 0.62 | 395.2 | 1.31% | 3.9% | 25 | +9.3 |
| 8500 | 0.59 | 364.8 | 1.44% | 4.3% | 27 | +7.8 |
| 8600 | 0.54 | 311.0 | 1.73% | 5.1% | 30 | +5.5 |
| 8650 (ATM) | 0.51 | 284.8 | 1.90% | 5.6% | 32 | +4.2 |

Puts (buy on a bearish break), same method:

| Strike | Delta | LTP | Vega% | BE move (pts) | Net ₹ if fut −40, IV −3 |
|---|---|---|---|---|---|
| 9000 | −0.67 | 504.6 | 0.97% | 22 | +12.1 |
| 8950 | −0.65 | 469.2 | 1.07% | 23 | +10.9 |
| **8900** | −0.62 | 432.8 | 1.19% | 25 | +9.4 |
| 8850 | −0.60 | 401.1 | 1.31% | 26 | +8.3 |
| 8750 | −0.54 | 344.0 | 1.56% | 30 | +5.5 |
| 8650 (ATM) | −0.49 | 289.4 | 1.87% | 33 | +3.4 |

Findings:
- Deeper ITM wins on every metric except cost and liquidity: lower vega%, lower theta%, higher delta. The ATM option needs ~32 pts just to offset a 3-pt IV drop; an 8400 call needs ~23.
- **Gamma is irrelevant on this chain.** Shown as 0.0005–0.0006 everywhere; on a 40-pt move it adds only ≈ ₹0.4. Drop the "gamma edge" idea.
- **Theta is small for a 90-min hold** (≈ ₹15/day, roughly ₹1–2 over the window). Vega and delta decide the trade.
- IV is ~52–55% across strikes (shallow skew). ❓ The 3-pt IV drop and the 40-pt move are **illustrative assumptions**, not measured. At a 5-pt IV drop, an 8400 call nets about zero on a 40-pt move. Measure real IV change from the 10:30 ET release on past Wednesdays.
- Liquidity (volume column): 8400 call 78,986 and 8450 call 56,318 are liquid. 8250–8350 calls are thin (1,198–18,206). Put volumes are lower and the column is cut off in the screenshot; ITM puts at 8950/9000 look thin. ❓ Check bid-ask live; the screenshot shows only LTP.
- Cost: premium × lot size. ❓ Confirm the lot size (assumed 100 barrels).
- 🔧 Working rule: **calls ≈ 8400–8450, puts ≈ 8900–8950 (delta 0.62–0.65)** on this chain, then re-pick from the live chain each Wednesday by the same table. Skip any strike with a wide bid-ask.
- No strike wins every row. IV protection and gamma pull in opposite directions. 🔧 Compromise: **delta 0.60–0.70**, then compare candidates on the live chain by **vega ÷ premium** (lower = better IV protection) and **bid-ask spread** (tighter = better). ❓ Exact band to be tested.
- Options for real vega control: (a) trade the **future** (zero vega, linear, margin-based), (b) deeper ITM (delta ≥ 0.8; costs more, lower leverage), (c) a debit spread (caps vega and theta, caps profit).
- Bid-ask spread and depth are information only while broker execution is parked (`eia_common_execution.md` §12).
- ❓ MCX specifics to confirm from the contract spec: lot size, strike interval, option expiry vs future expiry, which future underlies the option, trading hours.

## 7. Execution Rules

Moved to `eia_common_execution.md` §6–§12 (entry, stop loss, targets and scaling, breakeven, trailing, time stop, order mechanics). Identical for crude and gas. All the corrections in the log below (#10–#32) now live there.

## 8. Risk Management

Moved to `eia_common_execution.md` §11: 1 lot, 1 trade per report, risk filter at 1% of equity (CRUDEOIL 100 bbl, CRUDEOILM 10 bbl).

## 9. Corrections Log

| # | Source claim | Verdict |
|---|---|---|
| 1 | Release at 8:00 PM IST | ⚠️ Only during US daylight time. 9:00 PM IST otherwise. |
| 2 | Open Table 1 for Cushing | ⚠️ **Wrong.** Cushing is in Table 4 (and 9). |
| 3 | Open Table 1 for refinery utilization | ⚠️ **Wrong.** Utilization is in Table 2 (and 9). |
| 4 | Column "week-on-week change" in Table 1 | ⚠️ Table 1 says "Difference". |
| 5 | "PADD 2 Stocks at Cushing" label | ⚠️ Actual row label is "Cushing". |
| 6 | 4 pillars = full picture | ⚠️ Incomplete. Add distillates, products supplied, imports/exports, production. |
| 7 | 922 = build of 922,000 barrels | ✅ |
| 8 | Pivot formulas | ✅ |
| 9 | Midpoint formula | ✅ |
| 10 | 15-min macro chart needed | ⚠️ Redundant. |
| 11 | ITM options insulate from vega | ⚠️ Wrong. Only reduces *percentage* loss. |
| 12 | ITM options have max gamma | ⚠️ Wrong. ATM has max gamma. |
| 13 | IV spikes at release then implodes | ⚠️ Loosely true. IV usually peaks before the print. |
| 14 | Draw = bullish | ⚠️ Only versus consensus. |
| 15 | "Positive surprise" | ⚠️ Ambiguous. Use bullish/bearish. |
| 16 | 35–45 point TP1 capture | ❓ Unverified. Removed. |
| 17 | Breakeven stop = zero risk | ⚠️ False for options. |
| 18 | 1h vs 1.5h window | ⚠️ Inconsistent. |
| 19 | "Institutional" framing | ⚠️ A retail breakout rule set, not a documented institutional method. The label is not evidence of edge. |
| 20 | Overall edge | ❓ No evidence provided. Needs backtest (§10). |
| 21 | Targets are "volatility-adjusted" | ⚠️ Pivots use yesterday's range. Only the ATR trail is volatility-based. |
| 22 | Stops can be "market-stop orders" on the option from a future-price level | ⚠️ Not native on MCX options. Alerts or premium-level conversion needed. (execution parked). |
| 23 | 60/40 split | ⚠️ Needs ≥ 5 lots. |
| 24 | Delta 0.60 "cushions" a 20-pt drop to ~12 | ⚠️ Arithmetic ✅ (0.60 × 20), but it is pass-through of 60%, not protection. IV, spread, slippage add. |
| 25 | News breakouts "systematically" reach pivots | ❓ No evidence. |
| 26 | TP1 locks profitability | ⚠️ Break-even win rate ≈ 58% in the worked example. |
| 27 | "Swing low" vs "low of previous candle" | ⚠️ Inconsistent. Use previous closed candle. |
| 28 | Trail formula | ⚠️ Missing the never-loosen (max/min) rule. |
| 29 | "Trailing take profit" | ⚠️ It is a trailing stop. |
| 30 | ATR 14 × 2.0 "institutional" | ⚠️ Not a standard. Classic Chandelier is 22 × 3.0. |
| 31 | Candle trail and ATR trail on the same position | ⚠️ No priority rule. Use one, or the tighter. |
| 32 | No pivot resistance past R2 | ⚠️ R3/S3 exist. |

**My own earlier errors, corrected:** I first said utilization was in Table 1 (it is in Table 2), and that Cushing was "probably" in Table 4 (now verified).

## 10. Open Questions / To Validate

- Backtest ≥ 50 Wednesdays. **No MCX 5-min history available.** Proxy: NYMEX CL 5-min around the same release (TradingView) for pattern testing, then forward-test on MCX with paper trades or minimum size. ❓ The proxy ignores USD/INR and MCX spreads. Metrics: win rate, average R, max drawdown, with and without the data filter, midpoint SL vs alternatives.
- Surprise threshold X (kb).
- Stop touch vs candle close; TP1 buffer after breakeven; trail buffer (2 pts vs ATR fraction); ATR/Chandelier parameters; time stop length.
- Confirm the crude specs against the official MCX page (see common file §1). Broker execution is parked.
- MCX contract specs (lot, strike interval, expiries, hours).
- Consensus source (Reuters, Bloomberg, Investing.com) and API timing.
- Confirm account size and risk % (§8).

## 11. References (crude)

Checked 6 Oct 2026. Details of what each does and does not support are in `eia_common_execution.md` §14.

| Source | Status | Use |
|---|---|---|
| [EIA WPSR](https://www.eia.gov/petroleum/supply/weekly/) | ✅ read | Primary source. Summary TXT "released after 10:30 am". Downloads: XLSX, CSV, JSON, PDF. Tables 1–9 verified in §2 |
| [ACY: WTI with API, EIA and technical indicators](https://acy.com/en/market-news/education/wti-crude-oil-trading-strategy-api-eia-technical-indicators-i-r-102027/) | ✅ read | Retail article. Confirms API Tue ~4:30 PM, EIA Wed 10:30 AM and our surprise rule. Pullback strategy P1 is a test variant, not support for ours |
| [Roboforex: how to use the EIA oil report](https://roboforex.com/blog/education/how-to-use-eia-oil-report-in-trading/) | ✅ read | Generic. Crude stocks are the key line. No thresholds or rules |
| [Insignia Futures: learn to trade crude oil futures](https://insigniafutures.com/learn-to-trade-crude-oil-futures/) | ❌ not read | Bot-check screen, not bypassed |
| [StarTrader: day trading crude oil futures](https://www.startrader.com/knowledge-intermediate/day-trading-crude-oil-futures-strategy-indicators-risks/) | ❌ not read | HTTP 403 / bot challenge, not bypassed |

The EIA gas page link with a signed `Policy`/`Signature` query string is time-limited and is not stored. The public URL is used in the gas file.

## Change Log
- 2026-10-06: file created; first research batch evaluated and merged with corrections.
- 2026-10-06: renamed to eia_wpsr_mcx_crude.md; risk rules (1 trade, 1% cap); CL proxy backtest plan.
- 2026-10-06: full rearrangement. Verified Table 1/2/4/9 contents on eia.gov; fixed Cushing and utilization locations; added data map, units, reference print.
- 2026-10-06: stop-loss / targets / trailing batch evaluated; §7 rewritten (order mechanics, lot split, break-even win rate, single trailing engine); corrections #21-32 added.
- 2026-10-06: sections 5, 7, 8 moved to eia_common_execution.md (rules are the same for crude and gas). This file keeps report mechanics, data map, signal, and the crude option-chain analysis.
- 2026-10-06: added references section with links.
- 2026-10-07: consensus sources added (§4.1); 30 Sep surprise computed (+1.622 mb, bearish); Cushing TE link flagged.
- 2026-10-07: broker execution parked.
- 2026-10-07: MCX specs added in the common file §1; crude options expire 15 Oct 2026; next WPSR (14 Oct) falls one day before expiry.
- 2026-10-07: contract chosen: CRUDEOIL standard (100 bbl). Cost and risk per lot in the common file §11.
- 2026-10-07: account ₹50,000. CRUDEOIL standard fails the 1% risk filter and the premium guard; CRUDEOILM passes. Contract decision pending (common file §11).
- 2026-10-07: 1% cap dropped for Phase 1 (₹50,000). Crude contract (standard vs CRUDEOILM) still open; see common file §11.
- 2026-10-07: crude contract final: CRUDEOIL standard, Wednesdays only, one trade per report.
- 2026-10-07: independent research applied (§4.2): products as same-direction flags, move per SD, timing, IV test.
