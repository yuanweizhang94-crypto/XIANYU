Change ID: CHG-0016-local-only-manual-platform-verification-handoff
Status: ARCHIVED
# Acceptance

## IMPLEMENTING acceptance

This implementation is acceptable when:

- The Change status is `IMPLEMENTING` or `VERIFYING`.
- Reuse decision is `PATCH_UPSTREAM`.
- Upstream pinned/latest evidence is recorded.
- Local historical search evidence is recorded.
- The upstream patch artifact is recorded with pinned base SHA and SHA256.
- The upstream patch artifact is Git parseable with
  `git apply --numstat --unidiff-zero`.
- The upstream patch artifact passes `git apply --check --unidiff-zero` against
  a clean pinned upstream SHA worktree.
- The upstream patch artifact is a deterministic Git-generated zero-context
  patch produced with `--unified=0`.
- The upstream patch artifact contains no context lines inside hunks.
- The upstream patch artifact contains no added payload with trailing spaces or
  tabs.
- The upstream patch artifact passes clean pinned-SHA `git apply --check` with
  `--whitespace=error-all` and `--unidiff-zero`.
- The applied upstream source passes `git diff --check`.
- Applied Git blobs match build Git blobs 5/5.
- Git-canonical content is identical for all five target files. Raw
  working-tree byte differences are permitted only when proven to be CRLF/LF
  expansion differences under upstream text attributes, with matching BOM,
  matching trailing newline, no lone CR, canonical LF comparison 5/5, and
  staged Git blob comparison 5/5.
- CHG-0009 wrapper starts and stops only the host patched upstream websocket process.
- Docker websocket and host manual-listener are mutually exclusive.
- No second IM, Token, WebSocket, sender, or automatic reply executor is created.
- No automated page interaction or remote solver is added.
- Default replies remain disabled pending owner decision after ignored backup.
- Host manual-listener startup forces `AUTO_START_WEBSOCKET=false`.
- Host manual-listener startup disables DrissionPage fallback and remote
  captcha/Token environment inheritance.
- Host manual-listener startup maps Pilot MySQL and Redis to host loopback
  ports and waits for `/health` before reporting success.
- Failed or timed-out manual-listener startup removes stale PID state.
- Manual verification browser launch is process-wide single-shot.
- Existing same `x5sec` Cookie is not treated as success.
- Manual success retries upstream native Token at most once; repeated platform
  verification becomes `manual_verification_not_accepted`.
- Host manual-listener logs are written to ignored local logs instead of being
  discarded.
- No websocket, scheduler, or CHG-0010 worker is started.
- No message is sent.
- Threat model covers the required risks.
- Test plan covers unit, structure, fake-browser, local integration, and separately approved live validation.

## Implementation acceptance

An implementation Change must prove:

1. Owner scope blocks cross-account handoff.
2. One task per account and one task globally are enforced.
3. Verification URL is memory-only, single-use, not logged, and expires within five minutes.
4. Browser is visible and uses an isolated temporary profile.
5. Programmatic mouse, keyboard, click, drag, trajectory, Playwright solver, DrissionPage solver, real_mouse, and remote solver calls are structurally absent.
6. Browser host allowlist blocks arbitrary URL navigation.
7. Cookie values are never logged or returned.
8. Only allowed Cookie delta fields are merged.
9. Wrong-account Cookie write is blocked.
10. Complete without expected Cookie delta is blocked.
11. Cookie merge uses upstream account service and does not write directly to the database.
12. Token recovery returns to upstream native online-chat and automatic-reply Token flows.
13. The bridge does not create or copy IM Tokens.
14. The bridge does not send messages.
15. Unknown state fails closed.

## Test plan

Unit tests:

- owner scope.
- task state transitions.
- TTL expiry.
- cancel.
- one-task-per-account.
- URL host allowlist.
- URL never logged.
- Cookie value never logged.
- unknown state fail closed.
- no automatic browser interaction.
- allowed Cookie delta.
- rejected Cookie field.
- wrong-account write blocked.
- complete without expected Cookie blocked.
- direct DB write absent.

Structure tests must forbid imports or calls to:

