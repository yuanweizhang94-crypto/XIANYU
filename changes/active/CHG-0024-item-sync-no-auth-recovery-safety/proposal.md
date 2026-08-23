# CHG-0024 Item Sync No-Auth-Recovery Safety

Status: VERIFYING

Change ID: CHG-0024-item-sync-no-auth-recovery-safety

CHG0024_SCOPE_APPROVED=true
COMMANDER_AUTHORIZATION_RECORDED=true
ITEM_SYNC_EXECUTION_APPROVED=true_CONDITIONAL_AFTER_T6_GATES
PRODUCTION_ACTIVATION_APPROVED=true
QR_RESTORATION_APPROVED=false_PENDING_PR_MAIN_GATE

## Execution contract

User outcome: preserve the existing full-account Item Sync owner while adding the commander-authorized Item-specific safe mode that never performs automatic credential recovery.

Confirmed blocker: the existing full-account Item Sync has two authentication-recovery callsites and no caller-selectable no-auth-recovery mode.

Minimal intervention: patch only the existing Item Sync owner. Do not create a second Item Sync owner, service, scheduler, worker, Session owner, Cookie owner, or Token owner.

Smallest success test: deterministic tests prove both authentication-recovery callsites fail closed or preserve unknown in safe mode with zero Session maintain, renew, password login, Cookie refresh, Token refresh, or QR action while historical/default behavior remains unchanged.

Stop condition: any evidence that a new execution owner, remote listing mutation path, generic Session lifecycle control, production activation, or unapproved business invocation is required.

## Commander decision

COMMANDER_DECISION=AUTHORIZE_NEW_NARROW_ITEM_SYNC_SAFETY_CHANGE
NEW_CHANGE_ID=CHG-0024-item-sync-no-auth-recovery-safety
PATCH_EXISTING_ITEM_SYNC_OWNER_ONLY=true

BOOTSTRAP_DO_NOT_IMPLEMENT_CHG0024=HISTORICAL_SUPERSEDED_BY_20260823_AUTONOMOUS_AUTHORIZATION
AUTONOMOUS_T2_T8_AUTHORIZED=true
ITEM_SYNC_AUTHORIZATION=EXACTLY_ONE_AFTER_T6_GATES
QR_RESTORATION_AUTHORIZATION=CONDITIONAL_AFTER_ITEM_SYNC_AND_GIT_MAIN_GATE

## Purpose

Add `no_auth_recovery: bool = False` as the narrow Item-specific safe mode on the existing full-account Item Sync owner; no new owner or lifecycle abstraction is introduced.

Target semantics remain:

```text
remote item catalog read
-> local XIANYU Item truth synchronization
```

Safe mode must additionally enforce:

```text
NO Session maintain
NO Session renewal
NO password login
NO Cookie refresh
NO Token refresh
NO QR recovery
```

Any state requiring authentication recovery must fail closed or preserve unknown and must never automatically recover credentials.

## Post-CHG-0023 failed-closed Item Sync attempt

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

This historical failed-closed invocation is recorded here only. It is not part of CHG-0023 runtime acceptance and must not be replayed during bootstrap.

## Capability audit authority

ITEM_ROUTE_FILE=`backend-web/app/api/routes/items.py`
ITEM_SERVICE_FILE=`common/services/item_service.py`
ITEM_SESSION_CONVERGENCE_FILE=`common/services/item_service.py`
SESSION_MAINTAIN_ROUTE_FILE=`websocket/app/api/routes/cookies_refresh.py`
SESSION_MAINTAIN_SERVICE_FILE=`common/services/cookie_renew_api_service.py`
COMPANY_ITEM_SYNC_ADAPTER_FILE=`D:/TikTok_Auto/devspace_proxy/proxy.cjs`

STALE_AUDIT_ITEM_ROUTE_SHA256=`405d6fa3fea84740050b37783de9b9da422efde918e086fb709d6c29d6cacf5`
STALE_AUDIT_ITEM_SERVICE_SHA256=`909307861de1df2e07dafd0ac936ca00959f81992a4a36c74419842883ff3c5f`
AUTHORITATIVE_IMPLEMENTATION_PREIMAGE_ITEM_ROUTE_SHA256=`5be558b4c01cc14b99a88dde19c8f8a9c2f890aedbd132f0bc97dbf464a5d78a`
AUTHORITATIVE_IMPLEMENTATION_PREIMAGE_ITEM_SERVICE_SHA256=`5a875adc11adb6b19320206a4e9c34cd63453f9c5f35be482bf055574325b517`
SESSION_MAINTAIN_ROUTE_SHA256=`421251967fff0cceb2af3eabdd5659ac7539a81d17511a217006fae6f62ceb3b`
SESSION_MAINTAIN_SERVICE_SHA256=`49074386640af9f938b3165329ed70fa9725ef9a955f423bdac2d4e3f782f95f`
STALE_AUDIT_COMPANY_ADAPTER_SHA256=`7aa238c6f4747255a584a61e4d1b1d5952a23338528ad643e73f1f7aa2ede346`
AUTHORITATIVE_PRE_T5_COMPANY_PROXY_SHA256=`b7537ad0a2b5e3e24310ec1fb99b7aac374e02c7f72894ffad642632107d1bf7`

