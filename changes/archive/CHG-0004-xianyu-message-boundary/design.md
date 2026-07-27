# CHG-0004 Design

Status: ARCHIVED
Change ID: CHG-0004-xianyu-message-boundary

## Design state

CHG-0004 remains VERIFYING for final review.

T1 through T9 are complete.

There is no next task in CHG-0004.

The local, synchronous, Profile-scoped, Synthetic Message receiving boundary is implemented and frozen.

CAP-XY-MESSAGE remains verified.

PR #4 is Ready for review, open and unmerged.

No Reviewer was manually requested.

Auto-merge, merge, close, source-branch deletion, archive, and next Change creation are not authorized.

Merge requires separate explicit authorization against an exact PR HEAD.

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

## Runtime ownership summary

CAP-XY-MESSAGE remains owned by the `worker.message` capability namespace recorded in the Capability Registry.

The approved future Python package is:

```text
app/xianyu_system/worker/message/
```

The corresponding import namespace is:

```text
xianyu_system.worker.message
```

The `worker` name identifies capability and orchestration ownership.

It does not mean that CHG-0004 creates or starts:

- a background thread;
- an asyncio event loop;
- a subprocess;
- a daemon;
- a Scheduler Job;
- a browser Worker;
- an external-platform Worker;
- a polling loop;
- a real WebSocket;
- a network connection.

T5 approves only the future ownership and package boundary.

T5 must not create the package or modify the Capability Registry.

CAP-XY-MESSAGE remains `planned`, unbound, and without evidence paths.

## Approved future package boundary

T6 may create only the following minimal Message capability package:

```text
app/xianyu_system/worker/message/__init__.py
app/xianyu_system/worker/message/domain.py
app/xianyu_system/worker/message/persistence.py
app/xianyu_system/worker/message/service.py
app/xianyu_system/worker/message/transport.py
app/xianyu_system/worker/message/worker.py
```

The existing file:

```text
app/xianyu_system/worker/__init__.py
```

must remain unchanged unless a separately verified technical requirement proves that a minimal compatibility edit is necessary.

T6 must not create:

```text
client.py
websocket.py
network.py
listener.py
consumer.py
daemon.py
scheduler.py
tasks.py
background.py
provider.py
credential.py
browser.py
api.py
router.py
schemas.py
handlers.py
plugins.py
events.py
event_bus.py
unit_of_work.py
base_repository.py
```

T6 must not create a second package for the same Message capability.

## domain.py ownership

`domain.py` owns pure local Message domain concepts and invariants.

It may own future implementations of:

- Local Conversation Identifier;
- Local Message Identifier;
- Local Delivery Attempt Identifier;
- Delivery Identity;
- Participant Reference;
- normalized Message Content;
- local receipt timestamp;
- untrusted Platform timestamp;
- Deduplication Decision;
- Worker Lifecycle State;
- sanitized domain errors;
- immutable domain values;
- approved validation and normalization rules.

`domain.py` may use only Python standard-library value types and local pure helpers.

`domain.py` must not import SQLAlchemy, FastAPI, Transport, Worker, Core Database, application state, environment settings, Socket libraries, HTTP clients, WebSocket clients, browser libraries, Scheduler libraries, or Credential providers.

Importing `domain.py` must not register ORM metadata, open a database, create a Socket, read credentials, start a Worker, create a thread, or access the network.

## persistence.py ownership

`persistence.py` owns the future SQLAlchemy relational projection and exactly one concrete Message Repository.

It may own:

- Conversation, Message, and Delivery Attempt ORM mappings;
- table-level constraints and indexes approved in T6;
- Profile-scoped uniqueness enforcement;
- Repository methods that receive an explicit Session;
- flush-only persistence operations;
- sanitized persistence exceptions.

`persistence.py` must use the existing Core Database Base, Engine, Session, and Alembic boundaries.

Repository methods may flush but must not independently commit.

`persistence.py` must not own Worker lifecycle, Transport behavior, Credential resolution, network access, WebSocket access, API routes, Scheduler Jobs, message sending, reply generation, or external acknowledgements.

