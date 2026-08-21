# CHG-0023 Acceptance

Status: DRAFT

Change ID: CHG-0023-websocket-auto-reply-readiness-contract-restoration

This DRAFT records the approved scope and future acceptance contract only. It does not authorize implementation.

- [ ] Existing WebSocket status exposes `token_ready=true` only when the existing live instance owns a current token.
- [ ] Existing WebSocket status exposes `token_ready=false` when no current token is present.
- [ ] Existing internal status route returns the existing status payload including `token_ready` and `token_refresh_state` without adding a new endpoint or state owner.
- [ ] Backend authoritative `HUMAN_QR_REQUIRED` takes precedence over `connected + token_ready`; such an account must not be ONLINE.
- [ ] Backend authoritative platform-verification-required state takes precedence over `connected + token_ready`; such an account must not be ONLINE.
- [ ] Backend authoritative expired/invalid Session state takes precedence over `connected + token_ready`; such an account must not be ONLINE.
- [ ] Healthy authenticated controls may become ONLINE only when authoritative blockers are absent and existing WebSocket readiness is satisfied.
- [ ] Confirmed positive-control set remains `2804730247`, `1951966327`, `2214313339860`, `2196106636`.
- [ ] Conditional positive `2219319284219` is added to positive acceptance only after later read-only evidence proves Session convergence; current truth must not be rewritten as `SESSION_AUTH_VALID=true` prematurely.
- [ ] Untouched negative controls `2221422775489` and `2221501265279` remain authoritative `HUMAN_QR_REQUIRED` and fail closed even if future WebSocket observations report connected/token-ready.
- [ ] CHG-0022 DNS/gaierror/reset/timeout/network-recovery, explicit-auth, QR fail-closed, and healthy-maintenance regressions remain PASS.
- [ ] No real message, automated QR action, password login, Cookie refresh, Token refresh, Chat connect, Item Sync, Scheduler/Publisher change, JZAI/COMPANY/ZIDONG/Payment change, or new execution owner is introduced.

## Upstream capability audit

Use the recorded audit in `proposal.md`; later implementation must stop if newer authoritative upstream evidence changes the reuse decision.

## Pinned upstream evidence

Recorded inspected upstream base: `9cbb3725b7e91daec33cb824a3ff4bd84acdcb12`. Historical validated reference: `73316f1d26c41545a61a965cc9a5a18f144fef74`.

## Existing local implementation search

Existing WebSocket status producer, internal pass-through route, and Backend readiness consumer are the only implementation owners in scope.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Any new Auto Reply, Token, Session, WebSocket, availability, login, cache, scheduler, or readiness owner is an acceptance failure.

## Why upstream cannot satisfy the requirement

The latest inspected upstream state lacks the validated readiness contract behavior required by this Change.

## Approved exception ADR

Not applicable.

## Component owner

Existing WebSocket status producer and Backend readiness consumer, with existing Session/platform state remaining authoritative for blockers.

## Retirement plan for overlapping local code

No overlapping local owner may be added. Review any minimal patch for retirement when upstream provides an equivalent verified contract.
