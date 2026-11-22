"""
Exercise 13: Understanding Data Processing

Part A - identify structured vs semi-structured vs unstructured data in the given datasets.
Part B - the five stages of data processing (see README.md in this folder for the write-up),
         demonstrated end to end on the sales dataset.
"""
import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def classify(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix in {".csv", ".tsv", ".xlsx"}:
        df = pd.read_csv(path, nrows=5)
        return "Structured", f"fixed schema: {len(df.columns)} columns {list(df.columns)[:4]}..."
    if suffix in {".json", ".xml"}:
        return "Semi-structured", "self-describing keys/tags, schema can vary per record"
    if suffix in {".txt", ".log", ".jpg", ".png", ".mp3", ".mp4", ".pdf"}:
        return "Unstructured", "no predefined schema; needs parsing / NLP / vision to extract fields"
    return "Unknown", "-"


def five_stages_demo(out: Path) -> None:
    # 1. Collection
    raw = pd.read_csv(DATA_DIR / "sales.csv")
    print(f"1. Collection   : loaded {len(raw)} raw sales records")
    # 2. Preparation (cleaning)
    prepared = raw.dropna(subset=["sales"]).copy()
    prepared["region"] = prepared["region"].fillna("Unknown")
    print(f"2. Preparation  : dropped {len(raw) - len(prepared)} rows with missing sales, filled regions")
    # 3. Input (convert to a machine-usable form)
    prepared["date"] = pd.to_datetime(prepared["date"])
    prepared["month"] = prepared["date"].dt.to_period("M").astype(str)
    print("3. Input        : parsed dates, derived a month column")
    # 4. Processing
    summary = prepared.groupby("month")["sales"].sum().round(2)
    print("4. Processing   : aggregated monthly revenue")
    # 5. Output & storage
    summary.to_csv(out / "monthly_sales.csv")
    print(f"5. Output/Store : saved {out / 'monthly_sales.csv'}")
    print(summary.to_string())


def main() -> None:
    out = output_dir(__file__)
    sample_json = out / "orders.json"
    sample_json.write_text(json.dumps([{"id": 1, "items": ["pen", "book"]},
                                       {"id": 2, "coupon": "NEW10"}], indent=2))

    print("Part A - classifying datasets")
    for path in [DATA_DIR / "titanic.csv", DATA_DIR / "sales.csv",
                 sample_json, DATA_DIR / "customer_reviews.txt"]:
        kind, why = classify(path)
        print(f"  {path.name:<22} -> {kind:<16} ({why})")

    print("\nPart B - five stages of data processing")
    five_stages_demo(out)


if __name__ == "__main__":
    main()
