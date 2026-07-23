# CHG-0004 Design

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Design state

CHG-0004 is approved for controlled, task-by-task execution.

No runtime message design or implementation has been approved yet.

T2-T5 must finalize the terminology, transport, authentication, risk-control, ordering, deduplication, persistence, worker ownership, lifecycle, failure, and testing boundaries before T6 may begin.


## Architecture context

- One worker per Xianyu account.
- One local Profile boundary per account.
- WebSocket is the future message-receiving transport direction.
- Fixed rules take priority over AI fallback.

These directions do not authorize a real transport implementation.

## Proposed terminology

Future review may define:

- Message Event
- Conversation Identifier
- Sender Reference
- Recipient Profile Identifier
- Platform Message Identifier
- Delivery Cursor
- Delivery Attempt
- Acknowledgement
- Duplicate Delivery
- Replay
- Reconnect
- Ordering Boundary
- Synthetic Transport Fixture

No term is final until an approved task records the decision.

## Required decisions before runtime implementation

- Exact terminology.
- Profile and account ownership.
- Transport ownership.
- Authentication and credential-resolution ownership.
- Reconnect and backoff.
- Acknowledgement behavior.
- Ordering guarantees.
- Deduplication and idempotency.
- Replay and recovery.
- Persistence and retention.
- Logging and observability.
- Failure classification.
- Testing strategy.
- Migration requirements.
- Import-safety requirements.

## Security constraints

- Never open a real Xianyu WebSocket.
- Never import real credentials, browser Profiles, or customer messages.
- Never bypass platform verification.
- Never infer missing protocol behavior.
- Never share state across Profiles.
- Never log full message content or Secret Material.
- Use Synthetic Fixtures only.
- Fail closed when state is uncertain.

## Current implementation

None.

No `worker.message` runtime package is approved.

No transport, WebSocket, message model, persistence model, Migration, background worker, API, or scheduler behavior is added.

## Execution boundary

The project-owner approval completes T1 only.

T2 is the next executable task.

T2 must be performed in a separate execution.

No runtime implementation may begin before T2-T5 are completed and all approved decisions are recorded in this document.
