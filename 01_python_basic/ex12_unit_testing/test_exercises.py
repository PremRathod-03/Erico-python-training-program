"""
Exercise 12: Unit Testing

unittest test cases for earlier exercises:
  - Exercise 3  (functions.py)
  - Exercise 5  (text_encoding.py)
  - Exercise 8  (math_utils.py)
  - Exercise 10 (data_structures.py)
  - Exercise 11 (exception_handling.py)

Run from the repo root:   python -m unittest discover -s 01_python_basic/ex12_unit_testing -v
or from this folder:      python -m unittest -v
"""
import sys
import unittest
from pathlib import Path

BASIC_DIR = Path(__file__).resolve().parent.parent
for folder in ["ex03_functions", "ex05_text_encoding", "ex08_package_imports",
               "ex10_data_structures", "ex11_exception_handling"]:
    sys.path.insert(0, str(BASIC_DIR / folder))

import data_structures as ds          # noqa: E402
import exception_handling as eh       # noqa: E402
import functions as fn                # noqa: E402
import math_utils                     # noqa: E402
import text_encoding as te            # noqa: E402


class TestFunctions(unittest.TestCase):
    def test_add_default_and_keyword(self):
        self.assertEqual(fn.add(5), 15)
        self.assertEqual(fn.add(b=1, a=2), 3)

    def test_total_unpacking(self):
        self.assertEqual(fn.total(*[1, 2, 3]), 6)

    def test_factorial(self):
        self.assertEqual(fn.factorial(0), 1)
        self.assertEqual(fn.factorial(5), 120)
        with self.assertRaises(ValueError):
            fn.factorial(-1)


class TestTextEncoding(unittest.TestCase):
    SAMPLE = "Mail a.b@test.com and bad@@x on 2025-12-31. Café ☕"

    def test_extract_emails(self):
        self.assertEqual(te.extract_emails(self.SAMPLE), ["a.b@test.com"])

    def test_convert_dates(self):
        self.assertIn("31/12/2025", te.convert_dates(self.SAMPLE))

    def test_round_trips(self):
        self.assertEqual(te.from_base64(te.to_base64(self.SAMPLE)), self.SAMPLE)
        self.assertEqual(te.from_code_points(te.to_code_points(self.SAMPLE)), self.SAMPLE)
        self.assertEqual(te.rot13(te.rot13(self.SAMPLE)), self.SAMPLE)

    def test_url_encode(self):
        self.assertEqual(te.url_encode("a b&c"), "a%20b%26c")


class TestMathUtils(unittest.TestCase):
    def test_factorial(self):
        self.assertEqual(math_utils.factorial(6), 720)
        with self.assertRaises(ValueError):
            math_utils.factorial(-3)

    def test_is_prime(self):
        primes = [n for n in range(20) if math_utils.is_prime(n)]
        self.assertEqual(primes, [2, 3, 5, 7, 11, 13, 17, 19])

    def test_gcd_fibonacci(self):
        self.assertEqual(math_utils.gcd(48, 18), 6)
        self.assertEqual(math_utils.fibonacci(6), [0, 1, 1, 2, 3, 5])


class TestDataStructures(unittest.TestCase):
    def test_stack_lifo(self):
        s = ds.Stack()
        s.push(1)
        s.push(2)
        self.assertEqual(s.pop(), 2)
        self.assertEqual(len(s), 1)

    def test_queue_fifo(self):
        q = ds.Queue()
        q.enqueue("a")
        q.enqueue("b")
        self.assertEqual(q.dequeue(), "a")
        with self.assertRaises(IndexError):
            q.dequeue()
            q.dequeue()

    def test_binary_search(self):
        self.assertEqual(ds.binary_search([1, 3, 5, 7], 5), 2)
        self.assertEqual(ds.binary_search([1, 3, 5, 7], 4), -1)


class TestExceptionHandling(unittest.TestCase):
    def test_withdraw(self):
        self.assertEqual(eh.withdraw(100, 40), 60)
        with self.assertRaises(eh.InsufficientFundsError):
            eh.withdraw(100, 400)
        with self.assertRaises(ValueError):
            eh.withdraw(100, -5)

    def test_safe_divide_and_parse(self):
        with self.assertLogs(eh.log, level="ERROR"):
            self.assertIsNone(eh.safe_divide(1, 0))
        self.assertEqual(eh.parse_int_list(["1", "x", None, "4"]), [1, 4])

    def test_assert(self):
        with self.assertRaises(AssertionError):
            eh.average([])


if __name__ == "__main__":
    unittest.main()
