# Deployment Guide

## Deployment Approach

The project is designed for local coursework demonstration.

The three components remain independently runnable.

## Requirements

- Python 3.11
- Git
- Python virtual environment

## Installation

From the repository root:

```bash
python -m venv .venv
```

Activate the environment and install:

```bash
pip install -r requirements-dev.txt
pip install -r grid_analysis/requirements.txt
pip install -r gridcare_lite/requirements.txt
pip install -r cliniccare_lite/requirements.txt
```

Create the local environment file:

```bash
cp .env.example .env
```

Do not commit the `.env` file.

## Prepare Grid Data

```bash
cd data/raw
python ../../scripts/generate_grid_data.py
cd ../..
python grid_analysis/run_minimum_analysis.py
```

## Start Grid Analysis

```bash
python -m streamlit run grid_analysis/dashboard/app.py
```

## Start GridCare-Lite

```bash
python -m gridcare_lite.app.main
```

## Start ClinicCare-Lite

```bash
python cliniccare_lite/run.py
```

## Final Verification

Before demonstration or submission run:

```bash
python -m ruff check .
python -m black --check .
python -m pytest -q
```

All three applications should then be manually opened and their main workflows
checked before final submission.
