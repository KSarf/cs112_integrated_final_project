"""Contingency-analysis helpers for grid robustness checks."""

from __future__ import annotations

import networkx as nx


def compare_node_removal(graph: nx.Graph, node_to_remove: str) -> dict[str, int]:
    """Compare connected-component count before and after node removal."""
    baseline_components = nx.number_connected_components(graph) if graph.nodes else 0
    reduced_graph = graph.copy()
    if node_to_remove in reduced_graph:
        reduced_graph.remove_node(node_to_remove)
    post_components = (
        nx.number_connected_components(reduced_graph) if reduced_graph.nodes else 0
    )
    return {
        "components_before": baseline_components,
        "components_after": post_components,
    }
