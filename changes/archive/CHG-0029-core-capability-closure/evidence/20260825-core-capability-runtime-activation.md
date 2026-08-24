# CHG-0029 core capability runtime activation evidence - 2026-08-25

Status: ARCHIVED

Change ID: CHG-0029-core-capability-closure

## Bootstrap

```text
CURRENT_MAIN_SHA=4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89
WORKTREE=D:/xianyu-core-capability-closure-20260825
BRANCH=codex/CHG-0029-core-capability-closure
DIRTY_CHG0018_TOUCHED=NO
CHG0028_PR=41
CHG0028_MERGE_COMMIT=4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89
CHG0028_ARCHIVED_IN_THIS_CHANGE=true
CHG0029_ONLY_ACTIVE_CHANGE=true
ZIDONGZHUA_UNIVERSAL_PROTOCOL_URL_RESULT=404_NOT_PUBLICLY_READABLE
```

## Execution contract

```text
User outcome: automatic reply, online chat, and product publish are source-current, runtime-active, health-checked, and truthfully classified by account cohort.
Confirmed blocker: production containers were running older component images; Backend lacked the CHG-0028 selected-account on-demand route in runtime.
Smallest success test: source/patch deterministic tests pass, only affected Backend runtime is activated, health and runtime source hashes prove intended files are loaded, and sanitized read-only probes classify all three capabilities without sends, publish, Item Sync, QR, Browser, CDP, Playwright, or manual reconnect.
```

## Runtime preimage

```text
BACKEND_PREIMAGE_CONTAINER=90a42b082c2e
BACKEND_PREIMAGE_IMAGE=xianyu-chg0027-backend-web:session-transient-classification-20260824-r1
BACKEND_PREIMAGE_IMAGE_ID=sha256:fcada4935126e1b46360a560c76a1449e37f65d1344ae05cf5e37ddeeed6bf3e
BACKEND_PREIMAGE_HEALTH=HTTP_200
BACKEND_PREIMAGE_ROUTE_FILE_EXISTS=false
WEBSOCKET_IMAGE=xianyu-chg0023-websocket:readiness-contract-20260822-r1
WEBSOCKET_IMAGE_ID=sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256
SCHEDULER_IMAGE=xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1
SCHEDULER_IMAGE_ID=sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8
FRONTEND_IMAGE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2
FRONTEND_IMAGE_ID=sha256:71cfebe276e3d5ca84db01cd9ed1e6b70211dedf75cbe1b3da210b19e19da416
```

## Root cause and fix

```text
PUBLISH_ROOT_CAUSE=STALE_RUNTIME
NEW_CODE_REQUIRED=false
RUNTIME_PATCH_SOURCE=Git blob vendor/patches/xianyu-auto-reply/chg0028-selected-account-on-demand-capability.patch
PATCH_SHA256_LF_BLOB=CED451293701C53475E23F9B87DF205AB97AFDD0B3696D35A4D9C8675BC4E490
WORKTREE_CRLF_SHA256=2FAA21FFA8D836ED204BE5038B571FB774BF6EC9EC7ECDA8659CF13C853842F0
DEPLOYMENT_ARTIFACT=LF_GIT_BLOB
```

The Windows checkout has CRLF bytes because `core.autocrlf=true`; the Git blob has the locked CHG-0028 SHA. Deployment used the Git blob/LF bytes, not the checkout representation.

## Candidate build and failed r1 recovery

```text
R1_IMAGE=xianyu-chg0029-backend-web:selected-account-on-demand-20260825-r1
R1_IMAGE_ID=sha256:db208fe72407e51aaa255297ad799630e2a3c913a56b90abe80cbdf0c678871d
R1_FAILURE=ENTRYPOINT_INHERITED_FROM_PATCH_BUILDER
R1_ENTRYPOINT=["sh"]
R1_CMD=["-lc","sleep infinity"]
R1_RUNTIME_FAILURE=restart_loop_exit_2_sh_cannot_open_python
ROLLBACK_AFTER_R1=PASS
ROLLBACK_HEALTH=HTTP_200
```

The failed candidate did not expose a business-code defect. It was a Docker image metadata error caused by committing from a temporary builder container. The old Backend container was preserved and restored before continuing.

## Final Backend deployment

