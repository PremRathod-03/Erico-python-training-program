"""
Exercise 22: Introduction to Flask

Install:  pip install flask
Run:      python app.py      then open http://127.0.0.1:5001
(Port 5001 is used because macOS reserves 5000 for AirPlay Receiver.)
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, Flask!"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
