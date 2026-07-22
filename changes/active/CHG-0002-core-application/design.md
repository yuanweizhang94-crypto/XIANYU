# CHG-0002 Core Application Design

Status: VERIFYING
Change ID: CHG-0002-core-application

## Design goal

CHG-0002 establishes a runnable and testable modular-monolith Core.

The Core provides infrastructure boundaries for future Xianyu workers, fixed reply rules, listing workflows, scheduling, WeCom adapters, and AI adapters without implementing those business capabilities in this change.

## Locked technology direction

- Python 3.12.
- FastAPI.
- Pydantic Settings.
- Jinja2.
- HTMX.
- SQLite in WAL mode.
- SQLAlchemy.
- Alembic.
- APScheduler.
- Structured redacted logging.
- Modular-monolith Core.
- Local single-machine execution.

This technology direction is approved for CHG-0002 only within the scope and boundaries recorded in the active change.

## Target directory layout

```text
app/xianyu_system/
|-- __init__.py
|-- main.py
|-- application.py
|-- core/
|   |-- __init__.py
|   |-- config.py
|   |-- logging.py
|   |-- database.py
|   `-- scheduler.py
|-- api/
|   |-- __init__.py
|   |-- router.py
|   `-- health.py
|-- web/
|   |-- __init__.py
|   |-- router.py
|   |-- templates/
|   |   |-- base.html
|   |   `-- index.html
|   `-- static/
|       |-- styles.css
|       `-- vendor/
|           |-- htmx.min.js
|           `-- htmx.LICENSE.txt
`-- domain/
    `-- __init__.py
```

## Responsibility rules

1. `main.py` provides the application entry point only.
2. `application.py` owns the application factory and lifespan coordination.
3. `core/config.py` is the single typed configuration boundary.
4. `core/logging.py` is the single logging configuration and redaction boundary.
5. `core/database.py` is the single database engine and session infrastructure boundary.
6. `core/scheduler.py` owns scheduler creation, startup, and shutdown.
7. `api/` contains HTTP API boundaries only.
8. `web/` contains server-rendered pages, templates, and static resource boundaries only.
9. `domain/` must not depend on FastAPI, SQLAlchemy, browser automation, or external platforms.
10. Routes must not create database engines or direct database connections.
11. Module import must not start the scheduler.
12. Module import must not create database files.
13. Module import must not access an external network.
14. Module import must not read real platform credentials.
15. The application must support repeated creation in the same test process.
16. Tests must use temporary directories and temporary databases.
17. The scheduler must start and stop through the application lifespan.
18. Logging must redact Secret, Token, Cookie, Password, and equivalent sensitive fields.
19. Global non-replaceable runtime singletons are prohibited.
20. CHG-0002 must not implement Xianyu, WeCom, or AI business logic.

## Capability boundaries

* `CAP-CORE-CONFIG` owns typed settings and safe environment override behavior.
* `CAP-CORE-DATABASE` owns SQLite WAL, SQLAlchemy engine and session infrastructure, and Alembic baseline support.
* `CAP-HEALTH-MONITOR` owns `/health`, the OpenAPI health contract, and read-only runtime health reporting.

## Import-side-effect rules

Importing any Core module must not:

* Start a web server.
* Start the scheduler.
* Create a database file.
* Execute a migration.
* Open a browser.
* Access Xianyu, WeCom, AI, or any other external service.
* Read or log real credentials.

## T4 implementation decision

- `application.py` owns the reusable FastAPI application factory.
- T4 initially introduced the no-op lifespan.
- T6 extends the project lifespan with logging startup and shutdown while preserving custom lifespan composition.
- T7 extends the project lifespan with database initialization after logging startup and database disposal before logging shutdown.
- `create_application()` accepts an optional lifespan handler for isolated tests and later approved infrastructure integration.
- `main.py` exposes one ASGI entry application created by the factory.
- Application creation does not start a server, scheduler, database, migration, browser, or external client.
- No API or web route is registered in T4.

## T5 implementation decision

- `ApplicationSettings` is the single typed configuration model.
- Supported sources are safe defaults, `XIANYU_` environment variables, and explicit constructor overrides.
- Explicit constructor overrides have higher priority than environment variables.
- Environment variables have higher priority than defaults.
- Settings are immutable after validation.
- `.env` files are not loaded automatically.
- Configuration instantiation does not create directories, database files, logs, or network clients.
- The application factory stores the resolved settings instance in `app.state.settings`.
- T5 does not implement logging, database connections, migrations, scheduler behavior, API routes, or web routes.

## T6 implementation decision

