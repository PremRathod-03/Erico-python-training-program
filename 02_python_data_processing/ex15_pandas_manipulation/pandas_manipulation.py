"""
Exercise 15: Pandas - Data Manipulation

- load a dataset and display its structure (shape, dtypes, info, head, describe)
- filter data based on conditions (e.g. sales above $1000)
"""
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def load_sales() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "sales.csv", parse_dates=["date"])


def high_value_orders(df: pd.DataFrame, threshold: float = 1000) -> pd.DataFrame:
    return df[df["sales"] > threshold]


def main() -> None:
    df = load_sales()
    print("Shape:", df.shape)
    print("\nColumns & dtypes:\n", df.dtypes)
    print("\ninfo():")
    df.info()
    print("\nFirst 5 rows:\n", df.head())
    print("\ndescribe():\n", df.describe().round(2))

    big = high_value_orders(df)
    print(f"\nOrders with sales above $1000: {len(big)} of {len(df)}")
    print(big[["order_id", "region", "product", "sales"]].head(10))

    laptops_north = df[(df["product"] == "Laptop") & (df["region"] == "North")]
    print(f"\nLaptops sold in the North: {len(laptops_north)}")
    phone_or_tablet = df[df["product"].isin(["Phone", "Tablet"]) & (df["quantity"] >= 4)]
    print(f"Phones/Tablets with quantity >= 4: {len(phone_or_tablet)}")
    print("query() version:", len(df.query("sales > 1000 and region == 'South'")), "South orders > $1000")

    out = output_dir(__file__)
    big.to_csv(out / "sales_above_1000.csv", index=False)
    print("Saved", out / "sales_above_1000.csv")


if __name__ == "__main__":
    main()
