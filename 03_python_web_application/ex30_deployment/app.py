"""
Exercise 30: Deploying Flask Applications (production-ready app)

Local dev:     python app.py
Local WSGI:    gunicorn --bind 0.0.0.0:8000 app:app
Heroku:        uses Procfile  (web: gunicorn app:app)
Docker:        docker build -t flask-deploy-demo . && docker run -p 8000:8000 flask-deploy-demo
"""
import os

from flask import Flask, jsonify

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "change-me-in-production")


@app.route("/")
def index():
    return "Hello, World!"


@app.route("/health")
def health():
    """Used by Docker HEALTHCHECK / load balancers."""
    return jsonify(status="ok"), 200


if __name__ == "__main__":
    # debug is off unless FLASK_DEBUG=1 is set
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)),
            debug=os.environ.get("FLASK_DEBUG") == "1")
