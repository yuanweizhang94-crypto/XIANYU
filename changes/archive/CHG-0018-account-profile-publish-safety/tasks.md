# CHG-0018 Tasks

Status: ARCHIVED

Change ID: CHG-0018-account-profile-publish-safety

- [x] T1 Implement P0 credential safety and false-disable prevention.
- [x] T2 Run P0 targeted tests and commit the P0 boundary.
- [x] T3 Implement P1 persistent Profile publish readiness.
- [x] T4 Implement P2 Profile initialization and repair boundaries.
- [x] T5 Implement P3 shared read-only publish preflight.
- [x] T6 Implement P4 canonical browser lock usage for publish readiness paths.
- [x] T7 Run P1-P4 targeted tests and commit the Profile readiness boundary.
- [x] T8 Generate CHG-0018 patch artifact, evidence, and full validation.
- [x] T9 Complete CANARY-A01 UI/Profile/preflight runtime verification and native auto-polish canary hardening.
- [x] T10 Return CHG-0018 to VERIFYING after scoped runtime evidence and repository validation.
- [x] T10A Add default-off exact platform-item scope and default-compatible item-list no-retry control to the existing upstream-native paths.
- [x] T10B Validate the exact-item/no-retry patch, regenerate the Vendor Patch, and deploy only the scheduler image while global polish remains disabled.
- [x] T10C Repair item-list-to-polish Session handoff, add one bounded polish auth recovery, validate, deploy only Scheduler, and run the owner-authorized four-item fixed-account polish validation.
- [x] T11 Fix real batch publish Profile runtime, readiness classification, and duplicate-safe retry path.
- [x] T12 Return CHG-0018 to VERIFYING after real batch publish recovery evidence, repository validation, and CI.

## T9 result

- Frontend CHG-0018 image was deployed without restarting WebSocket, backend, MySQL, Redis, or creating a second runtime.
- CANARY-A01 Profile initialization completed from the authoritative database Cookie path, and read-only publish preflight returned ready without filling, uploading, or publishing.
- Auto-polish root causes were classified as `SCHEDULER_NOT_RUNNING` and `PLATFORM_DAY_NOT_READY` before recovery; scheduler task isolation was corrected to only `day_switch`, `fetch_items`, and `polish`.
- Native scoped polish canary processed one CANARY-A01 item successfully with other-account polish delta `0`, password-login trigger `0`, and account-disabled delta `0`.
- The single scheduler then remained running and processed only CANARY-A01 remaining eligible polish items; follow-up polish intervals found no duplicate work.

## T10 result

- CHG-0018 returned to `VERIFYING` after targeted tests, repository validation, patch clean-apply checks, and masked runtime evidence.

## T10A result

- `PolishTaskService.execute` now accepts internal optional `platform_item_ids` and `retry_on_token_expiry` controls without adding a second execution path.
- Exact platform-item scope is enforced inside the existing unpolished-item SQL `SELECT`; absent, cross-account, and already-polished targets fail closed without fallback.
- `ItemInfoManager.get_item_list_info` keeps retry enabled by default and supports a one-request strict mode that performs no recursive retry or response-Cookie update.
- The existing polish HTTP method has no recursive retry path; T10C may orchestrate one native auth recovery and one final retry only after explicit Session/Token expiry.

## T10B result

- CHG-0018 targeted tests passed 30/30; CHG-0017 regression tests passed 58/58; repository verification passed 595/595.
- Vendor Patch parse, staged-base clean apply, and current-source byte equivalence checks passed; new SHA256 is `03F79D07F1177786CF9F9A8B835E71D106BBC4099627A7D39CCA0A3D2F317CCF`.
- Only `xianyu_chg0017_scheduler` was replaced with `xianyu-chg0018-scheduler:56d62e2-03f79d0`; the prior scheduler container and image were retained for rollback.
- Backend, frontend, MySQL, Redis, and WebSocket were not restarted. `polish=false` and `day_switch=true` were confirmed after deployment.
- No real polish, publish, login, Cookie refresh, message send, database business write, Redis write, GitHub write, or PR #26 change occurred.

## T10C result

- Item-list Token/Cookie rotation is handed back through the existing `merge_account_cookie_fields` path so later polish does not reload stale account Cookie fields.
- An explicit polish Session/Token expiry may perform at most one existing auth recovery plus one final polish retry; no third polish request is allowed.
- CHG-0018 targeted tests passed 36/36, CHG-0017 regression tests passed 58/58, and repository tests passed 595/595 before final deployment.
- Final Vendor Patch SHA256: `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`.
- Final production Scheduler image: `xianyu-chg0018-scheduler:56d62e2-94c8682`.
- Owner-recovered account `2219319284219` processed the four fixed platform items with four explicit `SUCCESS::调用成功` responses, four `is_polished=false -> true` transitions, zero auth failures, zero unknown failures, zero other-account requests, and zero out-of-scope requests.
- `END_TO_END_ACCOUNT_POLISH_VERIFIED=true` and the existing scheduled-task path subsequently re-enabled global polish while `day_switch=true` remained unchanged.
- One natural global Scheduler cycle completed with `RestartCount=0`; expired-account sessions failed closed after one bounded recovery attempt while later accounts continued.

## Governance closeout boundary

