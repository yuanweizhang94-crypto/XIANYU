# CHG-0001 Design

Status: APPROVED
Change ID: CHG-0001-project-baseline

## Design

This change uses documents and deterministic scripts as the baseline. Generated state comes from Git, VERSION, active change, task progress, the capability registry, and recent test summary only.

## Verification strategy

`python scripts/verify_repository.py` runs structure checks, change checks, contract checks, duplicate capability checks, security scan, tests, project-state generation, and project-state schema validation.
