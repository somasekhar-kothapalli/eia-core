# Scripts

## Investing.com consensus history

Each Investing.com event page embeds its own recent history in the page data: about 100 releases with actual, forecast, previous and the exact UTC release time, plus the next upcoming release. Two scripts read it and write the same outputs.

| Script | How it gets the page | Use |
|---|---|---|
| `fetch_investing_playwright.py` | Loads each page in a real Chrome through Playwright over the DevTools protocol (`--launch-chrome` starts the installed Chrome with a throwaway profile; `--cdp URL` attaches to a Chrome you started). No download needed | **The one that worked** (7 Oct 2026: all five pages, no block) |
| `fetch_investing_history.py` | One plain HTTP request per page | The API page returned HTTP 403 to it on 7 Oct 2026, so it stopped. Keep as a fallback; also holds the shared parse/save code |

```
python scripts/fetch_investing_playwright.py --launch-chrome                      # all five series
python scripts/fetch_investing_playwright.py --launch-chrome --series crude_stocks gas_storage
```

Series: `crude_stocks` (EIA crude), `api_crude`, `gas_storage`, `gasoline`, `distillates`.

**Outputs** (`data/consensus/`): `<series>.csv` (completed releases: release_date, release_time_gmt, actual, forecast, previous, unit, occurrence_id; the forecast is as shown at fetch time, so history is *backfilled* consensus), `upcoming_snapshots.csv` (append-only: the upcoming release's forecast with the fetch time; run it about 5 minutes before a release to get a true pre-release snapshot), `raw/` (occurrences exactly as received).

## Rules the scripts follow (do not weaken them)

- Ordinary browsing only: no stealth plugins, no automation-flag hiding, no user-agent or fingerprint spoofing, no proxies, no CAPTCHA solving.
- One page load per series, a pause between pages, never retried.
- Stop on any non-200 status or a verification page. Do not try to get past it; copy by hand instead.
- Investing.com's terms could not be read when these were written. robots.txt allowed `/economic-calendar/`. Keep the volume low and use for personal research only.

## Limits

About 100 releases (back to Nov 2024) per page. Older history needs another source. Release times from the page are mostly right but a few look odd (for example 13:30 GMT in Mar 2025, a Monday 22:00 GMT row in Dec 2025): validate against the EIA schedule before relying on them for intraday work.
