# 2026-09-21 account enable / Native Chat runtime evidence

## Current account authority

At root-cause capture time, the only enabled account was 2219319284219. Its canonical Session state was REAL_BROWSER_LOGIN_READY with no HUMAN_QR_REQUIRED evidence.

## Real enable timeline

2026-09-21 17:49:14:
- formal account enable lifecycle invoked the existing WebSocket start_account owner;
- CookieManager account task was created;
- XianyuAsync instance was created.

2026-09-21 17:49:15:
- Native WebSocket connected;
- matching /reg ACK was confirmed.

2026-09-21 17:49:16:
- registration completed;
- connection state became connected;
- background tasks and message listening started.

This proves ACCOUNT_ENABLE_RUNTIME_REHYDRATION_MISSING is not the Native WS root cause.

## First divergence

Beginning at 17:49:20, current Backend Online Chat repeatedly called the WebSocket internal Native Chat conversation/message endpoints. The current CHG0039 WebSocket runtime returned HTTP 404 because the routes were not present in that image.

The production-equivalent local source already contains those routes and the matching XianyuAsync LWP methods.

## Runtime/source comparison

Current CHG0039 runtime versus production-equivalent WebSocket/Common source produced only three relevant business-source SHA differences:
- internal.py: runtime lacks Native Chat RPC routes;
- cookie_token_manager.py: intentional CHG0039 delta;
- xianyu_async.py: intentional CHG0038 delta plus local Native Chat methods absent from runtime.

CHG0041 is constructed from the current CHG0039 runtime preimage and adds only the Native Chat deltas, so it preserves CHG0038 and CHG0039.

## Upstream

Pinned upstream origin/main fdc8eb039be771456ecfbbbe43fa26f57feb3947 does not contain the local Native Chat internal RPC integration. A fresh fetch attempt during this Change failed with a network reset.

## Final production readback after CHG0041 activation

The production WebSocket service is running:

`xianyu-chg0041-websocket:native-chat-rpc-20260921-r1`

The previous CHG0039 image has no running container.

All four production services read healthy after the CHG0041 switch:
- Backend: PASS
- Frontend: PASS
- WebSocket: PASS
- Scheduler: PASS

Current Account Authority contains exactly one enabled account:
- 2219319284219 / 王侠

The formal read-only Account API reports:
- ACCOUNT_ENABLED=true
- ACCOUNT_ONLINE=true
- LOGIN_READY=true
- HUMAN_QR_REQUIRED=false

All other 15 accounts remain disabled. WebSocket connection-stats reports one total Native instance, one connected instance, and only 2219319284219 in connected_account_ids. Formal status readback for every disabled account found no running/connected/reconnecting account runtime.

### Message-loop-ready proof

No account restart was issued after CHG0041 activation.

At 18:21:11 the WebSocket cold-start reconciliation automatically created the sole Native account task for 2219319284219. The same runtime then logged:
- matching WebSocket /reg response confirmed successfully;
- registration completed;
- connection state connecting -> connected;
- all background tasks started;
- "开始监听WebSocket消息";
- continuing successful heartbeat responses.

Therefore:

`WANGXIA_MESSAGE_LOOP_READY=true`

### Production Native Chat RPC proof

The current formal Backend path `/api/v1/chat-new/conversations/{account_id}` was invoked read-only for 2219319284219 and returned SUCCESS.

The current Backend `websocket_client.chat_conversations` call to the production WebSocket shared Native owner returned:
- code=200
- success=true
- data present

Before CHG0041, the corresponding WebSocket internal path returned HTTP 404. After CHG0041, the same capability is present and the Backend production call succeeds.

Therefore:

`NATIVE_CHAT_RPC_RUNTIME_MATCH=true`
`NATIVE_CHAT_RPC_PRODUCTION_CALL=PASS`
`PRE_FIX_ENDPOINT_404=false` for the current production runtime.

### Existing production hotfix preservation

The active WebSocket image carries:
- CHG0038 registration-readiness label and matching-ACK implementation;
- CHG0039 token-invalidation-recovery label and explicit invalidation precedence implementation;
- CHG0041 Native Chat RPC restore label.

The active Backend image is:
`xianyu-chg0040-backend-web:qr-cookie-enrichment-20260921-r3`

and carries the CHG0040 QR cookie enrichment production label.

No Backend, Frontend or Scheduler component was replaced for CHG0041.

## Final root-cause statement

ROOT_CAUSE=WebSocket image baseline drift dropped existing Native Chat RPC while Backend expected the shared Native owner.
FIRST_DIVERGENCE=Backend Native Chat RPC -> WebSocket internal endpoint -> HTTP 404.
POST_FIX=same production Backend Chat path -> shared Native owner -> HTTP 200 / success=true.
ACCOUNT_ENABLE_LIFECYCLE_ITSELF_NOT_PRIMARY_ROOT_CAUSE=true.
RUNTIME_IMAGE_CAPABILITY_REGRESSION=true.
