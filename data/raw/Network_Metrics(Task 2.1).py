from pathlib import Path

import networkx as nx
import pandas as pd
from networkx.algorithms.community import greedy_modularity_communities

BASE_DIR = Path(__file__).parent

substations = pd.read_csv(BASE_DIR / "substations.csv")
lines = pd.read_csv(BASE_DIR / "lines.csv")

G = nx.Graph()
# adding substations as nodes
for _, row in substations.iterrows():
    G.add_node(
        row["Substation ID"],
        name=row["Name"],
        region=row["Region"],
        voltage=row["Voltage (kV)"],
        capacity=row["Capacity (MVA)"],
        latitude=row["Latitude"],
        longitude=row["Longitude"],
        status=row["Status"],
    )
# adding lines as edges
for _, row in lines.iterrows():
    G.add_edge(
        row["Source Substation ID"],
        row["Destination Substation ID"],
        line_id=row["Line ID"],
        utility_id=row["Utility ID"],
        voltage=row["Voltage (kV)"],
        capacity=row["Capacity (MVA)"],
        length=row["Length (km)"],
        status=row["Status"],
    )

print(f"Graph built: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")
print()

degree = dict(G.degree())
betweenness = nx.betweenness_centrality(G)
closeness = nx.closeness_centrality(G)
pagerank = nx.pagerank(G)

# Calculating top 5 nodes under each metric

print("Top 5 by degree (most direct connections):")
for node_id, val in sorted(degree.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {G.nodes[node_id]['name']}: {val}")

print()
print("Top 5 by betweenness centrality (critical pathways):")
for node_id, val in sorted(betweenness.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {G.nodes[node_id]['name']}: {val:.3f}")

print()
print("Top 5 by PageRank:")
for node_id, val in sorted(pagerank.items(), key=lambda x: x[1], reverse=True)[:5]:
    print(f"  {G.nodes[node_id]['name']}: {val:.3f}")

# Network Diameter and Average Shortest Path Length
if nx.is_connected(G):
    diameter = nx.diameter(G)
    avg_shortest_path_length = nx.average_shortest_path_length(G)
    print()
    print(f"Network Diameter: {diameter}")
    print(f"Average Shortest Path Length: {avg_shortest_path_length:.3f}")

else:
    largest_cc = max(nx.connected_components(G), key=len)
    G_main = G.subgraph(largest_cc)
    print(
        f"Network is disconnected. Largest component: {len(largest_cc)}/{G.number_of_nodes()} nodes"
    )
    print("Diameter (largest component):", nx.diameter(G_main))
    print(
        "Average shortest path length (largest component):",
        round(nx.average_shortest_path_length(G_main), 2),
    )

# --- Clustering coefficients ---
print()
print("Average clustering coefficient:", round(nx.average_clustering(G), 3))

# --- Community detection ---
print()
communities = greedy_modularity_communities(G)
print(f"Detected {len(communities)} communities")
for i, comm in enumerate(communities):
    names = [G.nodes[n]["name"] for n in comm]
    print(f"  Community {i+1} ({len(comm)} nodes): {names}")

# --- Critical-substation identification (articulation points) ---
print()
articulation_points = list(nx.articulation_points(G))
print(f"Critical substations (articulation points): {len(articulation_points)}")
for node_id in articulation_points:
    print(f"  {G.nodes[node_id]['name']}")

# =====================================================================
# Analyse network structure
# =====================================================================

# --- Most-connected substations (regional 'superhubs') ---
# Already computed above via degree.

# --- Bridge lines (critical single points of connection) ---
print()
bridges = list(nx.bridges(G))
print(f"Bridge lines (single points of failure): {len(bridges)}")
for a, b in bridges:
    print(f"  {G.nodes[a]['name']} <-> {G.nodes[b]['name']}")

# --- Isolated components ---
print()
components = sorted(nx.connected_components(G), key=len, reverse=True)
print(f"Connected components (isolated network islands): {len(components)}")
for i, comp in enumerate(components):
    names = [G.nodes[n]["name"] for n in comp]
    print(f"  Component {i+1} ({len(comp)} nodes): {names}")

# --- Network efficiency ---
print()
print("Global network efficiency:", round(nx.global_efficiency(G), 3))
