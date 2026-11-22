"""
Exercise 16: Advanced Pandas - Data Handling & Aggregation

- detect and handle missing values (drop, fill with constant / mean / median, recompute)
- aggregate with groupby()
- summarise with pivot_table()
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def handle_missing(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["region"] = df["region"].fillna("Unknown")
    # unit price: fill with the median price of the same product
    df["unit_price"] = df["unit_price"].fillna(df.groupby("product")["unit_price"].transform("median"))
    # quantity: fill with the overall median (rounded to a whole number)
    df["quantity"] = df["quantity"].fillna(round(df["quantity"].median())).astype(int)
    df["sales"] = (df["quantity"] * df["unit_price"]).round(2)
    return df


def main() -> None:
    raw = pd.read_csv(DATA_DIR / "sales.csv", parse_dates=["date"])
    print("Missing values per column:\n", raw.isna().sum())
    print("\nRows with any missing value:", raw.isna().any(axis=1).sum())
    print("Option 1 - dropna():", len(raw.dropna()), "rows remain")

    clean = handle_missing(raw)
    print("Option 2 - fill:", clean.isna().sum().sum(), "missing values remain")

    print("\ngroupby - revenue by region:")
    print(clean.groupby("region")["sales"].sum().round(2).sort_values(ascending=False))

    print("\ngroupby with several aggregations by product:")
    agg = clean.groupby("product").agg(
        orders=("order_id", "count"),
        units=("quantity", "sum"),
        revenue=("sales", "sum"),
        avg_order=("sales", "mean"),
    ).round(2)
    print(agg)

    clean["month"] = clean["date"].dt.strftime("%Y-%m")
    pivot = pd.pivot_table(clean, values="sales", index="region", columns="product",
                           aggfunc="sum", fill_value=0, margins=True, margins_name="Total").round(0)
    print("\npivot_table - revenue by region x product:")
    print(pivot)

    out = output_dir(__file__)
    clean.to_csv(out / "sales_clean.csv", index=False)
    pivot.to_csv(out / "region_product_pivot.csv")
    print("\nSaved cleaned data and pivot to", out)


if __name__ == "__main__":
    main()
