# CHG-0028 Design

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: ARCHIVED

## Design intent

Converge Publisher readiness inside the existing authoritative owner. This Change does not redesign Publisher execution and does not make Browser readiness a publish gate.

## Authority and ordering

Use the following order for every finding:

1. current GitHub and active Change;
2. current local source;
3. current production runtime source/hash and read-only state;
4. freshly fetched current upstream;
5. archived evidence and historical documentation.

Repository HEAD, runtime deployment, and upstream SHA must remain separately identified.

## Completed investigation boundary

T1-T3 completed the approved read-only phase:

1. the deployed Accounts consumer accepts `session_maintenance.consumers.publish.state=READY` as its only positive readiness record;
2. the existing native producer is `PublishAccountCapabilityService.detect -> mtop.idle.pc.idleitem.preget`;
3. the current upstream Product Publish page invokes that producer after selected-account change and holds the result only in component state;
4. the pinned upstream, fresh upstream, current XIANYU branch, runtime images/source hashes, Session writers, and COMPANY thin adapter were compared separately;
5. deterministic evidence proved the exact missing transition between point-in-time producer success and the persisted record consumed by Accounts.

Evidence: `evidence/20260824-t1-t3-read-only-owner-audit-and-stop-decision.md`.

## T3 design decision

`REUSE_DECISION=PATCH_UPSTREAM`

`EXECUTION_DECISION=STOP`

- `ADOPT_UPSTREAM` is insufficient: the newer route/UI yields ephemeral selected-account capability but does not update the deployed Accounts contract.
- `CONFIGURE_UPSTREAM` is unavailable: no existing configuration connects the producer result to `consumers.publish`.
- `PATCH_UPSTREAM` cannot proceed under this approval: persisted convergence requires a new lineage-aware readiness writer, while avoiding persistence requires an explicit retirement/replacement of the current Accounts contract.
- invoking the native MTOP probe from the Accounts polling path is rejected because it is not the upstream-native trigger, fans out calls, and can enter the established Cookie update path after token refresh.

The original T1-T3 design stopped before IMPLEMENTING because a separate project-owner decision was required.

## T4 owner decision

`CHG0028_OWNER_CONTRACT_DECISION=APPROVED__SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY`

The approved contract is selected-account on-demand capability:

- keep `PublishAccountCapabilityService.detect -> mtop.idle.pc.idleitem.preget` as the only native Publisher capability producer;
- expose the existing upstream-style selected-account route, `/product-publish/accounts/{account_id}/capability`, for explicit capability checks;
- do not project selected-account success into `session_maintenance.consumers.publish`;
- do not create a lineage-aware writer, readiness table, scheduler, background producer, cache, Browser gate, or COMPANY-side truth source;
- represent global/unchecked Publisher capability as `mode=ON_DEMAND`, `checked=false`, and `state=NOT_CHECKED` or equivalent wire-compatible fields.

This is a `PATCH_UPSTREAM` continuation because fresh upstream already provides the selected-account route/service workflow, while the current deployed/patch source still needs the route adoption and Accounts consumer contract replacement.

## Readiness truth model

| Authoritative condition | Required outward state |
|---|---|
| Existing native readiness evidence is present for the selected account and current lineage | `READY` |
| Selected-account capability has not been explicitly checked | `ON_DEMAND` / `NOT_CHECKED`; `checked=false`; never false `READY` |
| Confirmed authentication, platform-verification, or fatal session blocker applies | Existing fail-closed blocker; never `READY` |
| Transient transport/upstream failure prevents a current determination | Existing temporary/retry-later semantics; never a false fatal session label |
| Evidence is missing or contradictory | Not ready / unknown according to the existing contract; never fabricated `READY` |

The exact field names and transition owner must be filled from T1 evidence rather than invented here.

## Ownership constraints

- normal publish remains `detect_publish_account_capability -> XianyuDirectPublisher / XianyuPersonalPublisher`;
- XIANYU Backend/current upstream path owns capability truth;
- COMPANY_LOCAL_EXECUTION_TOOL remains a thin status consumer and business bridge;
- Browser, Playwright, persistent profile, and fixed-target rendering are not Publisher readiness producers or gates;
- no second Publisher, readiness service, state machine, table, cache, writer, scheduler, or supervisor is allowed.

## Test design

The completed read-only reproduction proves missing record -> `RETRY_LATER`, synthetic existing-contract `READY` record -> `READY`, and fatal Session evidence -> fail closed. It also proves a mocked native capability success does not produce the consumed record.

If a separately approved implementation follows, it must first add deterministic tests that prove:

- an existing native authoritative signal produces `READY`;
- absence of selected-account on-demand checking is represented as `ON_DEMAND`/`NOT_CHECKED` and never becomes false `READY`, permanent pending, or Session invalid;
- fatal blockers remain fail-closed;
- transient failures do not become false Session-expired outcomes;
- selected-account and owner scope are preserved;
- normal Direct/Personal Publisher paths do not acquire a Browser prerequisite;
- no real publish or production mutation is needed for acceptance.

Additional owner-decision tests must prove the account list / periodic polling path does not call `PublishAccountCapabilityService.detect`, `mtop.idle.pc.idleitem.preget`, preget, MTop, or any capability producer.

Regression selection must be component-specific and include the relevant CHG0026/CHG0027 safety tests if shared Session/capability composition is touched.

## Runtime validation design

No runtime validation or activation is authorized by the current approval because T3 stopped. If a later separately approved source patch is required, build and replace only the owning component, then verify health, runtime source/hash, and sanitized synthetic readiness output. Real publish, real item mutation, QR login, manual reconnect, message send, and production account-state writes remain prohibited.

## Rollback

Before any approved runtime change, record the exact preimage, image/container identity, and source hash. Roll back only the affected component to that pinned preimage. Do not roll back CHG0027 or its production-accepted patch.

## Archive transition

`PR_NUMBER=41`

`MERGE_COMMIT_SHA=4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89`

CHG-0028 is archived after GitHub merge. Runtime deployment and three-capability closure now belong to `CHG-0029-core-capability-closure`.

## Separate Browser follow-up

`AUTHORIZED_BROWSER_CANNOT_RENDER_FIXED_LOCAL_XIANYU_FRONTEND` is intentionally absent from the design. Resolving it belongs to a separate COMPANY_LOCAL_EXECUTION_TOOL / authorized Browser change and cannot be used as a CHG0028 acceptance gate.
