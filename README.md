# XIANYU

XIANYU is the long-lived repository for a future Xianyu operations automation system. The current repository contains governance, specifications, validation scripts, tests, CI, and Registry-verified local deterministic boundaries. Those verified capabilities are valid only within local execution and synthetic fixtures. The repository does not provide real Xianyu access, real listing publication, real message receiving or sending, Playwright or browser automation, real Credential handling, WeCom integration, AI Provider integration, or external platform side effects.

## Current change state

- PR #6 was merged into `main`.
- PR #6 merge commit is `dcc4a770dfcb3a69fb3809cb3868ed752813482b`.
- Merged CHG-0006 feature HEAD is `417db817d8641755fb5f66d78db6c143bd1dc53c`.
- CHG-0006-xianyu-publish-boundary is archived.
- CAP-XY-PUBLISH remains verified.
- Evidence Candidate remains `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`.
- Historical acceptance evidence is under `changes/archive/CHG-0006-xianyu-publish-boundary/tests/test_acceptance.py`.
- There is no Active Change.
- There is no approved executable task.
- CHG-0007 has not been created.
- CAP-XY-PUBLISH `implementation_paths` are unchanged.
- CAP-XY-PUBLISH `test_paths` changed only by moving the CHG-0006 acceptance evidence path from `changes/active/` to `changes/archive/`.
- CAP-XY-PUBLISH `active_change` is null.
- CAP-XY-PUBLISH `last_verified_commit` is `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`.
- READY does not mean a real listing was published.
- The repository still has no real Xianyu access, real listing publication, real media upload, real message receiving or sending, browser automation, Playwright, Credential handling, browser Profile access, WeCom Provider, AI Provider, or external platform side effects.


## Historical phase record - CHG-0006 T5 approved publish architecture

This section records the state at T5 and is not the current repository state.

- At the end of T5, owner module remained `worker.publish`.
- At that historical point, package `app/xianyu_system/worker/publish` was documented only and had not been created by T5.
- At that historical point, publish Domain responsibilities covered ListingDraft, PublishRequest, PublishValidationResult, PublishDecision, PublishAttempt, PublishOutcome, lifecycle rules, reason codes, and fail-closed invariants.
- At that historical point, local Service orchestration could request a repository protocol, but it still could not call a real platform, receive Credential material, open a browser, or invoke Playwright.
- At that historical point, persistence and audit requirements were conceptual only; no schema, Migration, table, column, index, ORM model, or implementation file had been introduced by T5.
- ListingDraftLifecycle was `DRAFT`, `VALIDATED`, `READY_FOR_MANUAL_REVIEW`, and `ARCHIVED`; it intentionally excluded `PUBLISHED` because the local boundary does not publish.
- Failure classification covered `VALIDATION_ERROR`, `AUTHORIZATION_ERROR`, `RISK_BLOCKED`, `IDEMPOTENCY_CONFLICT`, `DUPLICATE_REQUEST`, `PERSISTENCE_ERROR`, `ADAPTER_ERROR`, `TIMEOUT`, `UNKNOWN_OUTCOME`, and `CANCELLED`.
- At that historical point, T6 was the next task.


## Historical phase record - CHG-0006 T6 local deterministic publish boundary

This section records the state at T6 completion and is not the current repository state.

- At the end of T6, the local package `app/xianyu_system/worker/publish/` existed.
- At the end of T6, runtime files were `__init__.py`, `domain.py`, `fingerprint.py`, `validation.py`, `persistence.py`, and `service.py`.
- At the end of T6, Migration `0005_xianyu_publish_boundary` created local publish request, sanitized audit, and attempt-snapshot tables.
- At the end of T6, the Service returned deterministic local decisions only: READY, INVALID_INPUT, UNAUTHORIZED, RISK_BLOCKED, DUPLICATE, CONFLICT, or MANUAL_REVIEW.
- READY meant local readiness for a separately authorized future boundary only; it did not publish listings and did not start a PublishAttempt.
- At T6 completion, CAP-XY-PUBLISH was still planned and unbound.
- At T6 completion, T7 was the next task and had not started.
- This is a historical phase record; T7 and T8 are now complete.


## Historical phase record - CHG-0006 T7 permanent Publish tests

