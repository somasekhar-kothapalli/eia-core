"""Reusable, site-independent helpers for reading pages in a real Chrome (Playwright over the DevTools protocol).

Used by fetch_investing.py; nothing here knows about any particular website.

    from browser import session, goto, next_data, load_all, table_rows, add_args

    ap = argparse.ArgumentParser(); add_args(ap)
    with session(args) as page:
        goto(page, url)                       # stops on a non-200 answer or a verification page
        data = next_data(page)                # Next.js sites: the page's embedded JSON
        load_all(page, "Show More", rows_selector="table tbody tr", close_selectors=["#overlay .close"])
        rows = table_rows(page, "table")

Rules (do not weaken them):
- Ordinary browsing only: a visible, installed Chrome with a throwaway profile. No stealth plugins, no
  automation-flag hiding, no user-agent or fingerprint spoofing, no proxies, no CAPTCHA solving.
- A non-200 status or a verification page stops the program (SystemExit). It is never retried or bypassed.
- Sign-up / cookie style overlays may be declined with their own close button (close_selectors); nothing else is dismissed.
- Keep the volume low: one load per page, a pause between pages (pause()), personal research only.
"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from pathlib import Path

from playwright.sync_api import TimeoutError as PlaywrightTimeout, sync_playwright

DEVTOOLS_PORT = 9223  # 9222 is used by the TradingView Desktop connection
PAUSE_SECONDS = 4
CHALLENGE = re.compile(r"Just a moment|cf-chl-|Attention Required|Verify you are human", re.I)
CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]


def add_args(ap):
    """Add --launch-chrome / --cdp URL (one is required) to an argparse parser."""
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--launch-chrome", action="store_true",
                      help="start the installed Chrome with a throwaway profile and a DevTools port, then attach (nothing is downloaded)")
    mode.add_argument("--cdp", metavar="URL", help="attach to a Chrome you started with --remote-debugging-port, e.g. http://localhost:9223")


def start_chrome(profile_dir, port=DEVTOOLS_PORT):
    exe = next((p for p in CHROME_PATHS if Path(p).exists()), None) or shutil.which("google-chrome") or shutil.which("chrome")
    if not exe:
        sys.exit("STOP: Google Chrome not found. Start Chrome yourself and use --cdp.")
    return subprocess.Popen(
        [exe, f"--remote-debugging-port={port}", f"--user-data-dir={profile_dir}",
         "--no-first-run", "--no-default-browser-check", "about:blank"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )


@contextmanager
def session(args):
    """Yield one Playwright page in a real Chrome; closes the page (and Chrome, if launched here) afterwards."""
    proc = tmp = None
    cdp = args.cdp
    if args.launch_chrome:
        tmp = tempfile.TemporaryDirectory(prefix="chrome-scrape-")
        proc = start_chrome(tmp.name)
        cdp = f"http://localhost:{DEVTOOLS_PORT}"
        time.sleep(4)
    try:
        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(cdp)
            ctx = browser.contexts[0] if browser.contexts else browser.new_context()
            page = ctx.new_page()
            try:
                yield page
            finally:
                page.close()
    finally:
        if proc:
            proc.terminate()
        if tmp:
            time.sleep(1)
            tmp.cleanup()


def pause(seconds=PAUSE_SECONDS):
    time.sleep(seconds)


def goto(page, url):
    """Load a page. Stops (SystemExit) on a non-200 answer or a verification page; never retries."""
    resp = page.goto(url, wait_until="domcontentloaded", timeout=45000)
    status = resp.status if resp else None
    if status != 200:
        sys.exit(f"STOP: {url} answered HTTP {status}. Not retrying and not working around it.")
    if CHALLENGE.search(page.title()) or CHALLENGE.search(page.inner_text("body")[:3000]):
        sys.exit(f"STOP: {url} shows a verification page. Not working around it; copy by hand instead.")


def next_data(page):
    """Parsed `__NEXT_DATA__` JSON of a Next.js page (stops if the page has none)."""
    raw = page.evaluate("() => { const e = document.getElementById('__NEXT_DATA__'); return e ? e.textContent : null; }")
    if not raw:
        sys.exit("STOP: page layout changed (no __NEXT_DATA__). Update the parser or copy by hand.")
    return json.loads(raw)


def load_all(page, button_text, rows_selector, max_clicks=150, pause_s=1.5, close_selectors=()):
    """Click a "load more" control until it disappears or the row count stops growing; return the row count.

    close_selectors: close buttons of overlays that may cover the page (declined before each click).
    If a normal click times out, the click event is sent straight to the element.
    """
    rows = page.locator(rows_selector)
    for _ in range(max_clicks):
        more = page.get_by_text(button_text, exact=True)
        if not more.count():
            break
        for sel in close_selectors:
            close = page.locator(sel)
            if close.count():
                close.first.dispatch_event("click")
                time.sleep(1)
        before = rows.count()
        try:
            more.first.click(timeout=4000)
        except PlaywrightTimeout:
            page.keyboard.press("Escape")
            more.first.dispatch_event("click")
        time.sleep(pause_s)
        if rows.count() == before:
            break
    return rows.count()


def table_rows(page, table_selector):
    """Text of every body row's cells in a table: [[cell, ...], ...]."""
    return page.evaluate("sel => [...document.querySelectorAll(sel + ' tbody tr')]"
                         ".map(r => [...r.querySelectorAll('td')].map(c => c.textContent.trim()))", table_selector)
