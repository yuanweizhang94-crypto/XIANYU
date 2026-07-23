# CHG-0003 Acceptance

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## T6 acceptance criteria

1. CHG-0003 remains the only active change.

2. CHG-0003 remains APPROVED in proposal, design, tasks, and acceptance.

3. T1 through T6 are complete.

4. T7-T9 remain incomplete.

5. generated/PROJECT_STATE.json reports six completed tasks.

6. generated/PROJECT_STATE.json reports T7 as next_task.

7. The local package, ORM mapping, Repository, Service, and Migration exist.

8. Only one account business table is created by the account Migration.

9. No Secret Material field is added.

10. No JSON, BLOB, payload, metadata, context, properties, extras, Cookie, Token, password, browser path, or customer-data field is added.

11. Profile Identifiers use UUID version 4.

12. The local lifecycle states are PENDING, ENABLED, and DISABLED.

13. Service owns transaction coordination.

14. Repository does not independently commit.

15. Uniqueness and stale-concurrency conflicts fail closed.

16. Application startup does not automatically run Migration.

17. No API, web UI, Scheduler Job, background Worker process, browser integration, Provider, or external platform behavior is approved or implemented.

18. CAP-XY-ACCOUNT remains planned, unbound, and without Registry evidence paths.

19. PR #3 remains Draft, open, and unmerged.

20. Auto-merge remains disabled.

21. Repository verification, security scan, Ruff, Mypy, and the complete test suite pass.

## Current authorization

T1 through T6 are complete.

T7 is the next executable task and must be performed separately.

This execution does not authorize T7 permanent tests, capability binding, Ready-for-review, auto-merge, or merge.
