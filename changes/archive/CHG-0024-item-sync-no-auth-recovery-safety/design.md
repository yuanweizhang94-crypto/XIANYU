# CHG-0024 Design

Status: ARCHIVED

Change ID: CHG-0024-item-sync-no-auth-recovery-safety

GIT_MAIN_INTEGRATION=PASS
RUNTIME_ACCEPTANCE=PASS
PR_37_MERGED=true
FINAL_STATUS=ARCHIVED

## Design intent

Patch the existing account-scoped full Item Sync owner only. The authorized implementation uses one narrow Item-specific `no_auth_recovery: bool = False` execution mode and preserves the existing owner, route, response vocabulary, and default behavior.

## Existing owner

EXISTING_OWNER_ONLY=true
CURRENT_ITEM_SYNC_OWNER=`ItemService.fetch_all_items_from_account`
AUTH_RECOVERY_CALLSITE_COUNT=2
DOWNSTREAM_ALLOW_RENEW_FALSE_ALREADY_SUPPORTED=true
SESSION_OWNER_REDESIGN_REQUIRED=false
NO_DUPLICATE_OWNER=true

## Safe-mode contract

SAFE_MODE_NAME=`no_auth_recovery`
SAFE_MODE_TYPE=`bool`
PROPOSED_DEFAULT_VALUE=false

The flag is Item-specific and is not a generic Session lifecycle control.

It must not become a generic Session lifecycle API.

DEFAULT_BEHAVIOR_PRESERVED=true
PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false
REMOTE_LISTING_MUTATION_FORBIDDEN=true
UNKNOWN_NEVER_BLIND_RETRY=true

### CALLSITE_1 — FIRST_PAGE_CATALOG_FAILURE

Current path:

```text
_fetch_all_items_from_account_impl
-> _item_failure_needs_session_convergence
-> _converge_session_for_item_status
-> POST /internal/session/maintain
-> allow_renew=true for active account
-> possible remote retry
```

Safe mode:

```text
Session/auth/verification-class first-page failure
-> NO _converge_session_for_item_status
-> FAIL_CLOSED
-> NO remote retry dependent on auth recovery
```

### CALLSITE_2 — MISSING_ITEM_AUTHORITATIVE_RECONCILIATION

Current path:

```text
_reconcile_missing_active_items
-> _confirm_missing_items_authoritatively
-> _probe_item_detail_page_status
-> session_or_verification_required
-> _converge_session_for_item_status
-> possible maintain/renew
-> possible retry
```

Safe mode:

```text
session_or_verification_required
-> NO _converge_session_for_item_status
-> do not falsely classify remote item as removed
-> preserve UNKNOWN / fail closed
```

Both callsites must be covered by deterministic tests. Fixing only one is an acceptance failure.

## Negative controls

Negative controls: `2221422775489`, `2221501265279`.

If HUMAN_QR_REQUIRED is authoritative under safe mode:

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

Item Sync must never turn a blocked account ONLINE.

## Remote listing invariant

Allowed semantics:

```text
REMOTE_READ
+
LOCAL_ITEM_TRUTH_SYNC
```

Required counters:

```text
REMOTE_LISTING_CREATE_COUNT=0
REMOTE_LISTING_EDIT_COUNT=0
REMOTE_LISTING_DELETE_COUNT=0
REMOTE_PRICE_CHANGE_COUNT=0
REMOTE_STOCK_CHANGE_COUNT=0
REMOTE_PUBLISH_COUNT=0
```

## UNKNOWN / failure contract

Future safe sync result classes are `SUCCESS`, `FAILED`, and `UNKNOWN`.

`FAILED` does not trigger an automatic second business invocation.

`UNKNOWN` stops writes, performs read-only recovery/classification only, and is never blindly retried.

## Public caller boundary

The ChatGPT-facing caller keeps ordinary Item Sync request fields only. It must not expose `allow_renew`, Cookie/Token refresh, Session maintain, login, or password-login controls.

COMPANY_T5_REQUIRED=true. The existing `xianyu_item_sync` thin-adapter mapping fixes the Backend query selector to `no_auth_recovery=true`; its public schema remains unchanged and no new tool owner is permitted.

## Exact implementation and propagation

RUNTIME_PATCH_FILES=`backend-web/app/api/routes/items.py; common/services/item_service.py`
FUNCTION_SIGNATURE_CHANGE_COUNT=5

```text
existing /api/v1/items/get-all-from-account route
-> ItemService.fetch_all_items_from_account
-> _fetch_all_items_from_account_impl
-> CALLSITE_1
-> _reconcile_missing_active_items
-> _confirm_missing_items_authoritatively
-> CALLSITE_2
```

