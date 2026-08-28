 GridCare-Lite

GridCare-Lite is a beginner-friendly desktop application for managing electrical grid outages, maintenance work orders, customer complaints, and basic operational reports.

The application is built with Python, Tkinter, SQLite, and bcrypt.

## Main Features

GridCare-Lite supports four user roles:

- Administrator
- Engineer
- Technician
- Customer-service representative

The application provides role-based access so each user only sees the actions needed for their role.

### Engineer

An Engineer can:

- View the dashboard.
- View substations.
- View outages.
- Report a new outage.
- Select a valid substation when reporting an outage.
- Set outage severity as Low, Medium, High, or Critical.

New outages begin with the status:

```text
Reported
Administrator

An Administrator can:

View the dashboard.
View substations.
View outages.
Review reported outages.
Create work orders for reviewed outages.
Assign work orders to technicians.
View work orders.
View operational reports.

When an Administrator reviews an outage, its status changes from:

Reported
   ↓
Under Review

When a work order is created, the outage becomes:

Assigned
Technician

A Technician can:

View the dashboard.
View only work orders assigned to that technician.
Start assigned work.
Complete work.
Enter resolution notes.

The technician workflow is:

Assigned
   ↓
In Progress
   ↓
Completed

When the technician completes the work order, the related outage becomes:

Resolved

Resolution notes and maintenance activity are stored in the database.

Customer-service Representative

A Customer-service representative can:

View the dashboard.
View outages.
Log customer complaints.
Link a complaint to an existing outage.

If an outage ID is entered, GridCare-Lite verifies that the outage exists before saving the complaint.

Complete Outage Workflow

The main GridCare-Lite workflow is:

Engineer
Creates outage
     ↓
Reported

Administrator
Reviews outage
     ↓
Under Review

Administrator
Creates work order
and assigns technician
     ↓
Assigned

Technician
Starts work
     ↓
In Progress

Technician
Completes work and
records resolution notes
     ↓
Completed Work Order
     ↓
Resolved Outage
Operational Reports

Administrators can open the Reports page.

The current reports include:

Number of open outages.
Average outage resolution time.
Number of outages by region.

The report values are calculated from the SQLite database.

Grid Data

GridCare-Lite uses the synthetic grid datasets stored in the repository's Datasets directory.

The database can be populated with:

Substations
Transmission lines

The current dataset contains 44 substations and 55 transmission lines.

Requirements

The GridCare-Lite requirements are stored in:

gridcare_lite/requirements.txt

The main Python dependencies are:

bcrypt
pytest

Tkinter is part of the standard Python installation on most systems.

Installation

Run the following commands from the root of the repository.

1. Create a virtual environment

Windows:

python -m venv .venv
.venv\Scripts\activate

Git Bash:

python -m venv .venv
source .venv/Scripts/activate

macOS/Linux:

python -m venv .venv
source .venv/bin/activate
2. Install GridCare-Lite requirements
python -m pip install -r gridcare_lite/requirements.txt
Database Setup

GridCare-Lite uses SQLite.

The database is created automatically when the application starts.

The default database location is:

gridcare_lite/database/gridcare.db
Load the grid dataset

From the repository root, run:

python -c "from gridcare_lite.app.config import load_config; from gridcare_lite.app.database.seed import seed_demo_data; seed_demo_data(load_config().database_path); print('Grid data loaded.')"

You can check that the data loaded with:

python -c "import sqlite3; c=sqlite3.connect('gridcare_lite/database/gridcare.db'); print('substations:', c.execute('SELECT COUNT(*) FROM substations').fetchone()[0]); print('lines:', c.execute('SELECT COUNT(*) FROM lines').fetchone()[0])"
Create Demo Users

A fresh GridCare-Lite database does not contain user accounts.

For demonstration and testing, four local accounts can be created with the following command:

python - <<'PY'
import sqlite3
from gridcare_lite.app.security.passwords import hash_password

users = [
    ("admin1", "Admin123!", "Administrator"),
    ("engineer1", "Engineer123!", "Engineer"),
    ("technician1", "Technician123!", "Technician"),
    ("csr1", "Customer123!", "Customer-service representative"),
]

with sqlite3.connect("gridcare_lite/database/gridcare.db") as connection:
    for username, password, role in users:
        connection.execute(
            """
            INSERT OR IGNORE INTO users (
                username,
                password_hash,
                role
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                hash_password(password),
                role,
            ),
        )

    connection.commit()

print("Demo users created.")
PY

The demo login accounts are:

Role	                        Username	        Password
Administrator	                admin1	            Admin123!
Engineer	                    engineer1	        Engineer123!
Technician	                    technician1	        Technician123!
Customer Service	            csr1	            Customer123!

These accounts are intended only for local demonstration and testing.

Passwords are stored as password hashes rather than plain-text passwords.

Running GridCare-Lite

From the repository root, run:

python -m gridcare_lite.app.main

The login screen should open.

Suggested Demonstration

To demonstrate the complete workflow:

Step 1 - Engineer

Login with the Engineer account.

Open:

Outages

Select:

Log Outage

Enter:

Outage title
Valid substation
Severity
Description

Save the outage.

The outage should show:

Reported
Step 2 - Administrator

Logout and login as the Administrator.

Open:

Outages

Select the reported outage and choose:

Review Selected

The outage should become:

Under Review

Next open:

Work Orders

Choose:

Create Work Order

Select:

The reviewed outage
A technician
Scheduled date
Instructions

Create the work order.

Step 3 - Technician

Logout and login as the assigned Technician.

Open:

Work Orders

The technician should only see work assigned to that account.

Select the work order and choose:

Start Selected

The status becomes:

In Progress

When the maintenance work is finished, select:

Complete Selected

Enter resolution notes.

The work order becomes:

Completed

The related outage becomes:

Resolved
Step 4 - Customer Service

Logout and login as the Customer-service representative.

Open:

Complaints

Enter:

Customer name
Complaint details
A valid outage ID

Save the complaint.

The complaint should appear in the complaints table.

An invalid outage ID should be rejected.

Step 5 - Reports

Login as the Administrator.

Open:

Reports

Verify that the application displays:

Open outages
Average resolution time
Outages by region
Testing

GridCare-Lite uses pytest.

Run the GridCare tests with:

python -m pytest gridcare_lite/tests -q

The test suite includes checks for:

Database creation
Password hashing
Role permissions
Outage creation
Invalid substation rejection
Duplicate active outage rejection
Complete outage-to-resolution workflow
Technician work-order ownership
Required resolution notes
Code Quality Checks

Run Ruff:

python -m ruff check gridcare_lite

Run Black:

python -m black --check gridcare_lite

To automatically format GridCare-Lite with Black:

python -m black gridcare_lite
Database Documentation

GridCare-Lite database documentation is available in:

docs/architecture/gridcare-data-dictionary.md

The GridCare-Lite ER diagram is available in:

docs/diagrams/gridcare-er-diagram.md

The main database tables are:

users
substations
lines
outages
work_orders
complaints
status_history
maintenance_activities
Security and Validation

GridCare-Lite includes the following basic protections:

Passwords are hashed with bcrypt.
User permissions are based on roles.
Invalid substations are rejected when reporting outages.
Duplicate matching active outages are rejected.
Only reviewed outages can receive new work orders.
Work orders must be assigned to Technician users.
Technicians cannot update work assigned to another technician.
Work must be started before it can be completed.
Resolution notes are required before completion.
Complaints linked to outages require a valid outage ID.