# CHG-0003 Design

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Design state

CHG-0003 is approved for controlled, task-by-task execution.

T1 through T7 are complete.

The terminology, security, credential-handling, persistence, migration, runtime ownership, and module boundaries are finalized.

T8 is the next executable task.

The minimal local account boundary has been implemented. No API route, browser integration, Provider integration, background process, or external account behavior has been implemented.

## Canonical terminology

### Platform Account

The real external Xianyu account that exists on the platform.

A Platform Account is outside the repository boundary.

CHG-0003 does not access, authenticate, inspect, or operate a real Platform Account.

The term Account must not be used to refer both to internal records and real platform accounts. Use Platform Account when referring to a real Xianyu account.

### Account Reference

A repository-owned, non-secret logical reference to exactly one intended Platform Account.

An Account Reference may contain only approved non-secret identity metadata.

It is not an authenticated session, credential, Cookie, Token, browser state, or proof that the Platform Account exists or is usable.

Internal model concepts use Account Reference. Account Reference must not be shortened to Credential or Session.

### Profile

The local account-isolation boundary that owns exactly one Account Reference and all future Profile-scoped configuration and references.

A Profile is a repository domain concept.

A Profile is not a browser profile, browser user-data directory, authenticated session, process, worker, or operating-system user.

A Profile is not a Chrome Profile, browser directory, login state, or Worker process.

### Profile Identifier

An opaque, immutable, repository-local identifier for one Profile.

The Profile Identifier is the canonical local identity of the Profile.

A display label, platform username, phone number, external identifier, or directory name must not be used as the canonical Profile Identifier.

T2 defines this term only and does not choose UUID, ULID, database-field format, or any runtime representation.

### Account Alias

A mutable, human-readable label used only to help an operator distinguish Profiles.

An Account Alias is not unique identity, authentication data, or authoritative platform metadata.

### External Account Identifier

An optional, non-secret identifier supplied by or associated with the external platform.

It must be treated as untrusted reference metadata.

It must not be treated as authentication, authorization, proof of ownership, or the canonical local Profile identity.

T2 does not decide its storage format or whether it is persisted.

### Credential Reference

An opaque reference to secret material that may be stored by a separately approved secure-storage boundary in the future.

A Credential Reference never contains the secret value itself.

The format, provider, encryption, access rules, and lifecycle of Credential References are deferred to T3.

T2 does not select a key store or credential manager.

### Session Material

Any authentication or session-bearing value, including Cookies, Tokens, authorization headers, browser local storage, browser session storage, QR-code login material, SMS verification data, passwords, private keys, or equivalent values.

Session Material is sensitive.

Session Material is not part of an Account Reference, Profile Identifier, Account Alias, or External Account Identifier.

T2 does not read, generate, store, or test any real Session Material.

### Profile-scoped State

Any mutable configuration, reference, lifecycle metadata, audit context, or future runtime state that belongs to exactly one Profile.

Profile-scoped State must not be shared as mutable state between Profiles.

The persistence model is deferred to T4.

### Isolation Boundary

The rule set that prevents one Profile from reading, writing, reusing, or implicitly inheriting another Profile's Profile-scoped State, Credential References, Session Material, audit context, or future runtime resources.

### Synthetic Fixture

Artificial test-only data that does not represent a real Platform Account, real credential, real customer, real browser directory, or real session.

Only Synthetic Fixtures may be used in CHG-0003 tests before later explicit authorization.


## Terminology invariants

1. Each Profile owns exactly one Account Reference.

2. Each Account Reference belongs to exactly one Profile.

3. A Profile Identifier is the canonical repository-local identity.

4. Account Alias and External Account Identifier are reference metadata and must not replace the Profile Identifier.

5. An Account Reference must not contain Session Material.

6. A Profile must not contain raw Session Material.

7. A Credential Reference must never contain a secret value.

8. Profile-scoped State must not be shared as mutable state across Profiles.

9. Missing, ambiguous, conflicting, or cross-Profile ownership information must fail closed.

