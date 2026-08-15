# Fresh QR → Chat Auth Trace and Recovery — 2026-08-15

## Scope

This run was limited to the existing authentication chain:

`fresh QR -> authoritative DB Cookie -> Chat auth invalidation -> fresh Chat Token -> IM connect`

No new auth/session/verification subsystem was added. No Cookie was cleared, no Profile was deleted, no message was sent, and no product action was executed.

## Baselines

- CURRENT_GITHUB_BASE: `4d065a4bb8f00f863ae5bff2f74eb3ed68b2d516`
- CURRENT_BRANCH: `feat/CHG-0018-account-profile-publish-safety`
- UPSTREAM_CURRENT_MAIN_SHA: `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`
- PATCH_BASE_SHA: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- MARU_ACCOUNT_ID: `2214313339860`
- QR_LOGIN_SUCCESS_AT: `2026-08-15 18:34:41 +08:00`
- QR_SCANS_TRIGGERED_BY_THIS_RUN: `0`
- QR_SCANS_ADDITIONAL: `0`

## Fresh QR timeline

1. `18:34:41` — QR login reported success for `unb=2214313339860`.
2. `18:34:43` — the existing account row was updated and Single QR convergence started.
3. `18:34:43` — Round 1 called existing Chat auth invalidation. There was no live Chat client to disconnect; the existing `chat_{unb}` cache was explicitly expired.
4. `18:34:43` — the first post-QR Chat connect observed an expired cache and therefore generated fresh Chat auth rather than reusing the old token.
5. `18:34:43` — the local web Token request returned `FAIL_SYS_USER_VALIDATE`; response Cookie fields were merged into the authoritative DB Cookie.
6. `18:34:43–18:34:55` — existing CAPTCHA delegation ran and the configured local slider engine was rejected by Baxia.
7. `18:34:55` — **local regression:** because the Token-response Cookie rotation changed the auth fingerprint and Round 1 ended in `PLATFORM_VERIFICATION_REQUIRED` rather than `READY`, Round 2 invalidated Chat again and generated a second Token/CAPTCHA attempt.
8. `18:35:25` and `18:35:42` — two later Token generations came from explicit `/chat-new/connect` POSTs, not from a frontend background retry loop.

The current flow therefore had two separate facts:

- The **first fresh upstream-equivalent Token request already hit real platform Baxia**.
- XIANYU then had a **local Round-2 regression** that unnecessarily generated Chat auth a second time after that terminal PVR result.

## Identity / stale-auth findings

- `QR_UNB == DB_ACCOUNT_ID == CHAT_MYID == 2214313339860`: PASS.
- No account-context mismatch was found.
- The old Chat token was not reused after QR; the cache lookup was expired/miss.
- `GoofishImClient` construction still re-reads the current DB Cookie through `ImSessionManager.get_or_connect()`.
- Device ID source after the expired cache was `GENERATED_FROM_MYID`; no stale cached Device ID was reused.
- No evidence was found that a pre-QR Browser, Auto Reply, Chat, or Scheduler task overwrote the fresh QR Cookie after QR success.
- Observed post-QR Cookie writes were the QR/account write followed by Token-response Cookie merges begun after the QR event.
- Exact pre-QR / QR-write Cookie fingerprints were not logged before this trace began, so they are intentionally not reconstructed or guessed.

## First divergence from the 2026-08-14 successful sample

Historical same-account evidence on 2026-08-14 converged from one QR to Browser READY, Chat READY, Auto Reply ONLINE, and Publish READY.

Current first platform-level divergence: `TOKEN_API_RESPONSE` — the first fresh Chat Token request returned `FAIL_SYS_USER_VALIDATE` instead of reaching a usable Chat token.

Current first XIANYU-local regression after that divergence: `ROUND2_CHAT_INVALIDATION` — a fresh Round-1 terminal `PLATFORM_VERIFICATION_REQUIRED` result was not preserved, so Round 2 invalidated and generated Chat auth again.

## Minimal regression patch

Only the existing AccountService convergence orchestration was changed:

- Added `_should_preserve_chat_auth_on_followup_round(round_number, state)`.
- Round 2 now preserves both fresh `READY` **and** fresh `PLATFORM_VERIFICATION_REQUIRED` Chat results.
- When preserved, Round 2 does not call `invalidate_auth_consumers()` again.
- When preserved, Round 2 does not call `get_or_connect()` / Token / CAPTCHA again; it only reads current Chat diagnostic state.
- No new service, worker, scheduler, queue, verification lifecycle, CAPTCHA engine, Session owner, or Cookie coordinator was created.

Behavior tests also prove `old client/cache B -> fresh QR Cookie A -> old client cannot be reused -> new client uses A`.

## Upstream request equivalence

Upstream `main` at `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72` was fetched and compared directly.

The core `request_im_token()` request construction remains upstream-equivalent for:

- endpoint / API name
- appKey
- API version
- `sessionOption=AutoLoginOnly`
- request params and signing path
- Chrome/139 Token HTTP User-Agent behavior
- Origin / Referer
- Cookie source
- Device ID input
- HTTP timeout behavior
- local-web-first behavior in remote mode

