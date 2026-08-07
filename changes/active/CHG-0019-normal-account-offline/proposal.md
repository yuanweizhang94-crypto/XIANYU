# CHG-0019 Normal Account Offline

Status: VERIFYING

Change ID: CHG-0019-normal-account-offline

## Execution contract

User outcome: make the existing `/items/batch-offline` operation safely take a normal Xianyu account's own item off sale through the official normal Web UI, then prove it on one owner-authorized fixed item.

Confirmed blocker: the existing backend defaults to `mtop.alibaba.idle.seller.pc.item.batch.offline`, but the fixed normal account is rejected by `seller.goofish.com` with `#/no-permission`; the same healthy session can access its own `www.goofish.com/item?id=<item_id>` detail page where owner controls include `下架` and `删除`.

Smallest success test: preserve the external batch-offline route and old PC Seller service, reuse the existing XianyuPublisher/Playwright/Cookie lifecycle, fail closed unless exactly one safe owner `下架` control is identified, then complete one real off-shelf canary for platform item `1070515947040` with no other product action.

## Scope

ROOT_CAUSE=CURRENT_BACKEND_USES_WRONG_PC_SELLER_OFFSHELF_API

- Keep `POST /items/batch-offline` compatible.
- Make the default execution for this route use the existing normal-Web Playwright publisher/browser lifecycle.
- Open `https://www.goofish.com/item?id=<item_id>` and verify the current item's owner-operation context before any click.
- Execute only a unique, visible, enabled `下架` owner control; never match or substitute `删除`.
- If a confirmation dialog appears, accept it only when the dialog and confirmation action are explicitly off-shelf semantics and contain no delete semantics.
- Determine success from explicit platform UI state: success toast and/or transition from `下架` to `上架`/`重新上架`; browser click success alone is insufficient.
- Batch results remain independent per item and preserve `success`, `message`, `suc_count`, `fail_count`, `results`, and `cookies_str` compatibility.
- Preserve the old PC Seller MTop service source for future account types, but do not use it as the default route in this Change.
- Real canary is limited to ACCOUNT_ID `2221384086829`, LOCAL_ITEM_ID `49`, PLATFORM_ITEM_ID `1070515947040`.

## Upstream capability audit

Pinned upstream and current upstream were previously audited for `offline`, `batch-offline`, `下架`, `seller.pc.item`, and item detail behavior. The pinned implementation provides `common/services/item_offline_service.py` using the PC Seller API; it does not provide a normal-account Web off-shelf executor. The existing publisher already owns normal-Web Playwright, Cookie injection, item-detail navigation after publish, browser lifecycle, and detection of `下架`/`删除` owner controls.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`. Evidence paths: `common/services/item_offline_service.py`, `backend-web/app/api/routes/items.py`, `backend-web/app/services/xianyu_publisher.py`, `common/services/promotion_xianyu_publisher.py`. Runtime evidence: the fixed account receives `FAIL_BIZ_IDLE_USER_UNAUTHORIZED` from the PC Seller batch-offline API and `seller.goofish.com` resolves to `#/no-permission`, while `www.goofish.com/item?id=1070515947040` is accessible with matching title/price and owner controls `下架,删除`. Official normal-Web bundle `idle-pc/xy-site/0.0.172/js/p_item-index.js` contains `mtop.taobao.idle.item.downshelf`, but this Change intentionally does not reimplement that MTop contract.

## Existing local implementation search

The repository and pinned upstream were searched for normal item detail, item_url, delete, off-shelf, publisher, browser lifecycle, Cookie injection, and batch-offline code. Existing `XianyuPublisher` is the reusable browser execution owner. No second browser service, alternate normal-account off-shelf service, or safe already-wired normal Web off-shelf method exists.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The main risk is creating a second browser/Cookie/session executor. The patch must extend the existing XianyuPublisher path and keep the existing HTTP route; it must not create another browser manager, Cookie manager, login system, queue, worker, table, or route family.

## Why upstream cannot satisfy the requirement

The pinned upstream's formal backend off-shelf path assumes PC Seller authorization that the fixed normal account does not possess. The normal Web UI does expose the owner's `下架` capability, but the upstream backend does not currently connect `/items/batch-offline` to that existing normal-Web browser context.

## Approved exception ADR

Not applicable. This is a minimal patch to existing upstream-native publisher/browser and item route ownership, not a local replacement capability.

## Component owner

Existing backend `/items/batch-offline` route plus existing `XianyuPublisher` Playwright lifecycle remain the execution owners.

## Retirement plan for overlapping local code

No overlapping runtime is added. If upstream later exposes a verified normal-account off-shelf method or fully documented `mtop.taobao.idle.item.downshelf` contract, this UI patch should be reviewed for retirement in favor of that upstream-native method.

## Forbidden work

No delete, publish, relist, edit, polish, other account/item operation, automatic login, QR scan, database/Redis manual write, new browser system, GitHub write, PR #26 change, CHG-0018 production rollback, or modification of CHG-0018 business code/Vendor Patch.
