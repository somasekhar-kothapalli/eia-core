"""Fetch EIA / API consensus history from Investing.com event pages into CSV.

How it works: each event page (a Next.js page) already contains its recent history in the server-rendered
JSON (`__NEXT_DATA__` -> economicCalendarEventStore.occurrences): about 100 releases with actual, forecast,
previous and the exact UTC release time, plus the next upcoming release. One plain GET per page is enough.

Rules this script follows (do not weaken them):
- One request per page, a pause between pages, a descriptive User-Agent, a timeout.
- It stops on any non-200 answer or a challenge page. It never retries, rotates headers, uses proxies or
  tries to get around a block.
- Only pages the user listed are fetched. robots.txt allowed /economic-calendar/ when this was written;
  the site's terms were not readable then, so keep the volume small and use for personal research only.

Outputs (default folder data/consensus/):
- <series>.csv                 completed releases. Columns: release_date, release_time_gmt, actual, forecast,
                               previous, unit, occurrence_id. The forecast is the value on the page at fetch
                               time, i.e. a BACKFILLED consensus (it may differ from the pre-release value).
- upcoming_snapshots.csv       append-only: the upcoming release's forecast with the fetch time. Run it
                               5 minutes before a release and the row is a true PRE-RELEASE snapshot.
- raw/<series>_<UTC stamp>.json  the occurrences exactly as received (provenance).

Usage:  python scripts/fetch_investing_history.py [--series crude_stocks gas_storage ...] [--out data/consensus]
"""
import argparse
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://in.investing.com/economic-calendar/"
SERIES = {
    "crude_stocks": ("eia-crude-oil-inventories-75", "EIA crude oil inventories (commercial)"),
    "api_crude": ("api-weekly-crude-stock-656", "API weekly crude oil stock"),
    "gas_storage": ("natural-gas-storage-386", "EIA natural gas storage (net change)"),
    "gasoline": ("gasoline-inventories-485", "EIA gasoline inventories"),
    "distillates": ("eia-weekly-distillates-stocks-917", "EIA distillates stocks"),
}
USER_AGENT = "eia-research-script/1.0 (personal research, low volume)"
PAUSE_SECONDS = 4
FIELDS = ["release_date", "release_time_gmt", "actual", "forecast", "previous", "unit", "occurrence_id"]
CHALLENGE = re.compile(r"Just a moment|cf-chl-|Attention Required|Verify you are human", re.I)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept-Language": "en-US,en;q=0.9"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            body = r.read().decode("utf-8", "replace")
            status = r.status
    except urllib.error.HTTPError as e:
        sys.exit(f"STOP: {url} answered HTTP {e.code}. Not retrying and not working around it.")
    except urllib.error.URLError as e:
        sys.exit(f"STOP: could not reach {url}: {e.reason}")
    if status != 200:
        sys.exit(f"STOP: {url} answered HTTP {status}.")
    if CHALLENGE.search(body[:20000]):
        sys.exit(f"STOP: {url} returned a challenge page. Not working around it; use the manual copy instead.")
    return body


def occurrences(html):
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if not m:
        sys.exit("STOP: page layout changed (no __NEXT_DATA__). Update the parser or copy by hand.")
    state = json.loads(m.group(1))["props"]["pageProps"]["state"]["economicCalendarEventStore"]
    return state["occurrences"]


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


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        for r in sorted(rows, key=lambda r: (r["release_date"], r["release_time_gmt"])):
            w.writerow({k: ("" if r[k] is None else r[k]) for k in FIELDS})


def save_series(name, occ, out, now, stamp):
    """Write raw JSON, the completed-rows CSV and (append-only) the upcoming snapshot for one series."""
    label = SERIES[name][1]
    (out / "raw").mkdir(parents=True, exist_ok=True)
    (out / "raw" / f"{name}_{stamp}.json").write_text(json.dumps(occ), encoding="utf-8")
    done = [row(o) for o in occ if o.get("actual") is not None]
    upcoming = [row(o) for o in occ if o.get("actual") is None]
    write_csv(out / f"{name}.csv", done)
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


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--series", nargs="+", choices=sorted(SERIES), default=sorted(SERIES))
    ap.add_argument("--out", default="data/consensus")
    args = ap.parse_args()
    out = Path(args.out)
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    for i, name in enumerate(args.series):
        if i:
            time.sleep(PAUSE_SECONDS)
        save_series(name, occurrences(fetch(BASE + SERIES[name][0])), out, now, stamp)


if __name__ == "__main__":
    main()
