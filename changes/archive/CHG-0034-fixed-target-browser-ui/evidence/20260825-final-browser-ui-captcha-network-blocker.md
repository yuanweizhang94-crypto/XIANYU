# CHG-0034 Browser/UI CAPTCHA Network Checkpoint (Superseded)

Change ID: CHG-0034-fixed-target-browser-ui
Status: ARCHIVED

## Result

`CHECKPOINT_DATE=2026-08-25`

`CHECKPOINT_SUPERSEDED=true`

`SUPERSEDED_BY=20260826-authenticated-browser-ui-acceptance.md`

`FIXED_TARGET_BROWSER_UI_ACCEPTANCE=HUMAN_BLOCKED_EXTERNAL_CAPTCHA_NETWORK`

`FINAL_CHECKPOINT=HUMAN_BLOCKED_EXTERNAL_CAPTCHA_NETWORK`

`NO_BUSINESS_CODE_DEFECT_PROVEN=true`

`BUSINESS_RUNTIME_PATCHES=0`

`SECOND_OWNER_CREATED=false`

At this chronological checkpoint, the fixed-target Browser/UI acceptance reached the upstream-native login page and then failed closed at the third-party Geetest slider. The observed blocker was external human/CAPTCHA/network state, not a proven XIANYU business-code defect and not a credential failure. It is not the final CHG-0034 conclusion; the authenticated 2026-08-26 checkpoint supersedes it.

## Fixed Target And Runtime

`FIXED_TARGET_URL=http://127.0.0.1:19000/`

`FRESH_DOCUMENT_LOADED=true`

`LOGIN_PAGE_NONBLANK=true`

`DOCUMENT_TITLE=闲鱼自动回复管理系统`

`ROOT_HEAD_STATUS=200`

`SAME_ORIGIN_HEALTH_URL=http://127.0.0.1:19000/health`

`SAME_ORIGIN_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_URL=http://127.0.0.1:28090/health`

`DIRECT_WEBSOCKET_HEALTH_STATUS=200`

`DIRECT_WEBSOCKET_HEALTH_DATABASE=connected`

`API_V1_HEALTH_STATUS=404`

`API_V1_HEALTH_404_EXPECTED_BECAUSE_CANONICAL_PATH_IS_HEALTH=true`

`FRONTEND_IMAGE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2`

`BACKEND_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2`

`WEBSOCKET_IMAGE=xianyu-chg0023-websocket:readiness-contract-20260822-r1`

`RUNTIME_MAIN_BUNDLE=assets/index-Bo8JNRra.js`

`RUNTIME_MAIN_BUNDLE_SHA256=86f8d7b597ceafdcc20a36f59a4834a2f2932d05fa054a98410f9c529e714d6f`

`RUNTIME_CSS_BUNDLE=assets/index-DSbQtSxR.css`

`RUNTIME_CSS_SHA256=ce943d8848b339c7c2ae380a2d7f50ff3ad25dd53581421c4d8a9464699124f3`

## Console

`CONSOLE_ERROR_WARN_COUNT_BEFORE_CAPTCHA=0`

`CONSOLE_ERROR_WARN_COUNT_AFTER_GEETEST_TIMEOUT=1`

`POST_THIRD_PARTY_CAPTCHA_EMPTY_CONSOLE_ERROR=true`

`POST_CAPTCHA_CONSOLE_APP_STACK_ATTRIBUTED=false`

The sole post-timeout console entry had an empty message and no attributable application stack or text. It is classified as a post-third-party-captcha empty console error, not proof of an application defect.

## Login And Geetest

`DEMO_ADMIN_CREDENTIAL_FILLED_THROUGH_UI=true`

`CREDENTIAL_VALUES_RECORDED=false`

`FALLBACK_PASSWORD_SUBMITTED=false`

`FALLBACK_PASSWORD_VALIDATED=false`

`CREDENTIAL_FAILURE_CLASSIFICATION=false`

`GEETEST_SLIDER_BLOCKED_LOGIN=true`

`USER_AUTHORIZED_ONE_CAPTCHA_CHALLENGE=true`

`SAME_CHALLENGE_ID_USED=true`

`FULL_CHALLENGE_ID_RECORDED=false`

`CHALLENGE_URLS_RECORDED=false`

`TWO_CALIBRATED_INCORRECT_DRAGS=true`

`ONE_FINAL_PRECISE_DRAG=true`

`GEETEST_VISIBLE_TEXT=网络不给力 / 请点击此处重试 / 加载失败，点击重试`

After the final precise drag, Geetest displayed a network/loader failure state. No authenticated session was created.

## Negative Action Evidence

`AUTHENTICATED_SESSION_CREATED=false`

`AUTHENTICATED_PAGES_ENTERED=0`

`DASHBOARD_VISITED=false`

`ACCOUNTS_PAGE_VISITED=false`

`ITEMS_PAGE_VISITED=false`

`CHAT_PAGE_VISITED=false`

`AUTO_REPLY_PAGE_VISITED=false`

`SERVICE_PAGE_VISITED=false`

`CAPTCHA_BYPASS_ATTEMPTS=0`

`CAPTCHA_REFRESH_ATTEMPTS=0`

`API_LOGIN_BYPASS_ATTEMPTS=0`

`PUBLISH_INVOCATIONS=0`

`ITEM_MUTATION_COUNT=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_ENABLEMENT_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`QR_INVOCATIONS=0`

`RECONNECT_INVOCATIONS=0`

`ORDER_ACTION_INVOCATIONS=0`

`PURCHASE_ACTION_INVOCATIONS=0`

`PLATFORM_BROWSER_ACTIONS_AFTER_CAPTCHA_BLOCK=0`

## Local Diagnostic Visual

`LOCAL_DIAGNOSTIC_SCREENSHOT_PATH=C:/Users/HUAWEI/.codex/visualizations/2026/08/25/01a03686-49c0-7c30-ac13-7b2c10b1541f/phase4-geetest-network-timeout.png`

`LOCAL_DIAGNOSTIC_SCREENSHOT_COMMITTED=false`

`FULL_LOGIN_SCREENSHOT_REFERENCED=false`

Only the sanitized local crop path is recorded. No binary screenshot is committed or copied into the repository, and the full login screenshot is not referenced because it contains login form/demo data.

## Pre-Existing Unrelated Debts

`CHG0020_MISSING_DESIGN_TASKS_PRE_EXISTING=true`

`CHG0022_STALE_ACTIVE_PATHS_PRE_EXISTING=true`

`README_AGENTS_DRIFT_PRE_EXISTING=true`

These debts are unrelated to CHG-0034 and are not absorbed by this closure.
