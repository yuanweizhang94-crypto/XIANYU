# CHG-0038 Root Cause and Source Gates — 2026-09-20

Change ID: CHG-0038-websocket-registration-readiness
Status: VERIFYING

## Production symptom

On 2026-09-19 the Native WebSocket fleet experienced a reconnect event. The affected account used in the controlled diagnosis had successful automatic replies earlier the same day. A later confirmed buyer inbound was visible through Online Chat while Native account status still reported connected and token_ready, but the event produced neither a Native MessageHandler receive trace nor an AutoReplyService activity row.

AutoReplyService records its processing outcome in a finally path for success, skip, no-rule, pause, and failure. Therefore the missing activity row places the first divergence before AutoReplyService.

Other accounts produced successful automatic-reply activity after the earlier reconnect window, so the evidence does not support a global Auto Reply configuration/template failure.

## Root cause

Pinned upstream bda1a859df63fa5f24e51398fa80a23490bb6dfc and the current production WebSocket lineage share the same Native registration sequence:

WebSocket open
-> send /reg
-> fixed sleep
-> send ackDiff
-> caller may mark CONNECTED

The sequence does not wait for the server to acknowledge the /reg mid. As a result, transport heartbeat health can be green while business-message subscription readiness is unproven.

ChatNew uses the same protocol family and already demonstrates the required matching-mid registration response pattern. Dual ChatNew + Native connection existence alone is not classified as root cause because automatic replies were proven working while both connection types already existed.

ROOT_CAUSE=NATIVE_WS_FALSE_HEALTH_AFTER_UNCONFIRMED_REGISTRATION
RESPONSIBLE_LAYER=existing upstream Native WebSocket registration lifecycle

## Minimal repair

Patch only websocket/app/services/xianyu/xianyu_async.py:

- generate explicit reg_mid;
- send the existing /reg request;
- receive with a 5-second bound until the matching reg_mid arrives;
- require code=200 before readiness;
- preserve heartbeat frames through the existing ConnectionManager;
- preserve unexpected early frames through the existing mid dispatcher and MessageHandler task path;
- send the existing ackDiff only after registration confirmation;
- allow timeout to enter the existing network reconnect path.

No Auto Reply rules/templates, Session/Cookie/Token owner, ChatNew owner, Frontend, Publisher, Scheduler, database schema, or second WebSocket implementation is introduced.

## Artifact

PATCH=vendor/patches/xianyu-auto-reply/chg0038-websocket-registration-readiness.patch
PATCH_SHA256=45cc5a9a3f73e17743b4d0f7e7a0160fc996eb92c65181ddc38b9233d61a0ecd
UPSTREAM_BASE=bda1a859df63fa5f24e51398fa80a23490bb6dfc
STRICT_APPLY_CHECK=PASS
UPSTREAM_PY_COMPILE=PASS
BEHAVIOR_HARNESS=PASS
BEHAVIOR_CASES=registration_success,timeout,non200_rejection,early_frame_preserved

## Repository verification

TARGETED_CHG0038=6/6 PASS
CHG0022_NETWORK_TOKEN_REGRESSION=6/6 PASS
CHAT_RECONNECT_REGRESSION=9/9 PASS
CHAT_SPINNER_REGRESSION=10/10 PASS
CHAT_CACHE_REGRESSION=5/5 PASS
CHANGE_VALIDATION=PASS
GIT_DIFF_CHECK=PASS
SECURITY_SCAN=PASS
FULL_REPOSITORY=683/683 PASS
PROJECT_STATE_VALIDATION=PASS

The full repository run used worktree-local module resolution (current worktree app + root in PYTHONPATH). Without that environment, one historical editable-install path test resolves ALEMBIC_CONFIG_PATH from D:/XIANYU instead of the isolated worktree; that environment-only condition is not a CHG-0038 failure.

## Production activation closure

The source-baked activation boundary is now closed. Production WebSocket runs:

`xianyu-chg0038-websocket:registration-readiness-20260920-r2`

All 8 active accounts completed a matching successful registration acknowledgement before entering the normal message loop. Account `2217936413500` also produced a real initial registration `code=401`; the new gate did not allow CONNECTED, the existing reconnect path ran, and a later attempt completed a successful acknowledgement and message-loop transition.

A later organic buyer inbound produced the complete post-activation chain:

Native receive
-> MessageHandler
-> AutoReplyService
-> item default rule
-> image send success
-> text send success
-> sanitized reply activity send_status=success

Therefore:

```text
PERMANENT_WEBSOCKET_RUNTIME_PATCH=PASS
REGISTRATION_ACK_PROVEN_COUNT=8
MESSAGE_LOOP_READY_COUNT=8
AUTO_REPLY_REAL_E2E=PASS
```

Full sanitized production evidence: `evidence/20260920-production-activation-and-real-e2e.md`.

## Historical immediate recovery

Before permanent activation, one affected Native WS account had been restarted through the existing internal account restart owner with `invalidate_token_cache=false`.

PRE_TARGET_CONNECTED=true
PRE_TARGET_TOKEN_READY=true
PRE_TARGET_LAST_CONNECTED_AT=2026-09-19T11:14:40.081181+00:00
POST_TARGET_CONNECTED=true
POST_TARGET_TOKEN_READY=true
POST_TARGET_LAST_CONNECTED_AT=2026-09-19T17:38:04.166462+00:00
POST_TARGET_LAST_ERROR_EMPTY=true
POST_TARGET_PLATFORM_VERIFICATION_REQUIRED=false
POST_TARGET_HUMAN_QR_REQUIRED=false
GLOBAL_WEBSOCKET_RESTART=false
TOKEN_CACHE_INVALIDATED=false

Two control accounts retained their original 19:14 last_connected_at values after that target restart, proving no fleet/global reconnect occurred. This block is retained only as historical immediate-recovery evidence; it is superseded by the permanent production activation above.

No customer message text, buyer identifier, Cookie, Token, Authorization, password, QR payload, or other credential is stored in this evidence.
