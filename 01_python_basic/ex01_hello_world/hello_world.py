"""
Exercise 1: Hello World & Basic Debugging

Setup (done once):
  1. Install Python 3.10+ from python.org (or `brew install python` on macOS).
  2. Install VS Code + the "Python" extension (or PyCharm Community).
  3. Open this repo folder, select the interpreter (Cmd/Ctrl+Shift+P -> "Python: Select Interpreter").
  4. Run:  python hello_world.py

Debugging practice:
  - Put a breakpoint on the line `message = build_message(name)` (click left of the line number).
  - Press F5 -> "Python File". Step Into (F11) to enter build_message, Step Over (F10) to move on.
  - Watch the `name` and `message` variables in the VARIABLES panel.
"""


def build_message(name: str) -> str:
    """Return a greeting for the given name."""
    return f"Hello, {name}!"


def main() -> None:
    print("Hello, World!")

    name = "Python Learner"
    message = build_message(name)   # <- good place for a breakpoint
    print(message)


if __name__ == "__main__":
    main()
