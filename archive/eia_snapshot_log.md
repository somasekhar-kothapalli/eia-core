# EIA Snapshot Log

Fill one block per release. Purpose: build our own consensus and reaction history, and test the sources side by side. No trading is implied. The rules are in `eia_common_execution.md`.

**Primary source:** Investing.com. **Cross-check:** Trading Economics (also the only source for API). Decided 7 Oct 2026.

**Times (IST, US daylight time):** release 8:00 PM. Take the snapshot at **7:55 PM**. After 1 Nov the release is 9:00 PM and the snapshot 8:55 PM.

---

## Schemas and field mapping

Each release can also be stored as a JSON record that follows these schemas (draft 2020-12):
- Crude (WPSR): [schemas/wpsr_crude.schema.json](schemas/wpsr_crude.schema.json), example [schemas/examples/wpsr_2026-09-30.json](schemas/examples/wpsr_2026-09-30.json)
- Gas (WNGSR): [schemas/wngsr_gas.schema.json](schemas/wngsr_gas.schema.json), example [schemas/examples/wngsr_2026-10-01.json](schemas/examples/wngsr_2026-10-01.json)

| Log block | JSON field(s) |
|---|---|
| A: Investing.com forecast column | `consensus[]` with `source: "investing.com"`, `role: "primary"`, `capture_type: "pre_release"` |
| A: Trading Economics column | `consensus[]` with `source: "tradingeconomics.com"`, `role: "cross_check"` |
| A: snapshot time | `consensus[].captured_at` (ISO 8601 with offset, e.g. `2026-10-07T19:55:00+05:30`) |
| A: previous | `consensus[].previous_crude_stocks_change_mb` / `previous_net_change_bcf` |
| A: API rows (crude) | `api.actual_crude_stocks_change_mb`, `api.consensus_crude_stocks_change_mb` |
| A: gas estimate range, if shown | `consensus[].range_low_bcf`, `range_high_bcf` |
| B: Actual | `actuals.*` (crude: `crude_stocks_change_mb` and the optional product, Cushing, refinery items; gas: `net_change_bcf` and the optional items) |
| B: Surprise columns, same-sign, trade allowed | `surprise.*` (`crude_vs_primary_mb` or `net_change_vs_primary_bcf`, `signs_agree`, `trade_allowed_by_sign_rule`) |
| C: Source behavior check | `post_release_check.*` |
| D: Price reaction, E: IV observation | **Not in these schemas.** Keep them in this log. A separate schema can be added once we know which fields we use. |

- Use `capture_type: "backfilled"` and `captured_at: null` for anything read after the release.
- Units: crude in mb, gas in Bcf. Build/injection positive, draw/withdrawal negative.
- Filename suggestion: `records/wpsr_YYYY-MM-DD.json` and `records/wngsr_YYYY-MM-DD.json`.

---

## Block A: Consensus snapshot (take at T − 5 min)

Copy the numbers exactly as shown. Units: crude stocks in mb, gas in Bcf. Sign: build +, draw −.

### WPSR (crude)

| Release date | Data point | Investing.com forecast | Trading Economics consensus | Previous | Snapshot time (IST) |
|---|---|---|---|---|---|
| Wed 7 Oct 2026 | Crude stocks change (mb) | | | | |
| | Gasoline stocks change (mb) | | | | |
| | Distillate stocks change (mb) | | | | |
| | API crude change, released Tue (mb) | n/a | | | |
| | API actual (Tue) | n/a | | | |

### WNGSR (gas)

| Release date | Data point | Investing.com forecast | Trading Economics consensus | Previous | Snapshot time (IST) |
|---|---|---|---|---|---|
| Thu 8 Oct 2026 | Net change (Bcf) | | | | |

---

## Block B: Actuals and surprise (fill within 5 minutes after the release)

`Surprise = actual − forecast`. Negative = bullish, positive = bearish.

| Release date | Data point | Actual (EIA) | Surprise vs Investing | Surprise vs Trading Economics | Same sign? (Y/N) | Trade allowed by sign rule? |
|---|---|---|---|---|---|---|
| Wed 7 Oct 2026 | Crude (mb) | | | | | |
| | Gasoline (mb) | | | | | |
| | Distillate (mb) | | | | | |
| | Refinery utilization change (pts) | | n/a | n/a | n/a | n/a |
| | Cushing change (mb) | | n/a | n/a | n/a | n/a |
| Thu 8 Oct 2026 | Gas net change (Bcf) | | | | | |

- Sign rule: if the two sources give opposite signs, or one gives zero, the bias is unclear: **no trade**.
- Actual figures come from the EIA page (primary). Investing.com is only for the forecast.

---

## Block C: Source behavior check (30 minutes after the release)

| Release date | Investing.com forecast now (changed? Y/N) | Trading Economics consensus now (changed? Y/N) | Notes |
|---|---|---|---|
| Wed 7 Oct 2026 | | | |
| Thu 8 Oct 2026 | | | |

- Purpose: confirm whether a site overwrites its forecast after the print (Trading Economics showed gas consensus = actual on 1 Oct).

---

## Block D: Price reaction (MCX future, execution chart: 5-min)

Fill from the chart after the window. Do not trade. Observe.

| Release date | Instrument | Range High | Range Low | Midpoint | Pivot P | R1 | R2 | S1 | S2 |
|---|---|---|---|---|---|---|---|---|---|
| Wed 7 Oct 2026 | CRUDEOIL | | | | | | | | |
| Thu 8 Oct 2026 | NATURALGAS | | | | | | | | |

| Release date | First 5-min close beyond range (time, direction) | Entry level (next candle) | Hit midpoint stop? (Y/N, time) | Hit TP1? (Y/N, time) | Hit TP2? (Y/N, time) | High / low in the 90 min | Direction agreed with bias? (Y/N) |
|---|---|---|---|---|---|---|---|
| Wed 7 Oct 2026 | | | | | | | |
| Thu 8 Oct 2026 | | | | | | | |

---

## Block E: Option observation (optional, MCX chain at T + 15 min)

| Release date | Underlying | ATM IV before (T − 5) | ATM IV after (T + 15) | IV change (pts) | Chosen strike | Delta | Premium | Bid-ask spread |
|---|---|---|---|---|---|---|---|---|
| Wed 7 Oct 2026 | CRUDEOIL | | | | | | | |
| Thu 8 Oct 2026 | NATURALGAS | | | | | | | |

- Purpose: measure the real IV drop. Our estimate of 3 points is an assumption.

---

## Running summary (update weekly)

| Week | Report | Crude/gas surprise (Investing) | Direction of surprise | Breakout direction | Agreed? | Result vs E1 / E2 / E3 |
|---|---|---|---|---|---|---|
| | | | | | | |

After about 50 rows per report, review: hit rates, typical surprise size, median IV drop, which exit design (E1–E3) looks best.
