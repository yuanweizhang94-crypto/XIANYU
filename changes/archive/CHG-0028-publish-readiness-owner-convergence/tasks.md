# CHG-0028 Tasks

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: ARCHIVED

- [x] T1 Fresh-fetched upstream and recorded current GitHub, local, runtime, and upstream SHAs plus the exact Publisher capability producer / Accounts readiness consumer ownership map.
- [x] T2 Reproduced lazy pending deterministically and proved the missing native transition without real publish, external MTOP, Browser, or production mutation.
- [x] T3 Finalized `REUSE_DECISION=PATCH_UPSTREAM` with `EXECUTION_DECISION=STOP`: a new readiness writer or explicit Accounts consumer-contract replacement requires a separate project-owner decision.
- [x] T4 UNBLOCKED — project owner approved `SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY`; implement without a lineage-aware writer, persisted readiness, Browser scope, account-list polling producer, or second owner.
- [x] T5 Implement only the proven existing-owner adoption, configuration, or patch while preserving Publisher routing, selected-account on-demand scope, fail-closed blockers, and no-Browser invariants.
- [x] T6 Run targeted Publisher readiness tests, relevant CHG0026/CHG0027 regressions, repository validation, generated-state checks, and diff-scope review.
- [x] T7 Production-frozen source-only acceptance: component patch clean-applies and deterministic behavior tests pass; no deployment, container restart, real publish, QR, reconnect, Item Sync, messaging, Browser, or account mutation was performed or claimed.
- [x] T8 Persist exact evidence, commit with precise staging, push normally, verify remote SHA, open a main-based PR, classify CI truthfully, and merge only after scoped acceptance passes. COMPLETE: PR #41 merged to current main at `4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89`; CHG0028 runtime activation remains outside this archived source/GitHub Change.

## Execution gate

`OWNER_APPROVAL_RECEIVED=true`

`T1_T3_AUDIT_COMPLETE=true`

`STOP_CONDITION_TRIGGERED=NEW_READINESS_WRITER_OR_CONSUMER_CONTRACT_CHANGE_REQUIRED`

`IMPLEMENTATION_AUTHORIZED=false`

T1-T3 are complete within the Publisher-only boundary and recorded the historical stop reason. The 2026-08-25 owner decision unblocked T4-T7 for the selected-account on-demand contract. T8 remains the only unfinished GitHub persistence and merge-closure task. Browser work and every production mutation remain prohibited.

## 2026-08-25 execution update

`CHG0028_OWNER_CONTRACT_DECISION=APPROVED__SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY`

`IMPLEMENTATION_AUTHORIZED=true`

`GLOBAL_PERSISTED_PUBLISH_READINESS=DEPRECATED`

`LINEAGE_AWARE_READINESS_WRITER=NOT_AUTHORIZED`

T8 is now the single unfinished persistence and merge-closure task. T7 completed as production-frozen source-only acceptance; no production mutation is authorized by this task.

## 2026-08-25 GitHub persistence checkpoint

`IMPLEMENTATION_COMMIT_SHA=95c4675c5dae785fab801affa85cd1975892cd7e`

`REMOTE_BRANCH=feat/CHG-0028-publish-readiness-owner-convergence`

`REMOTE_BRANCH_SHA=95c4675c5dae785fab801affa85cd1975892cd7e`

`MERGE_COMMIT_SHA=4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89`

`REMOTE_MAIN_SHA=4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89`

`PR_NUMBER=41`

`PR_URL=https://github.com/yuanweizhang94-crypto/XIANYU/pull/41`

`PR_HEAD_SHA=95c4675c5dae785fab801affa85cd1975892cd7e`

`PR_BASE_SHA=dc83ef23603c1725d3babcd8f89f54db0592f075`

`TRUSTED_BASELINE_GOVERNANCE_TRANSITION=42d0aa8_docs_archive_CHG0027_and_draft_CHG0028`

`PR_SCOPE_CLEAN=true`

`CHG0028_SPECIFIC_CI=PASS_BY_LOG_CLASSIFICATION`

`GLOBAL_CI_STATUS=FAIL_UNRELATED_PRE_EXISTING_GOVERNANCE_DEBT`

`CHG0020_DEBT_ABSORBED=false`

Initial PR CI for head `95c4675c5dae785fab801affa85cd1975892cd7e`: security passed; quality failed on pre-existing CHG-0020 archive validation debt; broad tests failed on unrelated existing governance tests for CHG-0020, CHG-0022 active evidence path assumptions, and README/AGENTS governance drift. No failed log points to CHG-0028 selected-account on-demand behavior, Browser scope, production mutation, or persisted readiness writer creation.