## service.py ownership

`service.py` owns accepted-message use cases and logical transaction coordination.

The Message Service owns the logical transaction.

It may coordinate:

- Profile ownership validation;
- Conversation lookup or creation;
- Deduplication Decision;
- Message Record creation or duplicate selection;
- Delivery Attempt recording;
- conflict rollback;
- sanitized use-case outcomes.

Service code must not open a WebSocket, create a Socket, perform DNS, perform HTTP, access a browser, read Secret Material, resolve real Credentials, start a background Worker, register a Scheduler Job, send a message, or reply to a customer.

## transport.py ownership

`transport.py` owns transport-neutral values and Protocol interfaces only.

It may define future local Protocol surfaces for caller-provided Synthetic Message Delivery values.

It must not implement a real Adapter.

It must not import Persistence.

It must not open a Socket, WebSocket, HTTP client, browser, DNS resolver, Credential store, thread, subprocess, or Scheduler Job.

It must not contain Endpoint constants, Cookie names, Token handling, provider URLs, handshake frames, heartbeat frames, acknowledgement frames, or retry loops.

## worker.py ownership

`worker.py` owns the in-process, Profile-scoped Message Worker lifecycle and orchestration.

The T6 Message Worker is synchronous.

The Worker is explicitly constructed by its caller.

The Worker is explicitly started and explicitly stopped.

The Worker may accept a caller-provided Synthetic Message Delivery only while `RUNNING`.

The Worker does not own process startup, application startup, FastAPI lifespan, operating-system signals, Scheduler Jobs, background threads, subprocesses, asyncio task creation, browser control, real Transport Adapter startup, or network connection management.

## Approved dependency direction

Approved import direction for the future package:

```text
domain.py <- transport.py
domain.py <- persistence.py
domain.py <- service.py
transport.py <- worker.py
service.py <- worker.py
persistence.py <- service.py
```

Rules:

1. `domain.py` is the lowest-level module.
2. `transport.py` may import Domain but must not import Persistence or Service.
3. `persistence.py` may import Domain and Core Database only.
4. `service.py` may import Domain and Persistence.
5. `worker.py` may import Domain, Transport, and Service.
6. Transport code must not import Persistence.
7. Persistence code must not import Transport.
8. Domain code must not import Transport, Persistence, Service, Worker, Core Database, FastAPI, or SQLAlchemy.
9. No module may import from API or Web packages.
10. No module may import browser, network, Credential Provider, Scheduler, or external platform integration modules in T6.

## Public package and import-safety boundary

Future package imports must be side-effect safe.

Importing `xianyu_system.worker.message` or `xianyu_system.worker.message.domain` must not:

- register ORM metadata;
- create a database Engine;
- open a database connection;
- run Alembic;
- read environment credentials;
- read Cookie, Token, Secret, or Session Material;
- instantiate a Worker;
- start a Worker;
- create a Socket;
- perform DNS resolution;
- perform HTTP;
- open a WebSocket;
- access a browser;
- create a thread;
- create a subprocess;
- register a Scheduler Job;
- start a background loop.

## Approved Worker Lifecycle States

The approved Worker Lifecycle States are:

```text
STOPPED
STARTING
RUNNING
STOPPING
BLOCKED
FAILED
```

- `STOPPED`: no delivery may be processed.
- `STARTING`: local preconditions are being checked.
- `RUNNING`: one caller-provided Synthetic Message Delivery may be accepted.
- `STOPPING`: shutdown is in progress and no new delivery may begin.
- `BLOCKED`: a security, ownership, authorization, risk, protocol, TLS, or deduplication-conflict boundary stopped the Worker.
- `FAILED`: an unexpected internal or persistence failure stopped the Worker.

Worker lifecycle state is local process state only.

Worker lifecycle state is not persisted.

Worker lifecycle state is not authentication, authorization, Credential, ordering, deduplication, replay, acknowledgement, or durable recovery evidence.

