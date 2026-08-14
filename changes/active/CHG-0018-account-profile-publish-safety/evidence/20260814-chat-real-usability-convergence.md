# CHG-0018 Chat real-usability convergence evidence — 2026-08-14

## Execution contract

- User outcome: account-page `在线聊天=可用` must mean the current ChatNew IM business client is actually usable; a historical READY value must never remain green after the live client is gone.
- Confirmed blocker: ChatNew had two runtime truths and an unbounded user-visible request chain: account capability accepted stored READY, Chat page used the in-memory manager, `ImSessionManager._lock` serialized all account network connects, and Chat platform-validation token flow could wait for the existing 90-second browser-verification owner while frontend Axios also timed out at 90 seconds.
- Smallest success test: reuse upstream ChatNew/GoofishImClient/ImSessionManager, make current manager usability authoritative, bound connect before frontend timeout, make same-account connect single-flight without a global network lock, preserve verification-vs-QR boundaries, and validate without sending messages, publishing products, or scanning QR codes.

## Governance and source baseline

- `AI_PROJECT_HANDOFF_PRESENT=false`.
- `CURRENT_GITHUB=983c86cb3d3d2cb6c6d3efcf23b803f89b03e41d` at task start.
- `CURRENT_LOCAL=983c86cb3d3d2cb6c6d3efcf23b803f89b03e41d` at task start.
- Production runtime at task start used the prior CHG-0018 transient-convergence images.
- `CURRENT_ACTIVE_CHANGE=CHG-0018-account-profile-publish-safety` / `VERIFYING`.
- `UPSTREAM_CURRENT_MAIN_SHA=c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`, freshly read through GitHub SSH over port 443.
- `UPSTREAM_FIRST=true`.
- Reuse decision: `PATCH_UPSTREAM` only. No second Chat service, client pool, Redis status owner, scheduler, or Session owner was created.

## Upstream comparison

The current upstream main still owns the formal online-chat path:

- `frontend/src/pages/chat-new/ChatNew.tsx`
- `frontend/src/api/chatNew.ts`
- `backend-web/app/api/routes/chat_new.py`
- `backend-web/app/services/chat_new/im_session_manager.py`
- `backend-web/app/services/chat_new/im_client.py`
- `GoofishImClient`

Fresh comparison against upstream main showed:

- upstream `ImSessionManager` still uses one global `self._lock` around the complete `get_or_connect()` path, including `await client.connect()`;
- upstream `/chat-new/connect/{account_id}` still has no backend deadline that returns before the frontend generic 90-second timeout;
- upstream ChatNew frontend has no structured platform-verification/connect-timeout error mapping;
- upstream ChatNew has no dedicated interactive platform-verification UI in the Chat page;
- upstream keeps Chat IM Token/device_id separate from the Auto Reply WebSocket, which remains the intended architecture and was preserved.

Therefore:

- `UPSTREAM_CHAT_FIX_AVAILABLE=false` for this observed defect.
- `UPSTREAM_REUSED_FILES=backend-web/app/api/routes/chat_new.py,backend-web/app/services/chat_new/im_session_manager.py,backend-web/app/services/chat_new/im_client.py,frontend/src/api/chatNew.ts,frontend/src/pages/chat-new/ChatNew.tsx`.

## Direct production evidence before repair

### Maru identity

Database/UI mapping confirmed:

- `MARU_ACCOUNT_ID=2214313339860`.
- The mapping was read from the account record; the implementation did not infer account identity from a guessed remark.

### User-visible false truth

The task-start user evidence reported:

- Account page: Chat `可用`.
- ChatNew page: the same account `未连接`.
- The page then surfaced `timeout of 90000ms exceeded`.

Code inspection confirmed why the two pages could disagree:

- Account capability first accepted a current matching live client, but then also accepted `session_maintenance.consumers.chat.state == READY` as green even when the current `ImSessionManager` had no connected matching client.
- ChatNew account list used `manager.get_connected_account_ids()`, i.e. current in-memory runtime only.
- Backend restart necessarily empties `ImSessionManager.clients`; historical READY could therefore remain green on Account while ChatNew truth was disconnected.

