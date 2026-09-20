# CHG-0038 Design

Change ID: CHG-0038-websocket-registration-readiness
Status: ARCHIVED

## Execution contract

Keep the existing Native WebSocket architecture. Repair only the readiness transition:

socket open
-> send /reg with unique mid
-> receive until matching /reg response
-> require code=200
-> send ackDiff
-> short synchronization settle
-> only then allow CONNECTED and normal receive/heartbeat operation.

If /reg confirmation does not arrive within a bounded timeout, raise into the existing network reconnect path so the current Token is preserved.

## Production evidence driving the design

- 2804730247 successfully auto-replied earlier on 2026-09-19.
- A confirmed buyer message at 23:58 was visible in Online Chat but produced no Native receive/MessageHandler/AutoReplyService trace.
- Native status remained connected + token_ready.
- AutoReplyService records activity in finally for success, skip, no-rule, pause, and failure, so a zero-row event places divergence before AutoReplyService.
- Native init() does not validate /reg.
- ChatNew uses the same endpoint/app-key/protocol family and already demonstrates matching-mid registration wait.
- Dual ChatNew + Native connections existed before the failure while Auto Reply still worked, so dual-connection existence alone is not treated as root cause.

## Minimal implementation

1. Add a bounded helper in xianyu_async.py that receives frames during initialization until headers.mid matches the /reg mid.
2. Reuse ConnectionManager heartbeat recognition.
3. Preserve unexpected early business/LWP frames through existing dispatch and MessageHandler paths.
4. Require matching registration code=200.
5. Timeout raises asyncio.TimeoutError and reuses existing reconnect handling.
6. Non-200 registration fails closed and must not produce CONNECTED.
7. Keep existing ackDiff after confirmed registration.

No new WebSocket owner, no new parser, no new reply worker, no new Token/Session owner.

## Allowed change scope

- websocket/app/services/xianyu/xianyu_async.py registration readiness.
- vendor patch/test/docs/evidence for CHG-0038.
- optional single affected-account restart using invalidate_token_cache=false.

## Forbidden change scope

- automatic reply configuration/content.
- frontend autoChat logic.
- ChatNew connection semantics.
- QR/password login.
- Token/Cookie invalidation for operational recovery.
- global WebSocket service restart for immediate recovery.
- real buyer/customer test messages.

## Upstream capability audit

Pinned upstream owns the capability but lacks acknowledgement gating.

## Pinned upstream evidence

bda1a859df63fa5f24e51398fa80a23490bb6dfc; websocket/app/services/xianyu/xianyu_async.py.

## Existing local implementation search

Reuse existing MessageHandler, _dispatch_mid_response, _create_tracked_task, ConnectionManager heartbeat handling, and reconnect loop.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The design adds no second lifecycle owner.

## Why upstream cannot satisfy the requirement

Pinned upstream readiness semantics are insufficient for reconnect half-health.

## Approved exception ADR

Not applicable.

## Component owner

Existing upstream Native WebSocket service.

## Retirement plan for overlapping local code

Remove after equivalent upstream registration gating is adopted and runtime-proven.
