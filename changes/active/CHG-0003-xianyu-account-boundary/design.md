# CHG-0003 Design

Status: APPROVED
Change ID: CHG-0003-xianyu-account-boundary

## Design state

CHG-0003 is approved for controlled, task-by-task execution.

T1 and T2 are complete.

The canonical account and Profile isolation terminology is finalized.

T3 is the next executable task.

No security model, persistence model, runtime ownership model, or runtime implementation has been approved.

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


## Decisions deferred after T2

### Deferred to T3

- Credential Reference security model.
- Secret-storage provider requirements.
- Encryption requirements.
- Permission and authorization checks.
- Risk-state handling.
- Sensitive logging and redaction.
- Credential and Session Material lifecycle.
- Failure behavior for invalid or unavailable credentials.

### Deferred to T4

- Persistence requirements.
- Database schema.
- Migration requirements.
- Retention and deletion behavior.
- Uniqueness constraints.
- Storage of Account Alias or External Account Identifier.
- Profile lifecycle persistence.

### Deferred to T5

- Module ownership.
- Worker ownership.
- API ownership.
- Process and concurrency isolation.
- Runtime resource ownership.
- Profile loading and unloading boundaries.

### Deferred to T6

- All runtime implementation.


## Security constraints

- Never commit real credentials.
- Never load real browser profiles in tests.
- Never bypass platform verification or risk controls.
- Never guess missing account state.
- Never log Cookie, Token, Secret, Password, authorization data, or customer data.
- Use synthetic fixtures only.

## Current implementation

None.

## Execution boundary

T1 and T2 are complete.

T3 is the next executable task.

T3 must be performed in a separate execution.

This T2 execution does not authorize credential handling, secret storage, persistence, database changes, API changes, worker changes, browser integration, account access, or runtime implementation.
