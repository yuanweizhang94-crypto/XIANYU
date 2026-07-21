# CAP-CORE-DATABASE

## Purpose

Provide the single SQLite WAL, SQLAlchemy, and Alembic infrastructure boundary for Core without creating business tables or touching real customer data.

## Current implementation change

- Active change: CHG-0002-core-application.
- Registry status during implementation: implementing.
- Final status after acceptance: verified.

## Planned implementation paths

- `app/xianyu_system/core/database.py`
- Alembic configuration and baseline migration files when T8 begins.
- `app/xianyu_system/application.py` for lifecycle wiring.

## Planned test paths

- `tests/unit/` for database engine/session and WAL behavior.
- `tests/contract/` for migration and schema-contract behavior when introduced.
- `changes/active/CHG-0002-core-application/tests/` for CHG-0002 acceptance coverage.

## Requirements

- Use SQLite with WAL mode for first-version local single-machine operation.
- Manage SQLAlchemy engine and session creation through one infrastructure module.
- Allow tests to use temporary directories and temporary database files.
- Avoid module-import side effects: imports must not create database files or open connections.
- Establish Alembic baseline without business tables in this change.

## Acceptance criteria

- SQLite WAL is enabled by the unified database module.
- SQLAlchemy sessions are created through the unified module.
- Alembic baseline can run in a temporary test database.
- No database files are committed.
- `CAP-CORE-DATABASE` is updated to verified only after CHG-0002 implementation and validation are complete.

## Security boundaries

- Do not store Cookie, Token, Secret, Password, real customer data, or browser credentials.
- Do not access real platform accounts.
- Do not create or migrate production databases.

## Out of scope

- Business tables for products, accounts, messages, replies, schedules, or external integrations.
- MySQL, PostgreSQL, Redis, Celery, or distributed database infrastructure.
- Real customer data migration.
