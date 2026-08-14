# CHG-0018 Chat PLATFORM_VERIFICATION_REQUIRED Official Verification Convergence

Date: 2026-08-14

Status: production verification complete without a natural platform-verification sample.

## Execution contract

User outcome: When normal Chat authentication returns `FAIL_SYS_USER_VALIDATE`, expose one account-level **去验证** action that sends the user to the official platform challenge, lets the user personally complete the required verification, and then automatically resumes the existing Chat Token / IM-client / conversation-list flow without requiring another Connect click or QR scan.

Confirmed blocker: The existing Chat client correctly classified `FAIL_SYS_USER_VALIDATE` as `PLATFORM_VERIFICATION_REQUIRED`, but the Chat business route stopped there. The official challenge URL returned by the platform was not retained for a user-visible Chat action, and there was no bounded user-completed verification lifecycle that resumed the existing Chat connection afterward.

Smallest success test: A synthetic/integration `PLATFORM_VERIFICATION_REQUIRED` sample must expose only an official HTTPS challenge URL, accept only one active verification flow per account, never invoke the existing automatic slider/human-trail solver, automatically retry the existing `ImSessionManager.get_or_connect()` path after user verification, confirm the conversation list read-only, and converge Chat to `READY`; all prior CHG-0018 Chat/QR/Session/Publish/PID tests must remain green.

## Baseline

- Repository: `D:\xianyu`
- Branch: `feat/CHG-0018-account-profile-publish-safety`
- GitHub/local baseline before this task: `a706ebc6b9ec93c6b1ae6c13befa771f5585a3ef`
- Active Change: `CHG-0018-account-profile-publish-safety`
- Upstream current main rechecked through GitHub SSH over 443: `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`
- Pinned cumulative patch base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- `docs/AI_PROJECT_HANDOFF.md` was not present.

The five historical root dirty files were preserved and were not reset, restored, cleaned, stashed, or staged by this task.

## Upstream-first review

### Current upstream capability

The current upstream already provides the required primitive owners:

- `common/services/captcha/token_response.py`
  - `extract_token_captcha_url()` parses the official challenge URL from a Token response.
  - existing Token response helpers distinguish captcha/platform-verification responses from Token expiry.
- `backend-web/app/services/chat_new/im_client.py`
  - the formal Chat Token owner continues to call the upstream Chat Token endpoint.
  - Chat keeps its independent IM Token and independent `device_id` architecture.
- `backend-web/app/services/chat_new/im_session_manager.py`
  - remains the sole Chat IM-client manager and the existing `get_or_connect()` owner.
- `backend-web/app/api/routes/chat_new.py`
  - remains the Chat HTTP surface.
- `frontend/src/api/chatNew.ts` and `frontend/src/pages/chat-new/ChatNew.tsx`
  - remain the formal Chat frontend path.
- Existing frontend authentication code already demonstrates the safe product pattern of opening an official verification URL in a new browser tab with `noopener,noreferrer` and waiting for an internal backend status.
- Existing human-verification session handling provides a 300-second bounded human-interaction envelope. This task reuses that duration only; it does **not** reuse QR-login semantics.

### Upstream gap

`UPSTREAM_VERIFICATION_FIX_AVAILABLE=false` at upstream main `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`.

No upstream ChatNew-specific flow was found that combines:

1. `PLATFORM_VERIFICATION_REQUIRED` Chat state;
2. a user-visible official challenge URL;
3. one account-level user verification action;
4. bounded status monitoring;
5. automatic retry of the existing Chat Token/IM client;
6. read-only conversation-list confirmation;
7. final Chat/Account `READY` convergence.

Reuse decision: `PATCH_UPSTREAM` with a thin orchestration layer around existing owners. No new verification engine, Chat stack, Session system, Profile manager, scheduler, worker, queue, or table was added.

## Safety boundary: automated solver explicitly excluded

The upstream WebSocket service contains `/internal/captcha/solve`, which is an automatic captcha/slider solving path and may involve browser automation / human-trail style processing. This task does **not** invoke, extend, or depend on that route.

