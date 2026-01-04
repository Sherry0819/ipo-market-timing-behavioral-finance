from __future__ import annotations

import argparse
from pathlib import Path
import pandas as pd

from src.io import load_inputs, attach_event_months
from src.analysis import (
    filter_ipos_with_60_months,
    estimate_betas,
    abnormal_returns,
    average_ar_car,
    abnormal_returns_beta1,
)
from src.plots import plot_avg_ar, plot_car, plot_two_cars


def main():
    parser = argparse.ArgumentParser(description="IPO post-issue returns: market timing & limits to arbitrage (event study).")
    parser.add_argument("--ipo_csv", type=str, default="data/raw/ipo_data.csv")
    parser.add_argument("--ret_csv", type=str, default="data/raw/return.csv")
    parser.add_argument("--outdir", type=str, default="reports")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    (outdir / "figures").mkdir(parents=True, exist_ok=True)

    data = load_inputs(args.ipo_csv, args.ret_csv)
    df = attach_event_months(data.ipo, data.ret)

    # Keep IPOs with at least 60 post-IPO months
    df = filter_ipos_with_60_months(df)

    # Optional time filter: IPOs from 1975-01 to 2015-12 (inclusive)
    df = df[(df["IpoDate"] >= "1975-01-01") & (df["IpoDate"] <= "2015-12-31")].copy()

    # 1) Estimate alpha/beta + idiosyncratic vol proxy (MSE) using event months 31..60
    betas = estimate_betas(df, 31, 60)
    betas.to_csv(outdir / "beta_estimates.csv", index=False)

    # Percentiles
    pct = betas["beta"].quantile([0.25, 0.50, 0.75]).rename("beta_percentiles")
    pct.to_csv(outdir / "beta_percentiles.csv")

    # 2) Abnormal returns + CAR for event months 1..30
    ar = abnormal_returns(df, betas, 1, 30)
    ar.to_csv(outdir / "abnormal_returns_1_30.csv", index=False)

    summary = average_ar_car(ar)
    summary.to_csv(outdir / "avg_ar_car_1_30.csv")

    plot_avg_ar(summary, outdir / "figures" / "avg_ar_by_event_month.png")
    plot_car(summary, outdir / "figures" / "car_1_30.png", title="CAR (Event months 1–30)")

    # 3) Limits to arbitrage split by above/below median idiosyncratic volatility (MSE)
    med_mse = betas["mse"].median()
    hi = betas[betas["mse"] > med_mse][["PERMNO"]]
    lo = betas[betas["mse"] <= med_mse][["PERMNO"]]

    ar_hi = ar[ar["PERMNO"].isin(hi["PERMNO"])]
    ar_lo = ar[ar["PERMNO"].isin(lo["PERMNO"])]

    sum_hi = average_ar_car(ar_hi)
    sum_lo = average_ar_car(ar_lo)
    sum_hi.to_csv(outdir / "avg_ar_car_high_ivol.csv")
    sum_lo.to_csv(outdir / "avg_ar_car_low_ivol.csv")

    plot_two_cars(
        sum_lo, sum_hi,
        label_a="Low idiosyncratic volatility (<= median MSE)",
        label_b="High idiosyncratic volatility (> median MSE)",
        outpath=outdir / "figures" / "car_low_vs_high_ivol.png",
        title="CAR (Event months 1–30): Limits to Arbitrage Split"
    )

    # 4) Sensitivity: assume beta=1 (alpha=0), recompute CAR
    ar_b1 = abnormal_returns_beta1(df, 1, 30)
    sum_b1 = average_ar_car(ar_b1)
    sum_b1.to_csv(outdir / "avg_ar_car_beta1.csv")

    plot_two_cars(
        summary, sum_b1,
        label_a="Market model (alpha,beta from months 31–60)",
        label_b="Assume beta=1, alpha=0",
        outpath=outdir / "figures" / "car_market_model_vs_beta1.png",
        title="CAR comparison: estimated beta vs beta=1"
    )

    print("Done. Outputs saved in:", outdir)


if __name__ == "__main__":
    main()
