"""
Exercise 14: Working with NumPy

- create arrays (from lists, arange, linspace, zeros/ones, random)
- element-wise operations and broadcasting
- statistics: mean, median, standard deviation (+ min/max/percentiles)
"""
import numpy as np


def describe(arr: np.ndarray) -> dict:
    return {
        "mean": float(np.mean(arr)),
        "median": float(np.median(arr)),
        "std": float(np.std(arr)),
        "min": float(np.min(arr)),
        "max": float(np.max(arr)),
    }


def main() -> None:
    a = np.array([10, 20, 30, 40, 50])
    b = np.arange(1, 6)                      # [1 2 3 4 5]
    grid = np.arange(1, 13).reshape(3, 4)
    print("a =", a, "| b =", b)
    print("linspace(0, 1, 5) =", np.linspace(0, 1, 5))
    print("zeros/ones:", np.zeros(3), np.ones((2, 2)).tolist())

    print("\nElement-wise operations")
    print("  a + b  =", a + b)
    print("  a - b  =", a - b)
    print("  a * b  =", a * b)
    print("  a / b  =", a / b)
    print("  a ** 2 =", a ** 2)
    print("  sqrt(a)=", np.sqrt(a).round(2))
    print("  a > 25 =", a > 25, "->", a[a > 25])

    print("\nBroadcasting: grid * [1, 10, 100, 1000]")
    print(grid * np.array([1, 10, 100, 1000]))
    print("Column sums:", grid.sum(axis=0), "| row means:", grid.mean(axis=1))

    print("\nStatistics on exam scores")
    rng = np.random.default_rng(7)
    scores = rng.normal(loc=70, scale=12, size=50).clip(0, 100).round(1)
    for k, v in describe(scores).items():
        print(f"  {k:<6} = {v:.2f}")
    print("  25th/75th percentile =", np.percentile(scores, [25, 75]).round(2))


if __name__ == "__main__":
    main()