`ROOT_CAUSE_CHAT_FALSE_READY=STORED_READY_WAS_ACCEPTED_WITHOUT_CURRENT_LIVE_MATCHING_IM_CLIENT`.

### Duplicate connect evidence

Production Nginx/Backend access logs showed same-account duplicate requests, not merely duplicate toast rendering.

For Maru at 2026-08-14 19:14:03 +08:00:

- two `POST /api/v1/chat-new/connect/2214313339860` completed HTTP 200 about 5 ms apart;
- a `GET /api/v1/chat-new/conversations/2214313339860` then completed HTTP 200.

Earlier, Maru also had two `POST /chat-new/connect` requests ending as HTTP 499 while the browser gave up.

`DUPLICATE_CHAT_CONNECT_REQUESTS=true` before the repair.

The exact initiating UI gesture cannot be reconstructed from access logs alone, but source confirmed there was no same-account in-flight guard. The repair makes the result deterministic regardless of double-click/effect/race origin.

### Exact 90-second endpoint

Nginx production logs directly showed HTTP 499 on:

- `POST /api/v1/chat-new/connect/{account_id}`

including Maru and multiple other enabled accounts.

There was no evidence that the observed 90-second browser timeout was caused by conversations/messages/avatar/profile. Maru's later successful natural attempt obtained conversations immediately after connect.

`TIMEOUT_ENDPOINT=POST /api/v1/chat-new/connect/{account_id}`.

### Slow stage / why 90 seconds

The existing Chat token path uses:

- Token API request timeout: 20 seconds;
- WebSocket open/connect timeout: 30 seconds;
- IM register response timeout: 5 seconds;
- post-register cooldown: 3 seconds.

When Chat Token response matches platform validation such as `FAIL_SYS_USER_VALIDATE`, the old Chat code delegated to `websocket_client.solve_captcha()`.

That existing browser-verification owner computes ordinary call timeout as `max(90, browser_timeout + 60)`; with the normal Chat call it therefore has a 90-second minimum.

Frontend global Axios timeout is also exactly 90 seconds.

In addition, `ImSessionManager._lock` was held around the complete network connect. One account waiting in Token/platform-verification could make unrelated accounts wait behind it.

Thus the observed user chain was:

`global manager lock wait -> Chat token obtain -> platform verification delegation may wait 90s -> frontend 90s expires first -> Nginx 499 -> naked Axios timeout`.

`CHAT_CONNECT_SLOWEST_STAGE=GLOBAL_MANAGER_LOCK_WAIT_BLOCKED_BY_TOKEN_FETCH_PLATFORM_VERIFICATION`.

`GLOBAL_LOCK_HELD_DURING_NETWORK_CONNECT=true` before repair.

## Multi-account platform-verification evidence

Current DB readiness naturally changed during the user's prior UI activity and, when this repair started its read-only sample, all six enabled rows were PENDING; the current stored `PLATFORM_VERIFICATION_REQUIRED_COUNT` was therefore 0. The repair did not manufacture a platform-validation state just for testing.

However, the immediately preceding production Backend log window contained concentrated direct evidence:

- five distinct enabled account IDs entered the platform-validation Chat token path;
- `FAIL_SYS_USER_VALIDATE` appeared 15 times in that sampled log window.

The code path is:

- `GoofishImClient._get_im_token()` / `_fetch_im_token_from_api()`;
- `common.services.im_token_api.request_im_token_with_fallback()`;
- local web mtop API `mtop.taobao.idlemessage.pc.login.token`;
- failure classification before IM registration/normal conversation usage.

Therefore:

- `ROOT_CAUSE_MULTI_ACCOUNT_PLATFORM_VERIFICATION=COMMON_CHAT_TOKEN_API_FAIL_SYS_USER_VALIDATE_PATH`, not six independently proven QR/login expirations.
- `PLATFORM_VERIFICATION_API=mtop.taobao.idlemessage.pc.login.token`.
- `PLATFORM_VERIFICATION_STAGE=TOKEN_OBTAIN`.
- `PLATFORM_VERIFICATION_DOES_NOT_IMPLY_QR=true`.

