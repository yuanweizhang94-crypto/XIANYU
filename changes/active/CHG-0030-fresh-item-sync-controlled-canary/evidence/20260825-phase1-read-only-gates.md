# CHG-0030 phase 1 read-only gate evidence - 2026-08-25

Change ID: CHG-0030-fresh-item-sync-controlled-canary
Status: IMPLEMENTING

## Execution Contract

User outcome: one controlled Fresh Item Sync canary with terminal and durable-truth proof, then GitHub closure.

Confirmed blocker: selected capability and trace identity are not yet explicit.

Smallest success test: one selected eligible account, exactly one owner invocation, terminal SUCCESS plus durable xy_catalog_items readback, duplicate 0 and all excluded safety counters 0.

## Current Git Authority

START_CWD=`D:/xianyu`

DIRTY_CHG0018_BRANCH=`feat/CHG-0018-account-profile-publish-safety`

DIRTY_CHG0018_HEAD=`a8b1a996f439d1136764ccd338de6438f1cb5082`

DIRTY_CHG0018_STATUS=PRE_EXISTING_DIRTY_FILES_PRESENT

DIRTY_CHG0018_TOUCHED=0

REMOTE_MAIN_SHA=`8d1d1d0fb272cd2715135d077be98ce0b575cb79`

FETCH_HEAD_SHA=`8d1d1d0fb272cd2715135d077be98ce0b575cb79`

REMOTE_MAIN_ANCESTRY=PASS

TARGET_PATH_ABSENT_BEFORE_CREATE=true

LOCAL_BRANCH_ABSENT_BEFORE_CREATE=true

REMOTE_BRANCH_ABSENT_BEFORE_CREATE=true

WORKTREE=`D:/xianyu-worktrees/CHG-0030-fresh-item-sync-controlled-canary`

BRANCH=`feat/CHG-0030-fresh-item-sync-controlled-canary`

WORKTREE_BASE_SHA=`8d1d1d0fb272cd2715135d077be98ce0b575cb79`

PROJECT_CONTEXT_BEFORE_DEVELOPMENT=PASS_CLEAN_NO_ACTIVE_CHANGE

## Pinned Upstream Evidence

PINNED_UPSTREAM=`D:/xianyu-upstream-pilot`

PINNED_UPSTREAM_SHA=`bda1a859df63fa5f24e51398fa80a23490bb6dfc`

UPSTREAM_ROUTE_FILE=`backend-web/app/api/routes/items.py`

UPSTREAM_ROUTE=`POST /api/v1/items/get-all-from-account`

UPSTREAM_SERVICE_FILE=`common/services/item_service.py`

UPSTREAM_OWNER=`ItemService.fetch_all_items_from_account`

UPSTREAM_LOCK=`item_sync:{account_id}`

UPSTREAM_IMPL=`ItemService._fetch_all_items_from_account_impl`

UPSTREAM_REMOTE_READ=`ItemInfoManager.get_item_list_info(page)`

UPSTREAM_DURABLE_TRUTH=`xy_catalog_items`

UPSTREAM_REMOTE_MUTATION_OWNER_PRESENT=false

## Existing Owner Chain

EXISTING_OWNER_CHAIN_PROVEN=true

ACCEPTED_CHAIN=`COMPANY xianyu_item_sync -> POST /api/v1/items/get-all-from-account?no_auth_recovery=true -> ItemService.fetch_all_items_from_account -> _fetch_all_items_from_account_impl -> ItemInfoManager.get_item_list_info -> save_fetched_items -> xy_catalog_items`

REUSE_DECISION=PATCH_UPSTREAM

NEW_ITEM_SYNC_OWNER_CREATED=false

MANUAL_REMOTE_READ_PLUS_DB_UPSERT_BYPASS_CREATED=false

SINGLE_PAGE_PRIMITIVE_USED_AS_OWNER=false

## COMPANY Adapter Read-Only Inspection

COMPANY_REPO_PROXY=`D:/TikTok_Auto/COMPANY_LOCAL_EXECUTION_TOOL/runtime/devspace_proxy/proxy.cjs`

COMPANY_REPO_PROXY_SHA256=`C8D7EB66F2720AFE874EB7D9B22E85499252B836525439D609FED3E869CEF4C9`

COMPANY_LIVE_PROXY=`D:/TikTok_Auto/devspace_proxy/proxy.cjs`

COMPANY_LIVE_PROXY_SHA256=`4013CF505BA036FFF11F0382761F14BE7711E8280DDD41097C285DC8D7FDE041`

COMPANY_GIT_STATUS_READ=BLOCKED_DUBIOUS_OWNERSHIP_NO_SAFE_DIRECTORY_MUTATION

LIVE_SCHEMA_TOOL=`xianyu_item_sync`

LIVE_SCHEMA_FIELDS=`account_id,page_size,max_pages`

LIVE_SCHEMA_TASK_ID_FIELD_PRESENT=false

LIVE_SCHEMA_REQUEST_ID_FIELD_PRESENT=false

