# 06 Data and Capture

**Last revised:** 7 Oct 2026. Purpose: grow from about 15 events per instrument to 50+ so the open questions in `07_open_items.md` can be tested.

## 1. What is saved (all under `data/`)

| File | Content | Rows |
|---|---|---|
| `events.csv` | The 12 release events with the **correct release times** (crude 10 Sep = 16:00 UTC, Thursday 12:00 ET) and notes on unusable days | 12 |
| `mcx_crudeoil_5min_release_windows.csv` | 5-min bars, release −30 to +90 minutes, 6 crude events: 26 Aug, 2 Sep, **10 Sep**, 16, 23, 30 Sep | 150 |
| `mcx_natgasmini_5min_release_windows.csv` | Same window, 6 gas events: 27 Aug, 3, 10, 17, 24 Sep, 1 Oct | 150 |
| `mcx_crudeoil_daily.csv`, `mcx_natgasmini_daily.csv` | Daily open/high/low/close/volume per MCX trading day, 24 Aug to 7 Oct (7 Oct partial) | 32 each |
| `consensus/crude_stocks.csv`, `gas_storage.csv`, `api_crude.csv`, `gasoline.csv`, `distillates.csv` | **Consensus history from Investing.com** (7 Oct 2026, 98–99 completed releases each, 14 Nov 2024 to 1 Oct 2026): actual, forecast, previous, unit, exact UTC release time. API forecast missing on 23 of 99 rows, gasoline on 5, distillates on 6. Forecasts are *backfilled* (as shown at fetch time) | 98–99 each |
| `consensus/upcoming_snapshots.csv`, `consensus/raw/` | Append-only snapshots of upcoming releases with the fetch time; raw JSON as received | |
| `../scripts/` | `fetch_investing_playwright.py` (real Chrome via Playwright, worked) and `fetch_investing_history.py` (plain request, got a 403 on the API page); `README.md` has the rules | |
| `eia/*.xls` (7 files) | Free EIA history, downloaded with the user's approval from eia.gov: WTI and Henry Hub daily spot (1986 and 1997 to 29 Sep 2026); weekly US crude, Cushing, gasoline, distillate stocks; weekly Lower 48 gas storage (2010 to 25 Sep 2026). Latest values match the EIA figures we verified | about 1.3 MB |
| `eia/daily_horizon_test.py`, `daily_horizon_output.txt`, `*_z_returns.csv` | The daily-horizon proxy test (reproducible) | |
| `../schemas/release_event.schema.json`, `examples/`, `README.md` | One unified JSON Schema (v2.0) for a release event, crude and gas, live and historical, plus three validated examples | |

- Source of intraday bars: MCX continuous front month `CRUDEOIL1!` and `NATGASMINI1!` read from the user's TradingView chart. Times in UTC. The raw 15-minute and 30-minute bars used in pass 2 were **not** saved, only the derived results.
- TradingView holds about **5,350 bars per symbol**: about 6 weeks of 5-min, 18 weeks of 15-min, 27–36 weeks of 30-min. The oldest days drop out as new days arrive, so **capture each week**.

## 2. Data-quality rules (found so far) ✅

1. **The continuous `1!` symbol includes the expiring contract near expiry.** Daily volume shows it: gas normal about 150,000–330,000, but 20,384 on 26 Aug and 56,378 / 19,073 on 24 / 25 Sep; crude normal about 40,000–100,000, but 24,739 on 18 Sep and 17,981 on 21 Sep.
2. 🔧 **Rule:** flag a day as unusable if its volume is under 50% of the median of the previous 5 days. Do not use a flagged day as an event day or as the "previous day" for pivots. Use the next contract (`2!`) or skip. Flagged events so far: crude 17 Jun, 19 Aug; gas 25 Jun, 27 Aug, 24 Sep.
3. 🔧 **Release time:** use the EIA schedule (spec §2). A delayed WPSR is Thursday 12:00 ET, not Wednesday 10:30.
4. 🔧 Use completed rows only on Investing.com history pages (the header can show the next release next to the last actual).

