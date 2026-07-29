# System Architecture

## Locked direction

- Modular-monolith Core.
- One worker per Xianyu account.
- One Chrome Profile per account.
- WebSocket is responsible for message receiving.
- Playwright is responsible for publishing automation.
- APScheduler is responsible for planned jobs.
- SQLite WAL is the first-version database direction.
- WeCom customer-service API is the customer-service direction.
- Fixed rules have priority; AI is fallback.
- AI must not hold platform secrets or browser permissions.

## Baseline limitation

This change writes architecture only. It does not implement the capabilities above. `app/` and `worker/` contain only package boundaries and explanatory files.

## Module boundaries

- `app/`: future Core application entry, configuration, database, rules, and contract adapter boundary.
- `worker/`: future per-account worker boundary; source files must not be copied per account.
- `adapters/`: future platform and external-service adapters.
- `contracts/`: OpenAPI and JSON Schema contracts.
- `specs/`: scope, architecture, capability, and ADR fact sources.

## CHG-0008 upstream pilot anti-drift rules

- Before adding a new Xianyu capability, check existing Account, Message, Reply, Publish, and Schedule boundaries and reuse their facts instead of reimplementing them.
- Do not create large adapter abstractions, fake sessions, mapping DTOs, or new runtimes only because they may be useful later.
- Pin upstream repositories to exact commits before audit or execution; never silently follow floating main or master.
- Do not copy upstream source code, deployment scripts, protocol constants, signing logic, decryption logic, or Cookie examples into this repository.
- Local verified capability means deterministic local evidence only; it does not mean live Xianyu operation works.
- Stop on CAPTCHA, slider, face verification, device verification, risk-control prompts, unknown outcomes, or uncertain permissions.
- CHG-0008 is an upstream pilot governance and evidence change. It must not create CHG-0009 or `app/xianyu_system/adapters/xianyu/` without later pilot evidence proving a specific interface is needed.

## CHG-0008 wrapper decision

CHG-0008 selected `WRAP` after supervised upstream Pilot evidence. The architecture direction is not to vendor or rewrite upstream protocol code. Future integration should use a narrow localhost-only wrapper around the independent upstream Pilot service while keeping Cookie, Token, Session, browser Profile, and platform protocol details outside `D:/xianyu`.

## CHG-0009 wrapper MVP architecture

The CHG-0009 architecture keeps `D:/xianyu` as the owner of business rules, manual confirmation, idempotency, audit, and CLI operations while `D:/xianyu-upstream-pilot` remains the owner of login, Cookie, Token, Session, browser Profile, WebSocket, and platform protocol behavior. The wrapper is localhost-only and fail-closed for writes.
