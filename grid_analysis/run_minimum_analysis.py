"""Run the minimum Grid Analysis workflow for the CS112 project."""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import plotly.express as px

PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"

OUTPUT_DIR = Path(__file__).resolve().parent / "outputs"
NOTEBOOK_DIR = Path(__file__).resolve().parent / "notebooks"

DOCS_DIR = PROJECT_ROOT / "docs"


def load_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load the three generated grid datasets."""

    utilities = pd.read_csv(RAW_DIR / "utilities.csv")
    substations = pd.read_csv(RAW_DIR / "substations.csv")
    lines = pd.read_csv(RAW_DIR / "lines.csv")

    return utilities, substations, lines


def clean_data(
    utilities: pd.DataFrame,
    substations: pd.DataFrame,
    lines: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Perform basic reproducible cleaning."""

    utilities = utilities.drop_duplicates().copy()
    substations = substations.drop_duplicates().copy()
    lines = lines.drop_duplicates().copy()

    utilities = utilities.dropna(
        subset=[
            "Utility ID",
            "Name",
        ]
    )

    substations = substations.dropna(
        subset=[
            "Substation ID",
            "Name",
            "Latitude",
            "Longitude",
        ]
    )

    lines = lines.dropna(
        subset=[
            "Line ID",
            "Utility ID",
            "Source Substation ID",
            "Destination Substation ID",
        ]
    )

    valid_coordinates = substations["Latitude"].between(-90, 90) & substations[
        "Longitude"
    ].between(-180, 180)

    substations = substations.loc[valid_coordinates].copy()

    valid_substation_ids = set(substations["Substation ID"])
    valid_utility_ids = set(utilities["Utility ID"])

    valid_lines = (
        lines["Source Substation ID"].isin(valid_substation_ids)
        & lines["Destination Substation ID"].isin(valid_substation_ids)
        & lines["Utility ID"].isin(valid_utility_ids)
    )

    lines = lines.loc[valid_lines].copy()

    return utilities, substations, lines


def save_cleaned_data(
    utilities: pd.DataFrame,
    substations: pd.DataFrame,
    lines: pd.DataFrame,
) -> pd.DataFrame:
    """Save cleaned and integrated datasets."""

    PROCESSED_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    utilities.to_csv(
        PROCESSED_DIR / "utilities_clean.csv",
        index=False,
    )

    substations.to_csv(
        PROCESSED_DIR / "substations_clean.csv",
        index=False,
    )

    lines.to_csv(
        PROCESSED_DIR / "lines_clean.csv",
        index=False,
    )

    utility_info = utilities[
        [
            "Utility ID",
            "Name",
            "Code",
            "Type",
            "Country",
        ]
    ].rename(
        columns={
            "Name": "Utility Name",
            "Code": "Utility Code",
            "Type": "Utility Type",
            "Country": "Utility Country",
        }
    )

    source_info = substations[
        [
            "Substation ID",
            "Name",
            "Region",
            "Country",
            "Voltage (kV)",
            "Capacity (MVA)",
        ]
    ].rename(
        columns={
            "Substation ID": "Source Substation ID",
            "Name": "Source Name",
            "Region": "Source Region",
            "Country": "Source Country",
            "Voltage (kV)": "Source Voltage (kV)",
            "Capacity (MVA)": "Source Capacity (MVA)",
        }
    )

    destination_info = substations[
        [
            "Substation ID",
            "Name",
            "Region",
            "Country",
            "Voltage (kV)",
            "Capacity (MVA)",
        ]
    ].rename(
        columns={
            "Substation ID": "Destination Substation ID",
            "Name": "Destination Name",
            "Region": "Destination Region",
            "Country": "Destination Country",
            "Voltage (kV)": "Destination Voltage (kV)",
            "Capacity (MVA)": "Destination Capacity (MVA)",
        }
    )

    master = (
        lines.merge(
            utility_info,
            on="Utility ID",
            how="left",
        )
        .merge(
            source_info,
            on="Source Substation ID",
            how="left",
        )
        .merge(
            destination_info,
            on="Destination Substation ID",
            how="left",
        )
    )

    master.to_csv(
        PROCESSED_DIR / "master_grid_dataset.csv",
        index=False,
    )

    return master


