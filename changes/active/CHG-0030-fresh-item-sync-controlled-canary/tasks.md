# CHG-0030 Tasks

Change ID: CHG-0030-fresh-item-sync-controlled-canary
Status: IMPLEMENTING

- [x] T1 Read root `AGENTS.md`, fetch remote main without changing `origin`, verify `origin/main=8d1d1d0fb272cd2715135d077be98ce0b575cb79`, verify ancestry, path absence, branch absence, and create the isolated worktree from `origin/main`.
- [x] T2 Run `python scripts/project_context.py` before development and create the active CHG-0030 execution record with the required three-line contract.
- [x] T3 Inspect pinned upstream, CHG-0024 local record, COMPANY `xianyu_item_sync` schema/implementation, and read-only auth/capability path without invoking Item Sync.
- [x] T4 Persist RED gate evidence: selected-account Item Sync eligibility is not explicit PASS, and `xianyu_item_sync` has no trackable request/task/trace identity.
- [x] T5 Run focused CHG-0030 tests, change validation, project context, and `git diff --check`. Focused tests and diff check passed; `validate_change.py` failed on pre-existing CHG-0020 archive debt outside CHG-0030.
- [x] T6 Report changed file list, command results, remaining gate state, and whether commander GO is safe.
- [x] T7 Phase 2 root-cause diagnosis: authoritative adapter source is separate dirty COMPANY checkout; sanitized account-status adapter and Item Sync adapter currently drop the needed XIANYU fields; upstream backend route/account-status can be patched without changing the ItemService owner.
- [x] T8 Add executable RED source-artifact test proving no CHG-0030 patch exists for explicit preflight and traceable terminal/durable readback contract.
- [x] T9 Implement minimal XIANYU vendor patch artifact and turn RED test GREEN without touching COMPANY dirty files, invoking sync, deploying, restarting, or changing generated state manually.
- [x] T10 Phase 2b repair commander-rejected acceptance defects: replace fake durable/duplicate fields with actual `xy_catalog_items` readback queries, add structured backend logs, and fail selected-account preflight closed unless disabled/checking/platform-verification/session-cookie-lineage/token-ready facts are authoritative.
- [x] T11 Prove the CHG-0030 artifact clean-applies to the current runtime-active stacked baseline and run patched upstream/runtime tests in a temporary clean copy.
- [x] T12 Run and record the Phase 3 local verification matrix, classify only proven unrelated global debt, and keep production invocation/deploy counts at 0.
- [x] T13 Stage only exact CHG-0030 paths, create the implementation commit, push the branch without changing `origin`, and verify local/remote SHA equality.
- [x] T14 Create the implementation PR, verify PR number/URL/head/base/scope files/check names/status, and do not merge.
- [x] T15 After later explicit authorization, perform validated deployment of the accepted CHG-0030 backend patch without changing the Item Sync owner.
- [x] T16 After deployment, run selected-account post-deploy preflight and prove explicit Item Sync eligibility PASS before any canary invocation.
- [x] T17 Phase 4b reproduce the skipped-lock false-success defect with an executable runtime-stack RED test and add a separate immutable follow-up patch artifact without editing the locked r1 artifact.
- [x] T18 Validate the exact r1 patch plus Phase 4b follow-up patch stack in a clean replay runtime source, including skipped-lock and full-active-list completeness cases.
- [ ] T19 Commit and push the Phase 4b correction, update PR #45, and classify scoped/current-commit CI before any deployment.
- [ ] T20 Build and deploy Backend r2 from the exact two-patch stack only, preserving r1 and CHG-0029 rollback images and leaving WebSocket/Scheduler/Frontend unchanged.
- [ ] T21 Repeat full read-only post-deploy preflight, including selected-account explicit Item Sync eligibility with authoritative platform-verification evidence type, item/duplicate baseline, safety counters, and service restarts.
- [ ] T22 After later commander GO, perform exactly one Fresh Item Sync canary invocation and capture operation identity, terminal result, real durable readback, measured duplicate count, and safety counters.
- [ ] T23 Complete closure commit/merge only after canary evidence and GitHub closure acceptance are satisfied.

## Upstream capability audit

Pinned upstream Item Sync owner was searched and found.

## Pinned upstream evidence

Pinned upstream SHA `bda1a859df63fa5f24e51398fa80a23490bb6dfc` is recorded in proposal and evidence.

## Existing local implementation search

CHG-0024 and the current COMPANY adapter were searched.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No duplicate Item Sync owner is planned.

## Why upstream cannot satisfy the requirement

Upstream lacks the external canary trace and eligibility proof required before production invocation.

## Approved exception ADR

Not applicable.

## Component owner

XIANYU `ItemService.fetch_all_items_from_account`.

## Retirement plan for overlapping local code

No overlapping local code is added.
