"""
Mini-Project 2: Personal Finance Transaction Tracker - command-line app

Run:   python main.py
Tests: python -m unittest discover -s tests -v
"""
from pathlib import Path

from transactions import (Expense, Income, InvalidTransactionError, Ledger,
                          create_transaction, logger)

DATA_FILE = Path(__file__).resolve().parent / "transactions.json"

MENU = """
===== Finance Tracker =====
 1. Add income
 2. Add expense
 3. View all transactions
 4. Summary
 5. Save
 0. Save & exit"""


def prompt_transaction(kind: str, input_func=input):
    """Ask for transaction details; returns a Transaction or None on bad input."""
    amount = input_func("  Amount (Rs.): ")
    category = input_func("  Category: ")
    when = input_func("  Date YYYY-MM-DD (blank = today): ")
    try:
        return create_transaction(kind, amount, category, when)
    except InvalidTransactionError as err:
        print(f"  Invalid input: {err}")
        logger.error("Invalid user input for %s: %s", kind, err)
        return None


def show_all(ledger: Ledger) -> None:
    if not ledger.transactions:
        print("  No transactions yet.")
        return
    for t in sorted(ledger.transactions, key=lambda t: t.date):
        if isinstance(t, Income):
            print(" ", t.display_income())
        elif isinstance(t, Expense):
            print(" ", t.display_expense())


def show_summary(ledger: Ledger) -> None:
    print(f"  Total income : Rs. {ledger.total_income():,.2f}")
    print(f"  Total expense: Rs. {ledger.total_expense():,.2f}")
    print(f"  Balance      : Rs. {ledger.balance():,.2f}")
    if ledger.by_category():
        print("  Spending by category:")
        for category, amount in ledger.by_category().items():
            print(f"    {category:<12} Rs. {amount:,.2f}")


def run(input_func=input, data_file: Path = DATA_FILE) -> Ledger:
    ledger = Ledger.load(data_file)
    while True:
        print(MENU)
        choice = input_func("Choose: ").strip()
        if choice == "1":
            t = prompt_transaction("income", input_func)
            if t:
                ledger.add(t)
                print("  Added:", t.display_income())
        elif choice == "2":
            t = prompt_transaction("expense", input_func)
            if t:
                ledger.add(t)
                print("  Added:", t.display_expense())
        elif choice == "3":
            show_all(ledger)
        elif choice == "4":
            show_summary(ledger)
        elif choice == "5":
            ledger.save(data_file)
            print(f"  Saved to {data_file.name}")
        elif choice == "0":
            ledger.save(data_file)
            print("Saved. Goodbye!")
            return ledger
        else:
            print("  Invalid option, choose 0-5.")


if __name__ == "__main__":
    run()
