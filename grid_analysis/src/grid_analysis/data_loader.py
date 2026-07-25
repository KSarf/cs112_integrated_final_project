"""Data loading utilities for grid-analysis workflows."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


def load_csv_files(file_map: dict[str, Path]) -> dict[str, pd.DataFrame]:
    """Load CSV files from a label-to-path mapping.

    TODO: Add schema-aware parsing options when source formats are finalized.
    """
    loaded: dict[str, pd.DataFrame] = {}
    for label, path in file_map.items():
        loaded[label] = pd.read_csv(path)
    return loaded
