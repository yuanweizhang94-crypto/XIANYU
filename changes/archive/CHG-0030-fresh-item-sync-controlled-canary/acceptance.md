# CHG-0030 Acceptance

Change ID: CHG-0030-fresh-item-sync-controlled-canary
Status: ARCHIVED

## Required Acceptance

- CHG-0030 was the only active Change in the isolated worktree before closure and is archived by this closure.
- The Change records the three-line execution contract:
  - User outcome: one controlled Fresh Item Sync canary with terminal and durable-truth proof, then GitHub closure.
  - Confirmed blocker: selected capability and trace identity are not yet explicit.
  - Smallest success test: one selected eligible account, exactly one owner invocation, terminal SUCCESS plus durable xy_catalog_items readback, duplicate 0 and all excluded safety counters 0.
- Existing owner remains `ItemService.fetch_all_items_from_account`.
- Reuse decision is `PATCH_UPSTREAM`.
- Exactly one commander-authorized production Item Sync canary was performed and no further Item Sync invocation is authorized.
- Deterministic CHG-0030 tests pass.

## GitHub Closure

`PR_NUMBER=45`

`PR_URL=https://github.com/yuanweizhang94-crypto/XIANYU/pull/45`

`PR_MERGED=PENDING_NORMAL_MERGE_AFTER_CLOSURE_COMMIT`

`PRE_CLOSURE_HEAD_SHA=9a5005214ef2d72553e4a962a54a045bebe0d18b`

`CLOSURE_COMMIT_SHA=PENDING_THIS_COMMIT_REPORTED_AFTER_COMMIT`

`REMOTE_BRANCH_SHA=PENDING_PUSH_VERIFICATION`

`MERGE_COMMIT_SHA=PENDING_GITHUB_NORMAL_MERGE`

`REMOTE_MAIN_SHA_BEFORE_MERGE_REQUIRED=8d1d1d0fb272cd2715135d077be98ce0b575cb79`

`REMOTE_MAIN_SHA_AFTER_MERGE=PENDING_GITHUB_NORMAL_MERGE`

`SCOPED_CI=PASS`

`LOCAL_ACCEPTANCE=PASS`

`GLOBAL_CI=FAIL_PRE_EXISTING_DEBT`

`GLOBAL_CI_DEBT_ABSORBED=NO`

## Gate State

`SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PASS_POST_DEPLOY_PREFLIGHT_R2`

`TRACE_IDENTITY_AVAILABLE=PASS_BACKEND_LOG_CONTRACT_DEPLOYED_R2`

`SKIPPED_LOCK_SUCCESS_GUARD=DEPLOYED_R2`

`FULL_ACTIVE_LIST_SUCCESS_GUARD=DEPLOYED_R2`

`PRODUCTION_ITEM_SYNC_CANARY_GO=USED_COMPLETE_NO_FURTHER_INVOCATION_ALLOWED`

`COMMANDER_GO_RECEIVED=true`

`ITEM_SYNC_INVOCATION_ALLOWED=false`

`CURRENT_COMPANY_ADAPTER_PASSTHROUGH_READY=false`

`BACKEND_LOG_OBSERVABILITY_PATCH_READY=true`

`PATCH_CLEAN_APPLY_RUNTIME_STACK=true`

`BACKEND_PATCH_DEPLOYED=R2_DEPLOYED`

`SELECTED_ACCOUNT_PREFLIGHT_MASKED=22*********60`

`SELECTED_ACCOUNT_PREFLIGHT_ITEM_SYNC_ELIGIBLE=true`

`SELECTED_ACCOUNT_PREFLIGHT_FAIL_CLOSED=false`

`SELECTED_ACCOUNT_PREFLIGHT_PLATFORM_VERIFICATION_EVIDENCE_TYPE=NONE`

`ONE_CONTROLLED_FRESH_ITEM_SYNC_CANARY=PASS`