Formal verification mode:

`PLATFORM_VERIFICATION_MODE=USER_COMPLETED_OFFICIAL_FLOW`

The system is responsible only for:

- parsing the official challenge URL already returned by the platform;
- exposing one **去验证** action;
- opening the official HTTPS page for the user;
- recording a bounded sanitized lifecycle;
- polling only XIANYU Backend state;
- detecting success by retrying the existing Chat authentication path;
- resuming the existing Chat client and reading the conversation list.

The user is responsible for completing whatever human verification the official Xianyu/Taobao page requires.

The task does not:

- solve CAPTCHA automatically;
- replay a human trail;
- synthesize or inject a verification result;
- forge a Token;
- turn `PLATFORM_VERIFICATION_REQUIRED` into QR login;
- delete or replace the canonical persistent Profile.

## Current platform verification flow

### Before this repair

`Chat connect -> Chat Token obtain -> mtop.taobao.idlemessage.pc.login.token -> FAIL_SYS_USER_VALIDATE -> PLATFORM_VERIFICATION_REQUIRED -> structured Chat failure`

The Chat state classification was correct, but the user only saw that platform verification was required. The official challenge URL was not exposed through the Chat product flow and no automatic Chat resume occurred after a user-completed official verification.

`CURRENT_VERIFICATION_GAP=OFFICIAL_CHALLENGE_NOT_EXPOSED_TO_CHAT_USER_AND_NO_BOUNDED_AUTO_RESUME`

### After this repair

`WAITING_CONNECT`

-> normal user Chat selection

-> existing `ImSessionManager.get_or_connect()`

-> existing Chat Token obtain

-> if `FAIL_SYS_USER_VALIDATE`: existing parser extracts official challenge URL

-> Chat remains `PLATFORM_VERIFICATION_REQUIRED`

-> Account and Chat UI show one **去验证** action

-> POST `/api/v1/chat-new/platform-verification/{account_id}/start`

-> validate account enabled + current Chat verification state + official HTTPS host

-> invalidate only the existing stale Chat client/token cache

-> return the official platform verification URL to the authorized user

-> frontend opens the official page in a new tab

-> user personally completes the platform-required verification

-> frontend polls only GET `/api/v1/chat-new/platform-verification/{account_id}` every 3 seconds

-> existing manager performs bounded retry of the existing `get_or_connect()` path

-> if Token/IM succeeds, read `get_conversations(limit=20)` only

-> `VERIFICATION_SUCCEEDED`

-> Chat `READY`

-> Account and Chat account lists refresh automatically

-> conversation list refreshes automatically

No message is sent.

## Verification owner and lifecycle

`PLATFORM_VERIFICATION_OWNER=ImSessionManager + existing Chat Token response parser + existing Chat get_or_connect`

The challenge URL is held only in short-lived Backend process memory. It is never persisted to account metadata, logs, Evidence, or Git.

Sanitized lifecycle fields are stored under the existing `session_maintenance.consumers.chat` metadata authority:

- `verification_state`
- `verification_active`
- `verification_started_at`
- `verification_deadline_at`
- `verification_source`
- `verification_reason`

No new database table exists.

Lifecycle states used by the orchestration:

- `NONE`
- `VERIFICATION_WAITING_USER`
- `VERIFICATION_IN_PROGRESS`
- `VERIFICATION_SUCCEEDED`
- `VERIFICATION_FAILED`
- `VERIFICATION_EXPIRED`
- `VERIFICATION_CANCELLED`

Final Chat readiness remains the existing authority:

- `READY`
- `WAITING_CONNECT`
- `TEMPORARY_FAILURE`
- `LOGIN_REQUIRED`
- `PLATFORM_VERIFICATION_REQUIRED`

### Deadline

`PLATFORM_VERIFICATION_DEADLINE_SECONDS=300`

`PLATFORM_VERIFICATION_DEADLINE_SOURCE=existing_human_verification_session_300s`

