# CHG-0030 Phase 4 Backend Deploy And Read-Only Preflight Evidence

Date: 2026-08-25

Production Item Sync canary: NOT AUTHORIZED

PR merge: no

Backend-only deployment: yes

WebSocket/Scheduler/Frontend rebuild or restart: no

## Authorization And CI Classification

`PHASE4_AUTHORIZED=true`

`SCOPED_CI=PASS`

`GLOBAL_CI=FAIL_PRE_EXISTING_DEBT`

Independently classified CI state: scoped CHG-0030 tests pass, deterministic security scan passes, quality fails only on CHG-0020 pre-existing archive debt, and broad tests fail only on README drift, CHG-0022 active-path debt, AGENTS drift, and CHG-0020 validation debt.

## Pre-Deploy Runtime Identity

`BACKEND_PRE_IMAGE=xianyu-chg0029-backend-web:selected-account-on-demand-20260825-r2`

`BACKEND_PRE_IMAGE_ID=sha256:4663ca89ba9702bc4f53572593f47f7413cd82e77919ee43b619fba63dbfa7f1`

`BACKEND_PRE_RESTART_COUNT=0`

`BACKEND_PRE_HEALTH=HTTP_200`

`WEBSOCKET_IMAGE=xianyu-chg0023-websocket:readiness-contract-20260822-r1`

`WEBSOCKET_IMAGE_ID=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256`

`WEBSOCKET_RESTART_COUNT=0`

`WEBSOCKET_HEALTH=HTTP_200`

`SCHEDULER_IMAGE=xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1`

`SCHEDULER_IMAGE_ID=sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8`

`SCHEDULER_RESTART_COUNT=0`

`SCHEDULER_HEALTH=HTTP_200`

`FRONTEND_IMAGE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2`

`FRONTEND_IMAGE_ID=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416`

`FRONTEND_RESTART_COUNT=0`

`FRONTEND_HEALTH=HTTP_200`

`NO_UNEXPLAINED_RUNTIME_DRIFT=true`

Current Backend source hashes matched the CHG-0029 evidence for `_exports.py`, `cookies.py`, `product_publish_capability.py`, and `publish_account_capability_service.py` before deployment.

## Selected Account Pre-Deploy Baseline

`SELECTED_ACCOUNT_MASKED=22*********60`

`SELECTED_ACCOUNT_CATALOG_ROWS_PRE=20`

`SELECTED_ACCOUNT_DUPLICATE_GROUPS_PRE=0`

The full account ID was handled only inside the Backend container and was not printed.

## Locked Patch And Image Build

`PATCH_ARTIFACT_SHA256=595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201`

`GIT_BLOB_PATCH_SHA256=595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201`

`CLEAN_REPLAY_SOURCE=D:/xianyu-worktrees/_chg0030_patch_replay2_tmp`

`NEW_BACKEND_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r1`

`NEW_BACKEND_IMAGE_ID=sha256:52af6761e3e6604b5e926977daf46432e53d2ec7bfd4818bb97660e7a1175586`

`BUILD_BASE_IMAGE=xianyu-chg0029-backend-web:selected-account-on-demand-20260825-r2`

`BUILDER_PY_COMPILE_EXIT=0`

`BUILDER_CHG0030_MARKERS_PRESENT=true`

Runtime source hashes copied into the image:

```text
/app/common/schemas/item.py sha256=d0ddda47586132cb0b9121ebe85d16d4d6050d42da2f34e572a90f5c56ed5fd4
/app/backend-web/app/api/routes/cookies.py sha256=1aee43e56fd794a189f9aed3d6d37de3a6f77602b0b366c7a297dbe17a4765a9
/app/backend-web/app/api/routes/items.py sha256=0deb7e3bd6bf0bd5b018731476cc93bf15e3127809a134194353b6d86b59c429
```

The image was built by copying only these patched Backend files from the clean replay source into a temporary builder based on the current CHG-0029 Backend image, then committing with the normal Backend command.

## Deployment And Rollback

`BACKEND_DEPLOYED_CONTAINER=afbd542944ef845db56eb29738227ad245de150d58b97b63a0b951ff7d704e4b`

`BACKEND_DEPLOYED_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r1`

`BACKEND_DEPLOYED_IMAGE_ID=sha256:52af6761e3e6604b5e926977daf46432e53d2ec7bfd4818bb97660e7a1175586`

`BACKEND_DEPLOYED_ENTRYPOINT=null`

`BACKEND_DEPLOYED_CMD=["python","backend-web/main.py"]`

`BACKEND_DEPLOYED_RESTART_COUNT=0`

`BACKEND_DEPLOYED_HEALTH=HTTP_200`

`ROLLBACK_CONTAINER=xianyu_chg0029_backend_web_pre_chg0030_20260825_phase4`

`ROLLBACK_IMAGE=xianyu-chg0029-backend-web:selected-account-on-demand-20260825-r2`

`ROLLBACK_IMAGE_ID=sha256:4663ca89ba9702bc4f53572593f47f7413cd82e77919ee43b619fba63dbfa7f1`

Rollback is available by stopping/removing the new Backend container, renaming the preserved rollback container back to `xianyu_chg0017_backend_web`, and starting it. Rollback was not performed because deployment health and source identity passed.