- `solve_slider`.
- trajectory generator.
- `pyautogui`.
- DrissionPage solver.
- remote captcha client.
- message sender.

Fake browser tests:

- open called once.
- mouse functions never called.
- keyboard functions never called.
- click never called.
- drag never called.
- Cookie delta returned.
- timeout cleanup.
- cancel cleanup.
- second call after any terminal state does not open a browser.
- concurrent accounts open at most one browser.
- existing same `x5sec` does not pass.
- changed/new exact `x5sec` passes.
- unsafe initial URL or unknown redirect fails closed.

Integration tests:

- local fake official verification page only.
- owner manually completes simulated task.
- expected fake Cookie delta appears.
- upstream account service merge called once.
- Token client not implemented by bridge.
- no message send.

Live platform validation:

- Future separate approval only.
- ACCOUNT-A only.
- One attempt.
- Owner manual operation.
- No automated interaction.
- No messages.
- Online chat recovery before automatic reply recovery.
- CHG-0012 business matrix resumes only after the manual handoff is proven.

## T11 repair closure acceptance

T11 closure is complete only because:

- PR #19, PR #20, PR #21, and PR #22 were merged at their recorded exact HEADs.
- All four merge commits are ancestors of current main.
- Applicable Actions succeeded.
- Repository artifact identity is verified from the Git blob, not from a
  platform-dependent working-tree checkout.
- Artifact Git blob SHA is
  `174fac36b92f87b25d669a5a3ad80c59983a37d2`.
- Artifact Git blob SHA256 is
  `E5791692B69D95157A2249EF6B4C04F71A65C8513412B1A87C70EFF03D117FFE`.
- Windows raw worktree SHA differences are accepted only after canonical
  CRLF-to-LF bytes equal the repository Git blob, with matching BOM, matching
  trailing newline and no lone CR.
- No service, account, browser, platform, AI or message operation occurred.
- T12 remains separately authorized.

T11 closure main:
`64db9f099d65341a9e118fbca07bfb5be6e5b89b`.

Final artifact SHA256:
`E5791692B69D95157A2249EF6B4C04F71A65C8513412B1A87C70EFF03D117FFE`.

## Upstream capability audit

Evidence is recorded in `evidence/upstream-audit.md`.

## Pinned upstream evidence

Pinned upstream SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.

## Existing local implementation search

No reusable local manual bridge exists.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

High if this Change creates a second sender, Token client, websocket, automatic reply executor, or browser solver. Acceptance forbids those outcomes.

## Why upstream cannot satisfy the requirement

Upstream lacks a pure manual local handoff and only provides automated or remote-solving verification paths.

## Approved exception ADR

Not applicable.

## Component owner

Upstream remains business runtime owner. The handoff is operations-only.

## Retirement plan for overlapping local code

Keep CHG-0010 frozen/deprecated and do not expand it.

## Blocked closeout acceptance

CHG-0016 is acceptable for archival only when:

- Status is `ARCHIVED` in proposal, design, tasks, acceptance and threat model.
- The Change exists only under `changes/archive/`.
- T12 remains unchecked and records `MANUAL_VERIFICATION_NOT_ACCEPTED`.
- T13 is checked because cleanup and blocked closure are complete.
- The masked failure evidence is preserved.
- `generated/PROJECT_STATE.json` has `active_change` set to `null`.
- Generated tasks total, completed and next task are `0`, `0` and `null`.
- No runtime is started during closeout.
- Message sends during CHG-0016 remain `0`.
- CHG-0010 remains frozen, deprecated and stopped.
- Follow-up delivery is directed to upstream-native Token, account, WebSocket,
  reply, AI and sender paths.

Validated by CHG-0016:

- local-only visible owner browser handoff implementation;
- official host allowlist;
- one-browser-only guard;
- expected changed `x5sec` acceptance checks;
- at most one native Token retry after successful handoff;
- deterministic cleanup and stop controls;
- zero message sends during the approved live attempt.

Not validated by CHG-0016:

- platform acceptance of the live manual verification;
- AI reply;
- keyword reply;
- default reply;
- real customer chat;
- production automatic reply;
- image reply;
- online-chat business matrix;
- order, refund, shipping or rating behavior.
