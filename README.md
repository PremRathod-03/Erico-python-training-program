# Python Training Program – Exercises & Mini-Projects

Solutions for the four-course Python training schema: **41 exercises** and **mini-projects 1, 2, 4, 5, 6 and 7**. The full schema is in [`curriculum/Python_Curriculum.xlsx`](curriculum/Python_Curriculum.xlsx).

| Course | Duration | Exercises | Mini-projects | Folder |
|---|---|---|---|---|
| Python Basic | 3 weeks | 1 – 12 | MP1 Calculator, MP2 Finance Transaction Tracker | [`01_python_basic`](01_python_basic) |
| Python Data Processing | 4 weeks | 13 – 21 | MP4 Titanic Analysis, MP5 Titanic Transformations | [`02_python_data_processing`](02_python_data_processing) |
| Python Web Application | 3 weeks | 22 – 30 | MP6 Flask To-Do App | [`03_python_web_application`](03_python_web_application) |
| Python MQTT | 3 weeks | 31 – 41 | MP7 MQTT Publisher/Subscriber | [`04_python_mqtt`](04_python_mqtt) |

Each module folder has its own README that maps every exercise to its files and shows how to run it.

## Setup
```bash
git clone <this-repo-url> && cd <repo-folder>
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
The MQTT module also needs a broker: `brew install mosquitto && mosquitto -v`.

## Run all tests
```bash
python -m unittest discover -s 01_python_basic/ex12_unit_testing
(cd 01_python_basic/mini_project_1_calculator && python -m unittest)
(cd 01_python_basic/mini_project_2_finance_tracker && python -m unittest discover -s tests)
python -m unittest discover -s 02_python_data_processing/tests
python -m unittest discover -s 03_python_web_application/tests
python -m unittest discover -s 04_python_mqtt/tests
```
Or run them all at once with `./run_tests.sh`.

## Highlights
- **MP1 Calculator** – menu-driven loop, one function per operation, input validation, history; tested with mocked `input()`.
- **MP2 Finance Tracker** – `Transaction` → `Income` / `Expense` inheritance, logging, validation, JSON persistence, 14 unit tests including mocked loggers.
- **MP4/MP5 Titanic** – pandas analysis of the 891-passenger dataset: crosstabs, age groups, Min-Max / Z-score normalisation, survival pivot and chart.
- **MP6 To-Do App** – Flask + Jinja2 template inheritance, add / complete / delete / filter / clear, flash messages, in-memory state.
- **MP7 MQTT** – paho-mqtt 2.x publisher of random JSON data and a subscriber that shows it as a live table.
- **Deployment** – gunicorn, Procfile (Heroku) and a non-root Dockerfile with a health check (Exercise 30).
- **MQTT security** – password file plus TLS certificates (Exercise 39), with secrets git-ignored.

## Tech
Python 3.10+ · NumPy · pandas · Matplotlib · Flask · gunicorn · Docker · Mosquitto · paho-mqtt · unittest
