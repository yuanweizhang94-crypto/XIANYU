# CHG-0007 Tasks

Status: APPROVED
Change ID: CHG-0007-xianyu-schedule-boundary

- [x] T1 Obtain explicit project-owner approval for CHG-0007
- [x] T2 Finalize schedule request, trigger, decision, dispatch, UTC, and grace-window terminology
- [x] T3 Approve Core scheduler reuse, Publish coupling, permission, credential, and platform boundaries
- [ ] T4 Approve validation, idempotency, duplicate, cancellation, misfire, and uncertainty behavior
- [ ] T5 Approve ownership, persistence, lifecycle, audit, concurrency, and failure boundaries
- [ ] T6 Implement the approved local deterministic scheduling boundary
- [ ] T7 Add permanent unit, contract, security, migration, and active-change acceptance tests
- [ ] T8 Bind capability evidence and complete two-phase verification
- [ ] T9 Complete final PR administration

## Current task state

Completed tasks: 3 / 9.

Next task: T4 Approve validation, idempotency, duplicate, cancellation, misfire, and uncertainty behavior.


## T1 approval record

Project-owner approval authorizes T1-T9 for CHG-0007 only, in order. Runtime, merge, archive, and branch deletion remain gated by their later checks.


## T2 terminology decision

Schedule Request means a local request to run exactly one Publish boundary call either immediately or at an explicit UTC run_at time. Trigger is IMMEDIATE or RUN_AT_UTC. Schedule Decision is the deterministic validation result. Dispatch is the local atomic claim of a due schedule. UTC is mandatory for all stored instants. Grace window is a finite misfire allowance in seconds; outside grace the item becomes MISFIRED and is not published. Cancellation is a terminal local state before claim.


## T3 safety boundary decision

CHG-0007 reuses xianyu_system.core.scheduler without modifying it. APScheduler MemoryJobStore is only an in-process wakeup adapter. Publish coupling is explicit through the existing local PublishService interface and never duplicates Publish validation or DTOs. No permissions, Credentials, browser Profile, Playwright, real Xianyu platform session, WeCom, AI, network request, Redis, Celery, or external queue is introduced.
