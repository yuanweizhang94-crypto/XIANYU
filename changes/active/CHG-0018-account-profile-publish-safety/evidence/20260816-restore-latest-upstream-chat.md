# 2026-08-16 Restore latest upstream Chat authority

## Execution contract

- User outcome: latest upstream ChatNew/Chat auth/conversation behavior becomes the production authority; old XIANYU PVR/readiness/manual-verification state may not short-circuit an upstream lazy connect.
- Confirmed blocker: production Chat-owned files contain large XIANYU-only readiness/PVR/auth-fingerprint state machines. Shared account serialization re-emits historical `session_maintenance.consumers.chat` PVR before a new connect. The frontend renders that historical state and can avoid the upstream lazy connect.
- Smallest success test: replace Chat-owned files with current `origin/main` exact content, minimally remove Chat-only state from shared files, preserve independent Auto Reply/QR/Publish fixes, then show one canary request reaches latest upstream without an old PVR short-circuit.
- Reuse decision: `ADOPT_UPSTREAM` for Chat-owned code; `PATCH_UPSTREAM` only where shared XIANYU production fixes must remain. Duplicate-development risk is reduced by deleting the XIANYU Chat readiness/PVR/manual-verification layer rather than adding another owner.
- Rollback: restore the 13 pre-deployment files/static frontend snapshot. No Cookie/Profile/account data is part of this patch.

## Upstream authority

- Fresh fetch: `git fetch origin main` on 2026-08-16.
- `origin/main`: `bf252be357f5e4261b04ce2b7419c5574aaf1b55`.
- The fetched commit title is `新增只发卡券开关`. The task text described this SHA with a different commit title; the actual fetched SHA/content is authoritative.
- Latest upstream Chat route remains lazy: account selection/connect invokes `ImSessionManager.get_or_connect()`; manager creates/reuses `GoofishImClient`; client is cache-first and uses the existing upstream Token owner only on cache miss.

## CHAT_FILE_MATRIX

### UPSTREAM_IDENTICAL before this repair

- `backend-web/app/api/routes/chat_new_image.py`
- `backend-web/app/api/routes/chat_new_ws.py`
- `backend-web/app/api/routes/chat_quick_phrase.py`
- `backend-web/app/services/chat_new/avatar_service.py`
- `backend-web/app/services/chat_new/official_blacklist_service.py`
- `backend-web/app/services/chat_new/push_message_parser.py`
- frontend Chat auxiliary files not modified by XIANYU Chat overlays (`useChatNewWs.ts`, `OrderDetailModal.tsx`, `QuickPhrasesPanel.tsx`, `orderStatus.ts`).

### XIANYU_MODIFIED_CHAT_ONLY / stale Chat surface -> latest upstream exact target

- `backend-web/app/api/routes/chat_new.py`
- `backend-web/app/services/chat_new/im_client.py`
- `backend-web/app/services/chat_new/im_session_manager.py`
- `frontend/src/api/chatNew.ts`
- `frontend/src/pages/chat-new/ChatNew.tsx`
Target normalized SHA256 values exactly matched fresh `origin/main` for all five core Chat files before patch generation.

`chat_customer_order.py` and `CustomerOrdersPanel.tsx` are intentionally preserved at the production order-surface version: the `bf252be` change there depends on the same commit's new `card_only_delivered` order model/database field. Importing that unrelated order schema change would violate this Chat-only repair boundary.

### SHARED_WITH_AUTO_REPLY_FIX

- `common/services/im_token_api.py`: not changed. Runtime `request_im_token()` and `request_im_token_with_fallback()` are source-identical to latest upstream; XIANYU-only difference is the existing remote optional-fallback balance cooldown/lock. Auto Reply per-account single-flight remains owned by `XianyuAsync._auto_reply_token_refresh_lock`.
- `websocket/app/services/xianyu/xianyu_async.py`: not changed; existing Auto Reply single-flight/token-storm fix retained.
- `websocket/app/services/xianyu/cookie_token_manager.py`: not changed; live connected WS keeps its current Token when PVR is marked.
- PID/zombie/connection manager fixes: not changed.

