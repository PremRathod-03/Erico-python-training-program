"""
Exercise 19: Data Cleaning & Preprocessing

- standardise column names
- remove duplicates
- fix text formatting, data types and invalid values
- handle missing values effectively
"""
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    def clean(name: str) -> str:
        name = re.sub(r"[^0-9a-zA-Z]+", "_", name.strip().lower())
        return name.strip("_")
    return df.rename(columns=clean)


def clean_employees(raw: pd.DataFrame) -> pd.DataFrame:
    df = standardize_columns(raw)
    df = df.drop_duplicates().copy()

    df["full_name"] = df["full_name"].str.strip().str.title()
    df["department"] = df["department"].str.strip().str.title()
    df["e_mail"] = df["e_mail"].str.strip().str.lower()

    df["salary"] = pd.to_numeric(df["salary"].astype(str).str.replace(",", ""), errors="coerce")
    df.loc[df["salary"] <= 0, "salary"] = np.nan                      # invalid values
    df["salary"] = df["salary"].fillna(df.groupby("department")["salary"].transform("median"))

    df["joining_date"] = pd.to_datetime(df["joining_date"].str.replace("/", "-"), errors="coerce")
    df["full_name"] = df["full_name"].fillna("Unknown")
    df["e_mail"] = df["e_mail"].fillna(
        df["full_name"].str.split().str[0].str.lower() + "@corp.com")
    df["joining_date_missing"] = df["joining_date"].isna()

    return df.reset_index(drop=True)


def main() -> None:
    raw = pd.read_csv(DATA_DIR / "employees_messy.csv")
    print("Raw columns:", list(raw.columns))
    print("Raw rows:", len(raw), "| duplicate rows:", raw.duplicated().sum())
    print("Missing values:\n", raw.isna().sum())

    clean = clean_employees(raw)
    print("\nClean columns:", list(clean.columns))
    print("Clean rows:", len(clean))
    print(clean.to_string())

    out = output_dir(__file__)
    clean.to_csv(out / "employees_clean.csv", index=False)
    print("\nSaved", out / "employees_clean.csv")


if __name__ == "__main__":
    main()
