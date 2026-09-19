# CHG-0038 Tasks

Change ID: CHG-0038-websocket-registration-readiness
Status: VERIFYING

- [x] T1 Reconstruct the 23:58 missed-message evidence and prove divergence occurs before AutoReplyService.
- [x] T2 Compare affected account evidence with healthy post-reconnect automatic-reply evidence.
- [x] T3 Audit current production Native registration and ChatNew registration behavior.
- [x] T4 Read pinned upstream bda1a859 and prove the same Native registration-readiness gap exists upstream.
- [x] T5 Implement the minimal registration acknowledgement gate in an isolated upstream worktree.
- [x] T6 Generate one exact vendor patch and add focused regression tests.
- [x] T7 Run targeted tests, change validation, repository verification, security scan and git diff --check.
- [ ] T8 Commit and push exact XIANYU task files; verify remote SHA.
- [x] T9 Perform only bounded production recovery/activation allowed by the no-global-restart constraint.
- [ ] T10 Read back Native status and wait for an organic buyer event for true Auto Reply E2E confirmation.

## Upstream capability audit

Native /reg exists upstream; acknowledgement readiness does not.

## Pinned upstream evidence

bda1a859df63fa5f24e51398fa80a23490bb6dfc.

## Existing local implementation search

Existing ChatNew matching-mid wait provides a reusable protocol pattern; Native reconnect and message handlers already exist.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second connection/reply system is allowed.

## Why upstream cannot satisfy the requirement

Pinned upstream marks registration complete without confirmation.

## Approved exception ADR

Not applicable.

## Component owner

Native WebSocket owner.

## Retirement plan for overlapping local code

Retire after equivalent upstream fix is proven.
