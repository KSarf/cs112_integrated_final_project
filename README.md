# CS 112 Final Project — Team 12

## National Electricity Grid Network Analysis, GridCare-Lite, and ClinicCare-Lite

This repository contains the three integrated components developed for the Ashesi University CS 112 Summer 2026 final project:

1. **National Electricity Grid Network Analysis**
2. **GridCare-Lite** — outage and maintenance management desktop application
3. **ClinicCare-Lite** — clinic administration and communication web application

## Team

**Team:** Team 12

> Before final submission, add every team member's full name and student ID here.

## Repository

GitHub repository: https://github.com/KSarf/cs112_integrated_final_project

**Submission note:** the repository must be made public before the final submission so the lecturer can access this link.

## Project Components

### 1. Grid Analysis

The Grid Analysis component uses synthetic electricity-grid datasets to study the structure of a national grid. It uses Python, pandas, NumPy, NetworkX, Matplotlib, Plotly, Folium, Streamlit, and Geopy.

The analysis includes:

- dataset loading, cleaning, and validation
- exploratory data analysis (EDA)
- integration of utilities, substations, and line datasets
- graph construction with NetworkX
- degree, betweenness, closeness, and related network measures
- simplified N-1 node and line contingency analysis
- geographic and network visualisations
- an interactive Streamlit dashboard

The electricity-grid data is **synthetic and illustrative** and must not be presented as official Ghanaian electricity-infrastructure data.

The dataset generator uses the required fixed seed:

```python
random.seed(42)
```

The seed has not been changed.

### 2. GridCare-Lite

GridCare-Lite is a Python/Tkinter desktop application backed by SQLite. It manages a simplified outage-to-resolution workflow.

Supported roles include:

- Administrator
- Engineer
- Technician
- Customer-service representative

Core functions include outage reporting, outage review, work-order creation, technician assignment, work progress updates, resolution notes, complaints, substations, and basic operational reports.

### 3. ClinicCare-Lite

ClinicCare-Lite is a Flask web application using SQLite and role-based access for clinicians and patients.

Core functions include registration and authentication, task assignment, patient file submission, clinician review, notifications, appointments, announcements, secure non-urgent messaging, and operational analytics.

**Important scope boundary:** ClinicCare-Lite is an administrative and communication system only. It does not diagnose patients, interpret symptoms, calculate disease risk, recommend treatment, prescribe medication, or replace professional clinical judgement. Its messaging system is not for emergencies.

## Integration

Grid Analysis produces cleaned grid data and analytical outputs.

GridCare-Lite uses the synthetic grid asset data to populate valid substations and transmission/distribution lines for outage-management workflows.

ClinicCare-Lite remains a separate application because clinic data and electricity-grid data have different purposes, privacy requirements, and security boundaries.

## Installation

### 1. Create a virtual environment

Windows PowerShell / Command Prompt:

```bash
python -m venv .venv
.venv\Scripts\activate
```

Git Bash:

```bash
python -m venv .venv
source .venv/Scripts/activate
```

macOS/Linux:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install runtime requirements

From the repository root:

```bash
python -m pip install -r requirements.txt
```

For development tools such as Ruff, Black, coverage, and pre-commit:

```bash
python -m pip install -r requirements-dev.txt
```

### 3. Environment configuration

Copy `.env.example` to `.env` if local environment settings are needed. Do not commit real secrets or credentials.

## Generate the Synthetic Grid Data

From the repository root:

```bash
cd data/raw
python ../../scripts/generate_grid_data.py
cd ../..
```

The generator produces:

- `utilities.csv`
- `substations.csv`
- `lines.csv`

A submission copy of these datasets is also kept in `Datasets/`.

## Run the Grid Analysis Pipeline

```bash
python grid_analysis/run_minimum_analysis.py
```

## Run the Grid Analysis Dashboard

```bash
python -m streamlit run grid_analysis/dashboard/app.py
```

## Run GridCare-Lite

```bash
python -m gridcare_lite.app.main
```

### GridCare-Lite Demo Accounts

| Role | Username | Password |
|---|---|---|
| Administrator | `admin1` | `Admin123!` |
| Engineer | `engineer1` | `Engineer123!` |
| Technician | `technician1` | `Technician123!` |
| Customer Service | `csr1` | `Customer123!` |

These accounts are for local demonstration/testing only. Passwords are stored as hashes rather than plain text in the application database.

## Run ClinicCare-Lite

```bash
python -m cliniccare_lite.run
```

### ClinicCare-Lite Demo Accounts

| Role | Username | Password |
|---|---|---|
| Clinician | `clinician1` | `Clinician123!` |
| Patient | `patient1` | `Patient123!` |

If the demo users have not yet been created, run:

```bash
python -m cliniccare_lite.seed_users
```

## Testing and Code Quality

Run the complete automated test suite:

```bash
python -m pytest -q
```

Run code-quality checks:

```bash
python -m ruff check .
python -m black --check .
```

GitHub Actions runs the configured automated checks on repository changes.

## Important Documentation

Key documentation is stored under `docs/` and includes:

- Grid Analysis data-quality report
- Grid Analysis data dictionary
- Grid Analysis findings and limitations
- GridCare data dictionary and ER diagram
- integration report
- deployment guide
- security and ethics documentation
- testing documentation
- team contribution evidence

Final submission reports, presentation slides, and demonstration videos should be included in the final submission package as required by the course instructions.

## Known Limitations

### Grid Analysis

- The grid datasets are synthetic rather than live operational data.
- Coordinates are illustrative rather than survey-grade.
- Centrality and N-1 fragmentation are structural graph measures, not electrical power-flow or stability studies.

### GridCare-Lite

- It is an educational desktop prototype rather than a production utility-management platform.
- SQLite is used for local storage.
- Operational reports are intentionally basic.

### ClinicCare-Lite

- It is an educational prototype rather than a production clinical system.
- SQLite is used for development/local demonstration.
- There is no production email/SMS service or emergency communication service.
- Messaging is basic and non-urgent rather than real-time clinical communication.
- No diagnostic or treatment-recommendation functionality is implemented.

## Security and Privacy

- Do not commit `.env` files, API keys, passwords, secret keys, private patient uploads, or other sensitive information.
- Demo data must remain fictional.
- ClinicCare-Lite applies role and ownership checks to protect user-specific records.
- GridCare-Lite stores passwords using bcrypt hashes and uses role-based permissions.

## Project Status

- Grid Analysis: complete
- GridCare-Lite: complete
- ClinicCare-Lite: complete
- Repository integration: complete
- Automated repository checks: passing on the latest integrated `main` build before final submission polish

## Final Submission Reminder

Before submission, confirm that:

- every team member's full name and student ID is added to the Team section above
- the repository is public
- the final reports are included
- presentation slides are included
- GridCare-Lite and ClinicCare-Lite demonstration videos are included
- no secrets, private uploads, virtual environments, caches, or development-only sensitive data are packaged