Observed XIANYU differences in `common/services/im_token_api.py` are outside the core request construction and concern remote-fallback/session-expiry metadata and logging. No UA normalization or request-shape rewrite was introduced.

## Post-fix production-environment canary

The local execution wrapper could not reload/recreate the main Backend container without reading its protected `.env`; direct process termination is also correctly blocked by the tool. The main Backend process therefore **was not claimed as reloaded**.

To validate the patched code without bypassing credential protection, one isolated ASGI process was run **inside the existing production Backend container**, loading the patched source on disk and using the same production DB/network. It executed exactly one real route call:

`POST /chat-new/connect/2214313339860`

Result:

- POST count: `1`
- HTTP status: `200`
- final state: `PLATFORM_VERIFICATION_REQUIRED`
- error code: `CHAT_PLATFORM_VERIFICATION_REQUIRED`
- old Chat cache: expired, not reused
- local Token attempt: yes
- first Token result: `FAIL_SYS_USER_VALIDATE`
- remote fallback: attempted once; unavailable because the existing remote service balance was insufficient
- local result remained authoritative; it was not rewritten as LOGIN_REQUIRED / QR_REQUIRED
- existing CAPTCHA delegation: executed once
- CAPTCHA result: Baxia rejected the current configured local slider attempt
- second QR: not requested
- messages sent: `0`
- products changed: `0`

The canary changed the authoritative auth fingerprint from `08f403a3f394feadcdddba8754591844adbd0319deee723b8cbd3b0d1675bfdc` to `7003c8b198fe7b984e474ec1fea4f28b15be29fda0b25faa84667cc8eb652804` through a Token-response Cookie merge initiated by that single canary request. This is a post-QR platform response rotation, not evidence of a stale pre-QR writer.

## Auto Reply / PID safety

Before canary:

- active accounts: `6`
- Auto Reply connected: `6/6`
- target account connected: true

After canary:

- active accounts: `6`
- Auto Reply connected: `6/6`
- target account connected: true

WebSocket process safety remained:

- PID1: `docker-init`
- zombies: `0`

No WebSocket image/source was rebuilt for this fix, and Scheduler/Frontend were not changed by this run.

## Verification

- Targeted Fresh QR / Chat suites: `99 passed`
- Focused CHG-0018 suites: `222 passed`
- Python compileall: PASS
- Frontend build: NOT_REQUIRED_THIS_RUN
- `git diff --check`: PASS
- `python scripts/verify_repository.py`: `595 passed`, repository verification PASS

Fresh cumulative patch:

- PATCH_BASE_SHA: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- PATCH_SHA256: `12d27b708be105b60272ec4d75adf95e5db5bf27eb6b904f8e36220e5273515b`
- PATCH_BYTES: `469104`
- PATCH_CLEAN_APPLY: PASS
- PATCH_APPLY: PASS
- CONTENT_EQUIVALENCE: PASS

Content equivalence was verified in a clean worktree at the exact base using `git apply --index`; the resulting binary diff was again `469104` bytes with the exact same SHA-256.

## Strict result fields

