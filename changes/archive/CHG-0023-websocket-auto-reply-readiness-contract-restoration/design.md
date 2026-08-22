# CHG-0023 Design

Status: ARCHIVED

Change ID: CHG-0023-websocket-auto-reply-readiness-contract-restoration

## Design intent

Restore only the previously validated readiness contract in the existing execution owners.

1. WebSocket status producer: expose `token_ready=false` when no current token is present and `token_ready=true` only when the existing live instance owns a current token.
2. Internal status endpoint: preserve the existing pass-through contract; do not create a new endpoint or state owner.
3. Backend readiness consumer: evaluate authoritative `HUMAN_QR_REQUIRED`, platform-verification-required, and expired/invalid Session state before considering `connected + token_ready -> ONLINE`.
4. Healthy authenticated accounts may become ONLINE only after authoritative blockers are absent and the existing WebSocket readiness signals are satisfied.
5. No Session, Token, Chat, WebSocket, Scheduler, Publisher, or availability state machine is redesigned.

## Historical reference

`73316f1d26c41545a61a965cc9a5a18f144fef74` is reference evidence only. Whole-commit cherry-pick is forbidden for implementation of this Change.

## Safety invariants

- `2221422775489` and `2221501265279` remain untouched QR fail-closed negative controls.
- `2219319284219` is excluded from untouched negative controls because the Owner performed a legitimate QR recovery action; it is only a conditional positive until Session convergence is read-only proven.
- No QR scan, password login, automatic login, Cookie refresh, Token refresh, Chat connect, message send, or Item Sync is authorized by this Change. Targeted Runtime deployment is allowed only after the approved executable test and regression gates pass.

## Upstream capability audit

Use the recorded upstream audit from the proposal as the current DRAFT evidence; refresh only if later implementation evidence contradicts it.

## Pinned upstream evidence

Recorded inspected upstream base: `9cbb3725b7e91daec33cb824a3ff4bd84acdcb12`. Historical validated reference: `73316f1d26c41545a61a965cc9a5a18f144fef74`.

## Existing local implementation search

Existing producer/consumer owners are already identified; no second owner or adapter is required.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The principal risk is accidentally creating a parallel readiness/session/token owner. This design forbids that expansion.

## Why upstream cannot satisfy the requirement

The latest inspected upstream state lacks the validated readiness contract behavior required by this Change.

## Approved exception ADR

Not applicable.

## Component owner

Existing WebSocket status producer and Backend readiness consumer.

## Retirement plan for overlapping local code

No overlapping local owner will be added. Any minimal patch should be retired when a verified upstream equivalent becomes authoritative.
