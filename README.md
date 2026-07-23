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
- FastAPI application factory, typed local configuration, structured logging, SQLite/Alembic infrastructure, scheduler lifecycle boundaries, a read-only health API, and a minimal server-rendered web skeleton.

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

The application disposes its Engine during lifespan shutdown. `Base.metadata` currently contains no business tables, Alembic is configured with an empty baseline revision, and the database layer does not store real customer data.

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


## Current health API

The current API boundary exposes only `GET /health`. A healthy local Core returns HTTP 200 with `status: ok`; a local component failure returns HTTP 503 with `status: degraded`.

The response includes safe `service`, `version`, and `environment` values from the current application settings. It reports database connectivity and WAL status, plus scheduler running state, job count, and UTC timezone.

The database probe is read-only and only executes `SELECT 1` and `PRAGMA journal_mode` against the existing application Engine. The health route does not write database data, automatically run migrations, create tables, or create a new database Engine.

The scheduler probe only reads running state and job count from the existing scheduler. It does not register, start, stop, pause, resume, or remove scheduler jobs.

The health API performs no external service checks and does not expose database paths, exception details, credentials, account identifiers, customer data, browser profile details, Cookies, Tokens, Secrets, or Passwords. The OpenAPI contract is `contracts/openapi.yaml`. There are currently no other business API routes.

## Current web skeleton

The current web boundary provides a minimal Core home page only:

- `GET /` renders through Jinja2 and is excluded from OpenAPI.
- Templates live inside the `xianyu_system.web` package.
- Static resources are mounted at `/static`.
- CSS is served from a local package file.
- HTMX is pinned to version 2.0.10 and vendored locally with its license.
- No CDN, external font, external image, frontend build system, `package.json`, or `node_modules` is used.
- The only HTMX interaction is a user-triggered `GET /health`.
- There are no form submissions, business pages, business APIs, database writes, automatic migrations, Scheduler job changes, or external network calls.
- Runtime OpenAPI still contains only `/health`.
- Web package-data is configured so templates and static assets are included with the Python package.

## Current scheduler infrastructure

The scheduler infrastructure boundary is `xianyu_system.core.scheduler`.

It creates an APScheduler 3.x `BackgroundScheduler` with an in-memory `MemoryJobStore` and UTC timezone. The scheduler is created and started during the FastAPI application lifespan after logging and database initialization, then shut down before database disposal and logging cleanup.

The current scheduler registers no jobs, uses no persistent job store, creates no scheduler database tables, and does not implement scheduled publishing or other business workflows.



## Core capability evidence registry

The capability registry is `specs/CAPABILITY_REGISTRY.yaml`.

CHG-0002 records exact repository-relative implementation and verification file paths for `CAP-CORE-CONFIG`, `CAP-CORE-DATABASE`, and `CAP-HEALTH-MONITOR`. Paths use POSIX separators and point to files, not directories, generated artifacts, temporary files, database files, logs, caches, or globs.

`app/xianyu_system/application.py` is a shared integration boundary where configuration injection, database lifecycle wiring, and health route registration meet. Integrated runtime, distribution, import-safety, security-boundary, and active-change acceptance tests may provide evidence for more than one Core capability when they exercise real cross-capability behavior.

The three Core capabilities are now `verified`, are no longer bound through registry `active_change`, and record `d11f1afc4564298e8c2709fdb80a41a491dbb1ea` as `last_verified_commit`. The seven non-Core capabilities remain `planned`, unbound, and without implementation or verification paths. Core Scheduler infrastructure does not make `CAP-XY-SCHEDULE` a business capability implementation.

## Core verification status

