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
mypy scripts
```

7. Confirm no sensitive data, unapproved dependency, duplicate capability, or out-of-scope business logic exists.

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
