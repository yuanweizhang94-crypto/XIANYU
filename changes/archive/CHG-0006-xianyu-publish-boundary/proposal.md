# CHG-0006 Proposal

Status: ARCHIVED
Change ID: CHG-0006-xianyu-publish-boundary

## Purpose

Prepare a formally reviewable local Xianyu publishing boundary without using Playwright, accessing a real account, or publishing a listing.

## Target capability

- `CAP-XY-PUBLISH`

## Current authorization

CHG-0006 is APPROVED for sequential governance and design work only.

The project owner authorized T1 through T5 in this execution, with each task completed, verified, and committed independently.

T1 through T6 are complete.

T7 is the next task but is not authorized in this execution and has not started.

No Runtime implementation, capability binding, reviewer request, Ready transition, auto-merge, or merge is authorized.

## Candidate goals for later review

The following topics are candidates for later review only and are not approved implementation commitments:

- Define Listing Draft, Publish Request, Publish Decision, Validation Result, Publish Attempt, and Publish Outcome terminology.
- Define future local synthetic publishing-boundary inputs and outputs.
- Define field validation, permission, risk-control, fail-closed, and audit boundaries.
- Define future Account, Schedule, Media, Browser, and Platform Adapter boundaries.
- Define idempotency, duplicate request, conflict, and unknown-result questions.
- Provide acceptance inputs for later review.

## Non-goals

- No Playwright call.
- No browser startup.
- No real Xianyu page access.
- No real account login.
- No real listing creation, editing, or publishing.
- No image or video upload.
- No HTTP, WebSocket, DNS, or other external network request.
- No Cookie, Token, Secret, Password, Session Material, or browser Profile storage.
- No real item, customer, or personal data handling.
- No Worker, Repository, Service, Scheduler, API, or Web UI implementation.
- No database table or Migration.
- No dependency addition.
- No capability binding.
- No Runtime implementation.
- No WeCom integration.
- No AI Provider integration.

## Security boundary

Use synthetic fixtures only.

Do not commit, store, or log credential material, browser profiles, real item data, real customer data, or personal data.

Do not infer platform permission, risk-control, or publishing behavior.

Do not bypass platform verification, risk-control, authorization, or permission control.

Fail closed on ambiguous, conflicting, unsupported, or missing publishing input.

## Approval boundary

Creation of this DRAFT does not approve T1, Runtime implementation, capability binding, reviewer request, Ready transition, auto-merge, or merge.

Moving CHG-0006 beyond DRAFT requires a new explicit project-owner authorization.

## T1 project-owner approval record

The project owner explicitly approves CHG-0006 and authorizes the sequential completion of governance and design tasks T1 through T5.

Each task must still be executed, verified, and committed independently.

T1 is complete. T2 is the next executable task.

T6 implementation is not authorized. Runtime implementation, capability binding, Ready transition, Reviewer request, Auto-merge, Merge, branch deletion, Playwright, browser automation, real Xianyu access, listing publication, media upload, external network access, Credential handling, WeCom integration, and AI Provider integration remain unauthorized.

## T2 completion record

T2 is complete. Approved terminology and local data contracts are recorded in design.md and CAP-XY-PUBLISH.md.

T3 is the next executable task.

CAP-XY-PUBLISH remains planned and unbound. T6 implementation remains unauthorized.

## T3 completion record

T3 is complete. Permission, credential, risk-control, and platform boundaries are approved as design-only constraints.

T4 is the next executable task.

Unknown authorization and unknown risk fail closed. Platform adapter behavior remains separate and unimplemented.

## T4 completion record

T4 is complete. Validation, idempotency, duplicate, and uncertainty behavior are approved as design-only constraints.

T5 is the next executable task.

READY remains local validation only and does not authorize publication. UNKNOWN outcomes require manual review and no automatic retry.

## T5 completion record

T5 is complete. Ownership, persistence, lifecycle, audit, and failure boundaries are approved as design-only constraints.

T6 Implement only the separately approved local publishing boundary is the next task, but T6 is not authorized in this execution and has not started.

CAP-XY-PUBLISH remains planned and unbound with null active_change, empty implementation_paths, empty test_paths, and null last_verified_commit. PR #6 remains Draft, open, and unmerged.

## T6 completion record

T6 is complete. The local deterministic publish boundary is implemented under `app/xianyu_system/worker/publish/`.

Implemented files are `__init__.py`, `domain.py`, `fingerprint.py`, `validation.py`, `persistence.py`, and `service.py`. Migration `0005_xianyu_publish_boundary` creates local publish request, sanitized audit, and attempt-snapshot tables.

