# CHG-0034 Acceptance

Change ID: CHG-0034-fixed-target-browser-ui
Status: ARCHIVED

## Required Readiness Acceptance

- CHG-0034 is the only active Change in the isolated worktree.
- The Change records the three-line execution contract:
  - User outcome: authorized Browser reliably loads and visually validates the fixed local XIANYU frontend at `http://127.0.0.1:19000/` across the required pages without platform actions or secret exposure.
  - Confirmed blocker: prior browser remained in stale SPA context; fresh document load, auth handoff, same-origin API/WebSocket and visible page state must be proven, and any XIANYU/COMPANY source drift must be classified.
  - Smallest success test: fixed target HTTP 200, nonblank fresh bundle, no fatal console errors, authorized API/WS visible, required account/item/chat/AI/service pages render with masked screenshots.
- No Browser, Chrome, platform action, QR/reconnect, sync, publish, send, AI enablement, account mutation, deployment, commit, or push occurs in the read-only prep phase.
- No Cookie, Token, JWT, Authorization value, API key, password, browser Profile secret, customer content, full account ID, or unmasked screenshot is printed or persisted.
- The readiness checkpoint reports whether a pre-browser blocker exists before commander action.

## Fixed Target

`FIXED_TARGET_URL=http://127.0.0.1:19000/`

## Expected Commander Pages

- `/`
- `/accounts`
- `/items`
- `/chat`
- `/ai-reply`
- `/service`

## Current Gate State

`COMMANDER_OWNS_BROWSER_ACTION=true`

`BROWSER_INVOCATIONS=0`

`PLATFORM_ACTION_INVOCATIONS=0`

`QR_INVOCATIONS=0`

`RECONNECT_INVOCATIONS=0`

`SYNC_INVOCATIONS=0`

`PUBLISH_INVOCATIONS=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_ENABLEMENT_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

`SECRET_VALUE_PRINTED=false`

`UNMASKED_SCREENSHOT_PERSISTED=false`

## GO/NO-GO Rule

If HTTP 200, fresh nonblank runtime bundle, same-origin authorized API/WebSocket visibility, and source-vs-runtime drift classification are not proven, the commander Browser action remains blocked.

## Readiness Checkpoint

`READINESS_CHECKPOINT=READY_FOR_COMMANDER_BROWSER_WITH_SOURCE_AUTHORITY_CAVEAT`

`FIXED_TARGET_URL=http://127.0.0.1:19000/`

`FIXED_TARGET_HEAD_STATUS=200`

`FIXED_TARGET_CACHE_CONTROL=no-store, must-revalidate, no-cache`

`FIXED_TARGET_HTML_SHA256=541e4051d48be50d7a7a94d01264cb80cc34d6d0c199958ec0019a44a80c499b`

`SAME_ORIGIN_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_STATUS=200`

`RUNTIME_MAIN_BUNDLE_SHA256=86f8d7b597ceafdcc20a36f59a4834a2f2932d05fa054a98410f9c529e714d6f`

`RUNTIME_ACCOUNTS_CHG0026_SHA256=0bf903f8e1fb09dcd48b79ab38901433a789095c937962d099616584cf47651a`

`RUNTIME_CHATNEW_CHG0026_SHA256=36716e3d273da8c71dc321784f0e8381eeecbe4fd4b098fceb612c1b699d876d`

`AUTH_SYNC_PATH=/internal/xianyu-auth-sync`

`AUTH_SYNC_ORIGIN_DEFAULT=http://127.0.0.1:19000`

`SOURCE_RUNTIME_DRIFT_CLASSIFICATION=RUNTIME_IMAGES_SPAN_CHG0018_FRONTEND_CHG0030_BACKEND_CHG0023_WEBSOCKET_WITH_CHG0026_NAMED_FRONTEND_CHUNKS_SOURCE_AUTHORITY_UNRESOLVED`

