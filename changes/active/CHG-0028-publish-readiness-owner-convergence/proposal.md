# CHG-0028 Publisher Readiness Owner Convergence

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: VERIFYING
Created: 2026-08-24
Predecessor: CHG-0027-session-transient-classification-qr-cooldown-lineage

## Trigger

CHG0027 is formally closed by PR #40 and merge commit `dc83ef23603c1725d3babcd8f89f54db0592f075`. Its scoped production acceptance passed. The remaining Publisher follow-up is independently classified as:

`PUBLISH_READINESS_LAZY_PENDING_NO_READY_PRODUCER`

The CHG0027 evidence shows existing Publisher readiness consumers can remain `LAZY_PENDING`, while no current authoritative `READY` producer was found. This is not a CHG0027 acceptance failure.

## User outcome

Make Publisher readiness converge truthfully through the existing upstream/current owner so an account is reported `READY` only when authoritative native readiness evidence exists. Preserve truthful `LAZY_PENDING` and fail-closed blockers when that evidence does not exist.

## Execution contract

User outcome: expose Publisher capability truth only for the selected account or an explicit on-demand request, using the existing Backend native capability owner.

Confirmed blocker: the previous Accounts-level persisted readiness contract expected an unwritten `session_maintenance.consumers.publish` record and misrepresented unprobed accounts as a stuck readiness problem.

Smallest success test: deterministic tests prove unprobed global/account-list Publisher status is `ON_DEMAND`/not checked, selected-account capability calls `PublishAccountCapabilityService.detect` exactly once when explicitly requested, and no persisted Publisher readiness writer or polling producer exists.

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

T1-T3 are complete. Fresh upstream main contains a selected-account capability route and UI workflow backed by `PublishAccountCapabilityService.detect -> mtop.idle.pc.idleitem.preget`. The result is point-in-time capability evidence held by the native Product Publish page; it is not persisted into the separate Accounts readiness contract. Production Runtime contains the same capability service and normal Direct/Personal routing, but not the newer capability route. The deployed Accounts consumer still requires `session_maintenance.consumers.publish.state=READY`, and no Backend, WebSocket, or Scheduler path writes that record.

Evidence: `evidence/20260824-t1-t3-read-only-owner-audit-and-stop-decision.md`.

## Pinned upstream evidence

The production-source upstream checkout remains pinned at `bda1a859df63fa5f24e51398fa80a23490bb6dfc`. T1 fresh-fetched upstream main at `29dc831d4498f3174f0502c989a352ef59815553`. The selected-account capability service/route/UI was introduced by upstream commit `5984b483b5bfd6c852ef00c22291b1bf163022ee`; those paths are absent from the pinned commit. Runtime contains the service but not the newer route registration. These separately identified revisions are comparison evidence, not permission to implement.

## Existing local implementation search

The completed bounded search covered the deployed Backend, WebSocket, Scheduler, COMPANY thin adapter, current upstream Publisher route/service/frontend workflow, CHG0027 evidence, and prior Publisher recovery history. The only `consumers.publish` handling is the Backend Accounts reader plus an explicit QR comment that Publisher consumers remain lazy. `set_session_maintenance_state` replaces the Session record without creating Publisher readiness. COMPANY reads sanitized account details and owns no Publisher state. No existing readiness writer, configuration switch, table, schema, cache, or event projection was found.

## Reuse decision

Decision: PATCH_UPSTREAM

Execution decision: STOP

`ADOPT_UPSTREAM` alone is insufficient because the fresh upstream route produces only ephemeral selected-account capability and does not feed the deployed Accounts consumer. No configuration connects the two contracts. Calling the MTOP probe from the four-second Accounts polling path is not the native workflow and can invoke the existing Cookie update path after token refresh. Persisted convergence requires a new lineage-aware readiness writer, while non-persisted convergence requires an explicit replacement of the current Accounts readiness contract. Either choice crosses the approved stop boundary and requires a separate project-owner decision.

