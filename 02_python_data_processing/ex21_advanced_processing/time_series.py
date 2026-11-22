"""
Exercise 21: Advanced Data Processing Techniques

- process time-series data (parse dates, DatetimeIndex, resample)
- extract trends with rolling averages (7-day and 30-day)
- visualise the series and the trend
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def load_series() -> pd.Series:
    df = pd.read_csv(DATA_DIR / "daily_temperature.csv", parse_dates=["date"])
    return df.set_index("date")["temperature_c"].asfreq("D").interpolate()


def main() -> None:
    s = load_series()
    print(f"{len(s)} daily readings from {s.index.min().date()} to {s.index.max().date()}")

    roll7 = s.rolling(window=7, center=True).mean()
    roll30 = s.rolling(window=30, center=True).mean()
    monthly = s.resample("MS").agg(["mean", "min", "max"]).round(2)
    print("\nMonthly summary:\n", monthly)

    hottest = roll30.idxmax()
    print(f"\nWarmest 30-day period centred on {hottest.date()} ({roll30.max():.2f} °C)")
    change = s.pct_change(periods=30).dropna()
    print(f"Largest 30-day rise: {change.max() * 100:.1f}% ending {change.idxmax().date()}")

    out = output_dir(__file__)
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(s.index, s, color="lightgray", label="Daily")
    ax.plot(roll7.index, roll7, color="#3b82f6", label="7-day rolling mean")
    ax.plot(roll30.index, roll30, color="#dc2626", linewidth=2.5, label="30-day rolling mean (trend)")
    ax.set_title("Daily temperature with rolling-average trends (2025)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(alpha=0.3)
    fig.tight_layout()
    fig.savefig(out / "rolling_trend.png", dpi=120)
    plt.close(fig)

    pd.DataFrame({"temperature": s, "rolling_7": roll7, "rolling_30": roll30}).to_csv(out / "rolling.csv")
    print("Saved rolling_trend.png and rolling.csv to", out)


if __name__ == "__main__":
    main()
