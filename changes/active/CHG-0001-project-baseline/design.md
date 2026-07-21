# CHG-0001 Design

Status: VERIFYING
Change ID: CHG-0001-project-baseline

## Design

This change uses documents and deterministic scripts as the baseline. Tracked generated state comes from VERSION, the dynamically discovered active change, task progress, and the capability registry only.

## Verification strategy

`python scripts/verify_repository.py` runs structure checks, change checks, contract checks, duplicate capability checks, security scan, tests, project-state comparison, and project-state schema validation.
