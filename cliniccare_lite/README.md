# ClinicCare-Lite

ClinicCare-Lite is a Flask-based clinic administration and communication application developed for the CS 112 Final Course Project.

The system supports administrative interaction between clinicians and patients while protecting patient privacy and maintaining a strict non-diagnostic boundary.

---

## Important Scope Boundary

ClinicCare-Lite is an administrative and communication system only.

It must not:

- Diagnose patients
- Interpret symptoms
- Calculate disease or health risk
- Recommend treatment
- Prescribe medication
- Assign automated health scores
- Replace professional clinical judgement

The messaging system is intended for non-urgent communication only.

ClinicCare-Lite must not be used for medical emergencies.

---

# Main Users

ClinicCare-Lite supports two user roles:

- Clinician
- Patient

Each role has different permissions and workflows.

---

# Clinician Features

A clinician can:

- Register and log in
- Access the clinician dashboard
- Create administrative tasks
- Assign tasks to patients
- Add task instructions
- Set task due dates
- View patient submissions
- Download submitted files
- Review submissions
- Add review notes
- Select a review outcome
- Request resubmission
- Send messages
- Receive notifications
- Schedule appointments
- Send appointment reminders
- Publish clinic announcements
- Mark announcements as Routine or Urgent
- Set announcement expiry dates
- View operational analytics

---

# Patient Features

A patient can:

- Register and log in
- Access the patient dashboard
- View assigned tasks
- Read task instructions
- View task due dates
- Upload approved files
- View submission status
- View submission history
- Read clinician review notes
- Receive notifications
- Send and receive messages
- View message read/unread status
- View appointments
- Receive appointment reminders
- View active clinic announcements
- View private administrative activity information

---

# Registration Rules

ClinicCare-Lite uses role-specific User IDs.

## Clinician ID

A clinician ID must:

- Contain exactly 8 digits
- End in `0000`

Example:

```text
12340000
```

## Patient ID

A patient ID must:

- Contain exactly 8 digits
- End in a registration year from 2022 to 2028

Example:

```text
12342026
```

---

# Password Rules

Passwords must:

- Be at least 8 characters long
- Contain an uppercase letter
- Contain a lowercase letter
- Contain a number
- Contain a special character

Example format:

```text
Patient123!
```

Passwords are not stored as plain text.

ClinicCare-Lite uses bcrypt password hashing.

---

# Technologies Used

ClinicCare-Lite uses:

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- Flask-Bcrypt
- SQLite
- HTML
- CSS
- Bootstrap
- Pytest

---

# Project Structure

```text
cliniccare_lite/
│
├── app/
│   ├── analytics/
│   ├── auth/
│   ├── clinician/
│   ├── messaging/
│   ├── models/
│   ├── patient/
│   ├── static/
│   ├── templates/
│   └── uploads/
│
├── tests/
├── README.md
├── requirements.txt
├── reset_db.py
├── run.py
└── seed_users.py
```

## Important Folders

### `app/auth/`

Contains:

- Registration
- Login
- Logout
- Registration validation

### `app/clinician/`

Contains clinician workflows such as:

- Task creation
- Submission review
- Appointment scheduling
- Appointment reminders
- Announcement publishing

### `app/patient/`

Contains patient workflows such as:

- Patient dashboard
- Task viewing
- File submission
- Submission history
- Appointment viewing
- Announcement viewing

### `app/messaging/`

Contains:

- Sending messages
- Inbox
- Notifications
- Read/unread message handling

### `app/models/`

Contains the database models.

Main models include:

- User
- Task
- Submission
- Message
- Notification
- Appointment
- Announcement

### `app/analytics/`

Contains non-diagnostic operational analytics for clinicians.

### `app/uploads/`

Contains file validation helpers.

### `app/templates/`

Contains the HTML pages displayed by Flask.

### `tests/`

Contains automated Pytest tests for the ClinicCare application.

---

# Installation

Open a terminal in the root folder of the repository.

Install the development requirements:

```bash
pip install -r requirements-dev.txt
```

Then install the ClinicCare requirements:

```bash
pip install -r cliniccare_lite/requirements.txt
```

---

# Database Setup

ClinicCare-Lite uses SQLite for development.

To recreate the development database:

```bash
python -m cliniccare_lite.reset_db
```

WARNING:

This command deletes the existing development database tables and recreates them.

Only use this command when resetting the development environment.

---

# Demo Users

Demo users can be created by running:

```bash
python -m cliniccare_lite.seed_users
```

The current development demo accounts are:

## Demo Patient

```text
Username: patient1
Password: Patient123!
```

## Demo Clinician

```text
Username: clinician1
Password: Clinician123!
```

These seeded accounts are development/demo accounts.

New users registering through the public registration form must follow the 8-digit User ID rules.

---

# Running ClinicCare-Lite

From the repository root run:

```bash
python -m cliniccare_lite.run
```

For Flask debug mode in Git Bash:

```bash
FLASK_DEBUG=true python -m cliniccare_lite.run
```

Flask will display the local application address in the terminal.

Open that address in a web browser.

---

# Main Demonstration Workflow

A complete ClinicCare demonstration can follow this workflow.

## Step 1 - Clinician Login

Log in using the demo clinician account:

```text
clinician1
Clinician123!
```

The clinician dashboard will open.

---

## Step 2 - Create a Task

Select:

```text
Create Task
```

Choose the patient and enter:

- Task title
- Instructions
- Due date

Example:

```text
Patient: patient1
Title: Administrative Document Upload
Instructions: Please upload the requested document.
Due Date: Select a future date
```

Submit the task.

The patient receives a notification.

---

## Step 3 - Patient Login

Log out from the clinician account.

