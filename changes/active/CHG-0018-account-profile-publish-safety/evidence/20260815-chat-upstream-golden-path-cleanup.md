# CHG-0018 Chat Upstream Golden Path Restore + Recent Complexity Cleanup Evidence

Date: 2026-08-15 (Asia/Taipei)

## Execution contract

- Task: `CHAT_UPSTREAM_GOLDEN_PATH_RESTORE_AND_RECENT_COMPLEXITY_CLEANUP=true`
- XIANYU branch: `feat/CHG-0018-account-profile-publish-safety`
- Root pre-run HEAD: `ed51168a666987a80b34d8bc70ca6840dd183506`
- Vendor Patch base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- Upstream current `main`, independently fetched on 2026-08-15: `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`
- Principle: Upstream First. No second Chat executor, Session owner, CAPTCHA solver, verification service, scheduler, or status authority was introduced.

## Safety boundary

This run did not send a real message, publish/relist/offline a product, trigger a QR scan, clear Cookies, delete browser Profiles, bulk-run verification, or restart/redeploy WebSocket/Scheduler for the final cleanup.

- `REAL_MESSAGES_SENT=0`
- `REAL_PRODUCTS_PUBLISHED=0`
- `REAL_PRODUCTS_RELISTED=0`
- `REAL_PRODUCTS_OFFLINED_BY_TEST=0`
- `QR_SCANS_TRIGGERED_BY_TEST=0`
- `COOKIE_CLEARS=0`
- `PROFILE_DELETES=0`
- `BULK_VERIFICATION_RUNS=0`

No credential/Cookie/Token/API key/private-key value is recorded in this evidence.

## Root cause and final design

The recent Chat convergence had accumulated a second, long-lived platform-verification lifecycle around the existing Upstream ChatNew owner. It added verification state/task dictionaries, a 300-second verification lifecycle, start/status/cancel routes, frontend polling/spinners, and a raw challenge-oriented interaction. Separately, the recent `FAIL_SYS_USER_VALIDATE` handling had regressed from Upstream semantics by returning PVR before invoking the existing CAPTCHA delegation.

The final source restores the Upstream Chat business sequence while retaining only XIANYU governance that is still required:

`chat_{myid}` cache -> Token API -> token-expired self-heal -> optional existing remote Token fallback -> existing CAPTCHA delegation -> bounded Token retry -> IM connect/register -> conversations -> truthful READY.

Retained XIANYU governance:

- live-client READY truth
- per-account single-flight
- bounded connect timeout
- disabled-account isolation
- strict read-only diagnostics
- structured status/reason reporting

Removed recent verification complexity:

- long-lived verification challenge/session/task/lock owner
- 300-second verification monitor lifecycle
- `/platform-verification/{account_id}/start`
- `/platform-verification/{account_id}` status endpoint
- `/platform-verification/{account_id}/cancel`
- frontend 3-second verification polling
- permanent verification spinner/cancel wait UI
- raw challenge/deep-link interaction
- verification lifecycle fields from the Chat business capability contract
- Accounts/ChatNew interactive `去验证` action

PVR remains a truthful terminal business state for the current Connect attempt. UI text now explains that automatic platform verification did not complete and the user should retry later or follow the platform's current requirement. PVR is not converted to QR.

## Upstream Token/CAPTCHA semantic equivalence

`backend-web/app/services/chat_new/im_client.py` was compared against Upstream `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72` at the behavior/hunk level.

Confirmed final semantics:

- Chat Token cache remains separate under `chat_{myid}`.
- Valid cache is used before Token API.
- Ordinary expired Token response can merge the existing allowed response-Cookie subset and retry through the existing Token owner.
- `FAIL_SYS_USER_VALIDATE` / equivalent CAPTCHA-required response calls the existing `_solve_captcha_via_websocket(result)` instead of failing before delegation.
- `CAPTCHA_MAX_RETRY=1`.
- If the WebSocket CAPTCHA path reports a newly saved Chat Token cache, the Chat client re-reads and uses that cache.
- Otherwise the old Chat Token cache is marked expired and Token API is retried once.
- CAPTCHA failure or retry-limit exhaustion returns structured `CHAT_PLATFORM_VERIFICATION_REQUIRED` and stops; no background Chat verification lifecycle is started.
- Existing remote Token fallback remains optional and does not create a QR or second CAPTCHA owner.