## 3. Forward capture (every release)

1. **Before the release (T − 5 min):** consensus snapshot from Investing.com (primary) and Trading Economics (cross-check), into `snapshot_log.md` Block A, plus a chain screenshot of the traded contract.
2. **After the print:** actuals (from the EIA page), surprises and the sign rule (Block B), a source check 30 minutes later (Block C), and a second chain screenshot at T + 15 (Block E: the real IV change).
3. **After the 90-minute window:** Claude extracts that day's 5-min bars from the TradingView chart (release −30 to +90 minutes) and appends them to the window CSV and the daily CSV; Claude also checks volume flags. Needs TradingView Desktop open.
4. **Store one JSON record per release** (`records/wpsr_YYYY-MM-DD.json`, `records/wngsr_YYYY-MM-DD.json`) following the schemas. Anything read after the release is `capture_type: "backfilled"` with `captured_at: null`.
5. Expect about **2 events per week** (1 crude, 1 gas), 100 per year; 50 per instrument takes about a year.

**JSON records:** one unified schema `schemas/release_event.schema.json` (v2.0) covers crude and gas and live, backfill and backtest runs; see `schemas/README.md`. Snapshot-log blocks map to it as: forecast columns → `metrics[].consensus[]`; API row → the `api_crude_change` metric; actuals → `metrics[].actual`; surprise columns → `metrics[].surprise` and `bias`; source check → a `data_quality` note; Block D (price) → `levels` and `signal`; Block E (IV) → `trade.option.iv_before/iv_after`. The two earlier schemas are in `archive/schemas_v1/`.

## 4. Historical data options

- **MCX directly: not available.** Broker APIs (e.g. Kite Connect) do not serve intraday candles for **expired** MCX futures. Forward capture is the only MCX route.
- **NYMEX proxy (CL, NG)** has the same release time and should carry over in percent terms, but ignores the INR rate, MCX spreads and hours. Providers (from search summaries ❓): Databento (CME Globex OHLCV, 1-minute, 15+ years, from about $0.50/GB, cost for our windows probably a few dollars), FirstRate Data (1/5/30-minute futures, up to 15 years), Kibot (about 4 years of minute data), Barchart (1-minute, about 10 years). **Databento skipped for now (user decision).**
- **Consensus history** (the surprise for each past release) is a separate and the most important need. Investing.com shows forecast, actual and previous per release; older rows must be copied by the user (no scraping). Depth unknown ❓.
- **Free alternative used:** 15-minute and 30-minute bars from the chart (done, pass 2); EIA free history (done, proxy test).
- What Claude cannot do: buy data, create accounts, enter API keys or card details.

## 5. History data needed (walk-through, 7 Oct 2026)

**Goal:** for each past release, one row with the **first-release actual**, the **pre-release consensus** and the **price reaction**, so we can set the surprise threshold (SD units), test the data filter and the flags, and rerun the daily-horizon test with real surprises.