This section records the state at the T7 commit. T8 has since completed.

- T7 added permanent unit, contract, security, migration, import-safety, and active-change acceptance coverage for the local deterministic Publish boundary.
- The T7 unit tests covered Publish domain normalization, media metadata canonicalization, fingerprint stability, validation fail-closed ordering, and service idempotency/duplicate/UNKNOWN/persistence-failure behavior.
- The T7 contract tests covered local SQLite publish persistence, Alembic migration constraints, empty downgrade, non-empty downgrade fail-closed behavior, and static/runtime security boundaries.
- At the T7 commit, T7 did not bind CAP-XY-PUBLISH evidence; CAP-XY-PUBLISH remained planned and unbound until T8.
- At the T7 commit, T8 was the next task and had not started.


## Historical phase record - CHG-0006 T8 Phase A Evidence Candidate

This was the Phase A Candidate state at commit `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`. Phase B verification has since completed.

- During Phase A, CAP-XY-PUBLISH was registered as `implementing` for the Evidence Candidate.
- During Phase A, `active_change` was `CHG-0006-xianyu-publish-boundary`.
- During Phase A, `last_verified_commit` was null until the Candidate commit itself completed local and GitHub Actions verification.
- During Phase A, evidence paths were exact repository-relative files for the local deterministic Publish runtime and permanent tests only.
- During Phase A, T8 was not complete; Phase B later recorded the verified Candidate SHA after Actions were green.


## Historical phase record - CHG-0006 final review preparation

- CHG-0006 status is VERIFYING.
- T1-T8 are complete.
- T9 remains incomplete until the Ready transition and final administration record are complete.
- CAP-XY-PUBLISH remains verified and frozen.
- Evidence Candidate remains `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`.
- T8 Verification commit remains `51bfefb4ca63e2c7ac0128359da1f00c62ad37e9`.
- PR #6 remains Draft until the Ready Candidate passes final CI.
- No Reviewer request is authorized.
- Auto-merge and Merge remain unauthorized.
- The actual T9 Ready Candidate SHA is the SHA of the separate Phase A preparation commit created after local verification.

## Historical phase record - CHG-0006 final PR administration

- CHG-0006 final PR administration is complete.
- CHG-0006 status is VERIFYING.
- All nine tasks are complete.
- T9 Ready Candidate SHA is `52e389e804ca24f144c6c1bd73cc21b1ba21d4cb`.
- CAP-XY-PUBLISH remains verified.
- Evidence Candidate remains `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`.
- T8 Verification commit remains `51bfefb4ca63e2c7ac0128359da1f00c62ad37e9`.
- PR #6 later merged through normal two-parent merge commit `dcc4a770dfcb3a69fb3809cb3868ed752813482b`.
- No Reviewer was manually requested.
- Auto-merge and Merge remain unauthorized.
- CHG-0006 later moved to `changes/archive/CHG-0006-xianyu-publish-boundary` after merge.
- Merge requires separate authorization against exact PR HEAD.

## CHG-0007 final review preparation

CHG-0007 status is `VERIFYING` for final PR review preparation. T1 through T8 are complete; T9 remains incomplete until the Ready transition and final administration record finish. CAP-XY-SCHEDULE remains verified and frozen for the local deterministic Schedule boundary. Evidence Candidate SHA is `0d9cfacedc1947e518d990151225ec8a15540f76` and verification commit is `853129698995a32464a17aa93c9c9066d709cf7f`. PR #8 remains Draft until the Ready Candidate passes final CI. No Reviewer request, auto-merge, merge, close, archive, branch deletion, CHG-0008, runtime expansion, dependency change, workflow change, real Xianyu access, real scheduled publishing, browser automation, Playwright, Credential handling, WeCom, AI, Redis, Celery, recurring schedule, or external queue is authorized by this preparation state.


## CHG-0007 T8 Schedule capability verification

CAP-XY-SCHEDULE evidence paths are registered and verified. Evidence Candidate SHA: `0d9cfacedc1947e518d990151225ec8a15540f76`. Registry status is verified, active_change is null, and last_verified_commit records the Candidate SHA. Tasks are now 8 / 9 and T9 Complete final PR administration is the next executable task. PR #8 remains Draft, open, and unmerged. Verified does not authorize Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, CHG-0008, real Xianyu access, real scheduled publishing, browser automation, Playwright, Credential handling, WeCom, AI, Redis, Celery, recurring schedule, or external queue behavior.