def build_graph(
    substations: pd.DataFrame,
    lines: pd.DataFrame,
) -> nx.Graph:
    """Build an undirected NetworkX grid graph."""

    graph = nx.Graph()

    for _, row in substations.iterrows():
        graph.add_node(
            row["Substation ID"],
            name=row["Name"],
            region=row["Region"],
            country=row["Country"],
            voltage=row["Voltage (kV)"],
            capacity=row["Capacity (MVA)"],
        )

    for _, row in lines.iterrows():
        graph.add_edge(
            row["Source Substation ID"],
            row["Destination Substation ID"],
            line_id=row["Line ID"],
            utility_id=row["Utility ID"],
            voltage=row["Voltage (kV)"],
            capacity=row["Capacity (MVA)"],
            length=row["Length (km)"],
            status=row["Status"],
        )

    return graph


def calculate_centrality(
    graph: nx.Graph,
) -> pd.DataFrame:
    """Calculate structural network centrality values."""

    degree = nx.degree_centrality(graph)
    betweenness = nx.betweenness_centrality(graph)
    closeness = nx.closeness_centrality(graph)

    rows = []

    for node in graph.nodes:
        rows.append(
            {
                "Substation ID": node,
                "Substation Name": graph.nodes[node].get(
                    "name",
                    str(node),
                ),
                "Region": graph.nodes[node].get(
                    "region",
                    "Unknown",
                ),
                "Degree": graph.degree(node),
                "Degree Centrality": degree[node],
                "Betweenness Centrality": betweenness[node],
                "Closeness Centrality": closeness[node],
            }
        )

    centrality = pd.DataFrame(rows)

    centrality = centrality.sort_values(
        "Betweenness Centrality",
        ascending=False,
    )

    centrality.to_csv(
        PROCESSED_DIR / "centrality_results.csv",
        index=False,
    )

    centrality.head(10).to_csv(
        PROCESSED_DIR / "critical_substations.csv",
        index=False,
    )

    return centrality


def run_n1_analysis(
    graph: nx.Graph,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Run simplified N-1 node and line removal checks."""

    baseline_components = nx.number_connected_components(graph)

    node_results = []

    for node in graph.nodes:
        test_graph = graph.copy()
        test_graph.remove_node(node)

        components_after = (
            nx.number_connected_components(test_graph)
            if test_graph.number_of_nodes()
            else 0
        )

        node_results.append(
            {
                "Removed Substation ID": node,
                "Substation Name": graph.nodes[node].get(
                    "name",
                    str(node),
                ),
                "Components Before": baseline_components,
                "Components After": components_after,
                "Fragmented": components_after > baseline_components,
            }
        )

    edge_results = []

    for source, destination in graph.edges:
        test_graph = graph.copy()
        test_graph.remove_edge(
            source,
            destination,
        )

        components_after = nx.number_connected_components(test_graph)

        edge_results.append(
            {
                "Source ID": source,
                "Destination ID": destination,
                "Components Before": baseline_components,
                "Components After": components_after,
                "Fragmented": components_after > baseline_components,
            }
        )

    node_frame = pd.DataFrame(node_results)
    edge_frame = pd.DataFrame(edge_results)

    node_frame.to_csv(
        PROCESSED_DIR / "n1_node_results.csv",
        index=False,
    )

    edge_frame.to_csv(
        PROCESSED_DIR / "n1_line_results.csv",
        index=False,
    )

    return node_frame, edge_frame


def save_network_graph(
    graph: nx.Graph,
) -> None:
    """Save a simple static network graph."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    plt.figure(
        figsize=(14, 10),
    )

    positions = nx.spring_layout(
        graph,
        seed=42,
    )

    nx.draw_networkx(
        graph,
        positions,
        node_size=140,
        with_labels=False,
        width=0.8,
    )

    plt.title("Synthetic National Electricity Grid Network")

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_DIR / "network_graph.png",
        dpi=150,
        bbox_inches="tight",
    )

    plt.close()


