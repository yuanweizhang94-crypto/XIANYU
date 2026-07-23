# CHG-0003 Design

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Design state

CHG-0003 is approved for controlled, task-by-task execution.

T1, T2, T3, and T4 are complete.

The terminology, security, credential-handling, persistence, and migration boundaries are finalized.

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

## Persistence scope

The future CHG-0003 persistence boundary stores only approved non-secret Profile and Account Reference metadata.

It does not store Secret Material.

It does not store browser state, browser paths, Cookies, Tokens, passwords, authorization headers, QR-code material, SMS verification data, local storage, session storage, customer data, request payloads, response payloads, or provider secret values.

The approved first-version persistence target is the existing local SQLite database managed by CAP-CORE-DATABASE.

Persistence does not authorize account access, credential resolution, provider integration, browser integration, or runtime implementation.

Secret Material remains outside SQLite.

Credential References may be persisted only as opaque non-secret references.

No encrypted Secret Material column is approved.

No generic JSON, BLOB, metadata, payload, context, properties, extras, or arbitrary key-value column is approved.

Generic or opaque payload columns are prohibited because they could bypass the approved field-level security boundary and conceal Secret Material.

## Approved relational projection

The only approved future first-version business table is:

```text
xianyu_account_profiles
```

One row represents the relational projection of exactly one Profile and its exactly one Account Reference.

Using one relational row does not collapse or redefine the domain terminology.

Profile and Account Reference remain distinct domain concepts.

No second business table is approved during T4.

No Audit table, Credential table, Session table, Cookie table, Token table, Browser table, or generic Metadata table is approved.

## Approved future columns

The approved future columns are limited to the following fields.

## profile_id

```text
Storage type: TEXT
Nullability: NOT NULL
Key: PRIMARY KEY
Semantic: immutable canonical Profile Identifier
Length boundary: 1 to 128 characters
```

profile_id must be opaque.

profile_id must not be a username, phone number, external account identifier, directory name, Cookie, Token, or Credential Reference.

The identifier-generation algorithm remains deferred to T5.

## account_alias

```text
Storage type: TEXT
Nullability: NOT NULL
Length boundary: 1 to 120 characters after trimming
Uniqueness: not unique
```

Account Alias is human-readable display metadata only.

Duplicate aliases are allowed.

Alias must not be used for authorization, lookup ownership, or canonical identity.

## external_account_identifier

```text
Storage type: TEXT
Nullability: NULL allowed
Length boundary: 1 to 256 characters when present
Uniqueness: unique when non-null
```

It remains untrusted reference metadata.

It must not prove ownership, authorization, account validity, or authentication.

Duplicate non-null values must fail closed.

No platform-specific normalization rule is approved in T4.

## credential_reference

```text
Storage type: TEXT
Nullability: NULL allowed
Length boundary: 1 to 512 characters when present
Uniqueness: unique when non-null
```

It is an opaque non-secret reference only.

It must never contain Secret Material.

A non-null Credential Reference belongs to exactly one Profile.

Duplicate non-null Credential References must fail closed.

The provider-specific format remains deferred to T5.

## lifecycle_status

```text
Storage type: TEXT
Nullability: NOT NULL
Allowed values:
PENDING
ENABLED
DISABLED
ARCHIVED
```

- PENDING: The local Profile record exists but is not enabled for operations.
- ENABLED: The Profile is locally enabled, but every operation still requires the T3 resolution, authorization, ownership, and risk gates.
- DISABLED: All account operations are denied.
- ARCHIVED: The Profile is retained as historical non-secret metadata and all account operations are denied.

ENABLED does not mean authenticated.

ENABLED does not mean authorized.

ENABLED does not mean the Platform Account exists or is safe to operate.

## created_at_utc

```text
Storage type: TEXT
Nullability: NOT NULL
Semantic: creation timestamp in normalized UTC RFC3339 form
```

## updated_at_utc

```text
Storage type: TEXT
Nullability: NOT NULL
Semantic: most recent successful row mutation in normalized UTC RFC3339 form
```

## archived_at_utc

```text
Storage type: TEXT
Nullability: NULL allowed
Semantic: archive timestamp in normalized UTC RFC3339 form
```

ARCHIVED requires archived_at_utc to be non-null.

Non-ARCHIVED requires archived_at_utc to be null.

## row_version

```text
Storage type: INTEGER
Nullability: NOT NULL
Default: 1
Constraint: row_version >= 1
Semantic: optimistic-concurrency version
```

