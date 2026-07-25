"""Exploratory analysis placeholders for grid datasets."""

from __future__ import annotations

import pandas as pd


def summarize_dataframe(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return a starter summary table.

    TODO: Add richer EDA summaries and profiling outputs.
    """
    return dataframe.describe(include="all", datetime_is_numeric=True)