`PRE_BROWSER_CODE_PATCH_NEEDED=false`

`PRE_BROWSER_DEPLOY_NEEDED=false`

`PRE_BROWSER_BLOCKER=NONE_FOR_COMMANDER_BROWSER_READINESS_WITH_SOURCE_AUTHORITY_CAVEAT`

## Final Controlled Browser/UI Acceptance

`FIXED_TARGET_BROWSER_UI_ACCEPTANCE=PASS_WITH_NONFATAL_CHART_WARNINGS`

`FINAL_CHECKPOINT=PASS_WITH_NONFATAL_CHART_WARNINGS`

`ACCEPTANCE_DATE=2026-08-26`

`FIXED_TARGET_URL=http://127.0.0.1:19000/`

`FRESH_DOCUMENT_LOADED=true`

`LOGIN_PAGE_NONBLANK=true`

`DOCUMENT_TITLE=闲鱼自动回复管理系统`

`USER_AUTHENTICATED_SESSION_AVAILABLE=true`

`AGENT_CREATED_AUTHENTICATED_SESSION=false`

### Chronological Login And CAPTCHA Evidence

`CONSOLE_ERROR_WARN_COUNT_BEFORE_CAPTCHA=0`

`CONSOLE_ERROR_WARN_COUNT_AFTER_GEETEST_TIMEOUT=1`

`POST_THIRD_PARTY_CAPTCHA_EMPTY_CONSOLE_ERROR=true`

`POST_CAPTCHA_CONSOLE_APP_STACK_ATTRIBUTED=false`

`CAPTCHA_NETWORK_BLOCKER_CHECKPOINT_SUPERSEDED=true`

`DEMO_ADMIN_CREDENTIAL_FILLED_THROUGH_UI=true`

`CREDENTIAL_VALUES_RECORDED=false`

`FALLBACK_PASSWORD_SUBMITTED=false`

`FALLBACK_PASSWORD_VALIDATED=false`

`CREDENTIAL_FAILURE_CLASSIFICATION=false`

`GEETEST_SLIDER_BLOCKED_LOGIN_AT_20260825_CHECKPOINT=true`

`USER_AUTHORIZED_ONE_CAPTCHA_CHALLENGE=true`

`SAME_CHALLENGE_ID_USED=true`

`FULL_CHALLENGE_ID_RECORDED=false`

`CHALLENGE_URLS_RECORDED=false`

`TWO_CALIBRATED_INCORRECT_DRAGS=true`

`ONE_FINAL_PRECISE_DRAG=true`

`GEETEST_VISIBLE_TEXT=网络不给力 / 请点击此处重试 / 加载失败，点击重试`

`CAPTCHA_BYPASS_ATTEMPTS=0`

`CAPTCHA_REFRESH_ATTEMPTS=0`

`API_LOGIN_BYPASS_ATTEMPTS=0`

The CAPTCHA/network event is retained only as chronological evidence. The user later made an authenticated session available in the existing Browser tab; the agent did not create or bypass authentication.

### Authenticated Read-Only Page Evidence

`AUTHENTICATED_PAGES_ENTERED=8`

`DASHBOARD_PATH=/dashboard`

`DASHBOARD_VISITED=true`

`DASHBOARD_NONBLANK=true`

`DASHBOARD_ACCOUNT_COUNT=12`

`DASHBOARD_ENABLED_ACCOUNT_COUNT=9`

`DASHBOARD_ONLINE_ACCOUNT_COUNT=9`

`DASHBOARD_TODAY_REPLY_COUNT=0`

`ACCOUNTS_PATH=/accounts`

`ACCOUNTS_PAGE_VISITED=true`

`ACCOUNTS_PAGE_NONBLANK=true`

`ACCOUNTS_ROW_COUNT=12`

`ACCOUNTS_CONSOLE_ERROR_COUNT=0`

`SELECTED_ACCOUNT_MASKED_ID=280***247`