10. The term Profile must not be used as a synonym for browser profile, browser user-data directory, authenticated session, worker process, or operating-system user.

11. No terminology decision in T2 proves that a Platform Account exists, is authenticated, is permitted, or is safe to operate.

12. Only Synthetic Fixtures may be used while real account access remains out of scope.


## Security data classification

### Secret Material

Secret Material includes all Session Material and any value that can authenticate, authorize, recover, impersonate, or continue access to a Platform Account.

Examples include Cookies, Tokens, passwords, private keys, authorization headers, QR-code login material, SMS verification data, recovery codes, browser local storage, browser session storage, device-binding secrets, and equivalent values.

Secret Material must never be committed to the repository.

Secret Material must never be stored directly in repository configuration, application configuration, environment files, ordinary environment variables, database columns, migration fixtures, logs, audit events, exception messages, telemetry, URLs, command-line arguments, PR text, issues, test snapshots, or Synthetic Fixtures.

### Sensitive Non-secret Metadata

Sensitive Non-secret Metadata includes Credential References, External Account Identifiers, account risk states, credential-resolution outcomes, provider identifiers, authorization outcomes, and Profile-to-credential associations.

Sensitive Non-secret Metadata is not authentication material, but it must remain Profile-scoped and subject to least-privilege access.

It must not be treated as public data.

### Ordinary Profile Metadata

Profile Identifier and Account Alias are non-secret repository concepts.

They must still follow Profile isolation and must not be used to infer authorization, authentication, ownership, or platform validity.

Data classification does not authorize persistence.

Persistence remains deferred to T4.

## Secure Storage Boundary

Secure Storage Boundary

A future external or operating-system-backed boundary responsible for storing and releasing Secret Material.

The Secure Storage Boundary is outside the repository domain model and outside ordinary application persistence.

1. Secret Material is stored outside the repository and outside ordinary application database storage.

2. Stored Secret Material must be encrypted at rest by the selected provider.

3. Provider access must be protected by operating-system, service-account, or equivalent access controls.

4. Access must follow least privilege.

5. Secret Material must be isolated by Profile and Credential Reference.

6. A provider must not return one Profile's Secret Material for another Profile.

7. A Credential Reference must remain opaque and must not embed the secret value, plaintext storage path, encryption key, raw provider token, or recoverable secret content.

8. Provider errors must not include Secret Material.

9. Provider selection, integration, module ownership, process ownership, and concrete APIs remain deferred to T5.

10. No Secure Storage Boundary is implemented during T3.

T3 does not choose a concrete provider, decide database fields, or define interface code.

## Credential Reference security rules

1. Each Credential Reference belongs to exactly one Profile.

2. A Credential Reference must not be shared across Profiles.

3. A Credential Reference must not be copied from one Profile to another.

4. A Credential Reference must not contain Secret Material.

5. A Credential Reference must not encode a password, Cookie, Token, authorization header, browser path, external account password, encryption key, or other recoverable secret.

6. A Credential Reference must not prove that Secret Material exists, is valid, is current, or is authorized for use.

7. Missing, malformed, unknown, conflicting, or cross-Profile Credential References must fail closed.

8. There must be no implicit default Credential Reference.

9. There must be no global current-account credential state.

10. Future credential resolution must require an explicit Profile Identifier and the Profile-owned Credential Reference.

11. A future operation must verify Profile ownership before requesting Secret Material.

12. Credential Reference persistence format remains deferred to T4.

13. Credential Reference provider and runtime ownership remain deferred to T5.

## Future credential resolution boundary

This section defines a future implementation constraint, not a current implementation.

A future credential-resolution operation must require:

- An explicit Profile Identifier.
- The Credential Reference owned by that Profile.
- An explicit operation purpose.
- An explicit authorization decision.
- A non-blocked risk decision.

A future credential-resolution operation must satisfy:

1. Resolve only the Secret Material required for one explicit operation.

2. Keep resolved Secret Material in memory for the shortest practical period.

3. Do not persist resolved Secret Material.

