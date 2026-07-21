# CAP-HEALTH-MONITOR

## Purpose

Provide a read-only Core health boundary that reports local application status without connecting to real external services.

## Current implementation change

- Active change: CHG-0002-core-application.
- Registry status during implementation: implementing.
- Final status after acceptance: verified.

## Planned implementation paths

- `app/xianyu_system/api/health.py`
- `app/xianyu_system/api/router.py`
- `app/xianyu_system/application.py`
- `contracts/openapi.yaml` for the `/health` contract when T10 begins.

## Planned test paths

- `tests/unit/` for route and response behavior.
- `tests/contract/` for OpenAPI `/health` contract coverage.
- `changes/active/CHG-0002-core-application/tests/` for CHG-0002 acceptance coverage.

## Requirements

- Expose `/health` as a structured HTTP API response.
- Include only local Core health information that is safe to disclose.
- Avoid external network calls, real Xianyu checks, real WeCom checks, and AI provider calls.
- Keep route code free of direct database connection creation.

## Acceptance criteria

- `/health` returns structured health status.
- OpenAPI contains `/health`.
- Health checks do not access real external networks or accounts.
- `CAP-HEALTH-MONITOR` is updated to verified only after CHG-0002 implementation and validation are complete.

## Security boundaries

- Do not expose Cookie, Token, Secret, Password, account identifiers, customer data, or browser profile details.
- Do not bypass platform verification or risk controls.
- Do not call external platforms.

## Out of scope

- Xianyu account health.
- WeCom API health.
- AI provider health.
- Browser profile or Playwright health checks.
- Production observability stack integration.
