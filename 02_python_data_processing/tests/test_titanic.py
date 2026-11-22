"""Sanity tests for the Titanic mini-projects (known values for the 891-row Kaggle set)."""
import sys
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(MODULE / "mini_project_4_titanic_analysis"))
sys.path.insert(0, str(MODULE / "mini_project_5_titanic_advanced"))
sys.path.insert(0, str(MODULE))

import titanic_advanced as mp5   # noqa: E402
import titanic_analysis as mp4   # noqa: E402


class TestTitanicPart1(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = mp4.load()

    def test_class_counts(self):
        self.assertEqual(mp4.passengers_per_class(self.df).to_dict(), {"1st": 216, "2nd": 184, "3rd": 491})

    def test_female_survival(self):
        self.assertAlmostEqual(mp4.pct_females_survived(self.df), 74.2, places=1)

    def test_age_groups_cover_all_rows(self):
        grouped = mp4.add_age_group(self.df)
        self.assertEqual(grouped["AgeGroup"].value_counts().sum(), len(self.df))
        self.assertEqual(grouped.loc[grouped["Age"] == 17, "AgeGroup"].unique().tolist(), ["Child"])

    def test_clean_has_no_cabin(self):
        self.assertNotIn("Cabin", mp4.clean(self.df).columns)


class TestTitanicPart2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = mp5.normalize_age(mp5.fill_age_with_mean(mp5.load()))

    def test_no_missing_age(self):
        self.assertEqual(self.df["Age"].isna().sum(), 0)

    def test_minmax_range(self):
        self.assertAlmostEqual(self.df["Age_MinMax"].min(), 0.0)
        self.assertAlmostEqual(self.df["Age_MinMax"].max(), 1.0)

    def test_zscore(self):
        self.assertAlmostEqual(self.df["Age_ZScore"].mean(), 0.0, places=6)
        self.assertAlmostEqual(self.df["Age_ZScore"].std(), 1.0, places=6)

    def test_survivors_by_sexcode(self):
        self.assertEqual(mp5.survivors_by_sexcode(self.df).tolist(), [109, 233])

    def test_pivot_shape(self):
        self.assertEqual(mp5.survival_pivot(self.df).shape, (3, 2))


if __name__ == "__main__":
    unittest.main()
