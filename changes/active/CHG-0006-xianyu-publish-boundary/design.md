# CHG-0006 Design

Status: APPROVED
Change ID: CHG-0006-xianyu-publish-boundary

## Draft design posture

This document records unresolved design topics for a future local Xianyu publishing boundary.

No Runtime design is approved.

No Playwright or external platform behavior is approved.

Current implementation: none.

## Pending terminology

The following terms remain pending and require later approval before implementation:

- Listing Draft.
- Publish Request.
- Publish Decision.
- Validation Result.
- Publish Attempt.
- Publish Outcome.
- Publish uncertainty state.
- Publish audit event.

## Pending ownership questions

- Which module owns local publishing-boundary domain types.
- Which future adapter owns platform-specific behavior.
- How Account, Schedule, Media, Browser, and Platform Adapter boundaries remain separated.
- Which component may construct synthetic publish requests.

## Pending permission and risk-control boundaries

- Required authorization states.
- Fail-closed behavior for missing permission.
- Risk-control categories and non-bypass requirements.
- Credential and browser-profile exclusion rules.
- Real-account and real-platform exclusion rules.

## Pending listing-draft validation questions

- Required and optional field names.
- Title, description, category, price, stock, location, and media metadata boundaries.
- Synthetic fixture constraints.
- Field normalization rules.
- Unsupported and ambiguous input handling.

## Pending idempotency and uncertainty questions

- Idempotency-key ownership.
- Duplicate request handling.
- Conflict handling.
- Unknown publish result handling.
- Retry, no-retry, and manual-review states.

## Pending persistence, lifecycle, audit, and failure questions

- Whether any persistence is required in a later approved phase.
- Lifecycle state names.
- Failure classification.
- Sanitized audit fields.
- Observability boundaries that do not reveal sensitive input.

## Pending browser/platform adapter boundary

Any future browser or platform adapter boundary requires separate approval.

This DRAFT does not approve Playwright, browser automation, real Xianyu access, login, listing creation, media upload, or network behavior.

## Pending test strategy

Future testing strategy remains unresolved and may include only synthetic fixtures unless separately approved.

Migration requirements are unresolved. No database schema is approved.

## Explicit non-approval

No module, database schema, API, Worker, Service, Repository, Scheduler, browser implementation, platform adapter, dependency, or workflow is approved by this DRAFT.

## T1 approved design posture

CHG-0006 status is APPROVED for sequential governance and design tasks only.

T1 approves entry into T2 through T5 design tasks, with each task completed and committed independently.

Current implementation: none.

No Runtime design or implementation is approved.

T2 is the current next executable task.

## T2 approved terminology and local data contracts

### ListingDraft

A local, versioned, platform-side-effect-free listing draft entity.

Conceptual fields: `draft_id`, `revision`, `title`, `description`, `category_reference`, `price`, `stock`, `location_reference`, `media_metadata`, `seller_profile_reference`, `lifecycle_state`, `created_at`, and `updated_at`.

Constraints: synthetic fixtures only; no Cookie, Token, Secret, Password, Session Material, Credential, or browser state; `media_metadata` is local descriptive metadata only and does not imply media upload; `seller_profile_reference` is a non-secret local reference; revision is explicit; semantic changes produce a new revision; ListingDraft does not represent a published listing.

### PublishRequest

An immutable DTO requesting deterministic evaluation by the local publishing boundary.

Conceptual fields: `request_id`, `draft_id`, `draft_revision`, `idempotency_key`, `requested_at`, `authorization_state`, `risk_state`, `synthetic_fixture`, and `correlation_id`.

PublishRequest does not call a platform and does not mean publication has started.

### PublishValidationResult

A local validation-result value object with `is_valid`, `issues`, `normalized_fingerprint`, and `reason_codes`.

Issues must be structured, machine-readable, and sanitized. They must not contain Credential material or complete sensitive content.

### PublishDecision

A local deterministic decision DTO with `decision_type`, `reason_code`, `draft_id`, `draft_revision`, `request_id`, `idempotency_key`, `normalized_fingerprint`, `manual_review_reason`, and `audit_identifiers`. It does not execute publication.

### PublishDecisionType

Approved initial decision types: `READY`, `INVALID_INPUT`, `UNAUTHORIZED`, `RISK_BLOCKED`, `DUPLICATE`, `CONFLICT`, and `MANUAL_REVIEW`.

`READY` means only that local validation passed and the request may enter a future separately authorized boundary. It does not mean published, browser-called, platform-called, Credential-ready, or that a PublishAttempt exists.

### PublishAttempt

A future possible local audit entity representing one separately authorized platform publishing attempt. T1-T5 do not create a PublishAttempt implementation, do not allow a real attempt, and do not allow simulated platform success.

