"""
Exercise 28: Managing Sessions and Cookies

/login      GET form / POST sets session["username"]
/dashboard  "Welcome, <username>!" if logged in, otherwise redirects to /login
/logout     clears the session
A plain cookie ("last_visit") is also set to show the difference between cookies and sessions.
"""
import os
from datetime import datetime

from flask import Flask, redirect, render_template_string, request, session, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")   # signs the session cookie

LOGIN_FORM = """
<h1>Login</h1>
<form method="POST">
  <input name="username" placeholder="Username" required>
  <button type="submit">Log in</button>
</form>
{% if last_visit %}<p>Your last visit: {{ last_visit }}</p>{% endif %}
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        if username:
            session["username"] = username
            return redirect(url_for("dashboard"))
    return render_template_string(LOGIN_FORM, last_visit=request.cookies.get("last_visit"))


@app.route("/dashboard")
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))
    response = app.make_response(
        f"Welcome, {session['username']}! <a href='{url_for('logout')}'>Log out</a>")
    response.set_cookie("last_visit", datetime.now().strftime("%Y-%m-%d %H:%M"), max_age=30 * 24 * 3600)
    return response


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True, port=5001)
