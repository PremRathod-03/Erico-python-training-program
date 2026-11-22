"""
Mini-Project 2: Personal Finance Transaction Tracker - core classes

- Transaction class with an (amount, category, date) constructor
- display_info() shows transaction details (and logs them)
- Income and Expense subclasses with display_income() / display_expense()
- basic logging configured with logging.basicConfig()
- errors while displaying are logged with logger.error()
- invalid data (negative amounts, empty categories, bad dates) is rejected
"""
import json
import logging
from datetime import date, datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "finance_tracker.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("finance_tracker")


class InvalidTransactionError(ValueError):
    """Raised when transaction data is invalid."""


def parse_amount(value) -> float:
    try:
        amount = float(value)
    except (TypeError, ValueError):
        raise InvalidTransactionError(f"Amount must be a number, got {value!r}")
    if amount != amount or amount in (float("inf"), float("-inf")):
        raise InvalidTransactionError("Amount must be a finite number")
    if amount <= 0:
        raise InvalidTransactionError("Amount must be greater than zero")
    return round(amount, 2)


def parse_category(value) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InvalidTransactionError("Category cannot be empty")
    return value.strip().title()


def parse_date(value) -> date:
    if value is None or value == "":
        return date.today()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    try:
        return datetime.strptime(str(value).strip(), "%Y-%m-%d").date()
    except ValueError:
        raise InvalidTransactionError(f"Date must be YYYY-MM-DD, got {value!r}")


class Transaction:
    kind = "Transaction"

    def __init__(self, amount, category, date=None):
        self.amount = parse_amount(amount)
        self.category = parse_category(category)
        self.date = parse_date(date)

    @property
    def signed_amount(self) -> float:
        return self.amount

    def display_info(self) -> str:
        try:
            info = (f"[{self.kind}] {self.date.isoformat()} | "
                    f"{self.category:<12} | Rs. {self.amount:,.2f}")
        except Exception as err:          # e.g. attributes corrupted after creation
            logger.error("Failed to display transaction: %s", err)
            raise
        logger.info("Displayed transaction: %s", info)
        return info

    def to_dict(self) -> dict:
        return {"type": self.kind, "amount": self.amount,
                "category": self.category, "date": self.date.isoformat()}

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.amount!r}, {self.category!r}, {self.date.isoformat()!r})"


class Income(Transaction):
    kind = "Income"

    def display_income(self) -> str:
        return f"+ {self.display_info()}"


class Expense(Transaction):
    kind = "Expense"

    @property
    def signed_amount(self) -> float:
        return -self.amount

    def display_expense(self) -> str:
        return f"- {self.display_info()}"


TYPES = {"income": Income, "expense": Expense}


def create_transaction(kind: str, amount, category, date=None) -> Transaction:
    cls = TYPES.get(str(kind).strip().lower())
    if cls is None:
        raise InvalidTransactionError(f"Unknown transaction type {kind!r}")
    return cls(amount, category, date)


class Ledger:
    """A collection of transactions with summaries and JSON persistence."""

    def __init__(self):
        self.transactions: list[Transaction] = []

    def add(self, transaction: Transaction) -> None:
        self.transactions.append(transaction)
        logger.info("Added %r", transaction)

    def total_income(self) -> float:
        return round(sum(t.amount for t in self.transactions if isinstance(t, Income)), 2)

    def total_expense(self) -> float:
        return round(sum(t.amount for t in self.transactions if isinstance(t, Expense)), 2)

    def balance(self) -> float:
        return round(sum(t.signed_amount for t in self.transactions), 2)

    def by_category(self) -> dict[str, float]:
        totals: dict[str, float] = {}
        for t in self.transactions:
            if isinstance(t, Expense):
                totals[t.category] = round(totals.get(t.category, 0) + t.amount, 2)
        return dict(sorted(totals.items(), key=lambda kv: kv[1], reverse=True))

    def save(self, path: Path) -> None:
        path.write_text(json.dumps([t.to_dict() for t in self.transactions], indent=2), encoding="utf-8")
        logger.info("Saved %d transactions to %s", len(self.transactions), path.name)

    @classmethod
    def load(cls, path: Path) -> "Ledger":
        ledger = cls()
        if not path.exists():
            return ledger
        try:
            rows = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as err:
            logger.error("Corrupt data file %s: %s", path.name, err)
            return ledger
        for row in rows:
            try:
                ledger.add(create_transaction(row["type"], row["amount"], row["category"], row["date"]))
            except (KeyError, InvalidTransactionError) as err:
                logger.error("Skipping bad record %r: %s", row, err)
        return ledger
