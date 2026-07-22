# CHG-0002 Acceptance

Status: VERIFYING
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

The change is VERIFYING.

T1 through T15 are complete.

The final branch is pushed and the existing Draft PR #2 is open, targets main, and remains unmerged.

No unfinished task remains in CHG-0002.

CAP-CORE-CONFIG, CAP-CORE-DATABASE, and CAP-HEALTH-MONITOR remain verified and continue to record d11f1afc4564298e8c2709fdb80a41a491dbb1ea as their last verified commit.

The seven non-Core capabilities remain planned and unbound.

The active change remains under changes/active until an explicitly authorized merge and later archive transition.

Completing T15 does not authorize marking the pull request Ready, enabling auto-merge, merging the pull request, or starting CHG-0003.