Log in using:

```text
patient1
Patient123!
```

The assigned task should appear on the patient dashboard.

The patient can see:

- Task title
- Instructions
- Due date
- Current status

---

# File Submission

Patients can submit approved files for their own open tasks.

Approved file types are:

```text
.txt
.csv
.pdf
```

ClinicCare validates:

- File extension
- File name
- File size
- Patient ownership
- Task ownership
- Whether the task is open
- Whether another normal submission should be allowed

Uploaded files are systematically renamed to reduce filename collisions.

The default maximum upload size is 10 MB.

After upload:

```text
Task Status = Submitted
```

The clinician receives a notification.

---

# Clinician Review

The clinician can open a submitted file and:

- Download the file
- Select a review result
- Write review notes
- Save the review

Possible review outcomes include:

- Reviewed
- Needs Follow-up
- Needs Resubmission
- Escalated

These are administrative categories selected by the clinician.

They are not diagnoses generated by ClinicCare-Lite.

The system records:

- Review status
- Review notes
- Reviewer
- Review time

The patient receives a notification when the review is saved.

---

# Patient Feedback

After review, the patient can see:

- Review status
- Clinician notes
- Review date
- Submission history

If the result is:

```text
Needs Resubmission
```

the task becomes available for another submission.

---

# Messaging

Patients and clinicians can send non-urgent messages.

The messaging section supports:

- Received messages
- Sent messages
- Message timestamps
- Read/unread status
- Notifications
- Sender and receiver information

Messages must not be used for emergencies.

---

# Notifications

Notifications are generated for events including:

- New task assignment
- New patient submission
- Submission review
- New message
- Appointment scheduling
- Appointment reminder
- Clinic announcement

Notifications can be marked as read.

---

# Appointments

Clinicians can schedule appointments for patients.

An appointment includes:

- Patient
- Appointment purpose
- Date and time
- Status

Patients can view their scheduled appointments.

Clinicians can also send appointment reminders.

---

# Clinic Announcements

Clinicians can publish clinic-wide administrative announcements.

Announcements include:

- Title
- Message
- Priority
- Publication time
- Optional expiry time

Priority options include:

```text
Routine
Urgent
```

Active announcements appear on the patient dashboard.

Expired announcements are not displayed to patients.

Announcements are administrative notices and must not provide diagnoses or treatment instructions.

---

# Operational Analytics

The clinician dashboard contains non-diagnostic operational statistics.

Examples include:

- Total tasks
- Pending tasks
- Submitted tasks
- Reviewed tasks
- Tasks needing resubmission
- Overdue tasks
- Total submissions
- Pending reviews
- Total appointments
- Total announcements

These metrics describe workflow activity only.

They do not calculate:

- Disease risk
- Diagnosis
- Symptom severity
- Medical scores
- Treatment recommendations

---

# Privacy and Access Control

ClinicCare-Lite uses login and role checks to protect user data.

Important privacy rules include:

- Patients can only see their own tasks
- Patients cannot submit to another patient's task
- Clinicians can only review submissions assigned to them
- Clinicians can only download submissions associated with their tasks
- Notifications are user-specific
- Patient history is private
- Protected pages require login

---

# Testing

Run the ClinicCare automated tests with:

```bash
pytest cliniccare_lite/tests -q
```

The ClinicCare test suite covers areas including:

- Application creation
- Authentication
- Correct role redirection
- Wrong password handling
- Protected routes
- File extension validation
- Filename sanitization
- Patient ownership
- Clinician ownership
- Privacy protection
- Non-diagnostic scope

Run ClinicCare lint checks with:

```bash
ruff check cliniccare_lite
```

Formatting can be checked with:

```bash
black --check cliniccare_lite
```

---

# Non-Diagnostic Safety Boundary

ClinicCare-Lite intentionally does not contain functions for:

- Diagnosing medical conditions
- Interpreting symptoms
- Calculating disease probability
- Assigning health-risk scores
- Recommending medication
- Recommending treatment
- Replacing clinical judgement

Automated processing must remain administrative.

For example, the system may determine whether:

- A file extension is allowed
- A required field is present
- A task belongs to the logged-in patient
- A submission has already been reviewed

It must not determine what a patient's medical information means.

---

# Known Limitations

ClinicCare-Lite is an educational prototype.

Current limitations include:

- SQLite development database
- No production deployment
- No real emergency communication system
- No production SMTP email service
- Basic operational analytics
- Basic text-based messaging rather than real-time chat
- No full electronic medical record system
- No automated medical interpretation

These limitations are intentionally documented rather than hidden.

---

# Development Notes

Generated development databases, private uploaded files, environment files, cache files and temporary files should not be committed to GitHub.

When changing a database model during development, the development database may need to be reset and reseeded.

For normal HTML, CSS, route or test changes, a database reset is usually not required.

---

# Final ClinicCare Checklist

Before submission confirm that:

- Registration works
- Password hashing works
- Patient and clinician roles work
- Protected routes work
- Tasks can be assigned
- Due dates appear
- Files can be submitted
- Invalid files are rejected
- Ownership is protected
- Clinicians can review submissions
- Patients can see feedback
- Notifications work
- Messaging works
- Read/unread status works
- Appointments and reminders work
- Announcements work
- Operational analytics work
- Privacy tests pass
- Non-diagnostic scope tests pass
- User guide is current
- ClinicCare automated tests pass

---

# CS 112 Final Project

ClinicCare-Lite is one component of the CS 112 Integrated Final Project.

The complete repository also contains:

- National Electricity Grid Network Analysis
- GridCare-Lite
- ClinicCare-Lite

The components share repository and testing standards while remaining separate applications with different responsibilities and security requirements.