Conceptual fields may include `attempt_id`, `request_id`, `attempt_number`, `started_at`, `completed_at`, `attempt_state`, `outcome_type`, and `sanitized_error_code`.

### PublishAttemptState

Approved conceptual states: `NOT_STARTED`, `IN_PROGRESS`, and `COMPLETED`. Current design tasks do not allow any real record to enter `IN_PROGRESS`.

### PublishOutcomeType

Approved conceptual outcome types: `SUCCEEDED`, `FAILED`, `UNKNOWN`, and `CANCELLED`. `UNKNOWN` is a first-class state and must not be guessed into success or failure.

### PublishReasonCode

Initial stable machine-readable reason codes: `MISSING_REQUIRED_FIELD`, `INVALID_FIELD_VALUE`, `UNSUPPORTED_CATEGORY`, `INVALID_PRICE`, `INVALID_STOCK`, `INVALID_LOCATION`, `INVALID_MEDIA_METADATA`, `AUTHORIZATION_DENIED`, `AUTHORIZATION_UNKNOWN`, `RISK_BLOCKED`, `RISK_UNKNOWN`, `IDEMPOTENCY_REPLAY`, `IDEMPOTENCY_CONFLICT`, `DUPLICATE_DRAFT`, `UNKNOWN_PREVIOUS_OUTCOME`, `MANUAL_REVIEW_REQUIRED`, and `READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY`.

### PublishEvaluationContext

A local DTO carrying only approved non-secret state: `authorization_state`, `risk_state`, `synthetic_fixture`, `request_time`, and `local_profile_reference`.

It must not contain Cookie, Token, Secret, Password, Session Material, browser Profile, Playwright object, HTTP client, platform page, or real customer data.

## T3 approved permission, credential, risk-control, and platform boundaries

### PublishAuthorizationState

Approved states: `AUTHORIZED`, `DENIED`, and `UNKNOWN`.

Rules:

- Only `AUTHORIZED` may continue local evaluation.
- `DENIED` must produce `UNAUTHORIZED` with reason `AUTHORIZATION_DENIED`.
- `UNKNOWN` must fail closed with `UNAUTHORIZED` and reason `AUTHORIZATION_UNKNOWN`.
- The local publishing boundary does not log in, resolve platform permission, or acquire platform authorization.

### PublishRiskState

Approved states: `CLEAR`, `BLOCKED`, and `UNKNOWN`.

Rules:

- Only `CLEAR` may continue local evaluation.
- `BLOCKED` must produce `RISK_BLOCKED`.
- `UNKNOWN` must fail closed with reason `RISK_UNKNOWN`.
- Verification codes, platform checks, rate limits, and risk controls must not be bypassed.

### Credential boundary

The publishing Domain, local Service, validation logic, audit records, and future repository protocol must not accept or store Cookie, Token, Secret, Password, Session Material, browser Profile, raw Credential, Playwright object, HTTP client, or platform page object.

`local_profile_reference` and `seller_profile_reference` are non-secret local references only.

### Platform boundary

The local publishing boundary is synthetic and deterministic. It does not open a browser, call Playwright, access Xianyu, log in, upload media, create or edit a listing, publish a listing, perform HTTP, WebSocket, DNS, or other external network access, or infer real platform state.

Any future platform adapter must be separately authorized and must remain outside Domain, Repository, and local Service responsibilities.

### Fail-closed rule

Missing, denied, unknown, blocked, expired, unavailable, verification-required, or ambiguous permission or risk state must fail closed. It must not be interpreted as permission to publish or permission to continue to platform behavior.

## T4 approved validation, idempotency, duplicate, and uncertainty behavior

### Deterministic validation order

The local boundary uses this fixed fail-closed order:

1. Request shape validation.
2. Synthetic-fixture validation.
3. Required-field validation.
4. Field normalization validation.
5. Authorization validation.
6. Risk-state validation.
7. Idempotency validation.
8. Duplicate detection.
9. Uncertainty-state validation.
10. Local READY decision.

Once a higher-priority failure occurs, later steps must not override it.

### Required-field boundary

At minimum the boundary must validate `draft_id`, `draft_revision`, `request_id`, `idempotency_key`, `title`, `description`, `category_reference`, `price`, `stock`, `location_reference`, `authorization_state`, `risk_state`, and `synthetic_fixture`.

Media is metadata only in this change; upload is not required or performed.

Missing, blank, type-invalid, out-of-bound, or unsupported fields must produce structured `INVALID_INPUT`.

### Normalization boundary

Normalization must be deterministic, local, and side-effect free. It must not call the network, read environment Credential, change business meaning, execute templates, run scripts or expressions, infer data from unknown fields, or silently discard unsupported fields.

### Idempotency rules

