# Snapshot Log (fill one block per release)

Purpose: build our own consensus and reaction history and test the sources side by side. No trading is implied. Rules: `01_strategy_spec.md`. Field mapping to JSON: `06_data_and_capture.md` §3.

**Primary consensus source:** Investing.com. **Cross-check:** Trading Economics (also the only API source).
**Snapshot time:** T − 5 minutes. In IST: release 8:00 PM → snapshot **7:55 PM** (daylight time). Delayed WPSR (Thursday 12:00 ET = 9:30 PM IST) → snapshot **9:25 PM**. After 1 Nov, add one hour.

**Schemas:** [wpsr_crude](../schemas/wpsr_crude.schema.json) (example [30 Sep](../schemas/examples/wpsr_2026-09-30.json)) and [wngsr_gas](../schemas/wngsr_gas.schema.json) (example [1 Oct](../schemas/examples/wngsr_2026-10-01.json)).

---

## Block A: Consensus snapshot (T − 5 min)

Copy exactly as shown. Crude stocks in mb, gas in Bcf. Build/injection +, draw/withdrawal −.

### WPSR (crude)

| Release | Data point | Investing.com forecast | Trading Economics consensus | Previous | Snapshot time (IST) |
|---|---|---|---|---|---|
| Wed 7 Oct | Crude stocks change (mb) | | | | |
| | Gasoline stocks change (mb) | | | | |
| | Distillate stocks change (mb) | | | | |
| | API actual (Tue) / API consensus (mb) | n/a | | | |
| **Thu 15 Oct (12:00 ET)** | Crude stocks change (mb) | | | | |
| | Gasoline stocks change (mb) | | | | |
| | Distillate stocks change (mb) | | | | |

### WNGSR (gas)

| Release | Data point | Investing.com forecast | Trading Economics consensus | Previous | Snapshot time (IST) |
|---|---|---|---|---|---|
| Thu 8 Oct | Net change (Bcf) | | | | |
| Thu 15 Oct | Net change (Bcf) | | | | |

---

## Block B: Actuals and surprise (within 5 minutes after the release)

`Surprise = actual − forecast`. Negative = bullish, positive = bearish. Actuals come from the EIA page. Investing.com is only for the forecast.

| Release | Data point | Actual (EIA) | Surprise vs Investing | Surprise vs Trading Economics | Same sign? | Trade allowed by sign rule? |
|---|---|---|---|---|---|---|
| Wed 7 Oct | Crude (mb) | | | | | |
| | Gasoline (mb) | | | | | |
| | Distillate (mb) | | | | | |
| | Refinery utilization change (pts) | | n/a | n/a | n/a | n/a |
| | Cushing change (mb) | | n/a | n/a | n/a | n/a |
| Thu 8 Oct | Gas net change (Bcf) | | | | | |

Sign rule: if the two sources give opposite signs, or one gives zero, the bias is unclear: **no trade**.

---

## Block C: Source behavior check (30 minutes after the release)

| Release | Investing.com forecast changed? | Trading Economics consensus changed? | Notes |
|---|---|---|---|
| Wed 7 Oct | | | |
| Thu 8 Oct | | | |

Purpose: confirm whether a site overwrites its forecast after the print (Trading Economics showed gas consensus = actual on 1 Oct).

---

## Block D: Price reaction (MCX future, 5-min execution chart; observe, do not trade)

| Release | Instrument | Range High | Range Low | Midpoint | P | R1 | R2 | S1 | S2 |
|---|---|---|---|---|---|---|---|---|---|
| Wed 7 Oct | CRUDEOIL | | | | | | | | |
| Thu 8 Oct | NATGASMINI | | | | | | | | |

| Release | First 5-min close beyond range (time, direction) | Entry (next open) | Stop (midpoint) touched? (time) | TP1 touched? | TP2 touched? | High / low in 90 min | Direction agreed with bias? |
|---|---|---|---|---|---|---|---|
| Wed 7 Oct | | | | | | | |
| Thu 8 Oct | | | | | | | |

Pivots come from the previous trading day of the same contract. Check the previous day's volume (data-quality rule, `06_data_and_capture.md` §2).

---

## Block E: Option observation (MCX chain of the traded contract)

| Release | Contract | ATM IV at T − 5 | ATM IV at T + 15 | Change (pts) | Chosen strike | Delta | Premium | Bid-ask |
|---|---|---|---|---|---|---|---|---|
| Wed 7 Oct | CRUDEOIL | | | | | | | |
| Thu 8 Oct | NATGASMINI | | | | | | | |

Purpose: measure the real IV drop (the 3-pt figure used in the chain tables is an assumption). Thu 15 Oct: CRUDEOIL options expire that day, so also record the **next-month** chain.

---

## Running summary (update weekly)

| Week | Report | Surprise (Investing) | Direction of surprise | Breakout direction | Agreed? | Result for E1 / E2 / E3 (₹ and % of account) |
|---|---|---|---|---|---|---|
| | | | | | | |

After about 50 rows per report review: hit rates, typical surprise size and SD, median IV drop, which exit design looks best. Pause rule: after 3 losing trades in a row, stop and review.