Process restart begins with the Worker in `STOPPED`.

## Approved Worker Lifecycle Transitions

Approved transitions:

```text
STOPPED -> STARTING
STARTING -> RUNNING
STARTING -> BLOCKED
STARTING -> FAILED
RUNNING -> STOPPING
RUNNING -> BLOCKED
RUNNING -> FAILED
STOPPING -> STOPPED
BLOCKED -> STOPPED
FAILED -> STOPPED
```

No other transition is approved.

A reset from `BLOCKED` or `FAILED` must be explicit and local.

A reset must not automatically retry delivery, reconnect, resolve Credentials, bypass risk controls, or restore previous transport state.

## Worker ownership invariants

One Message Worker instance belongs to exactly one Profile Identifier.

One Message Worker instance belongs to exactly one Account Reference owned by that Profile.

Worker ownership is immutable after construction.

There is no global Worker.

There is no implicit Worker.

There is no global current Profile.

There is no global current Account.

There is no global current Credential.

There is no global current Conversation.

Worker state, Repository state, Service state, Transport state, Delivery Identity, Cursor state, and mutable lifecycle state must not be shared across Profiles.

## Worker concurrency boundary

One Worker instance may process at most one delivery at a time.

Only one delivery may be in flight for one Worker instance.

Concurrent or re-entrant delivery processing on the same Worker must fail closed with a sanitized busy outcome.

The busy outcome must not expose Message Content, Secret Material, full external identifiers, raw Transport Frames, raw provider errors, or raw database errors.

T6 must not create threads, subprocesses, asyncio background tasks, Scheduler Jobs, polling loops, heartbeat loops, or automatic delivery loops.

## Transaction coordinator ownership

The Message Service owns the logical transaction.

The logical transaction must include Profile ownership validation, deduplication, Message Record selection or creation, Delivery Attempt recording, and commit or complete rollback.

Repository methods may flush but must not independently commit.

Transport code does not own transactions.

Worker code invokes Service use cases but must not bypass transaction coordination.

A failed persistence operation must roll back completely.

## Transport and Credential ownership boundary

Transport owns transport-neutral values and Protocol interfaces only.

Transport does not own Credential storage, Credential resolution, Authorization, Risk, TLS verification, Endpoint discovery, retry policy, reconnect policy, or real platform access.

Credential Resolution remains outside CAP-XY-MESSAGE and must be provided only by a separately approved boundary.

T6 may use only Synthetic Message Fixtures and caller-provided synthetic delivery values.

T6 must not read Cookie, Token, Secret Material, Session Material, browser Profiles, operating-system Credential stores, ordinary environment credentials, or real account data.

## Approved sanitized error hierarchy

T5 approves these conceptual sanitized error classes only:

```text
MESSAGE_ERROR
MESSAGE_VALIDATION_ERROR
MESSAGE_OWNERSHIP_ERROR
MESSAGE_AUTHORIZATION_ERROR
MESSAGE_RISK_ERROR
MESSAGE_PROTOCOL_ERROR
MESSAGE_DEDUPLICATION_CONFLICT
MESSAGE_BUSY
MESSAGE_PERSISTENCE_ERROR
MESSAGE_INTERNAL_ERROR
```

These are documentation concepts only until T6 is separately authorized.

No error may expose Message Content, Secret Material, full external identifiers, raw Transport Frames, raw provider errors, authentication data, Cookie, Token, Session Material, browser paths, or raw database errors.

## Approved failure disposition

- Event-local invalid synthetic input may be rejected without stopping a valid Worker when Profile ownership and security invariants remain valid.
- Profile ownership failures place the Worker in `BLOCKED`.
- Credential-boundary failures place the Worker in `BLOCKED`.
- Authorization-boundary failures place the Worker in `BLOCKED`.
- Risk-boundary failures place the Worker in `BLOCKED`.
- Protocol-boundary failures place the Worker in `BLOCKED`.
- TLS-boundary failures place the Worker in `BLOCKED`.
- Deduplication Conflict failures place the Worker in `BLOCKED`.
- Persistence failures place the Worker in `FAILED`.
- Unexpected internal failures place the Worker in `FAILED`.
- Busy or re-entrant delivery attempts fail closed with a sanitized busy outcome.

