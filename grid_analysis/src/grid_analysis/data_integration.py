"""Dataset integration helpers for grid-analysis."""

from __future__ import annotations

import pandas as pd


def merge_datasets(
    left: pd.DataFrame,
    right: pd.DataFrame,
    on: str,
    how: str = "inner",
) -> pd.DataFrame:
    """Merge two datasets on a shared key.

    TODO: Add explicit cardinality checks once schemas are finalized.
    """
    return left.merge(right, on=on, how=how)