## CHG-0007 T8 Phase A Evidence Candidate

CAP-XY-SCHEDULE is registered as `implementing` for the T8 Evidence Candidate. Exact implementation and test evidence paths are registered, and `last_verified_commit` remains unset until the Candidate commit is verified by local gates and GitHub Actions. Tasks remain 7 / 9 during Phase A; T8 is still the next task until Phase B completes. No real Xianyu access, real scheduled publishing, browser automation, Playwright, Credential handling, WeCom, AI, Redis, Celery, recurring schedule, external queue, Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, or CHG-0008 was performed.


## CHG-0007 T7 permanent Schedule tests

T7 added permanent unit, contract, security, migration, import-safety, and active-change acceptance coverage for the local deterministic Schedule boundary. Coverage includes one-time IMMEDIATE and RUN_AT_UTC requests, UTC normalization, deterministic fingerprints, idempotency replay, conflict detection, cancellation, atomic dispatch claim, finite misfire grace, local PublishService coupling, APScheduler DateTrigger registration through the existing in-memory Core scheduler, migration 0006 lineage, and security scans proving no real Xianyu, browser, Playwright, Credential, WeCom, AI, Redis, Celery, recurring schedule, or external queue behavior was introduced.

Tasks are now 7 / 9. T8 Bind capability evidence and complete two-phase verification is the next executable task. CAP-XY-SCHEDULE remains planned and unbound until T8.


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

The current phase is after CHG-0006 post-merge archive and before any separately authorized next change:

- Governance and fact-source rules remain active.
- Registry, generated project state, validation scripts, tests, and GitHub CI are present.
- The repository has verified local deterministic capability evidence for its completed boundaries.
- CAP-XY-PUBLISH is verified only for the local deterministic Publish boundary and synthetic fixtures.
- The repository still has no real Xianyu platform operation, real listing publication, media upload, browser automation, Credential handling, external network side effect, WeCom integration, or AI Provider integration.
- There is no Active Change and no approved executable task.
- CHG-0007 has not been created and requires separate project-owner authorization.


## Technical direction

The locked architecture direction is modular-monolith Core, one worker per Xianyu account, one Chrome Profile per account, and replaceable AI Provider. This baseline records the direction only and does not implement it.

The first phase does not introduce Redis, Celery, MySQL, PostgreSQL, React, n8n, OpenClaw runtime, vector databases, LangChain complex agents, Kubernetes, or multi-tenancy.

## Repository fact sources

Read these paths as the fact source, in order:

1. `AGENTS.md`
2. `specs/PROJECT_SCOPE.md`
3. `specs/SYSTEM_ARCHITECTURE.md`
4. `specs/CAPABILITY_REGISTRY.yaml`
5. `changes/active/`涓姩鎬佸彂鐜扮殑鍞竴娲诲姩鍙樻洿鐩綍 (the uniquely dynamically discovered active change directory)
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

CAP-XY-ACCOUNT capability evidence is verified.

- Evidence Candidate SHA: `2aab941cb7f713d7e46675789c47971a2c79c564`.
- The exact implementation and verification paths are registered.
- CAP-XY-ACCOUNT status is `verified`.
- T9 is the next executable task.
- PR #3 remains Draft, open, and unmerged.

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


CHG-0003 final PR administration is complete.

- CHG-0003 status is `VERIFYING`.
- All nine tasks are complete.
- CAP-XY-ACCOUNT remains verified.
- PR #3 is Ready for review, open and unmerged.
- Merge and auto-merge remain unauthorized.
- CHG-0003 remains under `changes/active/` until the PR is merged.

## CHG-0004 T7 permanent test coverage

