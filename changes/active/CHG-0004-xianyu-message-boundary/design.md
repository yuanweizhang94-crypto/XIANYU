# CHG-0004 Design

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Design state

CHG-0004 remains approved for controlled, task-by-task execution.

T1 and T2 are complete.

The canonical message, conversation, participant, and delivery terminology is finalized.

T3 is the next executable task.

No transport protocol, authentication model, risk-control model, ordering guarantee, deduplication algorithm, persistence model, runtime ownership model, or runtime implementation has been approved.

## Architecture context

- One worker per Xianyu account.
- One local Profile boundary per account.
- WebSocket is the future message-receiving transport direction.
- Fixed rules take priority over AI fallback.

These directions do not authorize a real transport implementation.


## Canonical terminology

### Platform Message

The real message object that exists on the external Xianyu platform.

A Platform Message is outside the repository boundary.

CHG-0004 does not connect to the platform, retrieve, inspect, acknowledge, modify, or reply to a real Platform Message.

The term Platform Message must be used when referring to an externally existing message.

### Message Event

The repository-boundary concept representing one observed inbound message occurrence associated with exactly one Profile and one Account Reference.

Message Event is a terminology concept only.

T2 does not create a runtime class, database entity, serialized schema, event bus object, or transport payload.

A Message Event does not prove that its source is authentic, authorized, ordered, unique, persisted, or safe to process.

### Message Content

Customer-provided text, media, attachment, structured payload, or equivalent business content associated with a Platform Message.

Message Content is customer data.

T2 does not read, store, log, redact, transform, retain, or test real Message Content.

Security and redaction requirements are deferred to T3.

Persistence and retention requirements are deferred to T4.

### Platform Message Identifier

An optional opaque identifier supplied by or associated with the external platform.

It is untrusted reference metadata.

It must not be treated as authentication, authorization, proof of ownership, a local canonical identity, or a guaranteed deduplication key.

Its format, uniqueness, stability, and persistence remain undecided.

### Conversation

A logical grouping of related Message Events scoped to exactly one Profile and one Account Reference.

A Conversation must not span multiple Profiles.

A Conversation is not a WebSocket connection, browser session, worker process, database transaction, or authenticated platform session.

T2 does not decide whether a Conversation is persisted.

### Conversation Reference

A repository-owned, non-secret logical reference to one Conversation within exactly one Profile.

A Conversation Reference is not authentication data and does not contain Session Material.

Its runtime representation, identifier format, persistence, creation, and lifecycle are deferred.

### Platform Conversation Identifier

An optional opaque identifier supplied by or associated with the external platform.

It is untrusted external reference metadata.

It must not replace Profile ownership or a future repository-local Conversation Reference.

It must not be assumed globally unique across Profiles.

### Participant Reference

An opaque, non-secret reference to one participant associated with a Conversation.

A Participant Reference is not proof of identity, authentication, authorization, account ownership, or customer consent.

T2 does not define participant storage, identity resolution, enrichment, or cross-conversation correlation.

### Delivery Attempt

One transport attempt to present a Message Event to the future receiving boundary.

Multiple Delivery Attempts may refer to the same underlying Platform Message.

A Delivery Attempt does not imply successful validation, acknowledgement, persistence, business processing, or reply.

Transport mechanics are deferred to T3.

### Delivery Cursor

An opaque transport position or continuation reference associated with future message delivery.

T2 assigns no ordering, monotonicity, uniqueness, durability, replay, persistence, or recovery guarantee to a Delivery Cursor.

A Delivery Cursor is not a Message Identifier, Conversation Identifier, deduplication key, or acknowledgement.

### Acknowledgement

A future transport-level signal that a delivery boundary has received or accepted a transport item according to a separately approved protocol.

Acknowledgement does not mean:

- the Platform Message is authentic;
- Message Content is safe;
- business processing succeeded;
- persistence succeeded;
- a reply was sent;
- the message will not be replayed;
- the delivery was unique.

The exact acknowledgement protocol and timing are deferred to T3.

### Duplicate Delivery

More than one Delivery Attempt representing the same underlying Platform Message or Message Event.

T2 defines the term only.

The deduplication identity, key, comparison rules, storage, retention window, and conflict behavior are deferred to T4.

### Replay

Redelivery of an already observed Message Event during recovery, reconnect, retry, or transport resumption.

Replay does not automatically mean corruption or a new business message.

Replay detection and processing behavior are deferred to T3 and T4.

### Ordering Boundary

The scope within which relative Message Event ordering may later be defined.

T2 does not approve a global, per-Profile, per-Conversation, per-participant, or transport-level ordering guarantee.

Ordering guarantees and out-of-order behavior are deferred to T4.

### Synthetic Message Fixture

Artificial test-only data that does not represent a real Platform Account, Profile credential, participant, customer, Conversation, Platform Message, Message Content, browser directory, or Session Material.

Only Synthetic Message Fixtures may be used until later explicit authorization.


## Terminology invariants

1. Every Message Event belongs to exactly one Profile.

2. Every Message Event is associated with exactly one Account Reference owned by that Profile.

3. Every Conversation and Conversation Reference belongs to exactly one Profile.

4. Message Events, Conversations, Conversation References, Participant References, Delivery Cursors, and mutable delivery state must not be shared across Profiles.

5. Platform Message Identifier and Platform Conversation Identifier are untrusted external metadata.

6. External identifiers must not establish Profile ownership.

7. Acknowledgement is a transport concept and must not be used as a synonym for business success, persistence, reply, or completion.

8. Delivery Cursor must not be used as Message identity, Conversation identity, or a deduplication key without a later approved decision.

9. Duplicate Delivery and Replay must not automatically be classified as a new business message.

10. Message Content is customer data and remains outside T2 processing.

11. Missing, ambiguous, conflicting, or cross-Profile ownership information must fail closed.

12. No T2 terminology proves that a message is authentic, authorized, unique, ordered, persisted, safe, or actionable.

13. Only Synthetic Message Fixtures may be used while real message access remains unauthorized.

## Decisions deferred after T2

### Deferred to T3

- WebSocket or transport protocol.
- Authentication and Credential resolution.
- Permission and authorization checks.
- Risk-state handling.
- Connection establishment and shutdown.
- Heartbeat behavior.
- Reconnect and backoff.
- Transport acknowledgement protocol and timing.
- Transport error classification.
- Sensitive logging and redaction.
- Handling of invalid, expired, denied, verification-required, or risk-blocked state.

### Deferred to T4

- Ordering guarantees.
- Out-of-order behavior.
- Deduplication identity and algorithm.
- Idempotency keys.
- Replay detection and retention window.
- Persistence requirements.
- Database schema and Migration.
- Conversation and Message local identifier formats.
- Storage of external identifiers.
- Message Content retention or deletion.
- Cursor durability and recovery state.

### Deferred to T5

- Module ownership.
- Worker ownership.
- Adapter ownership.
- Process and concurrency isolation.
- Runtime lifecycle.
- Profile loading and unloading.
- Failure and restart boundaries.
- Observability ownership.
- Testing ownership.

### Deferred to T6

- All runtime implementation.

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

T1 and T2 are complete.

T3 is the next executable task.

T3 must be performed in a separate execution.

T2 defines terminology only.

This execution does not authorize transport, authentication, Credential resolution, risk controls, ordering guarantees, deduplication, persistence, database changes, worker changes, API changes, network access, real message access, or runtime implementation.