Blocked and Failed Workers do not automatically retry or restart.

## Retry and reconnect boundary

No automatic reconnect or retry is approved in T6.

```text
automatic reconnect attempts = 0
automatic processing retries = 0
```

A future real transport reconnect policy requires a separate reviewed change.

A reset from `BLOCKED` or `FAILED` is not retry, reconnect, or delivery replay authorization.

## Graceful shutdown boundary

Stop is explicit and graceful.

While `STOPPING`, no new delivery may begin.

An in-flight operation must commit completely or roll back completely before the Worker becomes `STOPPED`.

T6 owns no operating-system signal handler.

T6 must not modify FastAPI application startup, application shutdown, scheduler startup, scheduler shutdown, or global process lifecycle hooks.

## Observability boundary

Future observability may report only non-secret state classes, sanitized outcome classes, safe counters, timestamps, Profile-scoped non-secret correlation identifiers, and lifecycle state transitions.

Message Content, Secret Material, raw Transport Frames, authentication data, Cookie, Token, Session Material, browser paths, full external identifiers, raw provider errors, and raw database errors must not appear in logs, metrics, traces, audit output, test snapshots, CI output, or PR text.

Observability must not create external telemetry, network export, files, logs directories, or background exporters in T6.

## Testing ownership boundary

T6 tests may cover only local, synchronous, Profile-scoped, Synthetic Message receiving behavior.

Tests must block or prove absence of Socket creation, DNS, HTTP, WebSocket, browser access, subprocesses, threads, Scheduler Jobs, automatic retry, automatic reconnect, real Credential access, real account access, and real customer data.

Tests must verify import safety for the package and Domain module.

Tests must verify that CAP-XY-MESSAGE remains unbound until a later capability-evidence task.

## Approved T6 implementation boundary

T6 may implement only the local, synchronous, Profile-scoped, Synthetic Message receiving boundary.

T6 may create only the approved future package and minimal modules listed in T5.

T6 may implement Domain, Persistence, Service, Transport Protocol interfaces, and Worker orchestration only within the approved local boundary.

T6 must not implement real WebSocket, real Endpoint, DNS, HTTP, external network access, Credential Provider, Cookie or Token handling, browser integration, background Worker, threads, subprocesses, Scheduler Jobs, automatic retry, automatic reconnect, message sending, reply, API, Web UI, real customer data, attachment persistence, media persistence, arbitrary JSON persistence, raw Transport Frame persistence, automatic retention, purge, capability binding, Ready-for-review, auto-merge, or merge.

T6 must be separately authorized against the exact T5 HEAD.

## Required decisions before runtime implementation

- Exact physical database schema.
- Exact table names.
- Exact column names.
- Exact indexes and constraints.
- SQLAlchemy model names.
- Alembic Revision identifier.
- Repository method names.
- Service method names.
- Domain class and Enum names.
- Exception class names.
- Synthetic transport Protocol signatures.
- Worker constructor and method signatures.
- Test evidence layout.

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

The local package `xianyu_system.worker.message` exists.

The package contains exactly:

```text
__init__.py
domain.py
persistence.py
service.py
transport.py
worker.py
```

Migration `0003_xianyu_message_boundary` exists with parent `0002_xianyu_account_boundary`.

The migration creates exactly these local Message tables:

```text
xianyu_message_conversations
xianyu_message_records
xianyu_message_delivery_attempts
```

The implementation provides:

- pure Domain values and sanitized errors;
- transport-neutral Synthetic Message Delivery values;
- SQLAlchemy relational projection;
- one concrete Message Repository;
- Message Service transaction coordination;
- a local, synchronous, explicitly started and stopped Message Worker;
- NEW, DUPLICATE, INDETERMINATE, and CONFLICT handling;
- complete rollback for conflicts and persistence failures;
- one in-flight delivery per Worker;
- zero automatic reconnect attempts;
- zero automatic processing retries.

