"""
Generates the practice datasets used in this module (deterministic, seed=42).
titanic.csv is the public Kaggle/Data Science Dojo Titanic training set (891 rows).

Run once:  python generate_datasets.py
"""
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent
rng = np.random.default_rng(42)


def make_sales() -> pd.DataFrame:
    n = 200
    regions = ["North", "South", "East", "West"]
    products = ["Laptop", "Phone", "Tablet", "Monitor", "Headphones"]
    base_price = {"Laptop": 900, "Phone": 600, "Tablet": 400, "Monitor": 250, "Headphones": 80}
    product = rng.choice(products, n)
    qty = rng.integers(1, 6, n)
    price = np.array([base_price[p] for p in product]) * rng.uniform(0.85, 1.15, n)
    df = pd.DataFrame({
        "order_id": np.arange(1001, 1001 + n),
        "date": pd.date_range("2025-01-01", periods=n, freq="D").strftime("%Y-%m-%d"),
        "region": rng.choice(regions, n),
        "product": product,
        "quantity": qty,
        "unit_price": price.round(2),
    })
    df["sales"] = (df["quantity"] * df["unit_price"]).round(2)
    # inject missing values for Exercise 16
    for col, k in [("region", 8), ("unit_price", 6), ("quantity", 5)]:
        idx = rng.choice(n, k, replace=False)
        df.loc[idx, col] = np.nan
    df.loc[df["unit_price"].isna() | df["quantity"].isna(), "sales"] = np.nan
    df["quantity"] = df["quantity"].astype("Int64")
    return df


def make_messy_employees() -> pd.DataFrame:
    rows = [
        [" Emp ID", "Full Name ", "Department", "Salary", "Joining Date", "E-mail"],
    ]
    data = [
        [101, "  asha rao", "engineering", "55000", "2021-03-15", "asha@corp.com"],
        [102, "RAVI KUMAR", "Engineering ", "62000", "2020/07/01", "ravi@corp.com"],
        [103, "neha s", "HR", None, "2019-11-20", "neha@corp.com"],
        [104, "Kiran M", "hr", "48000", None, "KIRAN@CORP.COM"],
        [101, "  asha rao", "engineering", "55000", "2021-03-15", "asha@corp.com"],
        [105, "Prem R", "Data Science", "70000", "2022-01-10", None],
        [106, None, "Sales", "45,000", "2023-05-05", "sam@corp.com"],
        [107, "meera j", "sales", "-1", "2023-08-12", "meera@corp.com"],
        [102, "RAVI KUMAR", "Engineering ", "62000", "2020/07/01", "ravi@corp.com"],
        [108, "arjun p", "Data Science", "68000", "2022-09-30", "arjun@corp.com"],
    ]
    return pd.DataFrame(data, columns=rows[0])


def make_temperature_series() -> pd.DataFrame:
    days = pd.date_range("2025-01-01", "2025-12-31", freq="D")
    t = np.arange(len(days))
    seasonal = 26 + 5 * np.sin(2 * np.pi * (t - 60) / 365)
    trend = 0.004 * t
    noise = rng.normal(0, 1.4, len(days))
    return pd.DataFrame({"date": days.strftime("%Y-%m-%d"),
                         "temperature_c": (seasonal + trend + noise).round(2)})


def main() -> None:
    make_sales().to_csv(DATA_DIR / "sales.csv", index=False)
    make_messy_employees().to_csv(DATA_DIR / "employees_messy.csv", index=False)
    make_temperature_series().to_csv(DATA_DIR / "daily_temperature.csv", index=False)
    (DATA_DIR / "customer_reviews.txt").write_text(
        "Loved the laptop, battery lasts all day!\n"
        "Phone arrived late and the box was damaged.\n"
        "Great headphones for the price, but the cable feels cheap.\n",
        encoding="utf-8")
    print("Datasets written to", DATA_DIR)


if __name__ == "__main__":
    main()
