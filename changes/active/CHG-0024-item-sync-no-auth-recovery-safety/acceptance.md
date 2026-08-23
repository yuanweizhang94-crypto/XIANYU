# CHG-0024 Acceptance

Status: VERIFYING

Change ID: CHG-0024-item-sync-no-auth-recovery-safety

This acceptance file records the approved narrow scope plus completed T1-T8 runtime acceptance. PR/main integration and QR restoration remain pending.

- [x] CHG0024_SCOPE_APPROVED=true and commander authorization are recorded.
- [x] EXISTING_OWNER_ONLY=true; the sole full-account owner remains `ItemService.fetch_all_items_from_account`.
- [x] AUTH_RECOVERY_CALLSITE_COUNT=2 is recorded: first-page catalog failure and missing-item authoritative reconciliation.
- [x] REUSE_DECISION=PATCH_EXISTING_OWNER and NO_DUPLICATE_OWNER=true are recorded.
- [x] DEFAULT_BEHAVIOR_PRESERVED=true is required by design.
- [x] PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false is required by design.
- [x] REMOTE_LISTING_MUTATION_FORBIDDEN=true is required by design.
- [x] UNKNOWN_NEVER_BLIND_RETRY=true is required by design.
- [x] Exact candidate/postimage source implements the Item-specific `no_auth_recovery` safe mode in the existing Item owner only.
- [x] CALLSITE_1 deterministic implementation test proves no Session convergence/maintain/renew/auth-dependent retry in safe mode.
- [x] CALLSITE_2 deterministic implementation test proves session/verification-required reconciliation preserves the prior local state/fails closed without Session convergence.
- [x] Historical/default Item Sync behavior remains unchanged outside safe mode; default-mode behavior test still invokes the existing convergence path.
- [x] Negative controls `2221422775489` and `2221501265279` remained authoritative HUMAN_QR_REQUIRED with `AUTH_WRITE_COUNT=0` through T7/T8.
- [x] Safe-mode live window proves `SESSION_MAINTAIN=0`, `SESSION_RENEW=0`, `PASSWORD_LOGIN=0`, `COOKIE_REFRESH=0`, `TOKEN_REFRESH=0`, `QR_ACTION=0`, and `QR_FALSE_GREEN_COUNT=0`.
- [x] Remote listing mutation counters remained zero for create/edit/delete/price/stock/publish.
- [x] Exactly one newly authorized controlled fresh Item Sync was executed after T5/T6 gates and returned SUCCESS.

## Bootstrap invariants

CHG0024_STATUS=VERIFYING
CHG0024_SCOPE_APPROVED=true
COMMANDER_AUTHORIZATION_RECORDED=true
ITEM_SYNC_EXECUTION_APPROVED=true_CONDITIONAL_AFTER_T6_GATES
PRODUCTION_ACTIVATION_APPROVED=true
QR_RESTORATION_APPROVED=false_PENDING_PR_MAIN_GATE
PRODUCTION_RUNTIME_SOURCE_CHANGED=true_VERIFIED_CHG0024_CANDIDATE
COMPANY_RUNTIME_SOURCE_CHANGED=true_VERIFIED_T5_MAPPING

## T2-T4 implementation evidence

SOURCE_PREIMAGE_AUTHORITY_RECONCILED=true
SAFE_MODE_NAME=`no_auth_recovery`
PERSISTENCE_MODEL=EXACT_VENDOR_PATCH_OVER_CURRENT_OWNER_PREIMAGE
PATCH_PATH=`vendor/patches/xianyu-auto-reply/chg0024-item-sync-no-auth-recovery-safety.patch`
PATCH_SHA256=`3a34f322be2cd18c789907ba48bc381a76ac513c00a9cfc102aa0252be759471`
PATCH_RUNTIME_FILE_COUNT=2
BEHAVIOR_TESTS=`7/7_PASS`
PATCH_REPLAY=PASS
CALLSITE_2_RESULT_MODEL_EXTENSION_REQUIRED=false
COMPANY_T5_REQUIRED=true
PUBLIC_TOOL_SCHEMA_CHANGED=false

T5-T8 live runtime counters are now accepted and are recorded below and in `evidence/20260823-runtime-acceptance.md`.

## Safe-mode negative-control model

NEGATIVE_CONTROL_SAFE_MODE_AUTH_WRITE_COUNT_MODEL=0

```text
SAFE_MODE_BEHAVIOR=FAIL_CLOSED_OR_SKIP
SESSION_MAINTAIN=0
SESSION_RENEW=0
PASSWORD_LOGIN=0
COOKIE_REFRESH=0
TOKEN_REFRESH=0
QR_ACTION=0
QR_FALSE_GREEN_COUNT=0
```

## Remote listing invariant

REMOTE_LISTING_MUTATION_FORBIDDEN=true

```text
REMOTE_LISTING_CREATE_COUNT=0
REMOTE_LISTING_EDIT_COUNT=0
REMOTE_LISTING_DELETE_COUNT=0
REMOTE_PRICE_CHANGE_COUNT=0
REMOTE_STOCK_CHANGE_COUNT=0
REMOTE_PUBLISH_COUNT=0
```

Allowed Item owner semantics are remote read plus local Item truth synchronization only.

## UNKNOWN / failure contract

UNKNOWN_NEVER_BLIND_RETRY=true

`FAILED` must not automatically trigger a second business invocation. `UNKNOWN` must stop writes and permit only read-only recovery/classification until authoritative state is known.

## Upstream capability audit

The completed read-only audit plus current accepted-image provenance reconciliation established the existing full-account owner, exact current preimages, and the absence of a safe full-account entrypoint before this patch.

## Pinned upstream evidence

Fresh XIANYU main base: `c9289081d3ec69d6f44b1a7259bf4760e3f0f081`. Exact authority hashes are persisted in the Change evidence.

## Existing local implementation search

The existing full-account owner is `ItemService.fetch_all_items_from_account`; no new owner is accepted. The single-page primitive cannot be manually orchestrated as a replacement full sync.

## Reuse decision

REUSE_DECISION=PATCH_EXISTING_OWNER
Project policy decision: `PATCH_UPSTREAM`.

## Duplicate implementation risk

Any second Item Sync owner/service/scheduler/worker, manual read-plus-upsert bypass, or new Session/Cookie/Token owner is an acceptance failure.

## Why upstream cannot satisfy the requirement as-is

The current full-account owner has two authentication-recovery callsites and no Item-specific no-auth-recovery safe mode.

## Approved exception ADR

Not applicable.

## Component owner

Existing XIANYU ItemService full-account sync owner. Existing Session/Cookie/Token lifecycle owners remain unchanged.

## Retirement plan for overlapping local code

No overlapping owner may be created. Review a minimal patch for retirement if upstream later provides an equivalent verified contract.
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