LIVE_SCHEMA_TRACE_ID_FIELD_PRESENT=false

LIVE_SCHEMA_OPERATION_ID_FIELD_PRESENT=false

LIVE_IMPL_FORCES_NO_AUTH_RECOVERY=true

TRACKABLE_SYNC_STATUS_TOOL_FOUND=false

TRACKABLE_ITEM_SYNC_OPERATION_LEDGER_FOUND=false

TRACE_IDENTITY_AVAILABLE=PATCH_ARTIFACT_AVAILABLE_NOT_DEPLOYED

TRACE_IDENTITY_GATE=BACKEND_CONTRACT_PATCHED_NOT_DEPLOYED_ADAPTER_NOT_PASSTHROUGH

## Read-Only Auth And Eligibility Path

CURRENT_READ_ONLY_ACCOUNT_TOOL=`xianyu_account_status`

ACCOUNT_STATUS_READ_ONLY=true

ACCOUNT_STATUS_FIELDS_INCLUDE=`LOGIN_READY,ACCOUNT_ENABLED,ACCOUNT_ONLINE,PLATFORM_CERTIFICATION_REQUIRED,diagnostics.fields_present`

ACCOUNT_STATUS_ITEM_SYNC_ELIGIBILITY_FIELD_PRESENT=false

ACCOUNT_STATUS_DOES_NOT_PROVE_ITEM_SYNC_SELECTED_ACCOUNT_ELIGIBLE=true

SELECTED_ACCOUNT_MASKED=`22*********60`

SELECTED_ACCOUNT_LOCAL_ROWS_PRIOR=20

SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PATCH_ARTIFACT_AVAILABLE_NOT_DEPLOYED

SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY_GATE=BACKEND_CONTRACT_PATCHED_NOT_DEPLOYED_ADAPTER_NOT_PASSTHROUGH

## Canary Decision

PRODUCTION_ITEM_SYNC_CANARY_GO=false

COMMANDER_GO_RECEIVED=false

ITEM_SYNC_INVOCATION_ALLOWED=false

NO_GO_REASON=PATCH_ARTIFACT_READY_BUT_NOT_DEPLOYED_AND_CURRENT_COMPANY_ADAPTER_DOES_NOT_PASS_THROUGH_REQUIRED_FIELDS

MINIMAL_NEXT_ACTION=DEPLOY_XIANYU_PATCH_THROUGH_EXISTING_RUNTIME_PATH_AND_UPDATE_CLEAN_COMPANY_ADAPTER_PASSTHROUGH_BEFORE_GO

## Safety Counters

ITEM_SYNC_INVOCATION_COUNT=0

REMOTE_ITEM_READ_COUNT=0

LOCAL_ITEM_WRITE_COUNT=0

REMOTE_LISTING_CREATE_COUNT=0

REMOTE_LISTING_EDIT_COUNT=0

REMOTE_LISTING_OFFLINE_COUNT=0

REMOTE_LISTING_DELETE_COUNT=0

REAL_PRODUCTS_PUBLISHED=0

REAL_PRODUCTS_MODIFIED=0

REAL_MESSAGES_SENT=0

BROWSER_INVOCATION_COUNT=0

PLAYWRIGHT_CDP_INVOCATION_COUNT=0

QR_LOGIN_INVOCATION_COUNT=0

MANUAL_RECONNECT_INVOCATION_COUNT=0

PRODUCTION_ACCOUNT_MUTATION_COUNT=0

PRODUCTION_CONFIG_CHANGE_COUNT=0

PRODUCTION_RESTART_COUNT=0

## Focused Validation

PYTEST_CHG0030_ACCEPTANCE=`pytest changes/active/CHG-0030-fresh-item-sync-controlled-canary/tests/test_acceptance.py -q`

PYTEST_CHG0030_ACCEPTANCE_RESULT=`7 passed in 0.03s`

VALIDATE_CHANGE_COMMAND=`python scripts/validate_change.py`

VALIDATE_CHANGE_RESULT=`FAILED_GLOBAL_PRE_EXISTING_CHG0020_ARCHIVE_DEBT`

VALIDATE_CHANGE_ERROR=`missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md`

GIT_DIFF_CHECK_COMMAND=`git diff --check -- changes/active/CHG-0030-fresh-item-sync-controlled-canary generated/PROJECT_STATE.json`

GIT_DIFF_CHECK_RESULT=PASS

PROJECT_CONTEXT_AFTER_ACTIVE_CHANGE=PASS_ACTIVE_CHG0030_IMPLEMENTING

VERIFY_REPOSITORY_COMMAND=`python scripts/verify_repository.py`

VERIFY_REPOSITORY_RESULT=`FAILED_GLOBAL_PRE_EXISTING_CHG0020_ARCHIVE_DEBT`

VERIFY_REPOSITORY_ERROR=`missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md`

## Phase 2 Root Cause

ROOT_CAUSE=EXISTING_SANITIZED_ADAPTER_CONTRACTS_DROP_ITEM_SYNC_PREFLIGHT_AND_TRACE_FIELDS

