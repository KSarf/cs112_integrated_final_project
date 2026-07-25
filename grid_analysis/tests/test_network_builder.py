"""Smoke tests for network-building helpers."""

from __future__ import annotations

import pandas as pd

from grid_analysis.src.grid_analysis.contingency_analysis import compare_node_removal
from grid_analysis.src.grid_analysis.network_builder import build_undirected_graph
from grid_analysis.src.grid_analysis.network_metrics import calculate_degree_information


def test_build_graph_smoke() -> None:
    nodes = pd.DataFrame(
        [
            {"node_id": "N1", "label": "Node 1"},
            {"node_id": "N2", "label": "Node 2"},
            {"node_id": "N3", "label": "Node 3"},
        ]
    )
    edges = pd.DataFrame(
        [
            {"source": "N1", "target": "N2"},
            {"source": "N2", "target": "N3"},
        ]
    )

    graph = build_undirected_graph(nodes, edges)

    assert graph.number_of_nodes() == 3
    assert graph.number_of_edges() == 2
    assert calculate_degree_information(graph)["average_degree"] > 0
    comparison = compare_node_removal(graph, "N2")
    assert comparison["components_after"] >= comparison["components_before"]
