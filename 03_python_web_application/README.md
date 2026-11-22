# Module 3 – Python Web Application (Flask)

| # | Topic | Files | URL to try |
|---|---|---|---|
| 22 | Intro to Flask | `ex22_flask_intro/app.py` | `/` → Hello, Flask! |
| 23 | Project structure | `ex23_flask_project_structure/my_flask_app/` | `/` |
| 24 | HTTP request handling | `ex24_http_requests/app.py` | `GET /greet?name=Alice`, `POST /submit` |
| 25 | Flask routes | `ex25_flask_routes/app.py` | `/`, `/about`, `/contact` |
| 26 | Jinja2 templating | `ex26_jinja2_templates/` | `/profile` |
| 27 | Forms & user input | `ex27_forms/` | `/register` |
| 28 | Sessions & cookies | `ex28_sessions_cookies/app.py` | `/login` → `/dashboard` |
| 29 | Basic CRUD | `ex29_crud/app.py` | `/books` (GET/POST/PUT/DELETE) |
| 30 | Deployment | `ex30_deployment/` (gunicorn, Procfile, Dockerfile) | `/`, `/health` |
| MP6 | Simple To-Do App | `mini_project_6_todo_app/` | `/` |

Run any app with `python app.py` from its folder, then open http://127.0.0.1:5001.
Port **5001** is used because macOS reserves 5000 for AirPlay Receiver.

Tests (Flask test client, no server needed): `python -m unittest discover -s tests -v`
