# CHG-0023 Tasks

Status: APPROVED

Change ID: CHG-0023-websocket-auto-reply-readiness-contract-restoration

- [ ] T1 Re-run project context after Owner approval to execute; refresh current upstream/local/runtime read-only evidence and confirm the historical contract delta is still exact.
- [ ] T2 Restore only the existing WebSocket `token_ready` status producer and existing Backend authoritative readiness precedence; do not add new owners or endpoints.
- [ ] T3 Run targeted producer/consumer tests for healthy token-ready, no-token, authoritative HUMAN_QR_REQUIRED, platform-verification-required, and expired Session states.
- [ ] T4 Run CHG-0022 network/token regressions plus QR fail-closed and healthy-maintenance regressions without real messages or QR actions.
- [ ] T5 If tests pass and executable status authorizes it, activate only the minimal required Runtime components and verify source/runtime match plus current acceptance controls.
- [ ] T6 Persist exact Change implementation/evidence to GitHub only after production acceptance; keep unrelated governance debt and other repositories out of scope.

## Upstream capability audit

Use the recorded audit in `proposal.md`; refresh only before executable implementation if current evidence changes.

## Pinned upstream evidence

`9cbb3725b7e91daec33cb824a3ff4bd84acdcb12`; historical reference `73316f1d26c41545a61a965cc9a5a18f144fef74`.

## Existing local implementation search

Existing WebSocket status and Backend readiness owners are already identified. No parallel implementation is planned.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second owner, service, endpoint, cache, scheduler, or recovery path is permitted.

## Why upstream cannot satisfy the requirement

The latest inspected upstream state lacks the validated readiness contract behavior required by this Change.

## Approved exception ADR

Not applicable.

## Component owner

Existing WebSocket status producer and Backend readiness consumer.

## Retirement plan for overlapping local code

No overlapping local owner will be introduced; retire any minimal patch when a verified upstream equivalent is available.
