# CHG-0028 Tasks

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: VERIFYING

- [x] T1 Fresh-fetched upstream and recorded current GitHub, local, runtime, and upstream SHAs plus the exact Publisher capability producer / Accounts readiness consumer ownership map.
- [x] T2 Reproduced lazy pending deterministically and proved the missing native transition without real publish, external MTOP, Browser, or production mutation.
- [x] T3 Finalized `REUSE_DECISION=PATCH_UPSTREAM` with `EXECUTION_DECISION=STOP`: a new readiness writer or explicit Accounts consumer-contract replacement requires a separate project-owner decision.
- [x] T4 UNBLOCKED — project owner approved `SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY`; implement without a lineage-aware writer, persisted readiness, Browser scope, account-list polling producer, or second owner.
- [x] T5 Implement only the proven existing-owner adoption, configuration, or patch while preserving Publisher routing, selected-account on-demand scope, fail-closed blockers, and no-Browser invariants.
- [x] T6 Run targeted Publisher readiness tests, relevant CHG0026/CHG0027 regressions, repository validation, generated-state checks, and diff-scope review.
- [x] T7 Production-frozen source-only acceptance: component patch clean-applies and deterministic behavior tests pass; no deployment, container restart, real publish, QR, reconnect, Item Sync, messaging, Browser, or account mutation was performed or claimed.
- [ ] T8 Persist exact evidence, commit with precise staging, push normally, verify remote SHA, open a main-based PR, classify CI truthfully, and merge only after scoped acceptance passes.

## Execution gate

`OWNER_APPROVAL_RECEIVED=true`

`T1_T3_AUDIT_COMPLETE=true`

`STOP_CONDITION_TRIGGERED=NEW_READINESS_WRITER_OR_CONSUMER_CONTRACT_CHANGE_REQUIRED`

`IMPLEMENTATION_AUTHORIZED=false`

T1-T3 are complete within the Publisher-only boundary. T4-T8 remain blocked. Browser work and every production mutation remain prohibited.

## 2026-08-25 execution update

`CHG0028_OWNER_CONTRACT_DECISION=APPROVED__SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY`

`IMPLEMENTATION_AUTHORIZED=true`

`GLOBAL_PERSISTED_PUBLISH_READINESS=DEPRECATED`

`LINEAGE_AWARE_READINESS_WRITER=NOT_AUTHORIZED`

T8 is now the single unfinished persistence task. T7 completed as production-frozen source-only acceptance; no production mutation is authorized by this task.
