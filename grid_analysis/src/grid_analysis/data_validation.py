"""Validation helpers for synthetic grid data."""

from __future__ import annotations

import pandas as pd


def check_required_columns(
    dataframe: pd.DataFrame, required_columns: set[str]
) -> list[str]:
    """Return a list of required columns missing from the dataframe."""
    return sorted(required_columns - set(dataframe.columns))


def check_missing_values(dataframe: pd.DataFrame, columns: list[str]) -> dict[str, int]:
    """Return missing-value counts for selected columns."""
    return {column: int(dataframe[column].isna().sum()) for column in columns}


def check_duplicates(dataframe: pd.DataFrame, subset: list[str] | None = None) -> int:
    """Return number of duplicated rows for an optional subset."""
    return int(dataframe.duplicated(subset=subset).sum())


def check_lat_lon_ranges(
    dataframe: pd.DataFrame,
    lat_column: str,
    lon_column: str,
) -> pd.DataFrame:
    """Return rows with latitude/longitude values outside valid ranges."""
    mask = ~dataframe[lat_column].between(-90, 90) | ~dataframe[lon_column].between(
        -180, 180
    )
    return dataframe.loc[mask]


def check_foreign_keys(
    child_dataframe: pd.DataFrame,
    parent_dataframe: pd.DataFrame,
    child_key: str,
    parent_key: str,
) -> pd.DataFrame:
    """Return child rows whose key does not exist in the parent dataframe."""
    parent_values = set(parent_dataframe[parent_key].dropna().tolist())
    return child_dataframe.loc[~child_dataframe[child_key].isin(parent_values)]
