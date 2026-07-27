# CAP-XY-PUBLISH

## Purpose

Define publishing boundary without invoking Playwright or publishing listings.

## Requirements

- Status remains planned.
- Define behavior and boundaries only.
- Do not implement runtime code before a later approved change.

## Scenarios

- Serve as requirement and acceptance input.
- Serve as ownership input for duplicate capability checks.

## Failure behavior

- Stop when permission, credential, specification, or risk state is uncertain.
- Do not guess missing business behavior.

## Security boundaries

- Do not hold real Cookie, Token, Secret, customer data, or browser credentials.
- Do not bypass platform verification or risk controls.

## Out of scope

- Runtime implementation is out of scope for CHG-0001.
- External platform or account access is out of scope for CHG-0001.

## Verification

- The capability exists in the registry with status planned.
- The specification path is unique.
- No conflicting implementation path exists.

## CHG-0006 T1 approval record

CHG-0006 is APPROVED for sequential governance and design tasks T1 through T5. T1 is complete.

CAP-XY-PUBLISH remains planned, unbound, without implementation paths, without test paths, and without a verified commit.

T6 implementation, Runtime, capability binding, Registry evidence, Ready transition, Reviewer request, Auto-merge, and Merge are not authorized.

## CHG-0006 T2 approved terminology

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


T2 records terminology only. CAP-XY-PUBLISH remains planned and unbound.
