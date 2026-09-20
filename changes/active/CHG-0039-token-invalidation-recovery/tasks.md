# CHG-0039 Tasks

Change ID: CHG-0039-token-invalidation-recovery
Status: VERIFYING

- [x] T1 Reproduce target explicit invalidation reusing the same Token.
- [x] T2 Verify pinned upstream contains the same gap.
- [x] T3 Build the minimal CookieTokenManager candidate.
- [x] T4 Compile the candidate and build a local image from the current CHG0038 base.
- [x] T5 Prove explicit-invalidated target cache becomes a miss in the candidate.
- [x] T6 Prove natural expired-cache startup fallback remains available.
- [x] T7 Recover 2214313339860 with a fresh Token using target-only state cleanup plus the existing restart owner.
- [x] T8 Verify Token fingerprint changed and matching /reg ACK/message-loop readiness recovered.
- [x] T9 Add the deterministic vendor patch, focused tests and sanitized evidence to XIANYU.
- [ ] T10 Activate CHG0039 globally only in a separately approved production switch.
- [ ] T11 Complete final 2214313339860 organic buyer-message E2E.

## Upstream capability audit

Pinned upstream lacks explicit invalidation discrimination.

## Pinned upstream evidence

bda1a859df63fa5f24e51398fa80a23490bb6dfc.

## Existing local implementation search

Existing CookieTokenManager and mark_token_cache_expired are reused.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second owner.

## Why upstream cannot satisfy the requirement

Pinned upstream reuses explicit-invalidated expired cache.

## Approved exception ADR

Not applicable.

## Component owner

CookieTokenManager.

## Retirement plan for overlapping local code

Retire the patch when upstream provides equivalent behavior.
