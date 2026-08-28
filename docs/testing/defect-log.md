# CS 112 Final Project Defect Log

**Team:** Team 12  
**Status:** Final development/release review

This log records confirmed defects or release-documentation gaps found during development and final integration. Entries are based on Git history, GitHub Actions output, and the final submission audit; no hypothetical defects are included.

| ID | Component | Defect / evidence | Severity | Corrective action | Retest / final status |
|---|---|---|---|---|---|
| D-01 | ClinicCare / CI | A ClinicCare feature build failed the CI Ruff step because of duplicate/redefined imports, unused imports, unsorted import blocks, missing trailing newlines and related code-quality errors. The CI run reported 34 Ruff errors and stopped before Black/Pytest. | Medium | Imports and formatting were cleaned up during subsequent integration/code-quality work. Duplicate and unused imports were removed and formatting was normalized. | **RESOLVED.** Final CI #53: Ruff PASS, Black PASS, Pytest 30/30 PASS. |
| D-02 | ClinicCare authentication | Authentication tests and the user model needed strengthening/cleanup. The repository contains a dedicated commit titled `Fix authentication tests and clean user model`, adding explicit patient/clinician login, protected-dashboard and wrong-password tests while cleaning password/model handling. | High | User password methods/model definitions were cleaned up and explicit authentication regression tests were added. | **RESOLVED.** Final ClinicCare authentication suite: 5/5 PASS, including wrong-password rejection. |
| D-03 | GridCare repository/code quality | Duplicate files/formatting inconsistencies were present during GridCare development. The repository records a cleanup commit titled `Clean GridCare formatting and remove duplicate files`. | Low | Duplicate files were removed and GridCare formatting was normalized. | **RESOLVED.** Final Ruff/Black checks PASS and GridCare automated tests PASS. |
| D-04 | Final submission datasets | `Datasets/utilities.csv` was missing during the final submission audit even though the generator defines and produces utilities data. This would have left the required three-dataset package incomplete. | Medium | Added `Datasets/utilities.csv` using the utility records defined by the unchanged synthetic-data generator. | **RESOLVED.** File is present on `main`; final CI PASS. |
| D-05 | Final submission dependencies | A single top-level `requirements.txt` required for the final package was missing; dependencies were previously split across component and development requirement files. | Medium | Added a root runtime `requirements.txt` combining Grid Analysis, GridCare-Lite and ClinicCare-Lite runtime dependencies while retaining component files. | **RESOLVED.** Root requirements file is present on `main`; final CI dependency installation/checks PASS. |
| D-06 | Grid Analysis documentation | Grid Analysis README formatting required a cleanup during final documentation work, recorded in the repository as `Fix Grid Analysis README formatting`. | Low | README formatting was corrected. | **RESOLVED.** Documentation retained in final integrated repository. |

## Final Defect Status

At the final automated verification point, there are **no known unresolved automated-test or CI failures** in the integrated `main` branch. The latest CI run completed successfully with Ruff, Black and all 30 Pytest tests passing.

The remaining pre-submission activities are release checks rather than known software defects: final clean-install verification, final application demo walkthroughs, and inspection of the submission ZIP for required documents and absence of private/sensitive files.
