# CHG-0004 Proposal

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Purpose

Prepare a formally reviewable boundary for receiving Xianyu customer-inquiry messages without opening a real WebSocket or accessing a real platform account.

## Target capability

- `CAP-XY-MESSAGE`

## Current authorization

The project owner approved CHG-0004 for controlled, one-task-at-a-time execution.

T1 through T6 are complete.

The local, synchronous, Profile-scoped, Synthetic Message receiving boundary is implemented.

T7 is the next executable task and must be performed separately.

CAP-XY-MESSAGE remains planned and unbound until the separate capability evidence task.

No real WebSocket, Endpoint, DNS, HTTP, external network access, Credential Provider, Cookie handling, Token handling, browser integration, background thread, subprocess, Scheduler Job, automatic retry, automatic reconnect, message sending, reply generation, API, Web UI, real account access, real customer-message processing, capability binding, Ready-for-review, auto-merge, or merge is authorized in this execution.

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

## T5 worker ownership, lifecycle, and failure outcome

- CAP-XY-MESSAGE remains owned by the `worker.message` capability namespace.
- The approved future package path is `app/xianyu_system/worker/message/`.
- The approved future import namespace is `xianyu_system.worker.message`.
- The approved minimal future modules are `domain.py`, `persistence.py`, `service.py`, `transport.py`, and `worker.py`.
- `domain.py` owns pure Message domain concepts, validation, immutable values, lifecycle states, and sanitized domain errors.
- `persistence.py` owns the SQLAlchemy relational projection and one concrete Message Repository.
- `service.py` owns accepted-message use cases and logical transaction coordination.
- `transport.py` owns transport-neutral delivery values and Protocol interfaces only.
- `worker.py` owns the in-process, Profile-scoped Message Worker lifecycle and orchestration.
- The `worker` namespace does not mean a background thread, subprocess, Scheduler Job, daemon, browser Worker, or external platform connection.
- The T6 Message Worker is synchronous and explicitly invoked by its caller.
- T6 creates no automatic start, reconnect, retry, polling, heartbeat, background loop, thread, subprocess, or scheduler behavior.
- One Message Worker instance belongs to exactly one Profile and one Account Reference.
- Worker state, Repository state, Service state, Transport state, Delivery Identity, Cursor state, and mutable lifecycle state must not be shared across Profiles.
- The approved Worker Lifecycle States are `STOPPED`, `STARTING`, `RUNNING`, `STOPPING`, `BLOCKED`, and `FAILED`.
- A Worker may accept a delivery only while `RUNNING`.
- Worker lifecycle state is local process state and is not persisted as durable authorization or recovery evidence.
- Process restart begins with the Worker in `STOPPED`.
- No implicit Worker, global current Profile, global current Account, global current Credential, or global current Conversation is approved.
- Only one delivery may be in flight for one Worker instance.
- Concurrent or re-entrant delivery processing on the same Worker must fail closed with a sanitized busy outcome.
- Message Service owns the logical transaction.
- Repository methods may flush but must not independently commit.
- Transport code must not import Persistence.
- Domain code must not import SQLAlchemy, FastAPI, Transport, Worker, Core Database, or application state.
- Importing the package or Domain module must not register ORM metadata, open a database, read environment credentials, start a Worker, create a Socket, or access the network.
- No automatic reconnect or retry is approved in T6.
- A future real transport reconnect policy requires a separate reviewed change.
- Profile ownership, Credential, Authorization, Risk, protocol, TLS, and security violations place the Worker in `BLOCKED`.
- Unexpected internal or persistence failures place the Worker in `FAILED`.
- Event-local invalid synthetic input may be rejected without stopping a valid Worker when Profile ownership and security invariants remain valid.
- No failure may expose Message Content, Secret Material, full external identifiers, raw Transport Frames, raw provider errors, or authentication data.
- Stop is explicit and graceful.
- While `STOPPING`, no new delivery may begin.
- An in-flight transaction must complete successfully or fully roll back before the Worker becomes `STOPPED`.
- T5 creates no runtime files.

## T6 local implementation outcome

