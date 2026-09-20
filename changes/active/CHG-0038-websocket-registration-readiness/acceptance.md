# CHG-0038 Acceptance

Change ID: CHG-0038-websocket-registration-readiness
Status: VERIFYING

## Required source gates

- Patch touches only websocket/app/services/xianyu/xianyu_async.py.
- /reg uses an explicit reg_mid.
- initialization waits for the matching reg_mid response.
- code=200 is required before readiness.
- registration timeout cannot produce CONNECTED.
- timeout reuses existing network reconnect semantics and does not force Token/Cookie invalidation.
- early non-registration frames are not silently dropped.
- ackDiff remains in the existing Native registration flow.
- no Auto Reply rule/template behavior changes.
- no ChatNew protocol rewrite.
- no second WebSocket owner.

## Required regression gates

- vendor artifact is deterministic and targets the existing owner only.
- focused CHG-0038 tests pass.
- existing CHG-0022 network/token classification regression passes.
- current ChatNew reconnect/spinner/cache regressions pass.
- validate_change.py passes.
- verify_repository.py passes or any unrelated pre-existing failure is documented.
- git diff --check passes.
- security scan passes.

## Production safety gates

- no global WebSocket restart for immediate recovery.
- no all-account restart.
- no QR/password login.
- no Cookie/Session refresh.
- no reply-template rewrite.
- no buyer/customer test message.
- if a single affected account is restarted, use existing /internal/accounts/{id}/restart with invalidate_token_cache=false and verify connected/token_ready afterward.

## Production success criteria

Immediate recovery: affected account reconnects using existing valid Token/Cookie and returns connected + token_ready without human verification.

Permanent Runtime acceptance is complete. Production now runs xianyu-chg0038-websocket:registration-readiness-20260920-r2; all 8 active accounts completed matching /reg acknowledgement and entered the normal message loop. One account (2217936413500) received an initial real /reg code=401, did not enter CONNECTED, reused the existing reconnect path, then completed a successful acknowledgement and message-loop transition. A later organic buyer inbound on account 2221384086829, item 1086370184047, produced MessageHandler -> AutoReplyService -> item default rule -> image send success -> text send success -> sanitized reply activity send_status=success. See evidence/20260920-production-activation-and-real-e2e.md.

## Upstream capability audit

Pinned upstream WebSocket registration exists but has no acknowledgement gate.

## Pinned upstream evidence

bda1a859df63fa5f24e51398fa80a23490bb6dfc.

## Existing local implementation search

Reuse existing Native reconnect/message stack and ChatNew matching-mid registration pattern.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No parallel owner is introduced.

## Why upstream cannot satisfy the requirement

The pinned implementation can expose false-ready connection state.

## Approved exception ADR

Not applicable.

## Component owner

Existing Native WebSocket service.

## Retirement plan for overlapping local code

Retire after upstream parity is verified.
