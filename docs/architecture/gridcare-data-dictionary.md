# GridCare-Lite Data Dictionary

This document describes the main SQLite database tables used by GridCare-Lite.

## users

Stores GridCare user accounts and their roles.

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| username | TEXT | Unique login username |
| password_hash | TEXT | Hashed user password |
| role | TEXT | Administrator, Engineer, Technician, or Customer-service representative |
| full_name | TEXT | User's full name |
| email | TEXT | User's email address |

## substations

Stores electrical substation information imported from the grid dataset.

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| name | TEXT | Substation name |
| short_name | TEXT | Short substation name |
| region | TEXT | Region where the substation is located |
| country | TEXT | Country |
| latitude | REAL | Latitude |
| longitude | REAL | Longitude |
| voltage_kv | REAL | Voltage rating |
| capacity_mva | REAL | Capacity rating |
| commissioning_year | INTEGER | Year commissioned |
| type | TEXT | Substation type |
| status | TEXT | Current substation status |

## lines

Stores transmission lines connecting substations.

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| utility_id | INTEGER | Utility-related identifier |
| source_substation_id | INTEGER | Foreign key to source substation |
| destination_substation_id | INTEGER | Foreign key to destination substation |
| voltage_kv | REAL | Line voltage |
| length_km | REAL | Line length |
| capacity_mva | REAL | Line capacity |
| status | TEXT | Current line status |
| line_type | TEXT | Transmission line type |

## outages

Stores reported power outages.

| Field | Type | Description |
|---|---|---|
| id | INTEGER | Primary key |
| title | TEXT | Short outage title |
| description | TEXT | Detailed outage description |
| substation_id | INTEGER | Foreign key to affected substation |
| severity | TEXT | Low, Medium, High, or Critical |
| status | TEXT | Current outage workflow status |
| reported_by | INTEGER | Foreign key to reporting user |
| reported_at | TEXT | Date and time outage was reported |
| resolved_at | TEXT | Date and time outage was resolved |

### Outage Status Flow

```text
Reported
   ↓
Under Review
   ↓
Assigned
   ↓
In Progress
   ↓
Resolved