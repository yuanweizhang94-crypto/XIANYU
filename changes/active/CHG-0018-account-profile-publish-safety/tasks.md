# CHG-0018 Tasks

Status: VERIFYING

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
- [ ] T11 Fix real batch publish Profile runtime, readiness classification, and duplicate-safe retry path.
- [ ] T12 Return CHG-0018 to VERIFYING after real batch publish recovery evidence, repository validation, and CI.

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
- T11/T12 remain open because the final polish production evidence does not prove the separate real-batch-publish runtime recovery. They are not falsely marked complete during this closeout.

## T11 target

User outcome: Fix the existing upstream Publisher category-selection defect and validate one owner-authorized ITEM_08 publish without changing login/Profile/Cookie or product content.
Confirmed blocker: `_select_category()` swallows its own unsupported-category exception and both category selection and submit pre-check can misread hidden/stale `网页版暂不支持发布此分类` DOM as the current category state.
Smallest success test: Targeted category tests pass, publish/Profile regressions pass, only Backend is deployed, and ITEM_08 performs at most one real publish submit after a current visible supported matching UI category is selected.

- Confirm the real batch publish executor, runtime image, and call chain from masked production logs and database records.
- Share one canonical persistent Profile root between backend publisher and websocket/Profile execution containers.
- Ensure batch publish passes authoritative `account_id` and `owner_id`, not only caller-supplied Cookie data.
- Replace the old early `publish_form_not_rendered` check with 60-second page-state polling and specific failure reasons.
- Retry only owner-authorized failed records classified as `NOT_PUBLISHED` after duplicate checks.

### T11 category-selection repair evidence (2026-08-11)

- Reuse decision remains `PATCH_UPSTREAM`; no second Publisher, category system, login path, Profile path, Cookie path, service, worker, or schema was introduced.
- Root cause confirmed in the existing Publisher: unsupported-category exceptions were swallowed by broad `except Exception`, the selection flow was duplicated, and global unsupported-text lookup could observe hidden/stale DOM.
- The existing Publisher now uses one UI-candidate loop and one shared current-visible unsupported-category check for both category selection and the pre-submit gate. Category IDs are recorded only when the rendered option exposes an ID; no category ID is injected or forced.
- Targeted CHG-0017 publish tests passed 17/17, including five category regressions; CHG-0018 Profile/publish-readiness tests passed 7/7; repository verification passed 595/595 before Backend-only deployment.
- Production deployment overlaid only `backend-web/app/services/xianyu_publisher.py` on the previously deployed Backend image, producing `xianyu-chg0018-backend-web:44c8ae9-category-9914805`; MySQL, Redis, Scheduler, WebSocket, and Frontend container identities/start times were unchanged.
- ITEM_08 account `1034641456` preflight remained ready. The current UI rendered ten candidates; current semantic matches `其他服务`, `其他技能服务`, and `其它互联网/软硬件相关服务` each showed the visible Web-unsupported warning. The unrelated `软件安装包/序列号/激活码` candidate was not used. No supported semantic match was selected, so publish submit count and publish network-request count remained zero.
- Final read-only account sync returned two products and no ITEM_08 title match. This validation therefore closes the category false-positive/exception-swallow defect while truthfully leaving ITEM_08 uncreated; no category mismatch or platform-limit bypass was attempted.

## T11 upstream 5d690ac Session/Token minimal sync contract (2026-08-11)

User outcome: adopt only the newer upstream Session-expiry recognition and Token fallback diagnostics needed to keep healthy sessions reusable and avoid pointless slider handling after confirmed Session expiry.

Confirmed blocker: pinned runtime `4c5e1ac5f532c7313365d70409ae115305de8a55` lacks upstream `5d690ac` unified Session-expiry result recognition, remote fallback failure propagation, local/remote timing separation, and Session-before-captcha ordering; the upstream no-credentials disable behavior conflicts with CHG-0018 and must not be copied.

Smallest success test: targeted Session/Token and renew tests prove healthy/temporary failures do not trigger login, explicit Session expiry reaches the existing renew/login chain before captcha without disabling no-credential accounts, canonical Profile and Publisher regressions remain unchanged, and only services owning the changed runtime modules are deployed.

- Reuse decision: `PATCH_UPSTREAM` by selective transplant from upstream commit `5d690ac6e77d415b886b1e87b5aaf446f0f29c48`; no blind cherry-pick.
- Duplicate-development risk: none; existing `im_token_api`, `token_refetch`, remote Token risk-log helper, and `CookieTokenManager` remain the sole execution owners.
- Compatibility boundary: preserve CHG-0018 `no_credentials` / bad-credential non-disable safety, canonical Profile rules, QR-login workflow, Publisher source, category logic, database schema, and existing browser locks.
- Rollback: revert only the selective `5d690ac` Session/Token hunks and the corresponding targeted tests; no data migration is required.

### T11 upstream 5d690ac Session/Token sync result

- Evaluated the four real owner/dependency files changed by upstream `5d690ac`: `im_token_api.py`, `captcha/token_refetch.py`, `remote_token_risk_log_service.py`, and WebSocket `cookie_token_manager.py`.
- Added unified Session-expired detection, remote fallback failure propagation, and local/remote Token timing while preserving the existing Cookie renewal/login chain.
- Moved explicit Session-expired handling before captcha in WebSocket; the conflicting upstream no-credentials account-disable hunk was not copied, preserving CHG-0018 credential safety.
- Added `tests/test_chg0018_session_token_upstream_sync.py`; final Session/Token targeted result is 10/10 passed.
- Combined Session/Token, credential/login, Profile, CHG-0017 publish, and CHG-0018 auth/polish regression result is 63/63 passed; governance full pytest is 595/595 passed.
- Vendor Patch SHA256 after this sync: `756410DB732B654D6A7DB62D9236A7477D1C608C7778AD5779D723308D807D69`.
- Deployed only Backend `xianyu-chg0018-backend-web:44c8ae9-session-5d690ac` and WebSocket `xianyu-chg0018-websocket:44c8ae9-session-5d690ac` using overlays on their current production images so unrelated dirty-worktree files were not pulled into deployment.
- Backend and WebSocket health checks passed; MySQL, Redis, Scheduler, and Frontend container identities were unchanged and no volume was deleted.
- Publisher/category/QR/Profile/schema/App-handoff code changed by this sync: none. Real product actions: 0.
- Evidence: `evidence/20260811-upstream-5d690ac-session-token-sync.md`.

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
