# CHG-0019 Design

Status: ARCHIVED

Change ID: CHG-0019-normal-account-offline

## Design

Patch the existing backend off-shelf execution boundary without changing its public route. The route continues to resolve the selected account and pass its authoritative Cookie plus item IDs. The implementation processes item IDs one at a time through the existing `XianyuPublisher` browser lifecycle.

For each item, the normal-Web off-shelf method opens `https://www.goofish.com/` for Cookie initialization and then the deterministic detail URL `https://www.goofish.com/item?id=<item_id>`. It fails closed on login/auth/verification pages, item mismatch, missing owner-action context, missing off-shelf control, multiple plausible off-shelf controls, browser errors, or ambiguous confirmation semantics.

The off-shelf control resolver must inspect visible actionable elements and their local owner-operation container. It must accept exactly one enabled control whose normalized action text is exactly an approved off-shelf phrase, and must reject any candidate/container/dialog containing delete semantics. A generic `text=下架` first-match click is forbidden.

After the initial off-shelf click, if a modal/dialog is present, confirmation is permitted only when the dialog contains explicit off-shelf semantics and no delete semantics, and exactly one safe enabled confirmation action is found.

Success requires an explicit UI outcome: an off-shelf-success toast/message or owner action state changing so `下架` is gone and `上架`/`重新上架` is visible. The result for every item is independent. Browser exceptions and unknown state return failure.

The old `mtop.alibaba.idle.seller.pc.item.batch.offline` implementation remains in source but is no longer the default path for `/items/batch-offline` during this Change. No direct implementation of `mtop.taobao.idle.item.downshelf` is added because its full signing/body/header contract is not yet approved.

Initial mutation deployment scope is backend only if source/deployment inspection confirms the route and publisher are both served by the backend image. MySQL, Redis, Scheduler, and WebSocket are not restarted.

## Formal frontend delivery design

The product-management frontend reuses the existing `batchOfflineItems()` wrapper and existing checkbox/batch selection, `ConfirmModal`, Toast, and `loadItems()` refresh infrastructure. The missing row-level single-item entry is added without creating another route or API client.

Single-item and batch off-shelf actions require an explicit project confirmation stating that off-shelf does not delete the item. Single-item requests use the row item's authoritative `cookie_id` and platform `item_id`. Batch requests preserve the existing explicit single-account filter design; cross-account selections fail closed rather than being regrouped implicitly.

Frontend request state is locked per item and per batch to prevent double submission. Response interpretation uses `success`, `message`, and `data.results/suc_count/fail_count`, never `cookies_str`. Success refreshes the item list. Because the local catalog does not persist an authoritative platform sale status, a successful item that remains visible is marked `已下架` only in current page-session state and cannot be re-submitted; `item_status=-9` is never inferred as off-shelf.

Frontend mutation wiring is verified with intercepted synthetic requests against actual deployed assets. Production smoke opens the project confirmation and cancels, with real `/items/batch-offline` forwarding required to remain zero. A repeated live platform mutation is intentionally excluded because the Backend real canary already proved the executor.

## Archive closeout

The verified implementation is preserved through the current CHG-0017 → CHG-0018 T12 → CHG-0019 main-integration Vendor Patch chain. Archive closeout changes governance state only and does not alter runtime design or execute another live mutation.