The implementation remains local and synthetic only. It does not publish listings, start a PublishAttempt, call Playwright, start a browser, access Xianyu, upload media, perform external network access, accept Credential material, or infer real platform state.

T7 Add unit, contract, security, and active-change acceptance tests is the next task, but T7 is not authorized in this execution and has not started. CAP-XY-PUBLISH remains planned and unbound with no Registry evidence.

## T7 completion record

T7 is complete. Permanent local Publish boundary tests now cover domain normalization, fingerprint stability, validation fail-closed ordering, service idempotency/duplicate/UNKNOWN/persistence-failure behavior, local SQLite persistence contracts, migration constraints, security boundaries, import safety, and active-change acceptance.

CAP-XY-PUBLISH remains planned and unbound until T8. T7 coverage includes test_publish_domain.py, test_publish_fingerprint.py, test_publish_validation.py, test_publish_service.py, test_publish_persistence.py, and test_publish_security.py. T8 is the next task and has not started in the T7 commit.

## T8 Phase A evidence candidate record

T8 Phase A registers CAP-XY-PUBLISH as `implementing` with exact local deterministic Publish implementation and test evidence paths. `active_change` is `CHG-0006-xianyu-publish-boundary`; `last_verified_commit` remains null until the Phase A Candidate commit has completed local verification and GitHub Actions. T8 remains incomplete until Phase B records the verified Candidate SHA.


## CHG-0006 T8 Phase B verification record

CAP-XY-PUBLISH evidence paths are registered and verified for the local deterministic Publish boundary.

Evidence Candidate SHA: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`

Candidate GitHub Actions result: quality push, quality pull_request, tests push, tests pull_request, security push, and security pull_request all completed successfully.

Registry status: verified

Active change: null

Last verified commit: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`

Tasks: 8 / 9

Next task: T9 Complete final PR administration

T9 is not authorized and has not started. PR #6 remains Draft, open, and unmerged. Verified does not authorize Ready, reviewer request, review submission, auto-merge, merge, archive, branch deletion, CHG-0007, real Xianyu access, listing publication, media upload, Credential handling, browser automation, external platform access, platform adapter, scheduler, worker loop, retry behavior, dependency change, or workflow change.


## T9 Ready Candidate preparation

CHG-0006 status is VERIFYING for final review preparation. T1-T8 are complete, and T9 remains incomplete until the Ready transition and final administration record are complete.

CAP-XY-PUBLISH remains verified and frozen. The Evidence Candidate remains `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`, and last_verified_commit must continue to point to that Candidate.

PR #6 must remain Draft, open, and unmerged until the Ready Candidate local gates and GitHub Actions pass. No manual Reviewer request, review submission, auto-merge, merge, close, archive, branch deletion, CHG-0007 creation, Runtime change, Migration semantic change, Registry change, dependency change, workflow change, browser/platform/Credential behavior, WeCom integration, or AI Provider integration is authorized.


## T9 final PR administration result

T9 final PR administration is complete. T1-T9 are complete, PROJECT_STATE completed is 9 / 9, and PROJECT_STATE next_task is null.

T9 Ready Candidate SHA: `52e389e804ca24f144c6c1bd73cc21b1ba21d4cb`

PR #6 is Ready for review, open, and unmerged. CAP-XY-PUBLISH remains verified and frozen with last_verified_commit `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`. No manual Reviewer request, review submission, auto-merge, merge, close, archive, branch deletion, CHG-0007 creation, Runtime change, Migration semantic change, Registry change, dependency change, workflow change, browser/platform/Credential behavior, WeCom integration, or AI Provider integration occurred.

Merge requires separate explicit authorization against the exact current PR HEAD.


## Archive transition record

PR #6: merged.

Merged feature HEAD: `417db817d8641755fb5f66d78db6c143bd1dc53c`.

Merge commit: `dcc4a770dfcb3a69fb3809cb3868ed752813482b`.

Merge method: normal two-parent merge commit.

Merged-main quality/tests/security: success.

CHG-0006 is complete and archived.

CAP-XY-PUBLISH remains verified.

Evidence Candidate remains: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`.

last_verified_commit remains: `66ac5134e0f62b9b30b7423e7bebab297c5ced7a`.

The archive transition does not re-verify CAP-XY-PUBLISH. The seven implementation paths remain unchanged. The ten test paths remain semantically unchanged. Only the CHG-0006 acceptance evidence location moves from `changes/active/` to `changes/archive/`.

This archive transition does not authorize Runtime, Migration, platform access, listing publication, media upload, browser automation, Playwright, Credential, Cookie, Token, Secret, Password, Session, browser Profile, WeCom, AI Provider, branch deletion, or CHG-0007 work.
