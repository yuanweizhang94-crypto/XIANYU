# CHG-0003 Acceptance

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## T4 acceptance criteria

1. CHG-0003 remains the only active change.

2. CHG-0003 remains APPROVED in proposal, design, tasks, and acceptance.

3. T1, T2, T3, and T4 are complete.

4. T5-T9 remain incomplete.

5. generated/PROJECT_STATE.json reports four completed tasks.

6. generated/PROJECT_STATE.json reports T5 as next_task.

7. All approved T2 terminology and T3 security rules remain intact.

8. The approved persistence target is the existing CAP-CORE-DATABASE SQLite database.

9. Exactly one future business table is approved: xianyu_account_profiles.

10. The approved future fields and their security semantics are defined.

11. Secret Material, browser state, payload blobs, and generic JSON or metadata columns are prohibited.

12. Profile Identifier is the primary key and canonical local identity.

13. External Account Identifier and Credential Reference are unique when non-null.

14. Credential Reference remains opaque, non-secret, and Profile-owned.

15. Lifecycle states are PENDING, ENABLED, DISABLED, and ARCHIVED.

16. ENABLED does not imply authentication or authorization.

17. ARCHIVED is terminal and requires clearing Credential Reference.

18. Optimistic row_version concurrency is approved.

19. Stale writes and uniqueness conflicts fail closed.

20. Mutation operations are transactional and partial writes are prohibited.

21. No bulk update, bulk delete, implicit Profile, credential fallback, automatic discovery, import, or backfill is approved.

22. Operation-scoped credential, authorization, risk, and provider state is not persisted as authoritative state.

23. No persistent audit-event table is approved.

24. No automatic purge or hard-delete runtime is approved.

25. The approved future Revision is 0002_xianyu_account_boundary.

26. Its down_revision is 0001_core_baseline.

27. The future upgrade creates only the approved empty table, constraints, and index.

28. The future downgrade fails closed when the table contains rows.

29. Application startup remains prohibited from automatically running migrations.

30. T4 creates no Migration file and modifies no existing Migration.

31. The current migration directory still contains only 0001_core_baseline.py and __init__.py.

32. T5 ownership decisions remain deferred.

33. T6 runtime and Migration implementation remains deferred.

34. T7 permanent implementation tests remain deferred.

35. CAP-XY-ACCOUNT remains planned and unbound.

36. CAP-XY-ACCOUNT retains no implementation or test evidence paths.

37. No runtime, ORM, API, contract, migration, dependency, CI, registry, capability specification, archived change, or permanent test file is modified.

38. No real account, credential, Cookie, Token, password, browser directory, customer data, or Secret Material is added.

39. PR #3 remains Draft, open, and unmerged.

40. Auto-merge remains disabled.

41. Repository verification, security scan, Ruff, Mypy, and the complete test suite pass.

## Current authorization

T1, T2, T3, and T4 are complete.

T5 is the next executable task and must be performed separately.

This execution does not authorize ORM code, Migration files, database mutation, provider selection, provider integration, API changes, worker changes, browser integration, account access, Secret Material handling, capability binding, Ready-for-review, auto-merge, or merge.