## Minimal implementation

### 1. Current Chat usability is one shared truth

`ImSessionManager.read_only_diagnostic()` remains strict and non-mutating, and now exposes an effective current Chat business state derived from:

1. account enabled status;
2. current in-memory client existence;
3. `client.is_connected`;
4. current client auth fingerprint matching the authoritative DB Cookie fingerprint;
5. current per-account connect activity;
6. stored failure/readiness evidence only when appropriate.

Effective semantics:

- live connected + matching fingerprint -> `READY`;
- actual per-account connect running -> `CONNECTING`;
- no live client, including stored READY -> `WAITING_CONNECT`;
- fresh platform verification -> `PLATFORM_VERIFICATION_REQUIRED`;
- fresh session/login failure -> `LOGIN_REQUIRED`;
- fresh rate limit -> `RATE_LIMITED`;
- fresh temporary failure -> `TEMPORARY_FAILURE`;
- disabled -> `DISABLED`.

Account capability now consumes this same read-only runtime authority. ChatNew `/accounts` also consumes it.

Therefore Backend restart, stale client, and cookie fingerprint rotation cannot leave Account green merely because DB once recorded READY.

### 2. Stored failure freshness

Stored Chat failure evidence uses its existing `updated_at` and is bounded by the existing Chat Token cache horizon:

- configured `TOKEN_CACHE_TTL_MAX_HOURS`;
- plus the existing maximum Token-cache jitter.

This avoids inventing an unrelated arbitrary status TTL. Old failure evidence can decay to `WAITING_CONNECT`; any later successful business connect immediately overwrites readiness to READY.

### 3. Per-account single-flight

The global network lock was removed from `get_or_connect()`.

Existing manager now keeps an in-process lock per account:

- same account: at most one actual client.connect;
- unrelated accounts: may connect independently;
- no Redis/distributed/new lock service;
- client dictionary remains owned by the same `ImSessionManager`.

`PER_ACCOUNT_CHAT_SINGLE_FLIGHT=true`.

### 4. Bounded backend connect

The client stage budget is explicit from existing owner timeouts:

- local Token: 20s;
- remote fallback Token: 20s;
- WS open: 30s;
- register: 5s;
- post-register cooldown: 3s.

`CHAT_CONNECT_DEADLINE_SECONDS=78`.

The HTTP route adds only 2 seconds for DB/route overhead:

`BACKEND_CONNECT_HTTP_DEADLINE_SECONDS=80`.

Only Chat `connectAccount()` gets an 85-second Axios timeout. Global Axios remains 90 seconds.

Thus:

`BACKEND_RETURN_BEFORE_FRONTEND_TIMEOUT=true`.

### 5. Structured connect failures

Existing `/chat-new/connect` remains the only business connect API and now returns backward-compatible success/message plus structured `error_code`/state/reason.

Supported user-facing codes include:

- `CHAT_PLATFORM_VERIFICATION_REQUIRED`;
- `CHAT_LOGIN_REQUIRED`;
- `CHAT_RATE_LIMITED`;
- `CHAT_TEMPORARY_FAILURE`;
- `CHAT_CONNECT_TIMEOUT`;
- `ACCOUNT_DISABLED`.

The frontend maps connection request timeout to `连接闲鱼聊天超时，请稍后重试`; raw `timeout of 90000ms exceeded` is no longer the intended primary connect error.

### 6. Platform verification is not QR and is not auto-bypassed

The old Chat Token path could automatically delegate a platform-validation response to the browser CAPTCHA solver. For this Chat business connect repair, `FAIL_SYS_USER_VALIDATE`/captcha-classified token evidence now fails closed immediately as `PLATFORM_VERIFICATION_REQUIRED`.

This repair does not:

- generate QR;
- convert platform verification to HUMAN_QR_REQUIRED;
- automatically solve/bypass CAPTCHA;
- forge human interaction;
- create a verification service.

Upstream latest has no dedicated ChatNew interactive verification UI to reuse. The state is surfaced as a platform boundary instead.

### 7. QR semantics

- Chat platform verification -> no QR.
- Chat temporary failure -> no QR.
- Chat rate limit -> no QR.
- Chat disconnected/stale client -> no QR.
- Chat generic `login_required`/session-expired classification -> `LOGIN_REQUIRED`, not QR.
- Explicit `HUMAN_QR_REQUIRED` remains distinct.
- The authoritative Browser/Session lifecycle remains the only owner allowed to conclude actual QR requirement.

### 8. Disabled Chat isolation

`/chat-new/accounts` now requires `XYAccount.status == active` in addition to non-empty Cookie.

Production DB contains five disabled/non-active historical accounts with Cookie data; they remain stored but are excluded from the normal Chat list.

`DISABLED_ACCOUNTS_VISIBLE_IN_CHAT_PAGE=0` by route contract.

`POST /chat-new/connect/{account_id}` also fails closed as `ACCOUNT_DISABLED` before manager connection/token work.

## Frontend request convergence

Before repair there was no same-account in-flight guard. Production access logs proved duplicate same-account POSTs.

Now:

- `connectInFlightRef` blocks a second same-account business POST even before React state commits;
- UI uses a set of connecting account IDs, so one slow account does not disable connect controls for unrelated accounts;
- account row shows connecting/connected/platform verification/login required/rate limited/temporary failure distinctly;
- conversations load only after connected=true or a successful connect;
- connect failure does not cascade into conversations/messages/avatar requests;
- only one toast is emitted by one `handleConnect` execution path.

## Tests

Targeted CHG-0018 suite after repair:

- `204 passed`.

This includes new/updated coverage for:

- stored READY + no live client -> WAITING_CONNECT;
- live connected matching client -> READY;
- disconnected/missing client -> not READY;
- backend restart/empty manager + stored READY -> WAITING_CONNECT;
- successful connect writes READY;
- failed connect overwrites old READY;
- FAIL_SYS_USER_VALIDATE -> PLATFORM_VERIFICATION_REQUIRED;
- login/session failure does not automatically become QR;
- structured connect timeout and partial-client cleanup;
- backend deadline before frontend timeout;
- same-account concurrent connect -> one real connect;
- slow account A does not globally serialize account B;
- Account GET uses strict read-only diagnostic and never get_or_connect;
- strict diagnostic does not mutate Cookie/token cache or send messages;
- disabled accounts hidden from Chat list;
- disabled Chat connect fail-closed;
- no message send in connect path;
- platform verification != QR;
- prior Single QR convergence, Auto Reply transient semantics, Publish readiness, disabled visibility, and PID/zombie tests remain green.

Frontend:

- `tsc && vite build=PASS`.

Diff:

- `git diff --check=PASS` in the cumulative source worktree.

## Production deployment

Only services with current-run runtime code changes were replaced:

- Backend: `xianyu-chg0018-backend-web:chat-real-usability-20260814-r1`;
- Frontend: `xianyu-chg0018-frontend:chat-real-usability-20260814-r1`.

Not restarted/changed for this repair:

- Auto Reply WebSocket source/runtime;
- Scheduler source/runtime;
- MySQL;
- Redis.

Post-deploy health:

- `FRONTEND_HEALTH=200`;
- `BACKEND_HEALTH=200`;
- `WEBSOCKET_HEALTH=200`;
- `SCHEDULER_HEALTH=200`;
- `ACTIVE_SCHEDULER_EXECUTORS=1` (PID1 exact argv `python scheduler/main.py`);
- `WEBSOCKET_INIT=true`.

Resource regression after deploy:

- `WEBSOCKET_ZOMBIES=0`;
- `CHROMIUM_PROCESS_COUNT_IDLE=0`;
- `PLAYWRIGHT_DRIVER_COUNT_IDLE=0`;
- PID1 remains docker-init for WebSocket.