- The local package `xianyu_system.worker.message` now exists at `app/xianyu_system/worker/message/`.
- The package contains exactly `__init__.py`, `domain.py`, `persistence.py`, `service.py`, `transport.py`, and `worker.py`.
- `domain.py` implements pure local Message domain values, sanitized errors, `DeduplicationDecision`, and `WorkerLifecycleState`.
- `transport.py` implements transport-neutral `SyntheticMessageDelivery` only.
- `persistence.py` implements SQLAlchemy table projections and one `MessageRepository`.
- `service.py` implements `MessageService` and owns logical transaction commit and rollback.
- `worker.py` implements a local, synchronous, Profile-scoped `MessageWorker` with explicit `start`, `stop`, and `reset`.
- Migration `0003_xianyu_message_boundary` creates `xianyu_message_conversations`, `xianyu_message_records`, and `xianyu_message_delivery_attempts`.
- NEW creates one Message Record and one Delivery Attempt.
- DUPLICATE creates no second Message Record and records another Delivery Attempt.
- INDETERMINATE creates a separate Message Record and is not silently discarded.
- CONFLICT fails closed, rolls back, and overwrites nothing.
- Platform Message Identifier alone is not a global deduplication key.
- Message Content and content hashes are not deduplication keys.
- The Message Worker allows one in-flight delivery per Worker.
- Automatic reconnect attempts are zero.
- Automatic processing retries are zero.
- The implementation uses only Synthetic Message Fixtures and local SQLite/Alembic infrastructure.
- T6 creates no real WebSocket, Endpoint, DNS, HTTP, external network access, Credential Provider, Cookie handling, Token handling, browser integration, background thread, subprocess, Scheduler Job, automatic retry, automatic reconnect, message sending, reply generation, API, Web UI, real account access, or real customer-data behavior.
- T6 does not modify the Capability Registry or capability specification.

## T6 corrective authorization and outcome

The project owner authorized one corrective T6 commit before T7.

The correction:

- adds Platform Conversation Identifier to Delivery Identity compatibility checks;
- restores the approved Worker failure-state mapping;
- requires explicit reset from BLOCKED and FAILED states;
- exposes Conversation through the import-safe public package surface;
- adds no new runtime module, table, Migration, dependency, network behavior, Credential behavior, or capability binding.

The project owner also approved retaining the existing generic Migration-head compatibility adjustments in:

- tests/contract/test_account_persistence.py;
- tests/contract/test_migrations.py;
- tests/unit/test_application_factory.py;
- tests/unit/test_database.py;
- tests/unit/test_health.py.

Those compatibility adjustments added no test functions and do not constitute T7 dedicated Message testing.

Tasks remain 6 / 9.

T7 remains the next executable task and was not started.

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
- No runtime implementation during T5.
- No worker.message Package during T5.
- No Domain, Persistence, Service, Transport, or Worker code during T5.
- No ORM model, database table, Migration, Repository, or Service during T5.
- No Socket, WebSocket, HTTP, DNS, browser, thread, subprocess, scheduler, or external network behavior.
- No automatic Worker startup.
- No automatic reconnect or retry.
- No background delivery loop.
- No real account, Credential, Message Content, or customer data.
- No capability binding.
- No runtime implementation before a separate T6 execution.

## Security boundary

- Do not bypass platform verification or risk controls.
- Do not guess protocol, permission, credential, acknowledgement, ordering, or reconnect behavior.
- Do not commit or log real message payloads or customer data.
- Use Synthetic Fixtures only.
- Stop when authorization, protocol, ownership, credential, or risk state is uncertain.

## Execution boundary

T1 through T6 are complete.

T7 is the next executable task.

T7 must be performed in a separate execution.

The local implementation exists, but CAP-XY-MESSAGE remains planned and unbound until T8.

Real transport, external platform access, real Credential access, customer-message processing, message sending, Ready-for-review, auto-merge, and merge remain unauthorized.

## T7 permanent coverage authorization and outcome

The project owner authorized only T7: `T7 Add unit, contract, security, and active-change acceptance tests`.

T1 through T7 are complete. Completed tasks are 7 / 9. T8 is the next executable task: `T8 Update capability evidence and run complete verification`. T8 was not started and requires separate authorization.

T7 added permanent Message coverage only: 12 Domain unit tests, 9 Service unit tests, 8 Worker unit tests, 8 Persistence Contract tests, and 5 Security Contract tests, for exactly 42 new permanent Message tests. The existing Import Safety file remains at three test functions and now covers the Message Package import-safe boundary.

