# EIA Report Breakout on MCX Options

**Revised:** 7 Oct 2026 (a full rewrite and re-evaluation of the earlier notes, which are kept in `archive/`).
**What this is:** a researched, written-down **hypothesis** for trading the weekly EIA reports with single MCX options: the Weekly Petroleum Status Report (WPSR) for crude on Wednesday and the Weekly Natural Gas Storage Report (WNGSR) for gas on Thursday. We are building the rules, checking every claim, and collecting data. We are **not** trading it yet, and broker execution is out of scope for now.

## Where we stand in one paragraph

The report mechanics, release calendar (including holiday delays), data tables, units, consensus sources, MCX contract specs and option chains are verified or documented. The rules are written ([`01`](docs/01_strategy_spec.md)) and are an **untested hypothesis**: no source we found gave a backtest, and our own first tests (about 15 events per instrument, free data) show **no visible edge and none ruled out**. The literature says most of the price reaction completes within 5–7 minutes, so entering after a 15-minute range is late. **Consensus-versus-actual history is now in** (about 2 years per series from Investing.com, via `scripts/`): typical misses are crude SD 4.8 mb and gas SD 9.4 Bcf. Gas reacts strongly to the surprise on the daily horizon (correlation −0.35); crude's reaction is weak and not significant. The main missing inputs are now the real IV change around releases and more intraday events. Crude risk at ₹50,000 is large (one standard lot is 79–94% of the account in premium and about 5% in price risk at the median stop); gas mini is comfortable (about 0.7%).

## Document map

| File | What it holds |
|---|---|
| [`01_strategy_spec.md`](docs/01_strategy_spec.md) | The rules: scope, calendar, signal, levels, entry, stop, exits, option selection, risk, pre-registered test variants, parked items |
| [`02_wpsr_crude.md`](docs/02_wpsr_crude.md) | WPSR facts: mechanics, data tables, consensus sources, worked example, CRUDEOIL option chain |
| [`03_wngsr_gas.md`](docs/03_wngsr_gas.md) | WNGSR facts: mechanics, regional table, consensus sources, NATGASMINI option chain |
| [`04_contracts_and_risk.md`](docs/04_contracts_and_risk.md) | MCX specs, what one lot costs at ₹50,000, Phase 1 and Phase 2 risk, why percentage-of-premium rules do not fit |
| [`05_evidence.md`](docs/05_evidence.md) | Literature, the external Cushing repo, our three tests and what they show; known vs unknown |
| [`06_data_and_capture.md`](docs/06_data_and_capture.md) | Files in `data/` and `schemas/`, data-quality rules, forward capture routine, historical data options |
| [`07_open_items.md`](docs/07_open_items.md) | Next 24 hours, inputs needed, rules still to set, unverified items, parked items |
| [`08_corrections_log.md`](docs/08_corrections_log.md) | Every source claim checked (74 rows), grouped by topic, plus my own errors |
| [`snapshot_log.md`](docs/snapshot_log.md) | The fill-in template for each release (consensus, actuals, price, IV) |
| [`data/`](data/), [`schemas/`](schemas/) | Raw bars, daily bars, event calendar, free EIA history, JSON schemas |
| [`archive/`](archive/) | The earlier versions of the notes (untouched) |

## Decisions made (by the user)

| Date | Decision |
|---|---|
| 6–7 Oct 2026 | Account ₹50,000. **CRUDEOIL standard** on Wednesdays (WPSR), **NATGASMINI** on Thursdays (WNGSR). **1 lot, 1 trade per report.** |
| 7 Oct | Investing.com is the primary consensus source; Trading Economics is the cross-check; sign-disagreement means no trade |
| 7 Oct | Broker execution parked. All rules are on the underlying MCX future |
| 7 Oct | No 1% cap in Phase 1 (₹50,000); adopt 2% then 1% as the account grows |
| 7 Oct | **Pause and review after 3 losing trades in a row, counted across both instruments combined** |
| 7 Oct | Databento skipped; free EIA history and chart bars used instead; capture forward each week |
| 7 Oct | Data stored as **CSV** (source of truth); consensus history copied by hand into `data/consensus/` |

## Headline findings

1. **Timing is easy to get wrong:** 8:00 PM IST only in US daylight time; holiday-delayed WPSRs come out **Thursday 12:00 ET** (9:30 PM IST), including **Thu 15 Oct**, the day the CRUDEOIL options expire.
2. **The literature** (Linn et al., 2003–2017): the reaction completes within about 5–7 minutes; no next-day drift. A different study says it reverts within about 25 minutes. Continuation after the first 15 minutes is unproven.
3. **Our tests:** continuation is 55–64% same-sign (t 0.7–1.8, not significant); every exit design is within noise of zero; pivot targets from yesterday's range are too far for a 90-minute window.
4. **Crude stops are large** (median 43 points, up to 91.5), gas mini stops small (median 2.2).
5. **Free data cannot replace consensus:** a de-seasonalised z-score fails the same-day sanity check for gas and for crude after 2015.
6. Many claims in the source material were wrong or inconsistent (about 50 of 74 checked rows are flagged); see [`docs/08_corrections_log.md`](docs/08_corrections_log.md).

## Conventions

- **Tags:** ✅ verified · ⚠️ wrong or misleading in a source and corrected · 🔧 rule decided or added in review · ❓ open or unverified.
- **Units and signs:** crude stocks in mb (or kb), gas in Bcf; build/injection positive, draw/withdrawal negative; surprise = actual − consensus (negative = bullish).
- **Time:** release 10:30 AM ET = 8:00 PM IST (daylight) or 9:00 PM IST (standard). Data files use UTC.
- **Evidence labels:** "read" = a source was opened and read; "snippet" = only a search summary.
- **Next steps:** [`docs/07_open_items.md`](docs/07_open_items.md).
