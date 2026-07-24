# CHG-0004 Acceptance

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## T5 acceptance criteria

1. CHG-0002 and CHG-0003 remain archived.
2. Their historical tests remain preserved.
3. CHG-0004 remains the only active change.
4. CHG-0004 remains APPROVED in proposal, design, tasks, and acceptance.
5. T1 through T5 are complete.
6. T6-T9 remain incomplete.
7. generated/PROJECT_STATE.json reports five completed tasks.
8. generated/PROJECT_STATE.json reports `T6 Implement only the approved local message-receiving boundary` as `next_task`.
9. All T2 terminology remains present.
10. All thirteen T2 terminology invariants remain present.
11. All T3 transport, authentication, risk-control, TLS, reconnect, acknowledgement, and redaction boundaries remain present.
12. All T4 ordering, deduplication, persistence, transaction, retention, and Migration boundaries remain present.
13. CAP-XY-MESSAGE remains owned by `worker.message`.
14. The approved future package path is `app/xianyu_system/worker/message/`.
15. The approved future import namespace is `xianyu_system.worker.message`.
16. The approved future modules are `domain.py`, `persistence.py`, `service.py`, `transport.py`, and `worker.py`.
17. `domain.py` owns pure local Message domain concepts and sanitized domain errors.
18. `domain.py` remains independent of SQLAlchemy, FastAPI, Transport, Worker, Core Database, and application state.
19. `persistence.py` owns the SQLAlchemy projection and one concrete Message Repository.
20. `service.py` owns accepted-message use cases and logical transaction coordination.
21. `transport.py` owns transport-neutral delivery values and Protocol interfaces only.
22. `worker.py` owns in-process, Profile-scoped Message Worker lifecycle and orchestration.
23. The `worker` namespace does not mean a background thread, subprocess, Scheduler Job, daemon, browser Worker, or external platform connection.
24. The T6 Message Worker is synchronous.
25. The Worker is explicitly constructed, started, and stopped.
26. No automatic start, reconnect, retry, polling, heartbeat, background loop, thread, subprocess, or Scheduler behavior is approved.
27. One Message Worker instance belongs to exactly one Profile Identifier.
28. One Message Worker instance belongs to exactly one Account Reference owned by that Profile.
29. Worker ownership is immutable after construction.
30. No global Worker, current Profile, current Account, current Credential, or current Conversation is approved.
31. Worker state, Repository state, Service state, Transport state, Delivery Identity, Cursor state, and mutable lifecycle state are not shared across Profiles.
32. Worker Lifecycle States are `STOPPED`, `STARTING`, `RUNNING`, `STOPPING`, `BLOCKED`, and `FAILED`.
33. A Worker may accept delivery only while `RUNNING`.
34. Worker lifecycle state is local process state.
35. Worker lifecycle state is not persisted as durable authorization or recovery evidence.
36. Process restart begins with the Worker in `STOPPED`.
37. One Worker instance may process at most one delivery at a time.
38. Concurrent or re-entrant delivery processing fails closed with a sanitized busy outcome.
39. The Message Service owns the logical transaction.
40. Repository methods may flush but must not independently commit.
41. Transport code must not import Persistence.
42. Package and Domain imports must not register ORM metadata, open a database, read credentials, start a Worker, create a Socket, or access the network.
43. Automatic reconnect attempts equal zero.
44. Automatic processing retries equal zero.
45. Future real transport reconnect policy requires a separate reviewed change.
46. Profile ownership, Credential, Authorization, Risk, protocol, TLS, and security violations place the Worker in `BLOCKED`.
47. Deduplication Conflict failures place the Worker in `BLOCKED`.
48. Persistence failures place the Worker in `FAILED`.
49. Unexpected internal failures place the Worker in `FAILED`.
50. Event-local invalid synthetic input may be rejected without stopping a valid Worker when Profile ownership and security invariants remain valid.
51. No failure output exposes Message Content, Secret Material, full external identifiers, raw Transport Frames, raw provider errors, authentication data, Cookie, Token, Session Material, browser paths, or raw database errors.
52. Stop is explicit and graceful.
53. While `STOPPING`, no new delivery may begin.
54. An in-flight transaction must commit completely or roll back completely before the Worker becomes `STOPPED`.
55. T6 owns no operating-system signal handler and modifies no application startup or shutdown hook.
56. T6 may implement only the local, synchronous, Profile-scoped, Synthetic Message receiving boundary.
57. T6 must be separately authorized against the exact T5 HEAD.
58. CAP-XY-ACCOUNT remains verified and unchanged.
59. CAP-XY-MESSAGE remains planned and unbound.
60. CAP-XY-MESSAGE has no implementation or test paths.
61. No runtime package, Domain code, ORM, table, Migration, Repository, Service, Transport, Worker, API, WebSocket, Socket, DNS, HTTP, network, thread, subprocess, Scheduler, message sending, Credential Provider, or real customer-data behavior is added.
62. No dependency, CI, Contract, Capability Registry, capability specification, archived change, Core, account, or runtime file is modified.
63. PR #4 remains Draft, open, and unmerged.
64. Auto-merge remains disabled.
65. Repository verification, security scan, duplicate capability validation, Ruff, Mypy, Pip Check, offline verification, and the complete test suite pass.

## Current authorization

T1 through T5 are complete.

The Package, Module, Worker ownership, lifecycle, concurrency, transaction, failure, shutdown, observability, testing, and import-safety boundaries are approved.

T6 is the next executable task and must be performed separately.

This execution does not authorize runtime code, ORM code, database table, Migration file, Repository, Service, Transport, Worker, WebSocket access, external network access, real account access, real customer-message processing, capability binding, Ready-for-review, reviewer requests, auto-merge, or merge.
