# Overall Project Architecture

This diagram shows the high-level relationship between the three CS 112 project components. Grid Analysis and GridCare-Lite share the synthetic electricity-grid data domain. ClinicCare-Lite is intentionally separated because it has a different administrative purpose and privacy boundary.

```mermaid
flowchart LR
    GEN["Synthetic Grid Data Generator\nrandom.seed(42)"] --> DATA["utilities.csv\nsubstations.csv\nlines.csv"]

    DATA --> GA["Grid Analysis\nPandas / NetworkX / Streamlit"]
    GA --> OUT["Analysis Outputs\nEDA charts / network graph / map / metrics"]
    DATA --> GC["GridCare-Lite\nTkinter Desktop Application"]
    GA -. "grid asset context" .-> GC
    GC --> GCDB[("GridCare SQLite Database")]

    ENG[Engineer] --> GC
    ADM[Administrator] --> GC
    TECH[Technician] --> GC
    CSR[Customer Service] --> GC

    subgraph CLINIC["Separate Clinic Administration Boundary"]
        CC["ClinicCare-Lite\nFlask Web Application"] --> CCDB[("ClinicCare SQLite Database")]
        CLIN[Clinician] --> CC
        PAT[Patient] --> CC
        CC --> SAFE["Administrative / Non-diagnostic Scope"]
    end

    DATA -. "No clinic data integration" .-x CC
```

## Architectural Notes

- The synthetic grid generator is the source of the three electricity-grid CSV datasets.
- Grid Analysis performs validation, exploratory analysis, network analysis, reliability analysis and visualisation.
- GridCare-Lite uses grid asset information for outage and work-order management and stores application records in SQLite.
- ClinicCare-Lite uses Flask/SQLAlchemy with its own SQLite database for administrative clinic workflows.
- ClinicCare-Lite does not consume grid data and does not implement diagnosis, symptom interpretation, disease-risk scoring, prescribing or treatment recommendations.
