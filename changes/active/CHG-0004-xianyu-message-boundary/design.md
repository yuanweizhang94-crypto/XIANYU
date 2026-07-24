# CHG-0004 Design

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Design state

CHG-0004 remains approved for controlled, task-by-task execution.

T1 through T4 are complete.

The canonical terminology and the transport, authentication, risk-control, ordering, deduplication, idempotency, replay, persistence, transaction, concurrency, retention, and Migration boundaries are approved.

T5 is the next executable task.

No Worker ownership model, Adapter ownership model, Repository or Service ownership model, connection lifecycle model, failure model, observability model, physical database schema, Migration file, or runtime implementation has been approved.

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

## Approved ordering boundary

No global Platform Message ordering guarantee is approved.

No ordering relationship may be inferred across Profiles.

No ordering relationship may be inferred across Conversations.

Within one Profile and one Conversation:

1. Transport arrival order is observational only.

2. Local receipt timestamp is observational only.

3. Platform timestamp is untrusted external metadata.

4. Platform Message Identifier is not an ordering value.

5. Platform Conversation Identifier is not an ordering value.

6. Delivery Cursor is not an ordering guarantee unless a later verified protocol explicitly defines that semantic.

7. Acknowledgement order is not Message Event order.

8. Database insertion order is not Platform Message order.

9. Reconnect or Replay may deliver an older Message Event after a newer Message Event.

10. Out-of-order and late Message Events must not be silently discarded.

11. T4 does not approve automatic reordering.

12. Business processing must not assume that the most recently received event is the newest Platform Message.

13. Missing or conflicting ordering metadata must not prevent safe local receipt unless another approved security boundary rejects the event.

14. A future deterministic presentation order may use local receipt time followed by Local Message Identifier.

15. Presentation order does not establish Platform order, causal order, customer intent order, or reply order.

## Approved local identifiers

### Local Conversation Identifier

A repository-local UUID version 4 identifier for exactly one persisted Conversation within exactly one Profile.

It is not an external Platform Conversation Identifier.

It is not authentication, authorization, ordering, or deduplication evidence.

### Local Message Identifier

A repository-local UUID version 4 identifier for exactly one persisted Message Record within exactly one Profile.

It is not a Platform Message Identifier.

It is not a Delivery Identity.

It is not proof that the Message Event is unique, authorized, ordered, or acknowledged.

### Local Delivery Attempt Identifier

A repository-local UUID version 4 identifier for one persisted Delivery Attempt Record.

It represents local evidence of an observed Delivery Attempt.

It does not prove that the external platform created a distinct delivery.

All local identifiers must be generated without external network access and must remain Profile-scoped through their ownership relationships.

## Delivery Identity boundary

Delivery Identity is an opaque, non-secret, Profile-scoped value that a future approved Transport Adapter may provide when verified protocol semantics support stable redelivery identification.

Delivery Identity rules:

1. It belongs to exactly one Profile.

2. It may identify repeated deliveries of the same approved transport item.

3. It must not be shared across Profiles.

4. It must not contain Message Content.

5. It must not contain Secret Material.

6. It must not contain raw Cookie or Token values.

7. It must not contain a raw Transport Frame.

8. It must not contain a browser path or Session Material.

9. It must not be derived solely from Message Content.

10. It must not be derived solely from a timestamp.

11. It must not be derived solely from Participant Reference.

12. It must not be assumed globally unique.

13. It must not be used unless its stability semantics are known and approved.

14. If a verified protocol later establishes that Platform Message Identifier is stable for redelivery within one Profile, a Transport Adapter may map that identifier into Delivery Identity.

15. T4 does not approve any concrete Delivery Identity format or extraction algorithm.

## Deduplication Decision

The approved conceptual Deduplication Decision values are:

```text
NEW
DUPLICATE
INDETERMINATE
CONFLICT
```

### NEW