## Post-Deploy Health

`BACKEND_POST_HEALTH=HTTP_200`

`BACKEND_POST_RESTART_COUNT=0`

`WEBSOCKET_POST_HEALTH=HTTP_200`

`WEBSOCKET_POST_RESTART_COUNT=0`

`SCHEDULER_POST_HEALTH=HTTP_200`

`SCHEDULER_POST_RESTART_COUNT=0`

`FRONTEND_POST_HEALTH=HTTP_200`

`FRONTEND_POST_RESTART_COUNT=0`

## Runtime Source And Log Marker Verification

`RUNTIME_SOURCE_HASH_MATCH=true`

`RUNTIME_CODE_HAS_PREFLIGHT_MARKER=true`

`RUNTIME_CODE_HAS_OPERATION_ACCEPTED_MARKER=true`

`RUNTIME_CODE_HAS_TERMINAL_READBACK_MARKER=true`

`CHG0030_PREFLIGHT_LOG_MARKERS_10M=1`

`CHG0030_OPERATION_ACCEPTED_LOG_MARKERS_10M=0`

`CHG0030_TERMINAL_READBACK_LOG_MARKERS_10M=0`

The operation and terminal markers are present in deployed code but absent from logs because Item Sync was not invoked.

## Post-Deploy Selected-Account Preflight

Route used: `GET /api/v1/cookies/details/paginated` with an internally generated short-lived token.

`SELECTED_ACCOUNT_MASKED=22*********60`

`SELECTED_ACCOUNT_PREFLIGHT_HTTP=200`

`SELECTED_ACCOUNT_ROUTE_TOTAL=1`

`SELECTED_ACCOUNT_ENABLED_NON_DISABLED=true`

`SELECTED_ACCOUNT_CHECKING_STATE=REAL_BROWSER_LOGIN_READY`

`SELECTED_ACCOUNT_CHECKING_ACTIVE=false`

`SELECTED_ACCOUNT_PLATFORM_VERIFICATION_REQUIRED=false`

`SELECTED_ACCOUNT_PLATFORM_VERIFICATION_SOURCE=none`

`SELECTED_ACCOUNT_SESSION_COOKIE_LINEAGE=MATCH`

`SELECTED_ACCOUNT_TOKEN_READY=true`

`SELECTED_ACCOUNT_ITEM_SYNC_STATE=READY`

`SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBLE=true`

`SELECTED_ACCOUNT_FAIL_CLOSED=false`

`SELECTED_ACCOUNT_FAILURE_REASONS=[]`

`SELECTED_ACCOUNT_CATALOG_ROWS_POST=20`

`SELECTED_ACCOUNT_DUPLICATE_GROUPS_POST=0`

No full account ID, Cookie, Token, phone, nickname, item ID, item title, or customer content was printed.

## COMPANY Adapter State

`COMPANY_PROXY_PATH=D:/TikTok_Auto/devspace_proxy/proxy.cjs`

`COMPANY_PROXY_SHA256=4013CF505BA036FFF11F0382761F14BE7711E8280DDD41097C285DC8D7FDE041`

`COMPANY_ITEM_SYNC_THIN_ADAPTER_UNCHANGED=true`

`COMPANY_ITEM_SYNC_BACKEND_PATH=/api/v1/items/get-all-from-account?no_auth_recovery=true`

`COMPANY_ITEM_SYNC_OPERATION_FIELD_PASSTHROUGH=false`

Backend logs can recover a future invocation identity and terminal durable-readback outcome through `CHG0030_ITEM_SYNC_OPERATION_ACCEPTED` and `CHG0030_ITEM_SYNC_TERMINAL_READBACK` even if the current COMPANY adapter strips extension response fields.

## Side-Effect Counters

`ITEM_SYNC_INVOCATION_COUNT=0`

`ITEM_SYNC_ACCEPTED_MARKERS_10M=0`

`ITEM_SYNC_TERMINAL_MARKERS_10M=0`

`GET_ALL_FROM_ACCOUNT_LOG_LINES_10M=0`

`PUBLISH_LOGS_10M=0`

`AUTO_REPLY_MESSAGE_LOGS_10M=0`

`ACCOUNT_LOGIN_LOGS_10M=0`

`RISK_CONTROL_LOGS_10M=0`

`REAL_PRODUCTS_PUBLISHED=0`

`REAL_PRODUCTS_MODIFIED=0`

`REAL_MESSAGES_SENT=0`

`QR_LOGIN_INVOCATION_COUNT=0`

`MANUAL_RECONNECT_INVOCATION_COUNT=0`

`BROWSER_INVOCATION_COUNT=0`

`PLAYWRIGHT_CDP_INVOCATION_COUNT=0`

## Gate State

`DEPLOYMENT_HEALTH=PASS`

`SELECTED_ACCOUNT_PREFLIGHT=PASS`

`TRACE_IDENTITY_CONTRACT_DEPLOYED=PASS`

`ITEM_SYNC_CANARY_AUTHORIZED=false`

`PRODUCTION_ITEM_SYNC_CANARY_GO=false`

The deployment and read-only preflight gates are now satisfied for masked account `22*********60`. The one Item Sync canary remains blocked until a later explicit commander GO.
