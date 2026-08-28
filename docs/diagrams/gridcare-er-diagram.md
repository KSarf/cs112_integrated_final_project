# GridCare-Lite ER Diagram

This diagram shows the main database entities and relationships used by GridCare-Lite.

```mermaid
erDiagram

    USERS {
        INTEGER id PK
        TEXT username
        TEXT password_hash
        TEXT role
        TEXT full_name
        TEXT email
    }

    SUBSTATIONS {
        INTEGER id PK
        TEXT name
        TEXT short_name
        TEXT region
        TEXT country
        REAL latitude
        REAL longitude
        REAL voltage_kv
        REAL capacity_mva
        INTEGER commissioning_year
        TEXT type
        TEXT status
    }

    LINES {
        INTEGER id PK
        INTEGER utility_id
        INTEGER source_substation_id FK
        INTEGER destination_substation_id FK
        REAL voltage_kv
        REAL length_km
        REAL capacity_mva
        TEXT status
        TEXT line_type
    }

    OUTAGES {
        INTEGER id PK
        TEXT title
        TEXT description
        INTEGER substation_id FK
        TEXT severity
        TEXT status
        INTEGER reported_by FK
        TEXT reported_at
        TEXT resolved_at
    }

    WORK_ORDERS {
        INTEGER id PK
        INTEGER outage_id FK
        INTEGER assigned_to FK
        TEXT scheduled_date
        TEXT status
        TEXT instructions
        TEXT resolution_notes
        TEXT completed_at
    }

    COMPLAINTS {
        INTEGER id PK
        TEXT customer_name
        TEXT details
        INTEGER outage_id FK
        TEXT status
        TEXT created_at
    }

    STATUS_HISTORY {
        INTEGER id PK
        INTEGER outage_id FK
        INTEGER work_order_id FK
        TEXT old_status
        TEXT new_status
        INTEGER changed_by FK
        TEXT changed_at
    }

    MAINTENANCE_ACTIVITIES {
        INTEGER id PK
        INTEGER work_order_id FK
        INTEGER technician_id FK
        TEXT activity_description
        TEXT activity_date
    }

    USERS ||--o{ OUTAGES : reports
    USERS ||--o{ WORK_ORDERS : assigned_to
    USERS ||--o{ STATUS_HISTORY : changes
    USERS ||--o{ MAINTENANCE_ACTIVITIES : performs

    SUBSTATIONS ||--o{ OUTAGES : has
    SUBSTATIONS ||--o{ LINES : source
    SUBSTATIONS ||--o{ LINES : destination

    OUTAGES ||--o{ WORK_ORDERS : generates
    OUTAGES ||--o{ COMPLAINTS : linked_to
    OUTAGES ||--o{ STATUS_HISTORY : records

    WORK_ORDERS ||--o{ STATUS_HISTORY : records
    WORK_ORDERS ||--o{ MAINTENANCE_ACTIVITIES : contains