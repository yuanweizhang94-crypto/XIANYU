# Contributing

## Branch and PR rules

- One change per branch.
- One target per PR.
- Do not push directly to `main`.
- Create an approved active change before implementation.
- Keep the branch, active change, and task identifier aligned.

## Required workflow

1. Create a change branch from current `main`.
2. Run `python scripts/project_context.py`.
3. Search existing specs, ADRs, scripts, and tests.
4. Work only on the next unfinished task.
5. Update `tasks.md` after a task is actually complete.
6. Run:

```bash
python scripts/verify_repository.py
pytest
ruff check .
mypy scripts app
```

7. Confirm no sensitive data, unapproved dependency, duplicate capability, or out-of-scope business logic exists.

## Tests for permanent governance and active changes

- Keep long-lived, change-agnostic repository tests under `tests/`.
- Each active change may maintain its own `tests/` directory, for example `changes/active/<change-id>/tests/`.
- The default pytest configuration collects both `tests/` and `changes/active/`, so active-change acceptance tests run in normal local verification and CI.
- Do not put temporary acceptance limits for one specific change into permanent tests.
- When archiving an old change, move its dedicated tests together with the whole change directory into `changes/archive/`.
- Historical tests under `changes/archive/` are preserved for audit only and are not part of default pytest or CI collection.
- A new active change must add or update dedicated acceptance tests according to its own `acceptance.md` before implementation is considered verified.

## Starting the next change

After the current change PR is merged, prepare the next change with one atomic preparation commit:

1. Move the previous change directory from `changes/active/` to `changes/archive/`.
2. Update the previous change status consistently to `ARCHIVED` in `proposal.md`, `design.md`, `tasks.md`, and `acceptance.md`.
3. Create exactly one new active change directory under `changes/active/`.
4. Set the new change status to `DRAFT`, or to `APPROVED` only after explicit project-owner approval.
5. Regenerate `generated/PROJECT_STATE.json` with `python scripts/generate_state.py`.
6. Commit the archive move, new active change directory, and regenerated project state together.

Rules for change transitions:

- Do not write business code before the new change is formally approved.
- The final tree must contain at most one directory under `changes/active/`.
- `ARCHIVED` changes must exist only under `changes/archive/`.
- The active change `acceptance.md` defines the allowed and forbidden scope for the current work.
- The archive move and the creation of the next active change must be committed atomically.
- Dedicated tests for the previous change move with that change into `changes/archive/`; dedicated tests for the new change live under `changes/active/<change-id>/tests/`.