AUTHORITATIVE_COMPANY_ITEM_SYNC_ADAPTER_SOURCE=`D:/TikTok_Auto/devspace_proxy/proxy.cjs`

AUTHORITATIVE_COMPANY_ITEM_SYNC_ADAPTER_CLASSIFICATION=SEPARATE_DIRTY_COMPANY_CHECKOUT_NOT_MODIFIED

AUTHORITATIVE_COMPANY_ACCOUNT_STATUS_ADAPTER_SOURCE=`D:/TikTok_Auto/devspace_proxy/proxy.cjs`

AUTHORITATIVE_COMPANY_ACCOUNT_STATUS_ADAPTER_CLASSIFICATION=SEPARATE_DIRTY_COMPANY_CHECKOUT_NOT_MODIFIED

AUTHORITATIVE_XIANYU_ITEM_SYNC_ROUTE_SOURCE=`backend-web/app/api/routes/items.py`

AUTHORITATIVE_XIANYU_ITEM_SYNC_ROUTE_CLASSIFICATION=PINNED_UPSTREAM_PLUS_XIANYU_VENDOR_PATCH_ARTIFACT

AUTHORITATIVE_XIANYU_ACCOUNT_STATUS_SOURCE=`backend-web/app/api/routes/cookies.py`

AUTHORITATIVE_XIANYU_ACCOUNT_STATUS_CLASSIFICATION=PINNED_UPSTREAM_PLUS_XIANYU_VENDOR_PATCH_ARTIFACT

COMPANY_DIRTY_FILES_TOUCHED=0

XIANYU_RUNTIME_DEPLOYED=false

PRODUCTION_CANARY_INVOKED=false

## Phase 2 RED To GREEN

RED_TEST_COMMAND=`pytest tests/unit/test_chg0030_fresh_item_sync_canary_patch_artifact.py -q`

RED_TEST_RESULT=`5 failed because vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch did not exist`

PATCH_ARTIFACT=`vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch`

PATCH_ARTIFACT_SCOPE=`common/schemas/item.py; backend-web/app/api/routes/cookies.py; backend-web/app/api/routes/items.py; tests/test_chg0030_fresh_item_sync_controlled_canary.py`

PATCH_REPAIR_CATEGORY=PATCH_UPSTREAM

PATCH_DEFAULT_COMPATIBILITY=EXISTING_FIELDS_PRESERVED_AND_NEW_FIELDS_ADDED

PATCH_ROLLBACK=REMOVE_CHG0030_VENDOR_PATCH_LAYER

GREEN_TEST_COMMAND=`pytest tests/unit/test_chg0030_fresh_item_sync_canary_patch_artifact.py -q`

GREEN_TEST_RESULT=`5 passed in 0.05s`

FOCUSED_CHG0030_COMMAND=`pytest changes/active/CHG-0030-fresh-item-sync-controlled-canary/tests/test_acceptance.py tests/unit/test_chg0030_fresh_item_sync_canary_patch_artifact.py -q`

FOCUSED_CHG0030_RESULT=`12 passed in 0.08s`

CHG0028_REGRESSION_COMMAND=`pytest tests/unit/test_chg0028_selected_account_on_demand_patch_artifact.py -q`

CHG0028_REGRESSION_RESULT=`5 passed in 0.10s`

CHG0024_ITEM_SYNC_SAFETY_REGRESSION_COMMAND=`pytest changes/archive/CHG-0024-item-sync-no-auth-recovery-safety/tests/test_acceptance.py -q`

CHG0024_ITEM_SYNC_SAFETY_REGRESSION_RESULT=`8 passed in 0.11s`

CHG0022_SESSION_LINEAGE_REGRESSION_COMMAND=`pytest tests/unit/test_chg0022_websocket_token_network_classification.py -q`

CHG0022_SESSION_LINEAGE_REGRESSION_RESULT=`FAILED_GLOBAL_PRE_EXISTING_ACTIVE_PATH_ASSUMPTION`

CHG0022_SESSION_LINEAGE_ERROR=`tests expect changes/active/CHG-0022-websocket-token-network-classification, which is absent on current main`

PHASE2_GIT_DIFF_CHECK_RESULT=PASS

## Minimal Patch

No XIANYU business-owner code defect is proven by phase 1. If the commander wants to unblock the canary in a later repair scope, the smallest likely patch is in the existing COMPANY `xianyu_item_sync` thin adapter only:

- accept a caller-supplied or adapter-created `task_id`/`operation_id` for one Item Sync invocation;
- persist an operation record before the backend call;
- return the identity in both terminal and UNKNOWN responses;
- provide a read-only status lookup for that identity;
- expose explicit selected-account Item Sync eligibility as a read-only preflight that does not invoke sync;
- keep `no_auth_recovery=true`, keep public credentials/endpoints forbidden, and keep XIANYU `ItemService.fetch_all_items_from_account` as the only business owner.

This is not implemented in CHG-0030 phase 1.
