# CS112 Final Project

This repository contains three completed components:

1. Grid Analysis
2. GridCare-Lite
3. ClinicCare-Lite

## Components

### Grid Analysis
Analyses synthetic electricity-grid data using pandas, NetworkX, Plotly,
Matplotlib and Streamlit.

### GridCare-Lite
Tkinter desktop application for outage, work-order and maintenance management.

### ClinicCare-Lite
Flask web application for non-urgent clinic administration and communication.

## Integration

Grid Analysis produces cleaned substation and transmission-line datasets.

GridCare-Lite uses the cleaned Grid Analysis datasets when available.
If processed data has not yet been generated, GridCare falls back to the
original synthetic datasets.

ClinicCare-Lite remains separate because clinic and electricity-grid data
have different purposes and security boundaries.

## Installation

Create and activate a virtual environment, then run:

```bash
pip install -r requirements-dev.txt
pip install -r grid_analysis/requirements.txt
pip install -r gridcare_lite/requirements.txt
pip install -r cliniccare_lite/requirements.txt
```

Copy the environment template:

```bash
cp .env.example .env
```

## Generate Grid Data

```bash
cd data/raw
python ../../scripts/generate_grid_data.py
cd ../..
```

Then run the Grid Analysis pipeline:

```bash
python grid_analysis/run_minimum_analysis.py
```

## Run Grid Analysis

```bash
python -m streamlit run grid_analysis/dashboard/app.py
```

## Run GridCare-Lite

```bash
python -m gridcare_lite.app.main
```

## Run ClinicCare-Lite

```bash
python cliniccare_lite/run.py
```

## Testing

Run the complete repository checks:

```bash
python -m ruff check .
python -m black --check .
python -m pytest -q
```

GitHub Actions runs the same checks automatically.

## Documentation

Important documentation includes:

- `grid_analysis/README.md`
- `docs/grid-analysis-data-quality-report.md`
- `docs/grid-analysis-data-dictionary.md`
- `docs/grid-analysis-findings.md`
- `docs/integration-report.md`
- `docs/deployment-guide.md`
- `docs/security-and-ethics.md`

## Important Limitations

Grid data is synthetic and must not be presented as official infrastructure data.

Grid Analysis uses graph-based educational reliability measures and does not
perform electrical power-flow or stability studies.

ClinicCare-Lite does not diagnose patients, interpret symptoms, recommend
treatment or replace professional clinical judgement.

## Project Status

- Grid Analysis: Complete
- GridCare-Lite: Complete
- ClinicCare-Lite: Complete
- Repository integration: Complete
- Automated repository tests: Passing
