# CHG-0002 Acceptance

Status: IMPLEMENTING
Change ID: CHG-0002-core-application

## Final acceptance criteria

1. The application can be created through a documented application factory.
2. Multiple application instances can be created in one test process without shared-state pollution.
3. `GET /health` returns a structured health response.
4. OpenAPI includes the `/health` operation.
5. Typed configuration supports environment variables and explicit test overrides.
6. Logs do not expose Secret, Token, Cookie, Password, or equivalent sensitive values.
7. SQLite engine and connection creation are managed through one infrastructure module.
8. SQLite connections enable WAL mode.
9. SQLAlchemy sessions are created and managed through one infrastructure boundary.
10. An Alembic baseline configuration and initial migration can be executed successfully.
11. Database tests use temporary directories and do not write to production or user data paths.
12. Importing application modules does not create a database file.
13. Importing application modules does not start the scheduler.
14. The scheduler starts through the application lifespan.
15. The scheduler shuts down through the application lifespan.
16. A minimal home page renders through Jinja2.
17. The HTMX static resource boundary exists and is served through the web module.
18. Tests do not access real external networks.
19. Tests and runtime initialization do not access real accounts, Cookies, Tokens, Secrets, or browser profiles.
20. CHG-0002 contains no Xianyu, WeCom, AI Provider, Playwright, or other external business integration.
21. `CAP-CORE-CONFIG` is marked `verified` only after implementation and complete validation.
22. `CAP-CORE-DATABASE` is marked `verified` only after implementation and complete validation.
23. `CAP-HEALTH-MONITOR` is marked `verified` only after implementation and complete validation.
24. All permanent tests and CHG-0002 active-change acceptance tests pass.
25. Ruff, Mypy, repository verification, and all required GitHub Actions pass.

## Current preparation-stage status

The change is IMPLEMENTING.

T1 through T11 are complete after the Jinja2 home page, local static resource, HTMX asset, package-data, isolation, and security-boundary tests pass.

T12 Add unit, contract and active-change acceptance tests is the next task.

GET / renders a minimal server-rendered Core page and is excluded from OpenAPI.

HTMX is served locally through the web static boundary and performs only a user-triggered GET /health request.

No business page, form submission, external service call, database write, migration, or scheduler job is implemented.

The three Core capabilities remain implementing.
