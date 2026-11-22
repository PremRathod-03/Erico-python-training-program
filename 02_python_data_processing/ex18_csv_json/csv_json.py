"""
Exercise 18: Working with CSV & JSON Files

- read a dataset from CSV and analyse its structure
- convert the data to JSON (records + nested/grouped form) and read it back
"""
import csv
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def analyse_structure(df: pd.DataFrame) -> pd.DataFrame:
    return pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "non_null": df.notna().sum(),
        "missing": df.isna().sum(),
        "unique": df.nunique(),
        "example": df.iloc[0],
    })


def csv_to_json_stdlib(csv_path: Path, json_path: Path) -> int:
    """Pure-Python conversion with the csv and json modules."""
    with open(csv_path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(rows, f, indent=2)
    return len(rows)


def main() -> None:
    out = output_dir(__file__)
    csv_path = DATA_DIR / "titanic.csv"
    df = pd.read_csv(csv_path)

    print(f"Rows: {df.shape[0]}, Columns: {df.shape[1]}")
    print(analyse_structure(df).to_string())

    # 1) records orient: one JSON object per row
    records_path = out / "titanic_records.json"
    df.to_json(records_path, orient="records", indent=2)

    # 2) nested JSON grouped by class
    nested = {
        f"class_{cls}": grp[["Name", "Sex", "Age", "Survived"]].head(3).to_dict(orient="records")
        for cls, grp in df.groupby("Pclass")
    }
    (out / "titanic_sample_by_class.json").write_text(json.dumps(nested, indent=2), encoding="utf-8")

    # 3) stdlib conversion
    n = csv_to_json_stdlib(DATA_DIR / "sales.csv", out / "sales.json")

    back = pd.read_json(records_path)
    print(f"\nWrote {records_path.name} ({len(back)} records, round-trip shape {back.shape})")
    print(f"Wrote titanic_sample_by_class.json and sales.json ({n} rows via csv/json modules)")


if __name__ == "__main__":
    main()