- T7 dedicated unit, contract, security, and active-change acceptance tests are complete.
- T1 through T7 are complete; tasks are now 7 / 9.
- T8 Update capability evidence and run complete verification is the next executable task.
- T8 has not started and requires separate project-owner authorization.
- The permanent Message test suite adds exactly 42 tests: 12 Domain, 9 Service, 8 Worker, 8 Persistence Contract, and 5 Security Contract tests.
- Existing Import Safety coverage remains three test functions and now includes the Message Package import-safe boundary.
- Coverage includes NEW, DUPLICATE, INDETERMINATE, Content Conflict, Conversation Conflict, UUID4 generation, transaction ownership, rollback, Profile scope, Account scope, Worker lifecycle, failure-state mapping, explicit reset, one in-flight delivery, re-entry protection, and graceful stop.
- Coverage includes the three-table schema, Migration lineage, Foreign Keys, database constraints, Repository no-commit behavior, empty downgrade, non-empty downgrade fail-closed behavior, import isolation, absence of external integrations, blocked network/subprocess/Home/thread entry points, sanitized errors, Synthetic Fixture-only evidence, and contract order independence.
- No Runtime, Migration, Registry, Capability Specification, dependency, or CI file was modified for T7.
- `CAP-XY-MESSAGE` remains planned and unbound with empty implementation paths, empty test paths, null active_change, and null last_verified_commit pending T8.

## CHG-0004 T7 corrective hardening

- T7 corrective hardening was completed before T8.
- The permanent Message test count remains exactly 42 and full collection remains 322.
- Worker re-entry is now triggered from inside an active Service operation; the inner call fails with `WorkerBusy` before any second Service operation begins, while the outer operation completes and leaves the Worker `RUNNING`.
- Graceful stop is now covered with deterministic Events and finite-timeout test threads; the Worker enters `STOPPING`, rejects new delivery, waits for the in-flight operation, and reaches `STOPPED` only after completion.
- Repository flush-without-commit behavior is tested directly, including visible flush, no Repository commit call, explicit rollback removal, ownership round-trip, and UTC timestamp round-trip.
- Real SQLite evidence covers NEW, DUPLICATE, INDETERMINATE, Content Conflict, Conversation Conflict, row-count preservation, and existing Message Content preservation.
- Schema and constraint evidence covers approved types, lengths, nullable rules, primary keys, foreign keys, unique constraints, check constraints, prohibited columns, Delivery Identity scope, nullable Delivery Identities, Platform Message Identifier reuse, Message Content, decisions, Attempt outcomes, and Attempt numbers.
- Message-only downgrade explicitly targets `0002_xianyu_account_boundary`; empty downgrade preserves Account table/data and re-upgrades, while non-empty downgrade fails closed and preserves revision, tables, and rows.
- Security evidence runs Message Service and Message Worker in an isolated process with network, DNS, subprocess, Home-directory, and production thread-start entry points blocked.
- Package lazy-import evidence verifies Persistence, Service, and Worker are initially unloaded.
- Synthetic Fixture and cleanup escape-hatch scans cover all dedicated Message tests and active acceptance evidence.
- No Runtime, Migration, Registry, Capability Specification, dependency, or CI file was modified by the T7 correction.
- T8 was not started.

## CHG-0004 T7 final evidence follow-up

- T7 final evidence follow-up was completed before T8.
- The permanent Message test count remains exactly 42 and full collection remains 322.
- All approved Message Check Constraints are permanently verified by name and by normalized SQL semantics in both ORM projection and reflected SQLite schema.
- Foreign Key evidence includes constrained columns, referred tables, referred columns, and `ON DELETE RESTRICT` for Conversation, Message, and Delivery Attempt ownership relationships.
- Migration evidence covers source restrictions, Alembic CLI `upgrade head`, and Alembic offline SQL without creating the offline target database file.
- Remaining database constraint evidence covers Profile and Account scope, Delivery Identity uniqueness scope, duplicate attempt numbers, nullable platform identifiers, nullable reason/correlation values, participant validation, persisted decisions, Attempt outcomes, Attempt numbers, reason limits, and correlation limits.
- Public package evidence verifies initially unloaded Service, Persistence, and Worker modules, then actual lazy Domain, Transport, Service, Persistence, and Worker resolution.
- Isolated Worker security evidence covers NEW, DUPLICATE, INDETERMINATE, Content Conflict, Conversation Conflict, reset, restart, and stop while network, DNS, subprocess, Home-directory, and production thread-start entry points are blocked.
- Every dedicated Message test file and active acceptance test is independently checked for UTF-8 decoding, absence of BOM, Synthetic Fixtures, sensitive value patterns, customer data, and cleanup escape hatches.
- No Runtime, Migration, Registry, Capability Specification, dependency, or CI file was modified by the final T7 evidence follow-up.
- Tasks remain 7 / 9, T8 was not started, and `CAP-XY-MESSAGE` remains planned and unbound.

