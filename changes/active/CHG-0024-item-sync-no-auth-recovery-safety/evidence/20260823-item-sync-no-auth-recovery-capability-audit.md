# 2026-08-23 Item Sync No-Auth-Recovery Capability Audit

Change: CHG-0024-item-sync-no-auth-recovery-safety

Audit type: read-only capability/owner-chain audit. No Item Sync, remote item read, Session maintain, credential recovery, real message, production container mutation, or remote listing mutation was performed during this audit/bootstrap.

## Fresh Git authority

BASE_MAIN_SHA=`c9289081d3ec69d6f44b1a7259bf4760e3f0f081`

The bootstrap phase refreshed `origin/main` and confirmed it matched the commander-authorized SHA before governance writes began.

## Source authority

ITEM_ROUTE_FILE=`backend-web/app/api/routes/items.py`
ITEM_SERVICE_FILE=`common/services/item_service.py`
ITEM_SESSION_CONVERGENCE_FILE=`common/services/item_service.py`
SESSION_MAINTAIN_ROUTE_FILE=`websocket/app/api/routes/cookies_refresh.py`
SESSION_MAINTAIN_SERVICE_FILE=`common/services/cookie_renew_api_service.py`
COMPANY_ITEM_SYNC_ADAPTER_FILE=`D:/TikTok_Auto/devspace_proxy/proxy.cjs`

ITEM_ROUTE_SHA256=`405d6fa3fea84740050b37783de9b9da422efde918e086fb709d6c29d6cacf5`
ITEM_SERVICE_SHA256=`909307861de1df2e07dafd0ac936ca00959f81992a4a36c74419842883ff3c5f`
SESSION_MAINTAIN_ROUTE_SHA256=`421251967fff0cceb2af3eabdd5659ac7539a81d17511a217006fae6f62ceb3b`
SESSION_MAINTAIN_SERVICE_SHA256=`49074386640af9f938b3165329ed70fa9725ef9a955f423bdac2d4e3f782f95f`
COMPANY_ADAPTER_SHA256=`7aa238c6f4747255a584a61e4d1b1d5952a23338528ad643e73f1f7aa2ede346`

These hashes are the frozen read-only audit authority persisted by commander instruction. The tracked governance repository does not itself vendor these runtime source files as ordinary tracked source; this bootstrap therefore records the proven audit authority rather than reconstructing or synthesizing source.

## Existing owner chain

EXISTING_OWNER_CHAIN_PROVEN=true
CURRENT_ITEM_SYNC_OWNER=`ItemService.fetch_all_items_from_account`
CURRENT_ITEM_SYNC_SCOPE=ACCOUNT_SCOPED
REMOTE_SEMANTICS=REMOTE_ITEM_CATALOG_READ_PLUS_LOCAL_XY_CATALOG_UPSERT
REMOTE_LISTING_MUTATION_OWNER_PRESENT=false

Formal current control flow:

```text
COMPANY xianyu_item_sync
-> POST /api/v1/items/get-all-from-account
-> ItemService.fetch_all_items_from_account
-> _fetch_all_items_from_account_impl
-> ItemInfoManager.get_item_list_info(page)
-> save_fetched_items
-> local xy_catalog_items upsert
```

The existing `/api/v1/items/get-by-page` / `fetch_items_page_from_account` path is only a single-page primitive. External/manual pagination plus DB-upsert orchestration would create a bypass and is not an acceptable full-account owner.

## Auth-recovery callsite 1

CALLSITE_1=FIRST_PAGE_CATALOG_FAILURE

```text
_fetch_all_items_from_account_impl
-> _item_failure_needs_session_convergence
-> _converge_session_for_item_status
-> POST /internal/session/maintain
-> allow_renew=true for active account
-> possible remote retry
```

The full-account sync has no Item-specific no-auth-recovery selector at this callsite.

## Auth-recovery callsite 2

CALLSITE_2=MISSING_ITEM_AUTHORITATIVE_RECONCILIATION

```text
_reconcile_missing_active_items
-> _confirm_missing_items_authoritatively
-> _probe_item_detail_page_status
-> session_or_verification_required
-> _converge_session_for_item_status
-> possible maintain/renew
-> possible retry
```

The future safe-mode repair must cover this reconciliation path as well as first-page failure. Fixing only callsite 1 would leave automatic auth recovery reachable.

