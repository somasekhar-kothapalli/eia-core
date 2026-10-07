# 01 Strategy Spec: EIA Report Breakout on MCX Options

**Status:** a hypothesis, not a proven system. Rules below are what we would trade and test. Evidence is in `05_evidence.md`; open parameters are in `07_open_items.md`.
**Last revised:** 7 Oct 2026.

**Tags:** ✅ verified · 🔧 rule decided or added in review · ❓ parameter or claim still open (needs data)

---

## 1. Scope

| Item | Decision |
|---|---|
| Catalyst | WPSR (crude, Wednesday) and WNGSR (natural gas, Thursday), both at 10:30 AM ET (exceptions in §2) |
| Instruments | **CRUDEOIL standard** (100 bbl) options on WPSR day. **NATGASMINI** (250 mmBtu) options on WNGSR day. User decision. |
| Account | ₹50,000 (Phase 1 of risk, §8) |
| Position | **1 lot. One trade per report, per instrument.** No re-entry after a stop. No second attempt that day. No trades on other days. |
| Levels | All levels (range, midpoint, pivots, stop, targets, trail) are defined on the **underlying MCX future**. The option is the traded instrument. |
| Parked | **Broker execution** (order types, stops on options, fills, slippage, spreads) is out of scope for now (user decision). See §10. |

## 2. Calendar and timing ✅

- Release time 10:30 AM ET = **8:00 PM IST in US daylight time**, **9:00 PM IST in US standard time**. The switch is Sun 1 Nov 2026 (releases from Wed 4 Nov and Thu 5 Nov are at 9:00 PM IST).
- 🔧 Derive the window start from the ET time each week. Never hardcode 8:00 PM.
- **WPSR holiday delays (EIA 2026): Thursday at 12:00 ET, not 10:30:** 22 Jan, 19 Feb, 28 May, 10 Sep, **15 Oct**, 12 Nov. 12:00 ET = **9:30 PM IST** in daylight time, 10:30 PM IST in standard time.
- **WNGSR exceptions (2026):** Fri 13 Nov 10:30 ET; Wed 25 Nov 12:00 ET. Otherwise Thursday 10:30 ET.
- MCX energy session: Mon–Fri 9:00 AM to **11:30 PM IST in US daylight time** and **11:55 PM IST in standard time** (rule in force from 9 Mar 2026, per broker notices ✅). A 90-minute window after a 12:00 ET release in standard time (10:30 PM IST) runs past the close: truncate at the close.
- Check the EIA schedule pages every week.

**Upcoming**

| Date | Report | Time (IST) | Note |
|---|---|---|---|
| Wed 7 Oct | WPSR | 8:00 PM | |
| Thu 8 Oct | WNGSR | 8:00 PM | |
| **Thu 15 Oct** | WPSR | **9:30 PM** (12:00 ET) | Columbus Day delay. **CRUDEOIL options expire this day.** Use the next-month chain (§7). |
| Thu 15 Oct | WNGSR | 8:00 PM | normal |
| Thu 22 Oct | WNGSR | 8:00 PM | gas options expire Fri 23 Oct |
| Thu 12 Nov | WPSR | 10:30 PM (12:00 ET, standard time) | window truncated at the 11:55 PM close |

## 3. Signal (data bias)

- **Surprise = actual − consensus** (crude: commercial stocks change in mb; gas: Lower 48 net change in Bcf). Build/injection positive, draw/withdrawal negative.
- **Negative surprise = bullish. Positive surprise = bearish.** ✅ Holds in both injection and withdrawal seasons.
- **Consensus protocol 🔧:**
  - Record consensus **before** the release (5 minutes earlier) with source and timestamp. Some sites may overwrite their forecast after the print (Trading Economics showed gas consensus = actual).
  - **Primary source: Investing.com** (user decision). **Cross-check: Trading Economics** (also the only API source).
  - **Sign-disagreement rule:** if primary and cross-check give opposite signs of surprise, or either is zero, the bias is unclear: **no trade.**