## CHG-0004 T7 exact evidence completion

- The final T7 correction closes the remaining direct database and isolated security evidence gaps.
- Every expected database failure is isolated in its own Connection and Transaction.
- Empty, blank, padded, over-limit, unknown-enum, ownership, scoped-identity, and Attempt-number cases are directly enforced.
- The same Delivery Identity is verified as valid for the same Profile under a different Account scope.
- Offline SQL is scanned for external URL, Credential, browser, and customer-data text.
- Both isolated conflict paths preserve Conversation, Message, and Delivery Attempt counts.
- Per-file security scans include plus-phone, standalone long-number, Credential-like, customer-data, raw-frame, production-account, and live-account patterns.
- Permanent test count remains 42.
- Full collection remains 322.
- Tasks remain 7 / 9.
- T8 remains separately authorized and has not started.

## CHG-0004 T7 sensitive scan completion

- CHG-0004 T7 sensitive-evidence scan correction is complete before T8.
- Every approved Message evidence file is scanned as complete UTF-8 Source after raw-byte and BOM checks.
- No prohibited source line is deleted, filtered, replaced, masked, or allowlisted before scanning.
- Plus-phone detection supports common separators and requires at least eight digits.
- Standalone long-number detection begins at eleven digits and avoids UUID-like embedded numeric segments.
- Bearer, Authorization Header, API Key, Access Token, Refresh Token, Session Cookie, Password, and Secret forms are covered.
- Real-customer, customer-message, customer-data, raw-frame, production-account, live-account, real-Xianyu-account, and real-account phrase forms are covered.
- Runtime positive controls prove every scanner category can detect its intended input.
- Scanner failure diagnostics report file path and category only, never matched values.
- No Runtime, Migration, Persistence Contract, Registry, Capability Specification, dependency, or CI file was modified by this correction.
- Permanent Message test count remains 42 and full collection remains 322.
- Tasks remain 7 / 9; T8 remains the next executable task and has not started.
- CAP-XY-MESSAGE remains planned and unbound.
- PR #4 remains Draft, open, unmerged, without requested reviewers, and without auto-merge.

## CHG-0004 T7 quoted-phrase scan completion

- The final quoted-string bypass was removed from forbidden-phrase scanning.
- Complete Source is checked with direct phrase matching.
- Single-quoted, double-quoted, embedded, commented, and assigned forbidden phrases are not exempt.
- Phrase positive controls use the same detector as real evidence-file scanning.
- Persistence scanner-rule literals are assembled at runtime without weakening Offline SQL checks.
- Scanner failure diagnostics expose only the path and category.
- Permanent Message test count remains 42.
- Full collection remains 322.
- Tasks remain 7 / 9.
- T8 remains separately authorized and has not started.

## CHG-0004 T8 capability verification

- CAP-XY-MESSAGE evidence paths are registered and verified.
- Evidence Candidate SHA: `49498e6f30944883c1a0a5a504932bbd02fc86de`.
- CAP-XY-MESSAGE status is verified.
- active_change is null.
- last_verified_commit records the Candidate SHA.
- Tasks are 8 / 9.
- T9 is the next executable task.
- PR #4 remains Draft, open, and unmerged.

## CHG-0004 T8 final-CI compatibility

- T8 final-CI shallow-checkout correction keeps evidence and verification state unchanged.
- The final CI correction handles depth-one pull-request merge checkouts.
- Complete repositories still require the Evidence Candidate object and strict ancestor verification.
- Missing Candidate history is accepted only when Git identifies the checkout as shallow.
- No Workflow, Runtime, Migration, Registry, Capability Specification, dependency, or evidence path was changed.
- CAP-XY-MESSAGE remains verified.
- Tasks remain 8 / 9.
- T9 remains the next executable task and has not started.
- PR #4 remains Draft, open, and unmerged.

## CHG-0004 final PR administration

