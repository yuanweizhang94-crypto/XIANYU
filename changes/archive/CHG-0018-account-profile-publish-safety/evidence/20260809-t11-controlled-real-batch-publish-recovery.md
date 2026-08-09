# CHG-0018 T11 Controlled Real Batch Publish Recovery Evidence

Status: VERIFYING

Change ID: CHG-0018-account-profile-publish-safety

Task: CHG0018_T11_CONTROLLED_REAL_BATCH_PUBLISH_RECOVERY

Date: 2026-08-09

## Authorization and boundary

The project Owner explicitly authorized one controlled real batch publish validation for only the four records that remained failed after the 2026-08-05 batch publish authentication audit. This evidence does not authorize CHG-0018 T12, PR Ready/Merge, PR #26/#28/#31 changes, unrelated product publication, login recovery, QR scanning, Token batch renewal, message sending, delete, offline, or polish operations.

Authoritative audit source: `D:/xianyu-handoff/LAPTOP-PUBLISH-AUTH-AUDIT-20260805-160855`.

Original failed batch: `a74c06a5-690a-414a-b9a7-57511941c270`.

Authorized failed publish-log records: `56`, `59`, `60`, `61`.

All four records use owner `1` and material `5`. Account and platform item identifiers are masked in repository evidence.

## Recovered records and duplicate-safe classification

| Original log | Account | Original failure | Original time | Later success log | Current catalog post-check | Retry state |
|---|---|---|---|---|---|---|
| 56 | `103***456` | `publish_form_not_rendered` | 2026-08-05 15:28:11 | 80 | same successful platform item and title present | `ALREADY_PUBLISHED` |
| 59 | `219***636` | `publish_form_not_rendered` | 2026-08-05 15:32:44 | 76 | same successful platform item and title present | `ALREADY_PUBLISHED` |
| 60 | `221***500` | `publish_form_not_rendered` | 2026-08-05 15:33:06 | 77 | same successful platform item and title present | `ALREADY_PUBLISHED` |
| 61 | `221***219` | `publish_form_not_rendered` | 2026-08-05 15:33:26 | 78 | same successful platform item and title present | `ALREADY_PUBLISHED` |

The later success rows are formal publish-log records with non-empty platform item identities. The three records `76/77/78` belong to one later batch, while record `80` belongs to another later batch. The current `xy_catalog_items` state still contains each successful item under the matching account and with the matching title.

Duplicate-safe result:

- `AUTHORIZED_FAILED_RECORDS=4`
- `FAILED_RECORDS_RECOVERED=4`
- `NOT_PUBLISHED_CONFIRMED=0`
- `ALREADY_PUBLISHED_SKIPPED=4`
- `UNKNOWN_STATE_SKIPPED=0`
- `IDENTITY_MISMATCH_SKIPPED=0`
- `REAL_PUBLISH_ATTEMPTS=0`
- `MAX_RETRY_PER_RECORD=1`

No authorized record was eligible for a new real publish attempt. Starting a new publish would have violated the Owner's duplicate-safe gate, so the correct controlled action was to perform zero new publishes.

## Existing real recovery evidence

The database contains later formal batch-publish successes for all four originally failed records, with matching owner/account/material identity and platform item identities. Current catalog post-check confirms those platform items remain associated with the same accounts.

Separate historical CHG-0018 evidence also records a formal backend publish-service success on 2026-08-06 from the persistent-Profile runtime, including explicit service success and a platform item identity. This is execution-path evidence; it is not counted as a new T11 publish attempt.

## Runtime and executor verification

