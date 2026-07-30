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
- [x] T11 Repair live manual verification defects, open repair PR, wait for CI, and merge.
- [ ] T12 Run controlled owner manual validation without sending messages.
- [ ] T13 Cleanup and close Change.

## Current progress

Completed tasks: 11 / 13
Next task: T12 Run controlled owner manual validation without sending messages.

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

## T11 repair closure

T11 closure main:
`64db9f099d65341a9e118fbca07bfb5be6e5b89b`.

PR #19:

- head `c0e78c341fd7a4d401396be6b9e71c2ff47ff4d7`.
- merge `c7bf9a52e795ee7f472c68d426b7bd44c79a88ed`.

PR #20:

- head `92e14642beb4bbdfa513e305474a37ee08135dad`.
- merge `c72c146f088b661bc9584364a9eecbddbfe27321`.

PR #21:

- head `84b1fdf376d3fa08199d85fac472cb502cbb0ea7`.
- merge `bb023f67c860125c5ec6043192e372d7fd9d52c2`.

PR #22:

- head `08c0021c672a86cc10d80b30c62217c1fc27d691`.
- merge `64db9f099d65341a9e118fbca07bfb5be6e5b89b`.

Closed defects:

- `AUTO_START_WEBSOCKET_NOT_DISABLED`.
- `EXISTING_X5_COOKIE_FALSE_SUCCESS`.
- `MANUAL_BROWSER_NOT_SINGLE_SHOT`.
- `MANUAL_LISTENER_LOGS_DISCARDED`.
- `DATABASE_CONNECTION_ERROR`.
- `EXPLICIT_DEFAULT_HTTPS_PORT_443_REJECTED`.
- `PATCH_ARTIFACT_CORRUPT`.
- `PATCH_ARTIFACT_REPAIR_BLOCKED_BY_DIFF_CHECK`.

Artifact Git blob:
`174fac36b92f87b25d669a5a3ad80c59983a37d2`.

Artifact Git blob SHA256:
`E5791692B69D95157A2249EF6B4C04F71A65C8513412B1A87C70EFF03D117FFE`.

Windows working-tree raw SHA256 diagnostic:
`E3BAA4F775AD09435C8CA9653E15844A67C5F7C507E17A396950A00DAF0E3796`.

Classification:
`WORKTREE_EOL_NORMALIZATION_ONLY`.

Live validation during T11 closure:
not performed.

T12:
not started.

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
