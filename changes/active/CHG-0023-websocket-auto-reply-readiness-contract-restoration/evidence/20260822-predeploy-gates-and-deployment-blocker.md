# CHG-0023 predeploy gates and deployment blocker — 2026-08-22

Status: VERIFYING

Change ID: `CHG-0023-websocket-auto-reply-readiness-contract-restoration`

## Formal authority

- Owner approval already persisted: `批准 CHG-0023 按当前已定义 scope 实施`.
- Approval commit / fresh remote readback: `2a55b9c0abaaaa111386cec754d91fab3bb3d42e`.
- This run did not repeat Change transition or Owner approval persistence.

## Current implementation scope

Only the approved existing owners are involved:

- WebSocket producer: `CookieManager.get_task_status()` restores `token_ready=false` by default and `token_ready=bool(current_token)` for a live instance.
- Backend consumer: `_build_business_capabilities()` evaluates authoritative platform-verification, HUMAN_QR/no-credentials, and expired Session blockers before `connected + token_ready -> ONLINE`.
- Existing internal account-status route remains a pure status pass-through.
- `xianyu_async.py` was not modified by CHG-0023.
- No new Token, Session, WebSocket, Auto Reply, availability, login, cache, scheduler, worker, endpoint, or execution owner was introduced.

## Candidate image composition

The current production WebSocket image was re-read before candidate construction and still had the CHG-0022 `xianyu_async.py` SHA256 `9e085fac9e4d5030a9b0ddc329e50434e23ea243dffdf3cc1161696ffd6a4fd5`, but its Session/Cookie closure files had regressed to older pre-closure hashes. Therefore the safe candidate was composed without modifying `xianyu_async.py`:

- Backend candidate: `xianyu-chg0023-backend-web:readiness-contract-20260822-r1`, using the already-validated CHG-0018 auth-cookie closure Backend image plus only the CHG-0023 readiness-consumer postimage.
- WebSocket candidate: `xianyu-chg0023-websocket:readiness-contract-20260822-r1`, using the already-validated CHG-0018 auth-cookie closure WebSocket image, then copying the exact CHG-0022 `xianyu_async.py` unchanged, then applying only the CHG-0023 `cookie_manager.py` readiness-producer postimage.

Build provenance emitted:

- Backend candidate manifest list: `sha256:5c3209890a93599081cc6b2a1de31714598bec7599d8f613f64dfd174c69e6d0`.
- Backend candidate config digest: `sha256:69fc58d07d8dcc8a5fb498ceb215697651c355e269795c8ee9bd181398eff47a`.
- WebSocket candidate manifest list: `sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256`.
- WebSocket candidate config digest: `sha256:deb884f4b0648de3aa0a00e6b16b1f229d7cd87f6db11466218ac0f134927f8e`.

## Candidate exact-source readback

Backend candidate:

- `backend-web/app/api/routes/cookies.py` SHA256 `ac341a5801f3ed521335fcaac3ed05e3f5179d33ce739ee8fc0788f3f2bd9dee`.
- `common/services/account_cookie_service.py` SHA256 `f4fa9d6f1ad329d3abb22b174c3844b4ff631dcd50439834babfbaff86e263e7`.
- `common/utils/cookie_refresh.py` SHA256 `eb9f4abdc03ac6f2852d8efd3e1b4523fc502e0374d507f0f42c445ca31d9d65`.
- `common/services/xianyu_mtop.py` SHA256 `17a9def5f01b1282050f00f44c93500f15c92eda083db4e831e573f46331c6d2`.
- Python compile: PASS.

WebSocket candidate:

- `websocket/app/services/xianyu/cookie_manager.py` SHA256 `b8681987c0aa04f596b5aaaf6a832941e11a576f547987bb3e8c8423eb5c8e5a`.
- `websocket/app/services/xianyu/xianyu_async.py` SHA256 `9e085fac9e4d5030a9b0ddc329e50434e23ea243dffdf3cc1161696ffd6a4fd5` (exact CHG-0022 runtime source retained).
- `common/services/account_cookie_service.py` SHA256 `9f0363b47870dec2436d0215d90f2f4e39bc82026a25c270abd3e28b195f1ee2`.
- `common/utils/cookie_refresh.py` SHA256 `53fdf2b3769daa6767fb869553f934c769ea243175b8e3d87f2cb1823d0f7d70`.
- `common/services/xianyu_mtop.py` SHA256 `97294767b3c728a78a7349c057c37bffa4e15b9b0104c97d8d40f965dc209aa2`.
- `websocket/app/services/xianyu/cookie_token_manager.py` SHA256 `2a727e3f32c8e392a5d59078f09ef75b50c2546a8065d504227aca1c9dfe32ec`.
- `websocket/app/api/routes/password_login.py` SHA256 `0db14da5fc5440572b69ecae3e122e95c47c19c3bae792c3168f8829549a0551`.
- Python compile: PASS.

## Executable candidate gates

CHG-0023 targeted readiness:

