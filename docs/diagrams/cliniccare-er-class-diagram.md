# ClinicCare-Lite ER / Class Diagram

This diagram represents the main persistent models in the completed ClinicCare-Lite application and the principal relationships between users, tasks, submissions, communication, appointments, notifications and announcements.

```mermaid
erDiagram
    USER {
        INTEGER id PK
        STRING username
        STRING full_name
        STRING email
        STRING password_hash
        STRING role
    }

    TASK {
        INTEGER id PK
        STRING title
        TEXT instructions
        DATE due_date
        STRING status
        INTEGER patient_id FK
        INTEGER clinician_id FK
    }

    SUBMISSION {
        INTEGER id PK
        INTEGER task_id FK
        INTEGER patient_id FK
        STRING file_name
        STRING status
        DATETIME submitted_at
        TEXT review_notes
        INTEGER reviewer_id FK
        DATETIME reviewed_at
    }

    MESSAGE {
        INTEGER id PK
        INTEGER sender_id FK
        INTEGER receiver_id FK
        TEXT body
        DATETIME created_at
        BOOLEAN is_read
    }

    APPOINTMENT {
        INTEGER id PK
        INTEGER patient_id FK
        INTEGER clinician_id FK
        STRING summary
        DATETIME appointment_time
        STRING status
    }

    NOTIFICATION {
        INTEGER id PK
        INTEGER user_id FK
        STRING message
        BOOLEAN is_read
        DATETIME created_at
    }

    ANNOUNCEMENT {
        INTEGER id PK
        STRING title
        TEXT body
        STRING priority
        DATETIME published_at
        DATETIME expires_at
        INTEGER clinician_id FK
    }

    USER ||--o{ TASK : "patient receives"
    USER ||--o{ TASK : "clinician creates"
    TASK ||--o{ SUBMISSION : "has"
    USER ||--o{ SUBMISSION : "patient uploads"
    USER ||--o{ SUBMISSION : "clinician reviews"
    USER ||--o{ MESSAGE : "sends"
    USER ||--o{ MESSAGE : "receives"
    USER ||--o{ APPOINTMENT : "patient attends"
    USER ||--o{ APPOINTMENT : "clinician schedules"
    USER ||--o{ NOTIFICATION : "receives"
    USER ||--o{ ANNOUNCEMENT : "clinician publishes"
```

## Model Responsibilities

- **User** stores account identity, role and password hash information.
- **Task** links a clinician and patient to an administrative request with instructions, due date and status.
- **Submission** records the patient's uploaded file and the clinician's review status/notes.
- **Message** supports basic non-urgent clinician/patient communication.
- **Appointment** stores scheduling information between a patient and clinician.
- **Notification** stores user-facing application alerts.
- **Announcement** stores clinic-wide administrative notices created by clinicians.