- `core/logging.py` owns structured JSON formatting, sensitive-value redaction, logger configuration, and managed-handler shutdown.
- Logging uses the Python standard library only.
- Each application receives a distinct non-propagating named logger during FastAPI lifespan startup.
- Logging is not configured during module import or application construction.
- The application logger is stored in `app.state.logger`.
- Startup and shutdown are emitted as structured lifecycle events.
- Project-managed handlers are removed and closed at lifespan shutdown.
- Root logging configuration and caller-owned handlers are not modified.
- No log file or log directory is created.
- T6 does not implement database, migration, scheduler, API, or web behavior.

## T7 implementation decision

- `core/database.py` is the single SQLite and SQLAlchemy infrastructure boundary.
- SQLite URLs are created with SQLAlchemy `URL.create()` and the `sqlite+pysqlite` driver.
- Engine creation is lazy and does not connect or create a database file.
- Explicit database initialization creates the parent directory, opens the database, enables and verifies WAL, and validates connectivity.
- SQLite foreign keys are enabled and busy timeout is set to 5000 milliseconds for each project-engine connection.
- `DatabaseResources` owns the resolved path, Engine, and Session factory for one application instance.
- `open_session()` closes sessions but does not automatically commit.
- `Base.metadata` is currently empty and no business schema is created.
- Database initialization and disposal are controlled by the FastAPI lifespan.
- Each application receives an independent Engine and Session factory.
- T7 does not introduce Alembic files, migrations, scheduler behavior, API routes, web routes, or business tables.

## T8 implementation decision

- `alembic.ini` and `migrations/` establish the repository migration environment.
- `Base.metadata` is Alembic's only target metadata.
- The first revision is the deterministic empty baseline `0001_core_baseline`.
- The baseline creates no business tables and writes no business data.
- Programmatic migrations share the existing application Engine connection through Alembic `Config.attributes`.
- Standalone CLI migrations require an explicit `-x database_path=...` argument and use the unified database infrastructure.
- No database URL or local machine path is stored in Alembic configuration.
- Alembic does not install or modify Python logging configuration.
- Application startup initializes SQLite infrastructure but does not automatically upgrade migrations.
- Migration execution is an explicit administrative action.
- `Base.metadata` remains empty after T8.
- The only database table produced by applying the baseline is Alembic's own version table.
- T8 does not implement scheduler, health API, web routes, or business schema.


## T9 implementation decision

- `core/scheduler.py` is the single scheduler infrastructure boundary.
- The scheduler uses APScheduler 3.x `BackgroundScheduler`.
- Scheduler state is process-local and uses APScheduler `MemoryJobStore` only.
- Scheduler timezone is UTC through `SCHEDULER_TIMEZONE`.
- Module import does not create, start, or register scheduler jobs.
- Application lifespan creates and starts one scheduler after logging and database initialization.
- The scheduler is stored on `app.state.scheduler` only while the application lifespan is active.
- Custom lifespan startup runs after the scheduler is ready, and custom lifespan shutdown runs before scheduler shutdown.
- Application shutdown closes the scheduler before database disposal and before logging handler cleanup.
- Scheduler shutdown failures do not skip database disposal or logging cleanup.
- T9 registers no jobs, creates no scheduler database table, adds no migration revision, and does not implement scheduled publishing business logic.
- `CAP-XY-SCHEDULE` remains planned and unbound because the T9 scheduler is infrastructure only.
- T9 does not implement health API, web routes, templates, static assets, or business schema.

## T10 implementation decision

- `api/health.py` owns the read-only Core health models, local probes, aggregation, and `GET /health` route.
- `api/router.py` is the HTTP API aggregation boundary.
- The application factory registers the Core API router once per application instance.
- A healthy response returns HTTP 200 with overall status `ok`.
- A local component failure returns HTTP 503 with overall status `degraded`.
- Database health uses the existing application Engine for `SELECT 1` and `PRAGMA journal_mode`; it does not create an Engine, write data, or run migrations.
- Scheduler health reads only running state, job count, and UTC timezone; it does not start, stop, or modify jobs.
- Health responses expose no database path, exception details, credentials, account identifiers, customer data, or browser information.
- Health checks do not access Xianyu, WeCom, AI providers, browsers, or any external network.
- `contracts/openapi.yaml` defines the `/health` operation and response schemas.
- T10 does not implement web pages, Jinja2 templates, HTMX resources, business API routes, or external integrations.

## T11 implementation decision