No real WebSocket, Endpoint, DNS, HTTP, network access, Credential Provider, Cookie, Token, browser integration, background thread, subprocess, Scheduler Job, message sending, reply generation, API, Web UI, real account access, or real customer-data behavior is implemented.

## T6 corrective implementation record

A repeated Delivery Identity is compatible only when the associated persisted Conversation has the same Platform Conversation Identifier as the incoming delivery.

A Platform Conversation Identifier mismatch is a Deduplication Conflict.

Invalid Message input is event-local and may leave a valid Worker RUNNING.

Profile ownership, authorization, risk, protocol, and Deduplication Conflict failures place the Worker in BLOCKED.

Persistence and internal failures place the Worker in FAILED.

BLOCKED and FAILED Workers cannot be stopped directly to bypass recovery.

Only explicit reset changes BLOCKED or FAILED to STOPPED.

Conversation is part of the import-safe public Message package surface.

The correction changes no database schema, Migration, retry count, reconnect count, transport, network, Credential, or capability evidence boundary.

## Execution boundary

T1 through T6 are complete.

T7 is the next executable task.

T7 must be performed in a separate execution.

The local implementation exists, but CAP-XY-MESSAGE remains planned and unbound until T8.

Real transport, external platform access, real Credential access, customer-message processing, message sending, Ready-for-review, auto-merge, and merge remain unauthorized.

## T7 permanent coverage implementation record

T7 permanent Message test coverage is complete.

Added permanent tests:

- `tests/unit/test_message_domain.py` with 12 explicit top-level tests.
- `tests/unit/test_message_service.py` with 9 explicit top-level tests.
- `tests/unit/test_message_worker.py` with 8 explicit top-level tests.
- `tests/contract/test_message_persistence.py` with 8 explicit top-level tests.
- `tests/contract/test_message_security.py` with 5 explicit top-level tests.

Updated `tests/unit/test_import_safety.py` without changing its three-test function count so package import safety includes the Message Package, Message Domain, and transport-neutral synthetic delivery values while keeping persistence metadata out of package import.

The tests cover Domain normalization and immutable values, UUID4 local identifier generation, NEW, DUPLICATE, INDETERMINATE, Content Conflict, Conversation Conflict, Profile/Account scope, Service transaction ownership, rollback, Worker lifecycle, failure-state mapping, explicit reset, one in-flight delivery, re-entry, graceful stop, the three-table schema, Migration lineage, Foreign Keys, database constraints, empty downgrade, non-empty downgrade fail-closed behavior, Repository no-commit behavior, public surface, import isolation, no external side effects, sanitized errors, and contract order independence.

No Message Runtime, Migration, Registry, Capability Specification, dependency, or CI file was modified by T7. T8 remains the next task.

## T7 corrective hardening record

T7 corrective hardening closes coverage gaps before T8 while preserving the T7 task state.

Worker coverage now proves real re-entry by causing the active fake Service operation to call the same Worker again. The nested call fails with `WorkerBusy` before a second Service operation begins, the outer operation completes, and the Worker remains `RUNNING`.

Graceful-stop coverage now uses deterministic `threading.Event` and finite-timeout test threads. The test observes `STOPPING`, verifies new delivery is rejected during `STOPPING`, releases the in-flight operation, joins all test threads, and verifies final `STOPPED` state with no remaining thread.

Persistence Contract coverage now directly exercises `MessageRepository` add methods inside an explicit Session, verifies flush visibility, verifies no Repository commit call, verifies rollback removes uncommitted Conversation, Message, and Delivery Attempt rows, and verifies ownership and UTC timestamp round-trip. Real SQLite Service coverage now verifies NEW, DUPLICATE, INDETERMINATE, Content Conflict, and Conversation Conflict atomicity.