No existing Profile-scoped Message Record has the same approved Delivery Identity.

A future operation may create:

- one Message Record;
- one Delivery Attempt Record;
- the required Profile and Conversation ownership references.

### DUPLICATE

An existing Profile-scoped Message Record has the same approved Delivery Identity and compatible immutable event metadata.

A duplicate delivery:

- must not create another Message Record;
- may create another Delivery Attempt Record;
- must return or reference the existing Local Message Identifier;
- must not trigger a second business action solely because delivery repeated;
- must not overwrite the original Message Record.

### INDETERMINATE

No reliable approved Delivery Identity exists.

An indeterminate event:

- must not be silently discarded;
- must not be collapsed using Message Content;
- must not be collapsed using timestamp proximity;
- must not be collapsed using Participant Reference alone;
- must not be collapsed using Platform Conversation Identifier alone;
- may create a separate Message Record;
- must record that deduplication identity was unavailable.

The approved bias is against false-positive collapse and silent message loss.

### CONFLICT

The same approved Delivery Identity is presented with incompatible immutable Profile, Conversation, sender, Message Content, or external-reference data.

A conflict:

- must fail closed;
- must not overwrite the existing Message Record;
- must not create a second Message Record using the conflicting identity;
- must roll back the current persistence transaction;
- must return only a sanitized non-secret reason;
- must not acknowledge success.

## Deduplication scope and idempotency

Deduplication is scoped by:

```text
exact Profile Identifier
approved Delivery Identity
```

A Delivery Identity from one Profile must never deduplicate a Message Event from another Profile.

Platform Message Identifier alone is not an approved global deduplication key.

Platform Conversation Identifier alone is not an approved deduplication key.

Participant Reference alone is not an approved deduplication key.

Message Content or a Message Content hash is not an approved deduplication key.

Timestamp proximity is not an approved deduplication key.

A future message-persistence operation is idempotent with respect to Message Record creation when the same Profile-scoped approved Delivery Identity and compatible immutable event metadata are submitted repeatedly.

Idempotency means:

- at most one Message Record for that approved Profile-scoped Delivery Identity;
- repeated delivery may add Delivery Attempt evidence;
- repeated operation returns the existing Local Message Identifier;
- existing immutable Message data is not overwritten;
- a conflicting retry fails closed.

T4 does not approve idempotency for message sending, reply generation, acknowledgement transmission, or external side effects.

## Replay boundary

Replay is not automatically a new business message.

Replay is not automatically a duplicate.

Replay classification depends on an approved Profile-scoped Delivery Identity.

If replay has the same approved Delivery Identity and compatible immutable metadata, the Deduplication Decision is `DUPLICATE`.

If replay has no approved Delivery Identity, the Deduplication Decision is `INDETERMINATE`.

If replay reuses an approved Delivery Identity with conflicting immutable metadata, the Deduplication Decision is `CONFLICT`.

No replay-retention time window is approved.

No time-based assumption may automatically convert a previous Message Event into a new Message Event.

No Replay record may cross Profile ownership.

Delivery Cursor must not be used as replay identity unless a verified protocol later explicitly approves that semantic.

## Conceptual persistence boundary

The existing `CAP-CORE-DATABASE` SQLite, SQLAlchemy, and Alembic infrastructure remains the only approved local persistence boundary.

T4 approves conceptual persistence for:

### Conversation Record

Minimal Profile-scoped projection of one Conversation.

It may contain:

- Local Conversation Identifier;
- Profile Identifier ownership;
- Account Reference ownership;
- optional untrusted Platform Conversation Identifier;
- created timestamp;
- separately approved lifecycle metadata.

### Message Record

Minimal Profile-scoped projection of one accepted Message Event.

It may contain:

- Local Message Identifier;
- Local Conversation Identifier;
- Profile Identifier ownership;
- optional Platform Message Identifier;
- optional approved Delivery Identity;
- Participant Reference;
- normalized text Message Content;
- local receipt timestamp;
- optional untrusted Platform timestamp;
- Deduplication Decision evidence required for the stored record;
- separately approved lifecycle metadata.

