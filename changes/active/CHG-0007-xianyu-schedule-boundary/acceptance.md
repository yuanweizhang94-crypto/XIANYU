# CHG-0007 Acceptance

Status: VERIFYING
Change ID: CHG-0007-xianyu-schedule-boundary

## Draft acceptance gates

1. Exactly one Active Change exists: CHG-0007-xianyu-schedule-boundary.
2. proposal.md, design.md, tasks.md, and acceptance.md are DRAFT.
3. Exactly nine tasks exist.
4. Completed tasks are 0 / 9.
5. next_task is null while status is DRAFT.
6. CAP-XY-SCHEDULE remains planned and unbound.
7. app/xianyu_system/schedule does not exist in DRAFT.
8. Migration 0006 does not exist in DRAFT.
9. Core scheduler remains unchanged.
10. Capability counts remain planned = 3 and verified = 7.
11. No real Xianyu access, browser, Playwright, Credential, WeCom, AI, Redis, Celery, recurring schedule, or external side effect is introduced.

## Final acceptance target

CHG-0007 is complete only after T1-T9, local deterministic Schedule Runtime, tests, CAP-XY-SCHEDULE evidence, PR Ready, merge, post-merge archive, archive CI, and safe branch cleanup are complete.


## T1 approval record

This instruction is the explicit project-owner authorization for CHG-0007 T1 through T9, executed in order.

T6 may implement only the approved local deterministic Schedule boundary. It does not authorize real Xianyu access, browser automation, Playwright, Credential handling, WeCom, AI, operations-console work, recurring schedules, Redis, Celery, or external queues.

Merge, archive, and branch deletion remain gated by the later exact CI, PR, merge, post-merge, and archive checks in this change.


## T2 terminology decision

Schedule Request means a local request to run exactly one Publish boundary call either immediately or at an explicit UTC run_at time. Trigger is IMMEDIATE or RUN_AT_UTC. Schedule Decision is the deterministic validation result. Dispatch is the local atomic claim of a due schedule. UTC is mandatory for all stored instants. Grace window is a finite misfire allowance in seconds; outside grace the item becomes MISFIRED and is not published. Cancellation is a terminal local state before claim.


## T3 safety boundary decision

CHG-0007 reuses xianyu_system.core.scheduler without modifying it. APScheduler MemoryJobStore is only an in-process wakeup adapter. Publish coupling is explicit through the existing local PublishService interface and never duplicates Publish validation or DTOs. No permissions, Credentials, browser Profile, Playwright, real Xianyu platform session, WeCom, AI, network request, Redis, Celery, or external queue is introduced.


## T4 deterministic decision rules

Validation accepts only IMMEDIATE and RUN_AT_UTC one-time schedules. run_at must be timezone-aware UTC when provided. Idempotency key and deterministic fingerprint prevent duplicates. Cancellation is allowed only before dispatch claim. Atomic claim prevents duplicate dispatch. Due schedules outside the finite grace window become MISFIRED. Any uncertain Publish result is recorded for manual review and does not retry automatically.


## T5 ownership and persistence decision

Schedule Repository is the business fact source. It owns schedule records and audit events. Lifecycle states are PENDING, CLAIMED, DISPATCHED, CANCELLED, MISFIRED, FAILED, and NEEDS_MANUAL_REVIEW. Persistence uses local SQLAlchemy tables in migration 0006. Concurrency uses atomic claim predicates. Failures are recorded as local audit facts. APScheduler never becomes the fact source.


## T6 implementation record

T6 implemented the approved local deterministic Schedule boundary: pure domain types, deterministic fingerprinting, validation, SQLAlchemy repository facts, local ScheduleService dispatch, APScheduler DateTrigger adapter, and migration 0006. It reuses PublishService explicitly and does not modify Core scheduler or Publish modules. No real Xianyu, browser, Playwright, Credential, WeCom, AI, Redis, Celery, recurring schedule, or external queue was added.


## T7 permanent test evidence

T7 added permanent unit, contract, security, migration, import-safety, and active-change acceptance coverage for the local deterministic Schedule boundary. The permanent evidence covers Schedule domain normalization, deterministic fingerprinting, validator fail-closed behavior, ScheduleService idempotency, conflict, cancellation, dispatch, misfire behavior, APScheduler DateTrigger registration through the existing Core scheduler, schedule table registration, migration lineage, offline SQL, and absence of real platform or integration side effects. CAP-XY-SCHEDULE remains planned and unbound until T8 evidence binding.


## T8 Phase A evidence candidate record

CAP-XY-SCHEDULE is registered as `implementing` for the Evidence Candidate. Exact implementation and test evidence paths are bound in `specs/CAPABILITY_REGISTRY.yaml` and documented in `specs/capabilities/CAP-XY-SCHEDULE.md`. `last_verified_commit` remains null until this Candidate commit completes local and GitHub Actions verification. Tasks remain 7 / 9 while Phase A is in progress; T8 is still the next task until Phase B records the verified Candidate SHA.


## T8 Phase B verification record

CAP-XY-SCHEDULE evidence paths are registered and verified. Evidence Candidate SHA: `0d9cfacedc1947e518d990151225ec8a15540f76`. Candidate GitHub Actions for quality, tests, and security on push and pull_request events completed successfully. Registry status is verified, active_change is null, and last_verified_commit records the Candidate SHA. Verified means only the local deterministic Schedule boundary with synthetic fixtures; it does not authorize real Xianyu scheduled publishing, browser automation, Credential handling, WeCom, AI, or platform access.


## T9 Ready Candidate record

CHG-0007 is in VERIFYING for final PR review preparation. T1 through T8 are complete and T9 remains incomplete until final PR administration is recorded. CAP-XY-SCHEDULE remains verified with Evidence Candidate SHA `0d9cfacedc1947e518d990151225ec8a15540f76` and verification commit `853129698995a32464a17aa93c9c9066d709cf7f`. PR #8 remains Draft until the Ready Candidate passes CI. No Reviewer request, auto-merge, merge, archive, branch deletion, CHG-0008, real Xianyu access, real scheduled publishing, browser automation, Playwright, Credential handling, WeCom, AI, Redis, Celery, recurring schedule, or external queue behavior is authorized by this preparation state.
