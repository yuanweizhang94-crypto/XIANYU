# CHG-0030 Design

Change ID: CHG-0030-fresh-item-sync-controlled-canary
Status: IMPLEMENTING

## Design Intent

Prepare a controlled Fresh Item Sync canary without invoking Item Sync. The design accepts the existing XIANYU owner and adds only deterministic governance/evidence locks until the canary can be explicitly authorized.

## Execution Order

1. CURRENT_GITHUB: fetch `origin/main` without changing `origin`, verify SHA, target path absence, branch absence, and new worktree base.
2. ACTIVE_RECORD: create this active Change with the three-line execution contract and upstream-first fields.
3. EXISTING_OWNER: map Item Sync to the existing upstream/XIANYU owner and CHG-0024 safe-mode record.
4. COMPANY_ADAPTER: inspect tool schema and implementation without invoking Item Sync.
5. GATES: classify selected-account Item Sync eligibility and trace identity as PASS or blocked.
6. TESTS: run CHG-0030 acceptance tests, change validation, project context, and `git diff --check`.
7. STOP_OR_GO_REPORT: report whether a production canary can safely receive commander GO.

## Canary Gate Contract

Gate 1: selected-account Item Sync eligibility must be explicit PASS for the masked target account before invocation.

Gate 2: the one invocation must have a trackable request/task/trace identity available before invocation.

Current gate state:

```text
SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PASS_POST_DEPLOY_PREFLIGHT_R1_RECHECK_REQUIRED_AFTER_R2
TRACE_IDENTITY_AVAILABLE=PASS_BACKEND_LOG_CONTRACT_DEPLOYED_R1_RECHECK_REQUIRED_AFTER_R2
SKIPPED_LOCK_SUCCESS_GUARD=PATCH_READY_NOT_DEPLOYED
FULL_ACTIVE_LIST_SUCCESS_GUARD=PATCH_READY_NOT_DEPLOYED
PRODUCTION_ITEM_SYNC_CANARY_GO=false
```

## Existing Owner Contract

The only accepted canary owner chain is:

```text
COMPANY xianyu_item_sync
-> POST /api/v1/items/get-all-from-account?no_auth_recovery=true
-> ItemService.fetch_all_items_from_account
-> _fetch_all_items_from_account_impl
-> ItemInfoManager.get_item_list_info
-> save_fetched_items
-> actual read-only xy_catalog_items post-service durable readback
```

No manual remote-read plus local write sequence may replace this owner.

## Deterministic Evidence Design

The active evidence locks:

- remote-main SHA and worktree cleanliness;
- dirty CHG-0018 worktree read-only boundary;
- pinned upstream SHA and owner paths;
- COMPANY schema fields and live/runtime source hash metadata;
- absence of `task_id`, `request_id`, `trace_id`, and `operation_id` from `xianyu_item_sync`;
- absence of explicit selected-account Item Sync eligibility from `xianyu_account_status`;
- CHG-0030 backend structured log events for accepted operation, terminal durable readback, and selected-account preflight status;
- real post-service `xy_catalog_items` row and duplicate-group queries under the existing unique account/item contract;
- zero safety counters and NO-GO canary state.

## Tests

Focused tests read only repository-controlled CHG-0030 records and verify:

- active Change identity/status and execution contract;
- upstream-first fields and ADOPT_UPSTREAM decision;
- owner uniqueness and forbidden side effects;
- selected-account eligibility and trace identity gates remain unresolved;
- production canary GO remains false;
- generated project state points to CHG-0030 while active.

Source-artifact tests verify the vendor patch itself:

- selected account preflight returns explicit `item_sync_eligible`, `fail_closed`, and deterministic false/unknown reasons from disabled, checking, platform-verification, session-cookie-lineage, and token-ready facts;
- Item Sync route responses return `operation_id`, `request_id`, `sync_status`, `terminal`, `retry_allowed=false`, and `durable_readback`;
- durable readback performs actual read-only `xy_catalog_items` queries, measures duplicate groups, reconciles response item IDs, and fails terminal UNKNOWN with `retry_allowed=false` on query failure or unknown reconciliation;
- structured backend log events expose the first invocation identity/outcome even when the current COMPANY adapter strips extension response fields;
- no second service, data owner, queue, scheduler, crawler, UI, Browser/CDP path, or lifecycle owner is introduced.
- Phase 4b follow-up tests prove an owner Redis-lock `skipped=true` result cannot become `SUCCESS` or `durable_readback.checked=true`;
- Fresh Item Sync `SUCCESS` requires `full_active_list_confirmed=true`, so a capped or incomplete result fails closed as terminal `UNKNOWN`;
- selected-account preflight exposes sanitized `platform_verification_evidence_type` so `source=none` is only accepted as authoritative when the classifier supplies an evidence type with `required=false`.

## Rollback

Before commit, rollback is deletion of this active Change record, its evidence, tests, and generated state refresh from the isolated CHG-0030 worktree only. After r1 deployment, rollback is deterministic restoration of the preserved CHG-0029 or r1 Backend image depending on whether the r2 follow-up deployment is the failure point. No database, account state, adapter runtime, WebSocket, Scheduler, Frontend, or `D:/xianyu` dirty worktree state is modified.

## Upstream Capability Audit

Same as proposal. Pinned upstream supplies the Item Sync owner and local catalog write path.

## Pinned Upstream Evidence

Same as proposal. Evidence is pinned to `D:/xianyu-upstream-pilot` at `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.

## Existing Local Implementation Search

Same as proposal. CHG-0024 is the local implementation record for safe-mode Item Sync ownership.

## Reuse Decision

Decision: PATCH_UPSTREAM

## Duplicate Implementation Risk

No second Item Sync owner may be added. Any future adapter traceability patch must pass through XIANYU truth and must not own business truth.

## Why Upstream Cannot Satisfy The Requirement

Upstream does not provide ChatGPT/COMPANY canary trace identity, actual terminal durable-readback contract, measured duplicate count, or explicit selected-account Item Sync eligibility without the CHG-0030 backend contract patch.

## Approved Exception ADR

Not applicable.

## Component Owner

XIANYU `ItemService.fetch_all_items_from_account` remains the owner.

## Retirement Plan For Overlapping Local Code

No overlapping local implementation is introduced.
