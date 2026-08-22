# CHG-0024 Design

Status: APPROVED

Change ID: CHG-0024-item-sync-no-auth-recovery-safety

## Design intent

Patch the existing account-scoped full Item Sync owner only. A later authorized implementation may add one narrow Item-specific safe execution mode; this bootstrap phase does not modify runtime source.

## Existing owner

EXISTING_OWNER_ONLY=true
CURRENT_ITEM_SYNC_OWNER=`ItemService.fetch_all_items_from_account`
AUTH_RECOVERY_CALLSITE_COUNT=2
DOWNSTREAM_ALLOW_RENEW_FALSE_ALREADY_SUPPORTED=true
SESSION_OWNER_REDESIGN_REQUIRED=false
NO_DUPLICATE_OWNER=true

## Safe-mode contract

A future implementation may choose a narrow name consistent with existing style, conceptually equivalent to `no_auth_recovery=true` or `sync_safety_mode=NO_AUTH_RECOVERY`.

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

If COMPANY needs an update later, it is limited to the existing `xianyu_item_sync` thin-adapter mapping and a trusted fixed selection of the Item-specific safe mode. No new tool owner is permitted.

## Allowed implementation files

Future implementation scope is limited to:

- `backend-web/app/api/routes/items.py`
- `common/services/item_service.py`
- directly related targeted tests when proven necessary

COMPANY runtime source is not modified during bootstrap.

## Upstream capability audit

The read-only capability audit proved that a full-account owner already exists and that no safe full-account entrypoint currently exists. The reuse decision is patch-existing-owner only.

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