4. Do not cache resolved Secret Material across operations.

5. Do not serialize resolved Secret Material.

6. Do not place resolved Secret Material in logs, events, exceptions, metrics, tracing attributes, URLs, command-line arguments, database values, or API responses.

7. Do not reuse resolved Secret Material across Profiles.

8. Do not silently fall back to another Credential Reference.

9. Do not retry using another Profile's credentials.

10. Release references to resolved Secret Material after the operation.

11. Do not claim guaranteed memory zeroization in a managed runtime.

12. If ownership, authorization, resolution, or risk state changes during an operation, stop and fail closed.

T3 does not implement this flow.

## Credential resolution and authorization states

This section defines two independent conceptual state axes.

### Credential Resolution Status

Allowed conceptual statuses:

```text
UNRESOLVED
RESOLVED
MISSING
UNAVAILABLE
INVALID
EXPIRED
REVOKED
```

- UNRESOLVED: No resolution result exists.
- RESOLVED: The Secure Storage Boundary returned operation-scoped Secret Material.
- MISSING: The Credential Reference or referenced material does not exist.
- UNAVAILABLE: The Secure Storage Boundary cannot safely provide a result.
- INVALID: The material is structurally or semantically invalid.
- EXPIRED: The material is no longer current.
- REVOKED: Use has been explicitly withdrawn.

### Operation Authorization Status

Allowed conceptual statuses:

```text
UNKNOWN
AUTHORIZED
VERIFICATION_REQUIRED
PERMISSION_DENIED
RISK_BLOCKED
```

- UNKNOWN: Authorization or platform risk state is not known.
- AUTHORIZED: A separate approved authorization boundary permits the explicit operation.
- VERIFICATION_REQUIRED: Human or platform verification is required.
- PERMISSION_DENIED: The operation is not permitted.
- RISK_BLOCKED: Risk controls prohibit the operation.

A future operation may proceed only when:

- Credential Resolution Status is RESOLVED; and
- Operation Authorization Status is AUTHORIZED; and
- Profile ownership remains exact and unambiguous.

Every other status or combination must deny the operation and fail closed.

RESOLVED alone does not authorize use.

AUTHORIZED without RESOLVED Secret Material does not authorize use.

UNKNOWN must never be treated as AUTHORIZED.

VERIFICATION_REQUIRED must never be bypassed or automatically converted to AUTHORIZED.

T3 does not implement state-machine code.

## Permission and risk boundary

1. Permission must be explicit and operation-specific.

2. Permission must be evaluated for the exact Profile.

3. Permission must not be inherited from another Profile.

4. Permission must not be inferred from previous success.

5. Permission must not be inferred from the presence of a Credential Reference.

6. Permission must not be inferred from the presence of Session Material.

7. Unknown permission fails closed.

8. Unknown risk state fails closed.

9. Platform verification or risk controls must never be bypassed.

10. VERIFICATION_REQUIRED requires explicit external resolution and cannot be handled automatically by CHG-0003.

11. PERMISSION_DENIED and RISK_BLOCKED prohibit retries that switch Profiles or credentials.

12. The repository must not guess whether a Platform Account is safe to operate.

## Logging, errors, and redaction

Allowed logging and audit fields:

```text
event type
Profile Identifier
timestamp
operation purpose
outcome class
non-secret reason code
non-secret correlation identifier
```

Prohibited fields:

```text
Secret Material
full Credential Reference
External Account Identifier
account password
Cookie
Token
authorization header
QR-code material
SMS verification data
browser local storage
browser session storage
browser user-data path
customer data
request or response payload containing sensitive values
raw provider error content that may contain sensitive values
```

1. Secret Material must never appear in logs, exception messages, audit events, traces, metrics, snapshots, test output, or PR text.

2. Full Credential References must not be logged.

3. A future implementation may use a separately generated non-secret correlation identifier, but the generation design remains deferred.

4. Errors exposed outside the Secure Storage Boundary must use non-secret reason codes.

5. Provider errors must be sanitized before they cross the provider boundary.