- CHG-0004 final PR administration is complete.
- CHG-0004 status is `VERIFYING`.
- All nine tasks are complete.
- T9 Ready Candidate SHA is `1cc4de90e88f607ab30b475232c7fa7ef01b8f14`.
- CAP-XY-MESSAGE remains verified.
- PR #4 is Ready for review, open and unmerged.
- No Reviewer was manually requested.
- Auto-merge and merge remain unauthorized.
- CHG-0004 remains under `changes/active/` until the PR is merged.
- Merge requires separate explicit authorization against an exact PR HEAD.

## CHG-0005 T6 local reply runtime

- T6 implements the local deterministic reply package under `app/xianyu_system/reply/`.
- Migration `0004_xianyu_reply_boundary` introduces local Reply Template, Rule, Condition, and sanitized Audit projections after the verified Message boundary.
- CAP-XY-REPLY remains planned and unbound during T6; T8 is responsible for evidence-path registration and verification.
- There is still no real Xianyu access, message sending, browser profile use, WeCom integration, AI Provider integration, API/Web UI, worker loop, scheduler, credential resolver, dependency change, workflow change, Ready transition, reviewer request, auto-merge, or merge.

## CHG-0005 T7 permanent reply evidence

- T7 permanent Reply tests are implemented across Domain, Evaluator, Renderer, Mapper, Service, Persistence Contract, Security Contract, Import Safety, Migration, Runtime compatibility, Capability Registry planned-state assertions, and active acceptance.
- Tasks are now 7 / 9 and T8 capability evidence is the next executable task.
- CAP-XY-REPLY remains planned and unbound pending T8.
- No real Xianyu access, message sending, browser profile use, WeCom integration, AI Provider integration, API/Web UI, worker loop, scheduler, credential resolver, dependency change, workflow change, Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, or CHG-0006 was introduced.

## CHG-0005 T8 evidence candidate

- CAP-XY-REPLY is registered as `implementing` for the T8 Evidence Candidate.
- Exact implementation and test evidence paths are registered.
- `last_verified_commit` remains unset until the Candidate commit is verified and the Verification Record is created.
- Tasks remain 7 / 9 during Phase A; T8 is still the next task until Phase B completes.
- No runtime semantics, migration semantics, permanent tests, dependency, workflow, PR metadata, Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, or CHG-0006 was changed by the candidate registration.


## CHG-0005 T8 reply capability verification

- CAP-XY-REPLY evidence paths are registered and verified.
- Evidence Candidate SHA: `5724d164619c64e93295595b3acdd1429d24e3e0`.
- CAP-XY-REPLY status is verified.
- active_change is null.
- last_verified_commit records the Candidate SHA.
- Tasks are 8 / 9.
- T9 is the next executable task.
- PR #5 remains Draft, open, and unmerged.
- No Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, CHG-0006, real Xianyu access, message sending, WeCom integration, AI Provider integration, browser profile use, credential resolution, dependency change, or workflow change was performed.


## CHG-0005 final review preparation

- CHG-0005 status is `VERIFYING` for final PR review preparation.
- T1 through T8 are complete; T9 remains incomplete until the Ready transition and final administration record finish.
- CAP-XY-REPLY remains verified and frozen.
- PR #5 remains Draft until the Ready Candidate passes final CI.
- No Reviewer request, auto-merge, merge, close, archive, branch deletion, CHG-0006 creation, runtime expansion, dependency change, workflow change, real Xianyu access, message sending, WeCom integration, AI Provider integration, browser Profile access, or Credential access is authorized by this preparation state.


## CHG-0005 final PR administration

- CHG-0005 final PR administration is complete.
- CHG-0005 status is `VERIFYING`.
- All nine tasks are complete.
- T9 Ready Candidate SHA is `365cce3ef6574974c1cee1bb676fe8c1ad8ad4e3`.
- CAP-XY-REPLY remains verified.
- Evidence Candidate SHA is `5724d164619c64e93295595b3acdd1429d24e3e0`.
- PR #5 is Ready for review, open and unmerged.
- No Reviewer was manually requested.
- Auto-merge and merge remain unauthorized.
- CHG-0005 remains under `changes/active/` until the PR is merged.
- Merge requires separate explicit authorization against an exact PR HEAD.
- No close, source-branch deletion, archive, CHG-0006 creation, runtime expansion, migration semantic change, dependency change, workflow change, real Xianyu access, message sending, WeCom integration, AI Provider integration, browser Profile access, Credential access, Cookie, Token, Secret, Session Material, or real customer-data access occurred.


