"""Graph-building helpers for grid network analysis."""

from __future__ import annotations

import networkx as nx
import pandas as pd


def build_undirected_graph(
    nodes: pd.DataFrame,
    edges: pd.DataFrame,
    node_id_column: str = "node_id",
    source_column: str = "source",
    target_column: str = "target",
) -> nx.Graph:
    """Build an undirected graph from node and edge dataframes."""
    graph = nx.Graph()

    for _, row in nodes.iterrows():
        node_id = row[node_id_column]
        attrs = row.drop(labels=[node_id_column]).to_dict()
        graph.add_node(node_id, **attrs)

    for _, row in edges.iterrows():
        graph.add_edge(row[source_column], row[target_column])

    return graph
