# CHG-0003 Acceptance

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## T2 acceptance criteria

1. CHG-0003 remains the only active change.

2. CHG-0003 remains APPROVED in proposal, design, tasks, and acceptance.

3. T1 and T2 are complete.

4. T3-T9 remain incomplete.

5. generated/PROJECT_STATE.json reports two completed tasks.

6. generated/PROJECT_STATE.json reports T3 as next_task.

7. The design defines Platform Account.

8. The design defines Account Reference.

9. The design defines Profile and explicitly distinguishes it from a browser profile.

10. The design defines Profile Identifier.

11. The design defines Account Alias.

12. The design defines External Account Identifier.

13. The design defines Credential Reference.

14. The design defines Session Material.

15. The design defines Profile-scoped State.

16. The design defines Isolation Boundary.

17. The design defines Synthetic Fixture.

18. The design records the one-to-one ownership relationship between Profile and Account Reference.

19. The design prohibits cross-Profile mutable-state, Credential Reference, and Session Material reuse.

20. Missing, ambiguous, conflicting, or cross-Profile ownership information fails closed.

21. T3 security decisions remain deferred.

22. T4 persistence and migration decisions remain deferred.

23. T5 module and runtime ownership decisions remain deferred.

24. CAP-XY-ACCOUNT remains planned and unbound.

25. CAP-XY-ACCOUNT retains no implementation or test evidence paths.

26. No runtime, API, contract, migration, dependency, CI, capability registry, capability specification, archived change, or permanent test file is modified.

27. No real account, credential, Cookie, Token, browser directory, customer data, or Session Material is added.

28. PR #3 remains Draft, open, and unmerged.

29. Auto-merge remains disabled.

30. Repository verification, security scan, Ruff, Mypy, and the complete test suite pass.

## Current authorization

T1 and T2 are complete.

T3 is the next executable task and must be performed separately.

This execution does not authorize security implementation, credential handling, persistence, database changes, API changes, worker changes, browser integration, account access, capability binding, Ready-for-review, auto-merge, or merge.
