# CHG-0039 Design

Change ID: CHG-0039-token-invalidation-recovery
Status: VERIFYING

## Existing owner

The sole Token owner remains CookieTokenManager. The sole Native WebSocket owner remains XianyuAsync.

No new Token owner.
No new WebSocket owner.
No new parser, Auto Reply engine, Session owner, reconnect manager or scheduler.

## Minimal behavior change

Inside CookieTokenManager._get_cached_token():

1. Preserve missing/incomplete cache handling.
2. Detect the exact explicit invalidation marker written by mark_token_cache_expired():
   expire_at == renew_expire_at == updated_at, with all three present.
3. Treat that row as a cache miss before ordinary expiry classification.
4. Preserve CURRENT and RENEWED behavior unchanged.
5. Preserve natural allow_expired startup fallback unchanged.

This makes invalidate_token_cache=true meaningful without forcing every reconnect to refresh Token.

## Safety

The guard is account-row local.
It does not invalidate any cache itself.
It does not restart any account.
It does not change normal connected maintenance behavior.
It does not change Session/Cookie/QR semantics.

## Upstream capability audit

Same as proposal.md: pinned upstream lacks an explicit-invalidation guard.

## Pinned upstream evidence

UPSTREAM_SHA=bda1a859df63fa5f24e51398fa80a23490bb6dfc

## Existing local implementation search

Existing mark_token_cache_expired() marker and current CookieTokenManager are reused.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No parallel Token or WebSocket owner is introduced.

## Why upstream cannot satisfy the requirement

Pinned upstream reuses explicit-invalidated cache under allow_expired.

## Approved exception ADR

Not applicable.

## Component owner

CookieTokenManager / XianyuAsync.

## Retirement plan for overlapping local code

Remove the vendor patch after upstream ships equivalent tested behavior.