6. Redaction failure must fail closed and suppress the unsafe diagnostic.

7. Debug mode must not weaken these rules.

8. Tests must not assert or snapshot raw Secret Material.

## Prohibited Secret Material ingress

Secret Material must not enter the future system through:

- Source files.
- Git-tracked configuration.
- .env files.
- Ordinary environment variables.
- Command-line arguments.
- URL paths.
- URL query parameters.
- HTTP response bodies intended for operators.
- Log fields.
- Audit fields.
- Issue or pull-request text.
- Test fixtures.
- Test snapshots.
- Browser-directory copies.
- Database seed files.
- Migration files.

A future secure ingress mechanism requires a separate approved design.

T3 does not approve or implement a Secret Material import channel.

## Credential lifecycle boundary

1. Rotation must not expose the previous or replacement Secret Material to ordinary application persistence.

2. Rotation must not create cross-Profile credential reuse.

3. A revoked credential must not be automatically restored.

4. An expired credential must not be treated as valid.

5. An invalid credential must not trigger fallback to another Profile.

6. A missing credential must not trigger credential discovery across Profiles.

7. A replaced Credential Reference must not cause automatic fallback to its predecessor.

8. Revocation must deny future resolution.

9. Credential history and retention policy remain deferred to T4 and the selected Secure Storage Boundary.

10. Concrete rotation and revocation workflows remain deferred to T5 and T6.

11. No lifecycle operation is implemented during T3.

## Security testing boundary

1. Only Synthetic Fixtures may be used.

2. Synthetic Fixtures must not be derived from real Platform Accounts, customers, credentials, browser directories, Cookies, Tokens, or Session Material.

3. Synthetic values must be visibly artificial.

4. Tests must not require a real Secure Storage Boundary.

5. Tests must not access an operating-system credential store.

6. Tests must not access browser user-data directories.

7. Tests must not access external networks.

8. Tests must validate documentation, generated state, repository boundaries, prohibited paths, and absence of real sensitive values.

9. T3 tests do not constitute implementation evidence for CAP-XY-ACCOUNT.

## Persistence principles

- Use the existing CAP-CORE-DATABASE SQLite boundary.
- Use the existing unified SQLAlchemy Engine and Session factory.
- Do not create a second database or Engine.
- Do not introduce MySQL, PostgreSQL, Redis, or another persistence stack for CAP-XY-ACCOUNT.
- Persist only minimal non-secret Profile and Account Reference metadata.
- Persistence does not authorize platform operations, account access, credential resolution, provider integration, browser integration, or runtime implementation.
- A minimal future relational projection is approved in principle.
- The exact table name and final table count remain deferred to T5 and T6.
- Unnecessary multi-table designs, Secret tables, Session tables, Cookie tables, and generic Payload tables are prohibited.

## Allowed persisted data categories

The future ordinary database boundary may persist only approved non-secret metadata categories:

- canonical local Profile identity;
- non-secret display metadata;
- optional untrusted external reference metadata;
- optional opaque non-secret Credential Reference;
- minimal lifecycle metadata;
- minimal timestamps and concurrency metadata when justified.

Credential References may be persisted only as opaque non-secret references.

Exact table names, column names, storage types, nullability, constraints, and field lengths remain deferred to T5 or T6.

Reasonable bounded lengths must be defined during implementation design and enforced consistently.

Exact limits are deferred to T5 or T6.

The Profile Identifier generation algorithm remains deferred to T5. T4 does not choose UUID, ULID, auto-increment identifiers, hash identifiers, or any other generation algorithm.

## Prohibited persisted data

The ordinary database boundary must not persist:

- Secret Material;
- Cookies or Tokens;
- passwords or authorization headers;
- browser Profile or user-data paths;
- browser state;
- local storage or session storage;
- QR-code or SMS verification material;
- provider secret values;
- customer data;
- raw request or response payloads;
- Credential Resolution Status as reusable proof of authorization;
- Operation Authorization Status as reusable proof of authorization;
- generic JSON, BLOB, payload, properties, extras, metadata, context, or arbitrary key-value fields.

