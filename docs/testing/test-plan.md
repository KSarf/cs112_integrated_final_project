# CS 112 Final Project Test Plan

**Team:** Team 12  
**Final test cycle:** August 2026

## 1. Purpose

The purpose of this test plan is to verify that the integrated CS 112 project operates reliably, enforces its required role and privacy boundaries, and remains within the approved non-diagnostic scope for ClinicCare-Lite. The plan covers automated testing for Grid Analysis, GridCare-Lite, ClinicCare-Lite, and repository structure, with final manual release checks for the two user-facing applications.

## 2. Test Scope

### Grid Analysis

Testing covers dataset validation, minimum analysis outputs, and graph/network construction.

### GridCare-Lite

Testing covers database initialization, password hashing and verification, role permissions, outage creation, outage review, work-order assignment, technician ownership, resolution requirements, and the full outage-to-resolution workflow.

### ClinicCare-Lite

Testing covers application creation, authentication, protected routes, patient/clinician role behavior, ownership/privacy controls, file-upload validation, filename sanitization, and the required administrative/non-diagnostic boundary.

## 3. Test Environment

Automated tests are run locally with Pytest and in GitHub Actions. The final CI verification uses Python 3.11 on an Ubuntu GitHub-hosted runner and installs the repository's development and component requirements before running quality checks and tests.

## 4. Test Strategy

| Test type | Purpose | Evidence |
|---|---|---|
| Unit tests | Verify isolated helpers such as password hashing, permissions and upload validation | `gridcare_lite/tests`, `cliniccare_lite/tests` |
| Integration/workflow tests | Verify multi-step workflows using temporary test databases | `gridcare_lite/tests/test_workflow.py`, ClinicCare route/privacy tests |
| Data-analysis tests | Verify validation, minimum analytical workflow and network construction | `grid_analysis/tests` |
| Security/privacy tests | Verify authentication, ownership, access restrictions and safe filenames | ClinicCare privacy/auth/upload tests; GridCare permission/password tests |
| Scope tests | Confirm ClinicCare contains no diagnostic/treatment routes or medical scoring | `cliniccare_lite/tests/test_scope.py` |
| Code-quality checks | Detect import, formatting and static-quality problems before release | Ruff and Black in GitHub Actions |
| Manual release checks | Confirm final GUI/web workflows and README setup instructions | Final pre-submission walkthrough |

## 5. Automated Test Matrix

### GridCare-Lite

- database initialization creates required schema;
- stored password hash differs from plaintext and verifies correctly;
- wrong password fails verification;
- Administrator has management permission while Technician does not;
- complete outage workflow reaches resolved/completed states;
- invalid substation IDs are rejected;
- duplicate active outage reports are rejected;
- a technician cannot start another technician's work order;
- resolution notes are required before completing a work order.

### ClinicCare-Lite

- public routes load correctly;
- protected patient and clinician dashboards require login;
- patient login reaches the patient dashboard;
- clinician login reaches the clinician dashboard;
- wrong-password login is rejected;
- a patient sees only their own assigned tasks;
- a patient cannot submit to another patient's task;
- a clinician cannot review another clinician's submission;
- a clinician cannot download another clinician's submission;
- the administrative/non-diagnostic warning is visible;
- no diagnostic/treatment routes exist;
- operational analytics contain no medical risk or diagnostic scoring;
- upload-extension and filename-sanitization controls work correctly.

### Grid Analysis and Repository

- expected repository structure is present;
- minimum analysis workflow behaves as expected;
- data-validation functions reject invalid input and accept valid input;
- network construction produces the expected graph behavior.

## 6. Test Execution

From the repository root, the complete automated suite can be run with:

```bash
python -m pytest -q
```

Code-quality checks can be run with:

```bash
python -m ruff check .
python -m black --check .
```

GitHub Actions executes the configured checks on pushes and pull requests.

## 7. Pass/Fail Criteria

A test passes when the actual result matches the expected result without an unhandled exception. A release-blocking failure is any failure that prevents application startup, breaks a core workflow, bypasses role/privacy restrictions, permits ClinicCare diagnostic/treatment functionality, or causes the configured CI pipeline to fail.

## 8. Exit Criteria

The final release candidate is considered ready for packaging when:

- all configured automated tests pass;
- Ruff passes;
- Black formatting check passes;
- no unresolved high-severity defect remains;
- GridCare's complete outage-to-resolution workflow is manually demonstrated;
- ClinicCare's clinician-task → patient-upload → clinician-review → patient-outcome workflow is manually demonstrated;
- both applications start from a clean copy using the root README instructions;
- final submission files contain only synthetic/demo data and no secrets or private uploads.

## 9. Final Automated Outcome

The final integrated `main` build collected **30 automated tests and all 30 passed**. Ruff and Black also passed. Detailed results are recorded in `test-report.md`, while defects discovered and corrected during development are recorded in `defect-log.md`.