## Production state validation

### Post-backend-restart read-only state

No Chat business connect was forced after deployment because doing so through the actual running HTTP API would require an authenticated UI/API credential. The local app login itself requires its own slider verification; bypassing/minting/reading a JWT solely for acceptance would violate the explicit verification/credential boundary.

Therefore `MARU_CONNECT_ATTEMPTS_AFTER_DEPLOY=0`.

A strict diagnostic/read-only DB snapshot after deployment showed all six enabled accounts as:

- `effective_state=WAITING_CONNECT`;
- `effective_reason=chat_client_not_currently_connected`;
- `client_exists=false`;
- `client_connected=false`;
- `connect_active=false`.

This is expected immediately after Backend restart and directly proves the main false-green bug is closed: manager memory is empty, and the UI authority is no longer historical READY.

The same strict read-only validation showed:

- `cookie_unchanged=true`;
- `token_metadata_unchanged=true`;
- `message_log_delta=0`;
- `publish_log_delta=0`.

### Natural Maru business evidence available before deployment

The user's real UI activity immediately before the repair produced direct production evidence, without this repair generating traffic:

- Maru real connect eventually completed HTTP 200;
- real conversations GET completed HTTP 200 immediately afterward;
- no message-send endpoint was invoked by this acceptance work;
- the same production window also proved duplicate POSTs and prior 499 timeouts.

This confirms the reused upstream ChatNew business path itself can obtain a conversation list. The post-repair timeout/single-flight/status changes are additionally covered by targeted tests and current deployed code/health, but no post-deploy credential was fabricated merely to create another connect sample.

## Side effects

- `REAL_MESSAGES_SENT=0`.
- `REAL_PRODUCTS_PUBLISHED=0`.
- `REAL_PRODUCTS_RELISTED=0`.
- `REAL_PRODUCTS_OFFLINED_BY_TEST=0`.
- `QR_SCANS_TRIGGERED_BY_TEST=0`.
- `COOKIE_WRITE_BY_ACCOUNT_STATUS_ACCEPTANCE=false`.
- `CHAT_TOKEN_MUTATION_BY_STRICT_DIAGNOSTIC=false`.
- `COOKIE_WRITE_BY_MARU_BUSINESS_CONNECT=false` for this repair run because no post-deploy Maru business connect was initiated by automation.

## Vendor patch

- Base: `64c245bc85ac56e34339fa056b0e291a16a3843b`.
- File: `vendor/patches/xianyu-auto-reply/64c245-chg0018-chat-real-usability-convergence.patch`.
- `PATCH_SHA256=A92D08B7C4A3322CCC11CB04165CDAF6468BD47C680380E802CFD699DD1BA412`.
- Patch headers: 41 files.
- `PATCH_CLEAN_APPLY=PASS` from a fresh detached worktree at the exact base.
- Clean-apply targeted tests: `204 passed`.
- `CONTENT_EQUIVALENCE_IGNORING_CRLF=PASS` for all 41 patch paths.
- Byte comparison differs only in three paths due CRLF/LF normalization; semantic/content comparison is exact.

## Preservation / non-regression

- `SINGLE_QR_CONSUMER_CONVERGENCE_PRESERVED=true`.
- `AUTO_REPLY_RECOVERY_PRESERVED=true`.
- `PUBLISH_READINESS_PRESERVED=true`.
- `TRANSIENT_STATUS_CONVERGENCE_PRESERVED=true`.
- `DISABLED_BUSINESS_ISOLATION_PRESERVED=true`.
- `PID_REAPER_PRESERVED=true`.
- `CHAT_STRICT_DIAGNOSTIC_PURE=true`.
- `NEW_CHAT_SYSTEM_CREATED=false`.
- `NEW_SCHEDULER_CREATED=false`.
- `NEW_SESSION_SYSTEM_CREATED=false`.
- `NEW_WEBSOCKET_MANAGER_CREATED=false`.
- `MYSQL_SCHEMA_CHANGED=false`.
