# CHG-0028 Tasks

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: APPROVED

- [x] T1 Fresh-fetched upstream and recorded current GitHub, local, runtime, and upstream SHAs plus the exact Publisher capability producer / Accounts readiness consumer ownership map.
- [x] T2 Reproduced lazy pending deterministically and proved the missing native transition without real publish, external MTOP, Browser, or production mutation.
- [x] T3 Finalized `REUSE_DECISION=PATCH_UPSTREAM` with `EXECUTION_DECISION=STOP`: a new readiness writer or explicit Accounts consumer-contract replacement requires a separate project-owner decision.
- [ ] T4 BLOCKED — do not move to IMPLEMENTING, add source tests, or patch runtime until the project owner separately chooses and approves the Backend readiness contract.
- [ ] T5 Implement only the proven existing-owner adoption, configuration, or patch while preserving Publisher routing, selected-account scope, fail-closed blockers, and no-Browser invariants.
- [ ] T6 Run targeted Publisher readiness tests, relevant CHG0026/CHG0027 regressions, repository validation, generated-state checks, and diff-scope review.
- [ ] T7 If source changed, perform component-specific deployment and sanitized production-safe acceptance without real publish, QR, reconnect, Item Sync, messaging, or account mutation.
- [ ] T8 Persist exact evidence, commit with precise staging, push normally, verify remote SHA, open a main-based PR, classify CI truthfully, and merge only after scoped acceptance passes.

## Execution gate

`OWNER_APPROVAL_RECEIVED=true`

`T1_T3_AUDIT_COMPLETE=true`

`STOP_CONDITION_TRIGGERED=NEW_READINESS_WRITER_OR_CONSUMER_CONTRACT_CHANGE_REQUIRED`

`IMPLEMENTATION_AUTHORIZED=false`

T1-T3 are complete within the Publisher-only boundary. T4-T8 remain blocked. Browser work and every production mutation remain prohibited.
