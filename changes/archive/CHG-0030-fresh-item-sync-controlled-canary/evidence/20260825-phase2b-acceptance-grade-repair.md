# CHG-0030 Phase 2b Acceptance-Grade Repair Evidence

Date: 2026-08-25

Production canary state: NO-GO

Item Sync invoked: no

Deploy/restart/commit/push: no

## Commander Rejection Findings

The commander rejected the prior CHG-0030 patch as not acceptance-grade:

- `durable_readback.checked=success` was not a real post-write durable DB readback.
- `duplicate_count=0` was hard-coded.
- current COMPANY adapter summaries strip backend operation/capability extension fields.
- eligibility inferred token readiness too narrowly and did not prove disabled/checking/platform-verification/session-cookie-lineage boundaries.

## Authoritative Source Locations

`AUTHORITATIVE_COMPANY_ITEM_SYNC_ADAPTER=D:/TikTok_Auto/devspace_proxy/proxy.cjs`

`AUTHORITATIVE_COMPANY_ITEM_SYNC_ADAPTER_CLASSIFICATION=separate_dirty_COMPANY_runtime_checkout_read_only`

`AUTHORITATIVE_COMPANY_TRACKED_ADAPTER=D:/TikTok_Auto/COMPANY_LOCAL_EXECUTION_TOOL/runtime/devspace_proxy/proxy.cjs`

`AUTHORITATIVE_COMPANY_TRACKED_ADAPTER_CLASSIFICATION=separate_dirty_COMPANY_checkout_read_only`

`AUTHORITATIVE_XIANYU_ACCOUNT_STATUS_SOURCE=D:/xianyu-chg0026-source/backend-web/app/api/routes/cookies.py plus CHG-0028 runtime patch`

`AUTHORITATIVE_XIANYU_ACCOUNT_STATUS_CLASSIFICATION=XIANYU_runtime_source_plus_pinned_vendor_patch_stack`

`AUTHORITATIVE_XIANYU_ITEM_SYNC_ROUTE_SOURCE=D:/xianyu-chg0026-source/backend-web/app/api/routes/items.py plus CHG-0024/CHG-0027/CHG-0028/CHG-0029 runtime stack`

`AUTHORITATIVE_XIANYU_ITEM_SYNC_ROUTE_CLASSIFICATION=XIANYU_runtime_source_plus_pinned_vendor_patch_stack`

`PINNED_UPSTREAM_SHA=bda1a859df63fa5f24e51398fa80a23490bb6dfc`

`CLEAN_APPLY_BASE_SHA=8c2723e552bb9f797c73b6c497858bc314549877`

The pinned upstream checkout is capability evidence. The clean apply base used for Phase 2b replay is a temporary full runtime-source baseline created from `D:/xianyu-chg0026-source` with the CHG-0028 patch applied over the CHG-0027/CHG-0029 runtime stack.

## Root Cause

`ROOT_CAUSE=backend_canary_contract_was_response_only_and_not_acceptance_grade`

The existing Item Sync business owner is valid, but the backend canary contract did not prove post-service durable truth, duplicate groups, or selected-account eligibility boundaries. The current COMPANY adapter also strips extension response fields, so operational observability must be available from sanitized backend structured logs as well as response fields.

## Repair Decision

`REUSE_DECISION=PATCH_UPSTREAM`

`WRAP_FOR_OPERATIONS=true`

`NEW_ITEM_SYNC_OWNER_CREATED=false`

`SECOND_DB_TRUTH_MODEL_CREATED=false`

`QUEUE_OR_STATUS_LEDGER_CREATED=false`

`SCHEDULER_OR_WORKER_CREATED=false`

`AUTH_RECOVERY_ADDED=false`

`REMOTE_PLATFORM_WRITE_ADDED=false`

`MESSAGE_BROWSER_ACCOUNT_MUTATION_ADDED=false`

The repair extends the existing XIANYU route/account-status contracts only. It preserves `ItemService.fetch_all_items_from_account` as the single Item Sync business owner.

## Actual Durable Readback Implementation

`DURABLE_READBACK_SOURCE=xy_catalog_items`

`DURABLE_READBACK_QUERY_ACTUAL_DB=true`

`DURABLE_READBACK_SCOPE=account_id`

`DURABLE_READBACK_ACCOUNT_ROW_COUNT_QUERY=true`

`DURABLE_READBACK_RESPONSE_ITEM_MATCH_QUERY=true`

`DURABLE_READBACK_DUPLICATE_GROUP_QUERY=true`

`DURABLE_READBACK_UNIQUE_CONTRACT=account_id,item_id`

`DUPLICATE_COUNT_MEASURED=true`

`DUPLICATE_COUNT_HARD_CODED=false`

`UNKNOWN_QUERY_FAILURE_TERMINAL=true`

`RETRY_ALLOWED_ON_UNKNOWN=false`

After `ItemService.fetch_all_items_from_account` returns, the patched route performs read-only SQLAlchemy queries against `XYCatalogItem` scoped to the selected account primary key:

