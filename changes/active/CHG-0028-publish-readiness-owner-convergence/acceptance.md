# CHG-0028 Acceptance

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: APPROVED

## Entry gate

`OWNER_APPROVAL_RECEIVED=true`

- the project owner explicitly approved `CHG-0028-publish-readiness-owner-convergence` on 2026-08-24;
- the scope remains Publisher readiness only;
- CHG0027 remains archived and production-frozen;
- the Browser fixed-target access follow-up remains separate.

## Required evidence

The complete pre-implementation record is persisted at `evidence/20260824-t1-t3-read-only-owner-audit-and-stop-decision.md` and includes:

- freshly fetched upstream SHA and current XIANYU main/local/remote SHAs;
- deployed Backend, WebSocket, and Scheduler image identities plus candidate-owner source hashes;
- the native point-in-time capability producer, Accounts readiness consumer, selected-account trigger, and exact missing transition;
- deterministic lazy-pending, positive-control `READY`, fatal-blocker, and mocked-producer results;
- upstream-first category `PATCH_UPSTREAM` with `EXECUTION_DECISION=STOP`, because no existing transition satisfies the consumer without a new writer or contract replacement.

After a separately approved implementation:

- exact changed-file list and preimage/postimage hashes;
- deterministic tests for READY, lazy pending, fail-closed blockers, and transient/unknown handling;
- relevant CHG0026/CHG0027 regression results if shared composition code is touched;
- component-specific build/deployment evidence when source changed;
- sanitized read-only or synthetic runtime evidence;
- exact commit, remote, PR, CI, merge, and final main SHAs.

## Scoped acceptance criteria

- an authoritative native readiness signal in the existing owner can converge the selected account to `READY`;
- no authoritative signal leaves the result truthfully lazy/pending or not ready;
- fatal authentication, platform-verification, and session blockers remain fail-closed;
- transient failures do not create a false Session-expired state;
- selected-account and owner scope remain intact;
- normal Direct/Personal Publisher execution remains Browser-independent;
- no second readiness owner, writer, service, table, schema, state machine, scheduler, or adapter-side truth source is introduced;
- all changed runtime source is proven deployed before any runtime acceptance claim;
- CHG0028-specific CI and deterministic tests pass.

## Safety acceptance

The complete Change must record:

`REAL_MESSAGES_SENT=0`

`REAL_PRODUCTS_PUBLISHED=0`

`REAL_PRODUCTS_MODIFIED=0`

`NEW_ITEM_SYNC_INVOCATION_COUNT=0`

`QR_LOGIN_INVOCATION_COUNT=0`

`MANUAL_RECONNECT_INVOCATION_COUNT=0`

`PRODUCTION_ACCOUNT_MUTATION_COUNT=0`

## Explicit non-acceptance

The following do not count as CHG0028 failure or success:

- whether an authorized Browser can render the fixed local XIANYU frontend;
- Browser port policy, CDP access, Playwright, or persistent-profile readiness;
- general UI visual acceptance;
- unrelated global CI debt that is independently reproduced on clean main;
- Publisher business success inferred only from HTTP 200 or submission acknowledgement.

## Stop acceptance

Stopping is the correct outcome if current evidence proves that convergence needs a new owner, persistence model, writer, schema, Browser dependency, or real production publish. Such a result must be returned to the project owner instead of expanding this Change.

`STOP_ACCEPTANCE=PASS`

`STOP_REASON=NEW_READINESS_WRITER_OR_CONSUMER_CONTRACT_CHANGE_REQUIRED`

`IMPLEMENTATION_AUTHORIZED=false`

T1-T3 proved that the current native producer is point-in-time only and the deployed Accounts consumer requires an unwritten persisted record. Enabling the newer upstream route alone is insufficient; polling it from account status can invoke the existing Cookie update path. T4-T8 therefore remain blocked pending a separate project-owner contract decision.
