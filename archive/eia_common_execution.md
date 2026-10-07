# EIA Reports → MCX Options: Common Execution Framework

Applies to both reports. Asset files keep only what is specific to the report and the instrument:
- `eia_wpsr_mcx_crude.md`: WPSR (Wed) → MCX Crude Oil
- `eia_wngsr_mcx_natgas.md`: WNGSR (Thu) → MCX Natural Gas

**Principle:** every level (range, midpoint, pivots, stop, targets, trail) is defined on the **underlying future**. The option is the instrument that gets traded. The rules are identical for both assets. Only lot size, tick size and the numeric levels differ.

**Scope of the hypothesis:** signal, levels and exit rules on the **underlying**, plus option choice from the chain. **Broker execution is parked** (see §12): order types, stops on options, fills, slippage.

**Tags:** ✅ verified · ⚠️ corrected from source · 🔧 rule added or tightened in review · ❓ unverified, needs backtest or contract-spec check

---

## 1. Asset Parameters

Lot sizes from the user. Other values from broker and news pages (Zerodha, Sharekhan, Fyers, ICICI Direct, Angel One) and the two chain screenshots. The official MCX page returned 403 to us, so an official check is still pending ❓. The values agree across sources.

| Contract | Qty per lot | Futures tick | ₹ per futures tick per lot | ₹ per 1-pt move per lot | Options | Strike step | Option tick | Strikes listed |
|---|---|---|---|---|---|---|---|---|
| CRUDEOIL | 100 bbl | ₹1 | ₹100 | ₹100 | ✅ | ₹50 ✅ (chain) | ₹0.05 ❓ | ❓ |
| CRUDEOILM | 10 bbl | ₹1 | ₹10 | ₹10 | ✅ since 23 Apr 2024 | ₹50 | ₹0.05 | 25 ITM + 25 OTM + 1 near |
| NATURALGAS | 1,250 mmBtu | ₹0.10 | ₹125 | ₹1,250 | ✅ | ₹5 ✅ (chain) | ₹0.05 | 15 ITM + 15 OTM + 1 near |
| NATGASMINI | 250 mmBtu | ₹0.10 | ₹25 | ₹250 | ✅ since 23 Apr 2024 | ₹5 | ₹0.05 | 15 ITM + 15 OTM + 1 near |

**Account: ₹50,000 (user, 7 Oct 2026). Contracts (final, user decision): CRUDEOIL standard (100 bbl) on Wednesdays for WPSR, NATGASMINI (250 mmBtu) on Thursdays for WNGSR.** ⚠️ One CRUDEOIL standard lot is 79–94% of the account in premium and about 3% in risk at a 25-pt stop (§11). The user has accepted this for Phase 1. CRUDEOILM and NATURALGAS standard are not used.

**Trading calendar and trade count:** crude only on the WPSR day (Wednesday), gas only on the WNGSR day (Thursday). **One trade per report, per instrument.** That one trade is taken after the post-report analysis (the 15-minute range, the data bias and the breakout close). If it is stopped out, or if no valid signal appears before the time stop, there is no second attempt that day. No trades on other days under this hypothesis.