EXISTING_OWNER_CHAIN_PROVEN=true
CURRENT_ITEM_SYNC_OWNER=`ItemService.fetch_all_items_from_account`
CURRENT_ITEM_SYNC_SCOPE=ACCOUNT_SCOPED
REMOTE_SEMANTICS=REMOTE_ITEM_CATALOG_READ_PLUS_LOCAL_XY_CATALOG_UPSERT
REMOTE_LISTING_MUTATION_OWNER_PRESENT=false

## Authentication-recovery callsites

AUTH_RECOVERY_CALLSITE_COUNT=2

CALLSITE_1=FIRST_PAGE_CATALOG_FAILURE

```text
_fetch_all_items_from_account_impl
-> _item_failure_needs_session_convergence
-> _converge_session_for_item_status
-> POST /internal/session/maintain
-> allow_renew=true for active account
-> possible remote retry
```

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

CURRENT_AUTH_RECOVERY_FALLBACK_PROVEN=true

Both callsites are covered by the exact existing-owner patch. Fixing only CALLSITE_1 remains insufficient.

## Reuse decision

Decision: PATCH_UPSTREAM
REUSE_DECISION=PATCH_EXISTING_OWNER
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false
EXISTING_SAFE_FULL_SYNC_ENTRYPOINT=false
MINIMAL_EXISTING_OWNER_PATCH_REQUIRED=true
DOWNSTREAM_ALLOW_RENEW_FALSE_ALREADY_SUPPORTED=true
SESSION_OWNER_REDESIGN_REQUIRED=false
NO_DUPLICATE_OWNER=true

Project policy label: `PATCH_UPSTREAM` because the current existing owner is patched in place and ownership is preserved.

The existing single-page primitive is not a replacement full-account owner. Manual remote-read plus DB-upsert orchestration is forbidden.

## Authorized implementation scope and current result

The implementation remains limited to the following existing XIANYU owner paths:

- `backend-web/app/api/routes/items.py`
- `common/services/item_service.py`
- targeted deterministic tests/evidence

PERSISTENCE_MODEL=EXACT_VENDOR_PATCH_OVER_CURRENT_OWNER_PREIMAGE
PATCH_PATH=`vendor/patches/xianyu-auto-reply/chg0024-item-sync-no-auth-recovery-safety.patch`
PATCH_RUNTIME_FILE_COUNT=2

The existing COMPANY `xianyu_item_sync` mapping was proven necessary for trusted safe-mode selection. Its public schema is unchanged; only the existing thin mapping is patched.

## Forbidden scope

NEW_ITEM_SYNC_OWNER=false
NEW_ITEM_SERVICE=false
PARALLEL_SYNC_STACK=false
MANUAL_REMOTE_READ_PLUS_DB_UPSERT_BYPASS=false
NEW_SCHEDULER=false
NEW_WORKER=false
NEW_SESSION_OWNER=false
NEW_COOKIE_OWNER=false
NEW_TOKEN_OWNER=false
SESSION_REDESIGN=false
COOKIE_REDESIGN=false
TOKEN_REDESIGN=false

Remote listing creation, editing, deletion, price changes, stock changes, and publishing are forbidden.

## Public caller contract

PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false

The public ChatGPT-facing caller must continue to expose only normal Item Sync request fields such as `account_id`, `page_size`, and `max_pages`. It must not expose generic Session/Cookie/Token lifecycle controls such as `allow_renew`, refresh controls, Session maintain, login, or password login.

The existing COMPANY adapter is used for controlled safe sync; the trusted mapping fixes `no_auth_recovery=true` while the public schema remains `account_id`, `page_size`, and `max_pages` only. No new tool owner is created.

## Safety invariants

DEFAULT_BEHAVIOR_PRESERVED=true
REMOTE_LISTING_MUTATION_FORBIDDEN=true
UNKNOWN_NEVER_BLIND_RETRY=true

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

## Upstream capability audit

The completed read-only capability audit and current accepted-image provenance reconciliation establish that the existing full-account Item Sync owner remains authoritative and that the correct decision is to patch that owner, not build a parallel implementation.

## Pinned upstream evidence

The current XIANYU fresh-main governance base for this Change is `c9289081d3ec69d6f44b1a7259bf4760e3f0f081`. Runtime/source capability authority and SHA256 values are recorded in the audit evidence for the files listed above.

## Existing local implementation search

The audit identified `ItemService.fetch_all_items_from_account` as the account-scoped owner and found no existing safe full-account entrypoint. The single-page primitive is not an acceptable replacement owner.

## Duplicate implementation risk

HIGH if a second Item Sync owner, service, scheduler, worker, manual read-plus-upsert bypass, Session owner, Cookie owner, Token owner, or public lifecycle-control surface is added. This Change forbids those outcomes.

## Why upstream cannot satisfy the requirement

The current existing full-account owner has two authentication-recovery callsites and no caller-selectable Item-specific no-auth-recovery safe mode. A minimal patch to the existing owner is required; a new implementation is not.

## Approved exception ADR

Not applicable. This is a patch to the existing owner, not `BUILD_LOCAL_EXCEPTION`.

## Component owner

Existing XIANYU `ItemService.fetch_all_items_from_account` remains the sole full-account Item Sync owner. Existing Session/Cookie/Token owners remain authoritative for their own lifecycle and are not redesigned.

## Retirement plan for overlapping local code

No overlapping local owner will be introduced. If upstream later provides an equivalent verified Item-specific safe mode, any local patch must be reviewed for retirement in favor of upstream.
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
