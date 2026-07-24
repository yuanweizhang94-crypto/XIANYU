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

## Current authorization

T1 through T6 are complete.

The local, synchronous, Profile-scoped, Synthetic Message receiving boundary is implemented.

T7 is the next executable task and must be performed separately.

CAP-XY-MESSAGE remains planned and unbound pending T8.

This execution does not authorize real WebSocket access, external network access, real Credential access, real account access, real customer-message processing, message sending, API, Web UI, capability binding, Ready-for-review, reviewer requests, auto-merge, or merge.
