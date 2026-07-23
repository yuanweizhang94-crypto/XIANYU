# CAP-XY-ACCOUNT

## Purpose

Define the local Xianyu account boundary, Profile isolation model, and non-secret Account Reference evidence without accessing real accounts or external platforms.

## Current implementation change

- Active change: CHG-0003-xianyu-account-boundary
- Registry status: implementing
- Last verified commit: unset until T8 complete verification

## Registered implementation paths

- `app/xianyu_system/worker/account/__init__.py`
- `app/xianyu_system/worker/account/domain.py`
- `app/xianyu_system/worker/account/service.py`
- `app/xianyu_system/worker/account/persistence.py`
- `migrations/versions/0002_xianyu_account_boundary.py`

## Registered verification paths

- `tests/unit/test_account_domain.py`
- `tests/unit/test_account_service.py`
- `tests/unit/test_import_safety.py`
- `tests/contract/test_account_persistence.py`
- `tests/contract/test_account_security.py`
- `tests/contract/test_migrations.py`
- `tests/contract/test_core_runtime.py`
- `tests/contract/test_capability_registry.py`
- `changes/active/CHG-0003-xianyu-account-boundary/tests/test_acceptance.py`

## Implemented local boundary

- The local domain model contains Profile and AccountReference concepts.
- Profile Identifier generation uses UUID version 4 through the Python standard library.
- Local lifecycle states are PENDING, ENABLED, and DISABLED.
- The persistence boundary is a local SQLAlchemy projection.
- Account Service owns transaction coordination.
- Repository does not independently commit.
- Optimistic concurrency is enforced by row version.
- Alembic revision `0002_xianyu_account_boundary` is explicit and follows the Core baseline.
- Application startup does not automatically run migrations.
- No API, browser, Provider, Secure Storage, network, or real-account behavior is implemented.
- Secret Material is not saved or resolved.

## T8 evidence candidate

The registered evidence paths form the T8 Evidence Candidate for complete verification. The capability remains `implementing` and `last_verified_commit` remains unset until the candidate completes full verification and a separate verification-record commit records the candidate SHA.

## Requirements

- Keep Profile and AccountReference data local and non-secret.
- Keep the Account Service transaction boundary explicit.
- Keep persistence under the approved Core database and Alembic infrastructure.
- Keep evidence paths repository-relative, concrete files, safe, and duplicate-free.

## Failure behavior

- Fail closed on invalid Profile ownership, invalid lifecycle transition, stale update, duplicate ownership, and persistence boundary failures.
- Do not guess missing platform behavior.
- Do not fall back to cross-Profile credential or Secret Material reuse.

## Security boundaries

- Do not hold real Cookie, Token, Secret, customer data, or browser credentials.
- Do not bypass platform verification or risk controls.
- Do not log Secret Material or full Credential References.
- Use Synthetic Fixtures only in tests.

## Out of scope

- Real Xianyu login, Cookie or Token import, browser Profile loading, external network access, Credential Provider integration, Secure Storage integration, Scheduler Jobs, background workers, API routes, web UI, and real-account behavior remain out of scope.

## Verification

- Registry evidence paths are exact and safe.
- Permanent account tests cover domain, service, persistence, security, migration, core-runtime interaction, import safety, and active-change acceptance.
- T8 complete verification has not yet been recorded for this candidate.
