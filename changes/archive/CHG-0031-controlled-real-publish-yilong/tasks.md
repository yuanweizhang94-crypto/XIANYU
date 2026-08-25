# CHG-0031 Tasks

Change ID: CHG-0031-controlled-real-publish-yilong
Status: ARCHIVED

- [x] T1 Verify the active CHG-0031 files were absent in the isolated target worktree before correction.
- [x] T2 Read current repository change conventions from archived CHG-0030 and the repository state generator.
- [x] T3 Create the minimum active CHG-0031 record in the actual target worktree using `apply_patch`.
- [x] T4 Run `python scripts/generate_state.py` from the target worktree.
- [x] T5 Verify with `Test-Path`, `Get-Item`, generated active state, and `git status --short`.
- [x] T6 Execute narrow read-only selected-account/material preflight only; no Fresh Item Sync, publish, deploy, restart, edit, offline, delete, message, Browser, QR, or credential access.
- [x] T7 Diagnose the identity discrepancy with schema-aware read-only evidence and fail closed when exact durable binding is absent.
- [x] T8 Record commander `NO-GO_FOR_REAL_PUBLISH`, `PUBLISH_INVOCATIONS=0`, and hard blocker `APPROVED_LABEL_NOT_BOUND_IN_PRODUCTION_DURABLE_TRUTH`.
- [x] T9 Do not perform publish; record that `xianyu_publish_single` was not invoked because the identity gate failed.
- [x] T10 Do not claim terminal platform ACTIVE/readback/item-count +1 acceptance; record `REAL_PUBLISH_ACCEPTANCE=BLOCKED_NO_IDENTITY_BINDING`.
- [x] T11 Add and run focused archived-evidence/zero-action invariant tests plus requested repository checks; classify only proven pre-existing debt without absorbing it.
- [x] T12 Archive CHG-0031, regenerate project state, review scoped diff, commit, push, open PR, classify CI, merge if permitted, and verify main closure.

## Upstream Capability Audit

Pinned upstream product publish implementation was searched and found.

## Pinned Upstream Evidence

Pinned upstream SHA `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.

## Existing Local Implementation Search

Local XIANYU and COMPANY records identify `xianyu_publish_single` as the formal publish path.

## Reuse Decision

Decision: ADOPT_UPSTREAM

## Duplicate Implementation Risk

No duplicate publish owner is planned.

## Why Upstream Cannot Satisfy The Requirement

Upstream satisfies publish execution; it does not choose or certify this account/material checkpoint.

## Approved Exception ADR

Not applicable.

## Component Owner

XIANYU native publish owner through Backend; COMPANY thin adapter only.

## Retirement Plan For Overlapping Local Code

No overlapping production code is added.