- FRESH_QR_CHAT_AUTH_TRACE_COMPLETE: `true`
- CURRENT_GITHUB_BASE: `4d065a4bb8f00f863ae5bff2f74eb3ed68b2d516`
- UPSTREAM_CURRENT_MAIN_SHA: `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`
- MARU_ACCOUNT_ID: `2214313339860`
- QR_LOGIN_SUCCESS_AT: `2026-08-15 18:34:41 +08:00`
- DB_COOKIE_FP_BEFORE_QR: `UNAVAILABLE_PRE_TRACE`
- QR_LOGIN_COOKIE_FP: `UNAVAILABLE_PRE_TRACE`
- DB_COOKIE_FP_AFTER_QR: `UNAVAILABLE_AT_EXACT_T1; later pre-canary=08f403a3f394feadcdddba8754591844adbd0319deee723b8cbd3b0d1675bfdc`
- QR_UNB_MATCHES_ACCOUNT: `true`
- AUTH_CONVERGENCE_TRIGGERED: `true`
- AUTH_CONVERGENCE_ROUNDS: `2 (pre-fix incident)`
- CHAT_OLD_CLIENT_DISCONNECTED: `false (no live old client was present); manager entry absent after invalidation`
- CHAT_CACHE_INVALIDATION_CALLED: `true`
- CHAT_CACHE_VALID_AFTER_INVALIDATION: `false`
- OLD_CHAT_TOKEN_REUSED_AFTER_QR: `false`
- BROWSER_HEALTH_COOKIE_CHANGED: `UNKNOWN_NOT_CAPTURED_AT_EXACT_BOUNDARY`
- CHAT_CLIENT_CONSTRUCTION_COOKIE_FP_MATCHES_LATEST_DB: `true by code path + behavior test; exact historic FP was not pre-instrumented`
- TOKEN_API_COOKIE_FP_MATCHES_CHAT_CLIENT: `true by single-owner call path; no separate Cookie source exists in request_im_token()`
- DEVICE_ID_SOURCE: `GENERATED_FROM_MYID`
- CHAT_CACHE_LOOKUP_RESULT: `EXPIRED/CACHE_MISS`
- CHAT_TOKEN_API_CALL_COUNT_AFTER_QR: `4 observed before fix (2 convergence + 2 explicit POST); post-fix canary=1`
- FIRST_FRESH_CHAT_TOKEN_RESULT: `FAIL_SYS_USER_VALIDATE`
- TOKEN_EXPIRED_SELF_HEAL_RESULT: `NOT_THE_FIRST_FAILURE_BRANCH; no ordinary token-expired final classification`
- LOCAL_TOKEN_ATTEMPTED: `true`
- REMOTE_FALLBACK_ATTEMPTED: `false on first fresh incident because existing cooldown; true on post-fix canary`
- REMOTE_FALLBACK_RESULT: `BALANCE_INSUFFICIENT on post-fix canary; local result preserved`
- CHAT_TOKEN_REQUEST_UPSTREAM_EQUIVALENCE: `true for core request construction`
- TOKEN_REQUEST_DIFFS: `remote fallback/session-expiry metadata and logging only; no core request-shape diff`
- STALE_CHAT_COOKIE_USED: `false`
- STALE_COOKIE_WRITEBACK_AFTER_QR: `false based on observed writer timeline`
- COOKIE_WRITER_TIMELINE: `QR/account commit -> Chat Token response merge(2 fields) -> erroneous Round2 Chat Token merge(1) -> explicit connect Token merges -> one post-fix canary Token merge`
- ROUND2_PRESERVED_NEW_CHAT_AUTH: `false pre-fix for PVR; true after patch by behavior test`
- AUTH_STORM_AFTER_QR: `true pre-fix for convergence duplicate; fixed for Round2 terminal PVR path`
- PAST_VS_CURRENT_QR_CHAT_DIFF: `2026-08-14 reached Chat READY; 2026-08-15 first fresh Token reached FAIL_SYS_USER_VALIDATE/Baxia, then local Round2 duplicated auth generation`
- FIRST_DIVERGENCE_STAGE: `platform=TOKEN_API_RESPONSE; local_regression=ROUND2_CHAT_INVALIDATION`
- ROOT_CAUSE_FRESH_QR_CHAT_FAILURE: `real fresh-auth platform Baxia is the remaining blocker; XIANYU also had a Round2 duplicate-auth regression that was fixed`
- FIX_TYPE: `MINIMAL_REGRESSION_PATCH`
- RECENT_CLEANUP_QR_CONVERGENCE_REGRESSION: `true`
- REAL_PLATFORM_BAXIA_AFTER_FRESH_QR: `true`
- CAPTCHA_DELEGATION_EXECUTED: `true`
- CAPTCHA_ENGINE: `existing local slider_stealth/Patchright path; DrissionPage fallback disabled/unavailable in current production configuration`
- CAPTCHA_RESULT: `BAXIA_REJECTED`
- POST_FIX_CHAT_CONNECT_COUNT: `1`
- CHAT_STATE_AFTER: `PLATFORM_VERIFICATION_REQUIRED`
- CHAT_RUNTIME_CONNECTED: `false`
- CONVERSATION_LIST_SUCCESS: `false`
- CONVERSATION_COUNT: `N/A`
- AUTO_REPLY_BEFORE: `6/6`
- AUTO_REPLY_AFTER: `6/6`
- AUTO_REPLY_REFRESH_STORM_REGRESSION: `false after patch path; post-fix canary did not touch Auto Reply`
- QR_SCANS_ADDITIONAL: `0`
- REAL_MESSAGES_SENT: `0`
- REAL_PRODUCTS_PUBLISHED: `0`
- WEBSOCKET_PID1: `docker-init`
- WEBSOCKET_ZOMBIES: `0`
- NEW_SUBSYSTEMS_CREATED: `0`
- TARGETED_TESTS: `99 passed; focused CHG-0018=222 passed`
- REPOSITORY_TESTS: `595 passed`
- PYTHON_COMPILE: `PASS`
- FRONTEND_BUILD: `NOT_REQUIRED_THIS_RUN`
- GIT_DIFF_CHECK: `PASS`
- PATCH_BASE_SHA: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- PATCH_SHA256: `12d27b708be105b60272ec4d75adf95e5db5bf27eb6b904f8e36220e5273515b`
- PATCH_CLEAN_APPLY: `PASS`
- PATCH_APPLY: `PASS`
- CONTENT_EQUIVALENCE: `PASS`
- MAIN_BACKEND_PATCH_FILE_PRESENT_ON_DISK: `true`
- MAIN_BACKEND_PATCH_PROCESS_RELOADED: `false — local execution wrapper could not access protected .env to recreate, and direct process kill is blocked`
- BLOCKER: `the remaining Chat usability blocker is real Baxia on a fresh upstream-equivalent request; separately, main Backend runtime reload of the fixed AccountService remains blocked by execution-tool container-restart permissions`
