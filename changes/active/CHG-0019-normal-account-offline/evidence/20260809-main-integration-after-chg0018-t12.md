# CHG-0019 Main Integration After CHG-0018 T12

Status: VERIFYING

Change ID: CHG-0019-normal-account-offline

Task: CHG0019_MAIN_REBASE_FINALIZE_PR33

Date: 2026-08-09

## Execution contract

User outcome: finalize PR #33 on the already merged and archived CHG-0017 -> CHG-0018 T12 main baseline while preserving the reviewed CHG-0019 normal-account off-shelf behavior.

Confirmed blocker: the historical CHG-0019 delivery was reviewed against the pre-T12 CHG-0018 layer, while current `main` contains the regenerated T12 CHG-0018 formal Patch that already folds in T11. The current-main CHG-0019 layer therefore needs an explicit Git-replayed integration artifact rather than assuming the historical layering is still canonical.

Smallest success test: reconstruct the historical base and reviewed CHG-0019 target, three-way merge that target with current CHG-0018 T12, generate one Git-produced incremental CHG-0019 Patch, replay it from pinned upstream, pass all targeted/frontend/repository gates, then normally push PR #33 without changing its Draft/Open/Unmerged state.

## Main and PR baseline

- Current `main`: `bca1f2381b1201f3b6fe58f2d8952c45a2ba880b`.
- PR #31 is merged; its final head was `0e438f19f8d65d5bd8bace7f143fb0d042807948`.
- CHG-0017 is archived under `changes/archive/CHG-0017-upstream-native-auto-ai-delivery`.
- CHG-0018 is archived under `changes/archive/CHG-0018-account-profile-publish-safety`.
- Suspended predecessor count: `0`.
- PR #33 initial head: `adab634788eb5316de41b66cf48915aa6c06afa8`; state at integration start: Draft/Open/Unmerged.
- Historical PR #28 remained Draft/Open/Unmerged at head `d339bc37d3fa9c4fb0e1487d0ebbca6a8cb55e5d` and was not modified.

## Generated state before source integration

`python scripts/generate_state.py` regenerated `generated/PROJECT_STATE.json`; it was not hand-edited.

- Active change: `CHG-0019-normal-account-offline`.
- Status: `VERIFYING`.
- Task total: `9`.
- Task complete: `9`.
- Next task: `null`.
- Suspended change count: `0`.
- Initial `python scripts/validate_change.py`: PASS using the repository-required exact Change-ID validation branch name, then the requested local branch name was restored.

## Exact source reconstruction

Pinned upstream: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

### CURRENT_T12_BASE

Replayed in a dedicated isolated upstream tree:

1. CHG-0017 canonical Patch SHA256 `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`.
2. Current CHG-0018 T12 formal Patch SHA256 `B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111`.

The current T12 Patch already includes T11, so `4c5e1ac-chg0018-t11-controlled-batch-publish-recovery.patch` was not applied again.

`CURRENT_T12_BASE_READY=true`.

### HISTORICAL_CHG0019_TARGET

Historical artifacts were extracted directly from Git commit `d339bc37d3fa9c4fb0e1487d0ebbca6a8cb55e5d`; the current B379 Patch was not substituted for the historical pre-T12 layer.

Historical canonical chain:

1. CHG-0017 Patch SHA256 `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`.
2. Historical pre-T12 CHG-0018 Patch SHA256 `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`.
3. Historical CHG-0019 formal-delivery Patch SHA256 `410308F81A2484C469694E8790E9C9C689DEDAEF5C73AB0D67DD3518D557C3CF`.
4. Historical PR #28 hardening Patch SHA256 `B4F9673CF486EC57FF235BAF97182066703FE6D2E4EE7910A3828AC769A1C912`.

`HISTORICAL_CHG0019_TARGET_READY=true`.

The historical formal-delivery Patch passes a direct `git apply --check` on current T12. The historical PR #28 hardening Patch does not apply as a standalone Patch directly on T12 because it depends on the formal-delivery CHG-0019 layer. Direct applicability was not used as proof of correct integration because `backend-web/app/services/xianyu_publisher.py` is modified by both T11 and CHG-0019.

## Three-way merge

Git graph used for the merge:

- BASE: historical pre-T12 CHG-0018 target.
- OURS: BASE plus the locked T11 supplement; its Git tree exactly matched the separately reconstructed current B379 T12 target.
- THEIRS: BASE plus historical CHG-0019 formal delivery plus PR #28 hardening; its Git tree exactly matched the separately reconstructed historical CHG-0019 target.

Git automatically merged THEIRS into OURS with `backend-web/app/services/xianyu_publisher.py` as an overlapping file. There were zero unmerged paths and no `ours`/`theirs` manual business-conflict resolution.

`THREE_WAY_MERGE_CLEAN=true`.

## New current-main CHG-0019 Patch

Generated only by Git from the current T12 target to the clean merged target:

