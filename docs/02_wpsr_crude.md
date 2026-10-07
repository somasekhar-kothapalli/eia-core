# 02 WPSR (Crude Oil): Report, Data, Consensus and Option Chain

**Catalyst:** EIA Weekly Petroleum Status Report. **Price driver:** NYMEX WTI. **Traded:** MCX CRUDEOIL standard (100 bbl) options. Rules are in `01_strategy_spec.md`.
**Last revised:** 7 Oct 2026. Tags: ✅ verified · 🔧 decided · ❓ open.

## 1. Report mechanics ✅

| Item | Value |
|---|---|
| Release | Wednesday 10:30 AM ET (= 8:00 PM IST in daylight time, 9:00 PM IST in standard time). **Holiday delays: Thursday 12:00 ET (9:30 PM IST)**: 10 Sep, **15 Oct**, 12 Nov 2026 (calendar in spec §2) |
| Data period | Week ending the previous Friday (release Wed 30 Sep = week ending Fri 25 Sep) |
| At 10:30 ET | Summary TXT, all CSV/XLS tables, combined "Data Overview" PDF (Tables 1 + 9). Most per-table PDFs appear at 1:00 p.m. ET. Do not wait for them |
| Units and signs | Headline box in **thousand barrels** (use this for trading). Tables 1, 2, 4 show stocks in **million barrels, 1 decimal** (rounding hides small moves). Flows in kb/d. **Positive = build, negative = draw.** Commercial crude **excludes SPR** |

## 2. Data map (verified on the 25 Sep 2026 tables) ✅

| Table | Name | Use it for |
|---|---|---|
| **1** | U.S. Petroleum Balance Sheet | Stocks (crude total, commercial, SPR, gasoline, jet, distillate, resid, propane); crude supply lines (production, imports, exports); crude input to refineries; **products supplied** (implied demand); net imports. Column label is "Difference" (week ago, year ago) |
| **2** | U.S. Inputs and Production by PAD District | **Refinery utilization %**, gross inputs, operable capacity |
| **4** | Stocks of Crude Oil by PAD District, and Petroleum Products | **Cushing** stocks and crude by PADD |
| **9** | U.S. and PAD District Weekly Estimates | Combined view (includes Cushing and utilization) |
| 3, 5, 5A, 6, 7, 8 | Refiner net production; gasoline stocks; distillate/jet/resid/propane; imports/exports; crude imports by country | Detail only |

- Cushing is **not** in Table 1 and refinery utilization is **not** in Table 1. The fastest single source is the Data Overview PDF (Tables 1 + 9) or the Table 9 CSV.
- "Four pillars" is incomplete: also watch distillate stocks, products supplied, crude imports/exports, production.

## 3. Reference print: week ending 25 Sep 2026 (released Wed 30 Sep) ✅

| Metric | Current | Prior | Change | Source |
|---|---|---|---|---|
| Commercial crude (kb) | 427,320 | 426,398 | **+922** build | headline box |
| Total crude incl. SPR (mb) | 711.1 | 711.0 | +0.1 | Table 1 |
| SPR (mb) | 283.8 | 284.6 | −0.8 | Table 1 |
| Cushing (mb) | 24.3 | 23.7 | ≈ +0.6 (EIA/Investing: +0.553) | Table 4 |
| Refinery utilization | ≈ 92.5% | ≈ 94.0% | ≈ −1.5 pt | Table 2 (gross inputs ÷ capacity: 16,670 ÷ 18,027) |
| Crude input to refineries (kb/d) | 16,257 | 16,811 | −554 | Table 1 |

## 4. Consensus sources (chosen by the user; pages read 7 Oct 2026)

