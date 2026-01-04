from __future__ import annotations

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_avg_ar(summary: pd.DataFrame, outpath: str | Path):
    plt.figure()
    plt.plot(summary.index, summary["avg_AR"].values)
    plt.axhline(0, linewidth=0.8)
    plt.title("Average Abnormal Return by Event Month")
    plt.xlabel("Event month")
    plt.ylabel("Average AR")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def plot_car(summary: pd.DataFrame, outpath: str | Path, title: str = "Cumulative Abnormal Return (CAR)"):
    plt.figure()
    plt.plot(summary.index, summary["CAR"].values)
    plt.axhline(0, linewidth=0.8)
    plt.title(title)
    plt.xlabel("Event month")
    plt.ylabel("CAR")
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()


def plot_two_cars(sum_a: pd.DataFrame, sum_b: pd.DataFrame, label_a: str, label_b: str, outpath: str | Path, title: str):
    plt.figure()
    plt.plot(sum_a.index, sum_a["CAR"].values, label=label_a)
    plt.plot(sum_b.index, sum_b["CAR"].values, label=label_b)
    plt.axhline(0, linewidth=0.8)
    plt.title(title)
    plt.xlabel("Event month")
    plt.ylabel("CAR")
    plt.legend()
    plt.tight_layout()
    plt.savefig(outpath, dpi=200)
    plt.close()