Generic or opaque payload columns are prohibited because they could bypass the approved field-level security boundary and conceal Secret Material.

Database records must not prove that a real Platform Account exists, is logged in, is authorized, or is safe to operate.

## Ownership, consistency, and concurrency requirements

- Every record belongs to one explicit Profile.
- Cross-Profile mutable state or Credential Reference reuse is prohibited.
- Mutations must be transactional.
- Partial writes are prohibited.
- Uniqueness conflicts fail closed.
- Stale concurrent writes fail closed.
- No implicit current Profile exists.
- No fallback Profile exists.
- No operation may search across Profiles for a usable Credential Reference.
- A local lifecycle state never proves authentication, authorization, platform validity, or safe operation.
- A minimal lifecycle model is required.
- The lifecycle model must distinguish an operationally allowed local record from a locally blocked or retired record.
- Exact lifecycle state names and transitions remain deferred to T5.
- Retirement, restoration, and Credential Reference cleanup behavior require explicit lifecycle and Secure Storage ownership decisions in T5.
- No automatic restoration or implicit credential reuse is permitted.
- Automatic destructive deletion is not approved.
- Final retention, archive, restoration, purge, and hard-delete behavior remains deferred to a later approved decision.
- Indexes must support approved identity and uniqueness invariants without exposing or indexing Secret Material.
- Exact indexes are deferred to implementation design.

## Migration principles

- Future migration follows 0001_core_baseline in one linear Alembic history.
- down_revision must reference 0001_core_baseline.
- Alembic must retain one linear head.
- Migration execution remains explicit.
- Migration must continue to use the existing CAP-CORE-DATABASE connection and configuration boundary.
- Application startup does not auto-migrate.
- Upgrade creates only the minimum approved account-boundary schema.
- Upgrade performs no seed, import, discovery, browser scan, credential access, Secure Storage access, external platform access, or network access.
- Downgrade must never silently destroy non-empty business data.
- The exact downgrade strategy and operational approval process remain deferred to T5 and T6.
- A single linear Alembic revision after 0001_core_baseline is expected for the first implementation.
- The final revision identifier is selected when T6 creates the migration.
- T4 creates no migration file.
- T4 creates no ORM model, database table, Repository, DAO, API, Worker, Credential Provider, or Secure Storage implementation.

## Runtime ownership summary

CAP-XY-ACCOUNT is owned by the `worker.account` capability namespace recorded in the capability registry.

The approved future Python package is:

`app/xianyu_system/worker/account/`

The corresponding import namespace is:

`xianyu_system.worker.account`

The `worker` name identifies capability ownership. It does not mean that CHG-0003 creates or starts a background process, thread, scheduler job, browser worker, or external-platform worker.

T5 approves only the future package path. T5 must not create this directory, must not modify the capability registry, and leaves the registry with `status=planned` and `owner_module=worker.account`.

## Approved module boundary

T6 may create only this minimal future package structure for the account capability:

```text
app/xianyu_system/worker/__init__.py

app/xianyu_system/worker/account/__init__.py
app/xianyu_system/worker/account/domain.py
app/xianyu_system/worker/account/persistence.py
app/xianyu_system/worker/account/service.py
```

### domain.py

`domain.py` owns pure domain concepts and invariants:

- Profile
- Account Reference
- Profile Identifier
- Account Alias
- optional External Account Identifier
- optional Credential Reference
- local lifecycle status
- domain validation
- domain-specific non-sensitive errors

`domain.py` may use only Python standard-library domain types.

`domain.py` must not import FastAPI, SQLAlchemy, Alembic, APScheduler, browser libraries, HTTP clients, Core database resources, application state, or concrete adapters.

### persistence.py

`persistence.py` owns the SQLAlchemy relational projection and the single concrete account Repository.

It may import Base, Session, and related infrastructure from `xianyu_system.core.database`.

It must not create an Engine, Session factory, database path, or second persistence stack.

Do not create both a Repository and DAO for the same data.

