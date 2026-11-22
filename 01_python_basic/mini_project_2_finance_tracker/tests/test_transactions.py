"""
Unit tests for the finance tracker:
- display_info() output
- Income / Expense inheritance and behaviour
- input validation, edge cases (negative amounts, empty categories)
- mock tests for logging
"""
import sys
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import main as app                                       # noqa: E402
from transactions import (Expense, Income, InvalidTransactionError,  # noqa: E402
                          Ledger, Transaction, create_transaction)


class TestDisplayInfo(unittest.TestCase):
    def test_display_info_format(self):
        t = Transaction(1500, "salary", "2026-01-05")
        self.assertEqual(t.display_info(),
                         "[Transaction] 2026-01-05 | Salary       | Rs. 1,500.00")

    def test_display_income_and_expense_prefix(self):
        self.assertTrue(Income(10, "Gift", "2026-01-01").display_income().startswith("+ [Income]"))
        self.assertTrue(Expense(10, "Food", "2026-01-01").display_expense().startswith("- [Expense]"))


class TestInheritance(unittest.TestCase):
    def test_subclasses(self):
        self.assertTrue(issubclass(Income, Transaction))
        self.assertTrue(issubclass(Expense, Transaction))
        i, e = Income(100, "Salary"), Expense(40, "Food")
        self.assertIsInstance(i, Transaction)
        self.assertIsInstance(e, Transaction)
        self.assertEqual(i.date, date.today())

    def test_signed_amount_and_methods(self):
        self.assertEqual(Income(100, "x").signed_amount, 100)
        self.assertEqual(Expense(40, "x").signed_amount, -40)
        self.assertTrue(hasattr(Income, "display_income"))
        self.assertFalse(hasattr(Income, "display_expense"))

    def test_ledger_summary(self):
        ledger = Ledger()
        ledger.add(Income(1000, "Salary", "2026-01-01"))
        ledger.add(Expense(200, "Food", "2026-01-02"))
        ledger.add(Expense(50.5, "food", "2026-01-03"))
        self.assertEqual(ledger.total_income(), 1000)
        self.assertEqual(ledger.total_expense(), 250.5)
        self.assertEqual(ledger.balance(), 749.5)
        self.assertEqual(ledger.by_category(), {"Food": 250.5})


class TestValidation(unittest.TestCase):
    def test_invalid_values(self):
        cases = [(-50, "Food"), (0, "Food"), ("abc", "Food"), ("nan", "Food"),
                 (100, ""), (100, "   "), (100, None)]
        for amount, category in cases:
            with self.subTest(amount=amount, category=category):
                with self.assertRaises(InvalidTransactionError):
                    Expense(amount, category)

    def test_bad_date_and_type(self):
        with self.assertRaises(InvalidTransactionError):
            Income(10, "Gift", "05-01-2026")
        with self.assertRaises(InvalidTransactionError):
            create_transaction("loan", 10, "Bank")

    def test_valid_string_amount(self):
        self.assertEqual(Income("99.999", "Bonus").amount, 100.0)

    def test_prompt_handles_invalid_input(self):
        answers = iter(["-20", "Food", ""])
        with patch("builtins.print") as mocked_print:
            result = app.prompt_transaction("expense", lambda _: next(answers))
        self.assertIsNone(result)
        self.assertIn("Invalid input", mocked_print.call_args[0][0])


class TestLoggingWithMocks(unittest.TestCase):
    @patch("transactions.logger")
    def test_display_info_logs(self, mock_logger):
        t = Income(500, "Freelance", "2026-02-01")
        info = t.display_info()
        mock_logger.info.assert_called_with("Displayed transaction: %s", info)

    @patch("transactions.logger")
    def test_display_error_logged(self, mock_logger):
        t = Expense(10, "Food", "2026-02-01")
        t.date = None                       # corrupt the object after creation
        with self.assertRaises(AttributeError):
            t.display_info()
        mock_logger.error.assert_called_once()

    @patch("main.logger")
    def test_invalid_user_input_logged(self, mock_logger):
        answers = iter(["10", "", ""])
        with patch("builtins.print"):
            app.prompt_transaction("income", lambda _: next(answers))
        mock_logger.error.assert_called_once()


class TestPersistence(unittest.TestCase):
    def test_save_and_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            ledger = Ledger()
            ledger.add(Income(100, "Salary", "2026-01-01"))
            ledger.add(Expense(30, "Food", "2026-01-02"))
            ledger.save(path)
            loaded = Ledger.load(path)
            self.assertEqual(loaded.balance(), 70)
            self.assertIsInstance(loaded.transactions[1], Expense)

    def test_cli_session(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "data.json"
            answers = iter(["1", "5000", "Salary", "2026-03-01",
                            "2", "1200", "Rent", "2026-03-02",
                            "2", "-5", "Food", "",
                            "4", "0"])
            with patch("builtins.print"):
                ledger = app.run(lambda _: next(answers), data_file=path)
            self.assertEqual(ledger.balance(), 3800)
            self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
