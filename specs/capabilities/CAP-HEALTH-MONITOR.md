# CAP-HEALTH-MONITOR

## Purpose

Provide a read-only Core health boundary that reports local application status without connecting to real external services.

## Current implementation change

- Active change: none; verification recorded by CHG-0002-core-application T14.
- Registry status: verified.
- Last verified commit: `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.

## Registered implementation paths

- `app/xianyu_system/api/health.py`
- `app/xianyu_system/api/router.py`
- `app/xianyu_system/application.py`
- `contracts/openapi.yaml`

## Registered verification paths

- `tests/unit/test_health.py`
- `tests/unit/test_application_factory.py`
- `tests/unit/test_import_safety.py`
- `tests/contract/test_health_openapi.py`
- `tests/contract/test_core_runtime.py`
- `tests/contract/test_distribution.py`
- `tests/contract/test_security_boundary.py`
- `changes/archive/CHG-0002-core-application/tests/test_acceptance.py`

## Requirements

- Expose `/health` as a structured HTTP API response.
- Include only local Core health information that is safe to disclose.
- Avoid external network calls, real Xianyu checks, real WeCom checks, and AI provider calls.
- Keep route code free of direct database connection creation.
- Do not run migrations or write database data from health checks.
- Do not start, stop, or mutate scheduler jobs from health checks.

## T10 implementation decision

- Implementation files:
  - `app/xianyu_system/api/health.py`
  - `app/xianyu_system/api/router.py`
  - `app/xianyu_system/application.py`
- Contract:
  - `contracts/openapi.yaml`
- Endpoint:
  - `GET /health`
- Healthy HTTP status:
  - `200`
- Degraded HTTP status:
  - `503`
- Health sources:
  - current application settings
  - existing `DatabaseResources`
  - existing `BackgroundScheduler`
- Database probe:
  - `SELECT 1`
  - `PRAGMA journal_mode`
- Scheduler probe:
  - running state
  - job count
  - UTC timezone
- Health collection is read-only.
- No external service checks are performed.
- No database path, exception text, credentials, account identifiers, or customer data are exposed.
- Application factory registers the API router.
- Capability remained `implementing` until T14 verification.

## T13 registry decision

- The health capability now records the health models and route, API aggregation boundary, application router registration, and OpenAPI contract.
- Verification paths cover unit health behavior, runtime OpenAPI, import safety, integrated runtime behavior, installed-package behavior, external-network blocking, sensitive-data boundaries, and active-change acceptance.
- Database, scheduler, and web implementation files are not claimed as health-owned implementation paths.
- The capability remained `implementing` until T14 verification.
- `last_verified_commit` remained unset until T14 complete verification.

## T14 verification decision

- Complete local verification passed for candidate commit `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.
- The registry status is now `verified`.
- The capability is no longer bound through `active_change`.
- `last_verified_commit` is `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.
- Verification covers the read-only `GET /health` endpoint, 200 and 503 behavior, runtime OpenAPI, local database and scheduler probes, and sensitive-data boundaries.
- No external service health check, database write, migration, scheduler mutation, account lookup, or customer-data exposure is included.

## Acceptance criteria

- `/health` returns structured health status.
- OpenAPI contains `/health`.
- Healthy local Core infrastructure returns HTTP 200.
- Degraded local Core infrastructure returns HTTP 503.
- Health checks do not access real external networks or accounts.
- `CAP-HEALTH-MONITOR` is updated to verified only after CHG-0002 implementation and validation are complete.

## Security boundaries

- Do not expose Cookie, Token, Secret, Password, account identifiers, customer data, database paths, exception details, or browser profile details.
- Do not bypass platform verification or risk controls.
- Do not call external platforms.

## Out of scope

- Xianyu account health.
- WeCom API health.
- AI provider health.
- Browser profile or Playwright health checks.
- Production observability stack integration.
