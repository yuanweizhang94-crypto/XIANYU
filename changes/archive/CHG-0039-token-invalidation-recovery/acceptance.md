# CHG-0039 Acceptance

Change ID: CHG-0039-token-invalidation-recovery
Status: ARCHIVED

## Source gates

- patch targets only websocket/app/services/xianyu/cookie_token_manager.py
- explicit invalidation marker is handled before ordinary expiry classification
- natural expired startup fallback is preserved
- no AutoReplyService/template/Publisher/Session changes
- targeted tests pass
- validate_change.py passes
- git diff --check passes

## Runtime evidence already proven

OLD_TOKEN_SHA12=f0a26cb28e07
OLD_TOKEN_GENERATION=2026-09-20 10:00:48
INVALIDATE_TRUE_REUSED_OLD_TOKEN=true

TARGET_CACHE_ROW_CLEANUP_ONLY=true
NEW_TOKEN_SHA12=2edfb21da80d
NEW_TOKEN_GENERATION=2026-09-20 22:37:55
TOKEN_CHANGED=true
TOKEN_REFRESH_STATE=success
REGISTRATION_ACK=PASS
MESSAGE_LOOP_READY=true

GLOBAL_WEBSOCKET_SWITCH=true
OTHER_ACCOUNT_RESTART=false
PRODUCTION_IMAGE=xianyu-chg0039-websocket:token-invalidation-recovery-20260920-r1
RUNTIME_EXPLICIT_INVALIDATION_GUARD=true
POST_SWITCH_TOTAL_INSTANCES=8
POST_SWITCH_NORMAL_CONNECTED=6
POST_SWITCH_TARGET_SESSION_EXPIRED=2

## Deferred gate

REAL_E2E_STABILITY=PENDING_REAL_INBOUND

## Upstream capability audit

Pinned upstream lacks explicit invalidation discrimination.

## Pinned upstream evidence

UPSTREAM_SHA=bda1a859df63fa5f24e51398fa80a23490bb6dfc

## Existing local implementation search

Existing CookieTokenManager and mark_token_cache_expired are reused.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second Token/WebSocket owner.

## Why upstream cannot satisfy the requirement

Pinned upstream allows explicit-invalidated cache to enter expired fallback.

## Approved exception ADR

Not applicable.

## Component owner

CookieTokenManager.

## Retirement plan for overlapping local code

Remove the patch after equivalent upstream behavior is proven.
