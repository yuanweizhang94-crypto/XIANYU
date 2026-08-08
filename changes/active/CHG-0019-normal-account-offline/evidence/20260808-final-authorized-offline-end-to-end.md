# CHG-0019 Final Authorized Off-shelf End-to-End

Date: 2026-08-08
Change: CHG-0019-normal-account-offline
Authorized account: `2221384086829`
Authorized local item: `49`
Authorized platform item: `1070515947040`

## Preflight

The production Backend was already deployed as `xianyu-chg0019-backend-web:44c8ae9-nonsemantic-confirm`.

Read-only preflight passed without Cookie renewal, Token bootstrap, QR scan, login recovery, source modification, image rebuild, or redeployment:

- SESSION_HEALTHY_INITIAL=true
- TARGET_ITEM_MATCHED=true
- TITLE_MATCHED=true
- OWNER_ITEM_CONTEXT_CONFIRMED=true
- PAGE_CURRENT_PRICE=9.90 (auxiliary only)
- ALREADY_OFFSHELF_CONFIRMED=false
- UNIQUE_OFFSHELF_CONTROL_FOUND=true
- AMBIGUOUS_OFFSHELF_CONTROL=false
- ITEM_STATUS_BEFORE=-9

The owner context contained the expected separate `下架` and `删除` controls. Only the unique `下架` control was eligible.

## Single authorized transaction

Exactly one call entered the deployed `POST /items/batch-offline` route logic for only platform item `1070515947040` and account `2221384086829`.

Execution path:

`/items/batch-offline -> offline_items_normal_web -> XianyuPublisher.offline_item -> www.goofish.com/item?id=1070515947040`

The old PC Seller API was not called.

Runtime evidence from the single transaction:

- REAL_OFFSHELF_ROUTE_CALLS=1
- INITIAL_OFFSHELF_CLICK_PERFORMED=true
- CONFIRM_DIALOG_REQUIRED=true
- CONFIRM_DIALOG_TEXT=`确定要下架这个宝贝吗？ 取消 确定`
- CONFIRM_DIALOG_BUTTONS=`取消;确定`
- CONFIRM_DIALOG_SAFE=true
- CONFIRM_CONTROL_TEXT=`确定`
- CONFIRM_BUTTON_CLICKED=true
- detailed UI action count=2 (`下架` + same-transaction `确定`)
- OFFSHELF_ROUTE_SUCCESS=true
- OFFSHELF_UI_SUCCESS=true

The dialog-local classifier accepted the unique positive `确定` control only after confirming down-shelf semantics, an escape control, no delete/dangerous semantics, exact-text matching, leaf-most deduplication, visibility, and overlay safety.

## Platform confirmation

The in-transaction and independent post-action read-only checks produced explicit platform state evidence:

- `下架` control no longer present
- page contains `已下架`
- no route retry was performed

The transient `下架成功` toast was not present when the post-state snapshots were read, but explicit `已下架` page state is sufficient platform confirmation under the acceptance rule.

Therefore:

- PLATFORM_OFFSHELF_CONFIRMED=true
- REAL_OFFSHELF_CANARY_SUCCESS=true

## Existing post-success sync

Because platform success was explicit, exactly one existing item synchronization was executed through `ItemService.fetch_all_items_from_account`.

Result:

- OFFSHELF_POST_SYNC_PERFORMED=true
- OFFSHELF_POST_SYNC_CONFIRMED=true
- sync success=true
- total_count=6
- saved_count=6
- ITEM_STATUS_AFTER=-9

The local cached status remained `-9`. Per the acceptance contract, stale local cache does not negate explicit platform UI confirmation. No manual database or Redis status write was performed.

## Safety/action counters

- OTHER_ITEM_PRODUCT_ACTIONS=0
- OTHER_ACCOUNT_PRODUCT_ACTIONS=0
- PRODUCTS_DELETED=0
- PRODUCTS_PUBLISHED=0
- PRODUCTS_RELISTED=0
- POLISH_REQUESTS=0
- OLD_PC_SELLER_API_CALLS=0
- GIT_COMMIT_CREATED=false
- GIT_PUSH_PERFORMED=false
- GITHUB_WRITES=0
- PR26_CHANGED=false

## Outcome

The CHG-0019 implementation and owner-authorized real normal-account off-shelf canary are complete. Evidence supports transition from `IMPLEMENTING` to `VERIFYING` for local verification/closeout. This does not authorize commit, push, GitHub write, PR #26 modification, or any additional real product action.