The route adds only an Item-specific `no_auth_recovery` query parameter. When true it is accepted only for a single-account request; global/multi-account use fails closed. No request-schema owner is changed.

CALLSITE_1 adds `and not no_auth_recovery` before convergence. Safe mode therefore falls through to the existing failed response without Session maintain or auth-dependent retry.

CALLSITE_2 propagates the flag into missing-item reconciliation/confirmation. Safe mode skips the pre-confirmation `NOT_IN_ACTIVE_LIST` write and skips convergence/reprobe on `session_or_verification_required`, reusing the existing `UNKNOWN + preserve_previous=true` model.

CALLSITE_2_RESULT_MODEL_EXTENSION_REQUIRED=false
PLANNED_NEW_FUNCTIONS_COUNT=0
PLANNED_NEW_ITEM_OWNER_COUNT=0
PLANNED_NEW_SERVICE_COUNT=0
PLANNED_NEW_ROUTE_COUNT=0
PLANNED_NEW_SCHEDULER_COUNT=0
PLANNED_NEW_WORKER_COUNT=0

PERSISTENCE_MODEL=EXACT_VENDOR_PATCH_OVER_CURRENT_OWNER_PREIMAGE
PATCH_PATH=`vendor/patches/xianyu-auto-reply/chg0024-item-sync-no-auth-recovery-safety.patch`

## Upstream capability audit

The read-only capability audit plus current-image provenance reconciliation proved that a full-account owner already exists, no safe full-account entrypoint existed before this patch, and the reuse decision remains patch-existing-owner only.

## Pinned upstream evidence

Fresh XIANYU main base for this Change: `c9289081d3ec69d6f44b1a7259bf4760e3f0f081`. Exact source/runtime SHA256 authority is persisted in `evidence/20260823-item-sync-no-auth-recovery-capability-audit.md`.

## Existing local implementation search

The existing full-account owner is `ItemService.fetch_all_items_from_account`. The single-page primitive is not a complete owner and must not be externally orchestrated into a bypass.

## Reuse decision

REUSE_DECISION=PATCH_EXISTING_OWNER
Project policy decision: `PATCH_UPSTREAM`.

## Duplicate implementation risk

Any new Item Sync owner/service/scheduler/worker, manual read-plus-upsert bypass, or Session/Cookie/Token owner is forbidden.

## Why upstream cannot satisfy the requirement as-is

The existing full-account owner lacks an Item-specific no-auth-recovery safe mode and contains two authentication-recovery callsites.

## Approved exception ADR

Not applicable.

## Component owner

Existing XIANYU ItemService remains authoritative for full-account Item Sync. Existing Session/Cookie/Token owners remain unchanged.

## Retirement plan for overlapping local code

No overlapping owner may be created. Retire a minimal local patch if a verified upstream equivalent later becomes authoritative.
## Runtime acceptance (2026-08-23)

CHG0024_RUNTIME_ACCEPTANCE=PASS
T5_COMPLETE=true
T6_COMPLETE=true
T7_COMPLETE=true
T8_COMPLETE=true
ITEM_SYNC_TARGET=`2804730247`
ITEM_SYNC_BUSINESS_INVOCATION_COUNT=1
ITEM_SYNC_RESULT=SUCCESS
QR_RESTORATION_NOT_YET_PERFORMED=true
NEGATIVE_CONTROLS_PRESERVED=true

The existing COMPANY thin adapter was activated from commit `c2cbaae2e658c371a950db56a4ac1cad4e7e2bce`; runtime/source SHA matched after Runner-owned Proxy reload, the public `xianyu_item_sync` schema remained unchanged, and the trusted mapping fixed `no_auth_recovery=true`. The accepted Backend candidate `xianyu-chg0024-backend-web:item-sync-no-auth-recovery-20260823-r1` (`sha256:923cc15d72900c7f6af3d3bd9a9bd3aeb0bccb80a9ac2af2cf307deea07cf1fb`) was activated exactly once through the existing COMPANY replacement transaction owner.

Exactly one fresh Item Sync then completed successfully for account `2804730247`: pre/post local item count `3 -> 3`, created `0`, updated `3`, removed `0`, unchanged `0`. Its exact execution window contained zero Session maintain/renew, Cookie refresh, Token refresh, password login, QR action, remote listing mutation, reconnect attempt, or real message send. Negative controls `2221422775489` and `2221501265279` remained authoritative `HUMAN_QR_REQUIRED` with zero auth-write indicators and `QR_FALSE_GREEN_COUNT=0`.

`2219319284219` retained its pre-existing authoritative `HUMAN_QR_REQUIRED` / `token_ready=false` state; this was not a new CHG-0024 invalidation and was not treated as green by the acceptance authority.
