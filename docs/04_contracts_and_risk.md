# 04 Contracts, Costs and Risk

**Last revised:** 7 Oct 2026. Tags: ✅ verified · 🔧 decided · ❓ open.

## 1. MCX contract specs

Lot sizes from the user. Everything else from broker and news pages (Zerodha, Sharekhan, Fyers, ICICI Direct, Angel One) and the two chain screenshots. MCX's own page returned 403 to us, so an **official check is pending ❓**. The values agree across sources.

| Contract | Qty per lot | Futures tick | ₹ per futures tick per lot | ₹ per 1-pt move per lot | Options | Strike step | Option tick | Strikes listed |
|---|---|---|---|---|---|---|---|---|
| **CRUDEOIL** (traded) | 100 bbl | ₹1 | ₹100 | ₹100 | ✅ | ₹50 ✅ chain | ₹0.05 ❓ | ❓ |
| CRUDEOILM | 10 bbl | ₹1 | ₹10 | ₹10 | ✅ since 23 Apr 2024 | ₹50 | ₹0.05 | 25 ITM + 25 OTM + 1 near |
| NATURALGAS | 1,250 mmBtu | ₹0.10 | ₹125 | ₹1,250 | ✅ | ₹5 ✅ chain | ₹0.05 | 15 + 15 + 1 |
| **NATGASMINI** (traded) | 250 mmBtu | ₹0.10 | ₹25 | ₹250 | ✅ since 23 Apr 2024 | ₹5 | ₹0.05 | 15 + 15 + 1 |

