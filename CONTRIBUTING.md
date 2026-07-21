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
