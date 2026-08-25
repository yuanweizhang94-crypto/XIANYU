# CHG-0030 Acceptance

Change ID: CHG-0030-fresh-item-sync-controlled-canary
Status: IMPLEMENTING

## Required Acceptance

- CHG-0030 is the only active Change in the isolated worktree.
- The active Change records the three-line execution contract:
  - User outcome: one controlled Fresh Item Sync canary with terminal and durable-truth proof, then GitHub closure.
  - Confirmed blocker: selected capability and trace identity are not yet explicit.
  - Smallest success test: one selected eligible account, exactly one owner invocation, terminal SUCCESS plus durable xy_catalog_items readback, duplicate 0 and all excluded safety counters 0.
- Existing owner remains `ItemService.fetch_all_items_from_account`.
- Reuse decision is `PATCH_UPSTREAM`.
- No production Item Sync invocation is accepted until both unresolved gates are PASS and a later explicit commander GO is received.
- Deterministic CHG-0030 tests pass.

## Gate State

`SELECTED_ACCOUNT_ITEM_SYNC_ELIGIBILITY=PATCH_ARTIFACT_ACCEPTANCE_GRADE_NOT_DEPLOYED`

`TRACE_IDENTITY_AVAILABLE=PATCH_ARTIFACT_ACCEPTANCE_GRADE_NOT_DEPLOYED`

`PRODUCTION_ITEM_SYNC_CANARY_GO=false`

`COMMANDER_GO_RECEIVED=false`

`ITEM_SYNC_INVOCATION_ALLOWED=false`

`CURRENT_COMPANY_ADAPTER_PASSTHROUGH_READY=false`

`BACKEND_LOG_OBSERVABILITY_PATCH_READY=true`

`PATCH_CLEAN_APPLY_RUNTIME_STACK=true`

## Safety Counters

`ITEM_SYNC_INVOCATION_COUNT=0`

`REMOTE_ITEM_READ_COUNT=0`

`LOCAL_ITEM_WRITE_COUNT=0`

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

Stopping before production canary is accepted while:

- selected-account Item Sync eligibility is not explicit PASS in current deployed runtime;
- trace identity and terminal durable-readback outcome are not yet available in current deployed runtime logs or response fields for exactly one invocation;
- no later explicit commander GO has been received.

## Future Canary Acceptance

Future production canary acceptance requires:

- masked selected account eligibility explicitly PASS before invocation;
- exactly one invocation through `xianyu_item_sync`;
- one trackable identity tied to the request before invocation;
- terminal `SUCCESS`;
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