def save_geographical_map(
    substations: pd.DataFrame,
) -> None:
    """Save an interactive geographical substation map."""

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    figure = px.scatter_geo(
        substations,
        lat="Latitude",
        lon="Longitude",
        color="Region",
        hover_name="Name",
        hover_data=[
            "Country",
            "Voltage (kV)",
            "Capacity (MVA)",
            "Status",
        ],
        title="Synthetic Grid Substation Locations",
    )

    figure.write_html(
        OUTPUT_DIR / "substation_map.html",
        include_plotlyjs="cdn",
    )


def write_quality_report(
    raw_utilities: pd.DataFrame,
    raw_substations: pd.DataFrame,
    raw_lines: pd.DataFrame,
    clean_utilities: pd.DataFrame,
    clean_substations: pd.DataFrame,
    clean_lines: pd.DataFrame,
) -> None:
    """Write a simple reproducible data-quality report."""

    valid_substation_ids = set(raw_substations["Substation ID"])

    valid_utility_ids = set(raw_utilities["Utility ID"])

    invalid_sources = int(
        (~raw_lines["Source Substation ID"].isin(valid_substation_ids)).sum()
    )

    invalid_destinations = int(
        (~raw_lines["Destination Substation ID"].isin(valid_substation_ids)).sum()
    )

    invalid_utilities = int((~raw_lines["Utility ID"].isin(valid_utility_ids)).sum())

    invalid_coordinates = int(
        (
            ~raw_substations["Latitude"].between(
                -90,
                90,
            )
            | ~raw_substations["Longitude"].between(
                -180,
                180,
            )
        ).sum()
    )

    report = f"""# Grid Analysis Data-Quality Report

## Dataset Source

The electricity-grid datasets are synthetic and reproducible.
They are generated with the project dataset generator using a fixed random seed.

## Raw Dataset Sizes

| Dataset | Rows |
|---|---:|
| Utilities | {len(raw_utilities)} |
| Substations | {len(raw_substations)} |
| Lines | {len(raw_lines)} |

## Validation Results

| Check | Result |
|---|---:|
| Duplicate utility rows | {int(raw_utilities.duplicated().sum())} |
| Duplicate substation rows | {int(raw_substations.duplicated().sum())} |
| Duplicate line rows | {int(raw_lines.duplicated().sum())} |
| Invalid latitude/longitude rows | {invalid_coordinates} |
| Invalid source-substation references | {invalid_sources} |
| Invalid destination-substation references | {invalid_destinations} |
| Invalid utility references | {invalid_utilities} |
| Missing utility values | {int(raw_utilities.isna().sum().sum())} |
| Missing substation values | {int(raw_substations.isna().sum().sum())} |
| Missing line values | {int(raw_lines.isna().sum().sum())} |

## Cleaned Dataset Sizes

| Dataset | Rows |
|---|---:|
| Utilities | {len(clean_utilities)} |
| Substations | {len(clean_substations)} |
| Lines | {len(clean_lines)} |

## Cleaning Decisions

- Exact duplicate rows are removed.
- Rows missing required identifiers are removed.
- Substations with latitude or longitude outside valid world-coordinate ranges are removed.
- Transmission lines with missing source or destination substations are removed.
- Lines referring to unknown utilities are removed.
- Raw files are preserved separately from cleaned files.

## Limitations

The dataset is synthetic and is intended for coursework.
Coordinates are illustrative rather than survey-grade.
The data does not represent live electrical loading, voltage stability,
protection systems, real-time faults, or power-flow conditions.
"""

    (DOCS_DIR / "grid-analysis-data-quality-report.md").write_text(
        report,
        encoding="utf-8",
    )


