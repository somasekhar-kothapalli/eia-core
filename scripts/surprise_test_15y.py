"""Daily-horizon test of the consensus surprise on 15 years (rerun of docs/05 section 2.4 on the merged tables).

Fixed before looking at results (7 Oct 2026):
- rows: usable == True, release date 2011-01-01 or later, forecast present, spot price > 0.5 on the days used
- surprise = actual - forecast; z = surprise / SD of earlier surprises only (z_exp, from build_releases.py)
- release day d0 = New York date of release_utc; returns are % log changes of EIA daily spot
  (WTI RWTC, Henry Hub RNGWHHD): R0 = d0 vs previous trading day, R1 = next day, R2 = day after that
- tests: corr(z, R0), corr(z, R1), corr(z, R2) and OLS slope of R0 on z (% per 1 SD); a draw (negative z) should lift price
- periods fixed in advance: 2011-2018, 2019-2026 (and the last 2 years for comparison with the earlier result)
- 2 instruments x 3 horizons = 6 main tests; Bonferroni |t| about 2.7
"""
from pathlib import Path

import numpy as np
import pandas as pd

from eia_hist import load

ROOT = Path(__file__).resolve().parents[1]
EIA = load()


def returns(rel, key):
    p = EIA[key].set_index("date").value.sort_index()
    p = p[p > 0.5]  # drops the negative WTI print of 20 Apr 2020
    rows = []
    for _, r in rel.iterrows():
        d0 = pd.Timestamp(r.release_et[:10])
        if d0 not in p.index:
            continue
        i = p.index.get_loc(d0)
        if i < 1 or i + 2 >= len(p):
            continue
        lr = lambda a, b: 100 * np.log(p.iloc[a] / p.iloc[b])
        rows.append(dict(d0=d0, z=r.z, s=r.s, R0=lr(i, i - 1), R1=lr(i + 1, i), R2=lr(i + 2, i + 1)))
    return pd.DataFrame(rows)


def stats(df):
    out = {"n": len(df)}
    for h in ("R0", "R1", "R2"):
        r = df.z.corr(df[h])
        out[h] = f"{r:+.3f} (t {r * np.sqrt((len(df) - 2) / (1 - r * r)):+.1f})"
    b = np.polyfit(df.z, df.R0, 1)[0]
    out["slope R0 %/SD"] = f"{b:+.2f}"
    out["same-sign hit R0"] = f"{((df.z < 0) == (df.R0 > 0)).mean():.0%}"
    return out


def main():
    tests = []
    for name, f, key, col in (("Crude (WTI spot)", "releases_crude.csv", "RWTCd", "crude_"), ("Gas (Henry Hub spot)", "releases_gas.csv", "RNGWHHDd", "")):
        d = pd.read_csv(ROOT / "data" / f)
        d = d[d.usable & d[col + "forecast"].notna() & (d.release_et.str[:4].astype(int) >= 2011)]
        d = d.rename(columns={col + "z_exp": "z", col + "surprise": "s"}).dropna(subset=["z"])
        df = returns(d, key)
        for label, sub in (("2011-2026", df), ("2011-2018", df[df.d0 < "2019-01-01"]), ("2019-2026", df[df.d0 >= "2019-01-01"]),
                           ("last 2 yrs", df[df.d0 >= "2024-11-01"]),
                           ("|z|>=1 only", df[df.z.abs() >= 1])):
            tests.append({"series": name, "sample": label, **stats(sub)})
    t = pd.DataFrame(tests)
    print(t.to_string(index=False))
    t.to_csv(ROOT / "data" / "surprise_test_15y.csv", index=False)


if __name__ == "__main__":
    main()
