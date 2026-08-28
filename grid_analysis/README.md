Grid Analysis

Grid Analysis is the analytical component of the CS112 final project.

It uses synthetic electricity-grid datasets to demonstrate data cleaning,
validation, network analysis, geographical analysis, simplified N-1
contingency analysis, exploratory data analysis, and dashboard visualisation.

## Technology

The component uses:

- Python
- pandas
- NetworkX
- Matplotlib
- Plotly
- Streamlit
- pytest

## Dataset

The project uses three synthetic datasets:

- `utilities.csv`
- `substations.csv`
- `lines.csv`

The data generator uses a fixed random seed so results are reproducible.

The generated dataset contains approximately:

- 10 utilities
- 44 substations
- 55 transmission/distribution lines

The data is educational and does not represent a live electricity grid.

## Generate the Raw Data

From the repository root:

```bash
cd data/raw
python ../../scripts/generate_grid_data.py
cd ../..
```

The generated CSV files are stored locally under:

```text
data/raw/
```

Raw and processed CSV files are ignored by Git because they can be
reproduced from the generator and analysis pipeline.

## Run the Minimum Analysis Pipeline

From the repository root:

```bash
python grid_analysis/run_minimum_analysis.py
```

The generated CSV files are stored locally under:

data/raw/

Raw and processed CSV files are ignored by Git because they can be
reproduced from the generator and analysis pipeline.

Run the Minimum Analysis Pipeline

From the repository root:

python grid_analysis/run_minimum_analysis.py

The pipeline performs:

Data loading
Duplicate handling
Missing-value checks
Coordinate validation
Foreign-key validation
Clean dataset creation
Master dataset integration
Network graph construction
Centrality analysis
Simplified N-1 substation analysis
Simplified N-1 line analysis
Network graph output
Geographic map output
Data-quality documentation
Data dictionary creation
Findings and limitations
EDA notebook creation

## Generated Processed Data

The pipeline generates:

data/processed/
├── utilities_clean.csv
├── substations_clean.csv
├── lines_clean.csv
├── master_grid_dataset.csv
├── centrality_results.csv
├── critical_substations.csv
├── n1_node_results.csv
└── n1_line_results.csv

## Analysis Outputs

Visual outputs are generated under:

grid_analysis/outputs/
├── network_graph.png
└── substation_map.html
## Exploratory Data Analysis

The reproducible EDA notebook is:

grid_analysis/notebooks/grid_analysis_eda.ipynb

It explores:

Dataset size
Substations by region
Capacity distribution
Transmission-line status
Infrastructure age
Structurally important substations

## Network Analysis

The grid is represented as an undirected NetworkX graph.

Substations are nodes and transmission/distribution lines are edges.

The project calculates:

Number of nodes
Number of edges
Average degree
Degree centrality
Betweenness centrality
Closeness centrality
Connected components
Clustering coefficient
Global network efficiency


## Simplified N-1 Analysis

The analysis removes one network component at a time.

Substation N-1

Each substation is removed and the number of connected components before
and after removal is compared.

Line N-1

Each line is removed and the network is checked for additional fragmentation.

This is a graph-based educational approximation.

It is not a power-flow or electrical stability study.

## Geographic Analysis

Substation coordinates are visualised using an interactive Plotly map.

The geographical analysis can be used to examine:

Regional infrastructure distribution
Substation locations
Voltage levels
Capacity values
Cross-border grid connections

## Dashboard

Start the Streamlit dashboard from the repository root:

python -m streamlit run grid_analysis/dashboard/app.py

The dashboard contains:

Overview
Network
Geography
Reliability
Search

The dashboard reads the cleaned datasets when they are available.

If cleaned datasets are not available, it falls back to the generated raw
datasets and displays a warning.

The dashboard includes calculated structural network metrics and does not use
a hard-coded reliability percentage.

## Documentation

Analysis documentation is generated under:

docs/grid-analysis-data-quality-report.md
docs/grid-analysis-data-dictionary.md
docs/grid-analysis-findings.md
Data-quality report

Documents:

Missing values
Duplicate rows
Invalid coordinates
Invalid foreign-key references
Cleaning decisions
Cleaned dataset sizes
Data dictionary

Documents the meaning and relationships of the utilities, substations,
and transmission-line fields.

Findings and limitations

Summarises the calculated network results and clearly explains the limits
of graph-based reliability analysis.

## Testing

Run Grid Analysis tests with:

python -m pytest grid_analysis/tests -q

The tests cover:

Data validation
Network graph construction
Basic network metrics
N-1 fragmentation behaviour

## Code Quality

Run:

python -m black grid_analysis
python -m ruff check grid_analysis

## Important Limitations

The dataset and analysis are educational.

The project does not perform:

AC power flow
DC power flow
Voltage stability
Frequency stability
Protection coordination
Real-time fault analysis
Real-time load analysis
Security-constrained contingency analysis

Network centrality and graph fragmentation should therefore be treated
as structural indicators only.

They should not be interpreted as proof that a real electricity system
is safe, stable, or reliable.