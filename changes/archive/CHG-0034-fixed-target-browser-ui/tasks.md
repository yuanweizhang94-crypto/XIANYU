# CHG-0034 Tasks

Change ID: CHG-0034-fixed-target-browser-ui
Status: ARCHIVED

- [x] T1 Verify latest remote main equals `41b3a527a06d85d77d46bccba2780ff080504936`, create the isolated CHG-0034 worktree/branch, and prove the branch is clean before Change creation.
- [x] T2 Run `python scripts/project_context.py` before development and confirm no prior executable active Change exists on this baseline.
- [x] T3 Create the active CHG-0034 governance record with the required three-line execution contract and zero-action gates.
- [x] T4 Regenerate `generated/PROJECT_STATE.json` with `python scripts/generate_state.py` and verify active state, file existence, and dirty `git status --short`.
- [x] T5 Inspect exact prior CHG-0033 closure evidence and confirm CHG-0034 is the legal next active Change.
- [x] T6 Inspect current frontend/backend/WebSocket runtime images, fixed URL HTTP status, document freshness headers, bundle names, and runtime asset hashes without Browser.
- [x] T7 Inspect source frontend/backend/WebSocket owners, source bundle/build hashes, nginx/API/WS/auth-sync contracts, and deterministic build/test commands from gathered evidence.
- [x] T8 Classify source-vs-runtime drift and determine whether current deployed assets already contain the fixes or whether a code/deployment patch is needed.
- [x] T9 If COMPANY changes may be needed, locate candidate source repo/root/remote and dirty fingerprints without modifying it or the installed proxy.
- [x] T10 Return the readiness checkpoint with shared-worktree file proof, fixed URL, expected routes/pages, source-vs-runtime hashes, minimal Browser steps for commander, and any pre-browser blocker.
- [x] T11 Record the chronological `HUMAN_BLOCKED_EXTERNAL_CAPTCHA_NETWORK` checkpoint with sanitized Geetest/network evidence, zero credential/challenge persistence, and zero business mutations.
- [x] T12 Record the user-available authenticated-session checkpoint and complete read-only validation of all required Browser/UI pages without creating a session or executing a business/platform write.
- [x] T13 Close the final acceptance as `PASS_WITH_NONFATAL_CHART_WARNINGS`, preserving the CAPTCHA event only as superseded chronology.
- [x] T14 Archive CHG-0034, regenerate project state with no active Change, add deterministic closure tests, and run scoped repository gates while classifying unrelated global debts as pre-existing.

## Readiness Checkpoint

`REMOTE_MAIN_VERIFIED=41b3a527a06d85d77d46bccba2780ff080504936`

`WORKTREE_PATH=D:/xianyu-worktrees/CHG-0034-fixed-target-browser-ui`

`BRANCH=feat/CHG-0034-fixed-target-browser-ui`

`PROJECT_CONTEXT_ACTIVE_CHANGE=CHG-0034-fixed-target-browser-ui`

`PROJECT_STATE_ACTIVE_CHANGE=CHG-0034-fixed-target-browser-ui`

`CHG0033_ARCHIVED_ON_BASELINE=true`

`FIXED_TARGET_URL=http://127.0.0.1:19000/`

`FIXED_TARGET_TCP_19000=true`

`FIXED_TARGET_HEAD_STATUS=200`

`FIXED_TARGET_SERVER=nginx/1.31.3`

`FIXED_TARGET_CACHE_CONTROL=no-store, must-revalidate, no-cache`

`FIXED_TARGET_PRAGMA=no-cache`

`FIXED_TARGET_HTML_LENGTH=1338`

`FIXED_TARGET_HTML_SHA256=541e4051d48be50d7a7a94d01264cb80cc34d6d0c199958ec0019a44a80c499b`

`FRONTEND_CONTAINER=xianyu_chg0017_frontend`

`FRONTEND_IMAGE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2`

`FRONTEND_IMAGE_ID=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416`

`BACKEND_CONTAINER=xianyu_chg0017_backend_web`

`BACKEND_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2`

`BACKEND_IMAGE_ID=sha256:f877b7273b2f4e23ff5f0dd5e599dbf860c1e83bc801fca8a26bea815cae4573`

`WEBSOCKET_CONTAINER=xianyu_chg0017_websocket`

`WEBSOCKET_IMAGE=xianyu-chg0023-websocket:readiness-contract-20260822-r1`

`WEBSOCKET_IMAGE_ID=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256`

`SAME_ORIGIN_HEALTH_URL=http://127.0.0.1:19000/health`

`SAME_ORIGIN_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_URL=http://127.0.0.1:28090/health`

`DIRECT_WEBSOCKET_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_DATABASE=connected`

`API_V1_HEALTH_ON_19000_STATUS=404`

`API_V1_HEALTH_ON_28089_STATUS=404`

`RUNTIME_MAIN_BUNDLE_SHA256=86f8d7b597ceafdcc20a36f59a4834a2f2932d05fa054a98410f9c529e714d6f`

`RUNTIME_CSS_SHA256=ce943d8848b339c7c2ae380a2d7f50ff3ad25dd53581421c4d8a9464699124f3`

`RUNTIME_ACCOUNTS_CHG0026_SHA256=0bf903f8e1fb09dcd48b79ab38901433a789095c937962d099616584cf47651a`

`RUNTIME_CHATNEW_CHG0026_SHA256=36716e3d273da8c71dc321784f0e8381eeecbe4fd4b098fceb612c1b699d876d`

`RUNTIME_ORDERS_ALL_SYNC_R2_SHA256=48f566cfa244cee3a7290b5f42e483b6cab70f1d5ce5ac423e6592fa652d6680`

