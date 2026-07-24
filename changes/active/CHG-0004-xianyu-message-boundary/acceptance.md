# CHG-0004 Acceptance

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## T3 acceptance criteria

1. CHG-0002 and CHG-0003 remain archived.
2. Their historical tests remain preserved.
3. CHG-0004 remains the only active change.
4. CHG-0004 remains APPROVED in proposal, design, tasks, and acceptance.
5. T1 through T3 are complete.
6. T4-T9 remain incomplete.
7. generated/PROJECT_STATE.json reports three completed tasks.
8. generated/PROJECT_STATE.json reports `T4 Approve ordering, deduplication, and persistence boundaries` as `next_task`.
9. All T2 canonical terminology remains present.
10. All thirteen T2 terminology invariants remain present.
11. The design defines the approved secure transport boundary.
12. Future external WebSocket transport requires `wss://`.
13. TLS certificate verification remains mandatory.
14. TLS hostname verification remains mandatory.
15. Plaintext `ws://` is prohibited.
16. The Endpoint must come from trusted approved configuration.
17. Customer or message data must not control the Endpoint.
18. Unknown protocol behavior fails closed.
19. A future connection remains scoped to one exact Profile and Account Reference.
20. Authentication material remains outside the message domain.
21. Message receiving requires the explicit operation purpose `RECEIVE_MESSAGES`.
22. Credential Resolution Status is defined.
23. Operation Authorization Status is defined.
24. Risk Decision is defined.
25. A connection requires `RESOLVED`, `AUTHORIZED`, and `ALLOWED`.
26. Every other credential, authorization, verification, or risk state fails closed.
27. Platform verification and risk controls are never bypassed.
28. Reconnect must preserve exact Profile and Credential ownership.
29. Reconnect is prohibited for denied, verification-required, blocked, invalid, expired, or revoked states.
30. Reconnect must be bounded and use delay and backoff.
31. Exact retry values remain deferred to T5.
32. Acknowledgement remains transport-level only.
33. Acknowledgement does not mean persistence, business success, reply, uniqueness, or completion.
34. Unknown acknowledgement semantics fail closed.
35. Message Content is prohibited from logs and diagnostics.
36. Secret Material and raw authentication data are prohibited from logs and diagnostics.
37. Full Credential References and full external identifiers are prohibited from logs.
38. Raw transport frames are prohibited from logs.
39. Only Synthetic Message Fixtures may be used.
40. Tests perform no Socket, DNS, HTTP, WebSocket, browser, or Credential Store access.
41. T4 ordering, deduplication, idempotency, replay-retention, and persistence decisions remain deferred.
42. T5 Worker, Adapter, lifecycle, reconnect ownership, failure, and observability decisions remain deferred.
43. CAP-XY-ACCOUNT remains verified and unchanged.
44. CAP-XY-MESSAGE remains planned and unbound.
45. CAP-XY-MESSAGE has no implementation or test paths.
46. No runtime, WebSocket, Socket, network, message persistence, Migration, Repository, Service, API, Worker, background process, Scheduler Job, message sending, Credential handling, or real customer-data behavior is added.
47. No dependency, CI, Contract, Capability Registry, capability specification, archived change, Migration, Core, account, or runtime file is modified.
48. PR #4 remains Draft, open, and unmerged.
49. Auto-merge remains disabled.
50. Repository verification, security scan, duplicate capability validation, Ruff, Mypy, Pip Check, offline verification, and the complete test suite pass.

## Current authorization

T1 through T3 are complete.

The transport, authentication, Credential-resolution, authorization, permission, risk-control, TLS, reconnect, acknowledgement, and redaction boundaries are approved.

T4 is the next executable task and must be performed separately.

This execution does not authorize ordering guarantees, deduplication identities or algorithms, idempotency, replay retention, persistence, database changes, Worker or Adapter implementation, real WebSocket access, external network access, real account access, customer-message processing, capability binding, Ready-for-review, reviewer requests, auto-merge, or merge.
