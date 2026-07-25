"""Tests for grid-analysis data validation helpers."""

from __future__ import annotations

import pandas as pd

from grid_analysis.src.grid_analysis.data_validation import (
    check_duplicates,
    check_foreign_keys,
    check_lat_lon_ranges,
    check_missing_values,
    check_required_columns,
)


def test_required_columns_and_missing_values() -> None:
    dataframe = pd.DataFrame({"node_id": [1, 2], "name": ["A", None]})
    assert check_required_columns(dataframe, {"node_id", "name", "region"}) == [
        "region"
    ]
    assert check_missing_values(dataframe, ["name"]) == {"name": 1}


def test_duplicates_lat_lon_and_foreign_keys() -> None:
    nodes = pd.DataFrame(
        {
            "node_id": [1, 1, 2],
            "latitude": [5.0, 101.0, 6.0],
            "longitude": [0.1, 0.2, -181.0],
        }
    )
    parents = pd.DataFrame({"node_id": [1]})

    assert check_duplicates(nodes, subset=["node_id"]) == 1
    assert len(check_lat_lon_ranges(nodes, "latitude", "longitude")) == 2
    assert len(check_foreign_keys(nodes, parents, "node_id", "node_id")) == 1
