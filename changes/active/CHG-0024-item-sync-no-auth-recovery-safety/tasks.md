# CHG-0024 Tasks

Status: APPROVED

Change ID: CHG-0024-item-sync-no-auth-recovery-safety

- [x] T1 Capability audit and formal scope lock: persist the existing owner chain, two authentication-recovery callsites, reuse decision, safety invariants, failed-closed prior attempt, and commander authorization without runtime implementation or production execution.
- [ ] T2 Exact implementation diff design against current source.
- [ ] T3 Implement Item-specific no-auth-recovery safe mode in the existing Item owner.
- [ ] T4 Add targeted deterministic implementation tests for both authentication-recovery callsites.
- [ ] T5 Update the existing COMPANY `xianyu_item_sync` thin-adapter fixed-safe-mode mapping only if proven necessary.
- [ ] T6 Controlled candidate/runtime validation with zero business writes.
- [ ] T7 One newly authorized controlled fresh Item Sync.
- [ ] T8 Negative-control post-check and formal persistence.

T1_COMPLETE=true
T2_COMPLETE=false
T3_COMPLETE=false
T4_COMPLETE=false
T5_COMPLETE=false
T6_COMPLETE=false
T7_COMPLETE=false
T8_COMPLETE=false

DO_NOT_IMPLEMENT_CHG0024=true for this bootstrap phase.
ITEM_SYNC_EXECUTION_APPROVED=false
PRODUCTION_ACTIVATION_APPROVED=false
QR_RESTORATION_APPROVED=false

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
