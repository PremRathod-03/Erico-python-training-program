"""
Exercise 25: Creating Flask Routes

/         -> "Welcome to the Home Page"
/about    -> "This is the About Page"
/contact  -> "Contact us at contact@example.com"
"""
from flask import Flask

app = Flask(__name__)


@app.route("/")
def home():
    return "Welcome to the Home Page"


@app.route("/about")
def about():
    return "This is the About Page"


@app.route("/contact")
def contact():
    return "Contact us at contact@example.com"


@app.errorhandler(404)
def not_found(_error):
    return "Page not found. Try /, /about or /contact", 404


if __name__ == "__main__":
    app.run(debug=True, port=5001)
