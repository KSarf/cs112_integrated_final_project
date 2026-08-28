# Integration Report

## Components

The final project contains three separately runnable components:

- Grid Analysis
- GridCare-Lite
- ClinicCare-Lite

## Grid Analysis and GridCare Integration

Grid Analysis cleans and validates the synthetic electricity-grid datasets.

GridCare-Lite checks for:

- `data/processed/substations_clean.csv`
- `data/processed/lines_clean.csv`

When those files exist, GridCare imports the cleaned datasets into its
SQLite database.

If the processed files do not exist, GridCare falls back to the original
synthetic datasets in `Datasets/`.

This allows GridCare outage and maintenance records to use valid grid assets
while still allowing the application to run independently.

## ClinicCare Integration Boundary

ClinicCare-Lite is part of the same repository and final project but remains
separate from the electricity-grid data.

No patient or clinic information is connected to Grid Analysis or GridCare.

## Validation

The integrated repository was checked using:

```bash
python -m ruff check .
python -m black --check .
python -m pytest -q
```

At integration time all checks passed and 14 automated tests passed.

## Integration Limitations

The three applications use different interfaces:

- Grid Analysis uses Streamlit.
- GridCare-Lite uses Tkinter.
- ClinicCare-Lite uses Flask.

They are therefore run as separate applications rather than being combined
into one large user interface.
