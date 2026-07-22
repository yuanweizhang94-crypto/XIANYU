# CAP-CORE-DATABASE

## Purpose

Provide the single SQLite WAL, SQLAlchemy, and Alembic infrastructure boundary for Core without creating business tables or touching real customer data.

## Current implementation change

- Active change: CHG-0002-core-application.
- Registry status during implementation: implementing.
- Final status after acceptance: verified.

## Registered implementation paths

- `app/xianyu_system/core/database.py`
- `app/xianyu_system/application.py`
- `alembic.ini`
- `migrations/env.py`
- `migrations/script.py.mako`
- `migrations/versions/0001_core_baseline.py`

## Registered verification paths

- `tests/unit/test_database.py`
- `tests/unit/test_application_factory.py`
- `tests/unit/test_import_safety.py`
- `tests/contract/test_migrations.py`
- `tests/contract/test_core_runtime.py`
- `tests/contract/test_distribution.py`
- `tests/contract/test_security_boundary.py`
- `changes/active/CHG-0002-core-application/tests/test_acceptance.py`

## Requirements

- Use SQLite with WAL mode for first-version local single-machine operation.
- Manage SQLAlchemy engine and session creation through one infrastructure module.
- Allow tests to use temporary directories and temporary database files.
- Avoid module-import side effects: imports must not create database files or open connections.
- Establish Alembic baseline without business tables in this change.

## T7 implementation decision

- Implementation file: `app/xianyu_system/core/database.py`.
- SQLite driver: `sqlite+pysqlite`.
- Database path comes from `ApplicationSettings.database_path`.
- Paths are resolved to absolute paths at initialization.
- Engine creation alone does not connect or create files.
- Database initialization occurs in FastAPI lifespan.
- SQLite uses WAL.
- SQLite foreign keys are enabled.
- SQLite busy timeout is 5000ms.
- File SQLite uses `check_same_thread=False`.
- Session factory is unified.
- Session context closes sessions but does not auto-commit.
- `Base.metadata` currently has no tables.
- No business schema is created.
- Engine is disposed during lifespan shutdown.
- Capability remains `implementing`.
- Alembic remains deferred to T8.

## T8 implementation decision

- Alembic config: `alembic.ini`.
- Migration environment: `migrations/env.py`.
- Baseline revision: `0001_core_baseline`.
- Target metadata: `Base.metadata`.
- Current metadata contains no business tables.
- Programmatic migration shares an existing SQLAlchemy Connection through `Config.attributes`.
- Standalone CLI migration requires explicit `-x database_path=...`.
- No default database URL is stored in `alembic.ini`.
- Alembic logging configuration is not installed.
- Upgrade and downgrade use the unified project Engine.
- Application startup does not automatically migrate.
- Current baseline creates no business schema.
- Capability remains `implementing`.

## T13 registry decision

- The database capability now records the unified SQLAlchemy module, application lifecycle wiring, Alembic configuration, migration environment, template, and deterministic empty baseline revision.
- Verification paths cover database unit behavior, migration contracts, import safety, integrated runtime behavior, installed-package behavior, security boundaries, and active-change acceptance.
- No database file, business table, ORM business model, or customer data path is registered.
- The capability remains `implementing`.
- `last_verified_commit` remains unset until T14 complete verification.

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