- ✅ **All four contracts have options.** Options are European style.
- ✅ **Option expiry = two business days before the underlying futures expiry** (stated for CRUDEOILM, NATGASMINI and NATURALGAS; the user's paste says the same for crude).
  - Chain headers: crude options 15 Oct 2026, gas options 23 Oct 2026.
  - Inferred futures expiry: crude Mon 19 Oct (inside the "16th–20th" range stated by the paste) and gas Tue 27 Oct ❓ inferred.
- ⚠️ **In-the-money options held to expiry convert into futures** (claimed in the paste, not verified here ❓). The "margin needed before 7 PM" is broker-specific ❓. Not relevant to an intraday hold, but relevant to expiry selection (§4).
- ❓ The paste's "mini spreads can be wider" is unsupported. Spread and order handling are parked (§12). The paste's limit-spread / calendar-spread offer does not apply: we trade single options.
- Per-lot P&L on the option ≈ `qty × delta × underlying move`.

## 2. Timing (both reports)

- Release 10:30 AM ET = **8:00 PM IST in US daylight time**, **9:00 PM IST in US standard time** ✅. The switch is Sun 1 Nov 2026. WPSR from Wed 4 Nov and WNGSR from Thu 5 Nov are at 9:00 PM IST.
- ✅ **MCX trading hours (energy):** Mon–Fri 9:00 AM to **11:30 PM IST during US daylight time** (2nd Sunday of March to 1st Sunday of November) and to **11:55 PM IST in US standard time** (rule in force from 9 Mar 2026, per broker notices). A 90-minute window after the release ends at 9:30 PM (EDT) or 10:30 PM (EST), well inside the session either way.
- ✅ **Schedule exceptions (EIA, 2026).** **WPSR holiday delays: Thursday at 12:00 ET (not 10:30)**: 22 Jan, 19 Feb, 28 May, 10 Sep, **15 Oct**, 12 Nov. 12:00 ET = **9:30 PM IST in US daylight time**, 10:30 PM IST in standard time. **WNGSR exceptions:** Fri 13 Nov at 10:30 ET and Wed 25 Nov at 12:00 ET. All other WNGSR releases are Thursday 10:30 ET. Use the EIA schedule pages each time.
- ⚠️ **Next WPSR is Thu 15 Oct, 12:00 ET = 9:30 PM IST. The CRUDEOIL options expire that same day** (15 Oct). Under the expiry-selection rule use the next-month crude chain. The gas report that day is normal (Thu 15 Oct, 8:00 PM IST).
- 🔧 In standard time (from 4 Nov) a 12:00 ET release is 10:30 PM IST and a 90-minute window would pass the 11:55 PM IST close. Truncate the window at the session close.
- 🔧 Derive the window start from 10:30 ET each week. Never hardcode 8:00 PM. Holiday weeks can shift either report.

## 3. Opening Range, Midpoint, Pivots

**3.1 Opening range**
- Window = the first 15 minutes after the release. `Range High` / `Range Low` = absolute high / low of the MCX future in the window.
- `Midpoint = (Range High + Range Low) / 2` ✅
- ⚠️ A separate "15-min chart" is redundant. Build the range from the execution-chart candles (three 5-min candles, or five 3-min candles).
- ❓ "Falling back through the midpoint = momentum failed" is a heuristic, not an established rule.
- Manual definition: (1) chart in IST, MCX current-month future. (2) After the window closes, read the highest high and lowest low. (3) Average them and draw a horizontal ray. Do not use opens or closes.

**3.2 Execution timeframe**
- 🔧 Default **5-min** for both assets (the user's rules are the same for both). The gas source's 3-min chart is a **test variant** ❓ (faster reaction, more noise).

**3.3 Floor pivots (default for both)** ✅ standard formulas
```
P  = (H + L + C) / 3
R1 = 2P − L        S1 = 2P − H
R2 = P + (H − L)   S2 = P − (H − L)
R3 = H + 2(P − L)  S3 = L − 2(H − P)
```
- 🔧 Inputs: previous MCX trading day, same current-month contract (never WTI or Henry Hub). Plot before the release.
- TradingView: "Pivot Points Standard", Type = Traditional, Timeframe = Daily. ❓ Confirm the daily bar matches the MCX trading day and the levels equal a hand calculation. Otherwise draw by hand.

**3.4 Camarilla pivots (test variant, from the gas source)** ✅ formulas
```
Range = H − L
R1 = C + 1.1·Range/12   S1 = C − 1.1·Range/12
R2 = C + 1.1·Range/6    S2 = C − 1.1·Range/6
R3 = C + 1.1·Range/4    S3 = C − 1.1·Range/4
R4 = C + 1.1·Range/2    S4 = C − 1.1·Range/2
```
- R3/S3 sit 0.275 × Range from the previous close; R4/S4 sit 0.55 × Range ✅ arithmetic. The "P" in the gas source is not part of Camarilla.
- ⚠️ Standard use treats R3/S3 as **reversal** levels and R4/S4 as **breakout** levels. Using R3 and R4 as profit targets is a design choice.
- ❓ "Crude respects floor pivots; gas respects Camarilla" has no evidence. 🔧 Test both pivot types on both assets.

## 4. Option Selection (method shared, numbers asset-specific)

- IV crush is real ✅. ⚠️ IV usually peaks *before* the print and falls *after*. It does not "spike at release then collapse". The size of the drop is ❓. Measure it.
- ⚠️ Vega is highest ATM. A deep-ITM option has lower vega but not zero. The benefit is a smaller **percentage** loss on a larger premium. ITM is **not** "shielded" and delta 0.70 is **not** a "synthetic future".
- ⚠️ Gamma peaks ATM. On the crude chain it added only ≈ ₹0.4 on a 40-pt move. Ignore it.
- ⚠️ Theta is small over a 90-minute hold (≈ ₹15/day on the crude chain).
- 🔧 **Pick by delta from the live chain, not by strike count.** Rank candidates by: `vega ÷ premium` (lower is better), breakeven move `= vega × ΔIV ÷ delta`, volume, and bid-ask spread as information only (execution is parked, §12). Skip strikes with wide spreads.
- 🔧 **Expiry selection:** options expire two business days before futures, and theta and gamma rise sharply near expiry. Next releases that fall close to expiry: WPSR Wed 14 Oct (crude options expire Thu 15 Oct) and WNGSR Thu 22 Oct (gas options expire Fri 23 Oct). Rule: use the **nearest expiry with at least N calendar days left**, otherwise the next month. N = ❓ (e.g. 5), to be tested. Check that the chain tool offers the next-month expiry.
- 🔧 Do not combine a delta band with an extrinsic-% cap. They disagree (crude chain: delta 0.72 had ≈ 25% extrinsic).
- The crude chain analysis (delta 0.60–0.65 zone) is in the crude file. The gas equivalent needs a MCX NATURALGAS chain screenshot.

## 5. Signal (asset files define it)

- Each report has its own signal vs consensus (crude stocks, gas net change). Both: **bullish surprise = lower stocks / smaller build than consensus**. Surprise = actual − consensus.
- 🔧 Conflict rule: data bias and breakout direction disagree = **no trade**.
- 🔧 Threshold `X` for "significant" is ❓ from backtest.
- 🔧 **Consensus capture protocol** (both reports):
  - Record the consensus **before** the release (e.g. 5 minutes before 10:30 ET), with the source name and a timestamp. Some sites may overwrite the forecast after the print (Trading Economics showed gas consensus = actual) ❓.
  - One **primary** source per data point. A second source is a cross-check only.
  - **Sign-disagreement rule:** if the primary and the cross-check give opposite signs of surprise (or one gives zero), the bias is unclear: **no trade**. Example: gas 1 Oct, Investing +1 vs Trading Economics 0 would have been a no-trade.
  - Primary source = **Investing.com** (user decision, 7 Oct 2026). Trading Economics = cross-check, and the only source for API. Capture in `eia_snapshot_log.md`. ❓ Revisit after a few weeks of side-by-side snapshots.

## 6. Entry

- Long: execution-chart candle **closes above Range High** + bullish bias. Buy the selected call.
- Short: candle **closes below Range Low** + bearish bias. Buy the selected put.
- ⚠️ "Body fully outside" vs "closes beyond" differ in the sources. Adopt **close beyond the range** ❓ (test the stricter version).
- Entry price for the hypothesis = the **open of the candle after the signal candle, on the underlying**. Fill mechanics are parked (§12).

## 7. Stop Loss

- Initial SL = Midpoint on the **underlying** ✅ formula.
- ⚠️ "Institutional order flow failed" is narrative ❓. Treat the midpoint as a rule to backtest.
- ⚠️ "Delta cushions the downside" is misleading. 0.60 delta passes through 60% of the move (0.60 × 20 = 12 ✅ arithmetic). That is price only. IV drop, spread and slippage add to it. Real loss = `lots × qty × (delta × distance + slippage + IV effect)`.
- ❓ The distance to the midpoint is at least half the range plus the extension. Any "20 points" is illustrative.
- ❓ **Touch vs candle close.** Intrabar touches in the first hour after a print cause whipsaw, especially in gas (the source itself says gas has violent wicks, yet it stops out on a touch). Backtest both.
- 🔧 **Skip** if `entry − SL > max risk` (§11) or if reward-to-risk to TP1 < 1.

## 8. Targets and Scaling

- Long: TP1 = R1, TP2 = R2. Short: TP1 = S1, TP2 = S2 (floor pivots).
- ⚠️ "Volatility-adjusted targets" is wrong. Pivots use **yesterday's range**. Only an ATR trail is volatility-based.
- ❓ "News breakouts systematically reach pivots" has no evidence. Hypothesis.
- 🔧 **TP1 = nearest level beyond the entry price.** If price is already past R1/S1 at entry, TP1 = R2/S2 and TP2 = R3/S3. Skip if no level is within reasonable distance. For Camarilla, same rule (R3 → R4 → none: trail-only or skip).
- 🔧 **Position = 1 lot, 1 trade per report** (user rule). No partial exits are possible, so the 60/40 scaling in the sources does not apply. The exit is one decision for the whole lot. Candidates to backtest:
  - **E1:** exit all at TP1.
  - **E2:** at TP1 move the stop to breakeven (§9), then trail the whole lot (§10). TP2 is an optional all-out.
  - **E3:** hold to TP2 with the stop at the midpoint. No breakeven move.
- Break-even math ✅ (underlying points, ignoring costs and delta): risk R = 25, TP1 distance A = 30.
  - **E1:** win +30, loss −25. Break-even win rate = `R / (R + A)` = 25 / 55 ≈ **45%**.
  - **E2:** a trade that reaches TP1 and then stops at breakeven earns ≈ 0, not +18 as in the old 60/40 split. Winners must run to TP2 or beyond. The break-even win rate is higher than E1's and needs the backtest. ❓
- ⚠️ "TP1 locks profitability" no longer holds. With 1 lot nothing is locked until the single exit.

## 9. Breakeven

- E2 only: when the future touches TP1, move the stop on the whole lot to the **underlying entry level**.
- ⚠️ "Mathematically risk-free / zero risk" is false for options. IV falls and theta accrues, so the option at the entry level is worth less than the premium paid. Costs and gaps remain.
- ⚠️ "Entry execution price" is ambiguous (underlying or option premium?). 🔧 Defined here as the **underlying entry level**.
- ❓ Price often retests the entry after TP1. Test a small buffer.

## 10. Trailing and TP2 Design

- 🔧 **One trailing engine only.** Long: `new_stop = max(old_stop, previous closed candle low − buffer)`. Short: `min(old_stop, previous closed candle high + buffer)`. A stop never moves against the position.
- ⚠️ "Swing low" and "previous candle low" differ. Adopt the **previous closed candle low/high**.
- ⚠️ **Buffer in "points" is scale-dependent** (crude source: 2 points; gas source: 1.5 points). 🔧 Define the buffer in **ticks or as a fraction of ATR**, identical for both assets. ❓ Values to test.
- ❓ A previous-candle trail is tight and may stop out ordinary pullbacks. Backtest.
- **ATR / Chandelier alternative:** `highest high since entry − k × ATR(n)` (long). ⚠️ This is a trailing **stop**, not a "trailing take profit". ⚠️ ATR 14 × 2.0 is not an "institutional standard" (classic Chandelier: 22 × 3.0). ⚠️ ATR at 8:15 PM IST includes the release spike candles. ❓ Treat all values as test parameters.
- ⚠️ The sources use both a candle trail and an ATR trail on the same position with no priority rule. 🔧 Use one, or the **tighter** (higher for longs, lower for shorts).
- ⚠️ The gas source says "close 100% of the remainder at TP2", then "if price blows past TP2, trail". Nothing is left to trail. With 1 lot the choices are E1–E3 in §8. A runner that trails after a partial exit (needs ≥ 2 lots) is not available.

## 11. Time Stop and Risk Sizing

**Time stop**
- ⚠️ Sources give 1 hour, 1.5 hours, or nothing (gas). 🔧 **90 minutes from release, then flat** ❓.

**Risk, Phase 1 (account ₹50,000) 🔧** (user decision, 7 Oct 2026: a 1% cap is not workable at this size; it is adopted when the account grows)

- **Position: 1 lot. Trades per report: 1.** No re-entry after a stop. No trade if there is no valid breakout.
- **No %-of-equity cap filter in Phase 1.** One minimum lot already sets the risk size. Every valid signal is taken (or logged as taken in the hypothesis).
- Risk is an **outcome of the stop distance**: `risk_per_lot = qty × delta × |entry − SL|`. Maximum loss = premium paid = `premium × qty`. 🔧 **Record both, in ₹ and as % of the account, for every trade.** They are results to be judged, not filters.
- **Guardrails that replace the cap (proposed ❓, user to set the numbers):**
  - The stop at the midpoint is always placed. It is never widened.
  - **Pause rule (user decision, 7 Oct 2026): after 3 losing trades in a row, stop trading and review.** No drawdown trigger.
    - "Loser" = a trade closed at a net loss (stop-out, or a time-stop exit below entry).
    - 🔧 Count in date order across both instruments (crude on Wednesday, gas on Thursday), not separately. ❓ User to confirm the combined count.
    - 🔧 A report where no trade was taken (no signal, sign rule said no) does not count as a win or a loss and does not reset the streak.
    - 🔧 A winning (or flat) trade resets the streak to zero.
    - 🔧 Review checklist before resuming: snapshot log vs actual, stop distance vs risk, whether any rule was broken, data-quality flags (contract roll, wrong release time). Resume only after the review is written down.
  - Premium per lot as a share of the account is reported every trade. A limit (for example ≤ 20%) is optional ❓.
- ❓ At one trade per report there are about 52 trades per year per asset. Results are noisy. Judge the system over many trades.

**Phase 2: adopt a % cap as the account grows 🔧.** Cap = **2%**, then **1%**. The account size needed depends on the contract and the stop distance. Table below uses the illustrative stops; replace with the **median measured stop distance** once the snapshot log has data ❓.

| Contract | Illustrative stop | Risk per lot | Account for 2% | Account for 1% |
|---|---|---|---|---|
| CRUDEOIL | 25 pts | ₹1,550–1,625 | ₹77,500–81,250 | ₹1.55–1.63 lakh |
| CRUDEOILM | 25 pts | ₹155–163 | ₹7,750–8,150 | ₹15,500–16,300 |
| NATGASMINI | 3 pts | ₹420–520 | ₹21,000–26,000 | ₹42,000–52,000 |

- NATGASMINI is already at about 1% of ₹50,000 with a 3-pt stop. A wider stop raises risk in proportion.
- CRUDEOIL standard needs about ₹80,000 for a 2% cap, so Phase 2 for crude starts at about that account size. NATGASMINI is within range now.
- 🔧 Phase 2 rule: when the account reaches the "2%" figure for a contract, switch on a 2% filter for it. At the "1%" figure, switch to 1%. Do not use the cap to skip trades before then.

**What one lot costs at ₹50,000** (chain snapshots 7 Oct 2026; ✅ arithmetic; stop distances illustrative ❓). Buying an option needs the full premium in cash; max loss = premium.

| Contract | Strike (delta) | Premium / unit | Cost per lot (max loss) | % of account | Risk at stop | % of account |
|---|---|---|---|---|---|---|
| CRUDEOIL | call 8400 (0.65) | 428.7 | ₹42,870 | **86%** | 25-pt stop: ₹1,625 | 3.3% |
| CRUDEOIL | call 8450 (0.62) | 395.2 | ₹39,520 | **79%** | ₹1,550 | 3.1% |
| CRUDEOIL | put 8900 (−0.62) | 432.8 | ₹43,280 | **87%** | ₹1,550 | 3.1% |
| CRUDEOIL | put 8950 (−0.65) | 469.2 | ₹46,920 | **94%** | ₹1,625 | 3.3% |
| CRUDEOILM | call 8400 (0.65) | 428.7 | ₹4,287 | 8.6% | 25-pt stop: ₹163 | 0.33% |
| CRUDEOILM | call 8450 (0.62) | 395.2 | ₹3,952 | 7.9% | ₹155 | 0.31% |
| NATGASMINI | call 290 (0.69) | 23.65 | ₹5,913 | 11.8% | 3-pt stop: ₹518 | 1.04% |
| NATGASMINI | call 295 (0.64) | 20.80 | ₹5,200 | 10.4% | ₹480 | 0.96% |
| NATGASMINI | call 300 (0.59) | 17.95 | ₹4,488 | 9.0% | ₹443 | 0.89% |
| NATGASMINI | put 315 (−0.56) | 20.60 | ₹5,150 | 10.3% | ₹420 | 0.84% |
| NATGASMINI | put 320 (−0.61) | 23.95 | ₹5,988 | 12.0% | ₹458 | 0.92% |

- ⚠️ **Honest note on CRUDEOIL standard:** dropping the cap does not remove the risk, it only stops the rule from skipping. Each stop-out would cost about 3% of the account, and a gap or failed exit could approach 86–94% (the premium). The user has accepted this for Phase 1 and chose CRUDEOIL standard.
- The real stop distance is set by the midpoint each week. A wide post-report range raises risk per lot in proportion.

## 12. Order Mechanics (PARKED)

Out of scope for the current hypothesis (user decision, 7 Oct 2026). Collected here so nothing is lost:
- How stops and targets are placed on MCX options (stops are not triggered by the future's price; alerts vs premium-level conversion `premium_level ≈ entry_premium + delta × (underlying_level − entry_underlying)`).
- Whether SL / SL-M orders are allowed on MCX options.
- Order type for entries and exits (market vs marketable limit vs mid-price limit, time limits for fills).
- Bid-ask spread, slippage, and partial fills.

Until this is un-parked, rules are evaluated on **underlying price levels**. Option premium appears only through delta approximations (risk filter, §11) and chain observations.

## 13. Open Questions (common)

- Backtest: ≥ 50 releases per asset (≈ one year of one report). **No MCX history.** Proxy: NYMEX CL / NG 5-min (and 3-min) around the same release, then forward-test small on MCX. ❓ The proxy ignores USD/INR and MCX spreads.
- **Daily-horizon test on free EIA history: `eia_daily_test_results.md`.** The consensus-free proxy (de-seasonalised z-score) passes a sanity check for crude only before 2015, fails for Cushing and gas. It cannot answer our question. True consensus history is needed.
- **Data plan:** forward capture each week plus historical NYMEX proxy data: see `eia_data_plan.md`. Raw event bars are saved in `data/`.
- **Second simulation (15 and 30-minute bars, about 15–22 events per instrument): `eia_pass2_results.md`.** No edge visible. Continuation is 55–64% same-sign (t 0.7–1.8, not significant). Pivot TP1 almost never reached. Crude median stop is 43 points (5% of the account per lot). Corrects pass 1 (crude 9 Sep was not a release day).
- **First simulation (6 + 6 events, 24 Aug to 1 Oct 2026) is in `eia_pass1_results.md`.** Illustration only. It leans toward continuation after the first 15 minutes, shows 2 touch-stop whipsaws and 2 saves, and measures real stop sizes (crude median about 34 points, gas mini about 1.8 points). The 24 Sep gas date is contaminated by the contract roll.
- **Entry-style variants:** B1 breakout continuation after the 15-minute range (default); F1 fade of a failed breakout (§16 finding R1 vs R2).
- **Stop variants to test:** S1 midpoint of the opening range (default); S2 opposite range edge (wider); S3 swing low/high of the last few candles (from the exit-rules research).
- **Time-stop variants:** T1 90 minutes from release (default); T2 exit if there is no progress within 30–45 minutes of entry.
- **Reward-to-risk entry filter variants:** R:R to TP1 ≥ 1, ≥ 1.5, ≥ 2.
- Test: stop touch vs close; TP1 buffer after breakeven; trail buffer; ATR/Chandelier parameters; time stop length; floor vs Camarilla; 3-min vs 5-min; TP design A/B/C.
- Confirm the MCX specs above against the official MCX page or exchange circulars (the page returned 403 to us). Check whether the chain tool lists the next-month expiry.

## 14. References and What They Do (and Do Not) Support

Checked 6 Oct 2026. Primary sources first.

| Source | Status | What it gives us |
|---|---|---|
| eia.gov/petroleum/supply/weekly (WPSR) | ✅ read | Summary TXT "released after 10:30 am". Downloads: XLSX, CSV, JSON, PDF; per-table CSV/XLS/PDF; combined Data Overview PDF. Release schedule is on a separate page; holiday notes are in an explanatory-notes appendix. |
| ir.eia.gov/ngs/ngs.html (WNGSR) | ✅ read | Main table, columns, Lower 48 values, standard error. Use this public URL. The signed `secure/ngs` link you sent is time-limited. Do not store the signature. |
| acy.com (WTI, API, EIA, indicators; 6 Aug 2026) | ✅ read | Retail broker article, written by a third party, with a disclaimer. Confirms API Tue ~4:30 PM and EIA Wed 10:30 AM (it says "EST"; in summer it is EDT ⚠️). Confirms the surprise rule: `actual − forecast`, positive (build) = bearish, negative (draw) = bullish ✅, same as ours. Case study ✅ arithmetic: forecast −1.0 mb, actual +2.0 mb, surprise **+3.0 mb** (week ending 17 Jul 2026, released Wed 22 Jul 2026 ✅ dates). ❓ Not checked against the EIA archive. |
| roboforex.com (how to use the EIA report) | ✅ read | Generic. Crude stocks are "the most important part". Lists other metrics. One anecdote: an unexpected 2.377 mb draw, WTI up about $1.5. No thresholds, no rules. |
| insigniafutures.com | ❌ not read | Behind a bot-check screen. Not bypassed. |
| startrader.com | ❌ not read | HTTP 403 / bot challenge. Not bypassed. |

**What the readable secondary sources do NOT provide:** no surprise-size thresholds, no typical move size per mb of surprise, no stop or target distances, no backtest, no option-specific guidance. None of them supports the "35–45 points", "institutional", pivot-gravitation or Camarilla claims.

**ACY is a different strategy**, not support for ours:
- Bias from the surprise, then wait for a **pullback** to a technical level. Longs only above the 50 EMA, shorts only below it. RSI(14) pullback to the 40–50 zone (longs) or 50–60 zone (shorts). Bollinger middle-band rejection. 5-min chart. ❓ No evidence or backtest given.
- ⚠️ It says "never trade raw numbers at the moment of release". Ours is a **breakout after 15 minutes**. They conflict on entry style.
- 🔧 Candidate test variant: "pullback entry" (**P1**) vs "range breakout" (**B1**, our default). Same bias rule, same exits. ❓ Test both.
- ⚠️ ACY uses Baker Hughes rig count (Fri) as context. Weekly, long-term. No intraday role in our rules.

## 15. Corrections Log (common rules)

**Exit-rules research batch 2 (7 Oct 2026)**

| # | Source claim | Verdict |
|---|---|---|
| C1 | Set the stop on the underlying chart, then translate to the option with delta | ✅ Same principle as ours. Formula `(entry − stop) × delta` ✅ arithmetic (40 × 0.50 = 20; ₹120 − 20 = ₹100). Approximate: delta, gamma and IV change. Translating to an order is parked (§12). |
| C2 | "Never base a stop on a % of premium" and, two sections later, "stop loss cap 20–30% of premium" | ⚠️ Contradicts itself. |
| C3 | Stop at a chart level: support / swing low (breakout level for a put) | ✅ Direction is right (puts stop above). Different from our midpoint stop. Logged as variants S2/S3. ❓ |
| C4 | A premium stop triggers before the underlying stop | ⚠️ It includes IV drop and theta, so it can fire while the underlying still holds. Our hypothesis uses underlying levels. |
| C5 | Naked option buying wins 30–40% of the time | ❓ Unsupported. |
| C6 | Minimum 1:2 or 1:3 reward-to-risk | ❓ No evidence. Break-even win rate at 1:2 is 33% (arithmetic), at 1:1 it is 50%. Logged as an entry-filter variant. |
| C7 | Stop cap 20–30% of premium | ⚠️ Our ITM stops are much smaller in premium terms (table below), so this cap is not binding. |
| C8 | "A 50%+ loss makes recovery mathematically impossible" | ⚠️ Overstated. Recovery needs +100%. Hard, not impossible. |
| C9 | Profit target 40–60% of premium | ⚠️ Incompatible with ITM options and pivot targets (table below). |
| C10 | 50% rule: sell half at +40%, move stop to breakeven, run the rest to 100%+ | ⚠️ Needs at least 2 lots. We trade 1 lot. Not applicable. |
| C11 | Time stop: exit if no breakout within 30–45 minutes of entry | ❓ Plausible idea. Their reason (theta) is weak (below). Logged as time-stop variant T2. |
| C12 | "Naked options are melting ice cubes" via theta in 30–45 minutes | ⚠️ Theta over 45 minutes is tiny (below). IV contraction is the real concern. |

**Arithmetic behind C7, C9, C12** (✅ chain snapshots 7 Oct 2026; stops illustrative ❓; delta held constant, gamma ignored):

| Option | Premium | Stop on premium | Stop as % of premium | +40% of premium | Underlying move needed for +40% | Theta / 45 min |
|---|---|---|---|---|---|---|
| CRUDEOIL call 8400 (0.65) | 428.7 | 0.65 × 25 = 16.3 | 3.8% | 171.5 | **264 pts** | ≈ 14.4 ÷ 24 × 0.75 ≈ ₹0.5 (0.1%) |
| NATGASMINI call 295 (0.64) | 20.80 | 0.64 × 3 = 1.92 | 9.2% | 8.32 | **13.0 pts** | ≈ ₹0.02 per unit (0.1%) |
| NATGASMINI put 315 (−0.56) | 20.60 | 0.56 × 3 = 1.68 | 8.2% | 8.24 | **14.7 pts** | ≈ ₹0.02 per unit (0.1%) |

- A 40% premium target needs a 264-pt crude move (≈ 3%) or a 13–15 pt gas move (≈ 4–5%), far beyond a pivot TP1 and a 90-minute window. Percentage-of-premium targets do not fit deep ITM options.
- Theta per 45 minutes is about 0.1% of premium using a 24-hour spread. The exchange session is shorter than 24 hours, so a per-session figure would be larger but still small. Time decay is not a reason for a 30–45 minute time stop. IV contraction is the argument to test.
- Our stops are 4–9% of premium, so a "20–30% cap" never binds.

## 16. Independent Research Findings (7 Oct 2026)

Done without relying on the user's pastes. "Read" = I opened and read the source. "Snippet" = only a search-result summary, so treat as ❓.

| # | Finding | Source | Status |
|---|---|---|---|
| R1 | Futures react to EIA inventory surprises **within about 5–7 minutes**, and the response **did not revert** by the study's later reference point (about 100 minutes). Sample 16 Jul 2003 to 30 Jun 2017, front-month NYMEX, surprise = actual − Bloomberg median forecast, scaled by its standard deviation | [Linn et al., EIA presentation, 2017](https://www.eia.gov/finance/markets/reports_presentations/2017/linn.pdf), citing Halova et al. 2014 | ✅ read |
| R2 | A different study reports the reaction **lasting about 25 minutes with the price reverting quickly afterwards**, and a larger reaction when analysts disagree more | Rousse et al., Energy Journal 40(2) (IAEE summary) | ❓ snippet |
| R3 | Response per **1 SD of surprise**: crude −0.429 (before June 2006) → **−0.271** after; natural gas −0.708 → **−1.163**. Units assumed to be % log price change ❓. Responses are inversely related to the surprise. No difference between positive and negative surprises | Linn et al., slides 9–10 | ✅ read; units ❓ |
| R4 | **No relation between surprises and price changes on the two days after the release** | Linn et al., slide 11 | ✅ read |
| R5 | Average absolute return is **positively related to the absolute size of the surprise**, so a bigger miss means a bigger early range | Linn et al., slide 11 | ✅ read |
| R6 | Crude, gasoline and distillate surprises each move crude **in the same direction** (companion-product surprises matter). Gas responds to its own surprise most (−1.005 per SD) | Linn et al., slide 9 | ✅ read |
| R7 | EIA's own **sampling standard error** for gas net change averaged about **2 Bcf** (Lower 48) and about 1 Bcf per region. In 2016 it was 2.2–5.5 Bcf in the 10 weeks with withdrawals above 100 Bcf and 1.0–3.2 Bcf in other weeks. (Our 25 Sep 2026 figure was 0.7.) | [EIA Today in Energy](https://www.eia.gov/todayinenergy/detail.php?id=29712) | ✅ read |
| R8 | Analyst gas storage forecasts averaged about **13.2 Bcf** absolute error per week since 2002. Bloomberg median crude storage forecasts are "considerably less accurate", underestimate the change, and have not improved | Search snippets (an academic abstract; Ederington et al., Energy Journal 40(5)) | ❓ snippet |
| R9 | **IV tends to drift up before scheduled releases and drop afterwards**; realized volatility rises on release days | Search snippets (several papers) | ❓ snippet; size unknown |
| R10 | Public academic tests of **floor/Camarilla pivot points on energy futures are scarce**; most pivot backtests are proprietary or blogs | Search result summary | ✅ finding |
| R11 | The one rigorous study found: published support and resistance levels **did predict intraday trend interruptions** (FX, six firms, 1996–98). Not floor pivots, not energy | [Osler, NY Fed, 2000](https://resources.newyorkfed.org/medialibrary/media/research/epr/00v06n2/0007osle.pdf) | ❓ snippet |
| R12 | **No comparative evidence** exists for a range-midpoint stop vs an opposite-edge stop. Only retail backtests of ORB on ES, where range width drives stop size | TradingView / edgeful pages | ✅ finding (nothing authoritative) |
| R13 | Trade-press examples show gas **partly retracing within 15 minutes** after a surprise (e.g. a 132 Bcf injection dipped, then recovered to −1.6 cents by 10:45) | NGI articles | ❓ anecdote |

**What this means for our hypothesis**

1. **Our entry waits 15 minutes. The literature says the main reaction is finished in 5–7 minutes.** By 8:15 PM IST most of the surprise-driven move is already in the range. Whether price **continues** beyond that range is exactly what the sources disagree on (R1 vs R2/R13). **The breakout-continuation idea (B1) has no direct evidence. Its edge is genuinely unknown.** This is the most important finding so far.
2. 🔧 Add test variants: **F1 (fade / failure)**: enter against a failed breakout when price returns through the midpoint. Keep B1 as the default to test; do not assume it works.
3. **No next-day drift (R4):** nothing to hold overnight. Consistent with our same-session exit.
4. 🔧 **Measure surprises in standard deviations**, not raw units. Compute the SD from our own history once we have it. Threshold X in SD units (for example ≥ 0.5 SD) ❓.
5. **Calibration of a typical move** (arithmetic ✅, coefficient assumptions ❓): 1 SD surprise ≈ 0.27% for crude ≈ **23 points** on MCX crude at 8,643 (8,643 × 0.00271); ≈ 1.16% for gas ≈ **3.6 points** at 306 (306 × 0.01163). Our illustrative stops (25 pts crude, 3 pts gas) are therefore about one SD-surprise move. Sample ends in 2017 and uses NYMEX front month, so MCX today may differ ❓.
6. **Gas surprise threshold:** EIA's own sampling error is about 2 Bcf (R7). A surprise below that is inside the measurement noise. Our 1 Oct figure (+1 Bcf) is noise. 🔧 For gas, X must be above about 2 Bcf at minimum. Analyst error (R8) is much larger ❓, so real surprises are not tiny.
7. **IV:** if most of the release-driven IV drop happens in the first minutes (R9, plausible given R1), then entering at ≥ 15 minutes buys **after** much of the crush. That would reduce the vega risk we worried about. ❓ Untested. Tonight's Block E (IV at T − 5 vs T + 15) tests it directly.
8. **Risk link (R5):** a larger surprise gives a larger early range, so a wider midpoint stop and a larger ₹ risk on a 1-lot trade. Record risk against surprise size.
9. **Pivots (R10, R11):** no energy-futures evidence. The little evidence on levels suggests price tends to **stall** near them, which supports using pivots as take-profit levels rather than as breakout levels. Still a hypothesis ❓.
10. **Stops (R12):** nothing authoritative separates S1/S2/S3. Keep all three as variants.

## 17. External Reference: Cushing Inventory WTI Trading Model (GitHub)

Repo: [codingshujaa/Cushing-Inventory-WTI-trading-model](https://github.com/codingshujaa/Cushing-Inventory-WTI-trading-model). Read 7 Oct 2026: the README and the `.qmd` source (through a page summariser, so exact figures are ❓ until the source is opened). A student quantitative-trading project in R and Quarto, using the EIA API.

| Item | What the repo does | Tag |
|---|---|---|
| Signal | z-score of the **weekly Cushing stocks change**, using the training-period mean and SD. **No consensus.** Thresholds ±0.8 SD (tuned by grid search) | ✅ from code |
| Trend filter | 4-week vs 13-week moving average of WTI daily price | ✅ |
| Direction | Large **build** (z ≥ +0.8) while the trend is **up** → short. Large **draw** (z ≤ −0.8) while the trend is **down** → long. That is *with* the data bias but *against* the prevailing trend. The README calls this "mean reversion", which is misleading | ✅ from code |
| Trade | Enter at the **WTI daily close on the release day**; take profit **$1.20**, stop **$0.80** per barrel; exit after 2 days at most | ✅ |
| Costs | **None** (no commissions or slippage) | ✅ |
| Split | Train 2010 to 2023, test 2024 on | ✅ |
| Results | Train: 87 trades, win rate about 59%, about +$32 per barrel. **Test: 16 trades, win rate about 44%, about +$1.9** (about 1.4%) | ✅ per the repo; ❓ unverified by us |

**Assessment**
- ✅ **A weak result by its own account.** Out-of-sample: 16 trades, no costs. With a $1.20 target and $0.80 stop, break-even win rate is 0.80 / (0.80 + 1.20) = **40%**, so 44% is barely above break-even before any costs. This matches our pass-2 finding of no clear edge.
- ⚠️ **Overfitting risk:** the thresholds come from a grid search on the training data, and the z-score uses the whole training sample's mean and SD. In-sample numbers are optimistic. Their "cumulative return" divides dollar PnL by a price base, not a capital base ❓.
- ⚠️ **Not comparable to our setup:** daily close entry (after the release reaction), WTI spot, Cushing only, no options, no consensus.
- ⚠️ **Seasonality is ignored.** A raw weekly change is dominated by season, especially for gas. A z-score should compare the change with the same week in earlier years (or the 5-year average).

**Ideas worth testing for our project (not adopted)**
1. **Consensus-free surprise proxy.** The z-score of the actual change, **de-seasonalised** (change versus the same-week 5-year average), standardises surprises in SD units without consensus data. EIA publishes long free histories (weekly stocks, weekly gas storage, daily WTI/Henry Hub spot). Limitation: "actual vs typical" is not "actual vs expected".
2. **Trend-relation filter.** Test whether signals whose data bias **opposes** the prior trend (reversal setups) behave differently from those that agree with it.
3. **Pre-register parameters.** Fix the thresholds before looking at results. Do not grid-search on a small sample. Our forward capture from 7 Oct 2026 is a natural out-of-sample set.
4. **Judge in R-multiples (risk units), not "cumulative return" on a price base.**
5. **Daily-horizon check on free data:** does the sign of a de-seasonalised inventory shock predict the next 1–2 day return, over 15 or more years? This tests whether the data has any predictive power at all. It needs downloads of EIA files (permission to be asked first).

## Change Log
- 2026-10-06: created. Exit/entry/risk rules unified across WPSR and WNGSR per the user's statement that SL, TP1, TP2 and trailing are the same for options (only lot sizes differ). Added lot table, per-lot sizing illustration, and the three-point list of what is still asset-specific (data signal, option chain numbers, price levels).
- 2026-10-06: position fixed at 1 lot, 1 trade per report. Removed 60/40 scaling and the lots-from-risk formula. Replaced with single-exit candidates E1–E3, a risk filter, minimum-equity table.
- 2026-10-06: added references table (EIA pages, ACY, Roboforex read; Insignia and Startrader blocked by bot checks, not bypassed). ACY pullback strategy logged as test variant P1.
- 2026-10-07: consensus capture protocol and sign-disagreement rule added to §5.
- 2026-10-07: strike intervals confirmed from chain headers (crude 50, gas 5).
- 2026-10-07: broker execution parked (§12). Entry price defined on the underlying.
- 2026-10-07: contract specs added (ticks, strike steps, option expiry rule, mini options, hours). Expiry-selection rule added to §4.
- 2026-10-07: contracts chosen: CRUDEOIL standard, NATGASMINI. Per-contract cost and risk table added to §11.
- 2026-10-07: account size ₹50,000 recorded. CRUDEOIL standard fails the 1% filter (3.1–3.3%) and premium guard; CRUDEOILM passes. NATGASMINI chain analysed (gas file §4).
- 2026-10-07: the 1% cap is replaced by Phase 1 rules (1 lot, record risk, drawdown pause) at ₹50,000. A 2% then 1% cap is adopted by account-size thresholds (Phase 2).
- 2026-10-07: contracts final (CRUDEOIL standard on Wednesday, NATGASMINI on Thursday). One trade per report after post-report analysis; no second attempt.
- 2026-10-07: exit-rules research batch 2 evaluated (corrections C1–C12, arithmetic table, stop/time-stop/R:R variants).
- 2026-10-07: independent research added (§16): response timing, size per SD, no next-day drift, EIA sampling error, IV pattern, pivot and ORB evidence gaps. Variant F1 added.
- 2026-10-07: pass 1 simulation on MCX 5-min history added (eia_pass1_results.md).
- 2026-10-07: data plan added (eia_data_plan.md); raw bars saved in data/.
- 2026-10-07: EIA schedule exceptions added to §2 (Thursday 12:00 ET WPSR delays, 15 Oct note). Pass 2 results linked.
- 2026-10-07: external reference added (§17): Cushing inventory WTI repo.
- 2026-10-07: free EIA history downloaded; daily-horizon proxy test added (eia_daily_test_results.md).
- 2026-10-07: pause rule set: 3 consecutive losers, then pause and review (no drawdown trigger).