```text
FINAL_BACKEND_IMAGE=xianyu-chg0029-backend-web:selected-account-on-demand-20260825-r2
FINAL_BACKEND_IMAGE_ID=sha256:4663ca89ba9702bc4f53572593f47f7413cd82e77919ee43b619fba63dbfa7f1
FINAL_BACKEND_CONTAINER=da101458a353
FINAL_BACKEND_ENTRYPOINT=null
FINAL_BACKEND_CMD=["python","backend-web/main.py"]
FINAL_BACKEND_RESTART_COUNT=0
FINAL_BACKEND_HEALTH=HTTP_200
ROLLBACK_CONTAINER=xianyu_chg0017_backend_web_pre_chg0029_20260825_0252
ROLLBACK_IMAGE_ID=sha256:fcada4935126e1b46360a560c76a1449e37f65d1344ae05cf5e37ddeeed6bf3e
```

The r2 container was created with explicit `--entrypoint=` so the committed builder entrypoint could not override the normal Backend command. Environment values were preserved without printing secrets.

## Runtime source and route evidence

```text
/app/backend-web/app/api/routes/_exports.py sha256=7a12eeaf419e63a6ff1c645b162157141482a9604f1de63509bea60e1a233855
/app/backend-web/app/api/routes/cookies.py sha256=f1c070eaa1cc8f9117f1c7679df3024314bd1e7793960e3ee9fa5bd023e739f3
/app/backend-web/app/api/routes/product_publish_capability.py sha256=1fad83c33dcab3c5e5dac649ef53e13427d3bc9dfd03cfd890b0f63f0fea1cf7
/app/backend-web/app/services/publish_account_capability_service.py sha256=702432eac538f4928927fb4a667b82d69b5cc6655e963e2baa01d79ea6685429
OPENAPI_HAS_SELECTED_ACCOUNT_CAPABILITY_ROUTE=true
UNAUTHENTICATED_ROUTE_PROBE=/api/v1/product-publish/accounts/1/capability -> HTTP_401
GLOBAL_ON_DEMAND_PRESENT=true
GLOBAL_NOT_CHECKED_PRESENT=true
PUBLISH_CONSUMER_WRITER_CREATED=false
ACCOUNT_LIST_POLLING_PRODUCER=false
BROWSER_GATE_ADDED=false
```

The 401 response proves the route is registered behind existing auth; no authenticated selected-account MTOP/preget call was made in this run.

## Account cohorts and read-only runtime state

```text
ACCOUNTS_ACTIVE=7
ACCOUNTS_DISABLED=5
SESSION_REAL_BROWSER_LOGIN_READY=7
SESSION_HUMAN_QR_REQUIRED=1
SESSION_CHECK_PENDING=3
SESSION_RENEW_FAILED=1
PUBLISH_CONSUMER_STATE_NULL=12
TOKEN_CACHE_TOTAL=24
TOKEN_CACHE_CURRENT=4
AUTO_REPLY_24H_TOTAL=0
PUBLISH_24H_TOTAL=0
```

No Cookie, Token, Authorization value, customer message text, item content, or address text was printed or persisted.

## Online chat authenticated read-only probe

Probe method: inside the Backend container, `ensure_jwt_secret_key(get_settings())` loaded the database-managed JWT secret and a short-lived admin JWT was generated in process only. The token was never printed or persisted. The probe used only formal `GET /api/v1/chat-new/accounts`, `GET /api/v1/chat-new/conversations/{account_id}`, and `GET /api/v1/chat-new/messages/{account_id}/{cid}` APIs. It did not call connect, disconnect, send, QR, Browser, ItemSync, or publish APIs.

