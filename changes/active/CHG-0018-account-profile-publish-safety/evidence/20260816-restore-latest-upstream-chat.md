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
- `backend-web/app/api/routes/chat_customer_order.py` (production was one upstream commit behind latest `bf252be`)
- `frontend/src/pages/chat-new/CustomerOrdersPanel.tsx` (same latest-upstream order-card update)

Target normalized SHA256 values exactly matched fresh `origin/main` for all seven files before patch generation.

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
- `frontend/src/types/index.ts`: retain XIANYU account/publish types while merging latest upstream fields needed by the current Chat/order surface (`only_send_card`, `card_only_delivered`).

### XIANYU_WRAPPER_ONLY removed

- Backend Chat manual-verification routes are removed by exact upstream `chat_new.py`.
- `backend-web/app/services/websocket_client.py`: remove only human-verification methods.
- `websocket/app/api/routes/internal.py`: remove only human-verification internal routes.
- `common/services/cookie_renew_browser_service.py`: remove only the human-verification headed worker/method and now-unused `threading` import.
- `common/utils/cookie_refresh.py`: remove the now-dead Chat-only `auth_convergence_fingerprint` helper; Session/Cookie utilities remain.

## Pre-deployment validation

- Python compile for all nine modified Python files: PASS.
- Latest-upstream exact source comparison: 7/7 PASS.
- Shared-state checks: old `read_only_diagnostic`, old Chat PVR branch, Chat auth-convergence gate and manual human-verification wrapper absent from target.
- QR no-eager-convergence checks: 3/3 PASS.
- Auto Reply single-flight + live-token preservation checks: PASS.
- `im_token_api.request_im_token` and `request_im_token_with_fallback` source equivalence to latest upstream: PASS.
- Frontend production build (`tsc && vite build`): PASS, 2692 modules transformed. Existing dependency/browser-data warnings only.
- Incremental patch changed files: 13.
- Patch SHA256: `3325CCBB263E968486A2804EA816E6B1E18FB8F2DB6C45F3FE9D1A4F19D01F72`.
- Patch `git apply --check`: PASS.
- Patch application normalized content match: 13/13 PASS.

## Production gate

No production Canary result is claimed here yet. Production deployment and the single `2214313339860` canary must be recorded after GitHub persistence. The canary must not scan QR, clear Cookie, delete Profile, send a message, publish a product, or exceed one explicit Chat connect request.