- File: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0019-main-integration-after-chg0018-t12.patch`.
- SHA256: `A0A07EA2EC4BC0046CBA39DA478EC9E530E1FBD10A9EEE23F3311D1A38677392`.
- Changed upstream files: 11.
- Patch parse: PASS.
- Strict clean apply: PASS.
- Applied `git diff --check`: PASS.
- Source Git-tree equivalence: PASS.

Independent replay:

`PINNED -> CHG-0017 -> CHG-0018 T12 B379... -> NEW CHG-0019 MAIN-INTEGRATION PATCH`

reproduced the exact three-way merged Git tree.

The historical CHG-0019 backend-verified, formal-delivery, and PR #28 hardening Patch files remain unchanged historical audit artifacts and are marked `HISTORICAL / SUPERSEDED_FOR_CURRENT_MAIN_LAYERING` in the Vendor README.

## T11 invariants preserved

Static source assertions and the CHG-0018/T11 regression suite confirm:

- `T11_AUTHORITATIVE_ACCOUNT_ID_PRESERVED=true`.
- `T11_AUTHORITATIVE_OWNER_ID_PRESERVED=true`.
- `T11_CANONICAL_PROFILE_PRESERVED=true`.
- `T11_60S_READINESS_PRESERVED=true`.
- `T11_SPECIFIC_FAILURE_CLASSIFICATION_PRESERVED=true`.
- `T11_NO_AUTO_SECOND_PUBLISH_PRESERVED=true`.

The batch publish path still forwards the database-loaded account identity and owner into one `publisher.publish_item()` call per concrete attempt. The canonical Profile path, authoritative Cookie lookup, 60-second readiness window, and `verification_required` / `page_load_timeout` / `page_structure_mismatch` classifications remain present.

## CHG-0019 hardened behavior preserved

Static source assertions plus the 47-test CHG-0019 suite confirm:

- `CHG0019_NORMAL_WEB_OFFLINE=true`.
- Default `/items/batch-offline` uses `offline_items_normal_web`; the PC Seller batch-offline path is not the default route.
- Exact normal detail URL remains `https://www.goofish.com/item?id=<item_id>`.
- `CHG0019_DELETE_ISOLATION=true`.
- `CHG0019_SAFE_DIALOG=true`.
- `CHG0019_NONSEMANTIC_CONFIRM=true`.
- `CHG0019_TARGET_SPECIFIC_SUCCESS=true`.
- `CHG0019_GLOBAL_BODY_SUCCESS=false`.
- `CHG0019_CONTROL_DISAPPEARANCE_ALONE_SUCCESS=false`.

Success remains bound to the target item and requires a new post-action notice or reverse owner-operation state. Whole `document.body.innerText`, unrelated/recommended/stale text, URL drift, and control disappearance alone are rejected as success evidence.

## Tests on final combined upstream source

- CHG-0019 targeted tests: `47/47 PASS`.
- CHG-0018/T11 targeted regressions: `38/38 PASS`.
- CHG-0017 regressions: `58/58 PASS`.
- Frontend offline UI tests: `27/27 PASS`.
- Frontend lint: PASS.
- Frontend TypeScript/Vite build: PASS.

The clean replay tree initially had no `frontend/node_modules`; the first frontend test invocation therefore failed only because `typescript` was not installed in that disposable tree. No package or dependency metadata was changed. The retry used the already-installed dependency directory from the same upstream project on this machine, after which offline UI tests, lint, and build all passed.

## Runtime and safety boundary

No new real canary was run. Historical controlled real-canary evidence remains the runtime evidence for CHG-0019; this task only reconciles source layering and repository delivery.

- `REAL_PRODUCT_ACTIONS=0`.
- `REAL_OFFSHELF_ACTIONS=0`.
- `REAL_PUBLISH_ACTIONS=0`.
- `MESSAGES_SENT=0`.
- `QR_SCANS_PERFORMED=0`.
- `CONTAINERS_CHANGED=0`.
- No Xianyu login, Cookie/Token refresh, Docker deployment, database write, Redis write, delete, polish, publish, or off-shelf action occurred.
- `FORCE_PUSH_PERFORMED=false`.

## Final repository gates before push

- Final `python scripts/generate_state.py`: completed; generated state is script-produced, not hand-edited.
- Final `python scripts/validate_change.py`: PASS.
- Final `python scripts/verify_repository.py`: PASS with worktree-local module resolution; repository test count `582/582 PASS`.
- Separate complete `pytest`: `582/582 PASS`.
- The only initial full-suite failure was a disposable-worktree import-path issue that loaded the already-installed `xianyu_system` package from `D:/xianyu`; a temporary untracked root symlink to this worktree's own `app/xianyu_system` fixed module resolution. No source/test file was changed for that issue, and the symlink is removed before commit.
- Scope/diff/secret checks, normal commit/push, and exact-head PR #33 CI are performed after this evidence file and README are finalized.

Remote CI is intentionally not self-recorded in this commit because doing so would create a new commit and invalidate the exact-head CI result being reported externally.