- total local row count for the account;
- duplicate groups by `item_id` under the existing account/item unique contract;
- distinct response item IDs matched back to `xy_catalog_items`.

`durable_readback.checked=true` is returned only when the DB queries succeed, the route result is successful, response item IDs are unique, every response item ID is present in `xy_catalog_items`, no duplicate groups are found, and saved count is reconciled with account row count. Query failure or unreconciled state becomes terminal `UNKNOWN` with `retry_allowed=false`.

## Structured Log Events

`LOG_EVENT_ACCEPTED=CHG0030_ITEM_SYNC_OPERATION_ACCEPTED`

`LOG_EVENT_TERMINAL=CHG0030_ITEM_SYNC_TERMINAL_READBACK`

`LOG_EVENT_PREFLIGHT=CHG0030_ITEM_SYNC_PREFLIGHT_STATUS`

`BACKEND_LOG_OBSERVABILITY_PATCH_READY=true`

`CURRENT_COMPANY_ADAPTER_PASSTHROUGH_READY=false`

The logs include operation/request identity, masked account ID, terminal state, readback counts, duplicate count, and failure reason. They do not include Cookies, Tokens, Authorization values, full account IDs, browser profile data, or item content.

## Selected-Account Eligibility Contract

`SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PATCH_ARTIFACT_ACCEPTANCE_GRADE_NOT_DEPLOYED`

`ELIGIBILITY_FACT_DISABLED=authoritative`

`ELIGIBILITY_FACT_COOKIE_PRESENT=authoritative`

`ELIGIBILITY_FACT_CHECKING=authoritative`

`ELIGIBILITY_FACT_PLATFORM_VERIFICATION=authoritative`

`ELIGIBILITY_FACT_SESSION_COOKIE_LINEAGE=authoritative`

`ELIGIBILITY_FACT_TOKEN_READY=authoritative`

`ELIGIBILITY_UNKNOWN_FAILS_CLOSED=true`

The patched account-status capability returns `item_sync_eligible=true` only when the selected account is enabled, a cookie exists, the bounded checking state is clear, platform verification is authoritatively not required, session-cookie lineage matches the current cookie fingerprint, and token readiness is explicitly true. Missing or incomplete facts return false/UNKNOWN with fail-closed reasons.

## Trace Gate Contract

`TRACE_IDENTITY_AVAILABLE=PATCH_ARTIFACT_ACCEPTANCE_GRADE_NOT_DEPLOYED`

The patched Item Sync route accepts an optional `request_id`, creates an `operation_id` when absent, emits operation-accepted and terminal-readback backend logs, and includes the identity in the synchronous terminal response. Because the current COMPANY adapter strips extension fields, the backend log events are required for first-invocation identity/outcome recovery after deployment.

## Patch Artifact

`PATCH_ARTIFACT=vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch`

`PATCH_ARTIFACT_SHA256=595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201`

`PATCH_ARTIFACT_SCOPE=common/schemas/item.py; backend-web/app/api/routes/cookies.py; backend-web/app/api/routes/items.py; tests/test_chg0030_fresh_item_sync_controlled_canary.py`

## Clean Runtime Replay

`PATCH_REPLAY_TEMP_PATH=D:/xianyu-worktrees/_chg0030_patch_replay2_tmp`

`PATCH_REPLAY_APPLY_CHECK_EXIT=0`

`PATCH_REPLAY_APPLY_EXIT=0`

`PATCH_REPLAY_DIFF_CHECK_EXIT=0`

`PATCH_REPLAY_PY_COMPILE_EXIT=0`

`PATCH_REPLAY_PYTEST=15 passed`

Command:

```powershell
git -C D:/xianyu-worktrees/_chg0030_patch_replay2_tmp apply --check --whitespace=error-all --unidiff-zero vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch
git -C D:/xianyu-worktrees/_chg0030_patch_replay2_tmp apply --whitespace=error-all --unidiff-zero vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch
git -C D:/xianyu-worktrees/_chg0030_patch_replay2_tmp diff --check
python -m py_compile common/schemas/item.py backend-web/app/api/routes/items.py backend-web/app/api/routes/cookies.py
python -m pytest tests/test_chg0028_selected_account_on_demand_capability.py tests/test_chg0030_fresh_item_sync_controlled_canary.py -q
```

Observed result:

```text
APPLY_CHECK_EXIT=0
APPLY_EXIT=0
DIFF_CHECK_EXIT=0
PY_COMPILE_EXIT=0
15 passed in 1.00s
PYTEST_EXIT=0
```

## Operational Gate State

`PRODUCTION_ITEM_SYNC_CANARY_GO=false`

`COMMANDER_GO_RECEIVED=false`

`ITEM_SYNC_INVOCATION_ALLOWED=false`

`DEPLOYMENT_REQUIRED=true`

`BOTH_PRE_CANARY_GATES_TECHNICALLY_SATISFIABLE_AFTER_DEPLOY=true`

The gates are technically satisfiable after backend deployment if the selected account returns authoritative PASS facts and backend container logs or response fields expose the operation identity and terminal durable readback. They are not yet proven in current deployed production, so the canary remains NO-GO.