- Real batch publish executor: `xianyu_chg0017_backend_web` / existing backend-web native `PublishExecutorService.batch_publish`.
- Current backend image observed during T11: `xianyu-chg0019-backend-web:44c8ae9-nonsemantic-confirm`.
- Backend and WebSocket both mount the same Docker volume `xianyu_chg0017_browser_data` at `/app/browser_data` read-write.
- The four authorized accounts have existing persistent Profile directories under that canonical root.
- Production WebSocket and Scheduler each have one running execution chain.
- The running Pilot backend has no `/app/browser_data` mount and no Chromium/Chrome executable; no Pilot Scheduler or Pilot WebSocket is running.
- `SECOND_EXECUTOR_RUNNING=false` for the browser publish path.

## T11 code-path hardening

Reuse decision: `PATCH_UPSTREAM`.

No new publisher, login system, Token system, Profile store, browser broker, service, queue, or database table was added.

The T11 supplemental patch changes only the existing upstream path:

1. Batch publish continues to use the `XYAccount` row loaded with owner scope and forwards `account.account_id` plus the authoritative `account.owner_id` into the existing publisher.
2. Each publish record explicitly uses `reuse_browser=False` and `should_close=True`; no batch-long browser context is reused.
3. Publisher Cookie lookup remains authoritative through `XYAccount.account_id + owner_id`.
4. Persistent Profile execution continues to use the existing account lock and global browser slot and releases both after the attempt.
5. Shared preflight and publish remain in the same concrete persistent browser context.
6. Publish readiness keeps the 60-second maximum wait and no longer fails at 15 seconds just because the page shell is still empty.
7. Required T11 failure categories are normalized to `profile_missing`, `browser_busy`, `login_required`, `verification_required`, `page_load_timeout`, `page_structure_mismatch`, and `unknown`; `ready` remains the success state.
8. Legacy `publish_form_not_rendered`, `publish_form_timeout`, `publish_page_load_failed`, and `manual_verification_required` exception inputs are compatibility-normalized and are no longer emitted by the T11 preflight path.
9. The existing batch method contains one `publisher.publish_item()` call site per record and no automatic publish retry loop.

## Tests and Vendor Patch

T11 supplemental patch:

`vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-t11-controlled-batch-publish-recovery.patch`

SHA256:

`99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882`

Patch validation:

- `git apply --check --whitespace=error-all`: PASS on an exact CHG-0017 -> CHG-0018 Git-blob preimage reconstruction.
- Clean apply: PASS.
- Applied Git-blob equivalence: 4/4 exact matches to the T11 source snapshot.
- CHG-0018 targeted suites: 38/38 PASS.
- CHG-0017 regression suites: 58/58 PASS.
- `python scripts/validate_change.py`: PASS.
- CHG-0018 governance acceptance: 9/9 PASS.
- `python scripts/verify_repository.py`: 596/596 PASS with the isolated worktree explicitly first on `PYTHONPATH`. The first isolated-worktree run was 595/596 only because the machine's existing editable install resolved `xianyu_system` from `D:/xianyu/app`; no code change was used to obtain the clean worktree-local rerun.

The historical CHG-0018 patch `4c5e1ac-chg0018-account-profile-publish-safety.patch` and its SHA256 `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD` are preserved unchanged. The T11 patch applies after that artifact.

## Production side effects

Because all four authorized failed records are already published, no new production runtime was required for T11 validation.

- New real publish attempts: 0
- Successful historical records retried: 0
- Unauthorized records touched: 0
- Other products published: 0
- Messages sent: 0
- Products deleted: 0
- Products offlined: 0
- Products polished: 0
- QR scans: 0
- Password batch logins: 0
- Token batch renewals: 0
- Containers changed: 0
- Database writes by this task: 0
- Redis writes by this task: 0
- GitHub writes by this task: 0

## T11 verdict

`CHG0018_T11_COMPLETE=true`

T11 is complete because the four authorized failures were recovered exactly, all four are now proven `ALREADY_PUBLISHED` by formal publish logs plus current catalog post-check, the duplicate-safe gate correctly prevented any re-publication, and the remaining T11 Profile/identity/readiness/retry contract is covered by the supplemental upstream patch and targeted/regression validation.

T12 remains explicitly incomplete and must be handled separately.