`SELECTED_ACCOUNT_MASKED_LABEL=艺龙8.19可用`

`SELECTED_ACCOUNT_FOUND=true`

`SELECTED_ACCOUNT_ENABLED=true`

`SELECTED_ACCOUNT_ONLINE=true`

`SELECTED_ACCOUNT_CHAT_AVAILABLE=true`

`SELECTED_ACCOUNT_PUBLISH_CAPABILITY=按需检查`

`SELECTED_ACCOUNT_AI_REPLY_CLOSED=true`

`SELECTED_ACCOUNT_DETAIL_VISITED_READ_ONLY=true`

`SELECTED_ACCOUNT_DETAIL_EXPECTED_FIELDS_PRESENT=true`

`SELECTED_ACCOUNT_DETAIL_CANCEL_USED=true`

`SELECTED_ACCOUNT_DETAIL_SAVE_INVOCATIONS=0`

`SELECTED_ACCOUNT_DETAIL_VALUES_RECORDED=false`

`ITEMS_PATH=/items`

`ITEMS_PAGE_VISITED=true`

`ITEMS_PAGE_NONBLANK=true`

`ITEMS_TOTAL_COUNT=39`

`ITEMS_CURRENT_PAGE_ROW_COUNT=20`

`ITEMS_LOADING_OR_ERROR_VISIBLE=false`

`ITEM_TITLES_OR_IDS_RECORDED=false`

`PUBLISH_LOGS_PATH=/product-publish/logs`

`PUBLISH_LOGS_PAGE_VISITED=true`

`PUBLISH_LOGS_PAGE_NONBLANK=true`

`PUBLISH_LOGS_TOTAL_COUNT=339`

`PUBLISH_LOGS_CURRENT_PAGE_ROW_COUNT=20`

`PUBLISH_LOGS_LOADING_OR_ERROR_VISIBLE=false`

`PUBLISH_LOG_TITLES_ACCOUNT_CUSTOMER_DATA_RECORDED=false`

`ONLINE_CHAT_PATH=/online-chat-new`

`ONLINE_CHAT_PAGE_VISITED=true`

`ONLINE_CHAT_PAGE_NONBLANK=true`

`ONLINE_CHAT_LABELS_VISIBLE=在线聊天 / 会话列表`

`ONLINE_CHAT_SEND_INPUT_PRESENT=true`

`ONLINE_CHAT_QUICK_PHRASE_INPUT_PRESENT=true`

`ONLINE_CHAT_CONNECTED_SIGNAL_COUNT=6`

`ONLINE_CHAT_DISCONNECTED_SIGNAL_COUNT=2`

`CUSTOMER_MESSAGE_CONTENT_RECORDED=false`

`AUTO_REPLY_PATH=/keywords`

`AUTO_REPLY_PAGE_VISITED=true`

`AUTO_REPLY_PAGE_NONBLANK=true`

`AUTO_REPLY_RULE_ROW_COUNT=2`

`AUTO_REPLY_LOADING_OR_ERROR_VISIBLE=false`

`PRIMARY_AI_REPLY_TOGGLE_COUNT=12`

`PRIMARY_AI_REPLY_ENABLED_COUNT=0`

`PRIMARY_AI_REPLY_ALL_CLOSED=true`

`PRIMARY_AI_REPLY_TOGGLE_CLICKS=0`

`SCHEDULED_TASKS_SERVICE_STATUS_PATH=/admin/scheduled-tasks`

`SCHEDULED_TASKS_SERVICE_STATUS_PAGE_VISITED=true`

`SCHEDULED_TASKS_SERVICE_STATUS_PAGE_NONBLANK=true`

`SCHEDULED_TASKS_ROW_COUNT=21`

`SCHEDULED_TASKS_LOADING_OR_ERROR_VISIBLE=false`

### Health And Console Classification

`ROOT_HEAD_STATUS=200`

`SAME_ORIGIN_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_DATABASE=connected`

