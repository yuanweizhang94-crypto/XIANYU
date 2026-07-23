# CHG-0003 Proposal

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Purpose

Prepare a formally reviewable boundary for Xianyu account and Profile isolation.

## Target capability

- CAP-XY-ACCOUNT

## Current authorization

The project owner approved CHG-0003 for controlled, one-task-at-a-time execution.

T1, T2, T3, and T4 are complete.

The terminology, security, credential-handling, and principle-level persistence and migration boundaries are finalized.

T5 is the next executable task and must be performed separately.

No runtime ownership implementation, ORM code, Migration file, database mutation, provider integration, account access, browser integration, capability binding, Ready-for-review, auto-merge, or merge is authorized.

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
- No runtime implementation during the T4 persistence boundary transition.
- No runtime implementation before T5 has been completed and its ownership decisions have been formally recorded.

## Execution boundary

Only one unfinished task may be executed at a time.

This execution completes T4 only.

T5 must not begin in the same execution.

Runtime implementation remains prohibited until T5 is complete and its ownership decisions are recorded.