Every successful mutation increments row_version exactly once.

Stale row_version writes fail closed.

Silent last-write-wins behavior is prohibited.

## Approved future constraints and indexes

1. PRIMARY KEY on profile_id.

2. UNIQUE constraint on external_account_identifier when non-null.

3. UNIQUE constraint on credential_reference when non-null.

4. CHECK constraint limiting lifecycle_status to PENDING, ENABLED, DISABLED, or ARCHIVED.

5. CHECK constraint requiring non-empty profile_id.

6. CHECK constraint requiring non-empty trimmed account_alias.

7. CHECK constraint enforcing the approved maximum lengths.

8. CHECK constraint requiring archived_at_utc only for ARCHIVED rows.

9. CHECK constraint requiring credential_reference to be null for ARCHIVED rows.

10. CHECK constraint requiring row_version to be at least 1.

11. Non-unique index on lifecycle_status.

12. No index on account_alias is approved for the first version.

SQLite NULL behavior allows multiple rows without External Account Identifier or Credential Reference.

Once a non-null value exists, uniqueness prevents ambiguous cross-Profile ownership.

No full-text index, JSON index, or provider-specific index is approved.

## Persisted lifecycle transitions

Approved future transitions:

```text
PENDING -> ENABLED
PENDING -> DISABLED
PENDING -> ARCHIVED

ENABLED -> DISABLED
ENABLED -> ARCHIVED

DISABLED -> ENABLED
DISABLED -> ARCHIVED

ARCHIVED -> no automatic transition
```

1. ARCHIVED is terminal for the first approved boundary.

2. Unarchive is not approved.

3. Hard deletion through normal runtime behavior is not approved.

4. Archiving must atomically:
   - set lifecycle_status to ARCHIVED;
   - set archived_at_utc;
   - clear credential_reference;
   - increment row_version.

5. A failed archive mutation must leave the previous row unchanged.

6. DISABLED and ARCHIVED deny account operations regardless of credential state.

7. Lifecycle status never replaces T3 authorization or risk evaluation.

## Future persistence operation boundary

Future conceptual operations are limited to:

```text
create Profile projection
read Profile projection by Profile Identifier
update Account Alias
update External Account Identifier
attach or replace Credential Reference
clear Credential Reference
change lifecycle status through an approved transition
archive Profile
```

1. Every mutation requires an explicit Profile Identifier.

2. No operation may select an implicit current Profile.

3. No operation may fall back to another Profile.

4. No operation may search across Profiles for a usable Credential Reference.

5. All mutations require the expected row_version.

6. Create, update, lifecycle transition, and archive operations are transactional.

7. Uniqueness, ownership, validation, or row-version conflicts fail closed.

8. Partial writes are prohibited.

9. No bulk update or bulk delete operation is approved.

10. No raw SQL supplied by an operator or external input is approved.

11. No automatic import, discovery, synchronization, or backfill is approved.

T4 does not design Python classes, function names, Repository interfaces, or API paths; those remain deferred to T5.

## Operation-scoped state that must not be persisted

The following T3 states must not be persisted as authoritative first-version business-table state:

```text
Credential Resolution Status
Operation Authorization Status
resolved Secret Material
authorization decision payload
risk decision payload
provider response
provider error payload
verification challenge
browser state
current session state
current-account global state
```

A future operation must evaluate these values for the exact operation.

A previously successful result must not be persisted and reused as proof of current authorization or credential validity.

## Audit persistence decision

CHG-0003 does not approve a persistent audit-event table.

Only created_at_utc, updated_at_utc, archived_at_utc, lifecycle_status, and row_version are approved as persisted operational metadata.

Persistent event history, actor identity, reason history, correlation history, and audit retention require a separate approved change.

T3 security logging rules remain effective, but T4 does not design a log-storage table.

## Retention and deletion boundary

1. Active, pending, and disabled Profile rows remain until explicitly archived.

2. Archived rows are retained by default.

3. No automatic purge is approved.

4. No retention timer is approved.

5. Hard deletion is outside the first runtime boundary.

6. A future hard-delete or purge feature requires a separate approved change with explicit dependency, audit, backup, and secure-storage cleanup rules.

7. Credential Reference must be cleared during archive.

8. Secret Material deletion remains the responsibility of the separately approved Secure Storage Boundary and is not implemented or orchestrated by T4.

## Database infrastructure ownership

1. The future table uses the existing CAP-CORE-DATABASE SQLite database.

2. The future implementation must use the existing unified SQLAlchemy Engine and Session factory.

