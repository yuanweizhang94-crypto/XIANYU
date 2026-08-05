# CHG-0018 Acceptance

Status: IMPLEMENTING

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
- No real account operation, message sending, true publish, CHG-0017 T17, archive, merge, or PR #26 state change occurs.
- Runtime verification may perform only the project-owner authorized CANARY-A01 read-only Profile/preflight checks and at most one native auto-polish canary item. It must not create products, publish products, send messages, start a second scheduler path, or affect PR #26.
- Auto-polish must use the pinned upstream native scheduler path with an explicit account scope and max-one-item limit for the canary.
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

## Final validation result

- Combined upstream targeted and regression tests: 68 passed.
- Frontend build: passed with `npm run build`.
- Frontend lint discovery: `npm run lint` exists, but the upstream frontend checkout does not contain an ESLint config file; this is recorded as a non-blocking upstream tooling gap, not a CHG-0018 code failure.
- Patch parse check: passed with `git apply --numstat --unidiff-zero`.
- Patch staged-base apply check: passed with `git apply --check --cached --whitespace=error-all --unidiff-zero`.
- Patch diff check: passed for `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`.
- Evidence: `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260805-final-validation.md`.
- Production operations executed: none.
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
- Patch SHA256: `F15F2161213EE7CD8B952D3DD475DEA18BA12F56570E332CE4711BD87D6350E2`.

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
