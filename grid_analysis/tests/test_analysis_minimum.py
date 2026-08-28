"""Tests for minimum Grid Analysis network functionality."""

from __future__ import annotations

import networkx as nx

from grid_analysis.src.grid_analysis.contingency_analysis import (
    compare_node_removal,
)
from grid_analysis.src.grid_analysis.network_metrics import (
    calculate_degree_information,
)


def test_degree_information() -> None:
    """Basic network metrics should be calculated correctly."""

    graph = nx.Graph()

    graph.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
        ]
    )

    result = calculate_degree_information(graph)

    assert result["node_count"] == 3
    assert result["edge_count"] == 2
    assert result["average_degree"] == 4 / 3


def test_empty_graph_metrics() -> None:
    """An empty graph should return zero network values."""

    graph = nx.Graph()

    result = calculate_degree_information(graph)

    assert result["node_count"] == 0
    assert result["edge_count"] == 0
    assert result["average_degree"] == 0


def test_n1_removal_can_fragment_network() -> None:
    """Removing a critical middle node should split a simple network."""

    graph = nx.Graph()

    graph.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
        ]
    )

    result = compare_node_removal(
        graph,
        "B",
    )

    assert result["components_before"] == 1
    assert result["components_after"] == 2


def test_n1_removal_can_leave_network_connected() -> None:
    """Removing one node from a triangle should keep it connected."""

    graph = nx.Graph()

    graph.add_edges_from(
        [
            ("A", "B"),
            ("B", "C"),
            ("C", "A"),
        ]
    )

    result = compare_node_removal(
        graph,
        "A",
    )

    assert result["components_before"] == 1
    assert result["components_after"] == 1
