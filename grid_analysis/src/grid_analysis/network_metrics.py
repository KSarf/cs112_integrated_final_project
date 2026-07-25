"""Network metrics for grid analysis."""

from __future__ import annotations

import networkx as nx


def calculate_degree_information(graph: nx.Graph) -> dict[str, float]:
    """Calculate basic degree metrics for a graph."""
    node_count = graph.number_of_nodes()
    edge_count = graph.number_of_edges()
    average_degree = (2 * edge_count / node_count) if node_count else 0.0
    return {
        "node_count": float(node_count),
        "edge_count": float(edge_count),
        "average_degree": average_degree,
    }