| # | Data point | Used for | Have? | Source | Needs from user |
|---|---|---|---|---|---|
| C1 | Crude commercial stocks change: **first-release actual** | Trigger | EIA revised history (`WCESTUS1w.xls`, 1982+) ✅; first-release actuals come with the consensus rows | Investing.com (page 75) | **Yes (copy)** |
| C2 | Crude **consensus** (forecast) | Surprise = actual − forecast; SD of misses | ❌ | Investing.com (page 75) | **Yes (copy)** |
| C3 | Gasoline and distillate: actual and consensus | Conflict flags (same-direction effect on crude) | Actuals ✅ (`WGTSTUS1w`, `WDISTUS1w`); consensus ❌ | Investing.com (pages 485, 917) | Yes (copy), optional |
| C4 | Cushing and refinery utilization change | Flags without consensus (direction only) | Cushing ✅ (2004+); utilization ❌ (EIA file `WPULEUS3w.xls`, 111 KB, exists) | EIA | Approve download |
| C5 | **API** crude change (actual) and **API consensus** | Pre-release signal; separates the part of the EIA surprise already priced | ❌ | **Investing.com page found 7 Oct 2026:** [API Weekly Crude Oil Stock](https://www.investing.com/economic-calendar/api-weekly-crude-stock-656), 20:30 GMT, 11 rows shown by default, **forecast present on about 6 of 10 completed rows (missing on others)** ❓ per a page summary | **Yes (copy; use "Show more")** |
| C6 | Optional EIA extras: SPR, production, products supplied, crude imports | Context only | ❌ (EIA files `WCSSTUS1w`, `WCRFPUS2w`, `WRPUPUS2w`, `WCEIMUS2w` exist, about 110–130 KB each) | EIA | Approve download if wanted |
| G1 | Gas Lower 48 net change: **first-release actual** | Trigger | EIA levels (`NW2_EPG0_SWO_R48_BCFw.xls`, 2010+, net change = difference) ✅ | Investing.com (page 386) | **Yes (copy)** |
| G2 | Gas **consensus** | Surprise; SD of misses; the threshold floor of about 2 Bcf | ❌ | Investing.com (page 386) | **Yes (copy)** |
| G3 | Gas optional: South Central Salt, regional, implied flow | Flag only | ❌ | EIA | Low priority |
| P1 | **Actual release dates** (resolves holiday delays) | Aligning prices | Calendar for 2026 ✅; earlier years come from the Investing rows | Investing.com dates | Comes with the copies |
| P2 | Daily WTI and Henry Hub spot | Daily-horizon test | ✅ (`RWTCd`, `RNGWHHDd`, to 29 Sep 2026) | EIA | None |
| P3 | MCX intraday bars around releases | Strategy tests | 6–22 events per instrument | TradingView chart; forward capture | Weekly capture |

**Why API matters (timing):** API publishes Tuesday about 4:30 PM ET = 20:30 UTC = **2:00 AM IST Wednesday**, outside MCX hours (9:00 AM to 11:30 PM). MCX trades the API news during Wednesday's session, so by the 8:00 PM IST EIA release the API surprise is largely priced and most consensus numbers already lean on it. Useful derived columns: `API surprise` (API − API consensus), `EIA − API`, `EIA − consensus`.

**Status 7 Oct 2026:** C1, C2, C3 (consensus part), C5, G1 and G2 are **done for about 2 years (14 Nov 2024 to 1 Oct 2026)** through `scripts/fetch_investing_playwright.py`. Each Investing page embeds only its latest 100 releases, so older history needs another source. Still open: C4/C6 extra EIA downloads (need approval), G3, and validating Investing's release times against the EIA calendar (a few look odd: 13:30 GMT in Mar 2025, a Monday 22:00 GMT row on 29 Dec 2025).

**Order of work (original plan)**
1. Crude: C1 + C2 from Investing.com (as far back as the page loads).
2. Gas: G1 + G2.
3. API: C5 (find the page, copy).
4. Gasoline and distillate consensus (C3), then approve extra EIA downloads (C4, C6) if wanted.
5. Claude merges into one `releases.csv` per report (first-release actual, forecast, surprise, API, spot returns) and reruns the tests.

## 6. Decision log (data)

| Date | Decision |
|---|---|
| 6–7 Oct 2026 | Capture forward and also get historical data |
| 7 Oct 2026 | Databento skipped for now |
| 7 Oct 2026 | Read 15- and 30-minute bars from the chart to widen the sample (done, pass 2) |
| 7 Oct 2026 | Free EIA history downloaded (7 files) and daily proxy test run |
| 7 Oct 2026 | Investing.com is the primary consensus source; Trading Economics is the cross-check |
| 7 Oct 2026 | **Storage: CSV files are the source of truth** (one file per series, ISO dates, UTC times, fixed units, raw files append-only, derived results generated by scripts). Revisit SQLite/DuckDB only if large history (millions of rows) is added; any database would be derived and gitignored |
| 7 Oct 2026 | Consensus history is copied by hand from Investing.com into `data/consensus/` (no scraping) |
