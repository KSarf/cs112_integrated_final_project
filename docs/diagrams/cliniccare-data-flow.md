# ClinicCare-Lite Data-Flow Diagram

This diagram shows the main administrative task/submission/review flow and the supporting communication features.

```mermaid
flowchart TD
    C[Clinician] --> LOGIN[Authenticate]
    P[Patient] --> LOGIN
    LOGIN --> AUTH[Role-based access]

    C --> CT[Create administrative task]
    CT --> DB[(ClinicCare SQLite Database)]
    DB --> PD[Patient dashboard]
    P --> PD

    PD --> UP[Select file for assigned task]
    UP --> VAL[Validate extension and sanitize filename]
    VAL -->|Valid| SUB[Create submission record and save file]
    VAL -->|Invalid| REJECT[Reject upload]
    SUB --> DB

    DB --> CD[Clinician dashboard]
    C --> CD
    CD --> REV[Open assigned submission]
    REV --> REVIEW[Record review notes / outcome / resubmission request]
    REVIEW --> DB
    REVIEW --> NOTE[Create patient notification]
    NOTE --> DB
    DB --> PD

    C --> MSG[Non-urgent messaging]
    P --> MSG
    MSG --> DB

    C --> APPT[Appointment scheduling]
    APPT --> DB
    DB --> PD

    C --> ANN[Publish announcement]
    ANN --> DB
    DB --> PD

    C --> OPS[Operational analytics]
    DB --> OPS
```

## Data-Handling Notes

- Role and ownership checks protect patient-specific tasks and submissions.
- Upload validation restricts file extensions and sanitizes filenames before storage.
- Review outcomes and notifications remain administrative; the application does not generate diagnoses or treatment recommendations.
- Messaging is intended for non-urgent communication and not emergencies.