- **Threshold X** for "significant" is ❓ and set in **standard-deviation units**. Measured from Investing.com history (Nov 2024 to Sep 2026): the SD of (actual − consensus) is **4.82 mb for crude** (median miss 3.0 mb, 90th percentile 7.7) and **9.39 Bcf for gas** (median 5.0, 90th percentile 13.6). Candidate X = **0.5 SD** (about 2.4 mb crude, 4.7 Bcf gas) ❓, to be chosen before looking at forward results. For gas X must also exceed EIA's own sampling error of about 2 Bcf. Example: 30 Sep crude (+1.622 mb) = 0.34 SD and 1 Oct gas (+1 Bcf) = 0.11 SD: both below 0.5 SD.
- **Conflict flags (secondary, ❓ rule not yet written):** crude: gasoline and distillate surprises (they move crude in the same direction in the literature), Cushing, refinery utilization. Gas: South Central Salt (**parked, left untested by user decision 7 Oct 2026**: no regional gas history downloaded, not part of the rules), stocks vs 5-year average. Only crude/gasoline/distillate and API have a consensus; Cushing and utilization do not.
- **Conflict rule 🔧:** if the data bias and the breakout direction disagree: **no trade.**
- ❓ The data filter may only duplicate what price already shows. Backtest whether it adds edge.

## 4. Levels

**4.1 Opening range and midpoint ✅**
- Window = first 15 minutes after the release. `Range High` / `Range Low` = absolute high/low of the MCX future in the window. `Midpoint = (High + Low) / 2`.
- Use execution-chart candles (three 5-min candles). A separate 15-minute chart is redundant.

**4.2 Execution timeframe 🔧:** default **5-min**. Test variants: 3-min (from the gas source), 15-min (used in most of our tests so far).

**4.3 Floor pivots (default) ✅** from the previous MCX trading day of the same contract (never WTI or Henry Hub; never an expiring contract):
```
P  = (H + L + C) / 3
R1 = 2P − L        S1 = 2P − H
R2 = P + (H − L)   S2 = P − (H − L)
R3 = H + 2(P − L)  S3 = L − 2(H − P)
```
**4.4 Camarilla (test variant) ✅ formulas:** `R/S n = C ± 1.1·(H − L)/{12, 6, 4, 2}` for levels 1–4. R3/S3 are normally reversal levels and R4/S4 breakout levels. No evidence that gas prefers Camarilla.

## 5. Entry and stop

- **Long:** an execution-chart candle **closes above Range High** + bullish bias → buy the selected call. **Short:** candle **closes below Range Low** + bearish bias → buy the selected put. (Close beyond the range; test the stricter "whole body outside".)
- **Entry price** for the hypothesis = **open of the candle after the signal candle, on the underlying.**
- **Stop = Midpoint on the underlying.** Touch vs candle close is ❓ (test both).
- 🔧 **Skip** the trade if reward-to-risk to TP1 < the chosen minimum (default ≥ 1) ❓.
- The stop is always placed and never widened.

## 6. Targets, breakeven, trailing, time stop

With **1 lot there are no partial exits**. Candidate designs to test:
- **E1:** exit all at TP1.
- **E2:** at TP1 move the stop to the **underlying entry level**, then trail the whole lot; TP2 is an optional all-out.
- **E3:** hold to TP2 with the stop at the midpoint; no breakeven move.

**Targets (default):** TP1 = nearest floor-pivot level **beyond the entry price**; TP2 = the next. If none is within reasonable distance, skip. **Alternative targets to test: 1×, 1.5×, 2× the stop distance**, because pivots built from yesterday's range proved far away (`05_evidence.md`).

**Trailing (one engine only) 🔧:** long `new_stop = max(old_stop, previous closed candle low − buffer)`, short `min(old_stop, previous closed candle high + buffer)`. The stop never moves against the position. Buffer in ticks or a fraction of ATR, not "points" ❓. Optional ATR/Chandelier alternative (this is a trailing stop; classic Chandelier is ATR 22 × 3.0).