```text
AUTH_USER_FOUND=true
DB_ACTIVE_SESSION_COUNTS={"active": 7, "active_cookie": 7, "active_human_qr_required": 0, "active_login_ready": 4, "active_other_not_authoritative": 0, "active_session_check_pending": 3, "active_session_renew_failed": 0, "disabled": 5, "total": 12}
CHAT_ACCOUNTS_HTTP=200
CHAT_ACCOUNTS_COUNT=12
CHAT_ACCOUNTS_FIRST_KEYS=account_id,chat_reason,chat_state,connected,connection_state,display_name,owner,platform_verification_evidence,platform_verification_required,platform_verification_source,remark,runtime_connected,session_reason,session_state,status,token_ready,token_state
CHAT_ACCOUNTS_AGG={"connected_true": 3, "disabled_true": 5, "failed_hint": 1, "human_qr_hint": 2, "login_ready_hint": 7, "online_true": 0, "runtime_connected_true": 3, "total": 12}
CHAT_COHORT_EXACT=READY_AND_RUNTIME_CONNECTED_3__READY_BUT_NO_CACHED_TOKEN_1__CHECKING_2__PLATFORM_VERIFICATION_1__DISABLED_5
CONVERSATION_CONNECTED_CANDIDATES=3
CONVERSATION_CONNECTED_RESULTS=HTTP200_SUCCESS_FOR_CONNECTED_SAMPLE
CONVERSATION_HTTP_200=3
CONVERSATION_SUCCESS_TRUE=3
CONVERSATION_FAILURES=0
CONVERSATION_SAMPLE_COUNT=5
CONVERSATION_SAMPLE_HAS_MORE=true
CONVERSATION_SAMPLE_FIRST_KEYS=cid,itemTitle,lastMessageSummary,lastMessageTime,otherUserAvatar,otherUserId,otherUserName,rawCid,unreadCount
MESSAGE_LIST_HTTP=200
MESSAGE_LIST_SUCCESS_TRUE=True
MESSAGE_LIST_COUNT=3
MESSAGE_LIST_SHAPE=dict
MESSAGE_LIST_FIRST_KEYS=images,isSelf,messageId,senderId,senderName,text,time,type
```

The API-level account list reports seven login-ready hints because it includes session/cache lineage visible to the existing Chat status composer. The startup runtime cohort is stricter: Backend r2 startup logged `eligible=4, ready=3, skipped=3`, and the current active database cohort has four active accounts in authoritative `REAL_BROWSER_LOGIN_READY`. Three are runtime-connected and pass formal read-only conversation evidence. A connected sample returned five conversations with `hasMore=true`, and its message list returned three records; only response shape/count was recorded. The fourth active+ready account failed closed during runtime-only rehydration because a valid cached Chat token was unavailable; no Session state was downgraded, no Token repair was attempted, and no manual reconnect was invoked.

`TOKEN_CACHE_CURRENT=4` is therefore not the same population as `CHAT_ACCOUNTS_AGG.login_ready_hint=7`: token cache current rows are cached Chat/IM token records, while login-ready hints include account Session/Cookie lineage and disabled/history rows surfaced by the account status API. The accepted runtime criterion is the connected queue and read-only conversation/message result above, not the raw token-cache total.

## WebSocket queue, reconnect, and self-rehydration evidence

```text
BACKEND_R2_STARTUP_REHYDRATION=eligible=4,ready=3,skipped=3
CHAT_RUNTIME_CONNECTED_QUEUE=3
CHAT_RUNTIME_CONNECTED_READ_PASS=3
CHAT_STARTUP_NOT_READY_REASON_FOR_REMAINING_ELIGIBLE=cached_chat_token_unavailable
CHAT_SELF_REHYDRATION=PASS_FOR_VALID_CACHED_TOKEN__3_READY_1_FAIL_CLOSED_NO_CACHE
WEBSOCKET_RECONNECT_WINDOW_20M=14_IN_SINGLE_EARLY_5M_BUCKET
WEBSOCKET_RECONNECT_WINDOW_15M=0
WEBSOCKET_RECONNECT_WINDOW_10M=0
WEBSOCKET_RECONNECT_WINDOW_5M=0
WEBSOCKET_ERROR_OR_CRITICAL_20M=0
WEBSOCKET_TOKEN_FETCH_OR_REFRESH_NONSKIP_20M=0
WEBSOCKET_INTERNAL_CONNECTION_STATS=success_total_instances_7_connected_7_by_state_connected_7
WEBSOCKET_RECONNECT_EVENTS_30M=2_INSTANT_ALL_ACCOUNT_EVENTS__NO_EVENT_AFTER_0247
```

The 30-minute reconnect text count corresponds to two full-account instantaneous events, around 02:41 and 02:47, with no new event for approximately 20 minutes afterward. Current WebSocket internal stats report seven of seven instances connected, RestartCount is 0, and ERROR/CRITICAL count is 0. This supports `RECONNECT_LOOP=false` for current runtime. The existing Backend self-rehydration owner remains `app.services.chat_new.im_session_manager.rehydrate_eligible_accounts_on_startup`; CHG-0029 did not add a second Chat/WebSocket lifecycle owner.

