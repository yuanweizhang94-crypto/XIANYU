# CHG-0003 Acceptance

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## T5 acceptance criteria

1. CHG-0003 remains the only active change.

2. CHG-0003 remains APPROVED in proposal, design, tasks, and acceptance.

3. T1, T2, T3, T4, and T5 are complete.

4. T6-T9 remain incomplete.

5. generated/PROJECT_STATE.json reports five completed tasks.

6. generated/PROJECT_STATE.json reports T6 as next_task.

7. All approved T2 terminology, T3 security rules, and T4 persistence principles remain intact.

8. CAP-XY-ACCOUNT remains owned by the `worker.account` capability namespace.

9. The approved future package path is `app/xianyu_system/worker/account/`, and the import namespace is `xianyu_system.worker.account`.

10. The minimal approved future modules are `domain.py`, `persistence.py`, and `service.py`.

11. The domain module is independent of persistence, SQLAlchemy, and FastAPI.

12. Persistence uses the existing Core Engine and Session ownership boundary without owning them.

13. The account service owns transaction coordination.

14. Profile Identifier generation uses UUID version 4 through the Python standard library.

15. The local lifecycle states are PENDING, ENABLED, and DISABLED.

16. ENABLED does not imply authentication, authorization, platform validity, credential validity, or safe operation.

17. Repository may flush when required but must not commit independently.

18. A second Engine, Session factory, or UnitOfWork framework is not approved.

19. Stable non-sensitive account-owned error categories are defined.

20. Credential Reference ownership remains separate from Secure Storage and Credential Provider ownership.

21. No API, web UI, Scheduler Job, background Worker process, or browser integration is approved.

22. T6 is allowed only within the approved package, documentation, generated-state, and active-change test surface.

23. T6 implementation must remain separate from this execution.

24. T7 permanent tests remain deferred.

25. T8 registry binding and evidence updates remain deferred.

26. CAP-XY-ACCOUNT remains planned, unbound, and without implementation or test evidence paths.

27. No runtime, ORM, API, contract, migration, dependency, CI, registry, capability specification, archived change, or permanent test file is modified.

28. No runtime package exists.

29. No Migration was added.

30. No real account, credential, Cookie, Token, password, browser directory, customer data, or Secret Material is added.

31. PR #3 remains Draft, open, and unmerged.

32. Auto-merge remains disabled.

33. Repository verification, security scan, Ruff, Mypy, and the complete test suite pass.

## Current authorization

T1, T2, T3, T4, and T5 are complete.

T6 is the next executable task and must be performed separately.

This execution does not authorize runtime code, ORM code, Migration files, database mutation, API changes, Worker processes, provider integration, browser integration, account access, Secret Material handling, capability binding, Ready-for-review, auto-merge, or merge.