Do not create a generic BaseRepository.

Do not create a generic UnitOfWork framework.

Do not create CQRS, an event store, an event bus, or a plugin framework.

### service.py

`service.py` owns account use cases and transaction coordination.

It coordinates domain validation and persistence.

It does not access a real Platform Account.

It does not resolve Secret Material.

It does not own browser, API, scheduler, or provider integration.

### __init__.py

`__init__.py` defines the intentionally small public package surface.

Internal ORM classes and SQLAlchemy details must not become the public capability interface.

Exact Python class and function names may be selected during T6, but they must remain within these responsibilities.

## Dependency direction

Approved dependency direction:

```text
domain.py
    -> imported by
persistence.py and service.py

persistence.py
    -> uses
xianyu_system.core.database

service.py
    -> coordinates
domain.py and persistence.py

future external adapters
    -> may call
service.py
```

- The domain module must not depend on persistence.
- Core database infrastructure must not import the account capability.
- The account capability must not modify Core Engine or Session ownership.
- API, web, scheduler, message, publish, reply, WeCom, or AI modules must not be imported into the account domain.
- No circular dependency is approved.
- No cross-capability mutable global state is approved.

## Profile Identifier ownership

The account service owns generation of new Profile Identifiers.

The approved first-version generation strategy is UUID version 4 using the Python standard library.

The canonical external representation is the lowercase hyphenated UUID string.

The database must not generate Profile identity through auto-increment behavior.

A Platform Account identifier, username, phone number, Account Alias, browser directory, or Credential Reference must not be used as the Profile Identifier.

T5 approves only the algorithm and ownership. T5 does not write generation code.

## Local lifecycle ownership

The approved local lifecycle states are:

```text
PENDING
ENABLED
DISABLED
```

- PENDING: The local Profile exists but is not locally eligible for an account operation.
- ENABLED: The local Profile is eligible to proceed to the separate T3 ownership, credential-resolution, authorization, and risk gates.
- DISABLED: Local account operations are denied.

Rules:

1. A newly created Profile starts as PENDING.
2. PENDING may transition to ENABLED or DISABLED.
3. ENABLED may transition to DISABLED.
4. DISABLED may transition to ENABLED.
5. No other transition is approved.
6. ENABLED does not prove authentication, authorization, platform validity, credential validity, or safe operation.
7. Every future operation still requires the T3 gates.
8. CHG-0003 does not approve archive, restore, purge, hard delete, or automatic deletion behavior.
9. Lifecycle changes must be explicit and Profile-specific.
10. Lifecycle changes must not automatically attach, replace, clear, restore, or resolve a Credential Reference.

The states ARCHIVED, DELETED, LOCKED, AUTHENTICATED, ONLINE, LOGGED_IN, and RISK_OK are not approved as CHG-0003 local lifecycle states.

## Domain and persistence ownership

The domain Profile and Account Reference remain distinct concepts with a one-to-one ownership invariant.

The first implementation uses one minimal relational projection owned by `xianyu_system.worker.account.persistence`.

The exact physical table name, final column names, SQLAlchemy storage types, field lengths, constraint names, index names, and Alembic Revision identifier are finalized during T6 implementation within the T2-T5 approved boundaries.

Required invariants:

- Every persisted projection belongs to exactly one Profile Identifier.
- A non-null Credential Reference belongs to exactly one Profile.
- A non-null External Account Identifier must not create ambiguous ownership across Profiles.
- Account Alias is not canonical identity and is not required to be unique.
- Secret Material is never persisted.
- Generic JSON, BLOB, payload, metadata, context, properties, extras, or arbitrary key-value storage remains prohibited.

Approved T6 conceptual operations:

```text
create a local Profile
read a Profile by Profile Identifier
list local Profiles
update non-secret display/reference metadata
attach or replace an opaque Credential Reference
clear an opaque Credential Reference
change the local lifecycle status through an approved transition
```

Not approved:

```text
hard delete
archive
restore
bulk update
bulk delete
credential discovery
cross-Profile lookup for usable credentials
real account login
browser Profile loading
external account validation
```

