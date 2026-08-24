# CHG-0028 Acceptance

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: DRAFT

## Entry gate

- the project owner explicitly approves `CHG-0028-publish-readiness-owner-convergence`;
- the scope remains Publisher readiness only;
- CHG0027 remains archived and production-frozen;
- the Browser fixed-target access follow-up remains separate.

## Required evidence

Before implementation:

- freshly fetched upstream SHA;
- current XIANYU main/local SHA;
- deployed runtime source/hash for every candidate owning component;
- exact readiness producer, consumers, native trigger, state contract, and account/lineage scope;
- an upstream-first decision supported by current evidence;
- a recorded stop decision if no existing owner can satisfy the requirement.

After an approved implementation:

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
