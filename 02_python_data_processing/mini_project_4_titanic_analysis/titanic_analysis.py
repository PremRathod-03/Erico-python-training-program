"""
Mini-Project 4: Titanic Data Analysis (Part 1)

 1-Load the Titanic dataset and display its structure
 2-Count the number of passengers in each class (1st, 2nd, 3rd)
 3-Count the number of male and female passengers in each class
 4-Calculate the percentage of female passengers who survived
 5-Count the survival rate for male and female passengers
 6-Calculate the median age of male and female passengers
 7-Calculate the average age of survivors vs non-survivors
 8-Filter passengers above the age of 40 and calculate their average age
 9-Add an age-group column ('Child', 'Adult', 'Senior') based on age
10-Select survivors in 1st class (Pclass == 1) and calculate their average fare
11-Save the cleaned dataset to a new CSV file after the transformations

Run: python titanic_analysis.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import TITANIC_CSV, output_dir  # noqa: E402

CLASS_NAMES = {1: "1st", 2: "2nd", 3: "3rd"}


def load(path: Path = TITANIC_CSV) -> pd.DataFrame:
    return pd.read_csv(path)


def passengers_per_class(df):
    return df["Pclass"].value_counts().sort_index().rename(index=CLASS_NAMES)


def gender_per_class(df):
    return pd.crosstab(df["Pclass"].map(CLASS_NAMES), df["Sex"])


def pct_females_survived(df) -> float:
    females = df[df["Sex"] == "female"]
    return round(females["Survived"].mean() * 100, 2)


def survival_rate_by_sex(df):
    return (df.groupby("Sex")["Survived"].mean() * 100).round(2)


def median_age_by_sex(df):
    return df.groupby("Sex")["Age"].median()


def avg_age_by_survival(df):
    return df.groupby("Survived")["Age"].mean().round(2).rename(index={0: "Did not survive", 1: "Survived"})


def over_40(df):
    return df[df["Age"] > 40]


def add_age_group(df):
    df = df.copy()
    df["AgeGroup"] = pd.cut(df["Age"], bins=[0, 17, 59, np.inf], right=True,
                            labels=["Child", "Adult", "Senior"], include_lowest=True)
    df["AgeGroup"] = df["AgeGroup"].cat.add_categories("Unknown").fillna("Unknown")
    return df


def first_class_survivors_avg_fare(df) -> float:
    return round(df[(df["Pclass"] == 1) & (df["Survived"] == 1)]["Fare"].mean(), 2)


def clean(df):
    """Transformations applied before saving the cleaned dataset."""
    df = add_age_group(df)
    df["AgeMissing"] = df["Age"].isna()
    df["Embarked"] = df["Embarked"].fillna(df["Embarked"].mode()[0])
    df["HasCabin"] = df["Cabin"].notna()
    df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
    df["SexCode"] = (df["Sex"] == "female").astype(int)      # female = 1, male = 0
    return df.drop(columns=["Cabin"])


def main() -> None:
    df = load()

    print("1) Dataset structure")
    print(f"   {df.shape[0]} rows x {df.shape[1]} columns")
    df.info()
    print(df.head(), "\n")

    print("2) Passengers per class\n", passengers_per_class(df), "\n")
    print("3) Male/female passengers per class\n", gender_per_class(df), "\n")
    print(f"4) Female passengers who survived: {pct_females_survived(df)}%\n")
    print("5) Survival rate (%) by sex\n", survival_rate_by_sex(df), "\n")
    print("6) Median age by sex\n", median_age_by_sex(df), "\n")
    print("7) Average age: survivors vs non-survivors\n", avg_age_by_survival(df), "\n")

    older = over_40(df)
    print(f"8) Passengers above 40: {len(older)}, average age {older['Age'].mean():.2f}\n")

    grouped = add_age_group(df)
    print("9) Age groups\n", grouped["AgeGroup"].value_counts(), "\n")

    print(f"10) Average fare of 1st-class survivors: £{first_class_survivors_avg_fare(df)}\n")

    out = output_dir(__file__)
    cleaned = clean(df)
    path = out / "titanic_cleaned.csv"
    cleaned.to_csv(path, index=False)
    print(f"11) Cleaned dataset saved to {path} ({cleaned.shape[0]} rows, {cleaned.shape[1]} columns)")


if __name__ == "__main__":
    main()
