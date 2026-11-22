"""Tests for every Flask exercise and the To-Do mini-project (uses Flask's test client)."""
import importlib.util
import sys
import unittest
from pathlib import Path

MODULE = Path(__file__).resolve().parent.parent


def load_app(relative: str):
    """Import an app.py by path (every exercise has its own app.py)."""
    path = MODULE / relative
    name = "app_" + relative.replace("/", "_").replace(".py", "")
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod          # Flask uses this to locate templates/ and static/
    spec.loader.exec_module(mod)
    mod.app.config["TESTING"] = True
    return mod


class TestIntroAndStructure(unittest.TestCase):
    def test_ex22_hello(self):
        client = load_app("ex22_flask_intro/app.py").app.test_client()
        self.assertEqual(client.get("/").data, b"Hello, Flask!")

    def test_ex23_template_and_static(self):
        client = load_app("ex23_flask_project_structure/my_flask_app/app.py").app.test_client()
        page = client.get("/")
        self.assertIn(b"My Flask App", page.data)
        with client.get("/static/style.css") as css:
            self.assertEqual(css.status_code, 200)


class TestHttpRequests(unittest.TestCase):
    def setUp(self):
        self.client = load_app("ex24_http_requests/app.py").app.test_client()

    def test_greet(self):
        self.assertEqual(self.client.get("/greet?name=Alice").data, b"Hello, Alice!")

    def test_submit_valid(self):
        r = self.client.post("/submit", json={"name": "Alice", "age": 25})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.get_json(), {"status": "success", "message": "Data received!"})

    def test_submit_invalid(self):
        for body in [{"name": "", "age": 25}, {"name": "Bob", "age": -1},
                     {"name": "Bob", "age": "25"}, {"name": "Bob", "age": True}, {"name": "Bob"}]:
            r = self.client.post("/submit", json=body)
            self.assertEqual(r.status_code, 400, body)
            self.assertEqual(r.get_json()["status"], "error")
        self.assertEqual(self.client.post("/submit", data="not json").status_code, 400)


class TestRoutesTemplatesForms(unittest.TestCase):
    def test_ex25_routes(self):
        c = load_app("ex25_flask_routes/app.py").app.test_client()
        self.assertEqual(c.get("/").data, b"Welcome to the Home Page")
        self.assertEqual(c.get("/about").data, b"This is the About Page")
        self.assertEqual(c.get("/contact").data, b"Contact us at contact@example.com")
        self.assertEqual(c.get("/nope").status_code, 404)

    def test_ex26_profile(self):
        html = load_app("ex26_jinja2_templates/app.py").app.test_client().get("/profile").data.decode()
        self.assertIn("Alice", html)
        self.assertIn("25", html)
        self.assertIn("FLASK", html)

    def test_ex27_register(self):
        c = load_app("ex27_forms/app.py").app.test_client()
        self.assertIn(b"<form", c.get("/register").data)
        ok = c.post("/register", data={"username": "prem", "password": "secret123"})
        self.assertIn(b"Registration received", ok.data)
        bad = c.post("/register", data={"username": "", "password": "123"})
        self.assertEqual(bad.status_code, 400)


class TestSessions(unittest.TestCase):
    def test_login_flow(self):
        c = load_app("ex28_sessions_cookies/app.py").app.test_client()
        r = c.get("/dashboard")
        self.assertEqual(r.status_code, 302)
        self.assertIn("/login", r.headers["Location"])
        c.post("/login", data={"username": "Prem"})
        r = c.get("/dashboard")
        self.assertIn(b"Welcome, Prem!", r.data)
        c.get("/logout")
        self.assertEqual(c.get("/dashboard").status_code, 302)


class TestCrud(unittest.TestCase):
    def test_crud_cycle(self):
        c = load_app("ex29_crud/app.py").app.test_client()
        self.assertEqual(len(c.get("/books").get_json()), 2)
        created = c.post("/books", json={"title": "Fluent Python", "author": "L. Ramalho", "year": 2022})
        self.assertEqual(created.status_code, 201)
        book_id = created.get_json()["id"]
        self.assertEqual(c.get(f"/books/{book_id}").get_json()["title"], "Fluent Python")
        updated = c.put(f"/books/{book_id}", json={"year": 2023})
        self.assertEqual(updated.get_json()["year"], 2023)
        self.assertEqual(c.delete(f"/books/{book_id}").status_code, 200)
        self.assertEqual(c.get(f"/books/{book_id}").status_code, 404)
        self.assertEqual(c.post("/books", json={"title": "x"}).status_code, 400)
        self.assertEqual(c.put("/books/999", json={"year": 2000}).status_code, 404)


class TestDeployment(unittest.TestCase):
    def test_app_and_files(self):
        c = load_app("ex30_deployment/app.py").app.test_client()
        self.assertEqual(c.get("/").data, b"Hello, World!")
        self.assertEqual(c.get("/health").get_json(), {"status": "ok"})
        for f in ["Procfile", "Dockerfile", "requirements.txt"]:
            self.assertTrue((MODULE / "ex30_deployment" / f).exists(), f)


class TestTodoApp(unittest.TestCase):
    def setUp(self):
        self.mod = load_app("mini_project_6_todo_app/app.py")
        self.c = self.mod.app.test_client()

    def test_add_view_toggle_delete(self):
        self.c.post("/add", data={"title": "Finish MQTT module", "priority": "high"})
        self.c.post("/add", data={"title": "Push to GitHub"})
        page = self.c.get("/").data.decode()
        self.assertIn("Finish MQTT module", page)
        self.assertIn("0/2 completed", page)

        first_id = self.mod.tasks[0]["id"]
        self.c.post(f"/toggle/{first_id}")
        self.assertTrue(self.mod.tasks[0]["done"])
        self.assertIn("Push to GitHub", self.c.get("/?show=active").data.decode())
        self.assertNotIn("Finish MQTT module", self.c.get("/?show=active").data.decode())

        self.c.post(f"/delete/{first_id}")
        self.assertEqual([t["title"] for t in self.mod.tasks], ["Push to GitHub"])

    def test_validation_and_missing_task(self):
        r = self.c.post("/add", data={"title": "   "}, follow_redirects=True)
        self.assertIn("cannot be empty", r.data.decode())
        self.assertEqual(self.mod.tasks, [])
        r = self.c.post("/delete/999", follow_redirects=True)
        self.assertIn("does not exist", r.data.decode())

    def test_clear_completed(self):
        for t in ["a", "b", "c"]:
            self.c.post("/add", data={"title": t})
        for task in self.mod.tasks[:2]:
            self.c.post(f"/toggle/{task['id']}")
        self.c.post("/clear-completed")
        self.assertEqual([t["title"] for t in self.mod.tasks], ["c"])


if __name__ == "__main__":
    unittest.main()
