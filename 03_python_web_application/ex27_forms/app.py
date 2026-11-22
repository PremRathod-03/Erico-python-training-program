"""
Exercise 27: Handling Forms and User Input

/register  GET  -> HTML form with username and password
           POST -> prints the submitted data (server console) and shows a confirmation
"""
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        errors = []
        if not username:
            errors.append("Username is required.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if errors:
            return render_template("register.html", errors=errors, username=username), 400

        # Requirement: print the submitted data. Never print real passwords in production.
        print(f"[register] username={username!r} password={'*' * len(password)}")
        return render_template("register.html", success=True, username=username)

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True, port=5001)
