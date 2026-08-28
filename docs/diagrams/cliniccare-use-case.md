# ClinicCare-Lite Use-Case Diagram

ClinicCare-Lite supports administrative and communication workflows for two roles: Clinician and Patient. The application is intentionally non-diagnostic.

```mermaid
flowchart LR
    CLIN[Clinician]
    PAT[Patient]

    subgraph APP[ClinicCare-Lite]
        REGISTER((Register / Login / Logout))
        DASH((View Role Dashboard))
        TASK((Create and Assign Task))
        VIEWTASK((View Assigned Tasks))
        UPLOAD((Upload Allowed File))
        REVIEW((Review Submission))
        OUTCOME((Record Review Notes / Outcome / Resubmission))
        MSG((Send / Receive Non-urgent Messages))
        APPT((Schedule / View Appointments))
        ANN((Create / View Announcements))
        NOTIFY((View Notifications / Reminders))
        ANALYTICS((View Operational Analytics))
    end

    CLIN --> REGISTER
    PAT --> REGISTER
    CLIN --> DASH
    PAT --> DASH

    CLIN --> TASK
    PAT --> VIEWTASK
    PAT --> UPLOAD
    CLIN --> REVIEW
    CLIN --> OUTCOME

    CLIN --> MSG
    PAT --> MSG

    CLIN --> APPT
    PAT --> APPT

    CLIN --> ANN
    PAT --> ANN

    CLIN --> NOTIFY
    PAT --> NOTIFY

    CLIN --> ANALYTICS
```

## Scope Boundary

```mermaid
flowchart LR
    ALLOWED["Allowed\nAdministrative tasks\nFile submission/review\nMessaging\nAppointments\nAnnouncements\nOperational analytics"]
    SYSTEM[ClinicCare-Lite]
    PROHIBITED["Excluded from scope\nDiagnosis\nSymptom interpretation\nDisease-risk scoring\nTreatment recommendations\nPrescribing\nEmergency care"]

    ALLOWED --> SYSTEM
    SYSTEM -. "not implemented" .-> PROHIBITED
```
