"""
Exercise 17: Data Visualization with Matplotlib

Creates line, bar, horizontal bar, scatter, histogram, pie and box plots,
customised for readability (titles, labels, grid, legends, annotations, tight layout).
Figures are saved to ./output/
"""
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common import DATA_DIR, output_dir  # noqa: E402


def main() -> None:
    out = output_dir(__file__)
    sales = pd.read_csv(DATA_DIR / "sales.csv", parse_dates=["date"]).dropna(subset=["sales"])
    titanic = pd.read_csv(DATA_DIR / "titanic.csv")

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(2, 3, figsize=(16, 9))
    fig.suptitle("Exercise 17 - Matplotlib chart gallery", fontsize=16, fontweight="bold")

    # 1. line - monthly revenue
    monthly = sales.set_index("date")["sales"].resample("MS").sum()
    ax = axes[0, 0]
    ax.plot(monthly.index, monthly.values, marker="o", color="#2563eb", linewidth=2)
    ax.set_title("Monthly revenue")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue ($)")
    peak = monthly.idxmax()
    ax.annotate(f"peak ${monthly.max():,.0f}", xy=(peak, monthly.max()),
                xytext=(10, -25), textcoords="offset points", arrowprops={"arrowstyle": "->"})
    ax.tick_params(axis="x", rotation=30)

    # 2. bar - revenue by product
    by_product = sales.groupby("product")["sales"].sum().sort_values()
    ax = axes[0, 1]
    bars = ax.barh(by_product.index, by_product.values, color="#16a34a")
    ax.bar_label(bars, labels=[f"${v/1000:.0f}k" for v in by_product.values], padding=3)
    ax.set_title("Revenue by product")
    ax.set_xlabel("Revenue ($)")

    # 3. scatter - quantity vs sales
    ax = axes[0, 2]
    for product, grp in sales.groupby("product"):
        ax.scatter(grp["unit_price"], grp["sales"], label=product, alpha=0.7, s=25)
    ax.set_title("Unit price vs order value")
    ax.set_xlabel("Unit price ($)")
    ax.set_ylabel("Order value ($)")
    ax.legend(fontsize=8)

    # 4. histogram - Titanic ages
    ax = axes[1, 0]
    ax.hist(titanic["Age"].dropna(), bins=20, color="#9333ea", edgecolor="white")
    ax.axvline(titanic["Age"].mean(), color="black", linestyle="--", label=f"mean {titanic['Age'].mean():.1f}")
    ax.set_title("Titanic passenger ages")
    ax.set_xlabel("Age")
    ax.set_ylabel("Passengers")
    ax.legend()

    # 5. pie - passengers by class
    ax = axes[1, 1]
    counts = titanic["Pclass"].value_counts().sort_index()
    ax.pie(counts, labels=[f"Class {c}" for c in counts.index], autopct="%1.0f%%",
           startangle=90, colors=["#f59e0b", "#3b82f6", "#ef4444"])
    ax.set_title("Passengers by class")

    # 6. box plot - fare by class
    ax = axes[1, 2]
    data = [titanic.loc[titanic["Pclass"] == c, "Fare"] for c in (1, 2, 3)]
    ax.boxplot(data, tick_labels=["1st", "2nd", "3rd"], showfliers=False)
    ax.set_title("Fare by class (outliers hidden)")
    ax.set_ylabel("Fare (£)")

    fig.tight_layout()
    path = out / "chart_gallery.png"
    fig.savefig(path, dpi=120)
    plt.close(fig)
    print("Saved", path)


if __name__ == "__main__":
    main()
