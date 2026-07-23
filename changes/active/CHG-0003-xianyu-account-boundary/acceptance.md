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

8. CAP-XY-ACCOUNT future persistence uses the existing CAP-CORE-DATABASE SQLite, SQLAlchemy, and Alembic infrastructure boundary.

9. A second database, second Engine, or alternate persistence stack is not approved.

10. Ordinary database persistence is limited to approved non-secret Profile and Account Reference metadata categories.

11. Credential Reference persistence is allowed only as an opaque, non-secret, Profile-owned reference.

12. Secret Material, Cookies, Tokens, passwords, authorization headers, browser state, browser directories, Local Storage, Session Storage, customer data, and provider secret values are prohibited from ordinary database persistence.

13. Generic JSON, BLOB, payload, properties, extras, metadata, context, or arbitrary key-value fields are prohibited.

14. Credential Resolution Status and Operation Authorization Status must not be persisted as reusable proof of authorization.

15. Database records must not prove that a real Platform Account exists, is logged in, is authorized, or is safe to operate.

16. Every future record must have explicit Profile ownership.

17. Cross-Profile mutable-state and Credential Reference reuse are prohibited.

18. Future mutations must be transactional and partial writes are prohibited.

19. Uniqueness and stale-concurrency conflicts must fail closed.

20. No implicit current Profile or fallback Profile is approved.

21. Future migration execution remains explicit and application startup must not automatically run Alembic migrations.

22. Future upgrade may create only the minimum approved account-boundary schema and must not perform seed, import, discovery, browser scan, credential access, or network access.

23. Downgrade must never silently destroy non-empty business data.

24. T4 creates no Migration file and modifies no existing Migration.

25. T4 creates no ORM model, database table, Repository, DAO, API, Worker, Credential Provider, Secure Storage, or runtime behavior.

26. The current migration directory still contains only 0001_core_baseline.py and __init__.py.

27. Exact table count and names remain deferred to T5 and T6.

28. Exact column names, storage types, nullability, field lengths, constraints, and indexes remain deferred to T5 or T6.

29. Profile Identifier generation strategy remains deferred to T5.

30. Lifecycle state names, transitions, retirement, restoration, and Credential Reference cleanup remain deferred to T5.

31. Retention, archive, restoration, purge, and hard-delete behavior remain deferred to a later approved decision.

32. Exact downgrade strategy and operational approval process remain deferred to T5 and T6.

33. Final Alembic revision identifier remains deferred to T6, while down_revision must reference 0001_core_baseline and Alembic must retain one linear head.

34. T5 ownership decisions remain deferred.

35. T6 runtime and Migration implementation remains deferred.

36. T7 permanent implementation tests remain deferred.

37. CAP-XY-ACCOUNT remains planned and unbound.

38. CAP-XY-ACCOUNT retains no implementation or test evidence paths.

39. No runtime, ORM, API, contract, migration, dependency, CI, registry, capability specification, archived change, or permanent test file is modified.

40. No real account, credential, Cookie, Token, password, browser directory, customer data, or Secret Material is added.

41. PR #3 remains Draft, open, and unmerged.

42. Auto-merge remains disabled.

43. Repository verification, security scan, Ruff, Mypy, and the complete test suite pass.

## Current authorization

T1, T2, T3, and T4 are complete.

T5 is the next executable task and must be performed separately.

This execution does not authorize ORM code, Migration files, database mutation, provider selection, provider integration, API changes, worker changes, browser integration, account access, Secret Material handling, capability binding, Ready-for-review, auto-merge, or merge.
