# National Electricity Grid Network Analysis, GridCare-Lite, and ClinicCare-Lite

## Course
- **Course:** CS 112 Computer Programming for CS
- **Semester:** Summer 2026

## Project Overview
This repository is the initial scaffold for a multi-component final course project containing:
1. National Electricity Grid Network Analysis
2. GridCare-Lite (desktop outage and maintenance management)
3. ClinicCare-Lite (web-based clinic administration and communication)

> ⚠️ **Grid data warning:** Electricity-grid datasets in this repository are synthetic and must not be presented as official Ghanaian electricity infrastructure data.

> ⚠️ **ClinicCare-Lite scope:** ClinicCare-Lite does not diagnose patients, interpret symptoms, recommend treatment, or replace professional clinical judgement.

## Components
- **grid_analysis/**: starter data pipeline, graph analysis modules, and Streamlit dashboard skeleton.
- **gridcare_lite/**: starter Tkinter desktop prototype with SQLite foundation and role/permission helpers.
- **cliniccare_lite/**: Flask application-factory starter with authentication, messaging, uploads, and dashboards.

## Repository Structure Summary
- `.github/` workflows and templates
- `data/` raw and processed synthetic datasets
- `grid_analysis/`, `gridcare_lite/`, `cliniccare_lite/` component directories
- `common/` shared constants/logging utilities
- `docs/` architecture, process, testing, ethics, and planning templates
- `scripts/` bootstrap and local quality-check scripts
- `tests/` repository-level checks

## Technology Stack
- **Grid Analysis:** Python, pandas, NumPy, NetworkX, matplotlib, plotly, folium, streamlit, geopy
- **GridCare-Lite:** Python, Tkinter, SQLite, bcrypt, pytest
- **ClinicCare-Lite:** Flask, HTML/CSS/JavaScript/Bootstrap, SQLite, Flask-SQLAlchemy, Flask-Login, Flask-WTF, bcrypt, pytest

## Local Installation
### 1) Create a virtual environment
**Windows (PowerShell)**
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS/Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -r requirements-dev.txt
pip install -r grid_analysis/requirements.txt
pip install -r gridcare_lite/requirements.txt
pip install -r cliniccare_lite/requirements.txt
```

## Running Components
### Grid Analysis (Streamlit)
```bash
streamlit run grid_analysis/dashboard/app.py
```

### GridCare-Lite (Tkinter prototype)
```bash
python -m gridcare_lite.app.main
```

### ClinicCare-Lite (Flask app)
```bash
python cliniccare_lite/run.py
```

## Testing and Linting
```bash
python scripts/run_checks.py
# or separately
ruff check .
black --check .
pytest
```

## Git Workflow Summary
- Work from short-lived feature branches.
- Open pull requests for review.
- Link issues in PRs.
- Use focused commits and run checks before review.

## Contribution Evidence Expectations
Each contribution should include issue linkage, branch name, tests/checks executed, and concise work notes in pull request discussions and logs.

## Team Placeholder
| Member | Primary Role | Secondary Responsibility |
|--------|--------------|--------------------------|
| To be decided | To be decided | To be decided |
| To be decided | To be decided | To be decided |
| To be decided | To be decided | To be decided |
| To be decided | To be decided | To be decided |

## Current Status
This repository currently contains the **initial scaffold only**. Core application features are intentionally marked with TODO notes.

## Roadmap
- **Week 1:** Repository setup and environment alignment (placeholder)
- **Week 2:** Data model and core workflow planning (placeholder)
- **Week 3:** Component-level MVP implementation (placeholder)
- **Week 4:** Integration, testing, and review (placeholder)
- **Week 5:** Final hardening, documentation, and presentation prep (placeholder)

## Known Limitations
- No production-ready authentication flow yet.
- No finalized real-world deployment architecture.
- Analytics and operational workflows are scaffolds only.

## Documentation Links
- `docs/project-plan.md`
- `docs/git-workflow.md`
- `docs/security-and-ethics.md`
- `docs/testing/test-plan.md`
- `docs/documentation-checklist.md`
