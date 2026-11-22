"""
Exercise 5: Text Encoding, Decoding and Pattern Matching

1. Regex
   Step 1: extract all valid e-mail addresses from input.txt -> emails.txt
   Step 2: replace dates YYYY-MM-DD with DD/MM/YYYY        -> updated_text.txt
2. Base64
   Step 3: encode input.txt                                  -> encoded.txt
   Step 4: decode encoded.txt back to the original text      -> decoded.txt
3. ASCII / Unicode
   Step 5: convert text to code points with ord()            -> ascii_values.txt
   Step 6: convert the code points back with chr()           -> ascii_decoded.txt
4. Other encodings
   Step 7: URL-encode input.txt                              -> url_encoded.txt
   Step 8: ROT13-encode input.txt                            -> rot13_encoded.txt

All outputs are written to ./output/
"""
import base64
import codecs
import re
from pathlib import Path
from urllib.parse import quote

BASE_DIR = Path(__file__).resolve().parent
INPUT_FILE = BASE_DIR / "input.txt"
OUTPUT_DIR = BASE_DIR / "output"

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}\b")
DATE_PATTERN = re.compile(r"\b(\d{4})-(\d{2})-(\d{2})\b")


def extract_emails(text: str) -> list[str]:
    return EMAIL_PATTERN.findall(text)


def convert_dates(text: str) -> str:
    return DATE_PATTERN.sub(r"\3/\2/\1", text)


def to_base64(text: str) -> str:
    return base64.b64encode(text.encode("utf-8")).decode("ascii")


def from_base64(encoded: str) -> str:
    return base64.b64decode(encoded.encode("ascii")).decode("utf-8")


def to_code_points(text: str) -> str:
    """ord() for every character. Non-ASCII characters give values > 127 (Unicode)."""
    return " ".join(str(ord(ch)) for ch in text)


def from_code_points(values: str) -> str:
    return "".join(chr(int(v)) for v in values.split())


def url_encode(text: str) -> str:
    return quote(text, safe="")


def rot13(text: str) -> str:
    return codecs.encode(text, "rot_13")


def write(name: str, content: str) -> Path:
    path = OUTPUT_DIR / name
    path.write_text(content, encoding="utf-8")
    print(f"  saved {path.relative_to(BASE_DIR)}")
    return path


def main() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)
    text = INPUT_FILE.read_text(encoding="utf-8")

    print("1. Regex operations")
    emails = extract_emails(text)
    print("  emails found:", emails)
    write("emails.txt", "\n".join(emails) + "\n")
    write("updated_text.txt", convert_dates(text))

    print("2. Base64")
    encoded = write("encoded.txt", to_base64(text)).read_text(encoding="utf-8")
    decoded = from_base64(encoded)
    write("decoded.txt", decoded)
    print("  round-trip OK:", decoded == text)

    print("3. ASCII / Unicode")
    values = write("ascii_values.txt", to_code_points(text)).read_text(encoding="utf-8")
    restored = from_code_points(values)
    write("ascii_decoded.txt", restored)
    non_ascii = sorted({ch for ch in text if ord(ch) > 127})
    print("  non-ASCII characters (Unicode):", non_ascii)
    print("  round-trip OK:", restored == text)

    print("4. Other encodings")
    write("url_encoded.txt", url_encode(text))
    write("rot13_encoded.txt", rot13(text))


if __name__ == "__main__":
    main()
