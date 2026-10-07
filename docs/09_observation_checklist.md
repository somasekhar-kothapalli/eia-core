# 09 Observation Checklist: WPSR Wed 7 Oct and WNGSR Thu 8 Oct 2026

**Mode: observe and verify, do not trade.** Two reports cannot show an edge. What they can do is check that our rules, data feeds, timings and assumptions work in real time, and show where the spec is vague or wrong. Data goes in `snapshot_log.md` (Blocks A–E) and, after review, in a `release_event` record (`schemas/`). Rules: `01_strategy_spec.md`. Tags: ✅ verified · 🔧 decided · ❓ open.

**Guardrails (do not skip)**
- No parameter is changed from one report. Two reports may fix **wording and mechanics** (a rule that was ambiguous, a data feed that failed), never thresholds.
- X is chosen after the 7 Oct report **from the 15-year history, not from today's outcome** (decision 7 Oct 2026, `01_strategy_spec.md` §3). Log every release at 0.25, 0.5 and 1.0 SD.
- Everything is **paper**: entries, stops, targets and option premiums are recorded as if taken, with no order placed. Broker execution stays parked.
- Keep **Claude Code and TradingView Desktop running** from before 7:30 PM IST to after 9:30 PM IST. Chart on `MCX:CRUDEOIL1!`, 5-minute, with "Pivot points standard" and "MCX Option Chain + Levels" both visible.

## 1. What we expect, and what would change our mind

| # | Expectation (from evidence) | What the two reports can say | Would matter if |
|---|---|---|---|
| H1 | Price reacts within about 5–7 minutes and does not revert (Linn et al.) | How much of the 90-minute move is already in at +5, +15, +30 min | Most of the move is done before the 8:15 PM range closes: B1 breakout is late (favours F1 or a shorter range) |
| H2 | The 15-minute range grows with the size of the surprise (R5) | Range width vs surprise in SD | Range far above the 43-pt median stop: risk too big for one lot |
| H3 | IV falls after the print; size unknown (chain ATM IV 52.0% before the 7 Oct print) | ATM IV and straddle at T−5, T+5, T+15, T+30 | Drop is small: IV protection is a non-issue; large and persistent: delta choice matters more |
| H4 | Pivots from yesterday's range are far or badly placed (R1 8,752 is only about 30 pts above 8,723) | Distance to TP1/TP2 vs the stop; whether R:R to TP1 passes the skip rule | Pivot targets mostly skipped: switch the default to 1× / 1.5× / 2× the stop |
| H5 | Investing keeps its forecast through the print; Trading Economics may overwrite (1 Oct gas) | Forecast at T−5 vs T+30 on both sites | A site changes it: that site can only be a pre-release source |
| H6 | History forecasts are backfilled, not pre-release | T−5 snapshot vs the same row in the history table fetched later | Differences: the 15-year consensus is noisier than assumed |
| H7 | Gasoline and distillate surprises move crude the same way (R6); API (Tuesday) hints at the EIA direction | Do they agree with the crude surprise and with price today? | Conflict rule fires on a real example |
| H8 | About −0.27% (crude) per SD of surprise, about 24 points per SD | One calibration point (surprise in SD vs the move at +15 min) | Never a conclusion from one point, only a sanity check |

## 2. Wed 7 Oct (WPSR, CRUDEOIL), times in IST

**Today's reference numbers.** Release 8:00 PM IST (10:30 ET, normal schedule). Investing forecast **+1.9 mb**; previous +0.922. Crude SD of surprise 4.82 mb. Qualifying actuals if X were: 0.25 SD (±1.2) → ≤ +0.7 or ≥ +3.1; **0.5 SD (±2.4) → ≤ −0.5 or ≥ +4.3**; 1.0 SD (±4.8) → ≤ −2.9 or ≥ +6.7. Previous day 6 Oct: PDH 8,694, PDL 8,388, PDC 8,634. Pivots: S2 8,264 · S1 8,446 · P 8,570 · R1 8,752 · R2 8,876. Chain expiry 15 Oct (DTE 8.3, passes N = 5). Candidate strikes if triggered: 8500 call, 9000 put (re-pick from the live chain).

### Before 7:30 PM: setup
- [ ] TradingView Desktop connected (`tv_health_check`), chart on CRUDEOIL1!, 5-min, both indicators visible
- [ ] EIA WPSR schedule page: no delay today (☐ normal 10:30 ET)
- [ ] Previous day volume vs 5-day median ≥ 50% (data-quality rule), and the contract is not expiring
- [ ] Any pop-up on TradingView or the browser closed (sign-up wall, dialogs)
- [ ] Note the `Missing x/34` and `Stale n/34` figures of the chain table (data quality). A leg marked `*` has no volume today, so its price and IV are old; a `STALE CHAIN` warning means do not pick a strike from it (needs the updated indicator, `tradingview/mcx_option_chain_levels.pine`)

