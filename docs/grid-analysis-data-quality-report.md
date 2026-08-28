# Grid Analysis Data-Quality Report

## Dataset Source

The electricity-grid datasets are synthetic and reproducible.
They are generated with the project dataset generator using a fixed random seed.

## Raw Dataset Sizes

| Dataset | Rows |
|---|---:|
| Utilities | 10 |
| Substations | 44 |
| Lines | 55 |

## Validation Results

| Check | Result |
|---|---:|
| Duplicate utility rows | 0 |
| Duplicate substation rows | 0 |
| Duplicate line rows | 0 |
| Invalid latitude/longitude rows | 0 |
| Invalid source-substation references | 0 |
| Invalid destination-substation references | 0 |
| Invalid utility references | 0 |
| Missing utility values | 0 |
| Missing substation values | 0 |
| Missing line values | 0 |

## Cleaned Dataset Sizes

| Dataset | Rows |
|---|---:|
| Utilities | 10 |
| Substations | 44 |
| Lines | 55 |

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
