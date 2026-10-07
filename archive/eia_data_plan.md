# EIA Data Plan: forward capture and historical data

Decided 7 Oct 2026: **capture forward and also get historical data.** Purpose: get from 6 events per instrument to 50+ so the open questions (continuation vs fade, stop type, exit design, surprise threshold) can be tested.

## 1. What is saved now (backfilled from the user's TradingView chart)

| File | Content | Rows |
|---|---|---|
| `data/mcx_crudeoil_5min_release_windows.csv` | 5-min bars 14:00–16:00 UTC (7:30–9:30 PM IST) on 6 Wednesdays: 26 Aug, 2, 9, 16, 23, 30 Sep | 150 |
| `data/mcx_natgasmini_5min_release_windows.csv` | Same window on 6 Thursdays: 27 Aug, 3, 10, 17, 24 Sep, 1 Oct | 150 |
| `data/mcx_crudeoil_daily.csv`, `data/mcx_natgasmini_daily.csv` | Daily open, high, low, close, volume per MCX trading day, 24 Aug to 7 Oct (7 Oct partial) | 32 each |

- Source: MCX continuous front month `CRUDEOIL1!` and `NATGASMINI1!`, 5-min, read from the chart's loaded series. Times in UTC (release = 14:30 UTC in US daylight time, 15:30 UTC in standard time). Checked: no malformed bars, and the 9 Sep crude range reproduces the pass-1 result.
- The chart only keeps about **5,350 bars (about 6 weeks)** per symbol. The oldest days drop out as new days arrive, so capture each week.

## 2. Data-quality rules found so far ✅

1. **The continuous `1!` symbol includes the expiring contract near expiry.** Daily volume shows it:
   - Gas: normal ≈ 150,000–330,000 per day. 24 Aug–26 Aug: 72,554 / 36,336 / 20,384. 24 Sep 56,378 and 25 Sep 19,073 (expiring contract).
   - Crude: normal ≈ 40,000–100,000. 18 Sep 24,739 and 21 Sep 17,981.
2. 🔧 **Rule:** flag a day as unusable if daily volume is under 50% of the median of the previous 5 days, and do not use it as an event day or as the "previous day" for pivots. On such days use the next contract (`2!`) or skip.
3. Impact on pass 1: gas 24 Sep (event) is unusable. **Gas 27 Aug pivot levels came from 26 Aug (20,384 contracts, the expiring contract), so its pivot-based TP1/TP2 are unreliable** (its range and signal are fine). Crude events are clean (the thin crude days, 18 and 21 Sep, are not event days or previous days of one).

## 3. Forward capture (every week)

After each release (Wednesday for crude, Thursday for gas, after the 90-minute window ends):
1. **Prices:** Claude extracts that day's 5-min bars (14:00–16:00 UTC; use 15:00–17:00 UTC after 1 Nov) from the chart and appends them to the window CSV. Also appends the day's row to the daily CSV. Needs TradingView Desktop open on the user's machine.
2. **Consensus and actuals:** one JSON record per release in `records/` (schemas in `schemas/`), from `eia_snapshot_log.md` Blocks A–C. Take the consensus **before** the release.
3. **IV:** ATM IV at T − 5 and T + 15 (Block E), if a chain screenshot was taken.
4. **Check volume** for the event day and the previous day (rule in §2).
5. Expect about **2 new events per week (1 crude, 1 gas), 100 per year**. To reach 50 events per instrument takes about a year. Historical data (§4) is what shortens that.

## 4. Historical data options

**MCX directly: not available.** Broker APIs (e.g. Kite Connect) do not serve intraday candles for **expired** MCX futures (developer-forum answers; they said they were working on it). So long MCX 5-min history cannot be bought or downloaded. Forward capture is the only MCX route.

**NYMEX proxy (WTI CL, Henry Hub NG).** The report release time is identical, and the reaction in percent should carry over to MCX, since MCX prices follow NYMEX × USD/INR. It ignores the INR rate, MCX spreads and MCX hours.

| Provider | What it offers (from search summaries ❓) | Notes |
|---|---|---|
| **Databento** | CME Globex (all CME/NYMEX futures). OHLCV at 1-second, 1-minute, 1-hour, 1-day, 15+ years. Pay-as-you-go from about $0.50/GB | We only need about 4 hours around each release, so the volume is tiny and the cost should be a few dollars ❓. Needs the user's own account and API key |
| **FirstRate Data** | 1-, 5-, 30-minute, 1-hour, daily futures data, up to 15 years, individual contracts and back-adjusted continuous series | One-off purchase ❓ price not checked |
| **Kibot** | Low-cost minute data, about 4 years on the premium plan | ❓ |
| **Barchart** | 1-minute data going back about 10 years | Subscription ❓ |

**Recommended:** Databento for CL and NG, 1-minute OHLCV, a window of about 13:00–17:00 UTC on Wednesdays and Thursdays from 2018 onward. We aggregate to 5-minute ourselves. That gives about 400 events per instrument.

**Consensus history** is a separate need (the surprise for each past release). Investing.com shows forecast, actual and previous per release; older rows must be copied by the user (no scraping). Without it, historical prices can test continuation and stops, but not the surprise filter.

## 5. What Claude cannot do

- Buy data, create accounts, or enter API keys or card details. The user does that.
- Once the user has a key set as an environment variable on their machine, a short script can pull the windows. Ask first, since the user had said no coding for the strategy itself.

## 6. Decisions needed from the user

1. Approve **Databento** (or name another provider)? Create the account and set the key yourself.
2. OK for a short data-pull script (data only, not strategy)?
3. Who copies the consensus history from Investing.com (about 50 weeks per report), and how far back does it go on your view?
4. Forward capture: run it on request after each release, or schedule it? A scheduled run needs TradingView and Claude open at the time.

## 7. Decision log
- 2026-10-07: **Databento skipped for now** (user). No external historical data. History grows by forward capture only (about 2 events per week). A free alternative to widen the sample is to read **15-minute and 30-minute bars** from the same TradingView chart (about 18 and 36 weeks respectively, same bar cap); not done yet.

- 2026-10-07: 15-min history (from 1 Jun, 5,232 bars) and 30-min history (from 30 Mar crude, 24 Apr gas) read from the chart and analysed in `eia_pass2_results.md`. Raw 15/30-min bars were not saved; only derived metrics. Event calendar with correct release times: `data/events.csv`.

- 2026-10-07: **free EIA history downloaded** (7 files, `data/eia/`, about 1.3 MB: WTI and Henry Hub daily spot; weekly crude, Cushing, gasoline, distillate stocks; weekly Lower 48 gas storage). First use: `eia_daily_test_results.md`.

## Change Log
- 2026-10-07: created. Backfilled 12 release windows and daily bars; roll/volume rule added; options for historical data listed.
- 2026-10-07: Databento skipped.
