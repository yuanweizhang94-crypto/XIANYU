# CHG-0018 T12 Final Integration Validation and CI Evidence

Status: LOCAL_VALIDATION_COMPLETE_REMOTE_CI_PENDING

Change ID: CHG-0018-account-profile-publish-safety

Task: CHG0018_T12_FINAL_INTEGRATION_VALIDATION_AND_REMOTE_SYNC

Date: 2026-08-09

## Execution contract

User outcome: integrate the verified T11 result into the main-based CHG-0018 PR #31 branch, preserve archived CHG-0017 state, validate the exact final repository state, push normally, and stop at Draft/Open/Unmerged after exact-head CI.

Confirmed blocker addressed by T11: real batch publish Profile/runtime readiness and duplicate-safe recovery evidence were incomplete.

Smallest success test: preserve the existing upstream publisher path and T11 evidence, regenerate one formal CHG-0018 Vendor Patch that contains the prior CHG-0018 source plus T11, pass local repository gates, then use one normal non-force push and verify CI on the exact remote head.

## Integration baseline

- PR #31 remote branch before integration: `review/CHG-0018-main-integration` at `80c7456f01b9ad54c1a2dcb492e14363ed1ab7bb`.
- `origin/main` observed before integration: `1d6d7d2bf47d75579d5129f9310774892c48e0fc`.
- T11 source commit: `8ffce692140d77a0b8bb46a84afc879d5d6b68a0`.
- T11 cherry-pick into isolated `integration/CHG-0018-t12-final`: clean; no business-source conflict and no ours/theirs conflict resolution.
- CHG-0017 remains under `changes/archive/CHG-0017-upstream-native-auto-ai-delivery`; the suspended predecessor path is absent.
- CHG-0018 remains the active `VERIFYING` change.

## T11 recovery truth preserved

- `AUTHORIZED_FAILED_RECORDS=4`
- `FAILED_RECORDS_RECOVERED=4`
- `ALREADY_PUBLISHED_SKIPPED=4`
- `NOT_PUBLISHED_CONFIRMED=0`
- `REAL_PUBLISH_ATTEMPTS=0`
- `SUCCESSFUL_HISTORICAL_RECORDS_RETRIED=0`
- `UNAUTHORIZED_RECORDS_TOUCHED=0`

Historical failed records do not imply that the platform item was never published. Duplicate/platform-state verification proved that all four authorized historical failed records already had matching later formal publish success and matching catalog/platform identity. Duplicate-safe recovery therefore correctly executed zero new real publish attempts. This evidence must not be described as four new real publish successes.

T11 implementation content remains present: canonical persistent Profile root, authoritative `account_id` forwarding, authoritative `owner_id` forwarding, one persistent context per concrete publish attempt, shared preflight and publish in that context, 60-second readiness polling, specific `verification_required` / `page_load_timeout` / `page_structure_mismatch` classification, one account lock plus one global browser slot, and no automatic second publish retry in the batch path. Retry eligibility remains limited to an externally verified `NOT_PUBLISHED` record with a maximum of one authorized retry.

## Vendor Patch final integration

- Historical T11 supplemental Patch SHA256 remains `99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882`.
- The prior formal CHG-0018 Patch `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD` represented the pre-T11 production state.
- T12 regenerated `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch` from an exact Git reconstruction of the archived CHG-0017 target blobs plus the prior CHG-0018 target blobs and the locked T11 supplemental Patch.
- No patch hunk was hand-spliced or manually rewritten.
- A first Git-generated candidate using the historical `--ignore-space-at-eol` option was discarded because strict apply passed but exact Git-blob equivalence was only 13/27; it was never committed or pushed.
- A second text candidate encoded the historical end-of-line differences and reached 27/27 blob equivalence, but it was discarded because storing those historical whitespace-bearing patch lines caused the outer XIANYU repository `git diff --check` to fail. It was never committed or pushed.
- The final artifact is still generated entirely by Git: the disposable patch-builder uses local `.git/info/attributes` to mark the 27 upstream target paths `-diff`, and `git diff --binary --full-index` emits 27 `GIT binary patch` records. That builder-only attribute file is not tracked or delivered. This preserves the exact source blobs without hand-editing patch hunks or embedding whitespace-bearing text lines in the repository artifact.
- Git binary patch syntax requires its final separator blank line. The XIANYU vendor directory therefore includes a tracked `.gitattributes` entry marking only `4c5e1ac-chg0018-account-profile-publish-safety.patch` as `binary`; this leaves the Patch bytes unchanged while allowing the outer repository `git diff --check` to treat the generated artifact as opaque binary data.
- Final T12 formal Vendor Patch SHA256: `B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111`.
- Patch parse: PASS.
- Strict clean apply with `--whitespace=error-all --unidiff-zero`: PASS.
- Applied `git diff --check`: PASS.
- Source/Git-blob equivalence: 27/27 PASS.
- Business meaning is equivalent to the prior formal CHG-0018 Patch followed by the locked T11 supplemental Patch; the SHA changed because T12 folds those layers into one exact formal delivery artifact and preserves historical EOL differences required for blob equivalence.

## Upstream tests on exact final Patch source

- CHG-0018 targeted tests: 38/38 PASS.
- CHG-0017 regression tests: 58/58 PASS.
- Frontend source changed by T11/T12: false.
- No frontend production deployment or rebuild was performed.

## Safety counters

- `REAL_PRODUCT_ACTIONS=0`
- `REAL_PUBLISH_ATTEMPTS=0`
- `MESSAGES_SENT=0`
- `QR_SCANS_PERFORMED=0`
- `CONTAINERS_CHANGED=0`
- `FORCE_PUSH_PERFORMED=false`
- No Xianyu login, password login, Token/Cookie business refresh, database business write, Redis business write, product mutation, polish, offlining, or message send occurred in T12.

## Local validation before final-state checkbox recheck

- `python scripts/validate_change.py`: PASS on the main-based integration content using the repository-required exact Change-ID validation branch name.
- CHG-0018 governance acceptance: 9/9 PASS.
- `python scripts/verify_repository.py`: PASS; current main-based repository suite count is 588/588, using worktree-local module resolution.
- Repository security scan: PASS.
- Targeted secret scan over T11 evidence, T12 evidence, the formal Vendor Patch, and T12 Git-added lines: PASS with zero credential-value matches and zero full long numeric account identifiers in the two evidence files.
- These gates passed before the T12 checkbox transition.

## Exact final local state after T12 completion

- T12 is marked complete while CHG-0018 remains `VERIFYING`.
- `generated/PROJECT_STATE.json` was regenerated by `python scripts/generate_state.py`; it was not hand-edited.
- Exact final `python scripts/validate_change.py`: PASS.
- Exact final CHG-0018 governance acceptance: 9/9 PASS.
- Exact final `python scripts/verify_repository.py`: PASS.
- Exact final main-based repository tests collected and passed: 588/588.
- The validation worktree temporarily used the repository-required branch name `integration/CHG-0018-account-profile-publish-safety` only so `validate_change.py` could match the active Change ID; the requested T12 integration branch name is restored before the delivery commit. No remote ref is created for the temporary validation name.
- Remote push and exact-head `quality/tests/security` CI verification occur only after this exact final local state is committed. CI results are checked against the final remote Git SHA and are intentionally not embedded through a recursive post-CI evidence commit unless a correction is required.
