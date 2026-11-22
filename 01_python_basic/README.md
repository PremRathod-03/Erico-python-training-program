# Module 1 – Python Basic

| # | Topic | Files |
|---|---|---|
| 1 | Setting up environment, IDE | `ex01_hello_world/hello_world.py` (setup + debugging steps in the docstring) |
| 2 | Basic variables | `ex02_basic_variables/basic_variables.py` |
| 3 | Functions | `ex03_functions/functions.py` |
| 4 | Iterative & conditional statements | `ex04_conditionals_loops/conditionals_loops.py` |
| 5 | Text encoding, decoding & pattern matching | `ex05_text_encoding/` (`input.txt` → 8 files in `output/`) |
| 6 | File handling | `ex06_file_handling/file_handling.py` |
| 7 | OOP | `ex07_oops/car.py` |
| 8 | Package imports | `ex08_package_imports/main.py` + `math_utils.py` |
| 9 | Logging | `ex09_logging/logging_demo.py` → `logs/app.log` |
| 10 | Data structures | `ex10_data_structures/data_structures.py` |
| 11 | Exception handling | `ex11_exception_handling/exception_handling.py` |
| 12 | Unit testing | `ex12_unit_testing/test_exercises.py` (tests Ex 3, 5, 8, 10, 11) |
| MP1 | Python Calculator | `mini_project_1_calculator/` |
| MP2 | Finance Transaction Tracker | `mini_project_2_finance_tracker/` |

## Run
```bash
python ex02_basic_variables/basic_variables.py
cd mini_project_1_calculator && python calculator.py
cd mini_project_2_finance_tracker && python main.py
```

## Tests
```bash
python -m unittest discover -s ex12_unit_testing -v
cd mini_project_1_calculator && python -m unittest -v
cd mini_project_2_finance_tracker && python -m unittest discover -s tests -v
```
