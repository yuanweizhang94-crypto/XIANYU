# CHG-0003 Acceptance

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## T7 acceptance criteria

1. CHG-0003 remains the only active change.

2. CHG-0003 remains APPROVED.

3. T1-T7 are complete.

4. T8-T9 remain incomplete.

5. PROJECT_STATE reports 7 completed tasks.

6. PROJECT_STATE reports T8 as next_task.

7. Four dedicated permanent account test files exist.

8. Account domain tests contain exactly 10 test functions.

9. Account Service tests contain exactly 7 test functions.

10. Account persistence Contract tests contain exactly 7 test functions.

11. Account security Contract tests contain exactly 4 test functions.

12. No parameterized test cases artificially change the collection count.

13. AccountReference immutability and Profile ownership are covered.

14. Input normalization and field boundaries are covered.

15. UUID version 4 Profile creation is covered.

16. All approved and prohibited lifecycle transitions are covered.

17. Service mutation and transaction behavior are covered.

18. Missing Profile behavior is covered.

19. Optimistic-concurrency conflicts are covered.

20. External Identifier uniqueness is covered.

21. Credential Reference uniqueness is covered.

22. Repository flush-without-commit behavior is covered.

23. Relational round-trip ownership is covered.

24. Migration upgrade and empty downgrade are covered.

25. Non-empty downgrade failure and data preservation are covered.

26. Database trim, lifecycle, version, and uniqueness constraints are covered.

27. Public package restrictions are covered.

28. Sanitized error behavior is covered.

29. Absence of network, browser, Provider, Secure Storage, API, Scheduler, and background-process behavior is covered.

30. Only Synthetic Fixtures are used.

31. No real Secret Material or customer data is added.

32. No runtime, Migration, dependency, CI, Registry, capability specification, or archived-change file is modified.

33. CAP-XY-ACCOUNT remains planned and unbound.

34. CAP-XY-ACCOUNT evidence paths remain empty.

35. Full collection equals 280.

36. Unit tests equal 196 passed.

37. Contract tests equal 65 passed.

38. Permanent acceptance tests equal 15 passed.

39. Active CHG-0003 acceptance tests equal 4 passed.

40. PR #3 remains Draft, open, and unmerged.

41. Auto-merge remains disabled.

42. Repository verification, security scan, Ruff, Mypy, Pip Check, warning mode, and offline gates pass.

43. Account operations execute successfully while socket creation and socket connections are blocked.

44. Account operations execute successfully while subprocess.run and subprocess.Popen are blocked.

45. Account operations execute successfully while Path.home is blocked.

46. Account tests do not call a browser directory or operating-system Credential Store.

47. Account Contract tests do not call clear_mappers.

48. Account Contract tests do not remove the account table from shared Base.metadata.

49. Account Contract tests do not evict account modules from sys.modules.

50. Account persistence and security Contract modules pass in both execution orders.

51. Database constraints explicitly reject whitespace-only External Account Identifiers.

52. Database constraints explicitly reject whitespace-only Credential References.

53. Permanent account test counts remain 10, 7, 7, and 4.

54. Full collection remains 280.

55. Tasks remain 7/9 and next_task remains T8.

## Current authorization

T1 through T7 are complete.

T8 is the next executable task and must be performed separately.

This execution does not authorize capability binding, Registry evidence updates, capability verification, Ready-for-review, auto-merge, or merge.
