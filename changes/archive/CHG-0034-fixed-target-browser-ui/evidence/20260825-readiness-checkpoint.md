# CHG-0034 Readiness Checkpoint

Change ID: CHG-0034-fixed-target-browser-ui
Status: ARCHIVED

## Shared Worktree Proof

`WORKTREE_PATH=D:/xianyu-worktrees/CHG-0034-fixed-target-browser-ui`

`BRANCH=feat/CHG-0034-fixed-target-browser-ui`

`REMOTE_MAIN_VERIFIED=41b3a527a06d85d77d46bccba2780ff080504936`

`BASELINE_CONTAINS_CHG0033_CLOSURE=true`

`PROJECT_CONTEXT_ACTIVE_CHANGE=CHG-0034-fixed-target-browser-ui`

`PROJECT_STATE_ACTIVE_CHANGE=CHG-0034-fixed-target-browser-ui`

## Fixed Target Runtime

`FIXED_TARGET_URL=http://127.0.0.1:19000/`

`FIXED_TARGET_TCP_19000=true`

`FIXED_TARGET_HEAD_STATUS=200`

`FIXED_TARGET_SERVER=nginx/1.31.3`

`FIXED_TARGET_CACHE_CONTROL=no-store, must-revalidate, no-cache`

`FIXED_TARGET_PRAGMA=no-cache`

`FIXED_TARGET_HTML_LENGTH=1338`

`FIXED_TARGET_HTML_SHA256=541e4051d48be50d7a7a94d01264cb80cc34d6d0c199958ec0019a44a80c499b`

## Runtime Images

`FRONTEND_CONTAINER=xianyu_chg0017_frontend`

`FRONTEND_IMAGE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2`

`FRONTEND_IMAGE_ID=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416`

`BACKEND_CONTAINER=xianyu_chg0017_backend_web`

`BACKEND_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2`

`BACKEND_IMAGE_ID=sha256:f877b7273b2f4e23ff5f0dd5e599dbf860c1e83bc801fca8a26bea815cae4573`

`WEBSOCKET_CONTAINER=xianyu_chg0017_websocket`

`WEBSOCKET_IMAGE=xianyu-chg0023-websocket:readiness-contract-20260822-r1`

`WEBSOCKET_IMAGE_ID=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256`

## Runtime Assets

`assets/Orders-CVzISxMo.js=25a999dd4e2e7aed2bc7a308eb933bb111d2a1991cbc5776278a62569fc89a09`

`assets/Orders-CVzISxMo-all-sync-r2.js=48f566cfa244cee3a7290b5f42e483b6cab70f1d5ce5ac423e6592fa652d6680`

`assets/Accounts-BoMMlrdD.js=61ff4db1d7dd40f2b15c6e940c317502e8c04f993f2e142ffe01551968a6e681`

`assets/Accounts-CHG0026-0bf903f8e1fb.js=0bf903f8e1fb09dcd48b79ab38901433a789095c937962d099616584cf47651a`

`assets/ChatNew-D15A1Lkf.js=64c5f7c367775bd8c6209e4d575c4523937cbfd7e227473ee09019595c32b231`

`assets/ChatNew-CHG0026-36716e3d273d.js=36716e3d273da8c71dc321784f0e8381eeecbe4fd4b098fceb612c1b699d876d`

`assets/index-Bo8JNRra.js=86f8d7b597ceafdcc20a36f59a4834a2f2932d05fa054a98410f9c529e714d6f`

`assets/index-DSbQtSxR.css=ce943d8848b339c7c2ae380a2d7f50ff3ad25dd53581421c4d8a9464699124f3`

## API, WebSocket, And Auth-Sync

`SAME_ORIGIN_HEALTH_URL=http://127.0.0.1:19000/health`

`SAME_ORIGIN_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_URL=http://127.0.0.1:28090/health`

`DIRECT_WEBSOCKET_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_DATABASE=connected`

`API_V1_HEALTH_ON_19000_STATUS=404`

`API_V1_HEALTH_ON_28089_STATUS=404`

`RUNTIME_BUNDLE_CONTAINS_API_V1=true`

`RUNTIME_CHAT_CHUNK_CONTAINS_WS=true`

`RUNTIME_CHAT_CHUNK_CONTAINS_CHAT_NEW=true`

`AUTH_SYNC_PATH=/internal/xianyu-auth-sync`

`AUTH_SYNC_ORIGIN_DEFAULT=http://127.0.0.1:19000`

`AUTH_SYNC_SECRET_VALUES_RECORDED=false`

## Source And Runtime Drift

`COMPANY_TOOL_ROOT=D:/COMPANY_LOCAL_EXECUTION_TOOL`

`COMPANY_TOOL_GIT_READ_BLOCKED_BY_DUBIOUS_OWNERSHIP=true`

`COMPANY_TOOL_RUNTIME_PROXY_PRESENT=true`

`CANDIDATE_SOURCE_ROOTS=D:/xianyu-chg0026-source;D:/xianyu-spa-cache-verify;D:/xianyu-upstream-latest-audit;D:/xianyu-upstream-pilot;D:/xianyu-chg0025-source`

`CLEAN_SOURCE_AUTHORITY_CONFIRMED=false`

`SOURCE_RUNTIME_DRIFT_CLASSIFICATION=RUNTIME_IMAGES_SPAN_CHG0018_FRONTEND_CHG0030_BACKEND_CHG0023_WEBSOCKET_WITH_CHG0026_NAMED_FRONTEND_CHUNKS_SOURCE_AUTHORITY_UNRESOLVED`

`PRE_BROWSER_CODE_PATCH_NEEDED=false`

`PRE_BROWSER_DEPLOY_NEEDED=false`

`PRE_BROWSER_BLOCKER=NONE_FOR_COMMANDER_BROWSER_READINESS_WITH_SOURCE_AUTHORITY_CAVEAT`

## Commander Browser Steps

1. Fresh-load `http://127.0.0.1:19000/` in the authorized Browser context, bypassing the stale SPA document.
2. Confirm document URL remains under `http://127.0.0.1:19000/` and the loaded HTML/bundles are nonblank.
3. Confirm no fatal console errors during first load.
4. Confirm same-origin health/API visibility and WebSocket visibility without printing tokens or Authorization values.
5. Visit or navigate to the required pages and capture masked screenshots only: `/`, `/accounts`, `/items`, `/chat`, `/ai-reply`, `/service`.
6. Record route labels as visible in Browser; do not click QR, reconnect, sync, publish, send, AI enablement, or account mutation controls.

## Zero-Action Confirmation

`BROWSER_INVOCATIONS=0`

`PLATFORM_ACTION_INVOCATIONS=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

`SECRET_VALUES_WRITTEN_TO_CHANGE_FILES=false`

## Upstream Capability Audit

CHG-0034 remains an operations-readiness wrapper around the existing deployed XIANYU UI/API/WS/auth workflow.

## Pinned Upstream Evidence

Pinned baseline: `origin/main` at `41b3a527a06d85d77d46bccba2780ff080504936`.

## Existing Local Implementation Search

Search was limited to archived CHG-0033 closure facts, current runtime metadata, fixed URL HTTP checks, runtime asset hashes, candidate source roots, and devspace proxy auth-sync metadata.

## Reuse Decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate Implementation Risk

No duplicate implementation is created by this readiness checkpoint.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the runtime workflow but not this local commander-readiness proof.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing deployed XIANYU frontend/backend/WebSocket/auth owners.

## Retirement Plan For Overlapping Local Code

No overlapping local code is added.