def write_data_dictionary() -> None:
    """Write the minimum grid-data dictionary."""

    text = """# Grid Analysis Data Dictionary

## utilities.csv

| Field | Meaning |
|---|---|
| Utility ID | Unique utility identifier |
| Name | Full utility name |
| Alias | Common utility abbreviation |
| Code | Short utility code |
| Type | Distribution, transmission or generation |
| Country | Utility location |
| Active | Whether the utility is marked active |

## substations.csv

| Field | Meaning |
|---|---|
| Substation ID | Unique substation identifier |
| Name | Full substation name |
| Short Name | Short location name |
| Region | Region or cross-border area |
| Country | Country |
| Latitude | Approximate latitude |
| Longitude | Approximate longitude |
| Voltage (kV) | Substation voltage rating |
| Capacity (MVA) | Approximate capacity |
| Commissioning Year | Approximate commissioning year |
| Type | Distribution, bulk supply point or transmission |
| Status | Active or inactive |

## lines.csv

| Field | Meaning |
|---|---|
| Line ID | Unique line identifier |
| Utility ID | Foreign key to utilities |
| Source Substation ID | Foreign key to source substation |
| Source Substation | Source name |
| Destination Substation ID | Foreign key to destination substation |
| Destination Substation | Destination name |
| Voltage (kV) | Line voltage |
| Length (km) | Approximate line length |
| Capacity (MVA) | Approximate line capacity |
| Status | Active or under maintenance |
| Line Type | Overhead or underground |

## Main Relationships

- `lines.Utility ID` references `utilities.Utility ID`.
- `lines.Source Substation ID` references `substations.Substation ID`.
- `lines.Destination Substation ID` references `substations.Substation ID`.
"""

    (DOCS_DIR / "grid-analysis-data-dictionary.md").write_text(
        text,
        encoding="utf-8",
    )


def write_findings(
    graph: nx.Graph,
    centrality: pd.DataFrame,
    node_n1: pd.DataFrame,
    line_n1: pd.DataFrame,
) -> None:
    """Write calculated findings and responsible limitations."""

    top = centrality.iloc[0]

    fragmented_nodes = int(node_n1["Fragmented"].sum())

    fragmented_lines = int(line_n1["Fragmented"].sum())

    findings = f"""# Grid Analysis Findings and Limitations

## Network Summary

- Number of substations: **{graph.number_of_nodes()}**
- Number of transmission/distribution lines: **{graph.number_of_edges()}**
- Connected components: **{nx.number_connected_components(graph)}**
- Average clustering coefficient: **{nx.average_clustering(graph):.3f}**
- Global network efficiency: **{nx.global_efficiency(graph):.3f}**

## Centrality

The highest-betweenness substation in this synthetic network is
**{top["Substation Name"]}**.

Its calculated betweenness centrality is
**{top["Betweenness Centrality"]:.3f}**.

High betweenness means the node lies on many shortest paths in the graph.
For this coursework this can be interpreted as a structural indicator of
network importance, but it does not directly measure electrical loading.

## N-1 Node Analysis

**{fragmented_nodes}** of **{len(node_n1)}** individual substation removals
increased the number of connected components.

## N-1 Line Analysis

**{fragmented_lines}** of **{len(line_n1)}** individual line removals
increased the number of connected components.

## Geographical Analysis

Substation latitude and longitude values are used to display the synthetic
network geographically. Regional comparisons can help identify where grid
assets and high-capacity substations are concentrated.

## Important Limitations

This analysis is a graph-based educational approximation.

It does **not** perform:

- AC or DC power-flow analysis
- Voltage-stability analysis
- Protection-coordination studies
- Frequency-stability studies
- Real-time load analysis
- Security-constrained contingency analysis

Centrality and N-1 graph fragmentation are therefore structural reliability
proxies only. They should not be presented as evidence that a real electrical
network is safe or operationally secure.
"""

    (DOCS_DIR / "grid-analysis-findings.md").write_text(
        findings,
        encoding="utf-8",
    )


