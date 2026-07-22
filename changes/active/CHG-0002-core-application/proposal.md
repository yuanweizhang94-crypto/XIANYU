# CHG-0002 Core Application Proposal

Status: VERIFYING
Change ID: CHG-0002-core-application

## Problem

The repository currently contains governance, specifications, validation scripts, tests, and CI, but it does not contain a runnable Core application.

Later Xianyu workers, fixed reply rules, listing workflows, scheduling, WeCom integration, and AI adapters require a stable local application foundation before business capabilities are implemented.

## Goal

Establish a local, single-machine, modular-monolith Core application skeleton.

The Core must provide stable boundaries for application creation, typed configuration, redacted structured logging, SQLite and SQLAlchemy infrastructure, Alembic migrations, scheduler lifecycle management, health reporting, and a minimal server-rendered web boundary.

## In Scope

- FastAPI application factory.
- Pydantic Settings configuration entry point.
- Structured and redacted logging.
- SQLite WAL connection infrastructure.
- SQLAlchemy engine and session infrastructure.
- Alembic migration baseline.
- APScheduler lifecycle skeleton.
- Structured health API.
- Jinja2 page skeleton.
- HTMX static resource boundary.
- Tests and OpenAPI contract updates.
- Local single-machine execution.
- Modular-monolith Core boundaries.

## Out of Scope

- Real Xianyu login.
- Cookie import.
- Browser profiles.
- Xianyu WebSocket connections.
- Xianyu message receiving or sending.
- Fixed reply business rules.
- Product template business logic.
- Product publishing.
- Playwright browser automation.
- Scheduled publishing business logic.
- WeCom API integration.
- AI Provider integration.
- Real customer data.
- Multi-account worker implementation.
- CAPTCHA or face-verification handling.
- Platform risk-control bypass.
- Production deployment.
- Redis.
- Celery.
- PostgreSQL.
- React frontend separation.
- Docker orchestration.

## Risks

- Introducing unnecessary abstractions before business requirements exist.
- Duplicating responsibilities across configuration, database, API, web, and scheduler modules.
- Misusing SQLite concurrency or connection lifecycle.
- Starting multiple scheduler instances.
- Creating database files or starting services during module import.
- Polluting tests with real local files.
- Exposing sensitive configuration through logs.

## Rollback

Revert the independent CHG-0002 pull request to remove the Core application skeleton.

Rollback must preserve the CHG-0001 governance baseline and its archived historical evidence.
