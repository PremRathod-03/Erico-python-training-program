"""
Mini-Project 1: Python Calculator

Requirements covered:
 1. First Python project, configured in the IDE (see README)
 2. Basic data types (int, float, str) and variable assignment
 3. Arithmetic: addition, subtraction, multiplication, division
 4. User input with input()
 5. A function for each operation
 6. Input validation with if/else and logical operators
 7. Loop until the user chooses to exit
 8. Menu system to navigate between operations

Run: python calculator.py
"""

APP_NAME: str = "Python Calculator"
VERSION: float = 1.0


# ---- 5. one function per operation -------------------------------------------
def add(a: float, b: float) -> float:
    return a + b


def subtract(a: float, b: float) -> float:
    return a - b


def multiply(a: float, b: float) -> float:
    return a * b


def divide(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot divide by zero")
    return a / b


def modulus(a: float, b: float) -> float:
    if b == 0:
        raise ZeroDivisionError("Cannot take modulus by zero")
    return a % b


def power(a: float, b: float) -> float:
    return a ** b


OPERATIONS = {
    "1": ("Addition", "+", add),
    "2": ("Subtraction", "-", subtract),
    "3": ("Multiplication", "*", multiply),
    "4": ("Division", "/", divide),
    "5": ("Modulus", "%", modulus),
    "6": ("Power", "**", power),
}
EXIT_CHOICES = {"0", "q", "quit", "exit"}


# ---- 6. validation -------------------------------------------------------------
def parse_number(text: str) -> float | int | None:
    """Return int/float for valid numeric text, otherwise None."""
    text = text.strip()
    if text == "":
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    if value != value or value in (float("inf"), float("-inf")):   # NaN / inf
        return None
    return int(value) if value.is_integer() and "." not in text and "e" not in text.lower() else value


def read_number(prompt: str, input_func=input) -> float:
    while True:
        value = parse_number(input_func(prompt))
        if value is not None:
            return value
        print("  Invalid number, please try again (e.g. 12 or 3.5).")


def is_valid_choice(choice: str) -> bool:
    return choice in OPERATIONS or choice.lower() in EXIT_CHOICES


def format_result(value: float) -> str:
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return f"{value:.6g}" if isinstance(value, float) else str(value)


def calculate(choice: str, a: float, b: float) -> float:
    _, _, func = OPERATIONS[choice]
    return func(a, b)


# ---- 8. menu ------------------------------------------------------------------
def show_menu() -> None:
    print(f"\n===== {APP_NAME} v{VERSION} =====")
    for key, (name, symbol, _) in OPERATIONS.items():
        print(f"  {key}. {name:<15} ({symbol})")
    print("  0. Exit")


# ---- 7. loop until exit -------------------------------------------------------
def run(input_func=input) -> list[str]:
    history: list[str] = []
    while True:
        show_menu()
        choice = input_func("Choose an option: ").strip()

        if not is_valid_choice(choice):
            print("  Invalid choice. Pick a number from the menu.")
            continue
        if choice.lower() in EXIT_CHOICES:
            break

        name, symbol, _ = OPERATIONS[choice]
        a = read_number("  Enter first number: ", input_func)
        b = read_number("  Enter second number: ", input_func)
        try:
            result = calculate(choice, a, b)
        except ZeroDivisionError as err:
            print(f"  Error: {err}")
            continue
        except OverflowError:
            print("  Error: result is too large")
            continue

        line = f"{a} {symbol} {b} = {format_result(result)}"
        history.append(line)
        print(f"  Result: {line}")

    if history:
        print("\nHistory:")
        for i, line in enumerate(history, 1):
            print(f"  {i}. {line}")
    print("Goodbye!")
    return history


if __name__ == "__main__":
    run()
