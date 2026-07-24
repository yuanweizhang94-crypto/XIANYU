# CHG-0004 Acceptance

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## T4 acceptance criteria

1. CHG-0002 and CHG-0003 remain archived.
2. Their historical tests remain preserved.
3. CHG-0004 remains the only active change.
4. CHG-0004 remains APPROVED in proposal, design, tasks, and acceptance.
5. T1 through T4 are complete.
6. T5-T9 remain incomplete.
7. generated/PROJECT_STATE.json reports four completed tasks.
8. generated/PROJECT_STATE.json reports `T5 Approve worker ownership, lifecycle, and failure boundaries` as `next_task`.
9. All T2 terminology remains present.
10. All thirteen T2 terminology invariants remain present.
11. All T3 transport, authentication, risk-control, TLS, reconnect, acknowledgement, and redaction boundaries remain present.
12. No global Platform Message ordering guarantee is approved.
13. No cross-Profile ordering guarantee is approved.
14. No cross-Conversation ordering guarantee is approved.
15. Transport arrival order is not authoritative Platform order.
16. Delivery Cursor is not automatically ordering evidence.
17. Out-of-order and late Message Events are not silently discarded.
18. Local Conversation Identifier uses UUID version 4.
19. Local Message Identifier uses UUID version 4.
20. Local Delivery Attempt Identifier uses UUID version 4.
21. Delivery Identity is Profile-scoped.
22. Delivery Identity contains no Message Content or Secret Material.
23. Platform Message Identifier alone is not a global deduplication key.
24. Message Content or a content hash is not a deduplication key.
25. Deduplication Decision defines NEW.
26. Deduplication Decision defines DUPLICATE.
27. Deduplication Decision defines INDETERMINATE.
28. Deduplication Decision defines CONFLICT.
29. DUPLICATE does not create a second Message Record.
30. INDETERMINATE is not silently discarded.
31. CONFLICT fails closed and does not overwrite data.
32. Message Record creation is idempotent for the same approved Profile-scoped Delivery Identity.
33. Replay classification depends on approved Profile-scoped Delivery Identity.
34. CAP-CORE-DATABASE remains the only approved persistence infrastructure.
35. Conceptual Conversation, Message, and Delivery Attempt records are Profile-scoped.
36. Message Content is plain UTF-8 text only.
37. Message Content maximum normalized length is 4096 characters.
38. Empty or whitespace-only content is invalid.
39. HTML execution is prohibited.
40. Attachment, media, binary, BLOB, arbitrary JSON, raw payload, and raw Transport Frame persistence are prohibited.
41. Generic metadata or property bags are prohibited.
42. Persistence mutations require one explicit logical transaction.
43. Deduplication checks and Message creation occur in the same transaction.
44. Partial writes are prohibited.
45. Repository methods must not independently commit.
46. Profile-scoped uniqueness protection is required.
47. Concurrent duplicate creation must not create multiple Message Records.
48. No automatic retention duration is approved.
49. No purge Worker or Scheduler Job is approved.
50. Delivery Cursor remains non-authoritative.
51. Application startup must not auto-migrate.
52. Migration must remain explicit.
53. Non-empty downgrade fails closed unless a data-preserving downgrade is separately approved.
54. T5 Worker, Adapter, Repository, Service, lifecycle, failure, observability, and testing ownership decisions remain deferred.
55. CAP-XY-ACCOUNT remains verified and unchanged.
56. CAP-XY-MESSAGE remains planned and unbound.
57. CAP-XY-MESSAGE has no implementation or test paths.
58. No runtime, ORM, table, Migration, Repository, Service, API, Worker, Adapter, WebSocket, Socket, network, message sending, Credential Provider, or real customer-data behavior is added.
59. No dependency, CI, Contract, Capability Registry, capability specification, archived change, Core, account, or runtime file is modified.
60. PR #4 remains Draft, open, and unmerged.
61. Auto-merge remains disabled.
62. Repository verification, security scan, duplicate capability validation, Ruff, Mypy, Pip Check, offline verification, and the complete test suite pass.

## Current authorization

T1 through T4 are complete.

The ordering, deduplication, idempotency, replay, persistence, transaction, concurrency, retention, and Migration boundaries are approved.

T5 is the next executable task and must be performed separately.

This execution does not authorize Worker, Adapter, Repository, Service, lifecycle, failure, observability, physical schema, Migration file, runtime implementation, real WebSocket access, external network access, real account access, real customer-message processing, capability binding, Ready-for-review, reviewer requests, auto-merge, or merge.
