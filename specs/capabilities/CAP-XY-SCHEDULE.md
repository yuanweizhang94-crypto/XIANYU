# CAP-XY-SCHEDULE

## Purpose

Provide a local deterministic one-time Schedule boundary for immediate or explicit UTC `run_at` dispatch into the already verified local Publish boundary.

## Registry status

Registry status: verified

Active change: null

Last verified commit: `0d9cfacedc1947e518d990151225ec8a15540f76`

This verified state records Evidence Candidate `0d9cfacedc1947e518d990151225ec8a15540f76` only for the local deterministic Schedule boundary. It does not mean real Xianyu scheduled publishing has occurred, and it does not authorize platform access.

## Requirements

- Accept only one-time `IMMEDIATE` or `RUN_AT_UTC` schedule requests.
- Require timezone-aware UTC instants for all persisted schedule times.
- Persist Schedule Repository business facts and sanitized audit events through migration `0006_xianyu_schedule_boundary`.
- Use deterministic fingerprints for idempotency replay and conflict detection.
- Allow cancellation only before dispatch claim.
- Atomically claim due schedules before invoking the existing local `PublishService`.
- Move schedules outside the finite grace window to `MISFIRED` without calling Publish.
- Route uncertain or non-ready local Publish outcomes to manual review without retrying.
- Reuse `xianyu_system.core.scheduler` and APScheduler `DateTrigger` only as an in-process wakeup adapter.

## Implementation evidence

- `app/xianyu_system/schedule/__init__.py`
- `app/xianyu_system/schedule/domain.py`
- `app/xianyu_system/schedule/fingerprint.py`
- `app/xianyu_system/schedule/validation.py`
- `app/xianyu_system/schedule/persistence.py`
- `app/xianyu_system/schedule/service.py`
- `app/xianyu_system/schedule/apscheduler_adapter.py`
- `migrations/versions/0006_xianyu_schedule_boundary.py`

## Verification evidence

- `tests/unit/test_schedule_domain.py`
- `tests/unit/test_schedule_fingerprint.py`
- `tests/unit/test_schedule_validation.py`
- `tests/unit/test_schedule_service.py`
- `tests/unit/test_schedule_apscheduler_adapter.py`
- `tests/unit/test_import_safety.py`
- `tests/contract/test_schedule_persistence.py`
- `tests/contract/test_schedule_security.py`
- `tests/contract/test_migrations.py`
- `tests/contract/test_capability_registry.py`
- `changes/archive/CHG-0007-xianyu-schedule-boundary/tests/test_acceptance.py`

## Scenarios

- Schedule an immediate local Publish boundary evaluation from synthetic fixtures.
- Schedule a single explicit UTC `run_at` local Publish boundary evaluation.
- Replay an identical idempotency key and fingerprint without creating duplicate facts.
- Detect idempotency conflicts when the same key carries different normalized semantics.
- Cancel a pending schedule before claim.
- Mark overdue schedules outside grace as `MISFIRED`.
- Dispatch ready local Publish decisions as `DISPATCHED`; send non-ready decisions to manual review.

## Failure behavior

- Invalid shape or values return sanitized local decisions.
- Persistence failures fail closed to manual review and never report dispatched success.
- Empty downgrade is allowed only for local schedule tables; non-empty downgrade fails closed.
- APScheduler is never the business fact source.

## Security boundaries

- No real Cookie, Token, Secret, customer data, browser credential, browser Profile, or Session Material is accepted or stored.
- No real Xianyu login, listing publication, message operation, media upload, browser automation, Playwright, WeCom, AI Provider, Redis, Celery, external queue, HTTP client, WebSocket, or external platform side effect is implemented.
- No recurring schedule, CRON, interval schedule, distributed scheduler, persistent APScheduler JobStore, or automatic retry loop is implemented.

## Out of scope

- Real Xianyu platform integration.
- Real scheduled publication.
- Browser or Playwright automation.
- Credential handling or browser Profile management.
- Recurring schedules, calendar rules, user timezone UI, Redis, Celery, or distributed scheduling.
- WeCom, AI, operations console, or CHG-0008 creation.

## Verification

- The capability is registered as verified for the local deterministic Schedule boundary.
- `last_verified_commit` records the exact Evidence Candidate SHA `0d9cfacedc1947e518d990151225ec8a15540f76`.
- GitHub Actions for the Candidate completed successfully for quality, tests, and security on push and pull_request events.


## Post-merge archive verification

CHG-0007 is archived after PR #8 merged via normal two-parent merge commit `4da2dbea8da9ec80819d04906e987e5856653ae9`. CAP-XY-SCHEDULE remains verified only for the local deterministic Schedule boundary. The acceptance evidence path now points to `changes/archive/CHG-0007-xianyu-schedule-boundary/tests/test_acceptance.py`, and the historical acceptance blob is `d5881c74aef833c32e87fce7b40ec39d5ef685e1`.
