"""
Exercise 24: Understanding HTTP Request Handling

GET  /greet?name=Alice   -> "Hello, Alice!"
POST /submit  JSON {"name": "Alice", "age": 25}
     valid   -> {"status": "success", "message": "Data received!"}
     invalid -> {"status": "error", "message": "Invalid input!"}  (HTTP 400)

Try it:
  curl "http://127.0.0.1:5001/greet?name=Alice"
  curl -X POST http://127.0.0.1:5001/submit -H "Content-Type: application/json" \
       -d '{"name": "Alice", "age": 25}'
"""
from flask import Flask, jsonify, request

app = Flask(__name__)


@app.route("/greet", methods=["GET"])
def greet():
    name = request.args.get("name", "").strip() or "Guest"
    return f"Hello, {name}!"


def is_valid(payload) -> bool:
    if not isinstance(payload, dict):
        return False
    name, age = payload.get("name"), payload.get("age")
    name_ok = isinstance(name, str) and name.strip() != ""
    # bool is a subclass of int, so exclude it explicitly
    age_ok = isinstance(age, int) and not isinstance(age, bool) and age > 0
    return name_ok and age_ok


@app.route("/submit", methods=["POST"])
def submit():
    payload = request.get_json(silent=True)
    if is_valid(payload):
        return jsonify({"status": "success", "message": "Data received!"}), 200
    return jsonify({"status": "error", "message": "Invalid input!"}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5001)
