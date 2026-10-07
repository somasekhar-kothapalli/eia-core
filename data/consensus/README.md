# Consensus history (copied by hand from Investing.com)

Primary source (user decision). Paste the raw rows to Claude, who parses them into the CSVs below. No scraping.

| Series | Page | Unit | Save as |
|---|---|---|---|
| Crude (commercial stocks change) | investing.com/economic-calendar/eia-crude-oil-inventories-75 | mb | `crude_stocks.csv` |
| Natural gas storage (net change) | investing.com/economic-calendar/natural-gas-storage-386 | Bcf | `gas_storage.csv` |
| Gasoline (optional) | investing.com/economic-calendar/gasoline-inventories-485 | mb | `gasoline.csv` |
| Distillates (optional) | investing.com/economic-calendar/eia-weekly-distillates-stocks-917 | mb | `distillates.csv` |

## CSV columns (Claude fills these from your paste)

`release_date,release_time_gmt,actual,forecast,previous`

- `release_date` as `YYYY-MM-DD`. Use completed rows only.
- Keep values exactly as shown (mb for crude products, Bcf for gas). Leave `forecast` empty if the page shows none.

## How to copy

1. Open the history table on the page. Use "Show more" until the oldest row you want is visible (as far back as the page allows; the goal is 50+ weeks, more is better).
2. Select the table rows (date, time, actual, forecast, previous) and paste them into the chat as plain text. Pasting in chunks is fine.
3. Tell Claude which series each paste is.

Do not paste the Trading Economics consensus history: its forecast may be overwritten after the print. It stays a pre-release cross-check only.