Same idempotency key with the same canonical request fingerprint returns a replay result consistent with the first local decision and reason `IDEMPOTENCY_REPLAY`. It must not create a new attempt.

Same idempotency key with a different fingerprint returns `CONFLICT` and `IDEMPOTENCY_CONFLICT`. It must not overwrite the previous request.

Different idempotency key with the same draft revision and fingerprint returns `DUPLICATE` with `DUPLICATE_DRAFT` or enters explicit manual review. It must not automatically publish a second time.

### Unknown outcome behavior

If a future historical attempt exists with outcome `UNKNOWN`, the boundary must not automatically retry, assume success, assume failure, or create a new attempt. It must return `MANUAL_REVIEW` with reason `UNKNOWN_PREVIOUS_OUTCOME` and wait for a separately authorized human or corrective process.

### READY rule

A local PublishDecision may be `READY` only when the synthetic fixture is confirmed, required fields are valid, authorization is `AUTHORIZED`, risk is `CLEAR`, no idempotency conflict exists, no duplicate draft blocks execution, no historical `UNKNOWN` outcome exists, and no real platform state confirmation is required.

`READY` still does not authorize publication.

## T5 approved ownership, persistence, lifecycle, audit, and failure boundaries

### Ownership boundary

The owner module remains `worker.publish`, matching the capability Registry ownership for CAP-XY-PUBLISH.

A future Python package may be recorded as `app/xianyu_system/worker/publish`, following the existing worker package convention, but this task creates no package, module, Domain, Service, Repository, Worker, Adapter, schema, or Migration.

### Future publish domain responsibilities

A future publish domain may own ListingDraft, PublishRequest, PublishValidationResult, PublishDecision, PublishAttempt, PublishOutcome, lifecycle rules, reason codes, and fail-closed invariants.

### Future application and service boundary

A future application or local Service boundary may orchestrate local validation and request a repository protocol. It must not call a real platform, receive Credential material, open a browser, invoke Playwright, or infer platform state.

### Future repository protocol

A future repository protocol may provide a local persistence abstraction only after separate authorization. T5 approves conceptual persistence rules but no physical table, column, index, ORM model, or Migration.

### Future platform adapter

Any platform adapter must be a separate capability or separately explicit approved boundary. It must not be mixed into the publish Domain, Repository, or local Service responsibilities.

### Conceptual persistence requirements

Future persistence must preserve idempotency-key uniqueness, immutable request fingerprints, monotonic attempt numbers, non-overwritten outcomes, preserved `UNKNOWN` outcomes, append-only audit history, identifiable synthetic fixtures, and fail-closed transaction failure.

Future persistence must not store Credential, Cookie, Token, Secret, Password, Session Material, browser Profile, media binaries, raw platform responses, real customer data, or real personal data.

### Lifecycle boundaries

ListingDraftLifecycle states are `DRAFT`, `VALIDATED`, `READY_FOR_MANUAL_REVIEW`, and `ARCHIVED`. It intentionally has no `PUBLISHED` state because the local boundary does not publish.

PublishRequestLifecycle states are `RECEIVED`, `VALIDATED`, `REJECTED`, `READY`, `DUPLICATE`, `CONFLICT`, and `MANUAL_REVIEW`.

PublishAttemptLifecycle states are `NOT_STARTED`, `IN_PROGRESS`, and `COMPLETED`. The current change does not create a real `IN_PROGRESS` attempt.

PublishOutcomeType remains `SUCCEEDED`, `FAILED`, `UNKNOWN`, and `CANCELLED`, and belongs to a future separately authorized platform boundary.

### Audit boundary

A future audit event may include `event_id`, `event_type`, `occurred_at`, `request_id`, `draft_id`, `draft_revision`, `attempt_id`, `decision_type`, `reason_code`, `correlation_id`, and `synthetic_fixture`.

A future audit event must not include full description, full media metadata, Credential, Cookie, Token, Secret, Password, Session Material, browser state, raw platform response, real personal data, or real customer data.

### Failure classification

Approved stable failure categories are `VALIDATION_ERROR`, `AUTHORIZATION_ERROR`, `RISK_BLOCKED`, `IDEMPOTENCY_CONFLICT`, `DUPLICATE_REQUEST`, `PERSISTENCE_ERROR`, `ADAPTER_ERROR`, `TIMEOUT`, `UNKNOWN_OUTCOME`, and `CANCELLED`.

Validation errors are not retried. Authorization and risk errors are not bypassed. Idempotency conflicts do not overwrite previous requests. Duplicate requests do not automatically create a second attempt. Persistence errors do not produce `READY`. Adapter errors and timeouts are not automatically interpreted as success or failure. `UNKNOWN_OUTCOME` does not automatically retry.

All retry, scheduler, and background-worker behavior requires future separate authorization and is not implemented by CHG-0006 T1-T5.
