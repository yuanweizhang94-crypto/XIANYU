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

## CHG-0008 upstream pilot anti-drift rules

- Before adding a new Xianyu capability, check existing Account, Message, Reply, Publish, and Schedule boundaries and reuse their facts instead of reimplementing them.
- Do not create large adapter abstractions, fake sessions, mapping DTOs, or new runtimes only because they may be useful later.
- Pin upstream repositories to exact commits before audit or execution; never silently follow floating main or master.
- Do not copy upstream source code, deployment scripts, protocol constants, signing logic, decryption logic, or Cookie examples into this repository.
- Local verified capability means deterministic local evidence only; it does not mean live Xianyu operation works.
- Stop on CAPTCHA, slider, face verification, device verification, risk-control prompts, unknown outcomes, or uncertain permissions.
- CHG-0008 is an upstream pilot governance and evidence change. It must not create CHG-0009 or `app/xianyu_system/adapters/xianyu/` without later pilot evidence proving a specific interface is needed.
