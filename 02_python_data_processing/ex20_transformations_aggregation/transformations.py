"""
Exercise 20: Data Transformations & Aggregation

- groupby operations
- pivot tables
- Min-Max normalisation:  x' = (x - min) / (max - min)          -> range [0, 1]
- Z-score normalisation:  z  = (x - mean) / std                  -> mean 0, std 1
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def min_max(series: pd.Series) -> pd.Series:
    rng = series.max() - series.min()
    return (series - series.min()) / rng if rng else series * 0


def z_score(series: pd.Series) -> pd.Series:
    std = series.std()   # sample std (ddof=1), same as scipy.stats.zscore(ddof=1)
    return (series - series.mean()) / std if std else series * 0


def main() -> None:
    df = pd.read_csv(DATA_DIR / "sales.csv").dropna(subset=["sales", "region"])

    print("groupby region -> total, mean, count of sales")
    print(df.groupby("region")["sales"].agg(["sum", "mean", "count"]).round(2))

    print("\ngroupby [region, product] -> units sold (top 6)")
    print(df.groupby(["region", "product"])["quantity"].sum().sort_values(ascending=False).head(6))

    print("\npivot_table: average order value, region x product")
    print(df.pivot_table(values="sales", index="region", columns="product", aggfunc="mean").round(0))

    df["sales_minmax"] = min_max(df["sales"])
    df["sales_zscore"] = z_score(df["sales"])
    print("\nNormalised sales (first 5):")
    print(df[["order_id", "sales", "sales_minmax", "sales_zscore"]].head().round(3))
    print(f"min-max range: [{df['sales_minmax'].min():.1f}, {df['sales_minmax'].max():.1f}]")
    print(f"z-score mean {df['sales_zscore'].mean():.3f}, std {df['sales_zscore'].std():.3f}")

    out = output_dir(__file__)
    df.to_csv(out / "sales_normalized.csv", index=False)
    print("Saved", out / "sales_normalized.csv")


if __name__ == "__main__":
    main()