### SHARED_WITH_QR_FIX

- `backend-web/app/api/routes/qr_login.py`: not changed; no eager Chat convergence.
- `backend-web/app/api/routes/shared_scan.py`: not changed; no eager Chat convergence.
- `backend-web/app/services/account_service.py`: not changed; QR-only convergence owner remains removed.

### SHARED_WITH_PUBLISH_FIX / account capability UI

- `backend-web/app/api/routes/cookies.py`: retain Auto Reply/Publish capability logic, but Chat capability now uses only the latest-upstream manager's live connected IDs. Historical Chat metadata/PVR/auth-convergence is not consulted for current Chat usability.
- `frontend/src/types/index.ts`: unchanged; XIANYU account/publish types remain owned by the existing production overlay. The unrelated `bf252be` order-only fields are not imported by this Chat repair.

### XIANYU_WRAPPER_ONLY removed

- Backend Chat manual-verification routes are removed by exact upstream `chat_new.py`.
- `backend-web/app/services/websocket_client.py`: remove only human-verification methods.
- `websocket/app/api/routes/internal.py`: remove only human-verification internal routes.
- `common/services/cookie_renew_browser_service.py`: remove only the human-verification headed worker/method and now-unused `threading` import.
- `common/utils/cookie_refresh.py`: remove the now-dead Chat-only `auth_convergence_fingerprint` helper; Session/Cookie utilities remain.

## Pre-deployment validation

- Python compile for all nine modified Python files: PASS.
- Latest-upstream exact source comparison for core Chat-owned files: 5/5 PASS.
- Shared-state checks: old `read_only_diagnostic`, old Chat PVR branch, Chat auth-convergence gate and manual human-verification wrapper absent from target.
- QR no-eager-convergence checks: 3/3 PASS.
- Auto Reply single-flight + live-token preservation checks: PASS.
- `im_token_api.request_im_token` and `request_im_token_with_fallback` source equivalence to latest upstream: PASS.
- Frontend production build (`tsc && vite build`): PASS, 2692 modules transformed. The final build uses the current production/order surface plus latest upstream `chatNew.ts` and `ChatNew.tsx`; existing dependency/browser-data warnings only.
- Incremental patch changed files: 10.
- Patch SHA256: `DCF41E892453F1E0208DF68C24E4D76CBC9851D6398E3FD59E967709D4D47489`.
- Patch `git apply --check`: PASS.
- Patch application normalized content match: 10/10 PASS.

## Production gate

No production Canary result is claimed here yet. Production deployment and the single `2214313339860` canary must be recorded after GitHub persistence. The canary must not scan QR, clear Cookie, delete Profile, send a message, publish a product, or exceed one explicit Chat connect request.


## Production deployment

- Source authority commit before deployment: `6310e62b5c4952af9e8ca8c4f60fb734072f5603`; remote branch equality verified over SSH 443.
- Backend runtime changed: latest core Chat route/client/manager plus the minimal shared Chat-state removals; Backend restarted once and health returned HTTP 200.
- WebSocket runtime changed only to remove the XIANYU manual human-verification wrapper and the now-dead shared Chat auth fingerprint helper. Existing Auto Reply token/reconnect/PID files were not replaced; WebSocket restarted once because its route/common owner changed.
- Frontend: static production output built from current production/order surface plus latest upstream `frontend/src/api/chatNew.ts` and `frontend/src/pages/chat-new/ChatNew.tsx`; `tsc && vite build` PASS. The deployed `index.html` and Chat bundle match the built artifacts. Nginx container restart was not required.
- `qr_login.py`, `shared_scan.py`, `account_service.py` were not touched; QR eager Chat auth remains disabled.
- `common/services/im_token_api.py` was not touched. Runtime `request_im_token()` and `request_im_token_with_fallback()` remain source-identical to latest upstream.
- After WebSocket restart, all six enabled Auto Reply accounts returned to `connected` using existing expired-startup cache semantics; no full-auth storm occurred.

