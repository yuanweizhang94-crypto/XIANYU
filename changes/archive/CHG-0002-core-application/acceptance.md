# CHG-0002 Acceptance

Status: ARCHIVED
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

## Archived status

CHG-0002 is ARCHIVED.

PR #2 is merged.

The archived change exists only under changes/archive/.

Its dedicated tests are preserved for audit and are not collected by default.

## Merge and archive record

PR #2 was merged into main.

Merge commit: `e2d41e0cc392ae0298688c01147e983317c7e1df`.

Merged feature head: `8180d67788c304548c1ad541011317ca41ab95cb`.

CHG-0002 is archived after successful merge.

The three Core capabilities remain verified.

Their `last_verified_commit` remains `d11f1afc4564298e8c2709fdb80a41a491dbb1ea`.

Archiving CHG-0002 does not change runtime behavior.

Archiving does not reverify capabilities.

Archiving does not authorize CHG-0003 implementation.
