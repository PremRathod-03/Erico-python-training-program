"""
Exercise 29: Basic CRUD Operations with Flask (in-memory, JSON REST API)

GET    /books           list all books
GET    /books/<id>      read one book
POST   /books           create   {"title": "...", "author": "...", "year": 2020}
PUT    /books/<id>      update   (any of title/author/year)
DELETE /books/<id>      delete

Example:
  curl -X POST http://127.0.0.1:5001/books -H "Content-Type: application/json" \
       -d '{"title": "Fluent Python", "author": "Luciano Ramalho", "year": 2022}'
"""
from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {"id": 1, "title": "Automate the Boring Stuff", "author": "Al Sweigart", "year": 2019},
    {"id": 2, "title": "Python Crash Course", "author": "Eric Matthes", "year": 2023},
]
next_id = 3


def find_book(book_id: int):
    return next((b for b in books if b["id"] == book_id), None)


def validate(data: dict, partial: bool = False) -> str | None:
    required = ["title", "author", "year"]
    if not isinstance(data, dict):
        return "Request body must be JSON"
    if not partial:
        missing = [f for f in required if f not in data]
        if missing:
            return f"Missing fields: {', '.join(missing)}"
    for field in ("title", "author"):
        if field in data and (not isinstance(data[field], str) or not data[field].strip()):
            return f"{field} must be a non-empty string"
    if "year" in data and (not isinstance(data["year"], int) or isinstance(data["year"], bool)
                           or not 0 < data["year"] <= 2100):
        return "year must be a valid integer"
    return None


@app.get("/books")
def list_books():
    return jsonify(books)


@app.get("/books/<int:book_id>")
def get_book(book_id):
    book = find_book(book_id)
    return (jsonify(book), 200) if book else (jsonify({"error": "Book not found"}), 404)


@app.post("/books")
def create_book():
    global next_id
    data = request.get_json(silent=True)
    error = validate(data)
    if error:
        return jsonify({"error": error}), 400
    book = {"id": next_id, "title": data["title"].strip(),
            "author": data["author"].strip(), "year": data["year"]}
    books.append(book)
    next_id += 1
    return jsonify(book), 201


@app.put("/books/<int:book_id>")
def update_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    data = request.get_json(silent=True)
    error = validate(data, partial=True)
    if error:
        return jsonify({"error": error}), 400
    for field in ("title", "author", "year"):
        if field in data:
            book[field] = data[field].strip() if isinstance(data[field], str) else data[field]
    return jsonify(book)


@app.delete("/books/<int:book_id>")
def delete_book(book_id):
    book = find_book(book_id)
    if not book:
        return jsonify({"error": "Book not found"}), 404
    books.remove(book)
    return jsonify({"message": f"Book {book_id} deleted"})


if __name__ == "__main__":
    app.run(debug=True, port=5001)
