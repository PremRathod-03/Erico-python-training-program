"""
Exercise 2: Basic Variables

- Ask for name and age, convert age to int, add 5 and print a message
- Lists: create three colours, print the second, change the first to "Blue"
- Tuples: create one with three numbers and try modifying it
- Arithmetic: multiply two numbers, 25 % 4, repeat "Python" 3 times
- Print the data types of all variables used
"""


def main() -> None:
    # --- user input -------------------------------------------------------
    name = input("Enter your name: ").strip() or "Friend"
    age_text = input("Enter your age: ").strip()
    try:
        age = int(age_text)
    except ValueError:
        print(f"'{age_text}' is not a whole number, using 0.")
        age = 0
    new_age = age + 5
    print(f"Hello {name}, in 5 years you will be {new_age} years old!")

    # --- list ---------------------------------------------------------------
    colors = ["Red", "Green", "Yellow"]
    print("Second colour:", colors[1])
    colors[0] = "Blue"                       # lists are mutable
    print("After change:", colors)

    # --- tuple --------------------------------------------------------------
    numbers = (10, 20, 30)
    try:
        numbers[0] = 99                      # tuples are immutable
    except TypeError as err:
        print("Cannot modify a tuple ->", err)

    # --- arithmetic & strings ----------------------------------------------
    a, b = 7, 6
    product = a * b
    print(f"{a} * {b} = {product}")
    remainder = 25 % 4
    print("25 % 4 =", remainder)
    repeated = "Python" * 3
    print(repeated)

    # --- data types ---------------------------------------------------------
    variables = {
        "name": name, "age_text": age_text, "age": age, "new_age": new_age,
        "colors": colors, "numbers": numbers, "a": a, "b": b,
        "product": product, "remainder": remainder, "repeated": repeated,
    }
    print("\nData types:")
    for var_name, value in variables.items():
        print(f"  {var_name:<10} -> {type(value).__name__}")


if __name__ == "__main__":
    main()
