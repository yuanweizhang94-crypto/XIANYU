# CHG-0002 Core Application Design

Status: APPROVED
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

## Testing rules

* Application factory tests must create more than one application instance.
* Database tests must use a temporary SQLite path.
* Scheduler tests must prove that startup and shutdown are lifecycle-controlled.
* Configuration tests must use explicit overrides or isolated environment variables.
* Tests must not require network access.
* Tests must not depend on execution order.

## Non-goals for the preparation stage

* No dependency installation before T3.
* No runtime Core module implementation before T4.
* No database file or migration creation before the relevant approved task.
* No `/health` implementation before T10.
* No HTML template implementation before T11.
* No external platform or AI integration.
