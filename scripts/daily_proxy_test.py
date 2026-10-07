"""Daily-horizon test: does a de-seasonalised inventory shock predict WTI / Henry Hub spot returns?

Parameters fixed before looking at results (7 Oct 2026):
- weekly change = stock_t - stock_(t-1)
- expected change = mean of the same ISO-week change over the previous 5 years (past data only)
- surprise s = change - expected; z = s / SD of the previous 260 weekly surprises (min 104; past data only)
- release day: Wednesday (crude) / Thursday (gas) after the week ending Friday, shifted +1 day when the
  Monday of that week (or Tuesday, crude) is a US federal holiday (approximate)
- returns, in % log terms: R0 = release day vs previous trading day; R1 = next day; R2 = two days later
  (both measured from the release-day close)
- strong signal: |z| >= 0.8 (the threshold in the Cushing repo). "aligned" = return in the direction of the
  bias (negative z is bullish).
- sub-periods fixed in advance.
"""
import warnings

import numpy as np
import pandas as pd
from pandas.tseries.holiday import USFederalHolidayCalendar

warnings.filterwarnings("ignore")
from eia_hist import load

H = load()
HOL = set(USFederalHolidayCalendar().holidays("1980-01-01", "2027-12-31"))


def release_date(week_end, off):
    nominal = week_end + pd.Timedelta(days=off)
    mon = nominal - pd.Timedelta(days=2 if off == 5 else 3)
    shift = 1 if mon in HOL or (off == 5 and mon + pd.Timedelta(days=1) in HOL) else 0
    return nominal + pd.Timedelta(days=shift)


def build(stock, price, off, start, min_price):
    s = stock.set_index("date")["value"].sort_index()
    df = pd.DataFrame({"d": s.diff().dropna()})
    df["woy"] = df.index.isocalendar().week.values
    exp = []
    for t in df.index:
        past = df[(df.index < t) & (df.index >= t - pd.Timedelta(days=5 * 365 + 10)) & (df.woy == df.loc[t, "woy"])]
        exp.append(past.d.mean() if len(past) >= 4 else np.nan)
    df["s"] = df.d - np.array(exp)
    df["sd"] = df.s.shift(1).rolling(260, min_periods=104).std()
    df["z"] = df.s / df.sd
    df = df.dropna(subset=["z"])
    df = df[df.index >= pd.Timestamp(start)]
    p = price.set_index("date")["value"].sort_index()
    p = p[p > min_price]
    rows = []
    for t, r in df.iterrows():
        rd = release_date(t, off)
        i = p.index.searchsorted(rd)
        if i < 1 or i + 2 >= len(p):
            continue
        d0 = p.index[i]
        if (d0 - rd).days > 3:
            continue
        rows.append(dict(week=t, release=d0, z=r.z,
                         R0=100 * np.log(p.iloc[i] / p.iloc[i - 1]),
                         R1=100 * np.log(p.iloc[i + 1] / p.iloc[i]),
                         R2=100 * np.log(p.iloc[i + 2] / p.iloc[i])))
    return pd.DataFrame(rows)


def report(name, df):
    n = len(df)
    print("\n==", name, "n =", n, df.release.min().date(), "to", df.release.max().date())
    for c in ["R0", "R1", "R2"]:
        r = df.z.corr(df[c])
        print(f"  corr(z,{c}) = {r:+.3f}  t={r * np.sqrt((n - 2) / (1 - r * r)):+.2f}")
    ex = df[df.z.abs() >= 0.8].copy()
    ex["al"] = -np.sign(ex.z)
    print(f"  |z|>=0.8: n={len(ex)}")
    for c in ["R0", "R1", "R2"]:
        a = ex.al * ex[c]
        print(f"    aligned {c}: mean {a.mean():+.3f}%  t={a.mean() / (a.std() / np.sqrt(len(a))):+.2f}  win {(a > 0).mean():.0%}")


if __name__ == "__main__":
    cr = build(H["WCESTUS1w"], H["RWTCd"], 5, "2000-01-01", 5)
    report("CRUDE commercial stocks vs WTI spot", cr)
    report("  crude 2000-2014", cr[cr.release < "2015-01-01"])
    report("  crude 2015-2026", cr[cr.release >= "2015-01-01"])
    cu = build(H["W_EPC0_SAX_YCUOK_MBBLw"], H["RWTCd"], 5, "2008-01-01", 5)
    report("CUSHING stocks vs WTI spot", cu)
    report("  cushing to 2016", cu[cu.release < "2017-01-01"])
    report("  cushing 2017-2026", cu[cu.release >= "2017-01-01"])
    gs = build(H["NW2_EPG0_SWO_R48_BCFw"], H["RNGWHHDd"], 6, "2015-01-01", 0.5)
    report("GAS storage vs Henry Hub spot", gs)
    report("  gas first half", gs[gs.release < gs.release.median()])
    report("  gas second half", gs[gs.release >= gs.release.median()])
