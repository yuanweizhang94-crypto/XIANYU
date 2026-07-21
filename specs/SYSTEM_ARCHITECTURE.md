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
