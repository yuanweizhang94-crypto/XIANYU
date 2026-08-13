# 2026-08-13 Password + Item Platform Status Production Closure

## Execution Contract

- User outcome: QR/shared/manual/import accounts must not show or persist an automatic Xianyu login password when the user did not provide one; own-account item platform status and account publish restriction signal must be visible from existing item sync.
- Confirmed blocker: source account detail APIs still returned plaintext `login_password`, frontend used that value for password status and edit prefill, and item sync did not persist platform status/reconciliation metadata.
- Smallest success test: no account detail plaintext password exposure, no empty edit password overwrite, default-password pollution cleared by strict signature, existing `fetch_items` sync writes `XYCatalogItem.metadata_json.platform_status` and `XYAccount.metadata_json.platform_restriction`, with no new scheduler.

## Reuse Decision

- Decision: PATCH_UPSTREAM.
- Upstream evidence: pinned local implementation `D:\xianyu-chg0018-t12-patchcheck` reuses upstream-native `ItemInfoManager.get_item_list_info()` and `ItemService.fetch_all_items_from_account()`.
- Existing scheduler reused: `scheduler/app/services/scheduler/fetch_items_task.py` still calls `ItemService.fetch_all_items_from_account()`; no new scheduler task or execution owner was added.
- Metadata-only persistence: item platform state uses `XYCatalogItem.metadata_json`; account restriction signal uses `XYAccount.metadata_json.platform_restriction`.
- Duplicate-development risk: low; no new table, service, browser profile, publisher, sender, or scheduler was introduced.
- Rollback: revert vendor patch `vendor/patches/xianyu-auto-reply/64c245-chg0018-password-item-platform-status.patch` and redeploy previous backend/scheduler/frontend assets.

## Production Evidence

- Upstream current SHA checked: `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`.
- Default password pollution probe before cleanup: 4 accounts matched strict condition `login_method != password`, blank username, nonblank password, same 8-byte password signature.
- Cleanup executed: cleared pks `[2, 3, 4, 10]`; remaining matching pollution `[]`.
- Password-login credential rows in current production DB: 0 rows, so no live password-login row needed preservation; code path `upsert_account_from_password()` remains unchanged for real credentials.
- Manual add / QR / shared scan source paths do not write `login_password`; account detail payload now returns `has_password` and no plaintext `login_password`.
- Production read-only item sync sample A: account returned 0 active items after complete sync; 7 local items marked `NOT_IN_ACTIVE_LIST`; account marked `RESTRICTION_SUSPECTED`.
- Production read-only item sync sample B: account returned 2 active items after complete sync; 2 local items marked `ACTIVE`.
- Production aggregate after validation: item status counts `NOT_IN_ACTIVE_LIST=7`, `ACTIVE=10`, `UNSET=13`; account restriction counts `RESTRICTION_SUSPECTED=1`, `UNSET=10`.
- Health: backend `/docs` HTTP 200; frontend `/` HTTP 200.
- Containers: existing `xianyu_chg0017_backend_web`, `xianyu_chg0017_scheduler`, `xianyu_chg0017_frontend`, `xianyu_chg0017_websocket`, `xianyu_chg0017_mysql`, and `xianyu_chg0017_redis` were reused.
- Side effects: `xy_publish_logs` recent count 0; `xy_auto_reply_message_logs` recent count 0; no publish/offline/send APIs were called by validation.

## Validation

- `python -m py_compile backend-web\app\api\routes\cookies.py backend-web\app\api\routes\items.py backend-web\app\services\account_service.py common\schemas\account.py common\services\item_service.py`
- `python -m pytest tests\test_chg0018_password_item_platform_status.py tests\test_chg0018_consumer_readiness.py tests\test_chg0018_chat_auth_convergence.py -q` -> 15 passed.
- `npm run build` in `D:\xianyu-chg0018-t12-patchcheck\frontend` -> passed.
- `python scripts\verify_repository.py` to be run from repository root after evidence/patch staging.

