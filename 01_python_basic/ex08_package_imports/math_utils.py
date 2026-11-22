"""Custom helper module for Exercise 8 (imported by main.py)."""


def factorial(n: int) -> int:
    if not isinstance(n, int) or n < 0:
        raise ValueError("n must be a non-negative integer")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def gcd(a: int, b: int) -> int:
    while b:
        a, b = b, a % b
    return abs(a)


def fibonacci(n: int) -> list[int]:
    seq, a, b = [], 0, 1
    for _ in range(n):
        seq.append(a)
        a, b = b, a + b
    return seq