| Data point | Unit | Source | Consensus shown? |
|---|---|---|---|
| Commercial crude change | mb | [Investing.com](https://www.investing.com/economic-calendar/eia-crude-oil-inventories-75) (**primary**); [Trading Economics](https://tradingeconomics.com/united-states/crude-oil-stocks-change) (cross-check) | Yes, both. They differ for 30 Sep: −0.700 vs −0.3 |
| API crude change (Tuesday) | mb | [Trading Economics](https://tradingeconomics.com/united-states/api-crude-oil-stock-change) | Yes. Week ending 2 Oct: actual −2.09, consensus −1.9 ❓ re-check on the page |
| Gasoline change | mb | [Investing.com](https://www.investing.com/economic-calendar/gasoline-inventories-485); [Trading Economics](https://tradingeconomics.com/united-states/gasoline-stocks-change) | Yes. 30 Sep: −1.684 vs −0.5 (same on both) |
| Distillate change | mb | [Investing.com](https://www.investing.com/economic-calendar/eia-weekly-distillates-stocks-917); [Trading Economics](https://tradingeconomics.com/united-states/distillate-stocks) | Yes. 30 Sep: −2.251 vs −0.2 (same on both) |
| Refinery utilization change | pts | [Investing.com](https://in.investing.com/economic-calendar/eia-weekly-refinery-utilization-rates-1961) | **No forecast.** Actual −1.5 (matches our Table 2 figure) |
| Cushing change | mb | [Investing.com](https://in.investing.com/economic-calendar/eia-weekly-cushing-oil-inventories-1657) | **No forecast.** Actual +0.553 |
| SPR | kb (level) | [Trading Economics](https://tradingeconomics.com/united-states/strategic-petroleum-reserve-crude-oil-stocks) | No. Level only (283,767 vs 284,552 = −785 kb ✅ matches Table 1). Not needed |

- ⚠️ The Trading Economics page `crude-oil-stocks-change` is the **commercial crude** series, not Cushing.
- Investing.com and Trading Economics both list 14:30 GMT = 10:30 ET (daylight time).
- Investing pages show only recent weeks by default; older rows needed for a backtest must be copied by hand (no scraping) ❓ depth unknown. The page header can show the next release date next to the last actual: use completed rows only.

**Worked example, 30 Sep 2026 (Investing.com forecast) ✅ arithmetic**

| Item | Actual | Forecast | Surprise | Read |
|---|---|---|---|---|
| Crude (mb) | +0.922 | −0.700 | **+1.622** | bearish (with Trading Economics −0.3: +1.222, same sign) |
| Gasoline (mb) | −1.684 | −0.5 | −1.184 | bullish |
| Distillate (mb) | −2.251 | −0.2 | −2.051 | bullish |

The primary trigger was bearish while both products were bullish. That is why the conflict-flag rule has to be written (spec §3). Products moving crude in the same direction is supported by the literature (`05_evidence.md`).

## 5. CRUDEOIL option chain (snapshot 6 Oct 2026, before the release; Fut 8,643, ATM 8,650, step 50, expiry 15 Oct 2026; Greeks as shown by the chart tool ❓)

`Vega%` = vega ÷ LTP. `BE move` = futures points needed to offset an assumed 3-pt IV drop = vega × 3 ÷ delta. `Net` = delta × 40 − vega × 3 (illustrative 40-pt move, 3-pt IV drop ❓, not measured).

Calls:

| Strike | Delta | LTP | Vega% | Theta%/day | BE move | Net ₹ | Cost per lot (×100) |
|---|---|---|---|---|---|---|---|
| 8250 | 0.72 | 524.7 | 0.87% | 2.6% | 19 | +15.2 | ₹52,470 |
| 8350 | 0.67 | 458.9 | 1.07% | 3.2% | 22 | +12.1 | ₹45,890 |
| **8400** | 0.65 | 428.7 | 1.18% | 3.6% | 23 | +10.9 | ₹42,870 |
| **8450** | 0.62 | 395.2 | 1.31% | 3.9% | 25 | +9.3 | ₹39,520 |
| 8500 | 0.59 | 364.8 | 1.44% | 4.3% | 27 | +7.8 | ₹36,480 |
| 8600 | 0.54 | 311.0 | 1.73% | 5.1% | 30 | +5.5 | ₹31,100 |
| 8650 (ATM) | 0.51 | 284.8 | 1.90% | 5.6% | 32 | +4.2 | ₹28,480 |

Puts:

| Strike | Delta | LTP | Vega% | BE move | Net ₹ | Cost per lot (×100) |
|---|---|---|---|---|---|---|
| 9000 | −0.67 | 504.6 | 0.97% | 22 | +12.1 | ₹50,460 |
| **8950** | −0.65 | 469.2 | 1.07% | 23 | +10.9 | ₹46,920 |
| **8900** | −0.62 | 432.8 | 1.19% | 25 | +9.4 | ₹43,280 |
| 8850 | −0.60 | 401.1 | 1.31% | 26 | +8.3 | ₹40,110 |
| 8750 | −0.54 | 344.0 | 1.56% | 30 | +5.5 | ₹34,400 |
| 8650 (ATM) | −0.49 | 289.4 | 1.87% | 33 | +3.4 | ₹28,940 |

Findings:
- On this chain **deeper ITM wins on every metric except cost and liquidity** (lower vega%, theta%, higher delta). ATM needs about 32 points to offset a 3-pt IV drop; the 8400 call needs about 23.
- **Gamma is irrelevant** (0.0005–0.0006; about ₹0.4 on a 40-pt move). **Theta is small** over 90 minutes (about ₹1–2). Vega and delta decide.
- IV about 52–55% across strikes (shallow skew). At a 5-pt IV drop an 8400 call nets about zero on a 40-pt move ❓ (real drop unmeasured).
- Liquidity (volume): 8400 call 78,986 and 8450 call 56,318 are liquid; 8250–8350 calls are thin (1,198–18,206). Put volumes are lower and the column is cut off. Bid-ask is not shown (parked).
- **Working zone: calls 8400–8450, puts 8900–8950 (delta 0.62–0.65)**, re-picked from the live chain each Wednesday by the same table. For vega-free exposure the alternatives are the future itself, deeper ITM (delta ≥ 0.8) or a debit spread.
- ⚠️ **Crude expiry:** these options expire **Thu 15 Oct**, the day of the next WPSR. Use the next-month chain then (spec §7).

## 6. Sources

| Source | Status | Use |
|---|---|---|
| [EIA WPSR](https://www.eia.gov/petroleum/supply/weekly/) | ✅ read | Primary: summary TXT "released after 10:30 am"; downloads XLSX, CSV, JSON, PDF. Tables 1–9 verified |
| [EIA WPSR schedule](https://www.eia.gov/petroleum/supply/weekly/schedule.php) | ✅ read | 2026 holiday delays (Thursday 12:00 ET) |
| [ACY article, 6 Aug 2026](https://acy.com/en/market-news/education/wti-crude-oil-trading-strategy-api-eia-technical-indicators-i-r-102027/) | ✅ read | Retail article. Confirms API Tue ~4:30 PM, EIA Wed 10:30 AM and our surprise rule (its case: forecast −1.0, actual +2.0, surprise +3.0 mb ✅ arithmetic). A different strategy (pullback + 50 EMA/RSI/Bollinger), no evidence. Test variant P1 only |
| [Roboforex](https://roboforex.com/blog/education/how-to-use-eia-oil-report-in-trading/) | ✅ read | Generic; no thresholds or rules |
| [Insignia Futures](https://insigniafutures.com/learn-to-trade-crude-oil-futures/) | ❌ not read | Bot-check screen, not bypassed |
| [StarTrader](https://www.startrader.com/knowledge-intermediate/day-trading-crude-oil-futures-strategy-indicators-risks/) | ❌ not read | HTTP 403 / bot challenge, not bypassed |

None of the readable secondary sources gives surprise thresholds, typical move size, stop or target distances, a backtest, or option guidance. See `08_corrections_log.md` for every claim checked.
