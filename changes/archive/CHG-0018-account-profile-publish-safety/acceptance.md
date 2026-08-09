# CHG-0018 Acceptance

Status: ARCHIVED

Change ID: CHG-0018-account-profile-publish-safety

## Acceptance

- P0 account APIs do not return raw `login_password`.
- Default account editing does not load, display, or submit saved passwords.
- Credential editing requires an explicit mode and dirty tracking.
- Password clearing requires an explicit operation.
- `no_credentials` and `bad_credentials` do not modify `XYAccount.status`.
- Publish execution uses authoritative `account_id` and database Cookie lookup, not caller-supplied account/Cookie pairing.
- Missing Profile returns a clear diagnosis without temp Profile fallback.
- API Cookie renewal does not imply Profile initialization.
- Existing healthy Profiles are not opened during passive checks.
- Formal publish runs shared preflight and publish inside one context for the concrete attempt.
- Batch publish does not keep one long-lived context for the whole batch or all accounts.
- Batch publish passes authoritative `account_id` and `owner_id` into the existing upstream publisher and does not silently fall back to a temporary Cookie-only context.
- Backend publisher and websocket/Profile execution containers use the same mounted canonical `browser_data` Profile root.
- Publish-page preflight waits up to 60 seconds and returns specific failure reasons instead of using `publish_form_not_rendered` for slow load, login, verification, or page-structure mismatch.
- Each browser task acquires at most one account lock and one global browser slot.
- No message sending, true product publish, CHG-0017 T17, archive, merge, or PR #26 state change occurs. Real polish is limited to the project-owner authorized controlled validation and normal production Scheduler operation after explicit global re-enable authorization.
- Runtime verification may perform the project-owner authorized fixed-account polish validation for account `2219319284219` and only platform items `1070297095320`, `1073348972265`, `1070510695919`, and `1073905692512`. It must not create products, publish products, send messages, start a second scheduler path, or affect PR #26.
- Auto-polish validation must use the pinned upstream native `PolishTaskService.execute` path with explicit account and `platform_item_ids` scope. Each item normally receives one polish request; only an explicit Session/Token-expiry response may trigger one native auth recovery and one final polish retry, with no third request.
- Internal controlled auto-polish may additionally provide `platform_item_ids`; when provided, the existing SQL query must select only the intersection of the scoped account, unpolished state, and requested platform item IDs, with no fallback to another item.
- `platform_item_ids=None` and `retry_on_token_expiry=True` must preserve default production behavior.
- `ItemInfoManager.get_item_list_info(..., retry_on_token_expiry=False)` must send at most one HTTP request and return the first auth, token, risk, or unknown failure without recursive retry or response-Cookie update.
- The polish request path must remain the existing single-request method; no parallel MTop executor or new scheduler/API path is allowed.
- Redis platform day read failures must fail closed without resetting polish state or running polish.
- Missing platform day must block polish until the day switch task safely initializes the platform day after a successful item-state reset.
- Missing or bad account credentials in polish must not trigger password login for accounts without complete credentials and must not disable the account.
- Polish API logs must not record Cookie, Token, full API responses, or full account identifiers.
- Token-expiry retry during polish is bounded to one retry.
- Real batch publish recovery may retry only the four owner-authorized failed publish records after duplicate checks classify them as `NOT_PUBLISHED`; successful or unknown records must not be retried.

## Test matrix

- P0 targeted credential/API/frontend/password-refresh tests.
- P1-P4 targeted Profile, preflight, and lock lifecycle tests.
- Existing CHG-0017 regression tests.
- Exact-item SQL-scope, target-not-eligible, duplicate-unverified, and item-list no-retry/default-retry tests in `tests/test_chg0018_auto_polish_safety.py`.
- Actual frontend scripts discovered from `package.json`.
- `python scripts/validate_change.py`.
- `python scripts/verify_repository.py`.
- Patch clean apply and blob equivalence checks.

## P0 result