### Delivery Attempt Record

Append-only local evidence of one observed Delivery Attempt.

It may contain:

- Local Delivery Attempt Identifier;
- Local Message Identifier;
- Profile Identifier ownership;
- local attempt timestamp;
- sanitized transport outcome class;
- sanitized non-secret reason code;
- optional attempt number;
- separately approved non-secret correlation identifier.

The exact table names, column names, SQLAlchemy classes, indexes, constraints, foreign-key names, and Alembic Revision remain deferred to T5 and T6.

## Message Content persistence boundary

Message Content is customer data.

The minimal approved local projection supports normalized UTF-8 plain text only.

Rules:

1. Text must be valid Unicode.

2. The maximum approved normalized length is 4096 characters.

3. Empty or whitespace-only content is invalid.

4. Internal whitespace may be preserved.

5. Line endings may be normalized to `\n`.

6. Content is treated as inert text.

7. Content must not be executed as HTML, Markdown, script, template, SQL, shell input, or command input.

8. HTML rendering is not approved.

9. Attachment storage is not approved.

10. Media download is not approved.

11. Binary storage is not approved.

12. BLOB storage is not approved.

13. Arbitrary JSON payload storage is not approved.

14. Raw Transport Frame storage is not approved.

15. Generic `payload`, `metadata`, `properties`, `extras`, `context`, or unrestricted key-value columns are prohibited.

16. Message Content must not appear in logs, metrics, traces, audit events, exception text, PR text, or test snapshots.

17. Only Synthetic Message Fixtures may supply content during CHG-0004 implementation and testing.

18. Real customer-message access remains unauthorized.

## Persistence ownership and relational integrity

1. Every Conversation Record belongs to exactly one Profile.

2. Every Message Record belongs to exactly one Profile.

3. Every Message Record belongs to exactly one Conversation Record owned by the same Profile.

4. Every Delivery Attempt Record belongs to exactly one Message Record owned by the same Profile.

5. Cross-Profile foreign-key relationships are prohibited.

6. A Platform Conversation Identifier must not establish Profile ownership.

7. A Platform Message Identifier must not establish Profile ownership.

8. Delivery Identity must not establish Profile ownership by itself.

9. Profile ownership must be explicit on every persistence mutation.

10. Missing, ambiguous, conflicting, or cross-Profile ownership fails closed.

11. Deleting or changing one Profile must not mutate another Profile's Conversation, Message, or Delivery Attempt records.

12. No global current Profile or global current Conversation is allowed.

## Transaction and concurrency boundary

A future accepted-message persistence operation must use one explicit logical transaction covering:

1. exact Profile ownership validation;

2. Conversation lookup or creation;

3. Deduplication Decision;

4. Message Record creation or existing-record selection;

5. Delivery Attempt Record creation;

6. approved state updates;

7. commit or complete rollback.

Rules:

- Deduplication checks and Message Record creation must occur in the same transaction.
- Duplicate and conflict checks must occur inside the same logical transaction as persistence.
- A conflict must roll back the complete operation.
- Partial Conversation, Message, or Delivery Attempt writes are prohibited.
- Repository methods must not independently commit.
- Logical transaction ownership is deferred to T5.
- Profile-scoped uniqueness must be protected by database constraints where applicable.
- Concurrent duplicate creation must resolve to one Message Record or a sanitized conflict.
- Lost-update protection is required for mutable lifecycle metadata.
- Message and Delivery Attempt immutable fields must not be overwritten by concurrent operations.
- T4 does not select an optimistic-lock field, isolation level, locking primitive, retry count, or Repository API.

## Retention and deletion boundary

CHG-0004 approves no automatic retention duration.

CHG-0004 approves no automatic purge job.

