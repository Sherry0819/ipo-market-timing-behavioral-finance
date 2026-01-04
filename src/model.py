from __future__ import annotations

from dataclasses import dataclass
import pandas as pd
import statsmodels.api as sm


@dataclass
class BetaEst:
    alpha: float
    beta: float
    mse: float
    nobs: int


def estimate_market_model(y: pd.Series, mkt: pd.Series) -> BetaEst:
    """OLS: y = alpha + beta * mkt + eps"""
    df = pd.concat([y, mkt], axis=1).dropna()
    df.columns = ["RET", "MKT"]
    if len(df) < 12:
        return BetaEst(alpha=float("nan"), beta=float("nan"), mse=float("nan"), nobs=len(df))

    X = sm.add_constant(df["MKT"])
    res = sm.OLS(df["RET"], X).fit()
    mse = float(res.mse_resid)
    return BetaEst(alpha=float(res.params["const"]), beta=float(res.params["MKT"]), mse=mse, nobs=int(res.nobs))
