# CHG-0004 Design

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Design state

CHG-0004 remains approved for controlled, task-by-task execution.

T1 through T3 are complete.

The canonical message terminology and the transport, authentication, Credential-resolution, authorization, permission, risk-control, TLS, reconnect, acknowledgement, and redaction boundaries are approved.

T4 is the next executable task.

No ordering guarantee, deduplication algorithm, idempotency model, replay-retention model, persistence model, runtime ownership model, or runtime implementation has been approved.

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

## Approved transport boundary

The long-term architecture direction permits a future WebSocket transport for receiving messages.

T3 approves only the security boundary around such a future transport.

T3 does not approve an Endpoint, protocol version, WebSocket subprotocol, request Header set, Cookie format, Token format, Payload schema, heartbeat frame, acknowledgement frame, reconnect interval, or concrete client library.

A future external connection must satisfy all of the following:

1. The connection uses `wss://`.

2. TLS certificate verification remains enabled.

3. TLS hostname verification remains enabled.

4. Plaintext `ws://` is prohibited.

5. Disabling certificate verification is prohibited.

6. Accepting an invalid, expired, self-signed, mismatched, or otherwise untrusted certificate is prohibited unless a separate reviewed design explicitly approves a trusted private certificate authority.

7. The Endpoint must come from trusted, approved configuration.

8. The Endpoint must not come from Message Content, Platform Message data, Participant data, an External Identifier, a redirect supplied by an untrusted source, or arbitrary customer-controlled input.

9. The transport must not silently follow an unexpected redirect or switch to a different host.

10. The transport must not downgrade from secure to insecure transport.

11. The transport must not infer undocumented Endpoint, Header, Subprotocol, heartbeat, acknowledgement, or payload behavior.

12. Unknown or conflicting protocol requirements fail closed.

13. A future transport must remain scoped to exactly one Profile and one Account Reference for its complete connection lifetime.

14. One Profile's connection state, authentication material, Delivery Cursor, acknowledgement state, or reconnect state must not be reused by another Profile.

15. T3 creates no Socket, WebSocket, HTTP client, network request, Endpoint configuration, or runtime adapter.

## Authentication and Credential boundary

Authentication material remains outside the message domain.

`CAP-XY-MESSAGE` does not own Cookie, Token, Secret Material, Session Material, browser state, login state, Credential storage, or Credential resolution.

A future message-receiving operation may request operation-scoped authentication material only through a separately approved Credential and Secure Storage boundary.

A future request for authentication material must include:

- an explicit Profile Identifier;
- the Account Reference owned by that Profile;
- the Credential Reference owned by that Profile;
- the explicit operation purpose `RECEIVE_MESSAGES`;
- an explicit authorization decision;
- an explicit risk decision.

Future resolved authentication material must satisfy:

1. It is resolved only for the exact Profile.

2. It is resolved only for the explicit `RECEIVE_MESSAGES` operation.

3. It is held in memory for the shortest practical period.

4. It is not persisted.

5. It is not written to application configuration.

6. It is not written to ordinary environment variables.

7. It is not placed in command-line arguments.

8. It is not placed in URL paths or query parameters.

9. It is not cached across operations.

10. It is not serialized.

11. It is not included in Message Events or Conversation References.

12. It is not included in logs, errors, metrics, traces, audit events, snapshots, test output, PR text, or API responses.

## Credential Resolution Status

The approved conceptual Credential Resolution Status values are:

```text
UNRESOLVED
RESOLVED
MISSING
UNAVAILABLE
INVALID
EXPIRED
REVOKED
```

- `UNRESOLVED`: no safe resolution result exists.
- `RESOLVED`: operation-scoped authentication material was safely returned for the exact Profile and purpose.
- `MISSING`: the Profile-owned Credential Reference or referenced material does not exist.
- `UNAVAILABLE`: the secure boundary cannot safely provide material.
- `INVALID`: the material is structurally or semantically invalid.
- `EXPIRED`: the material is no longer current.
- `REVOKED`: use has explicitly been withdrawn.

Only `RESOLVED` may satisfy the Credential-resolution precondition.

Every other status denies connection and fails closed.

`RESOLVED` alone does not authorize a connection.

## Operation Authorization Status

The approved conceptual Operation Authorization Status values are:

```text
UNKNOWN
AUTHORIZED
VERIFICATION_REQUIRED
PERMISSION_DENIED
```

- `UNKNOWN`: permission or authorization has not been established.
- `AUTHORIZED`: the exact Profile is explicitly permitted to perform `RECEIVE_MESSAGES`.
- `VERIFICATION_REQUIRED`: platform or human verification is required.
- `PERMISSION_DENIED`: the operation is not permitted.

Only `AUTHORIZED` may satisfy the authorization precondition.

`UNKNOWN` must never be interpreted as `AUTHORIZED`.

