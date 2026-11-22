import unittest
from unittest.mock import patch

import calculator as calc


class TestOperations(unittest.TestCase):
    def test_basic_operations(self):
        self.assertEqual(calc.add(2, 3), 5)
        self.assertEqual(calc.subtract(10, 4), 6)
        self.assertEqual(calc.multiply(3, 4), 12)
        self.assertEqual(calc.divide(9, 2), 4.5)
        self.assertEqual(calc.modulus(10, 3), 1)
        self.assertEqual(calc.power(2, 5), 32)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calc.divide(1, 0)


class TestValidation(unittest.TestCase):
    def test_parse_number(self):
        self.assertEqual(calc.parse_number("12"), 12)
        self.assertIsInstance(calc.parse_number("12"), int)
        self.assertEqual(calc.parse_number("3.5"), 3.5)
        self.assertEqual(calc.parse_number(" -2 "), -2)
        for bad in ["", "abc", "1,2", "nan", "inf"]:
            self.assertIsNone(calc.parse_number(bad), bad)

    def test_choice(self):
        self.assertTrue(calc.is_valid_choice("1"))
        self.assertTrue(calc.is_valid_choice("q"))
        self.assertFalse(calc.is_valid_choice("9"))


class TestMenuLoop(unittest.TestCase):
    def test_full_session(self):
        inputs = iter(["1", "2", "3", "9", "4", "8", "0", "4", "8", "2", "x", "0"])
        with patch("builtins.print"):
            history = calc.run(input_func=lambda _: next(inputs))
        self.assertEqual(history, ["2 + 3 = 5", "8 / 2 = 4"])


if __name__ == "__main__":
    unittest.main()
