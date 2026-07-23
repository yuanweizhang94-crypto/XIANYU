# CHG-0003 Proposal

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Purpose

Prepare a formally reviewable boundary for Xianyu account and Profile isolation.

## Target capability

- CAP-XY-ACCOUNT

## Current authorization

The project owner approved CHG-0003 for controlled, one-task-at-a-time execution.

T1 through T7 are complete.

The terminology, security, credential-handling, persistence, migration, runtime ownership, and module boundaries are finalized.

T8 is the next executable task and must be performed separately.

No T8 capability evidence work, capability binding, Ready-for-review, auto-merge, or merge is authorized in this execution.

## T6 correction

- The distinct Account Reference domain concept is now implemented.
- Profile-to-Account-Reference ownership is explicit and fail-closed.
- The one-table persistence projection remains unchanged.
- Database-level trim constraints now match the domain normalization boundary.
- Three existing Core unit-test files changed during T6 only to remove obsolete metadata and Migration assumptions.
- No permanent account test function was added.
- T7 remains the next executable task.
- T1-T6 are complete.
- T8/T9 are not started.
- PR #3 remains Draft, open, and unmerged.

## T7 correction

- Runtime account operations are tested with network, subprocess, and Home-directory access blocked.
- Contract tests no longer clear mappers, remove the account table from shared metadata, or evict account modules.
- Contract tests pass in both account persistence/security execution orders.
- Whitespace-only External Account Identifier and Credential Reference database writes are explicitly rejected.
- No runtime or Migration implementation changed.
- Test counts remain unchanged.
- T8 remains the next executable task.
- T1-T7 are complete.
- T8/T9 are not started.
- PR #3 remains Draft, open, and unmerged.

## T7 permanent test outcome

Permanent account-boundary coverage is complete.

- `tests/unit/test_account_domain.py` contains exactly 10 account domain tests.
- `tests/unit/test_account_service.py` contains exactly 7 account service tests.
- `tests/contract/test_account_persistence.py` contains exactly 7 account persistence and Migration contract tests.
- `tests/contract/test_account_security.py` contains exactly 4 account security-boundary contract tests.
- Total new permanent account tests: 28.
- The coverage verifies domain ownership, normalization, lifecycle rules, Account Service transactions, optimistic concurrency, Profile-scoped uniqueness, Repository behavior, Migration behavior, guarded downgrade, database constraints, sanitized errors, and absence of external integrations.
- No runtime, Migration, API, browser, Provider, Secure Storage, Scheduler, background-process, dependency, CI, Registry, or capability-specification change was made during T7.
- CAP-XY-ACCOUNT remains planned and unbound.
- T8 remains the next executable task.

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

## T6 implementation outcome

- The local domain model is implemented.
- A single SQLAlchemy relational projection is implemented.
- One concrete Repository and Account Service are implemented.
- UUID version 4 Profile Identifier generation is implemented.
- PENDING, ENABLED, and DISABLED local lifecycle states are implemented.
- Optimistic concurrency is implemented.
- The linear Alembic Revision `0002_xianyu_account_boundary` is implemented.
- No API, Worker process, browser integration, or Provider is implemented.
- No real Secret Material is added, accessed, persisted, or resolved.
- T7 has not started.

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
- No permanent T7 account coverage or capability binding before separate authorization and execution.

## Execution boundary

Only one unfinished task may be executed at a time.

This execution completes T6 only.

T7 must not begin in the same execution.

T7 may begin only in a separate execution after this commit is complete and pushed.
