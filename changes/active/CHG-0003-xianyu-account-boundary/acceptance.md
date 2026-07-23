# CHG-0003 Acceptance

Status: VERIFYING
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

56. Account Contract test modules do not insert a replacement production package into sys.modules.

57. Account Contract test modules do not assign to account-related sys.modules entries.

58. Account Contract test modules do not patch the type of Base.metadata.tables.

59. Account Contract test modules do not replace or patch __eq__ behavior.

60. Account Contract test modules have no top-level xianyu_system, SQLAlchemy, or Alembic imports.

61. Importing the Contract test modules leaves account-related sys.modules unchanged.

62. Importing the Contract test modules leaves Base.metadata table membership unchanged.

63. Importing the Contract test modules leaves the metadata table-mapping equality method unchanged.

64. ORM, Repository, Service, and Migration checks execute in isolated child processes.

65. Runtime external-resource blocking executes in an isolated child process.

66. Permanent account test counts remain 10, 7, 7, and 4.

67. Full test collection remains 280.

68. Tasks remain 7/9 and next_task remains T8.

69. Importing the account package does not eagerly import Account Service.

70. Importing account Domain types does not load account Persistence.

71. Importing account Domain types does not register ORM metadata.

72. AccountService remains in the package public `__all__` surface.

73. AccountService package access lazily loads the real Service class.

74. Permanent Import Safety covers the account package and account Domain module.

75. Core runtime metadata remains empty during Domain-only test collection.

76. No proxy module or test-only Service type is added.

81. The account package initializer is encoded as UTF-8 without a byte-order mark.

82. The account package initializer does not begin with the byte sequence EF BB BF.

83. Permanent Import Safety checks the raw account initializer bytes.

84. Active-change acceptance checks the raw account initializer bytes.

85. BOM verification does not use utf-8-sig before testing for the BOM.

86. Removing the BOM changes no account initializer byte after the first three bytes.

87. AccountService lazy-loading behavior remains unchanged.

88. Permanent test counts remain unchanged.

89. Full test collection remains 280.

90. Tasks remain 7/9 and next_task remains T8.

## T8 evidence candidate criteria

1. CAP-XY-ACCOUNT registers the exact five implementation paths.

2. CAP-XY-ACCOUNT registers the exact nine test paths.

3. All registered evidence paths are safe repository-relative files and exist.

4. CAP-XY-ACCOUNT status is `implementing`.

5. CAP-XY-ACCOUNT active_change is `CHG-0003-xianyu-account-boundary`.

6. CAP-XY-ACCOUNT last_verified_commit is null.

7. Capability status counts are planned 6, implementing 1, verified 3.

8. Tasks remain 7/9 and next_task remains T8.

9. Full collection remains 280.

10. PR #3 remains Draft, open, and unmerged.

## T8 acceptance criteria

1. T1-T8 complete.

2. T9 incomplete.

3. PROJECT_STATE completed = 8.

4. PROJECT_STATE next_task = T9.

5. CAP-XY-ACCOUNT status = verified.

6. active_change = null.

7. last_verified_commit is 40-character Candidate SHA `2aab941cb7f713d7e46675789c47971a2c79c564`.

8. Candidate SHA exists and is a HEAD ancestor.

9. Implementation Paths are the exact five approved paths.

10. Test Paths are the exact nine approved paths.

11. All evidence paths exist, are safe, and have no duplicates.

12. Account specification lists every evidence path.

13. Account specification records Candidate SHA `2aab941cb7f713d7e46675789c47971a2c79c564`.

14. Capability status counts are planned 6 and verified 4.

15. No capability remains implementing.

16. Unit = 196.

17. Contract = 65.

18. Permanent acceptance = 15.

19. Active acceptance = 4.

20. Full collection = 280.

21. Complete verification, Security, Ruff, Mypy, Pip Check, and offline gate pass.

22. No runtime, Migration, dependency, or CI file is modified.

23. PR #3 remains Draft, open, and unmerged.

24. Ready-for-review, auto-merge, and merge are not authorized.

## T9 Ready candidate criteria

1. CHG-0003 status is VERIFYING in proposal, design, tasks, and acceptance.
2. T1-T8 are complete.
3. T9 remains incomplete before the Ready transition.
4. PROJECT_STATE completed = 8.
5. PROJECT_STATE next_task remains T9.
6. CAP-XY-ACCOUNT remains verified.
7. CAP-XY-ACCOUNT active_change remains null.
8. CAP-XY-ACCOUNT last_verified_commit remains the Evidence Candidate SHA.
9. No runtime, Migration, Registry, dependency, CI, API, browser, Provider, Secure Storage, Scheduler, background-process, network, real-account, or Secret Material behavior changes.
10. Unit remains 196.
11. Contract remains 65.
12. Permanent acceptance remains 15.
13. Active acceptance remains 4.
14. Full collection remains 280.
15. Phase A GitHub Actions must pass before Ready transition.
16. PR remains open and unmerged.
17. Auto-merge remains disabled.
18. Merge and archive remain unauthorized.

## T9 final acceptance criteria

1. T1-T9 complete.
2. All nine tasks are checked.
3. PROJECT_STATE completed = 9.
4. PROJECT_STATE next_task = null.
5. CHG-0003 status is VERIFYING.
6. CAP-XY-ACCOUNT remains verified.
7. active_change remains null.
8. last_verified_commit remains the Evidence Candidate SHA.
9. Capability path evidence remains unchanged.
10. Unit = 196.
11. Contract = 65.
12. Permanent acceptance = 15.
13. Active acceptance = 4.
14. Full collection = 280.
15. PR #3 is Ready for review.
16. PR #3 remains open and unmerged.
17. Auto-merge is disabled.
18. No manual Reviewer request was made.
19. No merge, close, branch deletion, archive, or next Change creation occurred.
20. Final GitHub Actions pass on the final administration head.

## Current authorization

T1 through T9 are complete.

CHG-0003 remains VERIFYING while PR #3 is under review.

No further CHG-0003 task is authorized.

Merge requires separate explicit authorization against the exact current PR head.

Auto-merge, admin bypass, close, source-branch deletion, archive, and creation of the next active change are not authorized.
