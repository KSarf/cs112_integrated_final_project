"""Visualization placeholders for grid-analysis outputs."""

from __future__ import annotations

import pandas as pd


def build_placeholder_chart_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return data suitable for future visual rendering.

    TODO: Add matplotlib/plotly/folium visual generation.
    """
    return dataframe.copy()
