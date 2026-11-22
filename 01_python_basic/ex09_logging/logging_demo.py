"""
Exercise 9: Logging

- log at DEBUG, INFO, WARNING, ERROR, CRITICAL
- configure a logger that writes to a file (logs/app.log) with a custom format
- console handler shows INFO and above; file keeps everything (DEBUG+)
"""
import logging
from pathlib import Path

LOG_DIR = Path(__file__).resolve().parent / "logs"
LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(funcName)s:%(lineno)d | %(message)s"


def setup_logger(name: str = "training_app") -> logging.Logger:
    LOG_DIR.mkdir(exist_ok=True)
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    if logger.handlers:            # avoid duplicate handlers on re-import
        return logger

    file_handler = logging.FileHandler(LOG_DIR / "app.log", mode="w", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(LOG_FORMAT, datefmt="%Y-%m-%d %H:%M:%S"))

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
    return logger


logger = setup_logger()


def divide(a: float, b: float) -> float | None:
    logger.debug("divide called with a=%s b=%s", a, b)
    try:
        return a / b
    except ZeroDivisionError:
        logger.error("Division by zero attempted with a=%s", a, exc_info=True)
        return None


def main() -> None:
    logger.debug("Debug details - only visible in the log file")
    logger.info("Application started")
    logger.warning("Disk space is below 20%%")
    divide(10, 2)
    divide(5, 0)
    logger.critical("Database connection lost - shutting down")
    print(f"\nFull log written to {LOG_DIR / 'app.log'}")


if __name__ == "__main__":
    main()
