# 07 Open Items and Next Actions

**Last revised:** 7 Oct 2026 (before the WPSR release at 8:00 PM IST).

## 1. Next 24 hours

| When (IST) | Action |
|---|---|
| Wed 7 Oct, 7:55 PM | Consensus snapshot (Block A): run `python scripts/fetch_investing.py --launch-chrome --series crude_stocks api_crude gasoline distillates` for a timestamped pre-release row in `data/consensus/upcoming_snapshots.csv` (crude forecast was **+1.9 mb** at 10:00 UTC), plus a CRUDEOIL chain screenshot |
| Wed 7 Oct, 8:00 PM | WPSR release. Actuals and surprises into Block B within 5 minutes |
| Wed 7 Oct, 8:15 PM | Second chain screenshot (IV change, Block E) |
| Wed 7 Oct, after 9:30 PM | Source check (Block C); Claude captures the 5-min bars and volume flags into `data/` |
| Thu 8 Oct, 7:55 PM, 8:15 PM, after 9:30 PM | Same for WNGSR with NATGASMINI |

## 2. Inputs needed from the user

1. ~~Investing.com consensus history~~ **Done:** about 2 years (99 weeks) per series from `scripts/fetch_investing.py`. Optional: older history (each page embeds only the latest 100 releases) would need another source.
2. **Capture mode:** forward capture on request after each release, or scheduled (needs TradingView and Claude open).
3. **Does the chain tool list the next-month expiry?** Needed for **Thu 15 Oct** (WPSR at 9:30 PM IST; CRUDEOIL options expire that day) and Thu 22 Oct (gas options expire the next day).
4. Optional: a premium-per-lot limit (for example ≤ 20% of the account).

(Pause-rule count: **combined across both instruments**, confirmed by the user 7 Oct 2026.)

## 3. Rules and parameters still to set (all need data)

| Item | Default now | Needs |
|---|---|---|
| Surprise threshold X (SD units; gas floor about 2 Bcf) | none | consensus history |
| Conflict-flag rule for gasoline, distillate (and Cushing, utilization) | none | consensus history now in; test needs more intraday events |
| ~~Salt flag~~ (gas) | **parked, untested (user decision 7 Oct 2026)** | regional gas tables, only if revisited |
| Entry style | B1 breakout | more events; F1 and P1 variants |
| Exit design | E1 | E2, E3 and targets as 1×, 1.5×, 2× the stop |
| Stop trigger | touch | candle close |
| Timeframe | 5-min | 3-min, 15-min |
| Time stop | 90 min from release | no-progress 30–45 min |
| Trail buffer, ATR parameters | none | ticks or ATR fraction |
| Expiry selection N (days left) | suggest 5 | chain data |
| Reward-to-risk filter | ≥ 1 | ≥ 1.5, ≥ 2 |
| Pivots | floor | Camarilla; pivots may be poor targets (far from the day's price) |

## 4. Data needs

- ~~Consensus vs actual history~~ **Done for about 2 years** (crude SD 4.82 mb, gas SD 9.39 Bcf). Still to do: choose X (candidate 0.5 SD) and test the flags; consider a longer history only if 2 years proves too short.
- **IV change around the release** (T − 5 vs T + 15 chains).
- **More events:** about 2 per week by forward capture.
- Optional: an external intraday history (NYMEX CL, NG) if a provider is approved later.

## 5. Unverified items

- Official MCX specs (their page returned 403): ticks, strike steps, option expiry rule, minis.
- Studies known only from search summaries: the 25-minute reversal study (R2), analyst error of about 13 Bcf (R8), the IV pattern (R9), Osler's support/resistance result (R11).
- The Cushing repo's exact figures (read through a summariser).
- API consensus for the week ending 2 Oct (Trading Economics page summary was ambiguous).
- Whether ITM options convert into futures at expiry and the broker margin cutoff.

## 6. Parked

Broker execution: order types, stops on options, SL / SL-M availability, fills, spreads, slippage (spec §10).

## 7. Optional ideas (not scheduled)

| Idea | What it is | Why it is optional |
|---|---|---|
| **Kronos** ([shiyu-coder/Kronos](https://github.com/shiyu-coder/Kronos)) as an extra baseline | Open-source (MIT) foundation model that forecasts OHLCV candlesticks (tokenizer plus decoder-only Transformer, 4.1M to 499M parameters, trained on 45+ exchanges; arXiv 2508.02739, AAAI 2026). Read through the README only; the paper has not been read | It sees only price bars, not the consensus surprise or release schedule. The README gives no quantitative benchmarks and calls its backtest "not a production-ready quantitative trading system". It needs PyTorch and model downloads. We have only about 14–22 events per instrument, too few to judge it. Revisit once we have consensus history and 50+ events per report: test whether its predicted drift after the release adds anything beyond the surprise sign. First step would be reading the paper's out-of-sample results |

## 8. Risks to keep in view

- **CRUDEOIL standard lot is 79–94% of the account in premium and about 5% in price risk at the median stop** (worst measured stop: about 11%). Accepted for Phase 1.
- With about 15 events per instrument the results are inconclusive; do not tune on the forward sample.
- Continuous-contract rolls and wrong release times can silently corrupt a test (rules in `06_data_and_capture.md` §2).
