# Repository Agent Rules

These rules apply to any AI or automation agent and are not specific to one vendor or model.

## Required behavior

- Do not rely on old chats, model memory, or external memory.
- Run `python scripts/project_context.py` before development.
- Treat `changes/active/`, `specs/`, `docs/adr/`, `contracts/`, `generated/PROJECT_STATE.json`, `scripts/`, and `tests/` as the fact sources.
- Specific change scope must be read only from the current active change proposal, design, tasks, and acceptance files.
- Root `AGENTS.md` must not store the feature boundary for any specific change.
- The current active change `acceptance.md` has priority for defining what is allowed and forbidden in the current work.
- DRAFT status is read-and-review only and must not be implemented.
- APPROVED, IMPLEMENTING, and VERIFYING are executable statuses.
- Do not modify business code when there is no executable active change.
- Execute only the current executable active change.
- Complete only one unfinished task at a time.
- Search existing implementation, specs, ADRs, scripts, and tests before adding new work.
- Do not implement the same capability in parallel paths.
- Do not manually edit generated files, especially `generated/PROJECT_STATE.json`.
- Do not add unapproved dependencies.
- Stop and fail closed when risk, credentials, permissions, platform verification, or scope is uncertain.
- Do not commit Cookie, Token, Secret, private keys, real customer data, or browser Profiles.
- Do not hardcode any specific change identifier in this file.
- Run `python scripts/verify_repository.py` after completion.
