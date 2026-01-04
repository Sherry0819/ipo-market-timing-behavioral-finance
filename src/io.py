from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import pandas as pd
import numpy as np


@dataclass
class IPOData:
    ipo: pd.DataFrame   # columns: Company, Permno, IpoDate
    ret: pd.DataFrame   # columns: PERMNO, date, RET, sprtrn


def _to_month_period(x: pd.Series) -> pd.PeriodIndex:
    return pd.to_datetime(x).dt.to_period("M")


def load_inputs(ipo_csv: str | Path, ret_csv: str | Path) -> IPOData:
    ipo = pd.read_csv(ipo_csv)
    ipo = ipo.rename(columns={"Permno": "PERMNO"})
    ipo["PERMNO"] = pd.to_numeric(ipo["PERMNO"], errors="coerce").astype("Int64")
    ipo["IpoDate"] = pd.to_datetime(ipo["IpoDate"], errors="coerce")
    ipo = ipo.dropna(subset=["PERMNO", "IpoDate"]).copy()

    ret = pd.read_csv(ret_csv)
    ret["PERMNO"] = pd.to_numeric(ret["PERMNO"], errors="coerce").astype("Int64")
    ret["date"] = pd.to_datetime(ret["date"], errors="coerce")

    # Clean RET: WRDS/CRSP sometimes uses non-numeric codes (e.g., 'C')
    ret["RET"] = pd.to_numeric(ret["RET"], errors="coerce")
    ret["sprtrn"] = pd.to_numeric(ret["sprtrn"], errors="coerce")

    ret = ret.dropna(subset=["PERMNO", "date", "sprtrn"]).copy()
    return IPOData(ipo=ipo, ret=ret)


def attach_event_months(ipo: pd.DataFrame, ret: pd.DataFrame) -> pd.DataFrame:
    """
    Merge IPO metadata onto monthly return rows and create event_month:
      event_month = 1 for the first calendar month AFTER the IPO month,
      event_month = 2 for the next month, ...
    """
    ipo = ipo.copy()
    ret = ret.copy()

    ipo["ipo_m"] = ipo["IpoDate"].dt.to_period("M")
    ret["m"] = ret["date"].dt.to_period("M")

    df = ret.merge(ipo[["PERMNO", "Company", "IpoDate", "ipo_m"]], on="PERMNO", how="inner")

    # months since IPO month; +1 makes first month after IPO month = 1
    df["event_month"] = (df["m"] - df["ipo_m"]).apply(lambda p: p.n)  # integer months difference
    df["event_month"] = df["event_month"].astype(int)

    # keep months AFTER IPO month (event_month >= 1)
    df = df[df["event_month"] >= 1].copy()
    return df
