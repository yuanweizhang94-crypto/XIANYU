# CHG-0028 Publisher Readiness Owner Convergence

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: APPROVED
Created: 2026-08-24
Predecessor: CHG-0027-session-transient-classification-qr-cooldown-lineage

## Trigger

CHG0027 is formally closed by PR #40 and merge commit `dc83ef23603c1725d3babcd8f89f54db0592f075`. Its scoped production acceptance passed. The remaining Publisher follow-up is independently classified as:

`PUBLISH_READINESS_LAZY_PENDING_NO_READY_PRODUCER`

The CHG0027 evidence shows existing Publisher readiness consumers can remain `LAZY_PENDING`, while no current authoritative `READY` producer was found. This is not a CHG0027 acceptance failure.

## User outcome

Make Publisher readiness converge truthfully through the existing upstream/current owner so an account is reported `READY` only when authoritative native readiness evidence exists. Preserve truthful `LAZY_PENDING` and fail-closed blockers when that evidence does not exist.

## Scope

Approved scope:

- refresh current upstream, local, and runtime read-only evidence for the existing Publisher readiness producer and consumers;
- identify the native event or state transition that should produce authoritative readiness;
- make the smallest change inside the existing owner if a confirmed wiring, trigger, or missing transition defect exists;
- add deterministic tests, sanitized evidence, and only the component-specific deployment validation required by an approved implementation.

Explicitly excluded:

- Browser UI access, fixed local URL rendering, port allowlists, CDP, Playwright, or browser-profile work;
- changes to normal Direct/Personal Publisher ownership or account-capability routing;
- Session, Cookie, QR, WebSocket, Chat, Auto Reply, Item Sync, or Scheduler redesign;
- a second Publisher, readiness service, state machine, table, schema, writer, or supervisor;
- real publish, real item mutation, QR login, manual reconnect, real message send, or production account-state mutation.

The separate follow-up `AUTHORIZED_BROWSER_CANNOT_RENDER_FIXED_LOCAL_XIANYU_FRONTEND` remains owned outside this Change by COMPANY_LOCAL_EXECUTION_TOOL / authorized Browser infrastructure.

## Current evidence lock

- CHG0027 formal patch SHA256: `e3f42b96dd7bedc833a0e44f0397626ef48e133a57c463ae6e0ef5e193249b31`
- CHG0027 formal commit: `56698c0520a4d324584c3ab48389ccc7739a7cbb`
- CHG0027 merge/main commit: `dc83ef23603c1725d3babcd8f89f54db0592f075`
- CHG0027 scoped production acceptance: `PASS`
- Production freeze at transition: `true`
- Follow-up evidence: `changes/archive/CHG-0027-session-transient-classification-qr-cooldown-lineage/evidence/20260824-scoped-production-acceptance-and-formal-persistence.md`

## Upstream capability audit

Approval-stage finding: the Publisher executor, account-capability routing, and readiness consumers already exist. CHG0027 found no current authoritative `READY` producer. T1 must fresh-fetch and map the pinned upstream, current local source, runtime source/hash, native workflow, producer, consumers, and ownership before any implementation proposal is executable.

## Pinned upstream evidence

The inherited CHG0027 comparison evidence pins the production-source upstream checkout at `bda1a859df63fa5f24e51398fa80a23490bb6dfc` and records then-current upstream main `29dc831d4498f3174f0502c989a352ef59815553` for comparison only. These are historical input, not permission to implement. T1 must record a fresh upstream fetch SHA and runtime/source comparison before T1 can complete or this Change can move to IMPLEMENTING.

## Existing local implementation search

CHG0027 already established that readiness consumers can emit lazy `RETRY_LATER` / `LAZY_PENDING` and that normal Publisher execution remains in the existing upstream/current Publisher owners. CHG0028 must search those owners and their existing status composition, events, persistence, and tests. It must not infer that absence of a discovered producer authorizes a new one.

## Reuse decision

Decision: PATCH_UPSTREAM

This is the APPROVED audit default: repair only a proven defect in the existing upstream/current owner. If the fresh audit proves configuration or direct adoption is sufficient, the decision must narrow to `CONFIGURE_UPSTREAM` or `ADOPT_UPSTREAM` before approval. If satisfying the requirement needs a new owner, schema, table, writer, or parallel state machine, execution stops and requires a separately approved exception.

## Duplicate implementation risk

Creating readiness state in COMPANY_LOCAL_EXECUTION_TOOL, Browser automation, or a new XIANYU service would duplicate Publisher ownership and allow repository, runtime, and adapter truth to diverge. The adapter may consume authoritative status but must not become its producer.

## Why upstream cannot satisfy the requirement

The current confirmed evidence shows the existing consumed state remains `LAZY_PENDING` and no authoritative `READY` producer was found. The exact missing native transition is not yet proven. Owner approval has been received; the upstream/current-owner audit is now the first executable investigation. Implementation remains prohibited until T1-T3 prove the exact native transition and confirm that this reuse decision still applies.

## Approved exception ADR

Not applicable. This Change does not authorize `BUILD_LOCAL_EXCEPTION`. Any finding that requires one is a stop condition and needs a separate project-owner decision plus an approved ADR.

## Component owner

The existing XIANYU Backend capability-composition and upstream Publisher path remain the only candidate execution owners. T1 must name the exact existing producer and consumers before code changes. COMPANY_LOCAL_EXECUTION_TOOL remains a thin consumer/bridge and Browser infrastructure is out of scope.

## Retirement plan for overlapping local code

No overlapping local implementation is planned or authorized. If an approved minimal patch is later required, it must carry an upstream retirement trigger and be removed when an equivalent upstream fix is adopted.

## Stop conditions

Stop without implementation if:

- no current native producer or existing owner can be identified;
- a new owner, persistence model, writer, schema, or parallel readiness state machine is required;
- Browser fixed-target access or UI rendering becomes necessary;
- evidence would require real publish, QR login, manual reconnect, Item Sync, real messaging, or production account mutation;
- the requested work would reopen CHG0026 or expand CHG0027.

## Approval gate

`OWNER_APPROVAL_RECEIVED=true`

`OWNER_APPROVAL_DATE=2026-08-24`

`OWNER_APPROVED_SCOPE=PUBLISHER_READINESS_ONLY`

`BROWSER_SCOPE_INCLUDED=false`

T1 read-only audit is authorized. Business implementation, runtime deployment, and production operations remain gated by the evidence and stop conditions in T1-T3.
