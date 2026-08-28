# CS 112 Final Project Test Report

**Team:** Team 12  
**Date:** 28 August 2026  
**Applications covered:** GridCare-Lite and ClinicCare-Lite  
**Additional automated coverage:** Grid Analysis and repository structure

## 1. Purpose

This report records the final verification evidence for the integrated CS 112 project. It summarizes automated tests, security/privacy checks, workflow tests, code-quality checks, and the final GitHub Actions result.

## 2. Final Automated Result

The final integrated `main` build collected **30 tests and all 30 passed**. GitHub Actions also passed Ruff and Black checks. The successful CI run was executed on Python 3.11.16.

| Area | Automated tests | Result |
|---|---:|---|
| Repository structure | 1 | PASS |
| Grid Analysis minimum workflow | 4 | PASS |
| Grid Analysis data validation | 2 | PASS |
| Grid Analysis network builder | 1 | PASS |
| GridCare database | 1 | PASS |
| GridCare password security | 1 | PASS |
| GridCare permissions | 1 | PASS |
| GridCare outage/work-order workflow | 5 | PASS |
| ClinicCare app factory | 1 | PASS |
| ClinicCare authentication | 5 | PASS |
| ClinicCare privacy/ownership | 4 | PASS |
| ClinicCare non-diagnostic scope | 3 | PASS |
| ClinicCare upload validation | 1 | PASS |
| **Total** | **30** | **30 PASS** |

## 3. GridCare-Lite Test Results

| ID | Test objective and input | Expected outcome | Actual outcome | Result |
|---|---|---|---|---|
| GC-01 | Initialize a temporary GridCare SQLite database | Required tables are created | `users` table created successfully | PASS |
| GC-02 | Hash a sample password and verify correct/wrong passwords | Plain password is not stored; correct password verifies; wrong password fails | All assertions passed | PASS |
| GC-03 | Check Administrator and Technician permissions for `manage_users` | Administrator allowed; Technician denied | Permission rules enforced | PASS |
| GC-04 | Complete outage workflow: Engineer reports outage, Administrator reviews and assigns, Technician starts and completes work | Outage progresses Reported → Under Review → Assigned → In Progress → Resolved; work order ends Completed | Full workflow completed; resolution timestamp and maintenance activity recorded | PASS |
| GC-05 | Create outage with invalid substation ID | Request rejected | `ValueError` raised as expected | PASS |
| GC-06 | Create a duplicate active outage | Duplicate rejected | `ValueError` raised as expected | PASS |
| GC-07 | Wrong technician attempts to start another technician's work order | Action blocked | `PermissionError` raised as expected | PASS |
| GC-08 | Technician attempts to complete work without resolution notes | Completion rejected | `ValueError` raised as expected | PASS |

## 4. ClinicCare-Lite Test Results

| ID | Test objective and input | Expected outcome | Actual outcome | Result |
|---|---|---|---|---|
| CC-01 | Open public home and login pages | HTTP 200 responses | Pages responded successfully | PASS |
| CC-02 | Access clinician/patient dashboards without login | Redirect to authentication | Both protected dashboards redirected | PASS |
| CC-03 | Log in as patient with valid credentials | Redirect to patient dashboard | Correct redirect occurred | PASS |
| CC-04 | Log in as clinician with valid credentials | Redirect to clinician dashboard | Correct redirect occurred | PASS |
| CC-05 | Log in with wrong password | Login rejected with error message | Invalid-credentials message displayed; session not authenticated | PASS |
| CC-06 | Patient views dashboard when another patient's task exists | Only own tasks visible | Other patient's task not shown | PASS |
| CC-07 | Patient attempts to submit to another patient's task | Action blocked; no submission created | Redirected and submission count remained zero | PASS |
| CC-08 | Clinician attempts to review another clinician's submission | Action blocked | Redirected to clinician dashboard | PASS |
| CC-09 | Clinician attempts to download another clinician's submission | Action blocked | Redirected to clinician dashboard | PASS |
| CC-10 | Check home-page safety notice | Administrative/non-diagnostic warning visible | Required warning text present | PASS |
| CC-11 | Inspect application routes for diagnostic/treatment functions | No prohibited diagnostic routes | No prohibited route terms found | PASS |
| CC-12 | Inspect analytics metric names | Administrative metrics only; no medical scoring | No prohibited medical terms found | PASS |
| CC-13 | Validate upload extensions and filename sanitization | PDF/TXT accepted, PNG rejected, traversal path sanitized | All assertions passed | PASS |

## 5. Code Quality and Continuous Integration

The final CI pipeline completed successfully with the following sequence:

1. dependency installation — PASS
2. Ruff static analysis — PASS
3. Black formatting check — PASS
4. Pytest — **30 passed in 7.50 seconds**

The final successful CI run provides repeatable evidence that the integrated repository passes the configured automated checks in a clean GitHub-hosted Ubuntu environment.

## 6. Manual Release Checks

The automated suite covers the critical logic and security boundaries. The following manual checks should be performed once more during final packaging/demo preparation:

- start GridCare-Lite from a clean folder using only the root README instructions;
- log in with each GridCare demo role and visually confirm navigation;
- perform one complete outage-to-resolution workflow in the GUI;
- start ClinicCare-Lite from a clean folder using only the root README instructions;
- log in as clinician and patient and visually confirm the task → upload → review → outcome workflow;
- confirm announcements, messaging, appointments and analytics pages display correctly;
- verify the final ZIP contains only demo/synthetic data and no secrets or private uploads.

## 7. Conclusion

The final automated verification result is **PASS**. All 30 repository tests passed, and both linting and formatting checks passed. The tests specifically verify GridCare workflow integrity and role controls, ClinicCare authentication/privacy/upload safety, and ClinicCare's required administrative and non-diagnostic scope. Manual GUI/demo checks remain release-verification steps rather than unresolved automated test failures.