- Options are **European style**. **Expiry = two business days before the underlying futures expiry** ✅ (stated for CRUDEOILM, NATGASMINI, NATURALGAS; the user's paste says the same for crude).
- Chain headers: **CRUDEOIL options expire Thu 15 Oct 2026**, **gas options Fri 23 Oct 2026**. Inferred futures expiry: crude Mon 19 Oct (inside the stated "16th–20th" range) and gas Tue 27 Oct ❓.
- ⚠️ An in-the-money option held to expiry converts into a futures position (claimed, not verified ❓); the "margin needed before 7 PM" is broker-specific ❓. Irrelevant to an intraday hold; relevant to expiry selection.
- Per-lot P&L on the option ≈ `qty × delta × underlying move`.
- MCX energy trading hours: see spec §2.

## 2. Account and what one lot costs (₹50,000)

Buying an option needs the full premium in cash; **maximum loss = premium**. Price risk is measured at the **median stop from pass-2 simulations** (crude 43 points, gas mini 2.2 points; 15-minute opening range, n = 13 and 11) ❓ small samples. Pass-1 5-minute simulations (corrected, n = 5 each) gave 42 and 1.8.

| Contract | Strike (delta) | Premium / unit | Cost per lot (max loss) | % of account | Risk at median stop | % of account |
|---|---|---|---|---|---|---|
| CRUDEOIL | call 8400 (0.65) | 428.7 | ₹42,870 | **86%** | ₹2,795 | **5.6%** |
| CRUDEOIL | call 8450 (0.62) | 395.2 | ₹39,520 | **79%** | ₹2,666 | **5.3%** |
| CRUDEOIL | put 8900 (−0.62) | 432.8 | ₹43,280 | **87%** | ₹2,666 | **5.3%** |
| CRUDEOIL | put 8950 (−0.65) | 469.2 | ₹46,920 | **94%** | ₹2,795 | **5.6%** |
| NATGASMINI | call 290 (0.69) | 23.65 | ₹5,913 | 11.8% | ₹380 | 0.76% |
| NATGASMINI | call 295 (0.64) | 20.80 | ₹5,200 | 10.4% | ₹352 | 0.70% |
| NATGASMINI | call 300 (0.59) | 17.95 | ₹4,488 | 9.0% | ₹325 | 0.65% |
| NATGASMINI | put 315 (−0.56) | 20.60 | ₹5,150 | 10.3% | ₹308 | 0.62% |
| NATGASMINI | put 320 (−0.61) | 23.95 | ₹5,988 | 12.0% | ₹336 | 0.67% |

- **Worst measured stops:** crude 91.5 points ⇒ about ₹5,700 (11% of the account); gas mini 7.05 points ⇒ about ₹1,060 (2.1%).
- ⚠️ **Crude is the heavy leg.** One standard crude lot is 79–94% of the account in premium and about 5% in price risk at the median stop. A stop-out, a gap or a failed exit can cost far more than gas mini does. The user accepted this for Phase 1 and chose the standard lot over CRUDEOILM (CRUDEOILM at the same strikes would be 8% of the account in premium and 0.5% in risk).
- Gas mini is comfortable: about 0.7% median risk, 9–12% in premium.

## 3. Risk rules

**Phase 1 (now, ₹50,000)** (spec §8): 1 lot, 1 trade per report, **no %-of-equity filter**, record risk in ₹ and %, **pause after 3 losing trades in a row and review**.

**Phase 2: adopt a per-trade cap as the account grows.** Cap 2%, then 1%. Account needed = risk per lot ÷ cap, at the median (and worst) measured stop:

| Contract | Risk per lot, median (worst) | Account for 2% | Account for 1% |
|---|---|---|---|
| CRUDEOIL (delta ≈ 0.62) | ₹2,666 (₹5,673) | **₹1.33 lakh** (₹2.84 lakh) | **₹2.67 lakh** (₹5.67 lakh) |
| NATGASMINI (delta ≈ 0.6) | ₹330 (₹1,058) | **₹16,500** (₹52,900) | **₹33,000** (₹1.06 lakh) |

- NATGASMINI already fits **both caps at the median stop** (₹33,000 needed for 1%, account is ₹50,000). At the worst measured stop (7.05 points) it would be about 2.1% of the account. Crude needs several times today's account. Replace these estimates with the median of measured stops once the snapshot log has more data ❓.
- 🔧 Phase 2 rule: when the account reaches the "2%" figure for a contract, switch on a 2% filter for it; at the "1%" figure, switch to 1%. Do not use a cap to skip trades before then.
- Optional premium guard (for example premium ≤ 20% of the account) ❓ user decision. Gas mini (9–12%) passes; crude standard (79–94%) would fail.

## 4. Break-even arithmetic ✅ (underlying points, ignoring costs and delta)

With risk R and a single exit at distance A: break-even win rate = `R / (R + A)`. Example R = 25, A = 30 ⇒ 45%. At 1:2 reward-to-risk it is 33%, at 1:1 it is 50%. Exit E2 (breakeven stop after TP1) earns about zero on trades that reach TP1 then return, so it needs winners that run: its break-even win rate is higher than E1's and is not computable without the backtest.

## 5. Why percentage-of-premium rules do not fit ITM options ✅ arithmetic

(chain snapshots; delta held constant, gamma ignored)

| Option | Premium | Stop on premium at the median stop | As % of premium | A +40% premium target needs | Theta per 45 min |
|---|---|---|---|---|---|
| CRUDEOIL call 8400 (0.65) | 428.7 | 0.65 × 43 = 28.0 | 6.5% | 171.5 ⇒ **264 pts** underlying | about ₹0.5 (0.1%) |
| NATGASMINI call 295 (0.64) | 20.80 | 0.64 × 2.2 = 1.41 | 6.8% | 8.32 ⇒ **13 pts** | about ₹0.02/unit (0.1%) |
| NATGASMINI put 315 (−0.56) | 20.60 | 0.56 × 2.2 = 1.23 | 6.0% | 8.24 ⇒ **14.7 pts** | about ₹0.02/unit (0.1%) |

A 40% premium target would need a 264-point crude or 13–15-point gas move: far beyond a pivot TP1 and a 90-minute window. Our stops are about 6–7% of premium, so a "20–30% of premium" stop cap never binds. Theta over 45 minutes is about 0.1% of premium, so decay is not a reason for a 30–45 minute time stop; IV contraction is the argument to test.

## Option expiry calendar (looked up 7 Oct 2026)

**Rule (fits 9 of 9 checkable cases): option expiry = futures expiry minus 2 MCX business days.** Checked on gas Jan, Feb, Mar, Apr, May and Oct 2026, crude May and Oct 2026, and the NATGASMINI Jan 2027 circular. MCX's own calendar page returned 403, so the sources are third-party pages (Groww expiry tables, Fyers expiry notices, a TeamLease copy of the MCX circular); **verify against MCX before relying on a ❓ date.**

| Contract month | CRUDEOIL / CRUDEOILM option expiry | Basis | NATURALGAS / NATGASMINI option expiry | Basis |
|---|---|---|---|---|
| Oct 2026 (V2026) | **Thu 15 Oct** | ✅ chain loads | **Fri 23 Oct** | ✅ chain loads (mini and standard); a 27 Oct option does not exist |
| Nov 2026 (X2026) | **Tue 17 Nov** | ✅ ticker exists (CRUDEOIL and CRUDEOILM), thin volume | **Fri 20 Nov** | ✅ NATGASMINI ticker exists, thin volume; a 24 Nov option does not exist; standard NATURALGAS not seen |
| Dec 2026 (Z2026) | **Wed 16 Dec** | user-supplied, matches the rule; no Dec option found on TradingView on 7 Oct (probably not listed yet) | not set | futures Mon 28 Dec; option likely 23 or 24 Dec; no Dec gas option found yet |
| Jan 2027 (F2027) | not known | | **Thu 21 Jan** | ✅ NATGASMINI circular (futures Mon 25 Jan); NATURALGAS assumed same ❓ |
| Feb 2027 (G2027) | not known | | not known | |

- **The user's list of 7 Oct (gas 27 Oct, 24 Nov, 28 Dec; crude 15 Oct, 17 Nov, 16 Dec) mixes two kinds of dates.** The crude dates are option expiries. The gas dates are the **futures** expiries; the gas option expiries are 23 Oct and 20 Nov (tested: the option tickers exist only on those dates).
- Crude futures 2026 (Groww table): 16 Jan, 19 Feb, 19 Mar, 20 Apr, 18 May, 18 Jun, 20 Jul, 19 Aug, 21 Sep, **19 Oct, 19 Nov, 18 Dec**. The dates are not a plain "19th" rule (Jan 16, May 18, Jun 18), so 2027 cannot be extrapolated.
- Gas futures 2026 (Groww table): 27 Jan, 24 Feb, 26 Mar, 27 Apr, 26 May, 25 Jun, 28 Jul, 26 Aug, 25 Sep, **27 Oct, 24 Nov, 28 Dec**.
- The NATGASMINI Jan 2027 options start trading 26 Oct 2026, which suggests options are listed about three months ahead, so **Nov and Dec 2026 gas options should already exist** ❓ (not seen directly). Crude listing lead time not checked.
- CRUDEOILM is assumed to expire with CRUDEOIL ❓.
- The indicator (`tradingview/mcx_option_chain_levels.pine`) holds this table in `expiryFor()`. Unknown dates stay empty and the table says so.

**Nov chains on 7 Oct 2026 (tested with the updated indicator): they load (Missing 0/34) but are not usable yet.** Crude Nov (`CRUDEOILX2026`, Exp 17 Nov, Fut 8,664): 15 of 17 strikes had volume 0 and stale last prices, with call IV 31–45% against put IV 40–62%; ATM IV 36.5% is not trustworthy. Gas mini Nov (`NATGASMINIX2026`, Exp 20 Nov, Fut 340.30, about 10% above the Oct future): most strikes had no volume and no valid IV; ATM IV 57.6%. "Missing 0/34" does not detect stale quotes, so also check volume. Re-test on the day before 15 Oct (crude) and 22 Oct (gas) to see whether liquidity has moved to the next month.
