"""
Exercise 3: Functions

- function with two parameters returning their sum
- call with positional and keyword arguments
- default argument for the second number
- argument unpacking with a list
- lambda to square a number
- recursive factorial
- variable scope (local / global / nonlocal)
- function printing a formatted greeting multiple times
"""

counter = 0  # global variable used in the scope demo


def add(a, b=10):
    """Return a + b. `b` defaults to 10."""
    return a + b


def total(*numbers):
    """Sum any number of values (used with list unpacking)."""
    return sum(numbers)


square = lambda x: x * x  # noqa: E731  (lambda requested by the exercise)


def factorial(n: int) -> int:
    """Recursive factorial. Raises ValueError for negatives."""
    if n < 0:
        raise ValueError("factorial is not defined for negative numbers")
    if n in (0, 1):
        return 1
    return n * factorial(n - 1)


def scope_demo():
    """Show local, global and nonlocal scope."""
    global counter
    counter += 1                     # modifies the global
    message = "local to scope_demo"  # local variable

    def inner():
        nonlocal message
        message = "changed by inner()"

    print("  before inner:", message)
    inner()
    print("  after inner: ", message)
    print("  global counter is now", counter)


def greet(name: str, times: int = 3) -> None:
    for i in range(1, times + 1):
        print(f"  [{i}] Hello, {name.title()}! Welcome to Python functions.")


def main() -> None:
    print("Positional:", add(3, 4))
    print("Keyword:   ", add(b=4, a=3))
    print("Default b: ", add(5))

    nums = [1, 2, 3, 4, 5]
    print("Unpacking list into total(*nums):", total(*nums))
    pair = [8, 2]
    print("Unpacking list into add(*pair):  ", add(*pair))

    print("Lambda square(7):", square(7))
    print("Factorial(5):", factorial(5))

    print("Scope demo:")
    scope_demo()

    print("Greeting:")
    greet("prem", times=3)


if __name__ == "__main__":
    main()
