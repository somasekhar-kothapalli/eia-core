# Scripts

## Layout

| Script | Role |
|---|---|
| `browser.py` | **Reusable, site-independent** real-Chrome helpers (Playwright over the DevTools protocol): `session(args)` (launch or attach), `goto` (stops on non-200 or a verification page), `next_data`, `load_all` (click a "load more" control until it is gone, declining listed overlays), `table_rows`, `pause`, `add_args`. Holds the scraping rules; import it for any other site |
| `fetch_investing.py` | Investing.com only: series list, parsing, CSV writing, CLI. Uses `browser.py` |
| `build_releases.py` | Merges the Investing tables, validates release times and actuals |
| `surprise_test_15y.py` | Daily-horizon surprise test |

The old plain-HTTP fetcher was removed: the API page answered it with HTTP 403 on 7 Oct 2026.

## Investing.com consensus history

Each Investing.com event page embeds its own recent history in the page data: about 100 releases with actual, forecast, previous and the exact UTC release time, plus the next upcoming release. `--deep` also clicks the table's "Show More" until about 1,000 rows are loaded.

```
python scripts/fetch_investing.py --launch-chrome                      # all five series (embedded ~100 rows)
python scripts/fetch_investing.py --launch-chrome --series crude_stocks gas_storage
python scripts/fetch_investing.py --launch-chrome --deep                # also the full table (about 1,000 rows each)
```

Series: `crude_stocks` (EIA crude), `api_crude`, `gas_storage`, `gasoline`, `distillates`.

**Outputs** (`data/consensus/`): `<series>.csv` (completed releases: release_date, release_time_gmt, actual, forecast, previous, unit, occurrence_id; the forecast is as shown at fetch time, so history is *backfilled* consensus), `upcoming_snapshots.csv` (append-only: the upcoming release's forecast with the fetch time; run it about 5 minutes before a release to get a true pre-release snapshot), `raw/` (occurrences exactly as received).

## Rules the scripts follow (do not weaken them)

- Ordinary browsing only: no stealth plugins, no automation-flag hiding, no user-agent or fingerprint spoofing, no proxies, no CAPTCHA solving.
- One page load per series, a pause between pages, never retried.
- Stop on any non-200 status or a verification page. Do not try to get past it; copy by hand instead.
- Investing.com's terms could not be read when these were written. robots.txt allowed `/economic-calendar/`. Keep the volume low and use for personal research only.

## Limits

The embedded data holds about 100 releases (back to Nov 2024). The history table also has a **"Show More" div** under it (a div, not a button). `--deep` clicks it (150 clicks max, 1.5 s apart) until the page stops at about 1,000 rows and writes `<series>_table.csv`. A full-screen sign-up overlay ("All markets. One FREE account", `#regwall-container`) can appear and block clicks; the script declines it with its X. Dates on in.investing.com are `dd-mm-yyyy` (handled). Release times from the page are mostly right but a few look odd (for example 13:30 GMT in Mar 2025, a Monday 22:00 GMT row in Dec 2025): validate against the EIA schedule before relying on them for intraday work.

## Merge and validation

`python scripts/build_releases.py` merges the `_table.csv` files into `data/releases_crude.csv` and `data/releases_gas.csv`, checks release times (New York clock) and actuals against EIA's own series, and writes `data/release_checks.csv`. Details and results: `docs/06_data_and_capture.md`.