Schema and constraint coverage now includes approved column types, lengths, nullable flags, primary keys, foreign keys, unique constraints, check constraints, prohibited fields, ownership scope, nullable Delivery Identities, Platform Message Identifier reuse, Message Content constraints, decision constraints, and Attempt outcome/number constraints.

Message-only downgrade coverage now explicitly targets `0002_xianyu_account_boundary`, preserving Account table/data on empty downgrade and failing closed with revision/table/row preservation on non-empty downgrade.

Security coverage now runs Message Service and Message Worker in an isolated process while network, DNS, subprocess, Home-directory, and production thread-start entry points are blocked. Lazy package import evidence verifies Persistence, Service, and Worker are initially unloaded.

No Runtime, Migration, Registry, Capability Specification, dependency, or CI file was modified.

## T7 final evidence follow-up record

T7 final evidence follow-up closes the remaining evidence gates before T8 while preserving the T7 task state.

Persistence Contract evidence now verifies every approved Message Check Constraint by name and normalized SQL semantics in both ORM projection and reflected SQLite schema. The evidence covers UUID text length, Account Reference trimming and length, nullable platform identifiers, nullable Delivery Identity, participant validation, Message Content length and trimmed non-empty semantics, persisted decision values, Attempt outcomes, positive Attempt numbers, nullable reason codes, and nullable correlation identifiers.

Foreign Key evidence now verifies constrained columns, referred tables, referred columns, and `ON DELETE RESTRICT` for the Conversation-to-Profile, Message-to-Conversation owner, and Delivery Attempt-to-Message owner relationships in both projection and SQLite reflection.

Migration evidence now covers source restrictions, exact revision/down-revision metadata, only three Message table create/drop operations, Alembic CLI `upgrade head` against a temporary SQLite database, and Alembic offline SQL generation without creating the offline database file.

Database constraint evidence now covers the remaining ownership, content, decision, outcome, reason, correlation, uniqueness, nullable-value, and scope cases, including duplicate attempt numbers and different Account scope for the same Delivery Identity.

Security evidence now verifies initially unloaded public package state and actual lazy Domain, Transport, Service, Persistence, and Worker resolution. The isolated Worker flow covers NEW, DUPLICATE, INDETERMINATE, Content Conflict, Conversation Conflict, reset, restart, and stop while external side-effect entry points remain blocked.

Dedicated Message test files and active acceptance evidence are now checked independently for UTF-8 decoding, absence of BOM, Synthetic Fixtures, sensitive value patterns, customer data, and cleanup escape hatches.

No Runtime, Migration, Registry, Capability Specification, dependency, or CI file was modified.

## T7 exact contract evidence completion record

The exact T7 evidence completion keeps the approved runtime, schema, migration, registry, capability specification, dependencies, and CI unchanged. Persistence contract evidence now isolates each expected IntegrityError in a fresh Connection and Transaction, directly covers empty, blank, padded, over-limit, unknown-enum, scoped Delivery Identity, duplicate Attempt Number, and nullable-value cases, and scans offline SQL for external URL, Credential, browser-profile, and customer-data text. Security contract evidence now records row counts before and after both isolated conflict paths and verifies final isolated counts of one Conversation, two Messages, and three Delivery Attempts. Dedicated Message evidence files are scanned for email-like, plus-phone, standalone long-number, Credential-like, customer-data, raw-frame, production-account, live-account, real-account, and cleanup escape-hatch patterns.

## T7 sensitive-scan correction record

The Security Contract scanner now reads each approved Message evidence file as raw bytes, rejects UTF-8 BOM, strictly decodes UTF-8, and scans the complete decoded Source with `scan_source = source`.

The scanner does not delete lines, filter lines, replace Source content, mask Source content, or allowlist target files before scanning. It preserves the six approved scan targets exactly.

The scanner covers email-like values, plus-phone values with common separators and at least eight digits, standalone long numbers beginning at eleven digits, Credential-like forms, customer and raw-frame phrase forms, production-account and live-account phrase forms, real-Xianyu-account phrase forms, and cleanup escape hatches.

