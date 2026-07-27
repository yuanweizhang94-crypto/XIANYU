# CHG-0006 Design

Status: DRAFT
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
