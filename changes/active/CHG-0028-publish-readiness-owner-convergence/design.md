# CHG-0028 Design

Change ID: CHG-0028-publish-readiness-owner-convergence
Status: DRAFT

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

## Planned investigation boundary

After explicit approval, the first phase is read-only:

1. identify every current Publisher readiness consumer and the status vocabulary it accepts;
2. identify any existing producer, native trigger, persisted field, event, or derived signal;
3. trace the native Direct/Personal Publisher workflow without invoking a real publish;
4. compare pinned upstream, current upstream, local patch, and deployed runtime;
5. prove whether the gap is adoption, configuration, wiring, or an existing-owner defect.

No implementation phase begins until this evidence is recorded and the reuse decision remains valid.

## Conditional minimal design

Only one of these outcomes may follow the audit:

- `ADOPT_UPSTREAM`: use an already-present producer without a local rewrite;
- `CONFIGURE_UPSTREAM`: enable or connect an already-present native producer;
- `PATCH_UPSTREAM`: minimally repair the existing producer/consumer transition in its current owner;
- stop: if the result requires `WRAP_FOR_OPERATIONS`, `BUILD_LOCAL_EXCEPTION`, a new writer, or another owner, return for a separate approval decision.

The DRAFT default is `PATCH_UPSTREAM`; it is not implementation authorization.

## Readiness truth model

| Authoritative condition | Required outward state |
|---|---|
| Existing native readiness evidence is present for the selected account and current lineage | `READY` |
| Native workflow has not yet produced authoritative readiness evidence | `LAZY_PENDING` / existing retry-later semantics |
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

An approved implementation must first add deterministic tests that prove:

- an existing native authoritative signal produces `READY`;
- absence of that signal remains lazy/pending and never becomes false `READY`;
- fatal blockers remain fail-closed;
- transient failures do not become false Session-expired outcomes;
- selected-account and owner scope are preserved;
- normal Direct/Personal Publisher paths do not acquire a Browser prerequisite;
- no real publish or production mutation is needed for acceptance.

Regression selection must be component-specific and include the relevant CHG0026/CHG0027 safety tests if shared Session/capability composition is touched.

## Runtime validation design

If an approved source patch is required, build and replace only the owning component, then verify health, runtime source/hash, and sanitized read-only readiness output. A synthetic or existing passive native transition is preferred. Real publish, real item mutation, QR login, manual reconnect, message send, and account-state writes are prohibited.

## Rollback

Before any approved runtime change, record the exact preimage, image/container identity, and source hash. Roll back only the affected component to that pinned preimage. Do not roll back CHG0027 or its production-accepted patch.

## Separate Browser follow-up

`AUTHORIZED_BROWSER_CANNOT_RENDER_FIXED_LOCAL_XIANYU_FRONTEND` is intentionally absent from the design. Resolving it belongs to a separate COMPANY_LOCAL_EXECUTION_TOOL / authorized Browser change and cannot be used as a CHG0028 acceptance gate.
