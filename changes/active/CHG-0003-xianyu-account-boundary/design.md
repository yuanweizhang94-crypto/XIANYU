# CHG-0003 Design

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Design state

CHG-0003 is approved for controlled, task-by-task execution.

T1, T2, T3, and T4 are complete.

The terminology, security, credential-handling, and principle-level persistence and migration boundaries are finalized.

T5 is the next executable task.

No runtime module ownership, ORM implementation, migration implementation, provider integration, API implementation, worker implementation, or account behavior has been approved.

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

## Decisions deferred after T4

### Deferred to T5

- Module ownership.
- ORM and Repository ownership.
- Exact table count and names.
- Exact column names and types.
- Exact constraints and indexes.
- Identifier-generation strategy.
- Lifecycle state names and transitions.
- Retention, archive, restore, purge, and delete policies.
- Provider and Secure Storage ownership.
- Error ownership and runtime transaction coordination.

### Deferred to T6

- ORM implementation.
- Migration implementation.
- Persistence operations.
- Optimistic concurrency implementation.
- Lifecycle implementation.
- Downgrade guard implementation.

### Deferred to T7

- Permanent unit, migration, security, and integration tests.

### Deferred to T8

- Capability binding, evidence, status transition, and complete verification.

## Current implementation

None.

## Execution boundary

T1, T2, T3, and T4 are complete.

T5 is the next executable task.

T5 must be performed in a separate execution.

This T4 execution does not authorize ORM code, Migration files, database mutation, provider selection, API changes, worker changes, browser integration, account access, Secret Material handling, or runtime implementation.
