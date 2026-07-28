# CHG-0007 Design

Status: APPROVED
Change ID: CHG-0007-xianyu-schedule-boundary

## Draft design posture

DRAFT records design intent only. It does not authorize implementation.

## Proposed boundary

The proposed Schedule boundary will reuse xianyu_system.core.scheduler as infrastructure and will keep business facts in a Schedule Repository. APScheduler MemoryJobStore may only be an in-process wakeup adapter and never the business fact source.

## Proposed exclusions

The design excludes recurring schedules, distributed scheduling, persistent APScheduler JobStores, platform access, browser automation, Credential handling, WeCom, AI, Redis, Celery, and external queues.

## Review focus

T2 through T5 must approve terminology, safety boundaries, deterministic decision behavior, and ownership before Runtime code appears.


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

Permanent tests now cover the approved local Schedule boundary without binding CAP-XY-SCHEDULE evidence before T8. No real Xianyu access, browser automation, Playwright, Credential handling, recurring schedule, WeCom, AI, Redis, Celery, or external queue was introduced.


## T8 Phase A evidence candidate record

CAP-XY-SCHEDULE is registered as `implementing` for the Evidence Candidate. Exact implementation and test evidence paths are bound in `specs/CAPABILITY_REGISTRY.yaml` and documented in `specs/capabilities/CAP-XY-SCHEDULE.md`. `last_verified_commit` remains null until this Candidate commit completes local and GitHub Actions verification. Tasks remain 7 / 9 while Phase A is in progress; T8 is still the next task until Phase B records the verified Candidate SHA.