The 300-second duration reuses the project's existing bounded human-verification session envelope. It is not a QR-login classification.

Both the Chat reconnect and conversation-list read are wrapped by the remaining verification budget so one slow attempt cannot run indefinitely beyond the user-verification lifecycle.

### Single-flight and isolation

- `MAX_PLATFORM_VERIFICATION_PER_ACCOUNT=1`
- A second start for the same account returns the current active session as `VERIFICATION_ALREADY_ACTIVE` rather than starting another flow.
- Verification locks are per account.
- The existing Chat manager global network lock is not reintroduced.
- Account A verification does not hold an unrelated account's Chat connection lock.
- No scheduler-driven or batch verification trigger was added.

### Disabled and unrelated states

- Disabled account start fails closed as `ACCOUNT_DISABLED` before verification owner execution.
- `WAITING_CONNECT` keeps normal lazy Chat connect.
- `RATE_LIMITED` does not show or start platform verification.
- `TEMPORARY_FAILURE` does not show or start platform verification.
- `LOGIN_REQUIRED` does not show the platform-verification action.
- `READY` does not show the platform-verification action.

`PLATFORM_VERIFICATION_REQUIRED != HUMAN_QR_REQUIRED` remains enforced.

Only an authoritative `HUMAN_QR_REQUIRED` result may lead to QR-login guidance.

## Token / Cookie behavior

On a user-started verification lifecycle, XIANYU invalidates only the existing Chat token cache and disconnects a stale Chat client if present, then re-reads the authoritative DB Cookie through the existing Chat path.

If a legitimate existing Token/Cookie owner later receives an official Cookie update, the normal existing Cookie owner/convergence path remains authoritative. This task adds no direct Cookie writer.

The platform verification URL is not persisted and no Cookie or Token value is logged.

`COOKIE_WRITE_BY_PLATFORM_VERIFICATION_FLOW=false` in this production run because no natural verification sample existed and no real verification flow was started.

## Account GET and strict diagnostic

The Account page continues to obtain Chat state through `read_only_diagnostic()`.

Account GET does not:

- start verification;
- call `get_or_connect()`;
- renew a Token;
- write a Cookie;
- open a browser.

Post-deployment immediate before/after Cookie hash snapshots around all six enabled-account verification-status + strict-Chat diagnostic reads were identical:

- `ACCOUNT_COOKIE_WRITE_BY_STATUS_READ=false`
- `STRICT_CHAT_DIAGNOSTIC_COOKIE_WRITE=false`

## Frontend behavior

### Chat page

For a `PLATFORM_VERIFICATION_REQUIRED` account:

- selecting the account does not blindly POST another `/connect`;
- the row displays `需平台验证`;
- one **去验证** action is displayed;
- when active it displays `验证中...` and disables another start;
- the explanatory copy explicitly states this is not a QR re-login;
- **取消等待** cancels only XIANYU's monitoring task;
- one action is protected by a frontend in-flight set and a terminal-toast dedupe set;
- the frontend polls XIANYU Backend every 3 seconds and never polls Xianyu/Taobao directly;
- success automatically refreshes Chat accounts, selects the account, establishes the frontend WebSocket subscription, and reloads conversations.

### Account page

When `business_capabilities.chat.state == PLATFORM_VERIFICATION_REQUIRED`:

- the Chat badge remains `需平台验证`;
- tooltip context records platform verification as the required human action;
- one **去验证** action routes to the same Chat verification flow;
- active verification displays `验证中`.

Other Chat states do not display the platform-verification action.

## Test evidence

### Python compile

Changed Backend files compile successfully.

`PYTHON_COMPILE=PASS`

### Frontend build

`npm --prefix frontend run build`

Result: PASS (`tsc && vite build`). Existing dependency-age and existing chunking warnings remain non-blocking and were not changed by this task.

`FRONTEND_BUILD=PASS`

### Existing CHG-0018 regressions

