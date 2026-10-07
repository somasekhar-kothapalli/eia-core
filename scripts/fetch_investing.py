"""Fetch EIA / API consensus history from Investing.com event pages into CSV, through a real Chrome (see browser.py).

Each event page (Next.js) embeds its latest ~100 releases (actual, forecast, previous, exact UTC time) plus the next
upcoming release. With --deep the history table's "Show More" is clicked until about 1,000 rows are loaded.

Outputs (default folder data/consensus/):
- <series>_table.csv           (--deep) the full history table: release_utc, release_date_shown, time_shown_ist, actual,
                               forecast, previous (values keep their units, e.g. 1.900M). The forecast is the value on the
                               page at fetch time, i.e. a BACKFILLED consensus (it may differ from the pre-release value).
- upcoming_snapshots.csv       append-only: the upcoming release's forecast with the fetch time. Run it 5 minutes
                               before a release and the row is a true PRE-RELEASE snapshot.
- raw/<series>.json            the embedded occurrences exactly as received, overwritten each run (the snapshot file keeps
                               the forecast history; git keeps old versions)

Usage:  python scripts/fetch_investing.py --launch-chrome [--deep] [--series crude_stocks gas_storage ...] [--out data/consensus]
Rules: see browser.py. Investing.com's terms could not be read; robots.txt allowed /economic-calendar/. Low volume, personal research only.
"""
import argparse
import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path

from browser import add_args, goto, load_all, next_data, pause, session, table_rows

BASE = "https://in.investing.com/economic-calendar/"
SERIES = {
    "crude_stocks": ("eia-crude-oil-inventories-75", "EIA crude oil inventories (commercial)"),
    "api_crude": ("api-weekly-crude-stock-656", "API weekly crude oil stock"),
    "gas_storage": ("natural-gas-storage-386", "EIA natural gas storage (net change)"),
    "gasoline": ("gasoline-inventories-485", "EIA gasoline inventories"),
    "distillates": ("eia-weekly-distillates-stocks-917", "EIA distillates stocks"),
}
FIELDS = ["release_date", "release_time_gmt", "actual", "forecast", "previous", "unit", "occurrence_id"]  # upcoming_snapshots.csv columns


def row(o):
    t = datetime.strptime(o["occurrence_time"], "%Y-%m-%dT%H:%M:%SZ")
    return {
        "release_date": t.strftime("%Y-%m-%d"),
        "release_time_gmt": t.strftime("%H:%M"),
        "actual": o.get("actual"),
        "forecast": o.get("forecast"),
        "previous": o.get("previous"),
        "unit": o.get("unit", ""),
        "occurrence_id": o["occurrence_id"],
    }


def save_series(name, occ, out, now):
    """Overwrite raw/<series>.json with the embedded data and append the upcoming release's forecast to the snapshot file."""
    label = SERIES[name][1]
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "raw" / f"{name}.json").write_text(json.dumps(occ), encoding="utf-8")
    done = [row(o) for o in occ if o.get("actual") is not None]
    upcoming = [row(o) for o in occ if o.get("actual") is None]
    snaps = out / "upcoming_snapshots.csv"
    if upcoming:
        new_file = not snaps.exists()
        with open(snaps, "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            if new_file:
                w.writerow(["fetched_at_utc", "series"] + FIELDS)
            for r in upcoming:
                w.writerow([now.strftime("%Y-%m-%dT%H:%M:%SZ"), name] + ["" if r[k] is None else r[k] for k in FIELDS])
    rng = (min(r["release_date"] for r in done), max(r["release_date"] for r in done)) if done else ("-", "-")
    print(f"{name:13s} {label}: {len(done)} completed rows ({rng[0]} to {rng[1]}), "
          f"upcoming: {[(r['release_date'], r['forecast']) for r in upcoming]}")


TABLE = 'table[data-test="occurrence-table"]'
SIGNUP_WALL_CLOSE = "#regwall-container div.absolute.right-6.top-6"  # "All markets. One FREE account" overlay: decline it
IST = timedelta(hours=5, minutes=30)  # in.investing.com shows times in IST (no daylight saving)


def occurrences(page):
    return next_data(page)["props"]["pageProps"]["state"]["economicCalendarEventStore"]["occurrences"]


def write_table(name, rows, out):
    path = out / f"{name}_table.csv"
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["release_utc", "release_date_shown", "time_shown_ist", "actual", "forecast", "previous"])
        for r in rows:
            d = r[0].split(" (")[0]  # older rows read "Dec 01, 2005 (Nov)"
            day = datetime.strptime(d, "%d-%m-%Y" if d[2:3] == "-" else "%b %d, %Y").date().isoformat()  # in. site: 15-10-2026
            utc = (datetime.fromisoformat(f"{day}T{r[1]}") - IST).strftime("%Y-%m-%dT%H:%MZ")
            w.writerow([utc, day, *r[1:5]])
    print(f"{name}: {len(rows)} table rows -> {path}")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--series", nargs="+", choices=sorted(SERIES), default=sorted(SERIES))
    ap.add_argument("--out", default="data/consensus")
    ap.add_argument("--deep", action="store_true", help="also click Show More and save <series>_table.csv (about 1,000 rows)")
    add_args(ap)
    args = ap.parse_args()
    out = Path(args.out)
    now = datetime.now(timezone.utc)
    with session(args) as page:
        for i, name in enumerate(args.series):
            if i:
                pause()
            goto(page, BASE + SERIES[name][0])
            save_series(name, occurrences(page), out, now)
            if args.deep:
                page.wait_for_selector(TABLE, timeout=30000)
                load_all(page, "Show More", TABLE + " tbody tr", close_selectors=[SIGNUP_WALL_CLOSE])
                write_table(name, table_rows(page, TABLE), out)


if __name__ == "__main__":
    main()
