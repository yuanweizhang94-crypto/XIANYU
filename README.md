# XIANYU

XIANYU is the long-lived repository for a future Xianyu operations automation system. The current repository state contains governance, specifications, validation scripts, tests, CI, and the initial Core application boundary. It does not provide real Xianyu publishing, message receiving, message sending, automated reply, WeCom, AI Provider, business API routes, database business logic, WebSocket, Playwright, or scheduled publishing capability.

## Project goal

The final intended business path is:

1. Product templates.
2. Immediate or scheduled Xianyu listing.
3. Receive customer inquiries from Xianyu.
4. Reply with fixed scripts.
5. Guide customers to WeCom customer service.
6. Send website links through WeCom.
7. Use AI only as fallback for questions not covered by fixed knowledge.
8. Transfer sensitive issues to human support.

## Current phase

The current phase is repository baseline plus the initial Core application boundary:

- Governance and fact-source rules.
- Scope, architecture, capability, ADR, and contract placeholders.
- Context, state generation, validation, duplicate capability detection, and security scan scripts.
- Unit, contract, acceptance tests, and GitHub CI.
- FastAPI application factory and typed local configuration boundary.

## Technical direction

The locked architecture direction is modular-monolith Core, one worker per Xianyu account, one Chrome Profile per account, and replaceable AI Provider. This baseline records the direction only and does not implement it.

The first phase does not introduce Redis, Celery, MySQL, PostgreSQL, React, n8n, OpenClaw runtime, vector databases, LangChain complex agents, Kubernetes, or multi-tenancy.

## Repository fact sources

Read these paths as the fact source, in order:

1. `AGENTS.md`
2. `specs/PROJECT_SCOPE.md`
3. `specs/SYSTEM_ARCHITECTURE.md`
4. `specs/CAPABILITY_REGISTRY.yaml`
5. `changes/active/`中动态发现的唯一活动变更目录 (the uniquely dynamically discovered active change directory)
6. `docs/adr/`
7. `contracts/`
8. `generated/PROJECT_STATE.json`
9. `tests/`

Do not manually edit `generated/PROJECT_STATE.json`; generate it with `python scripts/generate_state.py`.

## Local setup

Recommended Python version: 3.12 or newer.

```bash
python -m venv .venv
. .venv/Scripts/activate
python -m pip install --upgrade pip
python -m pip install -e .[dev]
```

## Context command

```bash
python scripts/project_context.py
```

## Current configuration

The typed configuration class is `xianyu_system.core.config.ApplicationSettings`.

Current supported environment variables use the `XIANYU_` prefix:

- `XIANYU_ENVIRONMENT`
- `XIANYU_APP_TITLE`
- `XIANYU_APP_VERSION`
- `XIANYU_DEBUG`
- `XIANYU_LOG_LEVEL`
- `XIANYU_DATABASE_PATH`

Configuration source priority is explicit constructor override, then `XIANYU_` environment variable, then safe default value.

The application does not automatically load `.env` files. Constructing settings does not create a database file or directory. Current settings do not include real platform credential fields.

## Current logging

The structured logging boundary is `xianyu_system.core.logging`.

Logs are emitted as single-line JSON records. By default, project-managed loggers write to `stderr`, and the level comes from `XIANYU_LOG_LEVEL`.

Logging is configured during the FastAPI application lifespan startup, not during module import or application construction. Project loggers do not propagate to the root logger. Sensitive fields such as Secret, Token, Cookie, Password, Authorization, API key, and equivalent variants are redacted.

The current logging boundary does not create log files or a `logs/` directory and does not send logs to any external logging service.

## Current database infrastructure

The database infrastructure boundary is `xianyu_system.core.database`.

It uses SQLite through the `sqlite+pysqlite` driver. The database path comes from `XIANYU_DATABASE_PATH` through `ApplicationSettings.database_path`. Creating an Engine does not by itself connect or create a database file.

The database is initialized during FastAPI application lifespan startup. Initialization enables and verifies WAL mode, enables SQLite foreign keys, and sets a 5000ms busy timeout for project Engine connections. Sessions are created through one Session factory, and the Session context manager closes sessions without automatically committing.

The application disposes its Engine during lifespan shutdown. `Base.metadata` currently contains no business tables, Alembic has not been implemented yet, and the database layer does not store real customer data.

## Current migrations

Alembic is configured through `alembic.ini` and the `migrations/` directory. The current revision is `0001_core_baseline`. Current metadata is empty and there are no business tables. Applying the baseline records Alembic version state only.

Programmatic migrations share an existing project Engine `Connection`. CLI migrations must pass an explicit database path, for example:

```bash
python -m alembic -c alembic.ini -x database_path=/tmp/xianyu.db upgrade head
```

Inspect migration heads and history with:

```bash
python -m alembic -c alembic.ini heads
python -m alembic -c alembic.ini history
```

Application startup does not automatically run migrations. Do not run migration tests against real data stores. Future schema must be introduced through an approved change and a new revision.

## Verification commands

```bash
python scripts/verify_repository.py
pytest
ruff check .
mypy scripts app
```

## Development flow

1. Create one branch per approved change from `main`.
2. Run `python scripts/project_context.py` before development.
3. Search existing specs, ADRs, scripts, and tests before adding anything.
4. Complete only the next unfinished task.
5. Update the active change task list only after the work is actually complete.
6. Run unified verification before commit.
7. Create one commit and open a PR.

## Current capability statement

This repository currently contains no real business capability. It cannot log in to Xianyu, publish listings, receive messages, send messages, call WeCom, call AI, run business FastAPI routes, create business database tables, install browsers, or access real accounts.
