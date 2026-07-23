# CHG-0003 Proposal

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Purpose

Prepare a formally reviewable boundary for Xianyu account and Profile isolation.

## Target capability

- CAP-XY-ACCOUNT

## Current authorization

The project owner approved CHG-0003 for controlled, one-task-at-a-time execution.

T1, T2, T3, T4, and T5 are complete.

The terminology, security, credential-handling, persistence, migration, runtime ownership, and module boundaries are finalized.

T6 is the next executable task and must be performed separately.

No runtime code, ORM code, Migration file, database mutation, API route, Worker process, provider integration, browser integration, capability binding, Ready-for-review, auto-merge, or merge is authorized in this execution.

## Goals

- Define account and Profile isolation terminology.
- Define synthetic configuration and validation boundaries.
- Define security, permission, lifecycle, and failure behavior.
- Define future acceptance criteria before runtime implementation.
- Preserve fail-closed behavior when account state or permission is uncertain.

## T2 terminology outcome

- Platform Account means the real external account.
- Account Reference means the repository-owned non-secret logical reference.
- Profile means the local isolation boundary and does not mean a browser profile.
- Profile Identifier is the canonical local identity.
- Account Alias is display-only metadata.
- External Account Identifier is optional untrusted reference metadata.
- Credential Reference is an opaque reference and never a secret value.
- Session Material is sensitive and remains outside the approved boundary.
- Profile-scoped State belongs to exactly one Profile.
- Isolation Boundary prohibits cross-Profile mutable-state or secret reuse.
- Synthetic Fixture is the only allowed test data category.

## T3 security outcome

- Secret Material is prohibited from repository and ordinary application persistence.
- Credential References are opaque, Profile-owned, and never contain secret values.
- Future Secret Material storage requires a Secure Storage Boundary.
- Future resolution requires exact Profile ownership, explicit purpose, explicit authorization, and a non-blocked risk state.
- Only RESOLVED plus AUTHORIZED may permit a future operation.
- Unknown, missing, unavailable, invalid, expired, revoked, verification-required, denied, or risk-blocked states fail closed.
- Sensitive logs, errors, traces, metrics, and audits must not contain Secret Material.
- Full Credential References and External Account Identifiers must not be logged.
- Secret Material ingress through source files, environment variables, command-line arguments, URLs, tests, databases, or PR text is prohibited.
- Rotation and revocation must not create fallback or cross-Profile reuse.
- Only Synthetic Fixtures are allowed in tests.

## T4 persistence outcome

- The existing CAP-CORE-DATABASE SQLite, SQLAlchemy, and Alembic infrastructure remains the only approved persistence boundary.
- Only minimal non-secret Profile and Account Reference metadata may be persisted.
- Credential References remain opaque, non-secret, and Profile-owned.
- Secret Material, browser state, and generic payload fields are prohibited.
- Persistence mutations require explicit Profile ownership, transactions, uniqueness protection, and concurrency-conflict protection.
- Future migrations remain explicit and application startup must not auto-migrate.
- Exact schema, ORM, lifecycle, indexes, retention, and downgrade implementation remain deferred to T5 and T6.
- T4 creates no Migration file, ORM model, table, Repository, API, or Worker.

## T5 runtime ownership outcome

- CAP-XY-ACCOUNT remains owned by the `worker.account` capability namespace.
- The future package path is `app/xianyu_system/worker/account/`.
- The future import namespace is `xianyu_system.worker.account`.
- T6 may create the minimal `domain.py`, `persistence.py`, and `service.py` modules under the approved package.
- `domain.py` owns pure domain concepts and invariants.
- `persistence.py` owns the SQLAlchemy relational projection and the single concrete account Repository.
- `service.py` owns account use cases and transaction coordination.
- Profile Identifier generation uses UUID version 4 through the Python standard library.
- Local lifecycle states are PENDING, ENABLED, and DISABLED.
- The account service owns logical transactions; the Repository must not independently commit.
- Credential References are opaque non-secret metadata only.
- No API, web UI, Scheduler Job, background Worker process, browser integration, Secure Storage Provider, Credential Provider, login, or external account validation is approved.
- T5 creates no runtime file, ORM model, Migration, database table, Repository, Service, API, or Worker.

## Non-goals

- No real Xianyu login.
- No real Cookie, Token, Secret, QR code, SMS code, account, customer, or browser data.
- No browser automation.
- No Playwright or Selenium.
- No runtime account worker.
- No database business tables or migrations.
- No API route.
- No external network request.
- No registry capability binding.
- No runtime implementation during the T5 runtime ownership boundary transition.
- No runtime implementation before T6 is separately authorized and executed.

## Execution boundary

Only one unfinished task may be executed at a time.

This execution completes T5 only.

T6 must not begin in the same execution.

T6 may begin only in a separate execution after this commit is complete and pushed.