`PATCH_UPSTREAM` is the only remaining upstream-first category, but it remains unavailable under the current approval. No code implementation, runtime activation, or production operation is authorized.

## Duplicate implementation risk

Creating readiness state in COMPANY_LOCAL_EXECUTION_TOOL, Browser automation, or a new XIANYU service would duplicate Publisher ownership and allow repository, runtime, and adapter truth to diverge. The adapter may consume authoritative status but must not become its producer.

## Why upstream cannot satisfy the requirement

The exact gap is now proven: `detect_publish_account_capability` can return authoritative point-in-time success, but no transition projects that success into `session_maintenance.consumers.publish.state=READY`. Fresh upstream keeps its result only in the selected Product Publish page's component state. Enabling the route does not update the Accounts consumer. A new readiness writer or an explicit consumer-contract replacement is therefore required, and both are outside this approval.

## Approved exception ADR

Not applicable. This Change does not authorize `BUILD_LOCAL_EXCEPTION`. Any finding that requires one is a stop condition and needs a separate project-owner decision plus an approved ADR.

## Component owner

The existing XIANYU Backend remains the only candidate owner: `PublishAccountCapabilityService.detect` produces point-in-time native capability and `cookies.py::_build_business_capabilities` consumes the separate Accounts readiness contract. COMPANY_LOCAL_EXECUTION_TOOL remains a thin consumer/bridge. Browser infrastructure remains out of scope. No second owner is proposed or authorized.

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

`T1_T3_AUDIT_COMPLETE=true`

`STOP_CONDITION_TRIGGERED=NEW_READINESS_WRITER_OR_CONSUMER_CONTRACT_CHANGE_REQUIRED`

`IMPLEMENTATION_AUTHORIZED=false`

The approved read-only investigation is complete. T4 and every code/runtime/production action are blocked pending a separate project-owner decision.

## 2026-08-25 owner contract decision

`CHG0028_OWNER_CONTRACT_DECISION=APPROVED__SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY`

`GLOBAL_PERSISTED_PUBLISH_READINESS=DEPRECATED`

`LINEAGE_AWARE_READINESS_WRITER=NOT_AUTHORIZED`

`IMPLEMENTATION_AUTHORIZED=true`

The project owner selected the non-persisted contract option identified by T1-T3: Publisher capability is computed only for a selected account or another explicit on-demand request. The Accounts/global overview must express unchecked Publisher capability as `ON_DEMAND`/`NOT_CHECKED` instead of `READY`, permanent `PENDING`, system fault, or Session invalid. This decision does not authorize a lineage-aware readiness writer, a new table, a scheduled producer, a background probe, a Browser gate, or a second owner.

## Continuation reuse decision

Decision: PATCH_UPSTREAM

Execution decision: CONTINUE_SELECTED_ACCOUNT_ON_DEMAND

The upstream native path already exists in fresh upstream: `GET /product-publish/accounts/{account_id}/capability` calls `PublishAccountCapabilityService.detect` for the selected account. The minimal patch is to adopt that route shape in the existing Backend owner where absent and replace the old global persisted-readiness expectation with an explicit on-demand/not-checked outward contract. `ADOPT_UPSTREAM` alone is still insufficient because deployed source lacks the route registration and the existing Accounts readiness consumer still describes the missing persisted record as pending readiness. `CONFIGURE_UPSTREAM` remains unavailable. No `BUILD_LOCAL_EXCEPTION` is authorized.

## Updated duplicate implementation risk and rollback

Duplicate-development risk: low only if the patch stays inside the existing Backend route/consumer and uses `PublishAccountCapabilityService.detect`; high if COMPANY, Browser, Scheduler, Session maintenance, or a new persisted readiness owner produces Publisher truth.

Rollback: remove the CHG-0028 upstream patch layer and return to the previous CHG0027 behavior. No database cleanup, Profile cleanup, Cookie mutation, production account mutation, or persisted readiness data migration is required because this option does not write readiness.