Runtime positive controls prove each detector category can detect its intended input. Scanner failure diagnostics report only the file path and detector category, not the matched value.

## T7 quote-independent forbidden-phrase evidence

Forbidden-phrase detection now uses direct lowercase substring matching against complete Source.

No quote-aware regular expression, lookbehind, lookahead, line filter, replacement, masking rule, or file allowlist is used.

The same detector is exercised against:

- unquoted forbidden phrases;
- single-quoted forbidden phrases;
- double-quoted forbidden phrases;
- forbidden phrases embedded in surrounding text;
- every approved Message evidence file.

Detector failure output contains only the file path and category.

Persistence Contract scanner definitions use runtime string composition to avoid embedding prohibited phrase samples as continuous repository literals.

## T8 evidence candidate

The registered evidence contains seven implementation paths and ten test paths.

All paths are safe, repository-relative, concrete, duplicate-free files.

The Evidence Candidate contains no Runtime or Migration behavior change.

Complete verification must execute on the committed Candidate SHA.

The Candidate SHA must become last_verified_commit only after verification succeeds.

## T8 verification outcome

The exact CAP-XY-MESSAGE evidence paths were verified by Candidate SHA `49498e6f30944883c1a0a5a504932bbd02fc86de`.

Complete local verification and Candidate CI passed.

The capability moved from implementing to verified.

active_change was cleared.

last_verified_commit records the Candidate SHA.

T9 has not started.

## T8 final-CI shallow-checkout correction design

The active acceptance verification for the verified CAP-XY-MESSAGE Candidate now uses a single offline helper with the same semantics as the permanent Capability Registry Contract.

The helper first validates that the Candidate SHA has the expected forty-character lowercase hexadecimal form.

It then asks Git whether the Candidate commit object is present in the local object database.

When the Candidate object is present, the helper requires strict `merge-base --is-ancestor` success against HEAD before the test can pass.

When the Candidate object is absent, the helper asks Git whether the repository is shallow and allows continuation only if Git returns `true`; this covers depth-one pull-request merge checkouts.

The helper captures Git output for these probes so an expected shallow missing-object case does not write fatal Git diagnostics into normal test logs.

The correction does not use a provider environment-variable bypass, skip, xfail, network request, history fetch, file allowlist, or unconditional success path.

Complete repositories still require the Evidence Candidate object and strict HEAD-ancestor verification.

Missing Candidate history is accepted only when Git explicitly reports a shallow repository.

No Workflow, Runtime, Migration, Registry, Capability Specification, Project State, task, dependency, or evidence path is modified.

## T9 final review state

- T1 through T9 are complete.
- There is no next task in CHG-0004.
- CHG-0004 remains VERIFYING while PR #4 is under review.
- T9 Ready Candidate SHA is `1cc4de90e88f607ab30b475232c7fa7ef01b8f14`.
- Implementation and evidence are frozen.
- PR #4 is Ready for review, open and unmerged.
- No Reviewer was manually requested.
- Auto-merge remains disabled.
- Any further repository modification requires explicit correction authorization.
- Merge requires separate explicit authorization against an exact PR HEAD.
- Archive and next-change creation occur only after successful merge.

## Merge and archive record

PR #4 was merged into `main`.

Merge commit: `bab7a1a86239cb4dba9b2f7dc8db0ff33bc80dc6`.

Merged feature head: `0cfd719dff5d472e9e5ac26bf720afc7efb74e9f`.

CHG-0004 is archived after successful merge.

CAP-XY-MESSAGE remains verified.

Its `last_verified_commit` remains `49498e6f30944883c1a0a5a504932bbd02fc86de`.

Its seven implementation paths remain unchanged.

Its ten verification paths remain unchanged except that the CHG-0004 acceptance evidence now uses the archive location.

Archiving CHG-0004 does not change Runtime behavior.

Archiving does not reverify CAP-XY-MESSAGE.

Archiving does not authorize CHG-0005 implementation.

CHG-0005 is a DRAFT preparation only.