def create_eda_notebook() -> None:
    """Create a reproducible minimum EDA notebook."""

    NOTEBOOK_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cells = [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# Grid Analysis Exploratory Data Analysis\n",
                "\n",
                "This notebook analyses the synthetic CS112 electricity-grid datasets.\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "from pathlib import Path\n",
                "\n",
                "import matplotlib.pyplot as plt\n",
                "import pandas as pd\n",
                "root = Path('../..')\n",
                "substations = pd.read_csv(root / 'data/processed/substations_clean.csv')\n",
                "lines = pd.read_csv(root / 'data/processed/lines_clean.csv')\n",
                "centrality = pd.read_csv(root / 'data/processed/centrality_results.csv')\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Dataset overview\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "print('Substations:', substations.shape)\n",
                "print('Lines:', lines.shape)\n",
                "display(substations.head())\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Substations by region\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "substations['Region'].value_counts().plot(kind='bar', title='Substations by Region')\n",
                "plt.ylabel('Number of Substations')\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Substation capacity distribution\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "substations['Capacity (MVA)'].plot(kind='hist', bins=12, title='Substation Capacity Distribution')\n",
                "plt.xlabel('Capacity (MVA)')\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Transmission-line status\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "lines['Status'].value_counts().plot(kind='bar', title='Transmission Line Status')\n",
                "plt.ylabel('Number of Lines')\n",
                "plt.tight_layout()\n",
                "plt.show()\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Infrastructure age\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "substations['Asset Age'] = 2026 - substations['Commissioning Year']\n",
                "substations.groupby('Region')['Asset Age'].mean().sort_values(ascending=False)\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Most structurally important substations\n",
            ],
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "centrality[['Substation Name', 'Region', 'Degree', 'Betweenness Centrality']].head(10)\n",
            ],
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## Interpretation note\n",
                "\n",
                "Centrality measures describe structural importance in the synthetic graph. "
                "They do not directly measure real electrical load, voltage stability or power flow.\n",
            ],
        },
    ]

    notebook = {
        "cells": cells,
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3",
            },
            "language_info": {
                "name": "python",
            },
        },
        "nbformat": 4,
        "nbformat_minor": 5,
    }

    notebook_path = NOTEBOOK_DIR / "grid_analysis_eda.ipynb"

    notebook_path.write_text(
        json.dumps(
            notebook,
            indent=1,
        ),
        encoding="utf-8",
    )


def main() -> None:
    """Run the complete minimum analysis pipeline."""

    print("Loading raw datasets...")

    raw_utilities, raw_substations, raw_lines = load_data()

    print("Cleaning and validating datasets...")

    utilities, substations, lines = clean_data(
        raw_utilities,
        raw_substations,
        raw_lines,
    )

    print("Saving cleaned and integrated datasets...")

    save_cleaned_data(
        utilities,
        substations,
        lines,
    )

    print("Building network graph...")

    graph = build_graph(
        substations,
        lines,
    )

    print("Calculating centrality...")

    centrality = calculate_centrality(
        graph,
    )

    print("Running N-1 analysis...")

    node_n1, line_n1 = run_n1_analysis(
        graph,
    )

    print("Creating visualisations...")

    save_network_graph(
        graph,
    )

    save_geographical_map(
        substations,
    )

    print("Writing documentation...")

    write_quality_report(
        raw_utilities,
        raw_substations,
        raw_lines,
        utilities,
        substations,
        lines,
    )

    write_data_dictionary()

    write_findings(
        graph,
        centrality,
        node_n1,
        line_n1,
    )

    create_eda_notebook()

    print()
    print("Grid Analysis minimum pipeline complete.")
    print(f"Utilities: {len(utilities)}")
    print(f"Substations: {len(substations)}")
    print(f"Lines: {len(lines)}")
    print(f"Graph nodes: {graph.number_of_nodes()}")
    print(f"Graph edges: {graph.number_of_edges()}")


if __name__ == "__main__":
    main()
