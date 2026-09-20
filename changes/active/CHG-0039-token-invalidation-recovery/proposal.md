# CHG-0039 Token Invalidation Recovery

Change ID: CHG-0039-token-invalidation-recovery
Status: VERIFYING
Created: 2026-09-20
Owner task: xianyu_target_account_autoreply_recovery

## User Outcome

Make an explicit account-level Token invalidation actually produce a fresh Token generation instead of immediately reusing the same invalidated cache during WebSocket startup.

Production evidence on account 2214313339860:

- old Token generation: 2026-09-20 10:00:48
- old Token fingerprint: f0a26cb28e07
- restart with invalidate_token_cache=true marked the cache expired
- startup immediately logged the same Token cache hit and reused the same Token/Device
- connected + registration ACK + heartbeat returned, but the requested fresh-token recovery did not occur

A bounded target-only recovery then removed only that stale cache row and reused the formal single-account restart owner. The next startup produced a true cache miss, called the existing Token API, generated Token fingerprint 2edfb21da80d at 2026-09-20 22:37:55, completed matching /reg ACK, ackDiff initialization and the normal message loop.

## Scope

ALLOWED_CHANGE_SCOPE=existing Native WebSocket Token cache lookup in websocket/app/services/xianyu/cookie_token_manager.py; one vendor patch; focused tests; sanitized evidence.
FORBIDDEN_CHANGE_SCOPE=AutoReplyService, reply rules/templates, image/text configuration, Publisher, ChatNew, Session/Cookie renewal semantics, global WebSocket restart, all-account restart, database schema.

GLOBAL_TOKEN_INVALIDATION=false
GLOBAL_WEBSOCKET_RESTART=false
OTHER_ACCOUNT_RESTART=false

## Development precheck

TASK_TYPE=REPAIR
FAILURE_REASON=explicit account-level Token invalidation writes expire_at/renew_expire_at/updated_at to the same timestamp, but startup allow_expired=True treats that explicit recovery marker as a normal expired cache and reuses the exact Token that was invalidated.
RESPONSIBLE_LAYER=XIANYU upstream-native Token lifecycle.
CURRENT_UPSTREAM_CAPABILITY=PARTIAL; pinned upstream bda1a859df63fa5f24e51398fa80a23490bb6dfc has the same allow_expired fallback and does not distinguish an explicit invalidation marker.
CURRENT_LOCAL_CAPABILITY=PARTIAL; current CHG0038 production lineage preserves the same behavior.
CURRENT_RUNTIME_CAPABILITY=DEFECT_PROVEN; 2214313339860 reproduced invalidate=true -> same Token fingerprint reused.
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=CookieTokenManager._get_cached_token only.
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=it cannot distinguish a deliberate recovery invalidation from a naturally expired startup cache.
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=No parallel implementation is required; patch the existing cache owner with one explicit marker guard.

## Upstream capability audit

Pinned upstream websocket/app/services/xianyu/cookie_token_manager.py was read directly. The function checks completeness, classifies expiry, and then allows expired fallback. It does not distinguish an explicit recovery invalidation marker from natural expiry.

## Pinned upstream evidence

UPSTREAM_SHA=bda1a859df63fa5f24e51398fa80a23490bb6dfc
UPSTREAM_OWNER=websocket/app/services/xianyu/cookie_token_manager.py
UPSTREAM_EXPLICIT_INVALIDATION_GUARD=false

## Existing local implementation search

Current CHG0038 runtime and local recovery source were compared with the upstream owner. Existing mark_token_cache_expired() already emits a stable marker by writing expire_at, renew_expire_at and updated_at to the same timestamp. No second invalidation owner is required.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Low only if the existing CookieTokenManager lookup is patched. Creating a second Token cache owner, second restart path, or separate WebSocket recovery worker is forbidden.

## Why upstream cannot satisfy the requirement

The pinned upstream implementation has the same allow_expired behavior and no guard for the explicit invalidation marker, so the required recovery semantics are absent upstream.

## Approved exception ADR

Not applicable. No BUILD_LOCAL_EXCEPTION is used.

## Component owner

XIANYU upstream-native CookieTokenManager remains the sole Token cache owner. XianyuAsync remains the sole Native WebSocket owner.

## Retirement plan for overlapping local code

Retire this downstream patch when a future upstream version distinguishes explicit invalidation from natural expired-cache fallback and passes the same regression.

## Production activation

Not activated globally in this change cycle. A global WebSocket image switch was intentionally withheld because the user required account-level repair only and normal accounts must not be restarted. Runtime recovery for 2214313339860 was completed with a bounded one-row target cache cleanup plus the existing single-account restart owner.

Final buyer-message E2E remains pending natural inbound.