## Complexity delta

Comparison scope: eight production Chat/Account runtime/frontend files, comparing the preserved pre-cleanup worktree with final source.

- `CHAT_LINES_REMOVED_APPROX=922`
- `CHAT_LINES_ADDED_APPROX=47`
- `CHAT_NET_COMPLEXITY_DELTA=NEGATIVE`
- verification endpoints removed: 3
- frontend verification polling loops removed: 1
- backend long-lived verification monitor/task lifecycle removed: 1

The added lines are primarily the restored Upstream CAPTCHA delegation/retry branch and truthful static PVR presentation; the large net deletion is the recent verification lifecycle cleanup.

## Focused automated verification

Authoritative final source worktree:

`D:\xianyu-chg0018-chat-final-v2`

Focused CHG-0018 suite after final cleanup:

- `220 passed in 22.13s`

The focused suite includes direct behavioral tests proving:

- CAPTCHA-required Token result invokes the existing delegate exactly once when delegation fails.
- CAPTCHA success retries Token at most once.
- CAPTCHA success can reuse the WebSocket-written `chat_{myid}` cache without a second Token API call.
- retry-limit prevents a second CAPTCHA generation.
- no long-lived verification task/route/frontend poll remains.
- READY truth, per-account single-flight, bounded timeout, disabled isolation, consumer readiness, Session/Item behavior, and PID-reaper regressions remain covered.

Additional local verification:

- `python -m compileall -q backend-web common websocket scheduler` -> PASS
- Frontend `npm --prefix frontend run build` -> PASS
- source `git diff --check` -> PASS

The raw vendor-tree `pytest -q` is not the governance repository test command and encounters an unrelated collection-order/import-shadowing issue in the reconstructed vendor baseline; the required focused suite and the Root governance verification are authoritative for this change.

## Fresh cumulative Vendor Patch

Final cumulative Patch:

`vendor/patches/xianyu-auto-reply/64c245-chg0018-chat-upstream-golden-path-cleanup.patch`

- base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- file count: 42
- bytes: 468898
- SHA256: `CE55EF6D329DBB4FF982830E27F079C5AF3D3C990569BA6E6B3C3A137F955346`

Independent fresh applycheck worktree:

`D:\xianyu-chg0018-chat-final-applycheck`

Results:

- `PATCH_CLEAN_APPLY_CHECK=PASS`
- `PATCH_APPLY=PASS`
- `COMPARE_FILE_COUNT=42`
- `MISSING=0`
- `EXACT_BYTE_DIFF_COUNT=1`
- `CONTENT_DIFF_IGNORING_CRLF=0`
- `CONTENT_EQUIVALENCE=PASS`
- focused tests after Fresh Apply: `220 passed in 22.14s`

The single exact-byte difference is CRLF-only; semantic/file content comparison ignoring line endings is identical.

Root staged `git diff --cached --check` reports trailing whitespace only inside the immutable cumulative `.patch` artifact because the patch text faithfully contains historical vendor source lines with trailing whitespace. The final source worktree itself passed `git diff --check`; the cumulative patch is not normalized after its SHA256, clean-apply, actual-apply, and content-equivalence evidence is locked.

## Production Golden Path Canary

Exactly one normal Chat Connect was used for the production Golden Path gate before final cleanup deployment. No second Chat Canary was run afterward.

Canary account: `2214313339860` (production alias: 丸子).

Observed result:

- one Chat Connect business action
- total Connect duration about 14.91 seconds
- final stage: `CAPTCHA_DELEGATION`
- existing CAPTCHA delegation duration about 13.414 seconds
- Backend called the existing `/internal/captcha/solve`
- engine: existing Playwright/browser route
- DrissionPage fallback: disabled by current production configuration
- remote CAPTCHA: not configured
- the existing browser engine attempted its bounded internal trajectories and the platform Baxia control rejected them
- Chat CAPTCHA generation count: 1
- Chat Connect count: 1
- internal CAPTCHA solve count: 1
- background Chat retry after final result: 0
- final Chat result: structured `CHAT_PLATFORM_VERIFICATION_REQUIRED`
- Chat connected: false
- false READY: not observed
- QR conversion: not observed

