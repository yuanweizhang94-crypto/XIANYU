# CHG-0002 Core Application Design

Status: IMPLEMENTING
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
|   `-- static/
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
* Configuration, logging, database, scheduler, API, and web modules remain deferred to their approved tasks.
* No database file or migration creation before the relevant approved task.
* No `/health` implementation before T10.
* No HTML template implementation before T11.
* No external platform or AI integration.