`VERIFICATION_REQUIRED` must stop the operation.

`PERMISSION_DENIED` must stop the operation.

T3 does not implement authorization code.

## Risk Decision

The approved conceptual Risk Decision values are:

```text
UNKNOWN
ALLOWED
VERIFICATION_REQUIRED
BLOCKED
```

- `UNKNOWN`: no safe risk decision exists.
- `ALLOWED`: no known risk control prohibits the exact operation at the current decision point.
- `VERIFICATION_REQUIRED`: a platform or human verification step is required.
- `BLOCKED`: risk controls prohibit the operation.

Only `ALLOWED` may satisfy the risk precondition.

`UNKNOWN`, `VERIFICATION_REQUIRED`, and `BLOCKED` deny the operation and fail closed.

`ALLOWED` is not proof that the Platform Account, Message Content, external identifiers, or transport payload is authentic or safe.

## Connection authorization invariant

A future message-receiving connection may proceed only when all conditions are true:

```text
Profile ownership is exact and unambiguous
Credential Resolution Status = RESOLVED
Operation Authorization Status = AUTHORIZED
Risk Decision = ALLOWED
Transport protocol requirements are known and approved
TLS and hostname verification are enabled
```

If any condition is absent, unknown, stale, conflicting, or changes during the operation, the operation must stop and fail closed.

There must be no implicit default Profile.

There must be no global current account.

There must be no global current Credential.

There must be no cross-Profile fallback.

There must be no fallback to an older, alternate, or previously successful Credential.

Previous connection success must not establish current authorization.

Credential presence must not establish authorization.

Transport connectivity must not establish authorization.

## Platform verification and risk-control boundary

The future system must not bypass:

- CAPTCHA;
- face verification;
- device verification;
- SMS verification;
- QR-code verification;
- account confirmation;
- platform permission controls;
- platform risk controls;
- rate limits;
- access denials;
- verification challenges.

When verification is required:

1. Stop the current operation.

2. Do not automatically solve or bypass the challenge.

3. Do not switch Profiles.

4. Do not switch Credentials.

5. Do not replay hidden browser state.

6. Do not import browser directories.

7. Do not retry until an explicit external state change has been recorded through a separately approved process.

T3 does not approve any verification-resolution workflow.

## Reconnect and retry safety

Reconnect is a transport recovery concept.

Reconnect must not be treated as permission to change Profile, Account Reference, Credential Reference, Endpoint, operation purpose, or risk decision.

A future reconnect may be considered only after a transient transport failure and only if all approved connection preconditions are evaluated again.

Reconnect is prohibited when any of the following applies:

- Credential Resolution Status is `MISSING`;
- Credential Resolution Status is `UNAVAILABLE`;
- Credential Resolution Status is `INVALID`;
- Credential Resolution Status is `EXPIRED`;
- Credential Resolution Status is `REVOKED`;
- Operation Authorization Status is `UNKNOWN`;
- Operation Authorization Status is `VERIFICATION_REQUIRED`;
- Operation Authorization Status is `PERMISSION_DENIED`;
- Risk Decision is `UNKNOWN`;
- Risk Decision is `VERIFICATION_REQUIRED`;
- Risk Decision is `BLOCKED`;
- Profile ownership is missing, ambiguous, conflicting, or changed;
- protocol requirements are unknown;
- TLS validation failed;
- hostname validation failed.

A future reconnect policy must:

1. Be bounded.

2. Use delay and backoff.

3. Avoid a tight retry loop.

4. Avoid synchronized reconnect storms.

5. Re-evaluate Credential, Authorization, Risk, Profile ownership, and Endpoint trust before each attempt.

6. Stop permanently for the current operation when a non-transient denial occurs.

The exact retry count, delay, jitter, backoff formula, timeout, and lifecycle ownership remain deferred to T5.

## Acknowledgement safety boundary

Acknowledgement remains a transport-level receipt concept.

A future acknowledgement may be emitted only when:

- the official and approved transport protocol requires it;
- acknowledgement semantics are known;
- the transport item is associated with the exact Profile;
- Profile ownership is valid;
- Credential, Authorization, and Risk preconditions remain valid;
- the transport envelope is syntactically acceptable;
- the item is not rejected for a security or protocol violation.

Acknowledgement must not mean:

- authentication succeeded;
- Message Content is safe;
- business processing succeeded;
- persistence succeeded;
- deduplication succeeded;
- ordering is correct;
- a reply was generated;
- a reply was sent;
- the message will not be replayed;
- the delivery is unique;
- the customer request is complete.

The system must not guess an acknowledgement frame, timing, identifier, or protocol.

Malformed, cross-Profile, unauthorized, verification-required, risk-blocked, protocol-unknown, or security-rejected transport items must not be acknowledged unless an official verified protocol explicitly requires a safe negative acknowledgement.

