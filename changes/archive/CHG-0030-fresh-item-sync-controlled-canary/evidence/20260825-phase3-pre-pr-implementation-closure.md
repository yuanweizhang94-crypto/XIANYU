# CHG-0030 Phase 3 Pre-PR Implementation Closure Evidence

Date: 2026-08-25

Production deploy/restart: no

Item Sync invocation: no

Commit/push/PR state at evidence creation: pending

## Governance Repair

`IMPLEMENTING_CHANGE_ALL_TASKS_COMPLETE=false`

`PROJECT_STATE_NEXT_TASK_REQUIRED=true`

Phase 3 adds ordered incomplete tasks for final local verification, implementation commit/PR/CI, validated deployment, post-deploy preflight, one canary, terminal durable readback, and closure commit/merge.

## Locked Patch Artifact

`PATCH_ARTIFACT=vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch`

`PATCH_ARTIFACT_SHA256=595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201`

`PATCH_ARTIFACT_LOCKED=true`

`PATCH_ARTIFACT_EDIT_AFTER_LOCK=false`

`PATCH_CLEAN_APPLY_BASE_SHA=8c2723e552bb9f797c73b6c497858bc314549877`

The patch artifact is now registered in `vendor/patches/xianyu-auto-reply/README.md`. Do not edit the patch after this hash lock; generate a replacement patch with a new SHA only under a later authorized task if required.

## Runtime Result Shape Review

`ITEM_SERVICE_OWNER=ItemService.fetch_all_items_from_account`

`ITEM_SERVICE_RESULT_KEYS=success,message,items,total_count,total_pages,page_size,saved_count,full_active_list_confirmed,platform_status_reconciliation`

`ROUTE_ADDED_RESULT_KEYS=operation_id,request_id,masked_account_id,sync_status,terminal,retry_allowed,owner,durable_readback,page_size,max_pages`

The patched route preserves the existing ItemService result and appends canary-control fields around it. The selected-account path creates/logs an operation identity before the one owner call and attaches terminal durable readback after the owner returns.

## Current Durable Constraint Review

`XY_CATALOG_ITEMS_TABLE=xy_catalog_items`

`ORM_ACCOUNT_ITEM_INDEX=idx_cat_account_item(account_id,item_id)`

`RUNTIME_UNIQUE_KEY=uk_cat_account_item(account_id,item_id)`

`RUNTIME_UNIQUE_KEY_SOURCE=common/db/init_database.py`

`DUPLICATE_PRECHECK_BEFORE_UNIQUE_KEY_CREATE=true`

The ORM model declares the account/item index for query access. The runtime database initialization/migration path creates `uk_cat_account_item (account_id, item_id)` after checking for duplicate groups; if duplicates already exist, it refuses to create the key and logs a manual remediation warning instead of deleting data. CHG-0030 therefore measures duplicate groups during durable readback and does not assume duplicate count is zero.

## Deterministic Rollback Recipe

`ROLLBACK_DEFAULT_OFF=true`

`ROLLBACK_RESTORE_PREVIOUS_RUNTIME_IMAGE=true`

`ROLLBACK_REMOVE_CHG0030_PATCH_FROM_DEPLOYMENT_STACK=true`

`ROLLBACK_DB_MIGRATION_REQUIRED=false`

`ROLLBACK_DATA_DELETION_REQUIRED=false`

Rollback before deployment is deletion of CHG-0030 local artifacts from the isolated worktree. Rollback after deployment is to redeploy the previous accepted backend runtime image or rebuild the runtime stack without applying `chg0030-fresh-item-sync-controlled-canary.patch`. The patch adds no table, migration, queue, scheduler, worker, or persistent operation ledger, so rollback does not require DB schema change or data deletion.

## Deterministic Deployment Recipe

`DEPLOYMENT_REQUIRED_BEFORE_PREFLIGHT_PASS=true`

`PRODUCTION_CANARY_AFTER_DEPLOY_STILL_REQUIRES_COMMANDER_GO=true`

Deploy only after PR review/merge and explicit deployment authorization. Apply the locked CHG-0030 patch over the accepted CHG-0024/CHG-0027/CHG-0028/CHG-0029 backend source stack, verify patch SHA before apply, run strict clean-apply, run patched runtime tests, build/deploy the backend through the existing project deployment path, then inspect container logs for the structured CHG-0030 events. Do not invoke Item Sync during deployment.

## Safety Counters

`ITEM_SYNC_INVOCATION_COUNT=0`

`REMOTE_ITEM_READ_COUNT=0`

`LOCAL_ITEM_WRITE_COUNT=0`

`REMOTE_LISTING_CREATE_COUNT=0`

`REMOTE_LISTING_EDIT_COUNT=0`

`REMOTE_LISTING_OFFLINE_COUNT=0`

`REMOTE_LISTING_DELETE_COUNT=0`

`REAL_MESSAGES_SENT=0`