## Auto-reply worker and desired-connected cohort

```text
AUTO_REPLY_OWNER=XIANYU_WEBSOCKET_EXISTING_OWNER
AUTO_REPLY_DESIRED_ACTIVE_ACCOUNTS=7
AUTO_REPLY_AI_ENABLED_ACCOUNTS=0
AUTO_REPLY_AUTHORITATIVE_ONLINE_READY_ACTIVE=4
AUTO_REPLY_WEBSOCKET_CONNECTED_INSTANCES=7
AUTO_REPLY_BUSINESS_CAPABILITY_COHORT=ONLINE_4__CHECKING_2__PLATFORM_VERIFICATION_REQUIRED_1__DISABLED_5
AUTO_REPLY_SESSION_CHECK_PENDING_ACTIVE=2
AUTO_REPLY_24H_TOTAL=0
AUTO_REPLY_24H_ZERO_REASON=EXPECTED_CONFIGURATION__AI_ENABLED_FALSE_FOR_12_ACCOUNTS
AUTO_REPLY_WORKER_BACKLOG_OBSERVED=false
AUTO_REPLY_TOKEN_STORM=false
AUTO_REPLY_RECONNECT_LOOP=false
```

`/api/v1/cookies/details/paginated` returned HTTP 200 and total 12: enabled+online=7, disabled/offline=5, `AI_ENABLED=false` for all 12. The zero 24h auto-reply activity is therefore an expected configuration fact, not a worker failure. No recent inbound real message was available to reproduce an auto-reply send path, and sending a real message is outside authorization. The acceptance is source/runtime/health/cohort based with `REAL_E2E=NOT_RECENTLY_REPRODUCED_NO_MESSAGE_SENT`, not a live send canary.

## Business capability cohorts

```text
COOKIES_DETAILS_PAGINATED_HTTP=200
COOKIES_DETAILS_TOTAL=12
COOKIES_ENABLED_ONLINE=7
COOKIES_DISABLED_OFFLINE=5
COOKIES_AI_ENABLED_FALSE=12
AUTO_REPLY_BUSINESS_CAPABILITY=ONLINE_4__CHECKING_2__PLATFORM_VERIFICATION_REQUIRED_1__DISABLED_5
ONLINE_CHAT_BUSINESS_CAPABILITY=READY_3__CONNECTING_NO_CACHED_TOKEN_1__CHECKING_2__PLATFORM_VERIFICATION_REQUIRED_1__DISABLED_5
PUBLISH_BUSINESS_CAPABILITY=NOT_CHECKED_ON_DEMAND_7__DISABLED_5
PUBLISH_PREGET_OR_CAPABILITY_MARKER_DELTA_AROUND_ACCOUNT_LIST=0
```

## Health and safety

```text
BACKEND_HEALTH=HTTP_200
WEBSOCKET_HEALTH=HTTP_200
SCHEDULER_HEALTH=HTTP_200
FRONTEND_HEALTH=HTTP_200
WEBSOCKET_PID1=/sbin/docker-init -- python websocket/main.py
WEBSOCKET_ZOMBIES=0
WEBSOCKET_RESTART_COUNT=0
BACKEND_RESTART_COUNT=0
WEBSOCKET_TOKEN_FETCH_10M=0
WEBSOCKET_SKIP_REFRESH_10M=13
WEBSOCKET_LEVEL_ERROR_OR_GATE_10M=0
BACKEND_SIDE_EFFECT_ENDPOINTS_10M=0
BACKEND_READ_ENDPOINTS_10M=1
BACKEND_LEVEL_ERROR_OR_GATE_10M=0
REAL_MESSAGES_SENT=0
REAL_PRODUCTS_PUBLISHED=0
REAL_PRODUCTS_MODIFIED=0
ITEM_SYNC_INVOCATION_COUNT=0
QR_LOGIN_INVOCATION_COUNT=0
MANUAL_RECONNECT_INVOCATION_COUNT=0
BROWSER_INVOCATION_COUNT=0
PLAYWRIGHT_CDP_INVOCATION_COUNT=0
```

## Capability acceptance

