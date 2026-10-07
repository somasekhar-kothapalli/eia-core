# Consensus history (Investing.com, primary source)

Filled by `scripts/fetch_investing.py` (a real Chrome loads each event page; `--deep` also clicks "Show More"). Rules and usage: `scripts/README.md`.

| Series | Page | Unit | File |
|---|---|---|---|
| Crude (commercial stocks change) | investing.com/economic-calendar/eia-crude-oil-inventories-75 | mb | `crude_stocks_table.csv` |
| API crude stocks change (Tuesday evening) | investing.com/economic-calendar/api-weekly-crude-stock-656 | mb | `api_crude_table.csv` |
| Natural gas storage (net change) | investing.com/economic-calendar/natural-gas-storage-386 | Bcf | `gas_storage_table.csv` |
| Gasoline | investing.com/economic-calendar/gasoline-inventories-485 | mb | `gasoline_table.csv` |
| Distillates | investing.com/economic-calendar/eia-weekly-distillates-stocks-917 | mb | `distillates_table.csv` |

- `<series>_table.csv`: `release_utc, release_date_shown, time_shown_ist, actual, forecast, previous`. The forecast is the value shown at fetch time (backfilled), possibly different from the pre-release one. Rows with an actual only are completed releases; the upcoming one has no actual.
- `upcoming_snapshots.csv`: append-only forecasts of the next release with the fetch time. Run the fetch about 5 minutes before a release for a true pre-release snapshot.
- `raw/<series>.json`: embedded page data as received.
- Trading Economics stays a pre-release **cross-check only** (its forecast may be overwritten after the print); do not use its history as consensus. Copy its value by hand into the snapshot log.
