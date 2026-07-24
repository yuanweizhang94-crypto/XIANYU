# CHG-0004 Proposal

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Purpose

Prepare a formally reviewable boundary for receiving Xianyu customer-inquiry messages without opening a real WebSocket or accessing a real platform account.

## Target capability

- `CAP-XY-MESSAGE`

## Current authorization

The project owner approved CHG-0004 for controlled, one-task-at-a-time execution.

T1 through T4 are complete.

The canonical terminology and the transport, authentication, risk-control, ordering, deduplication, idempotency, replay, persistence, transaction, concurrency, retention, and Migration boundaries are approved.

T5 is the next executable task and must be performed separately.

No Worker, Adapter, Repository, Service, connection lifecycle, reconnect scheduler, runtime failure model, runtime implementation, real WebSocket, external network access, real account access, real customer-message processing, database table, ORM model, Migration file, capability binding, Ready-for-review, auto-merge, or merge is authorized.

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

## T3 security and transport outcome

- A future message transport may use WebSocket only through a separately implemented secure transport adapter.
- A future external WebSocket connection must use `wss://`.
- TLS certificate and hostname verification must remain enabled.
- Plaintext `ws://`, disabled certificate verification, insecure fallback, and guessed protocol behavior are prohibited.
- The transport endpoint must come from trusted, approved configuration and must not come from customer content, Platform Message data, external identifiers, URLs received from the platform, or arbitrary operator input.
- Authentication remains owned by the account and future Secure Storage boundaries, not by the message domain.
- CAP-XY-MESSAGE may consume only operation-scoped authentication material resolved for an exact Profile and explicit message-receiving purpose.
- Authentication material must not be persisted, cached across operations, serialized, logged, returned, or shared across Profiles.
- A future connection may proceed only when Credential Resolution is `RESOLVED`, Operation Authorization is `AUTHORIZED`, and Risk Decision is `ALLOWED`.
- Every other credential, permission, authorization, verification, and risk state fails closed.
- Platform verification, CAPTCHA, device verification, face verification, SMS verification, and risk controls must never be bypassed.
- Reconnect must preserve exact Profile and Credential ownership and must never switch Profiles or Credentials.
- Reconnect is prohibited for invalid, expired, revoked, denied, verification-required, or risk-blocked states.
- Acknowledgement remains a transport receipt concept and does not imply business processing, persistence, reply, uniqueness, or completion.
- No acknowledgement may be guessed when protocol semantics are unknown.
- Message Content, Secret Material, authentication headers, full external identifiers, and raw transport payloads are prohibited from logs and diagnostics.
- Only Synthetic Message Fixtures may be used in tests.

## T4 ordering, deduplication, and persistence outcome

- No global Platform Message ordering guarantee is approved.
- No cross-Profile or cross-Conversation ordering guarantee is approved.
- Transport arrival order, local receipt timestamps, Platform timestamps, external identifiers, and Delivery Cursors are not authoritative Platform ordering.
- Out-of-order and late Message Events must not be silently discarded.
- T4 does not approve automatic event reordering.
- A future deterministic display order may use local receipt time followed by Local Message Identifier, but this order is presentation-only.
- Local Conversation Identifier uses UUID version 4.
- Local Message Identifier uses UUID version 4.
- Deduplication is always scoped to one exact Profile.
- A future approved Transport Adapter may provide an opaque Profile-scoped Delivery Identity.
- Delivery Identity must not contain Message Content, Secret Material, raw Transport Frames, or cross-Profile state.
- Deduplication Decision values are `NEW`, `DUPLICATE`, `INDETERMINATE`, and `CONFLICT`.
- `NEW` creates one local Message Record and one Delivery Attempt Record.
- `DUPLICATE` does not create another Message Record but may record another Delivery Attempt.
- `INDETERMINATE` must not discard the event or falsely collapse it into another Message Record.
- `CONFLICT` must fail closed and must not overwrite existing data.
- Platform Message Identifier alone is not an approved global deduplication key.
- Message Content must not be hashed or compared to invent a deduplication identity.
- The existing Core SQLite, SQLAlchemy, and Alembic infrastructure remains the only approved local persistence boundary.
- A future minimal persistence projection may contain Profile-scoped Conversation, Message, and Delivery Attempt records.
- Message Content is restricted to normalized UTF-8 plain text with a maximum approved length of 4096 characters.
- HTML execution, attachment storage, media bytes, arbitrary JSON, BLOB, raw payload, raw frame, generic metadata, properties, extras, or unrestricted key-value storage are prohibited.
- All persistent Conversation, Message, Delivery Attempt, and external-reference data remains Profile-scoped.
- Persistence mutations require an explicit transaction.
- Duplicate and conflict checks must occur inside the same logical transaction as persistence.
- Messages and Delivery Attempts are append-only records except for separately approved lifecycle metadata.
- Application startup must not auto-migrate.
- Migration must remain explicit.
- A non-empty downgrade must fail closed unless a separately approved data-preserving downgrade exists.
- T4 creates no table, ORM model, Migration, Repository, Service, Worker, Adapter, API, or runtime file.

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
- No runtime implementation during T4.
- No database table or Migration during T4.
- No ORM, Repository, or Service during T4.
- No real Message Content during T4.
- No attachment, media, binary, HTML, JSON payload, or raw Transport Frame persistence.
- No global ordering guarantee.
- No content-hash deduplication.
- No cross-Profile deduplication.
- No automatic data-retention or purge job.
- No runtime implementation before T5 is complete.

## Security boundary

- Do not bypass platform verification or risk controls.
- Do not guess protocol, permission, credential, acknowledgement, ordering, or reconnect behavior.
- Do not commit or log real message payloads or customer data.
- Use Synthetic Fixtures only.
- Stop when authorization, protocol, ownership, credential, or risk state is uncertain.

## Execution boundary

Only one unfinished task may be executed at a time.

T1 through T4 are complete.

T5 is the next executable task.

T5 must not begin in the same execution.

T4 approves ordering, deduplication, idempotency, replay, persistence, transaction, concurrency, retention, and Migration principles only.

Worker, Adapter, Repository, Service, process ownership, connection lifecycle, reconnect scheduling, failure ownership, observability ownership, testing ownership, concrete physical schema, Migration file, and runtime implementation remain deferred.