- Backend healthy connected + token-ready -> ONLINE: PASS.
- Connected with no token -> not ONLINE: PASS.
- HUMAN_QR blocker before connected/token-ready: PASS.
- Platform-verification blocker before connected/token-ready: PASS.
- `failed_session_expired` blocker before connected/token-ready: PASS.
- `no_credentials` blocker before connected/token-ready: PASS.
- WebSocket producer current-token true: PASS.
- WebSocket producer no-current-token false: PASS.
- WebSocket not-started default includes `token_ready=false` and `token_refresh_state=not_started`: PASS.
- Internal status route pass-through: PASS.

Candidate harness accounting:

```text
CHG0023_BACKEND_TARGETED=6/6_PASS
TOKEN_READY_PRODUCER=3/3_PASS
QR_FALSE_GREEN_STATIC_COUNT=0
```

CHG-0022 network/token regression was rerun against the candidate image's exact `xianyu_async.py`:

```text
CHG0022_NETWORK_REGRESSION=10/10_PASS
REMOTE_TOKEN_CALL_COUNT=0_BY_NETWORK_BRANCH
TOKEN_INVALIDATION_COUNT=0_BY_NETWORK_BRANCH
NETWORK_BACKOFF=true
TOKEN_CACHE_REUSE=true
REMOTE_TOKEN_STORM=false
NEW_REMOTE_TOKEN_BURST_COUNT=0
RECONNECT_LOOP=false
```

Session/Cookie safety regression against both candidate images:

```text
UNKNOWN_COOKIE_WRITERS=0
MISSING_EXPECTED_BASELINE_CALLERS=0
SESSION_COOKIE_CANDIDATE_AUTH_GATE=PASS
STALE_RESPONSE_CAS=PASS
PER_ACCOUNT_SINGLE_FLIGHT=PASS
HUMAN_QR_STICKY_SAME_FINGERPRINT=PASS
SAFE_MTOP_AUTH_PROBE=PASS
```

This proves the candidate preserves the existing authoritative-candidate validation, stale-response CAS discard, per-account renewal single-flight, evidence-qualified QR stickiness for the same fingerprint, and the side-effect-free MTOP auth classifier. No Session/Cookie owner was redesigned.

## Deployment attempt and fail-closed recovery

Targeted production activation was attempted only after all candidate gates above passed. The deployment method intentionally used a single-service compose definition so Frontend, Scheduler, MySQL, Redis, and other services would not be reconciled.

The local execution connector rejected access to the protected runtime `.env` before container recreation:

```text
open D:\xianyu\.local\chg0017-candidate\.env: Access is denied.
```

The same secret-preservation boundary was confirmed when the targeted compose file was moved to the runtime root. No credentials were read, copied, printed, or embedded into a replacement compose file. No alternative secret-bypass deployment path was attempted.

Fresh read-only container recovery after the failed activation confirmed production remained unchanged:

- Backend container ID remains `3057d1d87c93`; image remains `xianyu-chg0018-backend-web:chat-upstream-golden-path-cleanup-20260815-r2`.
- WebSocket container ID remains `9289b9e1493e`; image remains `xianyu-chg0022-websocket:token-network-classification-20260821-r1`.
- Frontend container ID remains `7133189c0906`.
- Scheduler container ID remains `66dbc7e23895`.
- MySQL and Redis remained running/healthy and were not recreated.

Therefore:

```text
TARGETED_DEPLOYMENT=BLOCKED_BEFORE_CONTAINER_RECREATION
PRODUCTION_MUTATION_FROM_DEPLOYMENT_ATTEMPT=false
SOURCE_RUNTIME_MATCH_POSTDEPLOY=NOT_RUN
PRODUCTION_POSITIVE_CONTROL_ACCEPTANCE=NOT_RUN
CONDITIONAL_POSITIVE_ACCEPTANCE=NOT_RUN
UNTOUCHED_NEGATIVE_RUNTIME_ACCEPTANCE=NOT_RUN
POSTDEPLOY_TOKEN_STORM_ACCEPTANCE=NOT_RUN
AUTO_REPLY_FULL_PRODUCTION_READY=false
```

## Safety counters

No account action or business-side-effect action was performed during this continuation:

```text
REAL_MESSAGES_SENT=0
QR_ACTIONS_BY_AUTOMATION=0
PASSWORD_LOGIN_ACTIONS=0
COOKIE_MANUAL_CHANGES=0
TOKEN_MANUAL_REFRESH=0
ITEM_SYNC_PERFORMED=false
CHAT_CONNECT_ACTIONS=0
PUBLISH_ACTIONS=0
PAYMENT_ACTIONS=0
```

Untouched negative controls `2221422775489` and `2221501265279` were not scanned, logged in, refreshed, enabled, or otherwise mutated.

## Blocker

`BLOCKER=LOCAL_EXECUTION_CONNECTOR_PROTECTS_RUNTIME_ENV_FILE_AND_EXPOSES_NO_SAFE_IMAGE_SWAP_ACTION_THAT_PRESERVES_EXISTING_SECRET_ENV_WITHOUT_READING_OR_COPYING_CREDENTIALS`

The correct boundary is to stop deployment rather than copy secrets from container inspection, bake secrets into an image, hot-patch production outside the approved immutable-image path, or run a broader compose reconciliation.

`NEXT_SINGLE_ACTION=STOP_AND_RETURN_TO_COMMANDER_WITH_BLOCKER_EVIDENCE`