## Transaction and concurrency ownership

CAP-CORE-DATABASE continues to own Engine creation, Session factory creation, database-path resolution, WAL configuration, connection disposal, and Alembic infrastructure.

The account service owns the logical transaction boundary for each account mutation.

The account Repository participates in the caller-owned Session and must not independently commit.

Rules:

1. One logical mutation uses one Session and one transaction.
2. The service coordinates commit or rollback.
3. Repository may flush when required but must not commit independently.
4. Partial writes are prohibited.
5. Raw SQLAlchemy Sessions must not be stored globally.
6. There is no global current Profile.
7. There is no global current account Session.
8. Uniqueness conflicts fail closed.
9. Stale concurrent writes fail closed.
10. A minimal optimistic-concurrency token is required.
11. The exact physical concurrency column name and SQLAlchemy implementation are selected in T6.
12. Silent last-write-wins behavior is prohibited.

A second Engine, Session factory, UnitOfWork framework, database connection manager, or transaction manager framework is not approved.

## Error and diagnostic ownership

The future account package owns stable non-sensitive error categories for:

- invalid domain input
- Profile not found
- duplicate or ambiguous ownership
- invalid lifecycle transition
- stale concurrent update
- persistence conflict
- operation blocked by local lifecycle

Rules:

- Raw SQLAlchemy exceptions must not cross the public account service boundary.
- Persistence errors must be translated into account-owned non-sensitive errors.
- Error messages must not contain full Credential References, External Account Identifiers, Secret Material, raw SQL statements, provider responses, or customer data.
- Domain errors must not expose database implementation details.
- T5 does not require an elaborate error hierarchy.
- T6 should implement only the minimum stable errors required by the approved use cases.

## Credential and Secure Storage ownership

CHG-0003 owns only the Credential Reference as an opaque, non-secret Profile-owned value.

CHG-0003 does not own Secret Material storage, Secret Material resolution, credential import, browser-session import, credential rotation, provider authentication, or account login.

No Secure Storage provider interface, Credential Provider interface, resolver protocol, provider adapter, or secret-ingress interface is implemented in T6.

A future separately approved change must define the concrete Secure Storage capability and its integration boundary.

The account service may attach, replace, or clear an opaque Credential Reference string only as non-secret metadata.

The account service must not validate whether the referenced Secret Material exists or is usable.

## API, worker, and process boundary

CHG-0003 does not approve an HTTP API route.

CHG-0003 does not approve a web UI page.

CHG-0003 does not approve a Scheduler Job.

CHG-0003 does not approve a background Worker process.

CHG-0003 does not approve browser automation or browser Profile loading.

T6 implementation remains in the pure local package and tests only. Later exposure requires a separate approved change.

## Approved T6 implementation surface

T6 may create or modify only these future implementation and evidence paths:

```text
app/xianyu_system/worker/__init__.py
app/xianyu_system/worker/account/__init__.py
app/xianyu_system/worker/account/domain.py
app/xianyu_system/worker/account/persistence.py
app/xianyu_system/worker/account/service.py
migrations/versions/<one revision after 0001_core_baseline>.py
migrations/env.py
tests/contract/test_migrations.py
changes/active/CHG-0003-xianyu-account-boundary/tests/test_acceptance.py
generated/PROJECT_STATE.json
README.md
```

migrations/env.py modification is limited to account metadata registration. tests/contract/test_migrations.py modification is limited to removing obsolete 0001-only assumptions. Dedicated permanent account tests remain deferred to T7.

T6 explicitly excludes:

- FastAPI routes
- OpenAPI contracts
- web templates
- scheduler jobs
- browser code
- external platform adapters
- Secret Material provider or resolver
- WeCom
- AI
- message, publish, or reply modules
- dependency changes unless separately approved before T6

## Decisions deferred after T5

### Deferred to T6