Concrete acknowledgement frames and timing remain deferred to T6 after an approved protocol source exists.

## Logging, errors, and redaction

Future logs, traces, metrics, errors, and audit events may contain only approved non-secret fields such as:

```text
event type
Profile Identifier
operation purpose
transport state class
sanitized outcome class
non-secret reason code
attempt number
timestamp
non-secret correlation identifier
```

The following are prohibited:

```text
Message Content
raw Platform Message payload
raw transport frame
Cookie
Token
Secret Material
Session Material
authorization Header
full Credential Reference
full Platform Message Identifier
full Platform Conversation Identifier
full Participant Reference
full external Endpoint containing sensitive values
URL query parameters containing sensitive values
browser local storage
browser session storage
browser user-data path
QR-code material
SMS verification data
raw provider error
raw handshake request
raw handshake response
```

Rules:

1. Secret Material must never appear in logs, traces, metrics, exceptions, audit events, snapshots, fixtures, CI output, or PR text.

2. Message Content must never appear in logs or diagnostics.

3. Full Credential References must not be logged.

4. Full external identifiers must not be logged.

5. Raw transport frames must not be logged.

6. Provider and network errors must be sanitized before crossing their boundary.

7. Redaction failure must suppress the unsafe diagnostic and fail closed.

8. Debug mode must not weaken these rules.

9. Tests must not snapshot or assert raw Secret Material or real Message Content.

10. T3 adds no logging implementation.

## Approved non-secret reason-code classes

Future sanitized outcomes may use conceptual non-secret classes such as:

```text
PROFILE_OWNERSHIP_INVALID
CREDENTIAL_UNRESOLVED
CREDENTIAL_MISSING
CREDENTIAL_UNAVAILABLE
CREDENTIAL_INVALID
CREDENTIAL_EXPIRED
CREDENTIAL_REVOKED
AUTHORIZATION_UNKNOWN
VERIFICATION_REQUIRED
PERMISSION_DENIED
RISK_UNKNOWN
RISK_BLOCKED
ENDPOINT_UNTRUSTED
TLS_VERIFICATION_FAILED
PROTOCOL_UNSPECIFIED
TRANSPORT_UNAVAILABLE
TRANSPORT_RETRY_EXHAUSTED
ACKNOWLEDGEMENT_UNSPECIFIED
```

These are documentation concepts only.

T3 does not create an Enum, Exception class, response schema, API contract, log implementation, or transport implementation.

## Security testing boundary

1. Only Synthetic Message Fixtures may be used.

2. Synthetic values must be visibly artificial.

3. Fixtures must not be derived from real Platform Accounts, customers, Message Content, browser data, Cookies, Tokens, Credentials, or Session Material.

4. Tests must not open a Socket.

5. Tests must not perform DNS resolution.

6. Tests must not perform HTTP or WebSocket requests.

7. Tests must not access browser user-data directories.

8. Tests must not access an operating-system Credential Store.

9. Tests must not read real environment credentials.

10. Tests must not require a real Endpoint.

11. Tests must validate documentation, generated state, repository boundaries, and absence of implementation only.

12. T3 does not add permanent runtime tests.

## Decisions deferred after T3

### Deferred to T4

- Ordering scope and guarantees.
- Out-of-order handling.
- Deduplication identity.
- Deduplication algorithm.
- Idempotency keys.
- Replay detection.
- Replay retention window.
- Persistence requirements.
- Database schema.
- Migration requirements.
- Local Message Identifier format.
- Local Conversation Identifier format.
- Storage of external identifiers.
- Delivery Cursor durability.
- Message Content retention and deletion.
- Transaction and concurrency behavior.

### Deferred to T5

- Module ownership.
- Transport adapter ownership.
- Worker ownership.
- Credential-resolution interface ownership.
- Connection lifecycle ownership.
- Reconnect scheduling ownership.
- Process and concurrency isolation.
- Failure and restart ownership.
- Observability ownership.
- Testing ownership.
- Timeout values.
- Retry counts.
- Backoff and jitter values.
- Graceful shutdown behavior.

### Deferred to T6

- All runtime code.
- Concrete WebSocket client.
- Concrete Endpoint.
- Concrete Header and authentication injection.
- Concrete Subprotocol.
- Concrete handshake.
- Concrete heartbeat frames.
- Concrete acknowledgement frames.
- Concrete payload parsing.
- Concrete error types.
- Concrete reconnect implementation.

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

T1 through T3 are complete.

T4 is the next executable task.

T4 must be performed in a separate execution.

T3 approves security, transport, authentication, Credential-resolution, permission, risk-control, reconnect, acknowledgement, and redaction boundaries only.

This execution does not authorize ordering guarantees, deduplication, idempotency, replay retention, persistence, database changes, Worker or Adapter implementation, network access, real message access, or runtime implementation.