- Raw `login_password` is removed from ordinary account detail responses.
- Account editing defaults to no credential mode, empty password input, dirty tracking, and explicit password clearing.
- `no_credentials` and `bad_credentials` password-refresh paths keep `XYAccount.status` unchanged.
- Password and full Cookie values are removed from the touched refresh logs.
- Targeted upstream test: `python -m pytest tests/test_chg0018_credential_safety.py -q`.
- Frontend build: `npm run build`.
- Patch artifact: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`.
- Patch SHA256: `F15F2161213EE7CD8B952D3DD475DEA18BA12F56570E332CE4711BD87D6350E2`.

## Real batch publish recovery target

- Executor service: backend-web native batch publish service.
- Required fix: canonical Profile root shared through the existing Cookie/Profile service and deployment volume, authoritative account identity forwarding, and specific publish-page readiness classification.
- Required safety: duplicate check before retry, max one retry per authorized failed record, no Token batch renewals, no QR batch scans, no messages, and no PR #26 state change.

## P1-P4 result

- Publish execution passes authoritative account identity and owner scope to the existing publisher path.
- The publisher loads the latest Cookie from the authoritative account record and opens the existing persistent account Profile.
- Missing Profile and busy Profile states return existing-style `failure_reason` values: `profile_missing` and `browser_busy`.
- Formal publish calls shared `preflight_publish_form()` before form mutation in the same context.
- `preflight_only` returns readiness without upload, form fill, or publish click.
- Browser lifecycle uses existing captcha concurrency managers for one global slot and one account lock, released during close.
- Targeted upstream tests: `python -m pytest tests/test_chg0018_credential_safety.py tests/test_chg0018_profile_publish_readiness.py -q`.
- CHG-0017 regression tests: `python -m pytest tests/test_chg0017_publish_login_submit.py tests/test_chg0017_reply_allowlist.py tests/test_chg0017_ai_prompt_validation.py tests/test_chg0017_gemini_response_parser.py -q`.

## Exact-item/no-retry canary patch

- Reuse decision remains `PATCH_UPSTREAM`.
- No new service, HTTP API, frontend control, scheduler task, model, database table, Token system, Cookie recovery system, or Profile manager is introduced.
- Controlled parameters are internal and default-safe: `platform_item_ids=None` and `retry_on_token_expiry=True`.
- Exact item selection is applied in the existing `XYCatalogItem` `SELECT`, not by post-query Python filtering.
- Missing, cross-account, or already-polished targets fail closed as `target_item_not_eligible` and do not select another item.
- Item-list strict mode disables recursive Token-expiry and exception retry and suppresses response-Cookie updates for that call.
- The polish request method itself contains no recursive retry path. `PolishTaskService` may orchestrate at most one native Session/Token recovery followed by one final polish retry, so the per-item polish request ceiling is two.
- The controlled validation phase kept `polish.enabled=false` and `day_switch.enabled=true` until the four-item end-to-end run succeeded. After owner authorization and successful verification, the existing scheduled-task management path re-enabled `polish.enabled=true` without changing its interval; `day_switch.enabled=true` remains unchanged.
- Final validation result before production enablement: CHG-0018 targeted tests 36/36, CHG-0017 regressions 58/58, repository verification 595/595, patch parse/clean-apply/source-equivalence passed.
- Final production Scheduler image: `xianyu-chg0018-scheduler:56d62e2-94c8682`; Vendor Patch SHA256: `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`.
- Historical exact-item deployment evidence remains in `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260807-exact-item-no-retry-canary-patch.md`; current production state is recorded in `evidence/20260807-final-production-enable-closeout.md`.

## Final validation result

- Combined upstream targeted and regression tests: 68 passed.
- Frontend build: passed with `npm run build`.
- Frontend lint discovery: `npm run lint` exists, but the upstream frontend checkout does not contain an ESLint config file; this is recorded as a non-blocking upstream tooling gap, not a CHG-0018 code failure.
- Patch parse check: passed with `git apply --numstat --unidiff-zero`.
- Patch staged-base apply check: passed with `git apply --check --cached --whitespace=error-all --unidiff-zero`.
- Patch diff check: passed for `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`.
- Evidence: `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260805-final-validation.md`.
- This subsection is historical pre-runtime validation; later controlled production polish and global enablement supersede its former no-production-operation boundary.
- PR #26 state changed: no.

## Runtime verification result

- Evidence: `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260805-runtime-profile-preflight-auto-polish.md`.
- Target alias: `CANARY-A01`.
- Frontend deployed: yes.
- UI/API password status: unconfigured credentials; no raw `login_password` path is accepted.
- Remark regression: passed for the target account without credential resubmission.
- Profile created: yes.
- Profile healthy: yes.
- Manual verification required: no.
- Read-only preflight ready: yes.
- Preflight failure reason: null.
- Auto-polish root cause before recovery: `SCHEDULER_NOT_RUNNING` and `PLATFORM_DAY_NOT_READY`.
- Auto-polish code fixed: yes.
- Account auto-polish enabled: yes, only for `CANARY-A01`.
- Catalog item count: 7.
- Platform day ready: yes.
- Real polish canary executed: yes, one scoped item.
- Real polish canary success: yes.
- Other accounts polished: 0.
- Password login triggered for canary: false.
- Target account disabled: false.
- Synthetic messages sent: 0.
- Products created: 0.
- Products published: 0.
- Scheduler running: yes.
- Scheduler enabled tasks: `day_switch,fetch_items,polish`.
- `fetch_orders`, `dm_send`, and `auto_order` executed: false.
- Historical runtime patch SHA256 at that stage: `F15F2161213EE7CD8B952D3DD475DEA18BA12F56570E332CE4711BD87D6350E2`; this is superseded by the final production Patch SHA below.

## Final production verification and enablement

- `SESSION_RECOVERY_CONFIRMED=true` for controlled account `2219319284219` before the final fixed-scope run.
- Fixed platform items: `1070297095320`, `1073348972265`, `1070510695919`, and `1073905692512`.
- All four returned `API_CODE=SUCCESS` and `API_MESSAGE=调用成功`.
- All four changed `is_polished=false -> true` through the formal service path.
- `TOTAL_PLATFORM_POLISH_REQUESTS=4`, `SUCCESS_ITEM_COUNT=4`, `DUPLICATE_ITEM_COUNT=0`, `AUTH_FAILURE_ITEM_COUNT=0`, `UNKNOWN_FAILURE_ITEM_COUNT=0`, `SKIPPED_AFTER_FAILURE_COUNT=0`.
- `OTHER_ACCOUNT_PLATFORM_REQUESTS=0` and `OUT_OF_SCOPE_ITEM_REQUESTS=0` for the controlled run.
- `END_TO_END_ACCOUNT_POLISH_VERIFIED=true` and `SAFE_TO_REENABLE_GLOBAL_POLISH=true`.
- Duplicate classification remains `duplicate_unverified` and does not become explicit API success.
- Session/Token expiry remains fail-closed. Authentication recovery is bounded to at most one existing recovery plus one final polish retry; no third request or infinite recovery is allowed.
- Global `polish.enabled=true` was persisted through the existing scheduled-task management path and reloaded by the existing Scheduler internal reload path. The 60-second interval was unchanged and `day_switch.enabled=true` remained unchanged.
- One natural production Scheduler cycle completed. Healthy accounts continued to explicit success, expired sessions stopped their own account after one bounded recovery attempt while later accounts continued, and the already-completed controlled account had no remaining eligible items.
- Production Scheduler remained running with `RestartCount=0`; no second Scheduler or other-service restart occurred.
- Final Vendor Patch SHA256: `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`.
- Final production Scheduler image: `xianyu-chg0018-scheduler:56d62e2-94c8682`.
- Evidence: `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260807-final-production-enable-closeout.md`.
- Account Session expiry is an operational account-health condition and is no longer a CHG-0018 code acceptance blocker when the bounded fail-closed behavior is preserved.

## T11/T12 final integration result

- Historical publish failures are not treated as proof of platform non-publication. All four owner-authorized failed records were duplicate/platform-state checked and classified `ALREADY_PUBLISHED`; `NOT_PUBLISHED_CONFIRMED=0` and `REAL_PUBLISH_ATTEMPTS=0`.
- T11 preserves the existing backend Publisher as the sole publish executor, the shared canonical persistent Profile root, authoritative `account_id` and `owner_id`, one context per concrete publish attempt, one account lock plus one global slot, and the 60-second specific readiness classification.
- The T12 single formal Vendor Patch includes the complete prior CHG-0018 source plus T11 and has SHA256 `B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111`; the historical T11 supplemental SHA256 remains `99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882`.
- Formal Patch parse, strict clean apply, applied diff check, and exact source Git-blob equivalence passed 27/27.
- Exact upstream validation passed CHG-0018 targeted 38/38 and CHG-0017 regressions 58/58. Main-based repository pre-final verification passed 588/588 before the T12 checkbox transition, and exact final-state repository validation after generated state refresh also passed 588/588.
- T11/T12 changed no frontend source and performed no production runtime deployment, container restart, real publish, product mutation, login, QR scan, message send, database business write, or Redis business write.
- Evidence: `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260809-t11-controlled-real-batch-publish-recovery.md` and `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260809-t12-final-validation-and-ci.md`.

## Governance closeout boundary

- The repository defines `DRAFT`, `APPROVED`, `IMPLEMENTING`, `VERIFYING`, `MERGED`, and `ARCHIVED`; it does not define `VERIFIED`.
- T11 and T12 are complete as delivery-validation tasks, but the next formal status after `VERIFYING` is merge-bound. CHG-0018 therefore remains `VERIFYING` until PR #31 is explicitly reviewed and merged in a separate decision.
- PR #31 must remain Draft/Open/Unmerged at T12 completion; T12 completion itself does not Ready, Merge, Close, or retarget it.

## Post-merge archive closeout

- PR #31 merged normally into `main` at `64c37d20a00f77d7e860705123244692d134dd48` after exact-head CI passed.
- CHG-0018 T1-T12 were all complete before merge; T11 correctly performed zero duplicate publishes because all four authorized historical failures were proven already published.
- The Change is archived with no additional production, account, product, message, container, database, or Redis operation.

## Upstream capability audit

Acceptance is based on the pinned upstream account, password refresh, Cookie renewal, publisher, preflight diagnostics, and browser concurrency paths.

## Pinned upstream evidence

Pinned upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.

## Existing local implementation search

No local runtime replacement is allowed.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Acceptance fails if the Change adds a parallel sender, publisher, login system, Token system, Profile store, browser broker, service, queue, or table.

## Why upstream cannot satisfy the requirement

Pinned upstream requires a minimal patch to satisfy the safety and Profile readiness acceptance criteria.

## Approved exception ADR

Not applicable.

## Component owner

Pinned upstream runtime paths and XIANYU governance patch ownership.

## Retirement plan for overlapping local code

No overlapping local production code is introduced.
