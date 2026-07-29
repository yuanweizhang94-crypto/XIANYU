Change ID: CHG-0011-upstream-first-product-direction-freeze
Status: ARCHIVED
# Acceptance

## Acceptance criteria

- The current local autoreply worker and owned listener are stopped.
- Pinned upstream evidence is based on `D:/xianyu-upstream-pilot` at `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.
- The repository contains a capability matrix, local component disposition, and upstream-first policy.
- Repository governance requires upstream audit, pinned evidence, local search, reuse decision, duplicate-risk analysis, owner, and retirement plan before implementation.
- `BUILD_LOCAL_EXCEPTION` requires evidence and an accepted ADR.
- A change that adopts upstream cannot plan a local rewrite.
- The roadmap locks CHG-0012 through CHG-0015 without creating CHG-0012.
- Complete local verification and GitHub Actions pass before Ready/merge.
- The change is merged, archived, and final state has zero active changes.
- No platform messages are sent by CHG-0011.

## Verification commands

- `python scripts/generate_state.py`
- `python scripts/project_context.py`
- `python scripts/validate_change.py`
- `python scripts/verify_repository.py`
- `python -m pytest -W error`
- `python -m ruff check .`
- `python scripts/security_scan.py`
- `python -m mypy app/xianyu_system`
- `git diff --check`

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
