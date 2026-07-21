# Repository Agent Rules

These rules apply to any AI or automation agent and are not specific to one vendor or model.

## Required behavior

- Do not rely on old chats, model memory, or external memory.
- Run `python scripts/project_context.py` before development.
- Treat `changes/active/`, `specs/`, `docs/adr/`, `contracts/`, `generated/PROJECT_STATE.json`, `scripts/`, and `tests/` as the fact sources.
- Execute only the approved active change.
- Complete only one unfinished task at a time.
- Search existing implementation, specs, ADRs, scripts, and tests before adding new work.
- Do not implement the same capability in parallel paths.
- Do not manually edit generated files, especially `generated/PROJECT_STATE.json`.
- Do not add unapproved dependencies.
- Stop and fail closed when risk, credentials, permissions, platform verification, or scope is uncertain.
- Do not commit Cookie, Token, Secret, private keys, real customer data, or browser Profiles.
- Run `python scripts/verify_repository.py` after completion.

## CHG-0001 boundary

`CHG-0001-project-baseline` only establishes governance, specifications, validation scripts, tests, contract placeholders, and CI. It must not implement real Xianyu, WeCom, AI, database business, WebSocket, Playwright, FastAPI, or scheduled publishing capability.
