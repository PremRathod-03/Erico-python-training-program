"""
Exercise 11: Exception Handling

- try / except / else / finally
- handling multiple exceptions
- raising custom exceptions
- assert for debugging
- common built-in exceptions
- logging errors and safe-code best practices
"""
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)


class InsufficientFundsError(Exception):
    """Custom error raised when a withdrawal exceeds the balance."""

    def __init__(self, balance: float, amount: float):
        super().__init__(f"Cannot withdraw {amount:.2f}; balance is only {balance:.2f}")
        self.balance = balance
        self.amount = amount


def withdraw(balance: float, amount: float) -> float:
    if amount <= 0:
        raise ValueError("amount must be positive")
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount


def safe_divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        log.error("Cannot divide %s by zero", a)
        return None
    except TypeError as err:
        log.error("Bad operand types: %s", err)
        return None
    else:                         # runs only if no exception occurred
        log.info("Division succeeded: %s / %s = %s", a, b, result)
        return result
    finally:                      # always runs
        log.info("safe_divide finished")


def parse_int_list(items):
    """Multiple exceptions handled in one clause."""
    values = []
    for item in items:
        try:
            values.append(int(item))
        except (ValueError, TypeError):
            log.warning("Skipping invalid value: %r", item)
    return values


def average(values):
    assert len(values) > 0, "average() needs at least one value"   # debugging aid
    return sum(values) / len(values)


def common_exceptions_demo():
    examples = {
        "IndexError": lambda: [1, 2][5],
        "KeyError": lambda: {"a": 1}["b"],
        "ValueError": lambda: int("abc"),
        "TypeError": lambda: "2" + 2,
        "FileNotFoundError": lambda: open("missing_file.txt"),
        "AttributeError": lambda: None.upper(),
        "ZeroDivisionError": lambda: 1 / 0,
    }
    for name, func in examples.items():
        try:
            func()
        except Exception as err:            # demo only: catch-all to list them
            print(f"  {name:<18} -> {type(err).__name__}: {err}")


def main() -> None:
    safe_divide(10, 2)
    safe_divide(10, 0)
    safe_divide("10", 2)

    print("Parsed:", parse_int_list(["1", "2", "x", None, "5"]))

    try:
        withdraw(500, 800)
    except InsufficientFundsError as err:
        log.error("Custom error: %s", err)

    try:
        average([])
    except AssertionError as err:
        log.error("Assertion failed: %s", err)

    print("Common exceptions:")
    common_exceptions_demo()

    print("\nBest practices: catch specific exceptions, keep try blocks small,")
    print("never silence errors with a bare `except:`, log them, and clean up in finally/with.")


if __name__ == "__main__":
    main()
