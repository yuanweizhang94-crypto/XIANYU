# 2026-08-23 CHG-0024 Source Preimage Authority Reconciliation

Change: CHG-0024-item-sync-no-auth-recovery-safety

AUDIT_MODE=READ_ONLY_RUNTIME_IMAGE_PROVENANCE

## Result

SOURCE_PREIMAGE_AUTHORITY_RECONCILED=true
PREIMAGE_AUTHORITY_RECONCILIATION=OLD_AUDIT_HASH_STALE__CURRENT_ACCEPTED_RUNTIME_SOURCE_PROMOTED_TO_AUTHORITY
OLD_AUDIT_HASH_CLASSIFICATION=STALE_AUDIT_PREIMAGE

STALE_AUDIT_ITEM_ROUTE_SHA256=`405d6fa3fea84740050b37783de9b9da422efde918e086fb709d6c29d6cacf5`
STALE_AUDIT_ITEM_SERVICE_SHA256=`909307861de1df2e07dafd0ac936ca00959f81992a4a36c74419842883ff3c5f`

AUTHORITATIVE_ITEM_ROUTE_SHA256=`5be558b4c01cc14b99a88dde19c8f8a9c2f890aedbd132f0bc97dbf464a5d78a`
AUTHORITATIVE_ITEM_SERVICE_SHA256=`5a875adc11adb6b19320206a4e9c34cd63453f9c5f35be482bf055574325b517`

## Current accepted Backend authority

CURRENT_BACKEND_CONTAINER=`xianyu_chg0017_backend_web`
CURRENT_BACKEND_CONTAINER_ID=`35590e22d788c704b34fe6edb2cc0ac477cce492a117137ae7d26e58c5ebf31e`
CURRENT_BACKEND_IMAGE=`xianyu-chg0023-backend-web:readiness-contract-20260822-r1`
CURRENT_BACKEND_IMAGE_ID=`sha256:5c3209890a93599081cc6b2a1de31714598bec7599d8f613f64dfd174c69e6d0`
CURRENT_BACKEND_OCI_MANIFEST_DIGEST=`sha256:c83b80adc9830fcf90d03a624690bf0c98a26df98bb6e90d3f057b2d8c3e8723`
CURRENT_BACKEND_CONTAINER_CREATED=`2026-08-22T07:21:17.093316508Z`
CURRENT_BACKEND_CONTAINER_STARTED=`2026-08-22T07:21:17.47336475Z`
CURRENT_BACKEND_ROOTFS_LAYER_COUNT=85

The running Backend has only runtime data/log volumes under `/app/backups`, `/app/browser_data`, `/app/static`, and `/app/backend-web/logs`. Neither target source path is bind- or volume-mounted.

CURRENT_RUNTIME_IMAGE_AUTHORITY_PROVEN=true
CURRENT_FILES_MATCH_IMAGE_OR_PROVEN_MOUNT_SOURCE=true
UNKNOWN_RUNTIME_SOURCE_MUTATION=false

A never-started disposable container was created from the exact image and used only for `docker cp` byte comparison. The running container and immutable image matched byte-for-byte for both target files:

- `/app/backend-web/app/api/routes/items.py` -> `5be558b4c01cc14b99a88dde19c8f8a9c2f890aedbd132f0bc97dbf464a5d78a`
- `/app/common/services/item_service.py` -> `5a875adc11adb6b19320206a4e9c34cd63453f9c5f35be482bf055574325b517`

DISPOSABLE_CONTAINER_START_COUNT=0

## Current owner signatures and callsites

ROUTE_HANDLER_SIGNATURE=`fetch_all_items_from_account(payload: ItemFullFetchRequest, current_user=Depends(...), account_service=Depends(...), item_service=Depends(...)) -> Dict[str, Any]`
FETCH_ALL_ITEMS_SIGNATURE=`ItemService.fetch_all_items_from_account(self, account: XYAccount, page_size: int = 20, max_pages: int | None = None, stop_when_page_all_existing: bool = False, required_title_keyword: str | None = None, force_authoritative_probe: bool = False) -> dict[str, Any]`
FETCH_ALL_IMPL_SIGNATURE=`ItemService._fetch_all_items_from_account_impl(self, account: XYAccount, page_size: int = 20, max_pages: int | None = None, stop_when_page_all_existing: bool = False, required_title_keyword: str | None = None, force_authoritative_probe: bool = False) -> dict[str, Any]`
RECONCILE_MISSING_SIGNATURE=`ItemService._reconcile_missing_active_items(self, account: XYAccount, current_item_ids: set[str], now: str, *, force_authoritative_probe: bool = False) -> dict[str, Any]`
CONFIRM_MISSING_SIGNATURE=`ItemService._confirm_missing_items_authoritatively(self, account: XYAccount, missing_items: list[XYCatalogItem], now: str, *, force: bool = False) -> dict[str, Any]`
CONVERGE_SESSION_SIGNATURE=`ItemService._converge_session_for_item_status(self, account: XYAccount) -> dict[str, Any]`

AUTH_RECOVERY_CALLSITE_COUNT=2
CALLSITE_1=FIRST_PAGE_CATALOG_FAILURE
CALLSITE_2=MISSING_ITEM_AUTHORITATIVE_RECONCILIATION

A source-wide reference scan found exactly two calls to `_converge_session_for_item_status`: the missing-item authoritative confirmation path and first-page full-catalog failure path. No third full-sync auth-recovery callsite was found.

## Safety counters during reconciliation

ITEM_SYNC_INVOCATION_COUNT=0
REMOTE_ITEM_READ_COUNT=0
SESSION_MAINTAIN_CALL_COUNT=0
COOKIE_REFRESH_COUNT=0
TOKEN_REFRESH_COUNT=0
PASSWORD_LOGIN_ATTEMPTS=0
QR_ACTIONS=0
REAL_MESSAGES_SENT=0
PRODUCTION_CONTAINER_MUTATION_COUNT=0
PRODUCTION_CONTAINER_RESTART_COUNT=0
