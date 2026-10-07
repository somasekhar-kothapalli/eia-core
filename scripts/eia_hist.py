"""Load every EIA history file in data/eia/*.xls (weekly/daily series from eia.gov/dnav/pet/hist_xls) into DataFrames.

    from eia_hist import load
    H = load()                 # {"WCESTUS1w": DataFrame(date, value), ...}  key = file name without .xls

Units are EIA's own (stocks in thousand barrels or Bcf, prices in $, utilization in %); see each file's "Contents" sheet.
"""
from pathlib import Path

import pandas as pd

EIA_DIR = Path(__file__).resolve().parents[1] / "data" / "eia"


def load():
    out = {}
    for f in sorted(EIA_DIR.glob("*.xls")):
        d = pd.read_excel(f, sheet_name="Data 1", skiprows=2, header=0)  # rows: back-link, source key, then "Date | name"
        d = d.iloc[:, :2]
        d.columns = ["date", "value"]
        d = d.dropna()
        d["date"] = pd.to_datetime(d["date"])
        out[f.stem] = d.reset_index(drop=True)
    return out
