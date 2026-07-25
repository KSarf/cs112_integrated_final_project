"""Geographic-analysis placeholders for grid datasets."""

from __future__ import annotations

import pandas as pd


def summarize_coordinates(dataframe: pd.DataFrame) -> dict[str, int]:
    """Return placeholder coordinate summary.

    TODO: Add geospatial clustering and route-distance checks.
    """
    return {"records": int(len(dataframe))}