Therefore the Git gate is satisfied by the second accepted condition: the full intended Upstream Token -> existing CAPTCHA delegation chain executed in production; the remaining failure is a real platform Baxia boundary, not a local pre-delegation regression or XIANYU verification-lifecycle dead end.

## Production regression checks

Before/following the Canary and final deployment:

- Auto Reply remained independent from Chat Browser Session/PVR behavior.
- final WebSocket connection statistics: `CONNECTED=6`
- no Auto Reply Token-refresh storm was induced by the Chat acceptance action.
- Publish read-only preflight for the Canary exposed the existing `HUMAN_QR_REQUIRED` platform boundary; no QR scan and no publish followed.
- normal Item list total remained 17 in the validated production state.
- disabled-account historical items remained stored/read-only synchronized but leaked 0 rows into normal visibility in the validated sample.
- disabled manual item fetch remained `ACCOUNT_DISABLED`.
- WebSocket PID1/reaper protection remained active; prior final resource check showed PIDS=3, zombie=0, Chromium=0, Playwright driver=0 after completion.
- Scheduler single-instance invariant remained 1.

## Stale verification metadata convergence

After removing the verification lifecycle, production account metadata was checked read-only for stale `session_maintenance.consumers.chat.verification_active=true` records.

- `STALE_VERIFICATION_ACTIVE_COUNT_BEFORE=0`
- `STALE_VERIFICATION_ACTIVE_CONVERGED=0`

No DB metadata write was needed for this step.

## Final production deployment

Only Backend and Frontend were replaced for the final cleanup. Existing environment/volumes/ports/network were preserved without recording secret values. Stopped rollback containers were retained.

Current images:

- Backend: `xianyu-chg0018-backend-web:chat-upstream-golden-path-cleanup-20260815-r2`
- Frontend: `xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2`
- WebSocket unchanged: `xianyu-chg0018-websocket:recent-regression-cleanup-20260815-r1`
- Scheduler unchanged: `xianyu-chg0018-scheduler:upstream-verification-20260815-r1`

Unchanged service container IDs across final deployment:

- WebSocket: `0f912f554c45`
- Scheduler: `66dbc7e23895`

Post-deployment health:

- `FRONTEND_HEALTH=200`
- `BACKEND_HEALTH=200`
- `WEBSOCKET_HEALTH=200`
- `SCHEDULER_HEALTH=200`

Production artifact checks:

- ChatNew bundle contains no platform-verification API marker, `verify_account`, `去验证`, verification cancel-wait, or Chat verification spinner.
- Accounts bundle contains no `verify_account`, `去验证`, `verification_active`, or verification `human_action` marker.
- Backend Chat route/session manager contains no long-lived platform-verification endpoints/tasks/deadline lifecycle.
- production `im_client.py` contains the restored `_solve_captcha_via_websocket(result)` call.

Rollback containers retained:

- `xianyu_chg0017_backend_web_pre_chat_cleanup_20260815`
- `xianyu_chg0017_frontend_pre_chat_cleanup_20260815`

## Root governance verification

Executed from `D:\xianyu` after the new cumulative Patch was present:

`python scripts/verify_repository.py`

Result:

- collected: 595
- `595 passed, 1 warning`
- repository structure: PASS
- active change validation: PASS
- capability registry: PASS
- JSON schemas: PASS
- OpenAPI contract: PASS
- duplicate capability detection: PASS
- security scan: PASS
- unit and acceptance tests: PASS
- tracked project state validation: PASS
- `repository verification passed`

## Git delivery gate

The source/production gate is satisfied because the complete intended Upstream Chat Token/CAPTCHA delegation path was exercised and the remaining Canary failure is the platform Baxia boundary. The final cumulative Patch is Fresh Apply verified and content-equivalent. This evidence and the cumulative Patch are the only Root files intended for this run's commit; the five historical Root dirty files remain pre-existing and must not be staged.