The existing current CHG-0018 Chat/consumer/status/isolation/PID suite remained green.

### New platform-verification tests

`tests/test_chg0018_chat_platform_verification_convergence.py` covers:

- `FAIL_SYS_USER_VALIDATE -> PLATFORM_VERIFICATION_REQUIRED`;
- platform verification does not become QR;
- rate limit / temporary failure do not trigger verification;
- `WAITING_CONNECT` retains lazy connect;
- official URL allowlist accepts only approved HTTPS platform hosts;
- 300-second existing-owner deadline;
- same-account verification single-flight;
- disabled account fail-closed;
- only platform-required state may start;
- stale/missing in-memory challenge can be reacquired only through the existing user-initiated Chat auth path;
- success automatically retries Chat Token/client and reads conversations;
- the already-recovered race still performs read-only conversation confirmation before declaring success;
- another `PLATFORM_VERIFICATION_REQUIRED` remains platform verification, never QR;
- network failure maps to `TEMPORARY_FAILURE`;
- cancel clears active state/task;
- verification status read is non-authenticating;
- challenge URL is not persisted;
- no automatic captcha solver/human-trail dependency exists in the new flow;
- persistent Profile is not deleted;
- Account GET and strict Chat diagnostic remain read-only;
- thin start/status/cancel routes exist;
- frontend **去验证**, polling, auto refresh, and Toast dedupe semantics;
- Account page uses one unified action;
- no new scheduler/table/profile system.

Combined targeted result after the final adjustment:

`TARGETED_TESTS=238 passed`

### Patch clean apply

Cumulative patch:

`vendor/patches/xianyu-auto-reply/64c245-chg0018-chat-platform-verification-convergence.patch`

Base:

`64c245bc85ac56e34339fa056b0e291a16a3843b`

SHA256:

`A91A485DB324E1E3407BA42105E59B660FA4C6E2BF96050E7B1267F451B6A2E5`

- Patch files: 42
- `git apply --check`: PASS on a fresh managed worktree at the exact base SHA.
- Patch apply: PASS.
- Targeted tests on the clean-applied worktree: `238 passed`.
- Candidate vs clean-applied content comparison: 42/42 files present, zero normalized-content differences.
- `PATCH_BYTE_EQUIVALENCE=CRLF_DIFF_ONLY`
- `CONTENT_EQUIVALENCE_IGNORING_CRLF=PASS`

## Production deployment

### Natural sample decision

Immediately before implementation/deployment, six enabled production accounts were read-only inspected. None had a current stored natural `PLATFORM_VERIFICATION_REQUIRED` / `CHAT_PLATFORM_VERIFICATION_REQUIRED` state.

`NATURAL_PLATFORM_VERIFICATION_SAMPLE_FOUND=false`

Per task boundary, no failure was manufactured and no real account was forced through Chat Token risk control. Therefore no human verification action was requested from the project owner in this run.

Production acceptance uses unit/integration lifecycle coverage plus live no-side-effect API/UI/runtime checks.

### Images deployed

Only changed services were deployed:

- Backend: `xianyu-chg0018-backend-web:chat-platform-verification-20260814-r2`
- Frontend: `xianyu-chg0018-frontend:chat-platform-verification-20260814-r1`

WebSocket, Scheduler, MySQL, and Redis code/images were not changed by this task.

A first Compose override attempt failed before replacement because the local `.env` file was inaccessible to that invocation. The deployment script immediately restored the prior Backend/Frontend and did not modify file permissions or read the `.env` contents. Deployment was then completed by cloning the already-running containers' effective configuration internally while changing only the image; secret values were not printed or persisted in Evidence.

### Live API/UI checks

- Frontend `/health`: HTTP 200
- Backend `/health`: HTTP 200
- WebSocket `/health`: HTTP 200
- Scheduler `/health`: HTTP 200
- WebSocket initialization: true
- Live Backend OpenAPI contains all three thin Chat platform-verification routes.
- Live Frontend bundle contains the **去验证**, **验证中...**, official-verification explanation, Backend polling, and Account deep-link flow.

