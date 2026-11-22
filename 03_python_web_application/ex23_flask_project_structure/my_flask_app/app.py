"""
Exercise 23: Setting up a Flask project

my_flask_app/
├── app.py
├── templates/
│   └── index.html
└── static/
    └── style.css

Run:  python app.py   ->  http://127.0.0.1:5001
"""
from flask import Flask, render_template

app = Flask(__name__)   # finds ./templates and ./static automatically


@app.route("/")
def index():
    return render_template("index.html", title="My Flask App")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
