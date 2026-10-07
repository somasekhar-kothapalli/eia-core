"""Read Investing.com event-page history through a real Chrome (Playwright over the DevTools protocol).

This does the same job as fetch_investing_history.py but loads each page in an actual Chrome window, the way
a person would, and reads the page's own embedded data (`__NEXT_DATA__`). It parses and saves with the same
code, so outputs are identical (data/consensus/<series>.csv, upcoming_snapshots.csv, raw/*.json).

Two ways to get the browser:
  --launch-chrome   start the installed Google Chrome with a throwaway profile and a DevTools port, then attach.
                    Chrome opens a visible window and is closed at the end. Nothing is downloaded.
  --cdp URL         attach to a Chrome you already started with --remote-debugging-port (and its own
                    --user-data-dir), e.g. --cdp http://localhost:9223

Rules (do not weaken them):
- Ordinary browsing only: no stealth plugins, no automation-flag hiding, no user-agent or fingerprint
  spoofing, no proxies, no CAPTCHA solving.
- One page load per series, a pause between pages, never retried.
- If a page returns a non-200 status or shows a challenge or verification page, the script stops. It does not
  try to get past it. Use the manual copy instead.
- Investing.com's terms were not readable when this was written. Keep the volume small, personal research only.

Usage:  python scripts/fetch_investing_playwright.py --launch-chrome [--series crude_stocks gas_storage ...]
"""
import argparse
import json
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from playwright.sync_api import sync_playwright

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_investing_history import BASE, CHALLENGE, PAUSE_SECONDS, SERIES, save_series  # noqa: E402

CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
]
DEVTOOLS_PORT = 9223  # 9222 is used by the TradingView Desktop connection


def start_chrome(profile_dir):
    exe = next((p for p in CHROME_PATHS if Path(p).exists()), None)
    if not exe:
        sys.exit("STOP: Google Chrome not found. Start Chrome yourself and use --cdp.")
    return subprocess.Popen(
        [exe, f"--remote-debugging-port={DEVTOOLS_PORT}", f"--user-data-dir={profile_dir}",
         "--no-first-run", "--no-default-browser-check", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


def read_occurrences(page, url):
    resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
    status = resp.status if resp else None
    if status != 200:
        sys.exit(f"STOP: {url} answered HTTP {status}. Not retrying and not working around it.")
    title = page.title()
    if CHALLENGE.search(title) or CHALLENGE.search(page.inner_text("body")[:3000]):
        sys.exit(f"STOP: {url} shows a verification page. Not working around it; use the manual copy.")
    raw = page.evaluate("() => { const e = document.getElementById('__NEXT_DATA__'); return e ? e.textContent : null; }")
    if not raw:
        sys.exit("STOP: page layout changed (no __NEXT_DATA__). Update the parser or copy by hand.")
    return json.loads(raw)["props"]["pageProps"]["state"]["economicCalendarEventStore"]["occurrences"]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--series", nargs="+", choices=sorted(SERIES), default=sorted(SERIES))
    ap.add_argument("--out", default="data/consensus")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--launch-chrome", action="store_true")
    mode.add_argument("--cdp", metavar="URL")
    args = ap.parse_args()
    out = Path(args.out)
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")

    proc = tmp = None
    cdp = args.cdp
    if args.launch_chrome:
        tmp = tempfile.TemporaryDirectory(prefix="chrome-eia-")
        proc = start_chrome(tmp.name)
        cdp = f"http://localhost:{DEVTOOLS_PORT}"
        time.sleep(4)
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(cdp)
            ctx = browser.contexts[0] if browser.contexts else browser.new_context()
            page = ctx.new_page()
            for i, name in enumerate(args.series):
                if i:
                    time.sleep(PAUSE_SECONDS)
                occ = read_occurrences(page, BASE + SERIES[name][0])
                save_series(name, occ, out, now, stamp)
            page.close()
    finally:
        if proc:
            proc.terminate()
        if tmp:
            time.sleep(1)
            tmp.cleanup()


if __name__ == "__main__":
    main()