### Production no-side-effect checks

After deployment:

- six enabled accounts remained without a natural platform-verification sample;
- effective read-only Chat state after Backend restart was `WAITING_CONNECT`, not false `READY` and not QR-required;
- `verification_active_count=0`;
- no real verification start API was invoked;
- message count remained 41;
- auto-reply message-log count remained 532;
- publish-log count remained 216;
- no message-send or publish endpoint was called by this acceptance.

Cross-time Cookie fingerprints may legitimately rotate while the existing WebSocket/Session owners run, so cross-minute equality is not used as a side-effect assertion. The authoritative side-effect check is the immediate before/after snapshot around status/diagnostic reads, which was unchanged.

### Runtime process/resource checks

- `ACTIVE_SCHEDULER_EXECUTORS=1` (scheduler PID 1 only; the inspection command itself was excluded from matching).
- WebSocket PID 1 remains `docker-init`.
- `ZOMBIES=0`.
- Process inspection excluding the inspection command itself found no Chromium or Playwright driver at idle.
- `CHROMIUM_PROCESS_COUNT_IDLE=0`.
- `PLAYWRIGHT_DRIVER_IDLE=0`.
- No persistent Profile was deleted.

## Side effects

- `REAL_MESSAGES_SENT=0`
- `REAL_PRODUCTS_PUBLISHED=0`
- `REAL_PRODUCTS_RELISTED=0`
- `REAL_PRODUCTS_OFFLINED_BY_TEST=0`
- `QR_SCANS_TRIGGERED_BY_TEST=0`
- `ACCOUNT_COOKIE_WRITE_BY_STATUS_READ=false`
- `STRICT_CHAT_DIAGNOSTIC_COOKIE_WRITE=false`
- `MYSQL_SCHEMA_CHANGED=false`
- No scheduler task added.
- No second Chat system added.
- No second Session system added.
- No second verification engine added.
- No new Profile manager added.

## Regression invariants preserved

- `SINGLE_QR_CONSUMER_CONVERGENCE_PRESERVED=true`
- `CHAT_REAL_USABILITY_CONVERGENCE_PRESERVED=true`
- `CHAT_PER_ACCOUNT_SINGLE_FLIGHT_PRESERVED=true`
- `TRANSIENT_STATUS_CONVERGENCE_PRESERVED=true`
- `AUTO_REPLY_RECOVERY_PRESERVED=true`
- `PUBLISH_READINESS_PRESERVED=true`
- `DISABLED_BUSINESS_ISOLATION_PRESERVED=true`
- `PID_REAPER_PRESERVED=true`
- `BACKEND_RESTART_DOES_NOT_REQUIRE_QR=true`
- `CHAT_CLIENT_DISCONNECT_DOES_NOT_REQUIRE_QR=true`
- `TOKEN_STALE_DOES_NOT_REQUIRE_QR=true`
- `COOKIE_ROTATION_DOES_NOT_REQUIRE_QR=true`
- `PLATFORM_VERIFICATION_DOES_NOT_REQUIRE_QR=true`
- `ONLY_HUMAN_QR_REQUIRED_REQUIRES_QR=true`

## Files represented by this task

Runtime-source changes are persisted through the cumulative vendor patch. The new source/test delta includes:

- `backend-web/app/api/routes/chat_new.py`
- `backend-web/app/api/routes/cookies.py`
- `backend-web/app/services/chat_new/im_client.py`
- `backend-web/app/services/chat_new/im_session_manager.py`
- `frontend/src/api/chatNew.ts`
- `frontend/src/pages/accounts/Accounts.tsx`
- `frontend/src/pages/chat-new/ChatNew.tsx`
- `frontend/src/types/index.ts`
- `tests/test_chg0018_chat_platform_verification_convergence.py`

The formal root commit for this task stages only this sanitized Evidence and the cumulative vendor patch. Historical dirty governance/runtime artifacts remain untouched.
