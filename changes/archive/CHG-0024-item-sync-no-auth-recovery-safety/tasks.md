# CHG-0024 Tasks

Status: ARCHIVED

Change ID: CHG-0024-item-sync-no-auth-recovery-safety

- [x] T1 Capability audit and formal scope lock: persist the existing owner chain, two authentication-recovery callsites, reuse decision, safety invariants, failed-closed prior attempt, and commander authorization without runtime implementation or production execution.
- [x] T2 Exact implementation diff design against current accepted-image source; reconcile stale audit hashes and lock the `no_auth_recovery` propagation/persistence design.
- [x] T3 Implement Item-specific `no_auth_recovery` safe mode as the exact two-owner vendor patch without changing Session/Cookie/Token owners.
- [x] T4 Run deterministic postimage behavior/mock-spy tests for both auth-recovery callsites plus exact patch replay.
- [x] T5 Activate the proven existing COMPANY `xianyu_item_sync` trusted safe-mode mapping; public schema unchanged.
- [x] T6 Activate and verify the exact Backend candidate through the existing COMPANY replacement transaction owner.
- [x] T7 Execute exactly one controlled fresh Item Sync for `2804730247`; result SUCCESS.
- [x] T8 Negative-control/runtime acceptance post-check PASS; formal persistence is this commit preparation phase.

T1_COMPLETE=true
T2_COMPLETE=true
T3_COMPLETE=true
T4_COMPLETE=true
T5_COMPLETE=true
T6_COMPLETE=true
T7_COMPLETE=true
T8_COMPLETE=true

BOOTSTRAP_DO_NOT_IMPLEMENT_CHG0024=HISTORICAL_SUPERSEDED_BY_20260823_AUTONOMOUS_AUTHORIZATION
ITEM_SYNC_EXECUTION_APPROVED=true_CONDITIONAL_AFTER_T6_GATES
PRODUCTION_ACTIVATION_APPROVED=true
QR_RESTORATION_NOT_PERFORMED=true
QR_RESTORATION_FOLLOWUP=CHG-0025-web-self-service-qr-account-recovery
GIT_MAIN_INTEGRATION=PASS
RUNTIME_ACCEPTANCE=PASS
PR_37_MERGED=true
FINAL_STATUS=ARCHIVED
CHG0024_RUNTIME_ACCEPTANCE=PASS
ITEM_SYNC_RESULT=SUCCESS
NEGATIVE_CONTROLS_PRESERVED=true
QR_RESTORATION_NOT_YET_PERFORMED=true

## Upstream capability audit

The read-only audit already proved the existing full-account owner and two auth-recovery callsites. Bootstrap persists that authority only.

## Pinned upstream evidence

Fresh XIANYU main base: `c9289081d3ec69d6f44b1a7259bf4760e3f0f081`. Exact audit authority hashes are recorded in the Change evidence.

## Existing local implementation search

Existing owner: `ItemService.fetch_all_items_from_account`. No safe full-account entrypoint exists; the single-page primitive is not a replacement owner.

## Reuse decision

REUSE_DECISION=PATCH_EXISTING_OWNER
Project policy decision: `PATCH_UPSTREAM`.

## Duplicate implementation risk

Do not create a second Item Sync owner/service/scheduler/worker or Session/Cookie/Token lifecycle owner.

## Why upstream cannot satisfy the requirement as-is

The existing full-account owner has two auth-recovery callsites and no Item-specific no-auth-recovery mode.

## Approved exception ADR

Not applicable.

## Component owner

Existing XIANYU ItemService full-account sync owner.

## Retirement plan for overlapping local code

No overlap may be created; retire a minimal patch if upstream later provides an equivalent verified contract.