CHG-0004 approves no Scheduler-based deletion.

CHG-0004 approves no background cleanup Worker.

During the local synthetic boundary:

- records may remain until explicitly deleted through a future approved operation;
- no real customer data is accessed;
- no production retention claim is made.

Before real customer-message access is authorized, a separate reviewed change must approve:

- retention duration;
- deletion rights;
- operator deletion workflow;
- Profile deletion behavior;
- legal and business retention requirements;
- backup behavior;
- export behavior;
- audit requirements;
- secure deletion limitations.

T6 must not implement automatic deletion or retention scheduling.

## Delivery Cursor persistence boundary

Delivery Cursor remains opaque.

Because no verified real transport protocol is approved:

- T4 does not approve Delivery Cursor as ordering evidence;
- T4 does not approve Delivery Cursor as deduplication identity;
- T4 does not approve Delivery Cursor as acknowledgement evidence;
- T4 does not approve durable recovery semantics;
- T4 does not approve persistence of a real external Delivery Cursor.

A future local model may accept an optional Synthetic Message Fixture cursor for boundary testing, but it must remain non-authoritative and must not control ordering, deduplication, authorization, or Profile ownership.

## Migration boundary

Future message persistence must use the existing Core Alembic infrastructure.

Rules:

1. Migration must be explicit.

2. Application startup must not automatically migrate.

3. Migration history must remain linear.

4. No table may be created with `create_all`.

5. Migration fixtures must contain no real customer data.

6. Migration fixtures must contain no Secret Material.

7. Migration fixtures must contain no raw Transport Frames.

8. Upgrade must create only the separately approved minimal schema.

9. Empty downgrade may remove the message schema.

10. Non-empty downgrade must fail closed unless a separately approved data-preserving downgrade exists.

11. Downgrade failure must preserve existing records.

12. Exact Revision identifier and physical Migration remain deferred to T6.

13. T4 creates no Migration file.

## Persistence prohibitions

The following must not be persisted by the CHG-0004 minimal boundary:

- Cookie;
- Token;
- Secret Material;
- Session Material;
- authorization Header;
- browser state;
- browser user-data paths;
- raw handshake request;
- raw handshake response;
- raw Transport Frame;
- arbitrary JSON payload;
- attachments;
- media bytes;
- executable HTML;
- shell commands;
- SQL fragments;
- full network error payloads;
- raw provider errors;
- unrestricted metadata or property bags;
- data belonging to another Profile.

## Decisions deferred after T4

### Deferred to T5

- Package and module ownership.
- Domain module ownership.
- Persistence module ownership.
- Repository ownership.
- Service ownership.
- Transport Adapter ownership.
- Credential-resolution interface ownership.
- Worker ownership.
- Connection lifecycle ownership.
- Reconnect scheduling ownership.
- Transaction coordinator ownership.
- Failure and restart ownership.
- Observability ownership.
- Testing ownership.
- Concrete lifecycle states.
- Concrete exception hierarchy.
- Concrete timeout, retry, backoff, and jitter values.
- Concrete public package surface.
- Import-safety boundary.
- Graceful shutdown behavior.

### Deferred to T6

- All runtime code.
- Exact table names.
- Exact column names.
- Exact indexes and constraints.
- SQLAlchemy models.
- Alembic Revision.
- Repository implementation.
- Service implementation.
- Domain classes and Enums.
- UUID generation implementation.
- Text normalization implementation.
- Deduplication implementation.
- Transaction implementation.
- Concurrency implementation.
- Synthetic local transport boundary implementation.

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

T1 through T4 are complete.

T5 is the next executable task.

T5 must be performed in a separate execution.

T4 approves ordering, deduplication, idempotency, replay, persistence, transaction, concurrency, retention, and Migration boundaries only.

This execution does not authorize Worker, Adapter, Repository, Service, database schema, Migration file, WebSocket, network access, real message access, or runtime implementation.