The coverage records NEW, DUPLICATE, INDETERMINATE, Content Conflict, Conversation Conflict, UUID4 local identifier generation, transaction ownership, rollback, Profile scope, Account scope, Worker lifecycle, failure-state mapping, explicit reset, one in-flight delivery, re-entry protection, graceful stop, three-table schema, Migration lineage, Foreign Keys, database constraints, Repository no-commit behavior, empty downgrade, non-empty downgrade fail-closed behavior, import isolation, absence of external integrations, blocked network/subprocess/Home/thread entry points, sanitized errors, Synthetic Fixture-only evidence, and contract order independence.

No Runtime, Migration, Registry, Capability Specification, dependency, or CI file was modified. `CAP-XY-MESSAGE` remains planned and unbound; implementation_paths and test_paths remain empty until separately authorized T8 evidence work.

## T7 corrective authorization and outcome

The project owner authorized a T7 corrective execution: `Correct T7 permanent Message-boundary coverage before T8`.

Tasks remain 7 / 9. T1 through T7 are complete. T8 remains the next executable task and was not started.

The correction strengthens existing T7 evidence without changing test counts. The permanent Message test suite remains exactly 42 tests, Import Safety remains three tests, active acceptance remains four tests, and full collection remains 322 tests.

The correction adds true Worker re-entry coverage from inside an active Service operation, deterministic graceful-stop Event/thread coverage, direct Repository flush-without-commit evidence, real SQLite NEW/DUPLICATE/INDETERMINATE and conflict atomicity evidence, complete schema and database-constraint evidence, explicit Message-only downgrade to `0002_xianyu_account_boundary`, isolated Worker security runtime evidence, stronger package lazy-import evidence, and stronger Synthetic Fixture and cleanup escape-hatch scans.

No Runtime, Migration, Registry, Capability Specification, dependency, CI, `tasks.md`, or `generated/PROJECT_STATE.json` file was modified by this correction. `CAP-XY-MESSAGE` remains planned and unbound.

## T7 final evidence follow-up authorization and outcome

The project owner authorized a second T7 corrective follow-up execution: `Complete the remaining T7 evidence gates before T8`.

Tasks remain 7 / 9. T1 through T7 are complete. T8 remains the next executable task and was not started.

The follow-up completes remaining permanent evidence gates without changing test counts. The permanent Message test suite remains exactly 42 tests, Import Safety remains three tests, active acceptance remains four tests, and full collection remains 322 tests.

The follow-up adds complete Check Constraint name and SQL-semantics evidence, reflected Foreign Key referred-column and `RESTRICT` evidence, Migration source restrictions, Alembic CLI upgrade evidence, offline SQL evidence, remaining Profile/Account/Delivery Identity/Attempt constraint cases, actual lazy public package resolution, a complete isolated Worker security flow, and per-file UTF-8/Synthetic Fixture/sensitive-data/cleanup escape-hatch scans.

No Runtime, Migration, Registry, Capability Specification, dependency, CI, `tasks.md`, or `generated/PROJECT_STATE.json` file was modified by this follow-up. `CAP-XY-MESSAGE` remains planned and unbound.

## T7 exact contract evidence completion authorization and result

The project owner authorized a final T7 corrective evidence completion before T8. This correction is limited to permanent test evidence and governance documentation. It closes direct database constraint evidence gaps, isolated Worker row-count evidence gaps, offline SQL sensitive-output scanning, and per-file sensitive-data scan coverage while keeping CHG-0004 APPROVED, tasks at 7 / 9, and T8 not started.

## T7 sensitive-scan correction authorization and result

The project owner authorized the final T7 security-scan corrective execution before T8. The authorized scope is limited to the permanent Security Contract scanner implementation and governance documentation.

The correction keeps CHG-0004 APPROVED, keeps tasks at 7 / 9, and keeps T8 as the next executable task. T8 was not started.

CAP-XY-MESSAGE remains planned and unbound: implementation_paths and test_paths remain empty, active_change remains null, and last_verified_commit remains null.

## T7 quoted-phrase bypass removal

The project owner authorized one final T7 scanner correction before T8.

The previous forbidden-phrase detector excluded phrases immediately surrounded by quotation marks.

That exclusion was removed.

Forbidden phrases are now detected in complete Source regardless of whether they appear as ordinary text, single-quoted strings, double-quoted strings, assignments, comments, or embedded text.

Phrase positive controls invoke the same detection function used for real evidence files.

Scanner-rule literals in the Persistence Contract are assembled at runtime so the scanner can inspect complete Source without suppressing quoted content.

No test function was added or removed.

Tasks remain 7 / 9.

T8 remains the next executable task and was not started.
