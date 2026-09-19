# CHG-0038 Native WebSocket Registration Readiness

Change ID: CHG-0038-websocket-registration-readiness
Status: VERIFYING
Created: 2026-09-20
Owner task: xianyu_auto_reply_post_reconnect_recovery

## User Outcome

Restore reliable automatic replies after Native WebSocket reconnect without rebuilding reply templates, refreshing Session/Cookie/Token, or restarting every account.

Production evidence: account 2804730247 had successful automatic replies earlier on 2026-09-19. A confirmed buyer message at 23:58 was visible in Online Chat but produced no Native MessageHandler receive log and no AutoReplyService activity row while Native status still reported connected + token_ready.

Smallest success test: a reconnect is not reported CONNECTED until the existing /reg request receives a matching successful response; missing registration confirmation re-enters the existing reconnect path while preserving the current Token.

## Scope

ALLOWED_CHANGE_SCOPE=existing Native WebSocket registration/readiness path in websocket/app/services/xianyu/xianyu_async.py; one vendor patch; focused tests; sanitized evidence; bounded single-account production recovery.
FORBIDDEN_CHANGE_SCOPE=Auto Reply rules/templates, ChatNew business logic, Session/Cookie refresh semantics, QR/password login, Publisher, orders, Scheduler, Frontend, database schema, global WebSocket restart, all-account restart, buyer test messages.

## Development precheck

TASK_TYPE=REPAIR
FAILURE_REASON=Native WebSocket can report connected after reconnect without proving /reg registration acknowledgement, allowing heartbeat-live but business-message-silent half-health.
RESPONSIBLE_LAYER=XIANYU upstream-native WebSocket registration lifecycle.
CURRENT_UPSTREAM_CAPABILITY=PARTIAL; pinned upstream bda1a859 has /reg + ackDiff but does not wait for /reg confirmation before declaring readiness.
CURRENT_LOCAL_CAPABILITY=PARTIAL; current production WebSocket lineage retains the same blind registration sequence. ChatNew independently has a matching-mid registration wait, proving the protocol pattern is already available locally.
CURRENT_RUNTIME_CAPABILITY=PARTIAL; production status can be connected/token_ready while a confirmed buyer message leaves no MessageHandler or AutoReplyService trace.
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=websocket/app/services/xianyu/xianyu_async.py init/registration readiness only.
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=init() sends /reg, sleeps, sends ackDiff, logs registration complete, and the caller marks CONNECTED without validating /reg.
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=No parallel implementation is required; patch the existing upstream-native lifecycle and reuse the existing reconnect loop.

## Upstream capability audit

Pinned upstream path D:/xianyu-upstream-pilot at bda1a859df63fa5f24e51398fa80a23490bb6dfc was read directly. Its Native xianyu_async.py has the same blind /reg -> sleep -> ackDiff sequence. No newer upstream fix was proven during this incident.

## Pinned upstream evidence

Pinned upstream SHA: bda1a859df63fa5f24e51398fa80a23490bb6dfc.
Native owner: websocket/app/services/xianyu/xianyu_async.py.
Local comparison: backend-web/app/services/chat_new/im_client.py starts its receive loop and waits for a matching /reg mid response before declaring registration successful.

## Existing local implementation search

Current runtime already contains _pending_mid_futures, _dispatch_mid_response, tracked message tasks, MessageHandler, ConnectionManager heartbeat handling, and the reconnect state machine. No second socket owner, parser, reply engine, or login path is needed.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Low if the patch stays inside the existing Native WebSocket owner. High if a new listener, second Auto Reply connection, or second reconnect manager is created; those are forbidden.

## Why upstream cannot satisfy the requirement

The pinned upstream implementation itself contains the readiness gap. A minimal downstream patch is required until upstream ships and proves registration acknowledgement gating.

## Approved exception ADR

Not applicable.

## Component owner

Upstream Native WebSocket service remains the sole Auto Reply receive owner. XIANYU owns the minimal patch, regression evidence, and runtime activation.

## Retirement plan for overlapping local code

Retire this patch when a future upstream version waits for /reg acknowledgement before declaring Native readiness and passes the same reconnect regression.
