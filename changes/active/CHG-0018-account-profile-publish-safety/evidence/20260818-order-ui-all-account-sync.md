# 2026-08-18 Order UI all-account sync recovery

## Execution contract

- User outcome: restore the Order Management page so `获取闲鱼订单` can synchronize all enabled accounts when no account is selected, while still allowing an optional single-account sync.
- Confirmed blockers: the running Backend container still used the pre-fix sold-order `COMMONPRO` request header, and the current Orders UI added a local guard that returned `请先选择账号` before calling the Backend's existing all-account path.
- Smallest success test: remove only the UI guard, keep `fetchXianyuOrders(selectedAccount || undefined)`, deploy the matching runtime bundle, load the fixed sold-order header in Backend, then prove the recovered account can synchronize through the Backend runtime with no order errors.

## Upstream-first / existing-path decision

- Decision: `PATCH_UPSTREAM` / restore existing native route semantics; no new order API, crawler, model, worker, or scheduler was created.
- Existing Backend contract already supports the desired behavior:
  - `FetchXianyuOrdersRequest.cookie_id` defaults to `None`.
  - when `request.cookie_id` is omitted, `/orders/fetch-xianyu` calls `account_service.list_accounts(owner_id)` and synchronizes all non-inactive accounts.
- The frontend guard was therefore redundant and blocked a capability that the existing Backend route already owned.
- The account selector remains a filter and optional single-account sync selector; it is no longer a prerequisite for synchronization.

## Runtime defect confirmed from the reported UI error

The Order Management page reported a partial synchronization error for account `2214313339860` with `PERMISSION_EXCEPTION`.

Inspection showed the live Backend container had not received the already-proven sold-order permission fix:

- live Backend sold-order request still forced `idle_site_biz_code: COMMONPRO`;
- live Backend Referer was still the older seller root form;
- the repaired source/Scheduler path did not force the business header and had already proven native order success.

The Backend runtime was patched to the same proven sold-order request semantics and restarted. Health returned HTTP 200.

## UI repair

`frontend/src/pages/orders/Orders.tsx` now preserves the existing API call:

- selected account -> synchronize that account;
- no selected account -> pass `undefined`, which the API adapter serializes as `cookie_id: null`, activating the Backend's existing all-enabled-account synchronization path.

The local `请先选择账号` warning/return guard was removed.

To avoid deploying unrelated dirty frontend source, the current production bundle was patched narrowly and cache-busted:

- a new Orders chunk was created from the currently served chunk with only the selection guard removed;
- a new main entry references the new Orders chunk;
- `index.html` references the new main entry, so a normal page refresh loads the repaired behavior despite one-year immutable asset caching.

No other frontend route or feature was rebuilt as part of this runtime repair.

## Validation

- Frontend source regression tests: 4/4 PASS.
- Clean incremental patch apply check: PASS with `--whitespace=error-all --unidiff-zero`.
- Clean post-apply regression tests: 4/4 PASS.
- `python scripts/verify_repository.py` was executed in the formal repository and stopped only on the pre-existing `tmp/publish_restore/...` sensitive-pattern findings already present before this repair; no order-UI recovery file was reported by that scan.
- Production frontend HTTP 200.
- Production `index.html` references the new main entry.
- New main entry references the new Orders chunk.
- New Orders chunk contains no `请先选择账号` guard and retains the optional-account fetch call.
- Production Backend health: HTTP 200 after targeted restart.
- Production Backend `OrderService` for recovered account `2214313339860`: `total_fetched=1`, `failed=0`, `errors=[]`.

## Current expected UI behavior

- If `筛选账号=所有账号`, clicking `获取闲鱼订单` processes all currently enabled accounts.
- If one account is selected, the same button processes only that account.
- Accounts whose Seller Session has not yet been restored may still appear in the all-account result as explicit per-account failures. That is expected and must not be hidden as success.
- The already restored `2214313339860` account no longer produces the prior `PERMISSION_EXCEPTION` on the repaired Backend path.

## Artifact

- Patch: `vendor/patches/xianyu-auto-reply/64c245-chg0018-order-ui-all-account-sync.patch`
- Patch SHA256: `E223A29F6257B5EC2758D0D23AA4A7AECD9401E83A6DD063854C1DACDD29ACE4`
- Patch size: 2066 bytes.
- Changed upstream files recorded by the patch:
  - `frontend/src/pages/orders/Orders.tsx`
  - `tests/test_chg0018_order_sold_permission_header.py`
- New order engine created: false.
- Customer messages sent: 0.
- Products changed: 0.
