# CHG-0006 Proposal

Status: DRAFT
Change ID: CHG-0006-xianyu-publish-boundary

## Purpose

Prepare a formally reviewable local Xianyu publishing boundary without using Playwright, accessing a real account, or publishing a listing.

## Target capability

- `CAP-XY-PUBLISH`

## Current authorization

This change is DRAFT preparation only.

No CHG-0006 task is approved.

T1 has not started.

No task may execute while this change remains DRAFT.

DRAFT state has no executable next task.

Moving beyond DRAFT requires separate explicit project-owner approval.

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