- `web/router.py` owns the server-rendered home route, per-application Jinja2 template environment, and local static-resource registration.
- The home page is `GET /` and is excluded from OpenAPI.
- Templates and static files are resolved relative to the installed `xianyu_system.web` package rather than the current working directory.
- Each application receives an independent `Jinja2Templates` instance.
- Static resources are served from `/static` with directory indexes disabled and symbolic-link following disabled.
- `base.html` provides the HTML shell, local stylesheet reference, and locally vendored HTMX script reference.
- `index.html` displays only safe application title, version, and environment values.
- The only HTMX interaction is a user-triggered read-only `GET /health`.
- HTMX 2.0.10 is vendored locally with its license and verified SHA-384 digest.
- No CDN, Node package manager, frontend build system, form submission, authentication, database query, scheduler mutation, migration, or external request is introduced.
- Runtime OpenAPI remains limited to `/health`.
- T11 does not implement business pages, business APIs, domain modules, Xianyu, WeCom, AI, or browser automation.


## T12 implementation decision

- T12 adds permanent executable evidence without changing Core runtime behavior.
- Unit import-safety tests verify that importing Core modules does not create database files, start the scheduler, configure root logging, create log files, or attempt external network access.
- Core runtime contract tests exercise the application factory, lifespan startup and shutdown, SQLite WAL resources, empty SQLAlchemy metadata, scheduler lifecycle, OpenAPI health surface, local web surface, multiple concurrent application instances, and repeated lifecycle isolation.
- Distribution contract tests build a wheel from the approved source, verify packaged templates and static assets, validate the vendored HTMX bytes and license, install the wheel into an isolated target directory, and smoke-test `/`, `/health`, and local static assets from outside the source tree.
- Security-boundary contract tests use synthetic credential-like environment values, block socket connections, verify read-only HTTP methods, scan first-party web assets for external or mutating dependencies, and confirm no external business integration or scheduler jobs exist.
- Active-change acceptance tests now include explicit final acceptance evidence for all 25 CHG-0002 final criteria.
- These tests do not introduce skips, xfails, sleeps, real network clients, external service credentials, browser profiles, or unapproved dependencies.
- T12 does not modify runtime modules, OpenAPI contracts, specs, migrations, project dependencies, or GitHub workflow definitions.
- T12 does not mark Core capabilities as verified; capability registry implementation paths and verification metadata remain deferred to T13.
- T12 does not implement Xianyu, WeCom, AI Provider, Playwright, scheduled publishing, business routes, business pages, or database business schema.


## T13 implementation decision

- T13 registers exact implementation and verification file paths for `CAP-CORE-CONFIG`, `CAP-CORE-DATABASE`, and `CAP-HEALTH-MONITOR`.
- Registry paths use repository-relative POSIX syntax and point only to existing files.
- Primary implementation ownership remains separated across configuration, database, and health boundaries.
- Shared application-factory and integrated contract paths may appear under more than one Core capability where they provide real cross-capability evidence.
- Core scheduler infrastructure is not registered as `CAP-XY-SCHEDULE` business implementation.
- All three Core capabilities remained `implementing` and bound to `CHG-0002-core-application` until T14 verification.
- `last_verified_commit` remained unset until T14 complete verification.
- The seven non-Core capabilities remain planned, unbound, and without implementation or test paths.
- T13 changes registry evidence and documentation only; it does not change application runtime behavior.

## T14 verification decision

- Candidate commit `d11f1afc4564298e8c2709fdb80a41a491dbb1ea` was verified before any verification-state metadata was changed.
- Complete unit, contract, distribution, security, active-change acceptance, warning-mode, order-independence, Ruff, Mypy, repository, migration, OpenAPI, HTMX, and artifact checks passed.
- `CAP-CORE-CONFIG`, `CAP-CORE-DATABASE`, and `CAP-HEALTH-MONITOR` are now `verified`.
- Each verified capability records `d11f1afc4564298e8c2709fdb80a41a491dbb1ea` as `last_verified_commit`.
- Verified capabilities clear their registry `active_change` field.
- CHG-0002 moves from `IMPLEMENTING` to `VERIFYING` while final Draft PR administration remains incomplete.
- The seven non-Core capabilities remain planned and unbound.
- `CAP-XY-SCHEDULE` remains planned because Core scheduler lifecycle infrastructure does not implement Xianyu scheduling behavior.
- T14 changes verification metadata, tests, and documentation only; no application runtime, contract, migration, dependency, or workflow behavior changes.

## Testing rules

* Application factory tests must create more than one application instance.
* Database tests must use a temporary SQLite path.
* Scheduler tests must prove that startup and shutdown are lifecycle-controlled.
* Configuration tests must use explicit overrides or isolated environment variables.
* Tests must not require network access.
* Tests must not depend on execution order.

## Non-goals for the preparation stage

* No dependency installation before T3.
* T4 creates only `application.py` and `main.py`.
* Configuration, logging, database, scheduler, API, and web modules are introduced only in their approved tasks.
* No database file or migration creation before the relevant approved task.
* No `/health` implementation before T10.
* No HTML template implementation before T11.
* No external platform or AI integration.
