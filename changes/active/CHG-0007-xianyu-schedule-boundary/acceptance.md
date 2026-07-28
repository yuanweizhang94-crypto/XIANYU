# CHG-0007 Acceptance

Status: DRAFT
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
