# CHG-0007 Tasks

Status: VERIFYING
Change ID: CHG-0007-xianyu-schedule-boundary

- [x] T1 Obtain explicit project-owner approval for CHG-0007
- [x] T2 Finalize schedule request, trigger, decision, dispatch, UTC, and grace-window terminology
- [x] T3 Approve Core scheduler reuse, Publish coupling, permission, credential, and platform boundaries
- [x] T4 Approve validation, idempotency, duplicate, cancellation, misfire, and uncertainty behavior
- [x] T5 Approve ownership, persistence, lifecycle, audit, concurrency, and failure boundaries
- [x] T6 Implement the approved local deterministic scheduling boundary
- [x] T7 Add permanent unit, contract, security, migration, and active-change acceptance tests
- [x] T8 Bind capability evidence and complete two-phase verification
- [ ] T9 Complete final PR administration

## Current task state

Completed tasks: 8 / 9.

Next task: T9 Complete final PR administration.


## T1 approval record

Project-owner approval authorizes T1-T9 for CHG-0007 only, in order. Runtime, merge, archive, and branch deletion remain gated by their later checks.


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

T7 added permanent unit, contract, security, migration, import-safety, and active-change acceptance coverage for the local deterministic Schedule boundary. Coverage includes Schedule domain normalization, deterministic fingerprinting, validator fail-closed behavior, ScheduleService idempotency, conflict, cancellation, dispatch, misfire behavior, APScheduler DateTrigger registration, schedule table registration, migration lineage, offline SQL, and absence of real platform or integration side effects. CAP-XY-SCHEDULE remains planned and unbound until T8 evidence binding.


## T8 Phase A evidence candidate record

CAP-XY-SCHEDULE is registered as `implementing` for the Evidence Candidate. Exact implementation and test evidence paths are bound in `specs/CAPABILITY_REGISTRY.yaml` and documented in `specs/capabilities/CAP-XY-SCHEDULE.md`. `last_verified_commit` remains null until this Candidate commit completes local and GitHub Actions verification. Tasks remain 7 / 9 while Phase A is in progress; T8 is still the next task until Phase B records the verified Candidate SHA.


## T8 Phase B verification record

CAP-XY-SCHEDULE evidence paths are registered and verified. Evidence Candidate SHA: `0d9cfacedc1947e518d990151225ec8a15540f76`. Candidate GitHub Actions for quality, tests, and security on push and pull_request events completed successfully. Registry status is verified, active_change is null, and last_verified_commit records the Candidate SHA. Verified means only the local deterministic Schedule boundary with synthetic fixtures; it does not authorize real Xianyu scheduled publishing or platform access.


## T9 Ready Candidate record

CHG-0007 is in VERIFYING for final PR review preparation. T1 through T8 are complete and T9 remains incomplete until final PR administration is recorded. CAP-XY-SCHEDULE remains verified with Evidence Candidate SHA `0d9cfacedc1947e518d990151225ec8a15540f76` and verification commit `853129698995a32464a17aa93c9c9066d709cf7f`. PR #8 remains Draft until the Ready Candidate passes CI. No Reviewer request, auto-merge, merge, archive, branch deletion, CHG-0008, real Xianyu access, real scheduled publishing, browser automation, Playwright, Credential handling, WeCom, AI, Redis, Celery, recurring schedule, or external queue behavior is authorized by this preparation state.