### 7:55 PM: T−5 snapshot (Block A, Block E baseline)
- [ ] Claude: run `python scripts/fetch_investing.py --launch-chrome --series crude_stocks api_crude gasoline distillates`; check the new rows in `upcoming_snapshots.csv` carry a T−5 timestamp
- [ ] **You**: copy the Trading Economics consensus (crude, gasoline, distillates, API) with the time
- [ ] Claude: read the chain table (`data_get_pine_tables`): futures, ATM, ATM IV, straddle, implied range, candidate rows (delta, vega, theta, LTP, volume)
- [ ] Claude: record PDH/PDL/PDC and pivots from the chart

### 8:00 PM: the print (Block B)
- [ ] Claude: read actuals from the EIA page (crude, gasoline, distillates, utilization, Cushing); note the time they were readable
- [ ] Compute surprise vs Investing and vs Trading Economics, in mb and SD; same sign? (sign rule); qualifies at 0.25 / 0.5 / 1.0 SD?
- [ ] Compare with API (Tuesday −2.09 actual): same direction as the EIA actual?
- [ ] Note the time of the first large 5-minute bar (reaction speed)

### 8:00–8:15 PM: opening range (no trade)
- [ ] Chain read at **T+5 (8:05)** and **T+15 (8:15)** (Block E): ATM IV, straddle, candidate rows
- [ ] At the 8:15 close: Range High, Low, Midpoint (Block D); stop distance in points; distance to TP1/TP2 (pivots and 1×/1.5×/2×)

### 8:15–9:30 PM: observe the rules (paper)
- [ ] First 5-minute close beyond the range: time, direction, signal candle
- [ ] Bias vs breakout: agree? (conflict rule) · reward-to-risk to TP1 passes? (skip rule)
- [ ] Paper entry = open of the next candle; the option the chain would pick **at that moment** (strike, delta, premium, volume)
- [ ] Track: stop (touch and close variants), TP1, TP2, trail (previous-candle low/high), time stop 9:30 PM
- [ ] Chain read **at entry** and **at +30 (8:30)**: premium vs delta × underlying move (does the option behave as the table says?)

### 8:30 PM: source behavior (Block C)
- [ ] Investing forecast now vs T−5; Trading Economics consensus now vs T−5

### After 9:30 PM: close-out
- [ ] Claude: capture the 5-min bars 7:30–9:30 PM into `data/mcx/`; save the volume flags
- [ ] Outcome of each exit design: E1, E2, E3; stop touch vs close; targets (pivot, 1×, 1.5×, 2×) in points and in ₹/% of ₹50,000 for the chosen option
- [ ] Share of the 90-minute move reached at +5, +15, +30, +90 min (H1)
- [ ] Fill a `release_event` record (`live` → `reviewed`) and the Running summary row in `snapshot_log.md`
- [ ] **Rule-friction list:** anything the spec did not decide or decided unclearly (write it down, do not fix it live)
- [ ] Commit the data and logs

## 3. Thu 8 Oct (WNGSR, NATGASMINI), same flow

- **Release** 8:00 PM IST, 10:30 ET. Investing forecast **+79 Bcf** (previous +64). Gas SD 9.39 Bcf. Qualifying at X: 0.25 SD (±2.3) → ≤ 76.7 or ≥ 81.3; **0.5 SD (±4.7) → ≤ 74.3 or ≥ 83.7**; 1.0 SD (±9.4) → ≤ 69.6 or ≥ 88.4. EIA's own sampling error is about 2 Bcf, so a surprise under 2 Bcf is noise.
- Steps differ only in: `--series gas_storage`; chain **NATGASMINI** (expiry 23 Oct; working zone near calls 290–295 and puts 315–320, re-pick live); chain table must be switched to the gas contract; consensus sources Investing and Trading Economics (Bcf).
- Extra checks: **does the mini chain read cleanly from the table** (strike step 5, volume, delta)? Price reaction on gas may continue into the next day in the daily data (day 1), so also note the **Friday morning** move for the record.
- Gas is smaller in points (median stop about 2.2 pts, about 0.7% of the account per lot): record risk in ₹ and %.

## 4. Small things this week can verify or fix

| Item | How we know | Fix, if it fails |
|---|---|---|
| The T−5 routine runs end to end (script, hand-copy, chain read) | Rows exist with the right timestamps | Adjust the routine and `snapshot_log.md` |
| The chain table is readable at every step (T−5, +5, +15, entry, +30) | Table returns rows with `Missing 0/34`-style quality | Note stale quotes; use screenshots as backup |
| The next-month expiry can be shown by the chain tool (open item for Thu 15 Oct, 9:30 PM IST) | Check the indicator's settings tonight | Plan the 15 Oct capture differently |
| Release time and EIA readability (the time the actual is visible) | Compare the first bar reaction with 10:30 ET | Update the window start if different |
| The three exit designs and stop variants can be evaluated from saved bars | Close-out checklist completes | Fix the bar-capture steps |
| The rule book is complete | Rule-friction list | Reword the spec (not the numbers) |

## 5. After both reports

1. Update `snapshot_log.md`, `data/mcx/` and the `release_event` records; commit.
2. Write a short review: what worked, what failed, what was unclear (rule-friction list), and which data feeds need a fix.
3. Decide X from the 15-year history (separately from the outcome), then set the same X for forward use.
4. Next release: **Thu 15 Oct, 9:30 PM IST (WPSR, delayed to 12:00 ET)**; crude options expire that day, so use the next-month chain.
