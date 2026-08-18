# 2026-08-18 Seller order permission repair and no-scan recovery evidence

## Execution contract

- User outcome: restore native seller-order synchronization and first exhaust existing no-scan Session recovery before requiring any manual login.
- Confirmed blocker: the sold-order MTOP request hard-coded `idle_site_biz_code: COMMONPRO`, which causes ordinary seller accounts to receive `PERMISSION_EXCEPTION`; several other accounts also have genuinely expired seller browser Sessions.
- Smallest success test: on one currently healthy account, prove the same Cookie can access another merchant API, reproduce sold-order permission failure, remove only the unsupported business-code header, obtain native sold-order SUCCESS, and synchronize the result through the formal `OrderService`.

## Upstream-first / existing-owner decision

- Decision: `PATCH_UPSTREAM` on the existing `common/services/order_service.py` request path.
- No new order API, crawler, model, queue, worker, Scheduler owner, Session owner, or login implementation is introduced.
- `OrderService`, native MTOP signing, existing Scheduler tasks, `xy_orders`, and `/api/v1/orders` remain the sole order path.

## No-scan Session recovery investigation

All six active production accounts were checked through the existing XIANYU account/WebSocket status path. They remained enabled and online; no account was auto-disabled by this repair.

The existing Chat connect path was reused first. Several accounts reconnected without QR, proving Chat connectivity alone is not equivalent to seller-order Session readiness.

Three stale `auto_reply_platform_verification` metadata markers were found on accounts whose current authoritative WebSocket runtime explicitly reported connected Token success with `platform_verification_required=false`. Only those stale markers were cleared; no Cookie value was cleared or replaced.

Canonical Profile Session maintenance results:

- `2214313339860`: `REAL_BROWSER_LOGIN_READY`, no QR, no PVR. This account recovered without scanning.
- `2217936413500`: `HUMAN_QR_REQUIRED`, login UI and QR visible after bounded native maintenance.
- `2858469041`: `HUMAN_QR_REQUIRED`, login UI and QR visible after bounded native maintenance.
- `1034641456` and `2196106636`: canonical Profile checks showed login/QR UI.
- `2219319284219`: an old Chrome Singleton owner was proven to belong to an exited historical WebSocket container (`running=false`, PID 0). Only the three stale Singleton files were removed; after that, canonical maintenance still showed real QR/login UI.

The upstream-native browser `快速进入` recovery path was then tried without credentials or CAPTCHA automation:

- `1034641456`: no quick-enter button and no logged-in signal.
- `2196106636`: no quick-enter button and no logged-in signal.
- `2219319284219`: no quick-enter button and no logged-in signal.
- `2858469041`: no quick-enter button and no logged-in signal.
- `2217936413500`: native quick-enter helper encountered an invalid-cookie-field compatibility error, while authoritative Session maintenance had already independently confirmed real QR/login UI.

Therefore one account was recoverable without QR; the other five have no remaining proven existing no-scan seller Session path at this point.

## Sold-order permission root cause

After `2214313339860` reached `REAL_BROWSER_LOGIN_READY`, the native sold-order call still returned:

`PERMISSION_EXCEPTION::无权限访问`

This was not an account-wide seller permission failure:

- the same account successfully synchronized 8 active items through XIANYU ItemService;
- the same account and same stored Cookie successfully called the existing seller merchant-rate list API and returned one real result.

The sold-order request contained a locally hard-coded header:

`idle_site_biz_code: COMMONPRO`

Controlled read-only request comparison with the same account, Cookie, API, signature, body and page:

1. Keep `idle_site_biz_code: COMMONPRO` while adding normal Seller Origin/Referer: still `PERMISSION_EXCEPTION`.
2. Remove only the forced business-code header and use the normal Seller Origin/Referer: `SUCCESS::调用成功`, one item, total count one.

This proves the forced `COMMONPRO` business-code header was the permission regression for the sold-order endpoint.

## Repair

In `common/services/order_service.py`, only `_fetch_sold_orders_page` was changed:

- remove `idle_site_biz_code: COMMONPRO`;
- set `Referer` to `https://seller.goofish.com/?site=COMMONPRO`;
- set `Origin` to `https://seller.goofish.com`.

The refund-order request was deliberately left unchanged because no equivalent failure has been proven there.

## Runtime validation

After applying the minimal change to the current Scheduler runtime, formal `OrderService.fetch_xianyu_orders` for `2214313339860` returned:

- total_fetched: 1
- new_inserted: 1 on the first post-fix sync
- failed: 0
- errors: none

A second sync returned the same one order without duplicate insertion, proving the native database/upsert path remained authoritative.

One-page validation across all six active accounts after the code fix:

- `2214313339860`: native order SUCCESS, one order fetched.
- `1034641456`: seller Session expired.
- `2196106636`: seller Session expired.
- `2217936413500`: seller Session expired.
- `2219319284219`: seller Session expired.
- `2858469041`: seller Session expired.

Thus the global order-client permission defect is fixed. The remaining five failures are account-level seller Session expiry, not the former `COMMONPRO` permission bug.

## Deterministic validation

- Source targeted tests: 2/2 PASS.
- Source `py_compile`: PASS.
- Clean patch-generation baseline tests: 2/2 PASS.
- Second clean worktree `git apply --check --whitespace=error-all --unidiff-zero`: PASS.
- Second clean worktree post-apply tests: 2/2 PASS.

## Artifact

- Patch: `vendor/patches/xianyu-auto-reply/64c245-chg0018-order-sold-permission-fix.patch`
- SHA256: `701421E7FCF883CD290782EDBBD2A1992374EFE4416FE6BDD24D13D647DCE4A5`
- Patch size: 1833 bytes.
- Patch files:
  - `common/services/order_service.py`
  - `tests/test_chg0018_order_sold_permission_header.py`
- New order engine created: false.
- Credentials printed or persisted: false.
- Customer messages sent: 0.
- Product writes: 0.

## Repository verification note

`python scripts/verify_repository.py` was executed in the formal repository. It reached the security-scan phase and stopped only on the pre-existing `tmp/publish_restore/...` sensitive-pattern findings that also blocked prior unrelated repairs. No file from this seller-order permission patch was reported by that scan; the historical temporary directory was not deleted or altered.
