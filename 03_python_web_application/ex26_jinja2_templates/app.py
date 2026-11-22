"""
Exercise 26: Using Jinja2 for Templating

/profile renders templates/profile.html with a dictionary passed from the view.
"""
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/profile")
def profile():
    user = {"name": "Alice", "age": 25,
            "skills": ["Python", "Flask", "Pandas"], "is_admin": False}
    return render_template("profile.html", user=user)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
