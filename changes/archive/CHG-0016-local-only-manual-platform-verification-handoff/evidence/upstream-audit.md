Change ID: CHG-0016-local-only-manual-platform-verification-handoff
Status: ARCHIVED
# Upstream Evidence

## Summary

`upstream_capability_evidence`:

- pinned upstream has automated captcha solving.
- pinned upstream has no manual-only mode.
- latest upstream has no manual-only mode.
- upstream Issues/PRs reviewed.
- local historical research reviewed.
- no reusable manual bridge found.

## Pinned upstream evidence

- Path: `D:/xianyu-upstream-pilot`.
- Repository: `zhinianboke/xianyu-auto-reply`.
- SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.
- Pinned source exposes automated captcha handling paths through browser automation, DrissionPage, real_mouse, and remote solver flows.
- The online-chat Token cache and automatic-reply Token cache are separate.
- The manual Cookie input UI exists, but it is not a pure official verification handoff and is not suitable for the current Token-stage verification gap.
- Login and face-verification UI paths do not satisfy the IM Token `FAIL_SYS_USER_VALIDATE` manual handoff requirement.

## Latest upstream evidence

- Latest observed SHA: `fbeea7a09e616e6739bebd871c2c4647207ceefc`.
- Recent upstream changes include Token API mode, remote Token fallback, risk logs, and slider retry/cooldown work.
- No direct manual-only local verification handoff was found.

## Upstream Issues and PRs reviewed

- PR #266: token/slider and remote-token oriented changes; not manual-only.
- PR #260: slider-success retry-limit fix; not manual-only.
- Issue #253: slider verification difficulties; no reusable manual bridge.
- Issue #259: x5sec not issued after visual slider success; no reusable manual bridge.
- Issue #268: triggered slider report; no reusable manual bridge.

## Existing local implementation search

- CHG-0009 wrapper diagnostics are operations-only.
- CHG-0010 local worker is frozen/deprecated and not a sender for this work.
- CHG-0012 closed with `BLOCKED_BY_PLATFORM_VERIFICATION_GAP`.
- Local search found no pure manual verification bridge.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The handoff must not create a second IM, Token, WebSocket, sender, automatic reply, or browser solver.

## Why upstream cannot satisfy the requirement

Pinned/latest upstream have automated and remote-solving paths, but not the required local owner-only manual verification handoff.

## Approved exception ADR

Not applicable.

## Component owner

Upstream remains the business runtime owner. The proposed handoff is operations-only.

## Retirement plan for overlapping local code

Any future helper must remain local-only and must be retired or disabled when no longer needed.
