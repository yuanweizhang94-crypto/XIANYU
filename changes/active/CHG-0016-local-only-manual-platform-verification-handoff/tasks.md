Change ID: CHG-0016-local-only-manual-platform-verification-handoff
Status: DRAFT
# Tasks

- [x] T1 Create DRAFT proposal.
- [x] T2 Create DRAFT design.
- [x] T3 Record upstream evidence.
- [x] T4 Record threat model.
- [x] T5 Record DRAFT acceptance and test plan.
- [ ] T6 Await project-owner review before implementation approval.

## Current progress

Completed tasks: 5 / 6
Next task: T6 Await project-owner review before implementation approval.

## DRAFT allowed work

- Proposal.
- Design.
- Tasks.
- Acceptance.
- Threat model.
- Upstream evidence.
- Test plan.

## DRAFT prohibited work

- `IMPLEMENTING` status.
- Business code.
- UI code.
- Browser code.
- Backend route code.
- Platform calls.
- Live validation.
- Websocket startup.
- Scheduler startup.
- CHG-0010 worker startup.
- Cookie modification.
- Token cache modification.
- Message sending.
- Upstream tracked source modification.

## Upstream capability audit

The evidence records pinned automated captcha paths, absence of manual-only mode in pinned/latest upstream, reviewed upstream Issues/PRs, and local historical search.

## Pinned upstream evidence

Pinned upstream SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.

## Existing local implementation search

No reusable local manual bridge was found. CHG-0010 remains frozen/deprecated.

## Reuse decision

Decision: WRAP_FOR_OPERATIONS

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
