"""
Exercise 4: Iterative & Conditional Statements

- minor / adult / senior with if-elif-else
- logical operators: eligible for BOTH driver's licence and voting
- for loop over a list: print even numbers, continue on odd, break when > 20
- nested loop multiplication table 1..5
- validate age input (positive integer) with a while loop
- range() to print 1..10
"""

DRIVING_AGE = 18
VOTING_AGE = 18
SENIOR_AGE = 60


def age_category(age: int) -> str:
    if age < 18:
        return "minor"
    elif age < SENIOR_AGE:
        return "adult"
    else:
        return "senior"


def can_drive_and_vote(age: int, has_licence_test_passed: bool = True) -> bool:
    return age >= DRIVING_AGE and age >= VOTING_AGE and has_licence_test_passed


def read_positive_int(prompt: str) -> int:
    """Keep asking until the user enters a positive integer."""
    while True:
        text = input(prompt).strip()
        if text.isdigit() and int(text) > 0:
            return int(text)
        print("  Please enter a positive whole number (e.g. 25).")


def even_numbers_until_20(numbers):
    """Return even numbers, skipping odds, stopping when a number > 20 appears."""
    result = []
    for n in numbers:
        if n > 20:
            break
        if n % 2 != 0:
            continue
        result.append(n)
    return result


def main() -> None:
    age = read_positive_int("Enter your age: ")
    print(f"You are a(n) {age_category(age)}.")
    if can_drive_and_vote(age):
        print("You are eligible for BOTH a driver's licence and voting.")
    else:
        print("You are NOT eligible for both a driver's licence and voting yet.")

    numbers = [3, 4, 7, 10, 12, 15, 18, 21, 22, 24]
    print("\nEven numbers before the first number > 20:")
    for n in even_numbers_until_20(numbers):
        print(" ", n)

    print("\nMultiplication table (1-5):")
    for i in range(1, 6):
        row = ""
        for j in range(1, 6):
            row += f"{i * j:4}"
        print(row)

    print("\nNumbers 1 to 10:")
    for n in range(1, 11):
        print(n, end=" ")
    print()


if __name__ == "__main__":
    main()
