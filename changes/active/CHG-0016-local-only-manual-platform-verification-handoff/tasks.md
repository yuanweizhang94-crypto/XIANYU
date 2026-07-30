Change ID: CHG-0016-local-only-manual-platform-verification-handoff
Status: IMPLEMENTING
# Tasks

- [x] T1 Create DRAFT proposal.
- [x] T2 Create DRAFT design.
- [x] T3 Record upstream evidence.
- [x] T4 Record threat model.
- [x] T5 Record DRAFT acceptance and test plan.
- [x] T6 Project-owner implementation approval recorded.
- [x] T7 Disable the two enabled default replies after ignored backup to establish zero automatic-send baseline.
- [x] T8 Create upstream patch worktree from pinned SHA and implement manual-only mode.
- [x] T9 Implement CHG-0009 host manual-listener wrapper lifecycle.
- [x] T10 Run local verification.
- [ ] T11 Repair live manual verification defects, open repair PR, wait for CI, and merge.
- [ ] T12 Run controlled owner manual validation without sending messages.
- [ ] T13 Cleanup and close Change.

## Current progress

Completed tasks: 10 / 13
Next task: T11 Repair live manual verification defects, open repair PR, wait for CI, and merge.

Current live defect marker: `MANUAL_VERIFICATION_REPEATED_BROWSER_LAUNCH`.

Required repair roots:

- `AUTO_START_WEBSOCKET_NOT_DISABLED`.
- `EXISTING_X5_COOKIE_FALSE_SUCCESS`.
- `MANUAL_BROWSER_NOT_SINGLE_SHOT`.
- `MANUAL_LISTENER_LOGS_DISCARDED`.

Requested short repair branch created:
`fix/CHG-0016-manual-verification-single-shot`.

Governance-compatible repair PR branch:
`fix/CHG-0016-local-only-manual-platform-verification-handoff/manual-verification-single-shot`.

Manual-listener startup blocker:

- Safe category: `DATABASE_CONNECTION_ERROR`.
- Exact failing component: patched upstream host websocket lifespan database
  startup check.
- Root cause: host manual-listener inherited container/default MySQL settings
  and attempted `localhost:3306`; Pilot MySQL is exposed to Windows host on
  loopback port `13306`.
- Repair branch:
  `fix/CHG-0016-local-only-manual-platform-verification-handoff/manual-listener-startup`.

Patch artifact parseability repair:

- Initial blocker: `PATCH_ARTIFACT_CORRUPT`.
- Secondary diagnostic: `RAW_WORKTREE_HASH_MISMATCH_0_OF_5`.
- Verified cause: `WORKTREE_EOL_NORMALIZATION_ONLY`.
- Repair blocker: `PATCH_ARTIFACT_REPAIR_BLOCKED_BY_DIFF_CHECK`.
- Final root cause: the default-context Git patch copied unchanged
  whitespace-bearing upstream context lines into the vendor artifact. Generic
  repository diff checking then reported those representation lines. No defect
  was found in the five patched Git blobs.
- Minimal repair: regenerate the artifact directly from the staged Git index
  using `--unified=0`. Do not modify patched upstream source. Do not hand-edit
  patch hunks. Do not add a whitespace exemption.
- Artifact equivalence proof:
  - Git parseable.
  - clean apply check passed.
  - canonical LF comparison 5/5.
  - staged Git blob comparison 5/5.
  - target tests passed.
- Zero-context artifact proof:
  - Artifact is a deterministic Git-generated zero-context patch.
  - Artifact contains no context lines inside hunks.
  - Artifact contains no added payload with trailing spaces or tabs.
  - Artifact passes `git apply --numstat --unidiff-zero`.
  - Artifact passes clean pinned-SHA `git apply --check` with
    `--whitespace=error-all` and `--unidiff-zero`.
  - Applied upstream source passes `git diff --check`.
  - Applied Git blobs match build Git blobs 5/5.
- Git-canonical content identical for all five target files.
- Raw working-tree byte differences are permitted only when proven to be
  CRLF/LF expansion differences under upstream text attributes, with matching
  BOM, matching trailing newline, no lone CR, canonical LF comparison 5/5, and
  staged Git blob comparison 5/5.

## Implementing allowed work

- Proposal.
- Design.
- Tasks.
- Acceptance.
- Threat model.
- Upstream evidence.
- Upstream patch artifact.
- Host manual-listener wrapper lifecycle.
- Local tests.

## Implementing prohibited work

- Platform calls.
- Unapproved live validation.
- Scheduler startup.
- CHG-0010 worker startup.
- Token cache modification.
- Message sending.
- Pinned upstream tracked source modification.

## Upstream capability audit

The evidence records pinned automated captcha paths, absence of manual-only mode in pinned/latest upstream, reviewed upstream Issues/PRs, and local historical search.

## Pinned upstream evidence

Pinned upstream SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.

## Existing local implementation search

No reusable local manual bridge was found. CHG-0010 remains frozen/deprecated.

## Reuse decision

Decision: PATCH_UPSTREAM

CHG-0009 remains the operations wrapper for local host lifecycle control only.

## Duplicate implementation risk

Tasks must not create a second IM, Token, WebSocket, sender, automatic reply, or browser automation implementation.

## Why upstream cannot satisfy the requirement

Pinned/latest upstream lack a pure manual local verification handoff and expose automated or remote-solving paths instead.

## Approved exception ADR

Not applicable.

## Component owner

Manual handoff is operations-only; upstream keeps business runtime ownership.

## Retirement plan for overlapping local code

Any future implementation must keep CHG-0010 disabled and avoid overlapping local sender behavior.
