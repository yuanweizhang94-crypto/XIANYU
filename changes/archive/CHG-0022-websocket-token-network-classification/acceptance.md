# CHG-0022 Acceptance

Status: ARCHIVED

Change ID: CHG-0022-websocket-token-network-classification

- [x] DNS failure is classified NETWORK; cached Token remains valid; paid remote Token acquisition is not triggered by reconnect classification.
- [x] Pre-connect `socket.gaierror` is NETWORK and does not invalidate Token.
- [x] Pre-connect `ConnectionResetError` is NETWORK and does not invalidate Token.
- [x] Network timeout is NETWORK and uses existing network backoff.
- [x] Short `attempt_duration` alone cannot invalidate Token/cache.
- [x] Existing explicit Token/Auth/Session rejection semantics still invalidate/refresh through the existing Token/Session owner; executable rejection used exactly one cache invalidation after a bounded two-attempt Token refresh.
- [x] Four-account simultaneous DNS fault injection produces zero cache invalidation/remote-token fan-out from reconnect logic and uses network backoff.
- [x] Network recovery reuses the existing Token and reconnect path without forced paid Token refresh.
- [x] `HUMAN_QR_REQUIRED` executable behavior remains fail-closed with zero remote Token/password/CAPTCHA/cache-invalidation actions.
- [x] Healthy 180-second maintenance executable behavior reuses the live Token and performs zero active Token refresh calls.
- [x] Session/Cookie authority remains separated from Auto Reply: the three authoritative `HUMAN_QR_REQUIRED` Session states were preserved while their existing expired-startup Auto Reply Token caches could still reconnect WebSocket.
- [x] Auto Reply sole owner, Chat/Orders/Scheduler/Publisher ownership was not modified by this Change.
- [x] WebSocket-only production activation completed; Backend/Scheduler/Frontend/MySQL/Redis/COMPANY/JZAI container/code identities were not changed.
- [x] `SOURCE_RUNTIME_MATCH=true`; production health/readback passes and no new remote Token storm/reconnect loop has been observed after deployment.
- [x] `git diff --check` is required before commit; repository verification is blocked only by the proven pre-existing unrelated CHG-0020 archive missing `design.md`/`tasks.md`, with `CHG0022_NEW_VERIFY_FAILURES=0`.

## Upstream capability audit

Latest upstream contains the same defect; no equivalent fix found.

## Pinned upstream evidence

`9cbb3725b7e91daec33cb824a3ff4bd84acdcb12`.

## Existing local implementation search

No tracked equivalent repair found.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second WebSocket/Token/Session/Auth owner is permitted.

## Why upstream cannot satisfy the requirement

The defective reconnect classification is present in current upstream.

## Approved exception ADR

Not applicable.

## Component owner

Existing `XianyuAsync` reconnect loop and existing Token/Session authority.

## Retirement plan for overlapping local code

Review for retirement when upstream ships equivalent behavior.
