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

## Stale SPA entry follow-up

A later user reproduction still showed the old `请先选择账号` toast. Production access logs proved that the browser tab was navigating within the already-loaded SPA and requesting only order APIs; it did not request `/`, `index.html`, the new main entry, or the new Orders chunk after the runtime repair. The server files were correct, but the live tab retained the pre-fix JavaScript execution context.

To prevent the same stale-entry behavior on future frontend updates, `docker/frontend/nginx.conf` now keeps hashed `/assets` immutable while making the SPA entry and route fallback non-cacheable. The running frontend Nginx configuration was updated and reloaded after `nginx -t` passed.

Runtime validation:

- `/` HTTP 200 and references the cache-busted main entry.
- `/index.html` HTTP 200 and is returned with no-cache semantics.
- the served main entry references `Orders-DbMPg1v6-all-sync.js`.
- the served repaired Orders chunk does not contain the `请先选择账号` guard.
- clean follow-up patch apply check: PASS.
- combined order/UI/cache regression tests: 6/6 PASS.

Because an already-executing browser tab cannot be replaced server-side without a real document reload, one browser-level reload is still required for a tab that loaded the old SPA before the deployment. The in-page `刷新` button only reloads order data and does not reload the application JavaScript.

Follow-up artifact:

- Patch: `vendor/patches/xianyu-auto-reply/64c245-chg0018-frontend-spa-no-cache-followup.patch`
- Patch SHA256: `032897E506A8142EC1E24ADDF8F33C26A773301EA41FA6965D72ED06F2398320`
- Patch size: 1978 bytes.
- Changed upstream files:
  - `docker/frontend/nginx.conf`
  - `tests/test_chg0018_frontend_spa_cache.py`
