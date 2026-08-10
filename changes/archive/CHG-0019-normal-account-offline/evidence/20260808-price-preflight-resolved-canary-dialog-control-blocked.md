# CHG-0019 Price Preflight Resolved / Final Canary Dialog Control Blocked

Date: 2026-08-08
Change: CHG-0019-normal-account-offline
Status: IMPLEMENTING

## Authorized target
- ACCOUNT_ID: 2221384086829
- LOCAL_ITEM_ID: 49
- PLATFORM_ITEM_ID: 1070515947040
- Maximum route calls: 1

## Price preflight resolution
- Expected price: 9.90
- Target-item main price DOM raw: 9.90 (container text also renders as `¥ 9.90 包邮`)
- Normalized page price: 9.90
- Local cached price: ¥9.90
- Normalized local price: 9.90
- Classification: WRONG_PRICE_SELECTOR
- Root cause: the previous generic read could be polluted by whitespace/componentized currency rendering and many recommendation-card prices. The target item main-info price selector is unique and numerically matches.
- No business source change or Backend rebuild was required.

## Strong identity gate
- SESSION_HEALTHY=true
- TARGET_ITEM_MATCHED=true
- TITLE_MATCHED=true
- UNIQUE_OFFSHELF_CONTROL_FOUND=true
- AMBIGUOUS_OFFSHELF_CONTROL=false
- ALREADY_OFFSHELF_CONFIRMED=false

## Single real route call
- REAL_OFFSHELF_ROUTE_CALLS=1
- INITIAL_OFFSHELF_CLICK_PERFORMED=true
- Dialog local text captured: `确定要下架这个宝贝吗？ 取消 确定`
- The deployed classifier found no semantic `button` / `[role=button]` controls inside the live dialog even though its local text contains `取消` and `确定`.
- CONFIRM_DIALOG_REQUIRED=true
- CONFIRM_DIALOG_SAFE=false
- CONFIRM_BUTTON_CLICKED=false
- Route result: `unsafe_or_ambiguous_offline_confirmation`

## Post-action read-only verification
- Target page remained authenticated and matched.
- `下架` remained present.
- No `上架` / `重新上架` / `已下架` evidence was present.
- No success text was present.
- PLATFORM_OFFSHELF_CONFIRMED=false
- Post-success item sync was not performed.
- ITEM_STATUS_BEFORE=-9
- ITEM_STATUS_AFTER=-9

## Safety counters
- OLD_PC_SELLER_API_CALLS=0
- OTHER_ITEM_PRODUCT_ACTIONS=0
- OTHER_ACCOUNT_PRODUCT_ACTIONS=0
- PRODUCTS_DELETED=0
- PRODUCTS_PUBLISHED=0
- PRODUCTS_RELISTED=0
- POLISH_REQUESTS=0
- GIT_COMMIT_CREATED=false
- GIT_PUSH_PERFORMED=false
- GITHUB_WRITES=0
- PR26_CHANGED=false

## Blocker
`LIVE_DIALOG_CONFIRM_CONTROLS_ARE_NON_SEMANTIC_FOR_CURRENT_SELECTOR`

The current task prohibited changing the confirmation classifier and prohibited a second route call, so execution stopped fail-closed.
