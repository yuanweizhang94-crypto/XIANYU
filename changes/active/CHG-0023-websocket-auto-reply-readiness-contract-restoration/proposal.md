# CHG-0023 WebSocket Auto Reply Readiness Contract Restoration

Status: DRAFT

Change ID: CHG-0023-websocket-auto-reply-readiness-contract-restoration

CHG0023_SCOPE_APPROVED=true

Implementation remains prohibited while this Change is `DRAFT`.

## Execution contract

User outcome: restore the previously validated Auto Reply readiness contract without creating a new Auto Reply, Token, Session, WebSocket, or availability owner.

Confirmed blocker: current production WebSocket status omits `token_ready`, while current Backend readiness precedence can classify connected/token-ready accounts as ONLINE before authoritative `HUMAN_QR_REQUIRED`, platform-verification, or expired Session state is applied.

Smallest success test: the existing WebSocket status producer exposes current-token readiness, and the existing Backend readiness consumer evaluates authoritative QR/PVR/Session blockers before `connected + token_ready -> ONLINE`.

## Purpose

PURPOSE=restore previously validated Auto Reply readiness contract.

HISTORICAL_REFERENCE=`73316f1d26c41545a61a965cc9a5a18f144fef74`.

KNOWN_MISSING_CONTRACT:

- WebSocket: `token_ready` status producer.
- Backend: authoritative `HUMAN_QR_REQUIRED`, platform verification, and expired Session state must precede `connected + token_ready -> ONLINE`.

## Scope

ALLOWED_CHANGE_SCOPE=existing WebSocket status producer for `token_ready`; existing Backend Auto Reply readiness precedence; targeted/regression tests; sanitized evidence; minimal Runtime activation only after a later executable status authorizes implementation.

FORBIDDEN_CHANGE_SCOPE=Chat changes; Session renewal redesign; Token cache redesign; Publisher; Scheduler; JZAI; COMPANY; ZIDONG; Payment; Item Sync; new Auto Reply system; new Token owner; new Session owner; new WebSocket owner; new availability service.

NEW_AUTO_REPLY_SYSTEM=false
NEW_TOKEN_OWNER=false
NEW_SESSION_OWNER=false
NEW_WEBSOCKET_OWNER=false
NEW_AVAILABILITY_SERVICE=false

## Current acceptance-control truth

Confirmed positive controls remain the four Owner-recovered accounts: `2804730247`, `1951966327`, `2214313339860`, `2196106636`.

Conditional positive control: `2219319284219` (王侠). Current authoritative record: `SESSION_STATE=SESSION_CHECK_PENDING`, `HUMAN_QR_REQUIRED=false`, existing Chat connected/readable, WebSocket connected, `TOKEN_REFRESH_STATE=success_from_cache`. It must not be recorded as `SESSION_AUTH_VALID=true` unless later read-only evidence proves Session convergence.

Untouched negative controls: `2221422775489`, `2221501265279`. They remain authoritative `HUMAN_QR_REQUIRED` controls and must not be scanned or auto-recovered by this Change.

## Upstream capability audit

Existing project evidence records that the latest inspected upstream base `9cbb3725b7e91daec33cb824a3ff4bd84acdcb12` does not provide the missing `token_ready` readiness contract. This DRAFT does not repeat or expand that audit.

## Pinned upstream evidence

Historical validated reference: `73316f1d26c41545a61a965cc9a5a18f144fef74`. Current implementation work, when later authorized, must compare only the exact missing behavior against the current pinned/runtime source and must not cherry-pick the historical commit wholesale.

## Existing local implementation search

Prior triage established that the existing owners already exist: WebSocket `CookieManager.get_task_status()` is the status producer, the internal status endpoint already passes status fields through, and Backend `_build_business_capabilities()` is the readiness consumer. No parallel implementation is allowed.

## Reuse decision

Decision: PATCH_UPSTREAM

Reuse the existing WebSocket status producer and existing Backend readiness consumer. Restore only the missing/incorrect contract behavior.

## Duplicate implementation risk

HIGH if this Change introduces a second Auto Reply, Token, Session, WebSocket, readiness, availability, login, or recovery owner. The approved scope forbids those paths.

## Why upstream cannot satisfy the requirement

The latest inspected upstream state does not contain the validated readiness restoration already proven in project history; the smallest approved path is a minimal patch to the existing owners.

## Approved exception ADR

Not applicable. This is `PATCH_UPSTREAM`, not `BUILD_LOCAL_EXCEPTION`.

## Component owner

Existing WebSocket status owner and existing Backend Auto Reply capability/readiness consumer remain authoritative. Session/QR/platform-verification authority remains with the existing Session/platform state.

## Retirement plan for overlapping local code

No overlapping owner may be created. If upstream later provides an equivalent verified contract, the minimal local patch must be reviewed for retirement in favor of upstream.