`RUNTIME_BUNDLE_CONTAINS_API_V1=true`

`RUNTIME_CHAT_CHUNK_CONTAINS_WS=true`

`RUNTIME_CHAT_CHUNK_CONTAINS_CHAT_NEW=true`

`AUTH_SYNC_PATH=/internal/xianyu-auth-sync`

`AUTH_SYNC_ORIGIN_DEFAULT=http://127.0.0.1:19000`

`AUTH_SYNC_SECRET_VALUES_RECORDED=false`

`COMPANY_TOOL_ROOT=D:/COMPANY_LOCAL_EXECUTION_TOOL`

`COMPANY_TOOL_GIT_READ_BLOCKED_BY_DUBIOUS_OWNERSHIP=true`

`COMPANY_TOOL_RUNTIME_PROXY_PRESENT=true`

`CANDIDATE_SOURCE_ROOTS=D:/xianyu-chg0026-source;D:/xianyu-spa-cache-verify;D:/xianyu-upstream-latest-audit;D:/xianyu-upstream-pilot;D:/xianyu-chg0025-source`

`CLEAN_SOURCE_AUTHORITY_CONFIRMED=false`

`SOURCE_RUNTIME_DRIFT_CLASSIFICATION=RUNTIME_IMAGES_SPAN_CHG0018_FRONTEND_CHG0030_BACKEND_CHG0023_WEBSOCKET_WITH_CHG0026_NAMED_FRONTEND_CHUNKS_SOURCE_AUTHORITY_UNRESOLVED`

`PRE_BROWSER_CODE_PATCH_NEEDED=false`

`PRE_BROWSER_DEPLOY_NEEDED=false`

`PRE_BROWSER_BLOCKER=NONE_FOR_COMMANDER_BROWSER_READINESS_WITH_SOURCE_AUTHORITY_CAVEAT`

`BROWSER_INVOCATIONS=0`

`PLATFORM_ACTION_INVOCATIONS=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

`SECRET_VALUES_WRITTEN_TO_CHANGE_FILES=false`

## Final Browser/UI Acceptance

`FIXED_TARGET_BROWSER_UI_ACCEPTANCE=PASS_WITH_NONFATAL_CHART_WARNINGS`

`FINAL_CHECKPOINT=PASS_WITH_NONFATAL_CHART_WARNINGS`

`NO_BUSINESS_CODE_DEFECT_PROVEN=true`

`BUSINESS_RUNTIME_PATCHES=0`

`CAPTCHA_BYPASS_ATTEMPTS=0`

`SECOND_OWNER_CREATED=false`

`USER_AUTHENTICATED_SESSION_AVAILABLE=true`

`AGENT_CREATED_AUTHENTICATED_SESSION=false`

`AUTHENTICATED_PAGES_ENTERED=8`

`DASHBOARD_VISITED=true`

`ACCOUNTS_PAGE_VISITED=true`

`SELECTED_ACCOUNT_DETAIL_VISITED_READ_ONLY=true`

`ITEMS_PAGE_VISITED=true`

`PUBLISH_LOGS_PAGE_VISITED=true`

`ONLINE_CHAT_PAGE_VISITED=true`

`AUTO_REPLY_PAGE_VISITED=true`

`SCHEDULED_TASKS_SERVICE_STATUS_PAGE_VISITED=true`

`FINAL_DASHBOARD_NONFATAL_CHART_WARNING_COUNT=2`

`FINAL_FATAL_CONSOLE_ERROR_COUNT=0`

`PUBLISH_INVOCATIONS=0`

`ITEM_MUTATION_COUNT=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_ENABLEMENT_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`QR_INVOCATIONS=0`

`RECONNECT_INVOCATIONS=0`

`ORDER_ACTION_INVOCATIONS=0`

`PURCHASE_ACTION_INVOCATIONS=0`

`PLATFORM_WRITE_ACTIONS=0`

`FULL_CHALLENGE_ID_RECORDED=false`

`CREDENTIAL_VALUES_RECORDED=false`

`FALLBACK_PASSWORD_SUBMITTED=false`

`CREDENTIAL_FAILURE_CLASSIFICATION=false`

`LOCAL_AUTHENTICATED_SCREENSHOT_PATH=C:/Users/HUAWEI/.codex/visualizations/2026/08/25/01a03686-49c0-7c30-ac13-7b2c10b1541f/phase4-dashboard-authenticated.png`

`LOCAL_CAPTCHA_SCREENSHOT_PATH=C:/Users/HUAWEI/.codex/visualizations/2026/08/25/01a03686-49c0-7c30-ac13-7b2c10b1541f/phase4-geetest-network-timeout.png`

`LOCAL_DIAGNOSTIC_SCREENSHOT_COMMITTED=false`

## Pre-Existing Unrelated Global Debts

The following known repository debts are classified as pre-existing and unrelated to CHG-0034: CHG-0020 archived record missing design/tasks, CHG-0022 stale active-path references, and README/AGENTS drift. CHG-0034 does not absorb or repair them.

## Upstream Capability Audit

Runtime and source owner paths will be searched during T5 through T8.

## Pinned Upstream Evidence

Pinned baseline: `origin/main` at `41b3a527a06d85d77d46bccba2780ff080504936`.

## Existing Local Implementation Search

Archived CHG-0030 through CHG-0033 and local runtime/source contracts will be searched narrowly.

## Reuse Decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate Implementation Risk

No duplicate UI/API/WS/auth/Browser/runtime owner is planned.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the workflow but not this local Browser-freshness readiness checkpoint.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing deployed XIANYU frontend/backend/WebSocket/auth owners.

## Retirement Plan For Overlapping Local Code

No overlapping production code is added.