`API_V1_HEALTH_STATUS=404`

`API_V1_HEALTH_404_EXPECTED_BECAUSE_CANONICAL_PATH_IS_HEALTH=true`

`RAW_BROWSER_HEALTH_NAVIGATION_CLIENT_BLOCKED=true`

`RAW_BROWSER_HEALTH_NAVIGATION_LEFT_SPA_UNCHANGED=true`

`RAW_BROWSER_HEALTH_NAVIGATION_BACKEND_FAILURE=false`

`FINAL_DASHBOARD_NONFATAL_CHART_WARNING_COUNT=2`

`FINAL_DASHBOARD_CHART_WARNING_DIMENSIONS=-1`

`FINAL_FATAL_CONSOLE_ERROR_COUNT=0`

### Runtime Identity

`FRONTEND_IMAGE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2`

`BACKEND_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2`

`WEBSOCKET_IMAGE=xianyu-chg0023-websocket:readiness-contract-20260822-r1`

`RUNTIME_MAIN_BUNDLE=assets/index-Bo8JNRra.js`

`RUNTIME_MAIN_BUNDLE_SHA256=86f8d7b597ceafdcc20a36f59a4834a2f2932d05fa054a98410f9c529e714d6f`

`RUNTIME_CSS_BUNDLE=assets/index-DSbQtSxR.css`

`RUNTIME_CSS_SHA256=ce943d8848b339c7c2ae380a2d7f50ff3ad25dd53581421c4d8a9464699124f3`

### Negative Action And Data Evidence

`PUBLISH_INVOCATIONS=0`

`ITEM_MUTATION_COUNT=0`

`ITEM_SYNC_INVOCATIONS=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_ENABLEMENT_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`QR_INVOCATIONS=0`

`RECONNECT_INVOCATIONS=0`

`ORDER_ACTION_INVOCATIONS=0`

`PURCHASE_ACTION_INVOCATIONS=0`

`DEPLOY_INVOCATIONS=0`

`PLATFORM_WRITE_ACTIONS=0`

`NO_BUSINESS_CODE_DEFECT_PROVEN=true`

`BUSINESS_RUNTIME_PATCHES=0`

`SECOND_OWNER_CREATED=false`

`SECRETS_RECORDED=false`

`FULL_ACCOUNT_IDS_RECORDED=false`

`CUSTOMER_MESSAGES_RECORDED=false`

### Local Diagnostic Visuals

`LOCAL_AUTHENTICATED_SCREENSHOT_PATH=C:/Users/HUAWEI/.codex/visualizations/2026/08/25/01a03686-49c0-7c30-ac13-7b2c10b1541f/phase4-dashboard-authenticated.png`

`LOCAL_CAPTCHA_SCREENSHOT_PATH=C:/Users/HUAWEI/.codex/visualizations/2026/08/25/01a03686-49c0-7c30-ac13-7b2c10b1541f/phase4-geetest-network-timeout.png`

`LOCAL_DIAGNOSTIC_SCREENSHOT_COMMITTED=false`

`FULL_LOGIN_SCREENSHOT_REFERENCED=false`

## Pre-Existing Unrelated Global Debts

Known global debts remain outside CHG-0034 scope: CHG-0020 archived record missing design/tasks, CHG-0022 stale active-path references, and README/AGENTS drift. They must not be treated as CHG-0034 defects or absorbed into this closure.

## Upstream Capability Audit

Same as proposal.

## Pinned Upstream Evidence

Same as proposal.

## Existing Local Implementation Search

Same as proposal.

## Reuse Decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate Implementation Risk

No duplicate UI/API/WS/auth/Browser/runtime path is accepted.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the workflow but not this local Browser-freshness readiness checkpoint.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing deployed XIANYU frontend/backend/WebSocket/auth owners.

## Retirement Plan For Overlapping Local Code

No overlapping local code is introduced.