- Repository status definitions do not contain `VERIFIED`; the next formal status after `VERIFYING` is merge-bound `MERGED`.
- PR #26 must remain Draft/Open/Unmerged, so this task truthfully keeps CHG-0018 at `VERIFYING` and does not invent a status.
- The historical polish closeout did not prove real-batch-publish recovery; that gap is now separately closed by T11/T12 evidence. CHG-0018 nevertheless remains `VERIFYING` until its merge-bound transition.

## T11 target

- Confirm the real batch publish executor, runtime image, and call chain from masked production logs and database records.
- Share one canonical persistent Profile root between backend publisher and websocket/Profile execution containers.
- Ensure batch publish passes authoritative `account_id` and `owner_id`, not only caller-supplied Cookie data.
- Replace the old early `publish_form_not_rendered` check with 60-second page-state polling and specific failure reasons.
- Retry only owner-authorized failed records classified as `NOT_PUBLISHED` after duplicate checks.

## T11 result

- Recovered exactly the four owner-authorized historical failed publish logs `56`, `59`, `60`, and `61` from batch `a74c06a5-690a-414a-b9a7-57511941c270`; no successful historical record or unrelated record entered the recovery scope.
- Database and current catalog post-check proved all four records had later formal publish successes for the same owner/account/material and matching platform-item identity/title, so all four were classified `ALREADY_PUBLISHED` and `NOT_PUBLISHED_CONFIRMED=0`.
- Duplicate-safe gating therefore produced `REAL_PUBLISH_ATTEMPTS=0`; no duplicate product was published merely to satisfy the controlled-validation authorization.
- The production backend remains the native real batch executor. Backend and WebSocket share the same `xianyu_chg0017_browser_data` volume at `/app/browser_data`; the four authorized account Profiles exist under that canonical root.
- The running Pilot backend has no browser-data mount and no Chromium/Chrome executable, and no Pilot Scheduler/WebSocket is running; `SECOND_EXECUTOR_RUNNING=false` for the publish browser path.
- T11 keeps `PATCH_UPSTREAM`: batch publish forwards the database-loaded account identity and authoritative owner, each record uses an independent context, and the existing publisher continues to own the account lock/global browser slot and authoritative Cookie lookup.
- Publish readiness now waits up to 60 seconds and classifies `verification_required`, `page_load_timeout`, and `page_structure_mismatch` instead of early `publish_form_not_rendered`/generic timeout failures. Legacy exception inputs are compatibility-normalized.
- T11 supplemental Vendor Patch SHA256 is `99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882`; clean apply and source Git-blob equivalence passed 4/4.
- CHG-0018 targeted suites passed 38/38, CHG-0017 regression suites passed 58/58, `validate_change.py` passed, CHG-0018 governance acceptance passed 9/9, and repository verification passed 596/596 with worktree-local module resolution.
- No frontend source changed and no production container was replaced or restarted. T11 does not imply that any of the four historical failures were newly published.
- Evidence: `evidence/20260809-t11-controlled-real-batch-publish-recovery.md`.

## T12 result

- T11 commit `8ffce692140d77a0b8bb46a84afc879d5d6b68a0` was cleanly integrated into the main-based PR #31 lineage without reintroducing the archived CHG-0017 suspended path.
- The single formal CHG-0018 Vendor Patch was regenerated from exact Git source layers and now includes T11; final SHA256 is `B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111` while the historical T11 supplement remains locked at `99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882`.
- Patch parse, strict clean apply, applied diff check, and source Git-blob equivalence passed; equivalence is 27/27.
- Exact final upstream suites are CHG-0018 targeted 38/38 and CHG-0017 regressions 58/58. The main-based repository passed 588/588 before the checkbox transition and again 588/588 after T12 completion and generated-state refresh.
- Frontend source did not change in T11/T12; no frontend or production runtime was deployed, restarted, or rebuilt.
- Secret scans passed for T11 evidence, T12 evidence, the formal Patch, and T12 Git additions. Real product actions and real publish attempts remained zero.
- CHG-0018 remains `VERIFYING`; T12 completion does not set `MERGED`, `ARCHIVED`, or any invented `VERIFIED` state. Remote delivery readiness additionally requires the normal PR #31 push and exact-final-head GitHub CI to be green.
- Evidence: `evidence/20260809-t12-final-validation-and-ci.md`.

## Post-merge archive closeout

- PR #31 merged normally into `main` at merge commit `64c37d20a00f77d7e860705123244692d134dd48`.
- All 12 formal T1-T12 task groups are complete and the Change is archived after merge.
- Exact PR #31 head CI was green before merge; the archive operation contains governance-only state movement and no product/runtime side effects.

## Upstream capability audit

Pinned upstream account, password refresh, Cookie renewal, publisher, preflight diagnostics, and browser concurrency paths are the implementation sources.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

## Existing local implementation search

Local wrapper and archived changes were checked for overlap; no local runtime replacement is allowed.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Tasks must not add a second sender, publisher, login system, Token system, browser broker, service, queue, or database table.

## Why upstream cannot satisfy the requirement

Pinned upstream lacks the required safety and Profile lifecycle guarantees without a minimal patch.

## Approved exception ADR

Not applicable.

## Component owner

Pinned upstream runtime paths and XIANYU governance patch ownership.

## Retirement plan for overlapping local code

No overlapping local production code is introduced.