CURRENT_AUTH_RECOVERY_FALLBACK_PROVEN=true
AUTH_RECOVERY_CALLSITE_COUNT=2

## Existing downstream safety capability

DOWNSTREAM_ALLOW_RENEW_FALSE_ALREADY_SUPPORTED=true
SESSION_OWNER_REDESIGN_REQUIRED=false

The existing Session maintain route already supports `allow_renew=false`; the missing contract is at the Item full-sync owner/caller boundary. No second Session owner is required.

## Reuse decision

REUSE_DECISION=PATCH_EXISTING_OWNER
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false
EXISTING_SAFE_FULL_SYNC_ENTRYPOINT=false
MINIMAL_EXISTING_OWNER_PATCH_REQUIRED=true
NO_DUPLICATE_OWNER=true

A new Item Sync service, worker, scheduler, owner, or manual remote-read plus DB-upsert bypass is forbidden.

## COMPANY thin-adapter boundary

Current public adapter request fields are limited to ordinary Item Sync fields such as `account_id`, `page_size`, and `max_pages`.

PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false

A future COMPANY update, if actually necessary, must remain within the existing `xianyu_item_sync` thin adapter and fixed trusted safe-mode selection. Do not expose generic lifecycle fields such as `allow_renew`, refresh-cookie, refresh-token, Session-maintain, login, or password-login controls to the public caller.

## Failed-closed post-CHG-0023 attempt

POST_CHG0023_ITEM_SYNC_ATTEMPT_RESULT=FAILED_CLOSED
AUTHORIZED_TARGET_ACCOUNT=2804730247
AUTHORIZED_TARGET_ACTUALLY_INVOKED=false
ERRONEOUS_SENTINEL_ACCOUNT=__SCHEMA_ONLY_INVALID__
ERRONEOUS_SENTINEL_INVOCATION_COUNT=1
ERRONEOUS_SENTINEL_RESULT=FAILED_ACCOUNT_NOT_FOUND
ERRONEOUS_SENTINEL_REMOTE_ITEM_READ_COUNT=0
ERRONEOUS_SENTINEL_LOCAL_ITEM_WRITE_COUNT=0
ERRONEOUS_SENTINEL_REMOTE_LISTING_MUTATION_COUNT=0
ERRONEOUS_SENTINEL_SESSION_MAINTAIN_COUNT=0
PREVIOUS_PHASE_RETRY_PERFORMED=false

The sentinel invocation permanently closed the previous phase. It must not be replayed during CHG-0024 bootstrap and must not be inserted into CHG-0023 runtime acceptance.

## Future safe-mode contract

DEFAULT_BEHAVIOR_PRESERVED=true
REMOTE_LISTING_MUTATION_FORBIDDEN=true
UNKNOWN_NEVER_BLIND_RETRY=true

CALLSITE_1 safe mode:

```text
Session/auth/verification-class first-page failure
-> no _converge_session_for_item_status
-> fail closed
-> no remote retry dependent on auth recovery
```

CALLSITE_2 safe mode:

```text
session_or_verification_required
-> no _converge_session_for_item_status
-> do not falsely classify item as removed
-> preserve unknown / fail closed
```

## Negative-control contract

Negative controls: `2221422775489`, `2221501265279`.

```text
SAFE_MODE_BEHAVIOR=FAIL_CLOSED_OR_SKIP
AUTH_WRITE_COUNT=0
SESSION_MAINTAIN=0
SESSION_RENEW=0
PASSWORD_LOGIN=0
COOKIE_REFRESH=0
TOKEN_REFRESH=0
QR_ACTION=0
QR_FALSE_GREEN_COUNT=0
```

Item Sync must not make a HUMAN_QR_REQUIRED account appear ONLINE.

## Remote listing invariant

```text
REMOTE_LISTING_CREATE_COUNT=0
REMOTE_LISTING_EDIT_COUNT=0
REMOTE_LISTING_DELETE_COUNT=0
REMOTE_PRICE_CHANGE_COUNT=0
REMOTE_STOCK_CHANGE_COUNT=0
REMOTE_PUBLISH_COUNT=0
```

Item Sync owner semantics remain REMOTE_READ plus LOCAL_ITEM_TRUTH_SYNC only.

## Bootstrap execution counters

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
RUNTIME_SOURCE_CHANGED=false
COMPANY_RUNTIME_SOURCE_CHANGED=false

No implementation/runtime tests are claimed as PASS in this evidence. This file locks capability audit and governance scope only.
