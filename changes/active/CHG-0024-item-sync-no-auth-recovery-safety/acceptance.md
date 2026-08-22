# CHG-0024 Acceptance

Status: APPROVED

Change ID: CHG-0024-item-sync-no-auth-recovery-safety

This acceptance file defines the approved narrow scope and future safety contract. It does not claim runtime implementation or production execution.

- [x] CHG0024_SCOPE_APPROVED=true and commander authorization are recorded.
- [x] EXISTING_OWNER_ONLY=true; the sole full-account owner remains `ItemService.fetch_all_items_from_account`.
- [x] AUTH_RECOVERY_CALLSITE_COUNT=2 is recorded: first-page catalog failure and missing-item authoritative reconciliation.
- [x] REUSE_DECISION=PATCH_EXISTING_OWNER and NO_DUPLICATE_OWNER=true are recorded.
- [x] DEFAULT_BEHAVIOR_PRESERVED=true is required by design.
- [x] PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false is required by design.
- [x] REMOTE_LISTING_MUTATION_FORBIDDEN=true is required by design.
- [x] UNKNOWN_NEVER_BLIND_RETRY=true is required by design.
- [ ] Runtime source implements the Item-specific no-auth-recovery safe mode.
- [ ] CALLSITE_1 deterministic implementation test proves no Session convergence/maintain/renew/retry in safe mode.
- [ ] CALLSITE_2 deterministic implementation test proves session/verification-required reconciliation preserves unknown/fails closed without Session convergence.
- [ ] Historical/default Item Sync behavior remains unchanged outside safe mode.
- [ ] Negative controls `2221422775489` and `2221501265279` prove HUMAN_QR_REQUIRED fails closed or skips with `AUTH_WRITE_COUNT=0`.
- [ ] Safe mode proves `SESSION_MAINTAIN=0`, `SESSION_RENEW=0`, `PASSWORD_LOGIN=0`, `COOKIE_REFRESH=0`, `TOKEN_REFRESH=0`, `QR_ACTION=0`, and `QR_FALSE_GREEN_COUNT=0`.
- [ ] Remote listing mutation counters remain zero for create/edit/delete/price/stock/publish.
- [ ] A future newly authorized controlled fresh Item Sync is executed only after implementation/runtime gates pass.

## Bootstrap invariants

CHG0024_STATUS=APPROVED
CHG0024_SCOPE_APPROVED=true
COMMANDER_AUTHORIZATION_RECORDED=true
ITEM_SYNC_EXECUTION_APPROVED=false
PRODUCTION_ACTIVATION_APPROVED=false
QR_RESTORATION_APPROVED=false
RUNTIME_SOURCE_CHANGED=false
COMPANY_RUNTIME_SOURCE_CHANGED=false

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

The completed read-only audit established the existing full-account owner and the absence of a safe full-account entrypoint. This bootstrap does not repeat business execution.

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
