"""
Exercise 6: File Handling

- open/write/read/close a file manually
- use `with` for automatic closing
- write vs append
- CSV and JSON files (write, append, read)
- exception handling for missing files / bad JSON
- binary file operations
- read a large file line by line efficiently

All files are created in ./data/
"""
import csv
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"


def manual_open_close(path: Path) -> str:
    f = open(path, "w", encoding="utf-8")
    try:
        f.write("Written with open() and closed manually.\n")
    finally:
        f.close()
    f = open(path, "r", encoding="utf-8")
    try:
        return f.read()
    finally:
        f.close()


def write_and_append(path: Path) -> list[str]:
    with open(path, "w", encoding="utf-8") as f:       # overwrite
        f.write("Line 1: created with 'w'\n")
    with open(path, "a", encoding="utf-8") as f:       # append
        f.write("Line 2: added with 'a'\n")
        f.write("Line 3: added with 'a'\n")
    with open(path, encoding="utf-8") as f:
        return f.readlines()


def csv_demo(path: Path) -> list[dict]:
    rows = [{"name": "Asha", "dept": "ML", "score": 88},
            {"name": "Ravi", "dept": "CSE", "score": 76}]
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["name", "dept", "score"])
        writer.writeheader()
        writer.writerows(rows)
    with open(path, "a", newline="", encoding="utf-8") as f:   # append a row
        csv.DictWriter(f, fieldnames=["name", "dept", "score"]).writerow(
            {"name": "Prem", "dept": "AIML", "score": 91})
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def json_demo(path: Path) -> dict:
    data = {"course": "Python Basic", "students": ["Asha", "Ravi"]}
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    # "append": load -> modify -> save
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    data["students"].append("Prem")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def safe_read(path: Path) -> str | None:
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"  [handled] file not found: {path.name}")
    except PermissionError:
        print(f"  [handled] no permission to read: {path.name}")
    return None


def safe_load_json(path: Path):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as err:
        print(f"  [handled] invalid JSON in {path.name}: {err.msg}")
        return None


def binary_demo(path: Path) -> bytes:
    payload = bytes(range(16)) + "नमस्ते".encode("utf-8")
    with open(path, "wb") as f:
        f.write(payload)
    with open(path, "rb") as f:
        return f.read()


def count_lines_efficiently(path: Path, keyword: str) -> tuple[int, int]:
    """Iterate the file object: only one line is in memory at a time."""
    total = matches = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            total += 1
            if keyword in line:
                matches += 1
    return total, matches


def main() -> None:
    DATA_DIR.mkdir(exist_ok=True)

    print("Manual open/close:", manual_open_close(DATA_DIR / "manual.txt").strip())
    print("Write + append:", [l.strip() for l in write_and_append(DATA_DIR / "notes.txt")])
    print("CSV rows:", csv_demo(DATA_DIR / "students.csv"))
    print("JSON data:", json_demo(DATA_DIR / "course.json"))

    print("Exception handling:")
    safe_read(DATA_DIR / "does_not_exist.txt")
    (DATA_DIR / "broken.json").write_text("{bad json", encoding="utf-8")
    safe_load_json(DATA_DIR / "broken.json")

    raw = binary_demo(DATA_DIR / "sample.bin")
    print(f"Binary: {len(raw)} bytes, first 4 = {raw[:4]!r}, text part = {raw[16:].decode('utf-8')}")

    big = DATA_DIR / "large_log.txt"
    with open(big, "w", encoding="utf-8") as f:
        for i in range(100_000):
            level = "ERROR" if i % 50 == 0 else "INFO"
            f.write(f"{level} line {i}\n")
    total, errors = count_lines_efficiently(big, "ERROR")
    print(f"Large file: {total} lines read one at a time, {errors} ERROR lines")


if __name__ == "__main__":
    main()