**Breakeven is not "zero risk" for options** (IV drop, theta, costs, gaps).

**Time stop:** **90 minutes from release, then flat** ❓ (variant T2: exit if there is no progress within 30–45 minutes of entry).

## 7. Option selection (method shared; numbers in the report docs)

- **Select by delta from the live chain, not by strike count.** Rank candidates by `vega ÷ premium` (lower is better), breakeven move `= vega × ΔIV ÷ delta`, volume, theta ÷ premium. Spread is information only while execution is parked.
- **Working zones (from the 6–7 Oct chain snapshots, re-pick each week):** crude calls 8400–8450 and puts 8900–8950 (delta ≈ 0.62–0.65); gas mini calls 290–295 and puts 315–320 (delta ≈ 0.57–0.69). Gas near-ATM wins on % return; ITM wins on breakeven and theta; depends on move size ❓.
- Do **not** combine a delta band with an extrinsic-% cap (they disagree).
- **Expiry selection 🔧:** options expire **two business days before** the futures. Use the nearest expiry with at least **N calendar days** left, otherwise the next month. N = ❓ (suggest 5). Check the chain tool lists the next-month expiry.
- IV facts: ITM options are **not** immune to vega; vega is highest ATM. Gamma peaks ATM and is negligible here. Theta over 90 minutes is small. IV usually peaks before the print and falls after; the real drop is unmeasured ❓.

## 8. Risk (Phase 1, ₹50,000) 🔧

- A 1% cap is **not workable** at this account size (user decision). It is adopted as the account grows.
- **No %-of-equity filter in Phase 1.** One minimum lot sets the size. Every valid signal is taken.
- Risk is an **outcome**: `risk_per_lot = qty × delta × |entry − stop|`; maximum loss = premium. **Record both in ₹ and as % of the account for every trade.**
- **Pause rule (user decision): after 3 losing trades in a row, stop trading and review.**
  - "Loser" = a trade closed at a net loss (stop-out, or time-stop exit below entry).
  - **Count in date order across both instruments, combined (user confirmed 7 Oct 2026).** Crude on Wednesday and gas on Thursday share one streak.
  - A report with no trade neither adds to nor resets the streak. A winning or flat trade resets it.
  - Review before resuming: snapshot log vs actual, stop distance vs risk, any broken rule, data flags (contract roll, wrong release time). Write the review down.
- **Phase 2:** adopt a **2%** then **1%** per-trade cap when the account reaches the thresholds in `04_contracts_and_risk.md`.
- ⚠️ Honest note: one CRUDEOIL standard lot is 79–94% of the account in premium and about 5% of the account in price risk at the median measured stop. The user accepted this for Phase 1.

## 9. Pre-registered test variants (defaults first)

| Dimension | Default | Variants |
|---|---|---|
| Entry style | **B1** breakout after the 15-min range | F1 fade of a failed breakout; P1 pullback to the 50 EMA (ACY) |
| Timeframe | 5-min | 3-min, 15-min |
| Stop | S1 midpoint | S2 opposite range edge; S3 swing high/low of last candles |
| Stop trigger | touch | candle close |
| Exit | E1 | E2, E3 |
| Targets | nearest pivot | 1×, 1.5×, 2× stop distance |
| Pivots | floor | Camarilla |
| Time stop | T1 90 min from release | T2 no-progress 30–45 min |
| Reward-to-risk filter | ≥ 1 | ≥ 1.5, ≥ 2 |

Rule: **fix parameters before looking at results; do not grid-search on small samples.** Forward capture from 7 Oct 2026 is the out-of-sample set.

## 10. Parked: broker execution

Collected so nothing is lost: how stops/targets are placed on MCX options (stops are not triggered by the future's price: alerts, or premium-level conversion `premium_level ≈ entry_premium + delta × (underlying_level − entry_underlying)`); whether SL / SL-M orders are allowed on MCX options; market vs marketable limit vs mid-price limit; time limits for fills; bid-ask spread, slippage and partial fills. Until un-parked, rules are evaluated on underlying price levels.
