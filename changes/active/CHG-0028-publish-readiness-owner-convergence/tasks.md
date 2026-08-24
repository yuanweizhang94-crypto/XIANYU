# CHG-0028 Tasks

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: DRAFT

- [ ] T1 After explicit approval, fresh-fetch upstream and record current GitHub, local, runtime, and upstream SHAs plus the existing Publisher readiness producer/consumer ownership map.
- [ ] T2 Reproduce the lazy-pending state with deterministic or read-only evidence and prove the exact missing native transition without real publish or production mutation.
- [ ] T3 Finalize the upstream-first reuse decision; stop and return for separate approval if any new owner, writer, schema, table, Browser dependency, or local exception is required.
- [ ] T4 Move the Change to IMPLEMENTING only with the exact approved scope, then add failing deterministic acceptance tests before a minimal existing-owner patch.
- [ ] T5 Implement only the proven existing-owner adoption, configuration, or patch while preserving Publisher routing, selected-account scope, fail-closed blockers, and no-Browser invariants.
- [ ] T6 Run targeted Publisher readiness tests, relevant CHG0026/CHG0027 regressions, repository validation, generated-state checks, and diff-scope review.
- [ ] T7 If source changed, perform component-specific deployment and sanitized production-safe acceptance without real publish, QR, reconnect, Item Sync, messaging, or account mutation.
- [ ] T8 Persist exact evidence, commit with precise staging, push normally, verify remote SHA, open a main-based PR, classify CI truthfully, and merge only after scoped acceptance passes.

## Execution gate

DRAFT permits reading and review only. No task above is executable until the project owner explicitly approves this exact Publisher-only Change.