## Current verification record - CHG-0006 T8 Phase B

CAP-XY-PUBLISH evidence paths are registered and verified for the local deterministic Publish boundary.

Evidence Candidate SHA: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`

Verification commit: `51bfefb4ca63e2c7ac0128359da1f00c62ad37e9`

Candidate GitHub Actions result: quality push, quality pull_request, tests push, tests pull_request, security push, and security pull_request all completed successfully.

Registry status: verified

Active change: null

Last verified commit: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`

Tasks: 8 / 9

Next task: T9 Complete final PR administration

T9 is not authorized and has not started. PR #6 remains Draft, open, and unmerged. Verified does not authorize Ready, reviewer request, review submission, auto-merge, merge, archive, branch deletion, CHG-0007, real Xianyu access, listing publication, media upload, Credential handling, browser automation, external platform access, platform adapter, scheduler, worker loop, retry behavior, dependency change, or workflow change.

## CHG-0007 draft schedule boundary

CHG-0007-xianyu-schedule-boundary is open as DRAFT for governance review only. It proposes a narrow local deterministic Schedule boundary for one-time UTC publish scheduling. DRAFT does not authorize Runtime implementation, Registry binding, Migration work, real Xianyu access, browser automation, Playwright, Credential handling, recurring scheduling, WeCom, AI, or external platform side effects.


## CHG-0007 approval record

CHG-0007-xianyu-schedule-boundary is APPROVED by the project owner for ordered T1-T9 execution. The approval remains limited to local deterministic scheduling and does not authorize real Xianyu access, browser automation, Playwright, Credential handling, recurring scheduling, WeCom, AI, or CHG-0008.


## T2 terminology decision

Schedule Request means a local request to run exactly one Publish boundary call either immediately or at an explicit UTC run_at time. Trigger is IMMEDIATE or RUN_AT_UTC. Schedule Decision is the deterministic validation result. Dispatch is the local atomic claim of a due schedule. UTC is mandatory for all stored instants. Grace window is a finite misfire allowance in seconds; outside grace the item becomes MISFIRED and is not published. Cancellation is a terminal local state before claim.


## T3 safety boundary decision

CHG-0007 reuses xianyu_system.core.scheduler without modifying it. APScheduler MemoryJobStore is only an in-process wakeup adapter. Publish coupling is explicit through the existing local PublishService interface and never duplicates Publish validation or DTOs. No permissions, Credentials, browser Profile, Playwright, real Xianyu platform session, WeCom, AI, network request, Redis, Celery, or external queue is introduced.


## T4 deterministic decision rules

Validation accepts only IMMEDIATE and RUN_AT_UTC one-time schedules. run_at must be timezone-aware UTC when provided. Idempotency key and deterministic fingerprint prevent duplicates. Cancellation is allowed only before dispatch claim. Atomic claim prevents duplicate dispatch. Due schedules outside the finite grace window become MISFIRED. Any uncertain Publish result is recorded for manual review and does not retry automatically.


## T5 ownership and persistence decision

Schedule Repository is the business fact source. It owns schedule records and audit events. Lifecycle states are PENDING, CLAIMED, DISPATCHED, CANCELLED, MISFIRED, FAILED, and NEEDS_MANUAL_REVIEW. Persistence uses local SQLAlchemy tables in migration 0006. Concurrency uses atomic claim predicates. Failures are recorded as local audit facts. APScheduler never becomes the fact source.


## CHG-0007 T6 local Schedule Runtime

T6 implemented the approved local deterministic Schedule boundary: pure domain types, deterministic fingerprinting, validation, SQLAlchemy repository facts, local ScheduleService dispatch, APScheduler DateTrigger adapter, and migration 0006. It reuses PublishService explicitly and does not modify Core scheduler or Publish modules. No real Xianyu, browser, Playwright, Credential, WeCom, AI, Redis, Celery, recurring schedule, or external queue was added.
