"""Merge the Investing.com tables into one row per release and validate release times and actuals.

Reads  data/consensus/<series>_table.csv and data/eia/*.xls (free EIA history, via eia_hist.py).
Writes data/releases_crude.csv   (WPSR: crude + gasoline + distillates + API, surprises)
       data/releases_gas.csv     (WNGSR: net change, surprise)
       data/release_checks.csv   (every release whose time, weekday or actual did not pass; see docs/06)

Checks per release (America/New_York clock):
  time_status:  ok = expected weekday at 10:30 ET | holiday_shift = a US federal holiday in the release week and a
                later day or a time between 10:30 and 12:00 ET | unexplained = anything else (look at these by hand)
  actual_check: Investing actual vs the change in EIA's own weekly stock series (week ending = last Friday before release)
Surprise = actual - forecast (negative = bullish). z_exp = surprise / SD of earlier surprises only (min 52 weeks).
"""
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from eia_hist import load
from pandas.tseries.holiday import USFederalHolidayCalendar

ROOT = Path(__file__).resolve().parents[1]
CONS = ROOT / "data" / "consensus"
ET = ZoneInfo("America/New_York")
HOL = set(USFederalHolidayCalendar().holidays("1990-01-01", "2027-12-31"))
EIA = load()


def load(name, scale):
    d = pd.read_csv(CONS / f"{name}_table.csv")
    d = d[d.actual.notna()].copy()  # completed releases only
    for c in ("actual", "forecast", "previous"):
        d[c] = pd.to_numeric(d[c].astype("string").str.replace(r"[MB]$", "", regex=True)) * scale
    d["utc"] = pd.to_datetime(d.release_utc, utc=True)
    d["et"] = d.utc.dt.tz_convert(ET)
    d["surprise"] = d.actual - d.forecast
    sd = d.sort_values("utc").surprise.expanding(min_periods=52).std().shift(1)  # earlier weeks only
    d["z_exp"] = d.surprise / sd.reindex(d.index)
    return d.sort_values("utc").reset_index(drop=True)


def time_status(et, want_weekday):
    week = [et.date() - pd.Timedelta(days=et.weekday()) + pd.Timedelta(days=i) for i in range(5)]
    holiday = any(pd.Timestamp(x) in HOL for x in week)
    if et.weekday() == want_weekday and (et.hour, et.minute) == (10, 30):
        return "ok"
    in_slot = (10, 30) <= (et.hour, et.minute) <= (12, 0)  # delayed releases: 11:00 ET historically, 12:00 ET since 2025
    return "holiday_shift" if holiday and in_slot else "unexplained"


def check_actual(d, eia_key, factor):
    s = EIA[eia_key].set_index("date").value.sort_index()
    out = []
    for et, act in zip(d.et, d.actual):
        d0 = pd.Timestamp(et.date())
        fri = d0 - pd.Timedelta(days=(d0.weekday() - 4) % 7 or 7)
        if fri not in s.index or fri - pd.Timedelta(days=7) not in s.index:
            out.append("no_eia_row"); continue
        diff = (s[fri] - s[fri - pd.Timedelta(days=7)]) * factor
        out.append("ok" if abs(diff - act) < 0.5 else f"diff {act - diff:+.3f}")
    return out


def main():
    crude = load("crude_stocks", 1)  # million barrels
    crude["time_status"] = [time_status(t, 2) for t in crude.et]
    crude["actual_check"] = check_actual(crude, "WCESTUS1w", 1 / 1000)  # EIA is in thousand barrels
    gas = load("gas_storage", 1)  # Bcf
    gas["time_status"] = [time_status(t, 3) for t in gas.et]
    gas["actual_check"] = check_actual(gas, "NW2_EPG0_SWO_R48_BCFw", 1)

    out = crude[["utc", "release_date_shown", "actual", "forecast", "previous", "surprise", "z_exp", "time_status", "actual_check"]].rename(
        columns={c: f"crude_{c}" for c in ("actual", "forecast", "previous", "surprise", "z_exp")})
    for name, tag in (("gasoline", "gaso"), ("distillates", "dist")):
        p = load(name, 1)[["utc", "actual", "forecast", "surprise", "z_exp"]]
        p = pd.merge_asof(out[["utc"]], p, on="utc", direction="nearest", tolerance=pd.Timedelta(days=1))
        for c in ("actual", "forecast", "surprise", "z_exp"):
            out[f"{tag}_{c}"] = p[c].values
    api = load("api_crude", 1)[["utc", "actual", "forecast", "surprise"]].rename(columns={"utc": "api_utc"})
    a = pd.merge_asof(out[["utc"]], api, left_on="utc", right_on="api_utc", direction="backward", tolerance=pd.Timedelta(days=8))
    for c in ("api_utc", "actual", "forecast", "surprise"):
        out[c if c == "api_utc" else f"api_{c}"] = a[c].values
    out["usable"] = out.time_status != "unexplained"
    out.insert(1, "release_et", crude.et.dt.strftime("%Y-%m-%d %a %H:%M"))
    out.to_csv(ROOT / "data" / "releases_crude.csv", index=False)

    g = gas[["utc", "release_date_shown", "actual", "forecast", "previous", "surprise", "z_exp", "time_status", "actual_check"]]
    g = g.assign(usable=g.time_status != "unexplained")
    g.insert(1, "release_et", gas.et.dt.strftime("%Y-%m-%d %a %H:%M"))
    g.to_csv(ROOT / "data" / "releases_gas.csv", index=False)

    bad = []
    for tag, df in (("WPSR", out), ("WNGSR", g)):
        x = df[(df.time_status != "ok") | ~df.actual_check.isin(["ok", "no_eia_row"])].copy()
        x.insert(0, "report", tag)
        bad.append(x[["report", "utc", "release_et", "time_status", "actual_check"]])
    pd.concat(bad).to_csv(ROOT / "data" / "release_checks.csv", index=False)

    for tag, df in (("WPSR crude", out), ("WNGSR gas", g)):
        print(f"{tag}: {len(df)} releases {df.utc.min().date()} to {df.utc.max().date()} | time {df.time_status.value_counts().to_dict()} "
              f"| actual vs EIA {df.actual_check.str.split().str[0].value_counts().to_dict()}")


if __name__ == "__main__":
    main()
