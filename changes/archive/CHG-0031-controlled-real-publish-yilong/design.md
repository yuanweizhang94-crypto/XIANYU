# CHG-0031 Design

Change ID: CHG-0031-controlled-real-publish-yilong
Status: ARCHIVED

## Design Intent

Prepare one controlled real publish to the exact account labeled 艺龙, but stop before the side effect. Phase 1 proves account identity, publish capability, item baseline, candidate material readiness, idempotency/state-machine/durable-truth expectations, and runtime health with masked evidence.

## Execution Order

1. Confirm the isolated worktree and active Change files exist in `D:/xianyu-worktrees/CHG-0031-controlled-real-publish-yilong`.
2. Generate `generated/PROJECT_STATE.json` using the repository generator only.
3. Continue only narrow read-only preflight if requested after the active record is verified.
4. Stop before publish/deploy/commit/push unless the commander explicitly authorizes a later phase.

## Gate Contract

```text
REAL_PUBLISH_ALLOWED=false
COMMANDER_GO_FOR_REAL_PUBLISH=false
FRESH_ITEM_SYNC_INVOCATIONS=0
PRODUCTION_MUTATION_COUNT=0
REAL_PUBLISH_ACCEPTANCE=BLOCKED_HUMAN_MATERIAL_DATA
USER_PROVIDED_IDENTITY_BINDING=PASS
NO_GO_BLOCKER=HUMAN_BLOCKED_MATERIAL_DATA
```

## Expected Publish Owner

The only allowed later publish chain is:

```text
COMPANY xianyu_publish_single
-> XIANYU Backend /api/v1/product-publish/publish/batch
-> PublishExecutorService
-> execute_single_publish
-> detect_publish_account_capability
-> XianyuDirectPublisher / XianyuPersonalPublisher
-> MTOP publish
-> Publish Log
-> authoritative item sync/readback
```

## Commander Override Identity Binding

The project owner supplied direct identity authorization plus an external
sensitive screenshot for masked account `280***247`. For this run, that
evidence is authoritative identity binding. The screenshot itself, its hash,
and the full account id must not be copied or committed. Publish remains
forbidden until resumed narrow preflight proves status, session lineage,
verification state, publish capability, owner scope, material readiness,
baseline counts, duplicate state, and idempotent durable readback plan.

## Rollback

Before real publish, rollback is deletion of the CHG-0031 active record and regeneration of `generated/PROJECT_STATE.json` from the isolated worktree. No production data rollback is required because this phase performs no production mutation.

## Upstream Capability Audit

Same as proposal.

## Pinned Upstream Evidence

Same as proposal.

## Existing Local Implementation Search

Same as proposal.

## Reuse Decision

Decision: ADOPT_UPSTREAM

## Duplicate Implementation Risk

No second publish owner, material owner, account owner, session owner, scheduler, worker, or durable truth source may be introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream satisfies publish execution; CHG-0031 only adds the controlled business checkpoint and evidence record.

## Approved Exception ADR

Not applicable.

## Component Owner

XIANYU native publish owner via Backend and `detect_publish_account_capability`; COMPANY is transport only.

## Retirement Plan For Overlapping Local Code

No overlapping production code is planned.

## Final Phase 1 Closure

Final decision is no-go: `HUMAN_BLOCKED_MATERIAL_DATA`. The exact missing facts
are `sku_rows` and `specifications` for at least one existing non-duplicate
material. The existing publish-address owner works and must remain the
supply-chain/address owner.
