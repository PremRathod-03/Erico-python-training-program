"""
Exercise 8: Package Imports

- third-party package: `requests` fetches posts from the JSONPlaceholder API
- custom module: math_utils.py with factorial() and is_prime()

Install:  pip install requests
Run:      python main.py
"""
import requests                              # third-party package

import math_utils                            # custom module (whole module)
from math_utils import factorial, is_prime   # specific names

API_URL = "https://jsonplaceholder.typicode.com/posts"


def fetch_posts(user_id: int = 1, limit: int = 5) -> list[dict]:
    response = requests.get(API_URL, params={"userId": user_id}, timeout=10)
    response.raise_for_status()
    return response.json()[:limit]


def show_posts(posts: list[dict]) -> None:
    for post in posts:
        print(f"  #{post['id']}: {post['title']}")


def main() -> None:
    print("Posts from JSONPlaceholder (user 1):")
    try:
        show_posts(fetch_posts())
    except requests.RequestException as err:
        print("  Could not reach the API:", err)

    print("\nmath_utils:")
    print("  factorial(6) =", factorial(6))
    print("  primes under 30 =", [n for n in range(30) if is_prime(n)])
    print("  gcd(48, 18) =", math_utils.gcd(48, 18))
    print("  first 10 Fibonacci =", math_utils.fibonacci(10))


if __name__ == "__main__":
    main()
