# CHG-0030 Fresh Item Sync Controlled Canary And Closure

Change ID: CHG-0030-fresh-item-sync-controlled-canary
Status: IMPLEMENTING
Created: 2026-08-25
Owner task: chg0030_single_writer

## User Outcome

User outcome: one controlled Fresh Item Sync canary with terminal and durable-truth proof, then GitHub closure.

Confirmed blocker: selected capability and trace identity are not yet explicit.

Smallest success test: one selected eligible account, exactly one owner invocation, terminal SUCCESS plus durable xy_catalog_items readback, duplicate 0 and all excluded safety counters 0.

## Scope

Allowed scope:

- read-only fingerprinting of `D:/xianyu` dirty CHG-0018 worktree;
- isolated worktree development under `D:/xianyu-worktrees/CHG-0030-fresh-item-sync-controlled-canary`;
- current remote-main and pinned-upstream evidence;
- read-only COMPANY adapter/tool contract inspection;
- read-only sanitized auth/capability path inspection;
- deterministic CHG-0030 governance/evidence tests;
- Git diff and focused validation.

Forbidden scope:

- Item Sync invocation before a later explicit commander GO;
- Browser, UI, CDP, Playwright, QR, reconnect, account mutation, restart, production config change, retry, publish, edit, offline, delete, or message send;
- second Item Sync owner, crawler, scheduler, worker, manual pagination-plus-upsert bypass, Session owner, Cookie owner, Token owner, or COMPANY-side business truth source;
- printing full account IDs, secrets, Cookies, Tokens, Authorization values, Profiles, or customer-sensitive content;
- modifying the dirty `D:/xianyu` CHG-0018 worktree.

## Current Decision

PRODUCTION_ITEM_SYNC_CANARY_GO=false

NO_GO_REASON=ACCEPTANCE_GRADE_PATCH_ARTIFACT_NOT_DEPLOYED_AND_COMMANDER_GO_MISSING

The production canary remains blocked until the CHG-0030 XIANYU patch is deployed through the existing runtime path, the selected account preflight returns explicit PASS from authoritative backend facts, the one invocation identity and terminal durable-readback outcome are recoverable from backend structured logs or response fields, and the commander sends a later explicit GO message.

## Upstream Capability Audit

Pinned upstream `D:/xianyu-upstream-pilot` contains the native account-scoped Item Sync route and service:

```text
POST /api/v1/items/get-all-from-account
-> ItemService.fetch_all_items_from_account
-> Redis item_sync:{account_id} lock
-> _fetch_all_items_from_account_impl
-> ItemInfoManager.get_item_list_info(page)
-> save_fetched_items
-> local xy_catalog_items write/read truth
```

No upstream-native publish, edit, offline, delete, message, Browser, QR, reconnect, or account-mutation owner is part of this path.

## Pinned Upstream Evidence

Pinned upstream checkout: `D:/xianyu-upstream-pilot`

Pinned upstream SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`

Evidence paths:

- `backend-web/app/api/routes/items.py`
- `common/services/item_service.py`
- `common/utils/item_info_manager.py`
- `common/models/xy_catalog_item.py`

Current GitHub authority for this Change starts from `origin/main=8d1d1d0fb272cd2715135d077be98ce0b575cb79`, which includes closed CHG-0028 and CHG-0029.

## Existing Local Implementation Search

Existing local record CHG-0024 identifies the sole full-account Item Sync owner as `ItemService.fetch_all_items_from_account` and rejects the single-page primitive as a full-sync replacement. Existing CHG-0024 evidence also records the COMPANY `xianyu_item_sync` thin adapter as the trusted safe-mode caller that should force `no_auth_recovery=true` without exposing lifecycle controls to the public caller.

Current read-only adapter inspection found:

- live adapter schema for `xianyu_item_sync` exposes only `account_id`, `page_size`, and `max_pages`;
- live adapter implementation calls `/api/v1/items/get-all-from-account?no_auth_recovery=true`;
- no public or internal `task_id`, `request_id`, `trace_id`, `operation_id`, or status lookup was found for `xianyu_item_sync`;
- current COMPANY adapter summaries strip backend operation/capability extension fields, so CHG-0030 observability cannot depend only on adapter response pass-through;
- read-only `xianyu_account_status` can check account visibility/login fields but is not an explicit Item Sync eligibility contract.
- the authoritative ChatGPT-facing adapter source is a separate dirty COMPANY checkout and is not modified by CHG-0030.

## Reuse Decision

Decision: PATCH_UPSTREAM

The single Item Sync owner remains existing upstream/XIANYU `ItemService.fetch_all_items_from_account`. CHG-0030 packages a minimal vendor patch over the existing XIANYU backend route/account-status contract so selected-account preflight, structured operation logs, and real post-service durable readback can be supplied by XIANYU without creating a second owner.

## Duplicate Implementation Risk

Risk is low while CHG-0030 stays an evidence and controlled-canary gate around the existing owner. Risk becomes high if a second item crawler, manual pagination-plus-upsert script, Scheduler/worker, DB writer, Session/Cookie/Token lifecycle owner, or COMPANY-side Item Sync truth model is introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the Item Sync business owner, but it does not supply the external canary-control proof needed here: explicit selected-account Item Sync eligibility, one-invocation identity, terminal structured log recovery, measured duplicate groups, and actual `xy_catalog_items` readback. A minimal patch to existing backend route/account-status contracts is required; production remains NO-GO until the patch is deployed and the pre-canary gates are proven on the selected account.

## Approved Exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not authorized.

## Component Owner

The Item Sync business owner remains XIANYU `ItemService.fetch_all_items_from_account`. COMPANY remains a thin transport adapter only. CHG-0030 owns only canary governance, evidence, and closure tracking.

## Retirement Plan For Overlapping Local Code

No overlapping local code is added. Any future adapter traceability patch must remain a thin operations contract and be retired if upstream or COMPANY later provides an equivalent native status identity.