`ITEM_SYNC_OPERATION_ID=item_sync_e7ca45174a64408e80b8d72a95d2f37f`

`ITEM_SYNC_SYNC_STATUS=SUCCESS`

`ITEM_SYNC_TERMINAL=true`

`ITEM_SYNC_SKIPPED=false`

`ITEM_SYNC_FULL_ACTIVE_LIST_CONFIRMED=true`

`ITEM_SYNC_DURABLE_READBACK_SOURCE=xy_catalog_items`

`ITEM_SYNC_DURABLE_READBACK_QUERY_SUCCESS=true`

`ITEM_SYNC_DURABLE_READBACK_CHECKED=true`

`ITEM_SYNC_DURABLE_READBACK_RECONCILED=true`

`ITEM_SYNC_DURABLE_READBACK_MATCHED_RESPONSE_ITEM_COUNT=20`

`ITEM_SYNC_DURABLE_READBACK_DUPLICATE_COUNT=0`

`ITEM_SYNC_DURABLE_READBACK_DUPLICATE_ROW_COUNT=0`

## Safety Counters

`ITEM_SYNC_INVOCATION_COUNT=1`

`REMOTE_ITEM_READ_COUNT=1_AUTHORIZED_CANARY`

`LOCAL_ITEM_WRITE_COUNT=20_OWNER_REPORTED_UPSERT_ATTEMPTS`

`REMOTE_LISTING_CREATE_COUNT=0`

`REMOTE_LISTING_EDIT_COUNT=0`

`REMOTE_LISTING_OFFLINE_COUNT=0`

`REMOTE_LISTING_DELETE_COUNT=0`

`REAL_PRODUCTS_PUBLISHED=0`

`REAL_PRODUCTS_MODIFIED=0`

`REAL_MESSAGES_SENT=0`

`BROWSER_INVOCATION_COUNT=0`

`PLAYWRIGHT_CDP_INVOCATION_COUNT=0`

`QR_LOGIN_INVOCATION_COUNT=0`

`MANUAL_RECONNECT_INVOCATION_COUNT=0`

`PRODUCTION_ACCOUNT_MUTATION_COUNT=0`

`PRODUCTION_CONFIG_CHANGE_COUNT=0`

`PRODUCTION_RESTART_COUNT=0`

`DIRTY_CHG0018_TOUCHED=0`

## Stop Acceptance

Stopping after one production canary is accepted while:

- no second Item Sync invocation is authorized.

The selected-account eligibility, Backend log identity, skipped-lock success guard, full-active-list success guard, one controlled Item Sync invocation, terminal `SUCCESS`, and durable-truth readback are satisfied after the Phase 5 controlled production canary. No further invocation is authorized without a separate later commander decision.

## Future Canary Acceptance

Future production canary acceptance requires:

- masked selected account eligibility explicitly PASS before invocation;
- exactly one invocation through `xianyu_item_sync`;
- one trackable identity tied to the request before invocation;
- terminal `SUCCESS`;
- no owner-lock `skipped=true` result may become `SUCCESS` or `durable_readback.checked=true`;
- Fresh Item Sync `SUCCESS` requires `full_active_list_confirmed=true` or an equivalent authoritative complete-list service result;
- actual read-only durable `xy_catalog_items` readback after ItemService returns;
- measured duplicate group count 0 under the real account/item unique contract;
- all excluded safety counters 0;
- no retry after UNKNOWN.

## Upstream Capability Audit

Same as proposal.

## Pinned Upstream Evidence

Same as proposal.

## Existing Local Implementation Search

Same as proposal.

## Reuse Decision

Decision: PATCH_UPSTREAM

## Duplicate Implementation Risk

No second Item Sync owner is accepted.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies Item Sync but not the external canary trace/eligibility gates.

## Approved Exception ADR

Not applicable.

## Component Owner

XIANYU `ItemService.fetch_all_items_from_account`.

## Retirement Plan For Overlapping Local Code

No overlapping local code is introduced.
