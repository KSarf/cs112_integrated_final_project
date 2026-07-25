"""Business-intelligence placeholders for grid-analysis reporting."""

from __future__ import annotations

import pandas as pd


def prepare_kpi_table(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Prepare starter KPI table.

    TODO: Define domain KPI formulas.
    """
    return dataframe.head(0).copy()