## Canary stale-state cleanup

Canary account: `2214313339860` only.

- Before cleanup, the old XIANYU `session_maintenance.consumers.chat` record was `PLATFORM_VERIFICATION_REQUIRED`, and legacy `auth_convergence` metadata existed.
- The Chat-only cache row was already `EXPIRED`; no additional cache invalidation write was needed.
- Backend restart had already removed any stale in-memory Chat client.
- ORM cleanup removed only `session_maintenance.consumers.chat` and obsolete `auth_convergence` metadata. No raw SQL Cookie mutation was used.
- Authoritative Cookie SHA256 before/after cleanup was identical (`15fb90b...1fa7f7`); Cookie content was never printed.
- `auto_reply_platform_verification`, `platform_restriction`, remaining Session metadata, canonical Profile and account data were preserved.

## Production Canary result

- One preliminary HTTP request was rejected by FastAPI auth with HTTP 401 before the Chat route because an out-of-process settings instance had not loaded the database-managed JWT secret. It made zero Chat manager, Token, CAPTCHA, Cookie, Profile or platform calls and is not counted as a business Chat connect.
- The existing `jwt_secret_service.ensure_jwt_secret_key()` was then used in-memory to load the same managed signing key. No secret/token value was printed.
- Exactly one business POST reached `/api/v1/chat-new/connect/2214313339860` on the production Backend.
- Runtime source proof at the time of the request: `chat_new.py`, `im_client.py`, `im_session_manager.py` hashes exactly matched fresh `origin/main@bf252be357f5e4261b04ce2b7419c5574aaf1b55`.
- Old PVR short-circuit was absent. The request entered latest upstream `ImSessionManager.get_or_connect()` and `GoofishImClient`.
- Cache state: EXPIRED. Latest upstream made one Local Web Token request.
- Fresh platform result: `FAIL_SYS_USER_VALIDATE`.
- Latest upstream then invoked its existing bounded CAPTCHA delegation once. WebSocket verification ran its existing bounded trajectories; Baxia returned status 300 and verification did not succeed.
- Final route response: HTTP 200 application result `success=false`, generic upstream `IM连接失败`; no XIANYU `CHAT_PLATFORM_VERIFICATION_REQUIRED` response was emitted.
- No second Chat connect, Local Token request, QR scan or user-added CAPTCHA retry was made.
- Conversation list was not requested after failed connect because latest upstream conversation retrieval would call `get_or_connect()` again and violate the one-connect canary cap.
- A post-canary read-only `/chat-new/accounts` request shows the canary `connected=false`, `status=active`, and no legacy `chat_state/chat_reason/error_code/connecting` fields.

Conclusion: `LATEST_UPSTREAM_CHAT_RESTORED=true` and `FRESH_UPSTREAM_NATIVE_PLATFORM_VERIFICATION_REQUIRED=true`. The blocker is fresh platform behavior on the current upstream-native request, not stale XIANYU PVR metadata.

## Final Auto Reply/runtime invariants

- `AUTO_REPLY_ONLINE_COUNT=6`; all enabled accounts `is_connected=true`.
- `LIVE_WS_MAINTENANCE_TOKEN_REFRESH=0` after deployment.
- `UNEXPECTED_FULL_AUTH_RETRY=0` after deployment.
- `TOKEN_REFRESH_STORM_REGRESSION=false`.
- WebSocket PID1 is `docker-init`; final process count 3; zombies 0.
- Backend restart count in this task: 1.
- WebSocket restart count in this task: 1.
- Frontend restart count in this task: 0 (static artifact overlay only).
- Scheduler/MySQL/Redis restart counts: 0; their pre-task StartedAt values remained unchanged.
- QR scans: 0; Cookie clears: 0; Profile deletes: 0; real messages sent: 0; real products published: 0.
