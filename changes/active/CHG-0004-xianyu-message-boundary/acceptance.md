# CHG-0004 Acceptance

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## T6 acceptance criteria

1. CHG-0004 remains APPROVED.
2. T1-T6 are complete.
3. T7-T9 remain incomplete.
4. PROJECT_STATE reports 6/9.
5. Next task is `T7 Add unit, contract, security, and active-change acceptance tests`.
6. Message Package contains exactly six approved files.
7. No forbidden Message module exists.
8. Domain import uses no SQLAlchemy.
9. Package import does not register ORM metadata.
10. Migration 0003 exists.
11. Migration down_revision is 0002.
12. Alembic has one linear head.
13. Three approved tables exist after upgrade.
14. No create_all is used.
15. Conversation rows are Profile-scoped.
16. Message rows are Profile-scoped.
17. Delivery Attempt rows are Profile-scoped.
18. Message Content maximum length is 4096.
19. Generic JSON/BLOB/raw frame columns do not exist.
20. NEW creates one Message and one Attempt.
21. DUPLICATE creates no second Message.
22. DUPLICATE creates another Attempt.
23. INDETERMINATE creates a separate Message.
24. CONFLICT rolls back and overwrites nothing.
25. Platform Message Identifier alone is not a dedupe key.
26. Message Content hash is not a dedupe key.
27. Service owns transaction commit/rollback.
28. Repository does not commit.
29. Worker starts STOPPED.
30. Explicit start reaches RUNNING.
31. Only RUNNING accepts Delivery.
32. Worker ownership is immutable.
33. Cross-Profile Delivery blocks Worker.
34. One Worker allows one In-flight Delivery.
35. Busy failure starts no transaction.
36. Invalid content may leave valid Worker RUNNING.
37. Deduplication conflict blocks Worker.
38. Persistence failure fails Worker.
39. Reset is explicit.
40. Stop is graceful.
41. Automatic reconnect count is zero.
42. Automatic retry count is zero.
43. No Thread, Subprocess, Scheduler, DNS, HTTP or WebSocket is created.
44. Only Synthetic Message Fixtures are used.
45. CAP-XY-MESSAGE remains planned.
46. Registry implementation_paths remain empty.
47. Registry test_paths remain empty.
48. active_change remains null.
49. last_verified_commit remains null.
50. Capability Specification remains unchanged.
51. No real customer data exists.
52. PR remains Draft/open/unmerged.
53. Auto-merge remains disabled.
54. Complete verification passes.
55. Conversation is exposed through the import-safe package surface.
56. Package import still does not register Message ORM metadata.
57. Delivery Identity compatibility includes Platform Conversation Identifier.
58. A Platform Conversation Identifier mismatch causes Deduplication Conflict.
59. Conversation conflict writes no additional Conversation, Message, or Delivery Attempt.
60. Invalid Message input may leave a valid Worker RUNNING.
61. Authorization violations block the Worker.
62. Risk violations block the Worker.
63. Protocol violations block the Worker.
64. Deduplication Conflict blocks the Worker.
65. Persistence failures fail the Worker.
66. Internal failures fail the Worker.
67. Unexpected exceptions are converted to sanitized MessageInternalError.
68. stop() cannot transition BLOCKED directly to STOPPED.
69. stop() cannot transition FAILED directly to STOPPED.
70. BLOCKED and FAILED require explicit reset.
71. The five retained permanent-test edits are Migration-head compatibility changes only.
72. Those compatibility changes added no test functions.
73. Tasks remain 6 / 9 and T7 remains incomplete.

## Current authorization

T1 through T6 are complete.

The local, synchronous, Profile-scoped, Synthetic Message receiving boundary is implemented.

T7 is the next executable task and must be performed separately.

CAP-XY-MESSAGE remains planned and unbound pending T8.

This execution does not authorize real WebSocket access, external network access, real Credential access, real account access, real customer-message processing, message sending, API, Web UI, capability binding, Ready-for-review, reviewer requests, auto-merge, or merge.

## T7 acceptance criteria

55. T7 adds exactly 42 new permanent Message tests.
56. `tests/unit/test_message_domain.py` contains exactly 12 explicit top-level tests.
57. `tests/unit/test_message_service.py` contains exactly 9 explicit top-level tests.
58. `tests/unit/test_message_worker.py` contains exactly 8 explicit top-level tests.
59. `tests/contract/test_message_persistence.py` contains exactly 8 explicit top-level tests.
60. `tests/contract/test_message_security.py` contains exactly 5 explicit top-level tests.
61. Existing Import Safety coverage remains exactly three test functions and includes the Message Package import-safe boundary.
62. NEW, DUPLICATE, INDETERMINATE, Content Conflict, and Conversation Conflict behavior are covered.
63. UUID version 4 generation, transaction ownership, rollback, Profile scope, and Account scope are covered.
64. Worker lifecycle, failure-state mapping, explicit reset, one in-flight delivery, re-entry protection, and graceful stop are covered.
65. The three-table schema, Migration lineage, Foreign Keys, database constraints, Repository no-commit behavior, empty downgrade, and non-empty downgrade fail-closed behavior are covered.
66. Import isolation, absence of external integrations, blocked network/subprocess/Home/thread entry points, sanitized errors, and Synthetic Fixture-only evidence are covered.
67. Persistence and Security Contract tests pass in both orders.
68. Account and Message Contract tests pass in both orders.
69. No global SQLAlchemy mapper or metadata cleanup escape hatch is added.
70. No Runtime, Migration, Registry, Capability Specification, dependency, or CI file is modified.
71. `CAP-XY-MESSAGE` remains planned and unbound with empty implementation_paths and test_paths.
72. CHG-0004 remains APPROVED, T1 through T7 are complete, and T8 is the next executable task.
73. T8 is not started by T7.
