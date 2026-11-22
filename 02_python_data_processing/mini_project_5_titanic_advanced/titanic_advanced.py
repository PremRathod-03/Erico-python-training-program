"""
Mini-Project 5: Titanic Data Analysis (Part 2 - transformations & aggregation)

1-Group the data by Pclass and calculate the average age and survival rate for each class
2-Normalise the 'Age' column using Min-Max normalisation, then calculate the Z-score for 'Age'
3-Handle missing values in the 'Age' column by filling them with the mean value
4-Group the data by SexCode (0 or 1) and calculate the total number of survivors for each group
5-Create a new column indicating whether a passenger is a "child" (age < 18) or "adult" (age >= 18)
6-Create a pivot table showing the average survival rate for each Pclass and SexCode

Note: the Kaggle Titanic file has no SexCode column, so it is derived as female = 1, male = 0
(the same coding used by the Stat2Data Titanic dataset).

Run: python titanic_advanced.py
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import TITANIC_CSV, output_dir  # noqa: E402


def load(path: Path = TITANIC_CSV) -> pd.DataFrame:
    df = pd.read_csv(path)
    if "SexCode" not in df.columns:
        df["SexCode"] = (df["Sex"].str.lower() == "female").astype(int)
    return df


def class_summary(df):                                             # 1
    return df.groupby("Pclass").agg(
        avg_age=("Age", "mean"),
        survival_rate=("Survived", "mean"),
        passengers=("PassengerId", "count"),
    ).round(3)


def fill_age_with_mean(df):                                        # 3
    df = df.copy()
    df["AgeWasMissing"] = df["Age"].isna()
    df["Age"] = df["Age"].fillna(df["Age"].mean())
    return df


def normalize_age(df):                                             # 2
    df = df.copy()
    age = df["Age"]
    df["Age_MinMax"] = (age - age.min()) / (age.max() - age.min())
    df["Age_ZScore"] = (age - age.mean()) / age.std()
    return df


def survivors_by_sexcode(df):                                      # 4
    return df.groupby("SexCode")["Survived"].sum().rename(index={0: "0 (male)", 1: "1 (female)"})


def add_child_adult(df):                                           # 5
    df = df.copy()
    df["AgeCategory"] = df["Age"].apply(lambda a: "child" if a < 18 else "adult")
    return df


def survival_pivot(df):                                            # 6
    return pd.pivot_table(df, values="Survived", index="Pclass", columns="SexCode",
                          aggfunc="mean").round(3)


def main() -> None:
    df = load()

    print("1) Average age and survival rate per class")
    print(class_summary(df), "\n")

    # The Z-score/min-max are computed after filling (step 3) so every row gets a value.
    print(f"3) Missing ages before: {df['Age'].isna().sum()}, filled with mean {df['Age'].mean():.2f}")
    df = fill_age_with_mean(df)
    print(f"   Missing ages after: {df['Age'].isna().sum()}\n")

    df = normalize_age(df)
    print("2) Age normalisation (first 5 rows)")
    print(df[["Age", "Age_MinMax", "Age_ZScore"]].head().round(3))
    print(f"   Min-Max range [{df['Age_MinMax'].min():.1f}, {df['Age_MinMax'].max():.1f}],"
          f" Z-score mean {df['Age_ZScore'].mean():.3f}, std {df['Age_ZScore'].std():.3f}\n")

    print("4) Total survivors by SexCode\n", survivors_by_sexcode(df), "\n")

    df = add_child_adult(df)
    print("5) Child / adult counts\n", df["AgeCategory"].value_counts(), "\n")

    pivot = survival_pivot(df)
    print("6) Survival rate pivot (rows = Pclass, columns = SexCode)\n", pivot)

    out = output_dir(__file__)
    df.to_csv(out / "titanic_transformed.csv", index=False)
    pivot.to_csv(out / "survival_pivot.csv")

    ax = pivot.rename(columns={0: "Male (0)", 1: "Female (1)"}).plot(
        kind="bar", figsize=(8, 5), color=["#3b82f6", "#ec4899"], rot=0)
    ax.set_title("Titanic survival rate by class and sex")
    ax.set_xlabel("Passenger class")
    ax.set_ylabel("Survival rate")
    ax.set_ylim(0, 1)
    for container in ax.containers:
        ax.bar_label(container, fmt="%.2f")
    plt.tight_layout()
    plt.savefig(out / "survival_pivot.png", dpi=120)
    plt.close()
    print(f"\nSaved titanic_transformed.csv, survival_pivot.csv and survival_pivot.png to {out}")


if __name__ == "__main__":
    main()