- CHG-0002 was merged through PR #2.
- Merge commit: `e2d41e0cc392ae0298688c01147e983317c7e1df`.
- CHG-0002 is archived.
- CHG-0003-xianyu-account-boundary is the only active change.
- CHG-0003 status is `APPROVED`.
- T1 project-owner approval is complete.
- T2 account and Profile isolation terminology is complete.
- T3 security and credential-handling boundaries is complete.
- T4 persistence and migration principles is complete.
- T5 runtime module and ownership boundaries is complete.
- T6 minimal local account boundary implementation is complete.
- T7 dedicated permanent account tests are complete.
- T8 capability evidence and complete verification is the next executable task.
- No CHG-0003 external account integration has started.
- Complete local verification candidate SHA: `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.
- T1 through T15 are complete for archived CHG-0002.
- `CAP-CORE-CONFIG`, `CAP-CORE-DATABASE`, and `CAP-HEALTH-MONITOR` are `verified`.
- Each verified Core capability records `d11f1afc4564298e8c2709fdb80a41a491dbb1ea` in `last_verified_commit`.
- Verified Core capabilities have cleared their registry `active_change` field.
- The seven non-Core capabilities remain `planned`.
- `CAP-XY-ACCOUNT` remains planned and unbound.
- `CAP-XY-SCHEDULE` remains `planned`.
- No Xianyu account runtime, Cookie import, browser Profile loading, login, or external platform access is implemented.
- Approval and T5 completion of CHG-0003 do not mean that runtime implementation, real account access, Cookie or Token handling, browser Profile loading, Ready-for-review, auto-merge, or merge has been approved.

Within CHG-0003:

- Platform Account means the real external Xianyu account.
- Account Reference means the repository-owned non-secret logical reference.
- Profile means the local isolation boundary and does not mean a browser profile.
- Profile Identifier is the canonical local identity.
- Credential Reference is an opaque reference and never contains secret material.
- Session Material remains sensitive and outside the approved implementation boundary.


Within the approved CHG-0003 security boundary:

- Secret Material is prohibited from repository and ordinary application persistence.
- Credential References are opaque, Profile-owned, and never contain secret values.
- A future Secure Storage Boundary must enforce encryption at rest and least-privilege access.
- A future operation may proceed only with exact Profile ownership, successful resolution, explicit authorization, and a non-blocked risk decision.
- Unknown, unavailable, invalid, expired, revoked, denied, verification-required, or risk-blocked states fail closed.
- Secret Material and full Credential References must not appear in logs or diagnostics.
- Only Synthetic Fixtures are permitted in tests.


Within the approved CHG-0003 persistence boundary:

- The existing CAP-CORE-DATABASE SQLite, SQLAlchemy, and Alembic infrastructure remains the only approved persistence boundary.
- Only minimal non-secret Profile and Account Reference metadata may be persisted.
- Credential References remain opaque, non-secret, and Profile-owned.
- Secret Material, browser state, and generic JSON, BLOB, payload, properties, extras, metadata, context, or arbitrary key-value fields are prohibited.
- Persistence mutations require explicit Profile ownership, transactions, uniqueness protection, and concurrency-conflict protection.
- Future migrations remain explicit and application startup must not auto-migrate.
- Exact physical schema and Alembic implementation remain deferred to T6.
- T4 creates no Migration file, ORM model, table, Repository, API, or Worker.

Within the approved CHG-0003 runtime ownership boundary:

- CAP-XY-ACCOUNT is owned by the `worker.account` capability namespace.
- The future package is `xianyu_system.worker.account`.
- The minimal modules are `domain.py`, `persistence.py`, and `service.py`.
- Domain code remains independent of SQLAlchemy and FastAPI.
- Persistence uses the existing Core Engine and Session boundary.
- Account Service owns logical transaction coordination.
- Profile Identifier generation uses UUID version 4.
- Local lifecycle states are PENDING, ENABLED, and DISABLED.
- CHG-0003 owns opaque Credential References but does not resolve Secret Material.
- No API, browser integration, background process, Scheduler Job, or Provider is included.
- T5 created no implementation files.

Within the approved CHG-0003 T6 implementation:

The T6 implementation correction is complete.

- `Profile` and `AccountReference` are distinct immutable domain concepts.
- Their one-to-one ownership is enforced locally.
- They remain flattened into one non-secret relational projection.
- ORM and Migration constraints reject blank or padded reference metadata.
- Existing Core unit-test edits made during T6 were compatibility updates only.
- Dedicated permanent account testing remains T7.

- The local package `xianyu_system.worker.account` exists.
- A local SQLite table and Migration `0002_xianyu_account_boundary` exist.
- One SQLAlchemy relational projection, one Repository, and one Service exist.
- Profile Identifier generation, local lifecycle transitions, and optimistic concurrency are implemented.
- There is still no external account access, HTTP API, browser integration, Provider, or Secret Material handling.

Completion of T6 does not authorize starting T7 in the same execution, Ready-for-review, auto-merge, or merge.

CHG-0003 permanent account coverage now verifies:

- immutable Profile and AccountReference ownership;
- input normalization and lifecycle invariants;
- Account Service transactions and optimistic concurrency;
- Profile-scoped uniqueness and rollback;
- Repository and Migration behavior;
- guarded non-empty downgrade;
- database-level trim constraints;
- sanitized errors;
- absence of external account, browser, API, Provider, Secure Storage, network, Scheduler, and background-process behavior.

Completion of T7 does not authorize T8 in the same execution, Ready-for-review, auto-merge, or merge.

The T7 permanent evidence hardening is complete.

- Local account operations are tested with network, subprocess, and user-Home access blocked.
- Account Contract tests no longer clear mappers, remove the account table from shared metadata, or evict account modules.
- Persistence and security Contract tests pass in either execution order.
- Database constraints explicitly reject whitespace-only external and credential references.
- Test counts remain unchanged.
- T8 capability evidence remains the next executable task.

The T7 Contract evidence is now isolated from the parent pytest process.

- No replacement account package is inserted into `sys.modules`.
- No SQLAlchemy metadata type or equality behavior is patched.
- Account ORM, Repository, Service, and Migration checks run in isolated Python processes.
- Importing the Contract test modules leaves account runtime modules and Core metadata unchanged.
- Runtime external-resource blocking and database-constraint evidence remain intact.
- Test counts remain unchanged.
- T8 remains the next executable task.

The T7 import-boundary correction is complete.

- Importing the account package or account Domain no longer eagerly imports Account Service.
- Account Domain imports no longer load account Persistence or register ORM metadata.
- `AccountService` remains part of the public package surface and loads lazily as the real Service class.
- Permanent Import Safety evidence covers the account package and Domain module.
- Core runtime metadata remains empty during Domain-only test collection.
- No Migration, Core runtime, Registry, capability, dependency, CI, API, browser, Provider, Secure Storage, Scheduler, background-process, external-network, real-account, or Secret Material behavior was added.
- The next state transition requires explicit project-owner authorization.
- Verification does not implement any Xianyu, WeCom, AI, browser automation, business route, business page, or business table capability.

The final T7 encoding correction is complete.

- The account package initializer is UTF-8 without BOM.
- Only the leading BOM bytes were removed.
- AccountService lazy-loading behavior is unchanged.
- Permanent Import Safety and active-change acceptance verify the raw file bytes.
- Test counts remain unchanged.
- T8 remains the next executable task.

## Permanent test layers

CHG-0002 now has permanent test coverage across these layers:

- Unit tests for import safety and side-effect boundaries.
- Contract tests for Core runtime lifecycle, health, database, scheduler, web, distribution, and security boundaries.
- Distribution tests for offline wheel build, package-data inclusion, vendored HTMX integrity, and installed-package smoke behavior.
- Security-boundary tests for synthetic secret non-exposure, blocked external sockets, read-only HTTP behavior, and absence of external business integrations.
- Archived CHG-0002 acceptance tests mapping executable evidence to all 25 CHG-0002 final acceptance criteria, plus the active CHG-0003 draft acceptance tests.

The permanent tests specifically verify:

1. Application construction remains reusable and side-effect free.
2. Multiple application instances can run in one process without resource sharing.
3. `/health` remains the only OpenAPI path.
4. The home page and static resources are local package resources.
5. HTMX remains locally vendored with the approved SHA-384 digest.
6. SQLite is initialized only during lifespan startup and runs in WAL mode.
7. SQLAlchemy metadata remains empty and no business tables are created.
8. Scheduler startup and shutdown are controlled by the application lifespan and no jobs are registered.
9. Imports do not create databases, logs, scheduler threads, or network connections.
10. Synthetic credentials, account data, Cookies, Tokens, Secrets, and browser profiles are not loaded or exposed.
11. No Xianyu, WeCom, AI Provider, Playwright, browser automation, or external business integration is implemented.

The three Core capability registry entries are verified after complete validation and record the approved verification candidate commit. The seven non-Core capabilities remain planned.

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