`BROWSER_INVOCATION_COUNT=0`

`PLAYWRIGHT_CDP_INVOCATION_COUNT=0`

`PRODUCTION_ACCOUNT_MUTATION_COUNT=0`

`PRODUCTION_CONFIG_CHANGE_COUNT=0`

`PRODUCTION_RESTART_COUNT=0`

## Phase 3 Local Verification Matrix

`MATRIX_RUNNER_PRIMARY=D:/xianyu/.venv/Scripts/python.exe`

`MATRIX_RUNTIME_REPLAY_RUNNER=python`

The actual clean-replay runtime tests require the runtime-capable Python environment because `D:/xianyu/.venv/Scripts/python.exe` does not contain `loguru`. The venv replay attempt failed only with `ModuleNotFoundError: No module named 'loguru'`; the same replay passed with the runtime-capable Python used for prior patch replay.

### Passing checks

`CHG0030_FOCUSED_TESTS=14 passed`

Command:

```powershell
D:/xianyu/.venv/Scripts/python.exe -m pytest changes/active/CHG-0030-fresh-item-sync-controlled-canary/tests/test_acceptance.py tests/unit/test_chg0030_fresh_item_sync_canary_patch_artifact.py -q
```

`CLEAN_REPLAY_PY_COMPILE_EXIT=0`

`CLEAN_REPLAY_RUNTIME_TESTS=15 passed`

Command:

```powershell
python -m py_compile common/schemas/item.py backend-web/app/api/routes/items.py backend-web/app/api/routes/cookies.py
python -m pytest tests/test_chg0028_selected_account_on_demand_capability.py tests/test_chg0030_fresh_item_sync_controlled_canary.py -q
```

`CHG0024_OWNER_CONTRACT_TESTS=8 passed`

`CHG0026_SESSION_COOKIE_REGRESSION=6 passed`

`CHG0027_SESSION_LINEAGE_REGRESSION=5 passed`

`CHG0028_PATCH_ARTIFACT_TESTS=5 passed`

`CHG0028_ARCHIVE_ACCEPTANCE_CLEAN_HEAD=8 passed`

`CHG0029_ARCHIVE_ACCEPTANCE_CLEAN_HEAD=8 passed`

`CHG0018_PUBLISH_ACCEPTANCE_CLEAN_HEAD=9 passed`

`AUTO_REPLY_ONLINE_CHAT_PUBLISH_UNIT_REGRESSIONS=195 passed`

`CHG0023_ONLINE_CHAT_ACCEPTANCE=5 passed`

`DUPLICATE_CAPABILITY_TESTS=19 passed`

`DUPLICATE_CAPABILITY_SCRIPT=passed`

`SECURITY_SCAN=passed`

`RUFF=passed`

`GIT_DIFF_CHECK=passed`

Archive tests with basename `test_acceptance.py` were run one at a time or in a clean tracked-HEAD clone to avoid pytest module-name collisions and active-change assertions that are not behavioral regressions.

### Proven unrelated debt

`PRE_EXISTING_CHG0020_ARCHIVE_DEBT=missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md`

`PRE_EXISTING_CHG0022_ACTIVE_PATH_DEBT=tests/unit/test_chg0022_websocket_token_network_classification.py expects changes/active/CHG-0022-websocket-token-network-classification while CHG-0030 is active`

`PRE_EXISTING_AGENTS_DRIFT=test_governance_docs.py expects AGENTS.md text 'Do not create large adapter abstractions' that is absent from current HEAD`

`README_DRIFT_PROVEN=false`

`VERIFY_REPOSITORY_EXIT=1`

`VALIDATE_CHANGE_EXIT=1`

`GOVERNANCE_DOCS_TARGETED_EXIT=1`

The failing validation/governance commands are explained by the CHG-0020, CHG-0022, and AGENTS debt above. CHG-0030 focused tests, patch replay, owner/capability regressions, duplicate checks, security scan, ruff, and `git diff --check` passed.

## Implementation Commit And Push

`PRE_EXISTING_UNRELATED_DIRTY_FILES=none`

`STAGED_WITH_GIT_ADD_DOT=false`

`STAGED_WITH_GIT_ADD_A=false`

`IMPLEMENTATION_COMMIT_SHA=eb8b749a4dcb6a1461761f626daa89183af4f5e6`

`REMOTE_BRANCH_AFTER_IMPLEMENTATION_SHA=eb8b749a4dcb6a1461761f626daa89183af4f5e6`

`IMPLEMENTATION_REMOTE_SHA_MATCH=true`

`ORIGIN_URL_CHANGED=false`

`FORCE_PUSH_USED=false`

The implementation commit was pushed to `origin/feat/CHG-0030-fresh-item-sync-controlled-canary` over the existing HTTPS remote. The exact staged file list was limited to CHG-0030 active records, evidence/tests, generated state, the CHG-0030 patch artifact, and vendor patch README registration.
