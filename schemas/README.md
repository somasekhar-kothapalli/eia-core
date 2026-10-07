# Schemas

**`release_event.schema.json`** (v2.0, JSON Schema draft 2020-12): one record per WPSR (crude) or WNGSR (gas) release. One shape for both instruments and for backfilled history, backtest runs and live trading. The earlier two-schema version is in `../archive/schemas_v1/`.

## Shape

| Block | Holds | Filled when |
|---|---|---|
| `event_id`, `mode`, `status`, `report`, `instrument`, `release` | Identity, mode (`live` / `backfill` / `backtest`), lifecycle status, scheduled UTC time (handles holiday-delayed releases) | at creation |
| `metrics[]` | Each data point: `role` (trigger / flag / context), `actual`, `previous`, `consensus[]` per source (primary / cross-check, pre-release or backfilled, timestamp), derived `surprise` | consensus at T-5; actuals after the print |
| `bias` | Direction (bullish / bearish / unclear), rule result (allowed / blocked), reasons | after the print |
| `levels` | Previous-day high/low/close with a volume check, pivots, opening range and midpoint, pointer to the bar CSV (`bars_ref`) | previous day before the release; range after 15 minutes |
| `signal` | The price-only breakout (direction, entry, stop, targets) and its outcome, **recorded even when the data rule blocks the trade** | after the window |
| `trade` | `taken` flag with `skip_reason`, the option (strike, delta, premium, IV before/after), risk in INR and %, outcome | when a trade is taken |
| `config` | Strategy version and parameters (timeframe, stop rule, exit design, targets...) | at run time |
| `data_quality`, `provenance` | Flags (backfilled consensus, thin volume, roll suspect...) and sources | any time |

## Use

- **Live:** create the record before the release (`status: scheduled`, previous-day levels), fill consensus at T-5 min (`pre_release`), actuals and bias after the print (`released`), then signal, trade and outcome after the 90-minute window (`closed`). After review set `reviewed`.
- **Backfill:** reconstruct past releases from Investing.com history, EIA files and the bar CSVs (`mode: backfill`, consensus `capture_type: backfilled`).
- **Backtest:** apply `config` to the same records and write the results into `signal` and `trade` with `mode: backtest`, in a separate run folder (same `event_id`). Because live and backtest records share one structure and one `config`, the same code reads both.
- **Bars stay in CSV** (`data/`); records point to them through `levels.bars_ref`. Records live in `records/` (one file per event, `{event_id}.json`).

## Conventions

Units: stocks in mb (crude) or Bcf (gas); prices and stops in points of the MCX future; money in INR. Build/injection positive, draw/withdrawal negative; surprise = actual − consensus (negative = bullish). All timestamps ISO 8601 UTC with `Z`. Missing means `null` or an empty array, never zero.

## Examples (validated against the schema; pivots and opening range checked against `data/`)

- `examples/WPSR-2026-09-30_backfill.json`: crude, closed, trade blocked by the conflict rule, price-only outcome −42 points.
- `examples/WNGSR-2026-10-01_backfill.json`: gas, closed, trade blocked by the sign rule, price-only outcome −1.8 points.
- `examples/WPSR-2026-10-07_live_scheduled.json`: a live record before the release.
