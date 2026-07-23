# CHG-0004 Proposal

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Purpose

Prepare a formally reviewable boundary for receiving Xianyu customer-inquiry messages without opening a real WebSocket or accessing a real platform account.

## Target capability

- `CAP-XY-MESSAGE`

## Current authorization

The project owner approved CHG-0004 for controlled, one-task-at-a-time execution.

T1 and T2 are complete.

The message, conversation, participant, and delivery terminology is finalized.

T3 is the next executable task and must be performed separately.

No transport protocol, authentication, Credential handling, risk-control behavior, ordering guarantee, deduplication algorithm, persistence model, runtime implementation, real WebSocket, external network access, real account access, customer-message processing, capability binding, Ready-for-review, auto-merge, or merge is authorized.

## T2 terminology outcome

- Platform Message means the real message object that exists on the external platform.
- Message Event means the repository-boundary concept representing one observed inbound message occurrence.
- Message Content means customer-provided text, media, attachment, or equivalent payload data.
- Platform Message Identifier means an optional opaque identifier supplied by the external platform.
- Conversation means a logical grouping of related Message Events scoped to exactly one Profile.
- Conversation Reference means the repository-owned non-secret logical reference to one Conversation within one Profile.
- Platform Conversation Identifier means optional untrusted external reference metadata.
- Participant Reference means an opaque non-secret reference to a conversation participant.
- Delivery Attempt means one transport attempt to deliver a Message Event to the receiving boundary.
- Delivery Cursor means an opaque transport position whose ordering and durability semantics remain undecided.
- Acknowledgement means a transport-level receipt signal and does not mean business processing, persistence, reply, or completion.
- Duplicate Delivery means more than one Delivery Attempt representing the same underlying Platform Message.
- Replay means redelivery of an already observed Message Event during recovery or reconnection.
- Ordering Boundary means the scope within which relative event ordering may later be defined.
- Synthetic Message Fixture means artificial test-only data that represents no real account, participant, conversation, message, credential, or customer.

## Goals

- Define canonical terminology for message events, conversations, delivery cursors, acknowledgements, and duplicate delivery.
- Define ownership between Profile, account boundary, and a future per-account message worker.
- Define synthetic transport and adapter contracts.
- Define ordering, deduplication, replay, reconnect, and idempotency boundaries.
- Define fail-closed behavior.
- Define future persistence and observability questions.
- Define acceptance criteria before implementation.

## Non-goals

- No real Xianyu WebSocket connection.
- No external network request.
- No real Xianyu login.
- No Cookie, Token, Secret, Session Material, browser Profile, customer data, or platform credential.
- No message sending or automated reply.
- No background worker.
- No Scheduler Job.
- No database table or Migration.
- No Repository or Service.
- No API or web UI.
- No dependency addition.
- No capability binding.
- No implementation before explicit approval.
- No transport implementation during T2.
- No authentication or Credential resolution decision during T2.
- No ordering guarantee during T2.
- No deduplication key or algorithm during T2.
- No persistence or retention decision during T2.
- No runtime implementation before T3-T5 are completed.

## Security boundary

- Do not bypass platform verification or risk controls.
- Do not guess protocol, permission, credential, acknowledgement, ordering, or reconnect behavior.
- Do not commit or log real message payloads or customer data.
- Use Synthetic Fixtures only.
- Stop when authorization, protocol, ownership, credential, or risk state is uncertain.

## Execution boundary

Only one unfinished task may be executed at a time.

T1 and T2 are complete.

T3 is the next executable task.

T3 must not begin in the same execution.

T2 finalizes terminology only.

Transport, authentication, risk control, ordering, deduplication, persistence, worker ownership, lifecycle, failure, testing, and runtime implementation remain deferred.
