"""Shared paths for the Data Processing module."""
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # save figures to files; works without a display

MODULE_DIR = Path(__file__).resolve().parent
DATA_DIR = MODULE_DIR / "data"
TITANIC_CSV = DATA_DIR / "titanic.csv"


def output_dir(script_file: str) -> Path:
    """Return (and create) an `output/` folder next to the calling script."""
    out = Path(script_file).resolve().parent / "output"
    out.mkdir(exist_ok=True)
    return out