- exact Python class and function names
- ORM implementation
- ORM model implementation
- Migration implementation
- migration implementation
- Exact table count and names within the approved single minimal relational projection
- exact physical table name
- Exact column names and types
- exact column names, storage types, constraints, and indexes
- Exact constraints and indexes
- repository implementation
- service implementation
- unit and active-change implementation tests

### Deferred to T7

- full permanent test coverage
- migration contract tests
- security regression tests
- integration and contract tests for the account boundary

### Deferred to T8

- CAP-XY-ACCOUNT registry binding
- implementation and test evidence paths
- capability status transition
- full verification candidate

### Deferred to later changes

- API, web, or scheduler exposure
- real browser Profile and session integration
- secure storage provider or resolver
- external platform login and account validation

## T7 correction outcome

The T7 permanent account evidence was hardened before T8.

- Account operations are now executed while network sockets, subprocesses, and user-Home discovery are blocked.
- The runtime test proves that local Profile operations require only the supplied temporary SQLite boundary.
- The security evidence includes static absence of browser and Credential Store integrations.
- Persistence Contract tests no longer clear global SQLAlchemy mappers, remove shared Base metadata, or evict production modules from `sys.modules`.
- The account Contract tests can execute in either persistence-first or security-first order.
- Database-level checks explicitly reject whitespace-only External Account Identifiers.
- Database-level checks explicitly reject whitespace-only Credential References.
- Permanent test counts remain unchanged.
- T7 remains complete.
- T8 remains not started.

## T7 test evidence state

T7 added permanent account-boundary tests only.

- Domain Unit coverage verifies immutable `AccountReference`, `Profile` ownership, text normalization, field boundaries, row-version validation, and lifecycle transitions.
- Service Unit coverage verifies UUID version 4 Profile creation, reads, sorted listing, metadata mutations, lifecycle mutations, stale-write handling, uniqueness rollback, and sanitized persistence failures.
- Persistence Contract coverage verifies the single flattened table schema, one linear Migration head, upgrade and empty downgrade, guarded non-empty downgrade, Repository flush-without-commit behavior, relational round trips, database uniqueness, concurrency, lifecycle, version, and trim constraints.
- Security Contract coverage verifies public package restrictions, absence of external integration or secret-boundary behavior, sanitized diagnostics, and Synthetic Fixture-only account evidence.
- T7 did not modify account runtime files, Migration files, Core files, API, web, scheduler, browser, provider, Secure Storage, dependencies, CI, Registry, capability specs, or archived changes.
- CAP-XY-ACCOUNT remains planned and unbound until T8.

## Current implementation

`xianyu_system.worker.account` is implemented.

xianyu_system.worker.account is implemented.

- `domain.py` owns distinct immutable `Profile` and `AccountReference` domain objects, validation, lifecycle states, and account-owned non-sensitive errors.
- Each `Profile` owns exactly one `AccountReference`, and the Account Reference records the matching owning Profile Identifier.
- Ownership conflicts fail closed in the domain model.
- `persistence.py` owns one SQLAlchemy relational projection and one concrete Repository.
- The one table is only a flattened persistence projection; it does not merge the two domain concepts into one concept.
- `service.py` owns account use cases and transaction coordination.
- Revision `0002_xianyu_account_boundary` creates the minimum local account Profile table.
- ORM and Migration trim constraints reject blank, whitespace-only, and padded Account Alias, External Account Identifier, and Credential Reference values.
- `migrations/env.py` only registers account metadata for Alembic.
- There is no external integration.
- The three Core Unit-test files modified during T6 were pre-existing assertion compatibility updates for the new metadata, Migration head, and table state. They are classified as necessary T6 implementation compatibility updates.
- Dedicated permanent account testing remains T7.

## Execution boundary

T1 through T7 are complete.

The T6 implementation, T6 correction, and T7 permanent test coverage are complete.

T8 is the next executable task.

T8 must be performed in a separate execution.

This T7 execution did not execute T8 or T9 and does not authorize API changes, Worker processes, provider integration, browser integration, account access, Secret Material handling, capability binding, Ready-for-review, auto-merge, merge, or external platform behavior.
