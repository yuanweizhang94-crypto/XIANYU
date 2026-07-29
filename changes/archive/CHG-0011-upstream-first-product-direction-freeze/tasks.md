Change ID: CHG-0011-upstream-first-product-direction-freeze
Status: ARCHIVED
# Tasks

- [x] T1 Stop local autoreply worker and owned listener
- [x] T2 Verify pinned upstream SHA and audit real implementation files
- [x] T3 Create upstream capability matrix and local component disposition
- [x] T4 Add upstream-first policy to repository governance docs
- [x] T5 Enforce upstream audit and reuse decision in Change validation
- [x] T6 Add validator unit coverage for duplicate-development gates
- [x] T7 Run complete verification, PR, merge, archive, and final state sync

## Current progress

Completed tasks: 7 / 7
Next task: None

## Evidence

- The previously running local autoreply worker was stopped before this active change was created.
- The owned listener stopped with the local worker.
- Pinned upstream HEAD was verified as `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.
- No platform message was sent by this change.
- No upstream tracked source was modified.
- No CHG-0012 was created.

## Upstream capability audit

Pinned upstream `D:/xianyu-upstream-pilot` was audited at `bda1a859df63fa5f24e51398fa80a23490bb6dfc` by reading implementation files for account, keyword, default reply, AI, WebSocket, message filtering, reply logs, and frontend management pages. Evidence is summarized in `docs/UPSTREAM_CAPABILITY_MATRIX.md`.

## Pinned upstream evidence

- Upstream path: `D:/xianyu-upstream-pilot`
- Expected SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Actual SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Upstream tracked source modified by this change: no

## Existing local implementation search

`D:/xianyu` was searched for `autoreply`, `rule`, `keyword`, `fallback`, `watermark`, `cooldown`, `rate.limit`, `send_confirmed_reply`, `NormalizedInboundMessage`, `UpstreamClient`, and `listener` under `app`, `tests`, `docs`, and `changes`. Existing overlap is documented in `docs/LOCAL_COMPONENT_DISPOSITION.md`.

## Reuse decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate implementation risk

High for automatic reply, keyword matching, AI reply, context, message receiving, and send execution because pinned upstream already contains the business application and execution engine. This change freezes duplicate local expansion and requires future changes to adopt, configure, patch, or operationally wrap upstream before considering local exceptions.

## Why upstream cannot satisfy the requirement

Not applicable for this governance change. The requirement is not to implement a business feature; it is to document upstream capabilities and enforce upstream-first governance. Future `BUILD_LOCAL_EXCEPTION` requests must prove upstream cannot satisfy their feature requirement.

## Approved exception ADR

Not applicable. No `BUILD_LOCAL_EXCEPTION` is requested by CHG-0011.

## Component owner

- Business application and execution engine: pinned `zhinianboke/xianyu-auto-reply` deployment.
- Safety, governance, operations, validation, and release control layer: `D:/xianyu`.

## Retirement plan for overlapping local code

CHG-0010 local autoreply worker is frozen and deprecated by policy. CHG-0015 is reserved for evaluating and retiring duplicate local autoreply worker behavior after upstream native fixed-template and AI reply validation passes.


## T7 local verification evidence

Local verification passed before PR publication:

- `python scripts/generate_state.py` passed and `generated/PROJECT_STATE.json` was normalized to repository LF line endings.
- `python scripts/project_context.py` passed.
- `python scripts/validate_change.py` passed.
- `python scripts/verify_repository.py` passed with 566 tests.
- `python -m pytest -W error` passed with 566 tests.
- `python -m ruff check .` passed.
- `python scripts/security_scan.py` passed.
- `python -m mypy app/xianyu_system` passed.
- `git diff --check` passed.

PR merge and archive will be recorded after GitHub PR completion.

## Post-merge archive evidence

PR #12 was merged by normal merge commit `7f52613438ad6c5929e3fd08fe93d212f56e2342`. CHG-0011 was moved from `changes/active/` to `changes/archive/`, all change files were marked `ARCHIVED`, and project state was regenerated with zero active changes. CHG-0012 was not created.
