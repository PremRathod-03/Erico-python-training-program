"""
Exercise 10: Data Structures

- list: create, modify, sort, search
- tuple for fixed data
- dictionary for key/value items
- set operations
- stack (list) and queue (collections.deque)
- choosing the right data structure
- nested lists and dictionaries
"""
from bisect import bisect_left
from collections import deque


def binary_search(sorted_items: list, target) -> int:
    """Return index of target in a sorted list, or -1."""
    i = bisect_left(sorted_items, target)
    return i if i < len(sorted_items) and sorted_items[i] == target else -1


class Stack:
    """LIFO stack backed by a list."""
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if not self._items:
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        return self._items[-1] if self._items else None

    def __len__(self):
        return len(self._items)


class Queue:
    """FIFO queue backed by deque (O(1) pops from the left)."""
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if not self._items:
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def __len__(self):
        return len(self._items)


def main() -> None:
    # list
    marks = [72, 95, 58, 88, 64]
    marks.append(79)
    marks[0] = 75
    marks.remove(58)
    print("List:", marks, "| sorted:", sorted(marks), "| desc:", sorted(marks, reverse=True))
    print("Linear search 88 ->", marks.index(88))
    sorted_marks = sorted(marks)
    print("Binary search 79 ->", binary_search(sorted_marks, 79))

    # tuple
    RGB_WHITE = (255, 255, 255)
    print("Tuple (fixed data):", RGB_WHITE)

    # dict
    student = {"name": "Prem", "branch": "AIML", "sem": 7}
    student["cgpa"] = 8.9
    print("Dict:", student, "| keys:", list(student))

    # set
    python_club = {"Asha", "Ravi", "Prem", "Neha"}
    ml_club = {"Prem", "Neha", "Kiran"}
    print("Union:", python_club | ml_club)
    print("Intersection:", python_club & ml_club)
    print("Difference:", python_club - ml_club)
    print("Symmetric diff:", python_club ^ ml_club)

    # stack & queue
    s = Stack()
    for page in ["home", "about", "contact"]:
        s.push(page)
    print("Stack pop (browser back):", s.pop(), "-> now at", s.peek())
    q = Queue()
    for job in ["print A", "print B", "print C"]:
        q.enqueue(job)
    print("Queue dequeue (first come first served):", q.dequeue(), "| remaining", len(q))

    # deque directly
    recent = deque(maxlen=3)
    for item in [1, 2, 3, 4, 5]:
        recent.append(item)
    print("deque(maxlen=3) keeps the last 3:", list(recent))
    recent.appendleft(0)
    print("appendleft:", list(recent))

    # right data structure
    print("\nPicking the right structure:")
    print("  ordered + changeable      -> list")
    print("  fixed record              -> tuple")
    print("  lookup by key             -> dict")
    print("  unique items / membership -> set")
    print("  LIFO / FIFO               -> list as stack / deque as queue")

    # nested
    matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    transpose = [[row[i] for row in matrix] for i in range(3)]
    print("\nNested list transpose:", transpose)
    classroom = {
        "AIML-B": {"students": ["Prem", "Asha"], "mentor": "Dr. Rao"},
        "CSE-A": {"students": ["Ravi"], "mentor": "Dr. Iyer"},
    }
    classroom["AIML-B"]["students"].append("Kiran")
    for section, info in classroom.items():
        print(f"  {section}: mentor={info['mentor']}, students={info['students']}")


if __name__ == "__main__":
    main()