3. It must not create a second SQLite database.

4. It must not create a second SQLAlchemy Engine for the account boundary.

5. It must not introduce MySQL, PostgreSQL, Redis, or another persistence system.

6. It must preserve SQLite WAL, foreign-key, busy-timeout, explicit-path, and import-side-effect boundaries.

7. Database module and ORM ownership remain deferred to T5.

8. Runtime implementation remains deferred to T6.

## Approved future Alembic revision

Approved future revision identity:

```text
revision = 0002_xianyu_account_boundary
down_revision = 0001_core_baseline
```

1. This is the approved future revision identity.

2. T4 does not create the revision file.

3. The repository must continue to contain only 0001_core_baseline.py and __init__.py after T4.

4. The future revision must preserve one linear Alembic head.

5. The future revision must use the existing Base.metadata and migration environment.

6. It must use the existing shared Connection for programmatic migration.

7. Standalone CLI execution must continue to require explicit -x database_path=<path>.

8. Application startup must not automatically execute the revision.

9. No default production database URL may be introduced.

10. No external network access is permitted during migration.

## Approved future upgrade behavior

Future upgrade() may only:

1. Create xianyu_account_profiles.

2. Create the approved constraints.

3. Create the approved lifecycle_status index.

4. Create no seed rows.

5. Perform no data import.

6. Perform no data discovery.

7. Perform no browser or filesystem scan.

8. Access no Secure Storage Boundary.

9. Access no external platform.

10. Store no Secret Material.

11. Create no other business table.

The 0001 baseline contains no legacy account data.

No backfill or legacy-data transformation is approved.

## Approved future downgrade behavior

Future downgrade from 0002_xianyu_account_boundary to 0001_core_baseline must:

1. Check whether xianyu_account_profiles contains any rows.

2. If any row exists, abort and fail closed without dropping the table.

3. Never silently destroy Profile metadata.

4. Never automatically export data.

5. Never automatically delete Secret Material from a provider.

6. If the table is empty, drop the lifecycle_status index and then drop the table.

7. Leave the database at 0001_core_baseline.

8. Provide no force flag in the first approved boundary.

T4 does not run this logic.

## Future migration verification boundary

Future T6/T7 verification must cover at least:

- 0002 has down_revision 0001_core_baseline.
- Alembic still has one head.
- Fresh upgrade creates exactly the approved table plus alembic_version.
- Upgrade creates no Secret Material column.
- Upgrade creates no generic JSON, BLOB, payload, properties, extras, or metadata column.
- Approved constraints and indexes exist.
- Repeated upgrade is safe.
- Empty-table downgrade succeeds.
- Non-empty-table downgrade fails closed.
- Application startup does not auto-migrate.
- CLI still requires explicit database_path.
- Offline SQL creates no database file.
- Migration imports create no files.
- No real data, credentials, browser paths, or external requests are used.

These are future implementation tests.

T4 adds no permanent migration test and no Migration file.

## Decisions deferred after T4

### Deferred to T5

- Python package and module ownership.
- SQLAlchemy ORM model ownership.
- Repository or persistence-port ownership.
- Transaction coordinator ownership.
- Profile Identifier generation algorithm.
- UTC timestamp generation ownership.
- Credential Reference provider format.
- Secure Storage provider selection.
- Secure Storage integration ownership.
- API ownership.
- Worker ownership.
- Process and concurrency ownership.
- Secure ingress ownership.
- Error type ownership.
- Runtime lifecycle wiring.
- Exact method and class names.

### Deferred to T6

- Creating the SQLAlchemy model.
- Adding the model to Base.metadata.
- Creating 0002_xianyu_account_boundary.py.
- Implementing persistence operations.
- Implementing optimistic concurrency.
- Implementing lifecycle transitions.
- Implementing the downgrade guard.
- Implementing provider or credential integration.
- Implementing any runtime account behavior.

### Deferred to T7

- Permanent unit tests.
- Permanent migration contract tests.
- Permanent security tests.
- Final active-change implementation acceptance tests.

### Deferred to T8

- Capability registry binding and evidence.
- Capability status transition.
- Complete implementation verification.

## Current implementation

None.

## Execution boundary

T1, T2, T3, and T4 are complete.

T5 is the next executable task.

T5 must be performed in a separate execution.

This T4 execution does not authorize ORM code, Migration files, database mutation, provider selection, API changes, worker changes, browser integration, account access, Secret Material handling, or runtime implementation.
