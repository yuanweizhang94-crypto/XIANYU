# CHG-0004 Proposal

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Purpose

Prepare a formally reviewable boundary for receiving Xianyu customer-inquiry messages without opening a real WebSocket or accessing a real platform account.

## Target capability

- `CAP-XY-MESSAGE`

## Current authorization

The project owner approved CHG-0004 for controlled, one-task-at-a-time execution.

T1 through T3 are complete.

The canonical terminology and the transport, authentication, Credential-resolution, authorization, permission, risk-control, TLS, reconnect, acknowledgement, and redaction boundaries are approved.

T4 is the next executable task and must be performed separately.

No ordering guarantee, deduplication identity, idempotency algorithm, replay-retention policy, persistence model, database schema, Migration, runtime ownership model, runtime implementation, real WebSocket, external network access, real account access, customer-message processing, capability binding, Ready-for-review, auto-merge, or merge is authorized.

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
- No real WebSocket connection during T3.
- No DNS, HTTP, WebSocket, browser, subprocess, or external network access during T3.
- No real Endpoint, Cookie, Token, Header, Subprotocol, Payload schema, heartbeat frame, or acknowledgement frame is selected during T3.
- No ordering guarantee during T3.
- No deduplication or persistence decision during T3.
- No runtime implementation before T4 and T5 are complete.

## Security boundary

- Do not bypass platform verification or risk controls.
- Do not guess protocol, permission, credential, acknowledgement, ordering, or reconnect behavior.
- Do not commit or log real message payloads or customer data.
- Use Synthetic Fixtures only.
- Stop when authorization, protocol, ownership, credential, or risk state is uncertain.

## Execution boundary

Only one unfinished task may be executed at a time.

T1 through T3 are complete.

T4 is the next executable task.

T4 must not begin in the same execution.

T3 approves security and transport boundaries only.

Ordering, deduplication, idempotency, replay retention, persistence, local identifiers, database schema, Migration, Worker ownership, lifecycle, failure handling, testing ownership, and runtime implementation remain deferred.
