# CHG-0022 Tasks

Status: ARCHIVED

Change ID: CHG-0022-websocket-token-network-classification

- [x] T1 Re-run project context; refresh recovery Git baseline, current Runtime, latest upstream and historical Change/patch search.
- [x] T2 Record execution contract, `PATCH_UPSTREAM` decision, allowed/forbidden scope, pre-change Runtime SHA/image/container.
- [x] T3 Implement minimal reconnect classification patch on an isolated latest-upstream worktree and generate a vendor patch.
- [x] T4 Add/run targeted DNS, gaierror, reset, timeout, explicit-auth, four-account, recovery, QR fail-closed and healthy-maintenance executable regression coverage.
- [x] T5 Run related regressions and repository verification; verifier failure set is proven identical to the task base and limited to the pre-existing unrelated CHG-0020 archive defect.
- [x] T6 Activate WebSocket component only, verify source/runtime SHA, health, seven-account readback, Token cache reuse and absence of a new remote Token storm.
- [ ] T7 Perform at most one controlled read-only fresh item sync per target account; stop if it remains a separate blocker.
- [ ] T8 Persist exact XIANYU task files to GitHub and verify local/remote SHA equality.
- [ ] T9 Sync only impacted dynamic business truth to ZIDONGZHUA and durable invariant to AI-; do not modify COMPANY/JZAI code.

## Upstream capability audit

Latest upstream has the defective path; no equivalent current fix found.

## Pinned upstream evidence

`9cbb3725b7e91daec33cb824a3ff4bd84acdcb12`.

## Existing local implementation search

No tracked equivalent repair found.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No parallel owner is allowed.

## Why upstream cannot satisfy the requirement

Current upstream still contains the defect.

## Approved exception ADR

Not applicable.

## Component owner

Existing WebSocket reconnect owner.

## Retirement plan for overlapping local code

Replace with verified upstream equivalent when available.
