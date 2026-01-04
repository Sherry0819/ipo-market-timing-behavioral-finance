from __future__ import annotations

import numpy as np
import pandas as pd

from .model import estimate_market_model


def filter_ipos_with_60_months(df: pd.DataFrame) -> pd.DataFrame:
    """Keep IPOs that have the possibility of at least 60 post-IPO months."""
    max_em = df.groupby("PERMNO")["event_month"].max()
    keep = max_em[max_em >= 60].index
    return df[df["PERMNO"].isin(keep)].copy()


def estimate_betas(df: pd.DataFrame, start_em: int = 31, end_em: int = 60) -> pd.DataFrame:
    """Estimate alpha/beta/mse per IPO using event months [start_em, end_em]."""
    out = []
    for permno, g in df.groupby("PERMNO"):
        g_est = g[(g["event_month"] >= start_em) & (g["event_month"] <= end_em)]
        est = estimate_market_model(g_est["RET"], g_est["sprtrn"])
        out.append({
            "PERMNO": permno,
            "Company": g["Company"].iloc[0],
            "alpha": est.alpha,
            "beta": est.beta,
            "mse": est.mse,
            "nobs": est.nobs,
        })
    return pd.DataFrame(out)


def abnormal_returns(df: pd.DataFrame, betas: pd.DataFrame, em_start: int = 1, em_end: int = 30) -> pd.DataFrame:
    """Compute AR and CAR for event months 1..30 using estimated alpha/beta."""
    d = df.merge(betas[["PERMNO", "alpha", "beta", "mse"]], on="PERMNO", how="inner")
    d = d[(d["event_month"] >= em_start) & (d["event_month"] <= em_end)].copy()
    d["AR"] = d["RET"] - (d["alpha"] + d["beta"] * d["sprtrn"])
    return d


def average_ar_car(ar_df: pd.DataFrame) -> pd.DataFrame:
    """Average AR across IPOs by event month; CAR is cumulative sum of avg AR."""
    avg_ar = ar_df.groupby("event_month")["AR"].mean().sort_index()
    car = avg_ar.cumsum()
    out = pd.DataFrame({"avg_AR": avg_ar, "CAR": car})
    return out


def abnormal_returns_beta1(df: pd.DataFrame, em_start: int = 1, em_end: int = 30) -> pd.DataFrame:
    """AR assuming beta=1 and alpha=0."""
    d = df[(df["event_month"] >= em_start) & (df["event_month"] <= em_end)].copy()
    d["AR"] = d["RET"] - 1.0 * d["sprtrn"]
    return d
