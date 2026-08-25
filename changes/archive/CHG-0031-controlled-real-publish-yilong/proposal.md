# CHG-0031 Controlled Real Publish Yilong

Change ID: CHG-0031-controlled-real-publish-yilong
Status: ARCHIVED
Created: 2026-08-25
Owner task: chg0031_single_writer

## User Outcome

User outcome: safely publish exactly one real sellable existing material through the existing unique upstream-native owner to the uniquely identified account labeled 艺龙 and keep it online.

Confirmed blocker: exact selected-account publish capability and one non-duplicate production-ready material must be proven; any trace/durable-truth gap must fail closed.

Smallest success test: one invocation, one platform item ACTIVE, local durable truth and remote/readback match, account item count +1, zero duplicate/extra items.

## Scope

Allowed scope:

- isolated worktree work under `D:/xianyu-worktrees/CHG-0031-controlled-real-publish-yilong`;
- active Change governance/evidence creation and generated state via `python scripts/generate_state.py`;
- narrow read-only pre-publish evidence through already-discovered production durable-truth paths;
- masked selected-account identity proof for the approved label `艺龙`;
- deterministic RED test plus smallest auditable `PATCH_UPSTREAM` artifact only if a real Phase 1 evidence defect blocks acceptance-grade proof.

Forbidden scope:

- modifying the dirty `D:/xianyu` CHG-0018 worktree;
- real publish before exact later commander token `GO_FOR_REAL_PUBLISH`;
- deploy, commit, push, runtime restart, Browser, UI, CDP, Playwright, QR, reconnect, account edit, item edit, offline, delete, message send, AI enablement, credential access, or credential logging;
- Fresh Item Sync invocation;
- second Publisher, second Material owner, second Account/Session/Cookie/Profile owner, second scheduler/worker, or COMPANY-side business truth source;
- absorbing CHG-0020, CHG-0022, README, or AGENTS debt into CHG-0031.

## Phase 1 Decision State

`REAL_PUBLISH_ALLOWED=false`

`COMMANDER_GO_FOR_REAL_PUBLISH=false`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

`REAL_PUBLISH_ACCEPTANCE=BLOCKED_NO_IDENTITY_BINDING`

`NO_GO_BLOCKER=APPROVED_LABEL_NOT_BOUND_IN_PRODUCTION_DURABLE_TRUTH`

Commander decision: `NO-GO_FOR_REAL_PUBLISH`. CHG-0031 is closed as a
blocked/no-go evidence Change with `PUBLISH_INVOCATIONS=0`.

## Upstream Capability Audit

Pinned upstream and local governance identify the native product publish workflow:

```text
Product Publish UI/API
-> /api/v1/product-publish/publish/batch
-> PublishExecutorService
-> execute_single_publish
-> detect_publish_account_capability
-> XianyuDirectPublisher / XianyuPersonalPublisher
-> MTOP
-> Publish Log
-> authoritative item sync/readback
```

The required business capability exists and must be reused through the formal COMPANY thin adapter `xianyu_publish_single` if a later GO is issued.

## Pinned Upstream Evidence

Pinned upstream checkout: `D:/xianyu-upstream-pilot`

Pinned upstream SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`

Evidence paths:

- `frontend/src/api/productPublish.ts`
- `backend-web/app/api/routes/product_publish.py`
- `backend-web/app/services/publish_execution_service.py`
- `common/services/publish_execution_service.py`
- `common/services/xianyu_publish_service.py`
- `docs/AI_PROJECT_HANDOFF.md`
- `docs/CURRENT_PRODUCTION_BASELINE.md`
- `docs/XIANYU_EXECUTION_AND_DEVELOPMENT_RULES.md`

## Existing Local Implementation Search

Local XIANYU and COMPANY records identify `xianyu_publish_single` as the formal single-product publish entry. Real publishing by `run_program`, `container_run`, temporary scripts, direct imports, manual MTOP calls, or a second Publisher is forbidden.

## Reuse Decision

Decision: ADOPT_UPSTREAM

CHG-0031 does not implement a publish path. It prepares the pre-publish checkpoint around the existing upstream-native owner.

## Duplicate Implementation Risk

Risk is low while Phase 1 remains read-only and any later publish uses only `xianyu_publish_single`. Risk becomes high if a temporary publish script, direct Publisher import, manual MTOP call, Browser/UI publisher, duplicate Material owner, duplicate account/session owner, or COMPANY-side durable truth model is introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream satisfies publish execution. It does not by itself choose the exact business account/material or produce this commander checkpoint; CHG-0031 supplies only governance and read-only evidence around the existing owner.

## Approved Exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not authorized.

## Component Owner

The publish business owner remains XIANYU upstream-native `detect_publish_account_capability -> XianyuDirectPublisher / XianyuPersonalPublisher -> MTOP`, reached through XIANYU Backend and the COMPANY `xianyu_publish_single` thin adapter.

## Retirement Plan For Overlapping Local Code

No overlapping local code is added.
