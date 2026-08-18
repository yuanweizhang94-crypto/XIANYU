# 2026-08-18 Order fetch recovery

## Execution contract

- User outcome: restore XIANYU order acquisition so existing order lookup can receive newly synchronized orders again.
- Confirmed blocker: the three native order scheduler tasks were disabled, and a prior local Auto Reply stability patch changed order tasks from upstream-native `is_account_session_cooled(account_id)` to `is_account_session_cooled(account_id, metadata_json)`, causing stale Auto Reply platform-verification metadata to block order synchronization.
- Smallest success test: restore upstream-native order cooldown calls, enable the existing `fetch_orders`, `fetch_pending_orders`, and `fetch_refund_orders` tasks at their existing intervals, restart only Scheduler, and verify the tasks execute with real failure classification instead of being silently skipped or counted as success.

## Upstream-first decision

- Decision: `PATCH_UPSTREAM` for one confirmed defect in the existing upstream order scheduler path; no new order engine, API, table, queue, worker, or executor was created.
- Upstream comparison: current `origin/main` keeps `FetchOrdersTaskService` and `FetchRefundOrdersTaskService` on `is_account_session_cooled(account.account_id)` only.
- Local regression: production had `is_account_session_cooled(account.account_id, account.metadata_json)`, which allowed Auto Reply PVR metadata to block order acquisition.
- Duplicate-development risk: none; the native `OrderService`, Scheduler task services, database order model, and `/api/v1/orders` read path remain the sole owners.

## Pre-fix runtime evidence

- `xianyu_orders(account_id=2214313339860)` returned `SUCCESS` with zero rows; the adapter and Backend route were alive.
- Unfiltered `xianyu_orders` returned three historical rows, with the newest local order update dated 2026-08-07, proving the local order table existed but synchronization had stopped.
- Scheduler runtime status before repair:
  - `fetch_orders`: enabled=false, interval=600s
  - `fetch_pending_orders`: enabled=false, interval=60s
  - `fetch_refund_orders`: enabled=false, interval=120s
- Scheduler logs showed the `fetch_orders` loop loaded as disabled and had not performed live order synchronization during the observed window.
- A controlled manual pre-fix `fetch_orders` trigger showed three enabled accounts skipped by the Auto Reply platform-verification marker, while the other three reached the native order MTOP path and returned `FAIL_SYS_SESSION_EXPIRED`.

## Repair

Runtime code change in `scheduler/app/services/scheduler/fetch_orders_task.py`:

1. Restored both order-task cooldown calls to the upstream-native form:
   - `is_account_session_cooled(account.account_id)`
2. Removed cross-capability dependency on `account.metadata_json` / Auto Reply PVR for order acquisition.
3. Corrected task result semantics so a non-empty `errors` result increments `failed_count` instead of being counted as successful.
4. Applied the same failure classification to refund-order synchronization.

Operational configuration repair:

- Re-enabled the existing native tasks without changing their intervals:
  - `fetch_orders=true`, 600s
  - `fetch_pending_orders=true`, 60s
  - `fetch_refund_orders=true`, 120s
- Restarted only `xianyu_chg0017_scheduler` so the repaired source and persisted task configuration were loaded.
- Backend, WebSocket, MySQL, Redis, and Frontend were not restarted for this repair.

## Validation

- Runtime `py_compile`: PASS.
- Post-restart Scheduler status:
  - `fetch_orders`: enabled=true, task_running=true
  - `fetch_pending_orders`: enabled=true, task_running=true
  - `fetch_refund_orders`: enabled=true, task_running=true
- The previously skipped account paths now reach the native order service rather than being blocked solely by Auto Reply PVR metadata.
- Latest runtime task summary correctly reports failed account attempts when the native order API returns an error; it no longer reports those attempts as successful zero-order fetches.
- Clean patch-generation baseline targeted tests: 3/3 PASS.
- Second clean patch apply check: PASS with `--whitespace=error-all --unidiff-zero`.
- Second clean baseline after applying the patch: 3/3 PASS.
- `python scripts/verify_repository.py` was executed in the formal repository. It reached the security-scan step and stopped only on the pre-existing `tmp/publish_restore/...` sensitive-pattern findings already present before this repair; no order-recovery file was reported by that scan.

## Remaining platform/account blocker

The local regression is repaired, but the current enabled production accounts do not yet have a usable seller-order business session:

- observed native order responses include `FAIL_SYS_SESSION_EXPIRED` and `PERMISSION_EXCEPTION`;
- the existing `api_cookie_renew` task also reports official login/QR/platform-verification conditions for the affected business-maintenance accounts;
- therefore no local code path can truthfully claim new order synchronization is currently successful until the official account business session is refreshed.

This is an account/session condition, not a reason to create a second order crawler or bypass platform verification. The repaired scheduler remains enabled and will automatically resume native order synchronization after the account session is valid again.

## Artifact

- Patch: `vendor/patches/xianyu-auto-reply/64c245-chg0018-order-fetch-recovery.patch`
- Patch SHA256: `8FC6B31FAE1398AC3A8F67D6C20D986FF506654D0DC9E3EC89837FAA44850F6A`
- Changed upstream files recorded by the patch:
  - `scheduler/app/services/scheduler/fetch_orders_task.py`
  - `tests/test_chg0018_order_fetch_recovery.py`
- New order engine created: false.
- New scheduler executor created: false.
- Customer messages sent: 0.
- Products published/edited: 0.
