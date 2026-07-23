# CHG-0004 Acceptance

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## T2 acceptance criteria

1. CHG-0002 and CHG-0003 remain archived.
2. Their historical tests remain preserved.
3. CHG-0004 remains the only active change.
4. CHG-0004 remains APPROVED in proposal, design, tasks, and acceptance.
5. T1 and T2 are complete.
6. T3-T9 remain incomplete.
7. generated/PROJECT_STATE.json reports two completed tasks.
8. generated/PROJECT_STATE.json reports `T3 Approve transport, authentication, and risk-control boundaries` as `next_task`.
9. The design defines Platform Message.
10. The design defines Message Event.
11. The design defines Message Content.
12. The design defines Platform Message Identifier.
13. The design defines Conversation.
14. The design defines Conversation Reference.
15. The design defines Platform Conversation Identifier.
16. The design defines Participant Reference.
17. The design defines Delivery Attempt.
18. The design defines Delivery Cursor.
19. The design defines Acknowledgement.
20. The design defines Duplicate Delivery.
21. The design defines Replay.
22. The design defines Ordering Boundary.
23. The design defines Synthetic Message Fixture.
24. Every Message Event and Conversation remains Profile-scoped.
25. External identifiers do not establish Profile ownership.
26. Acknowledgement is not business-processing success.
27. Delivery Cursor is not automatically a message identity, conversation identity, or deduplication key.
28. Missing, ambiguous, conflicting, or cross-Profile ownership information fails closed.
29. T3 transport, authentication, and risk-control decisions remain deferred.
30. T4 ordering, deduplication, and persistence decisions remain deferred.
31. T5 worker ownership, lifecycle, and failure decisions remain deferred.
32. CAP-XY-ACCOUNT remains verified and unchanged.
33. CAP-XY-MESSAGE remains planned and unbound.
34. CAP-XY-MESSAGE has no implementation or test paths.
35. No runtime, WebSocket, network, message persistence, Migration, Repository, Service, API, background worker, Scheduler Job, message sending, Credential handling, or real customer-data behavior is added.
36. No dependency, CI, Contract, Capability Registry, capability specification, archived change, Migration, Core, account, or runtime file is modified.
37. PR #4 remains Draft, open, and unmerged.
38. Auto-merge remains disabled.
39. Repository verification, security scan, duplicate capability validation, Ruff, Mypy, Pip Check, and the complete test suite pass.

## Current authorization

T1 and T2 are complete.

The canonical message, conversation, participant, and delivery terminology is finalized.

T3 is the next executable task and must be performed separately.

This execution does not authorize transport implementation, authentication, Credential resolution, risk-control behavior, ordering guarantees, deduplication algorithms, persistence, database changes, runtime implementation, real WebSocket access, external network access, real account access, customer-message processing, capability binding, Ready-for-review, reviewer requests, auto-merge, or merge.