```text
AUTO_REPLY_SOURCE=PASS_EXISTING_OWNER
AUTO_REPLY_RUNTIME=PASS_WEBSOCKET_CHG0023_HEALTHY
AUTO_REPLY_COHORT=PARTIAL__AI_ENABLED_0__ONLINE_READY_4__CHECKING_2__PLATFORM_VERIFICATION_1__DISABLED_5
AUTO_REPLY_SYSTEM=RESOLVED
AUTO_REPLY_CURRENT_CONFIG=NO_REAL_AUTO_REPLY_BECAUSE_AI_ENABLED_0_OF_12
AUTO_REPLY_REAL_E2E=NOT_RECENTLY_REPRODUCED_NO_MESSAGE_SENT

ONLINE_CHAT_SOURCE=PASS_EXISTING_OWNER
ONLINE_CHAT_RUNTIME=PASS_BACKEND_AND_WEBSOCKET_HEALTHY__3_CONNECTED_CONVERSATION_READ_PASS
ONLINE_CHAT_COHORT=PARTIAL__READY_3__NO_CACHED_TOKEN_FAIL_CLOSED_1__CHECKING_2__PLATFORM_VERIFICATION_1__DISABLED_5
ONLINE_CHAT_SYSTEM=RESOLVED
ONLINE_CHAT_REAL_E2E=READ_ONLY_CONVERSATION_AND_MESSAGE_LIST_PASS_NO_SEND

PUBLISH_SOURCE=PASS_CHG0028_MAIN_MERGED
PUBLISH_RUNTIME=PASS_CHG0028_ROUTE_ACTIVE
PUBLISH_COHORT=NOT_CHECKED_ON_DEMAND_7__DISABLED_5__SELECTED_ACCOUNT_ROUTE_AUTH_REQUIRED
PUBLISH_SYSTEM=RESOLVED
PUBLISH_REAL_E2E=AWAITING_SEPARATE_EXPLICIT_CANARY_AUTHORIZATION
CHG0028_RUNTIME_ACTIVATED=true
```

## Deterministic tests and regressions

```text
pytest changes/active/CHG-0029-core-capability-closure/tests/test_acceptance.py changes/archive/CHG-0028-publish-readiness-owner-convergence/tests/test_acceptance.py tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py -q --import-mode=importlib = 20 passed
pytest changes/archive/CHG-0022-websocket-token-network-classification/tests/test_acceptance.py changes/archive/CHG-0026-qr-dual-mode-and-chat-connectivity-recovery/tests/test_acceptance.py changes/archive/CHG-0027-session-transient-classification-qr-cooldown-lineage/tests/test_acceptance.py -q --import-mode=importlib = 15 passed
ruff check . = PASS
security_scan.py = PASS
git diff --check = PASS
validate_change.py = PRE_EXISTING_BLOCKED_CHG0020_ARCHIVE_MISSING_DESIGN_TASKS
verify_repository.py = PRE_EXISTING_BLOCKED_CHG0020_ARCHIVE_MISSING_DESIGN_TASKS
tests/unit/test_chg0022_websocket_token_network_classification.py = PRE_EXISTING_BLOCKED_ACTIVE_PATH_ASSUMPTION
GLOBAL_CI_DEBT_ABSORBED=NO
```

The CHG0022 unit failure and CHG0020 archive validation failure are the same pre-existing governance debts already classified in CHG-0028 evidence; CHG-0029 did not modify or absorb them.

## GitHub closure

```text
PR_NUMBER=42
PR_MERGED=true
LOCAL_COMMIT_SHA=a90c508f010d7e46a91b7986154117f50f1fbaed
REMOTE_BRANCH_SHA=a90c508f010d7e46a91b7986154117f50f1fbaed
MERGE_COMMIT_SHA=fe1b184c9d32c9d94721320702b5d6b0c55fe169
REMOTE_MAIN_SHA=fe1b184c9d32c9d94721320702b5d6b0c55fe169
SCOPED_CI_SECURITY=PASS
SCOPED_CI_QUALITY=FAIL_SAME_AS_MAIN_GLOBAL_CHG0020_DEBT
SCOPED_CI_TESTS=FAIL_SAME_AS_MAIN_GLOBAL_GOVERNANCE_AND_CHG0022_DEBT
GLOBAL_CI_DEBT_ABSORBED=NO
```
