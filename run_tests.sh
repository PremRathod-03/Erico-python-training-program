#!/usr/bin/env bash
# Runs every unit-test suite in the repo. Usage: ./run_tests.sh
set -e
cd "$(dirname "$0")"

echo "== Module 1: exercises";        python -m unittest discover -s 01_python_basic/ex12_unit_testing
echo "== Module 1: MP1 calculator";   (cd 01_python_basic/mini_project_1_calculator && python -m unittest)
echo "== Module 1: MP2 finance";      (cd 01_python_basic/mini_project_2_finance_tracker && python -m unittest discover -s tests)
echo "== Module 2: data processing";  python -m unittest discover -s 02_python_data_processing/tests
echo "== Module 3: Flask";            python -m unittest discover -s 03_python_web_application/tests
echo "== Module 4: MQTT (offline)";   python -m unittest discover -s 04_python_mqtt/tests
echo "All test suites passed."
