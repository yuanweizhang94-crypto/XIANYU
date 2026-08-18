# Xianyu upstream patch artifacts

## CHG-0016 manual-only verification patch

- Base upstream repository: `zhinianboke/xianyu-auto-reply`
- Base pinned SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Patch file: `bda1a85-manual-only-verification.patch`
- Patch SHA256: `E5791692B69D95157A2249EF6B4C04F71A65C8513412B1A87C70EFF03D117FFE`
- Local patch worktree: `D:/xianyu-upstream-manual-chg0016`
- Patch apply check: `git apply --check --whitespace=error-all --unidiff-zero <patch-file>`

## CHG-0017 reply identity allowlist, catalog fallback, and Gemini content patch

- Base upstream repository: `zhinianboke/xianyu-auto-reply`
- Base pinned SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`
- Patch file: `4c5e1ac-chg0017-reply-identity-allowlist.patch`
- Canonical SHA256: `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`
- Raw Windows SHA256: `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`
- EOL state: LF, no BOM
- Local patch worktree: `D:/xianyu-upstream-delivery-chg0017`
- Patch apply check: passed with `git apply --check --whitespace=error-all --unidiff-zero`
- Targeted tests: passed with
  `python -m pytest tests/test_chg0017_publish_login_submit.py tests/test_chg0017_reply_allowlist.py tests/test_chg0017_ai_prompt_validation.py tests/test_chg0017_gemini_response_parser.py -q`
- Changed files:
  - `backend-web/app/services/ai_reply_service.py`
  - `backend-web/app/services/xianyu_publisher.py`
  - `common/services/ai_provider_service.py`
  - `common/services/publish_execution_service.py`
  - `common/utils/item_info_manager.py`
  - `frontend/src/pages/accounts/Accounts.tsx`
  - `tests/test_chg0017_ai_prompt_validation.py`
  - `tests/test_chg0017_gemini_response_parser.py`
  - `tests/test_chg0017_publish_login_submit.py`
  - `tests/test_chg0017_reply_allowlist.py`
  - `websocket/app/services/xianyu/ai_reply_engine.py`
  - `websocket/app/services/xianyu/auto_reply_service.py`

This patch adds a default-off fail-closed CHG-0017 test gate for automatic
reply validation. The receiver is matched by the current automatic-reply
`cookie_id` account identifier, while the sender is matched by the inbound
platform sender identity. It rejects missing, unknown, system, non-whitelist,
wrong-receiver, and own-message inputs before keyword, AI, default-reply, or
sender execution.

For production multi-account operation, the same gate supports `*` in the
receiver and sender allowlist environment values. This removes the CHG-0017
runtime dependency on hardcoded validation accounts while preserving the
existing empty, unknown, system, wrong-receiver, non-whitelist, and own-message
rejections when explicit allowlists are configured.

The patch also reclassifies a local item catalog miss as `item_catalog_missing`
instead of proof that the item does not belong to the account. When local
catalog data is absent, item-scoped keyword/default/image side-effect paths are
not eligible, while approved account-level text keyword and Gemini routing may
continue after the allowlist gate.

The item-list sync utility no longer logs full request headers, Cookie, signed
params, request data, data value, full response body, account ID, or user ID.
It logs only structured diagnostic counts and classifications.

The Gemini patch adds one shared `generateContent` parser for provider tests
and formal AI replies. It ignores `thought=true` parts, merges all final text
parts in order, checks `finishReason`, rejects truncated output, retries at
most once with a higher output limit, requests plain text with the verified
low thinking configuration, and rejects obvious non-customer-facing fragments
such as internal template fields, JSON-like output, Markdown wrappers, and
English-dominant replies before sender use.

The account-level custom prompt setting is now validated as a JSON object in
both the native backend service and the account UI before saving. Product-level
AI prompts remain normal plain text and are not parsed as JSON.

The product publish patch preserves the verified native publish path while
repairing the official quick-enter login handoff, runtime Chromium user agent,
publish text sanitization, publish button readiness checks, POST/PUT publish
request diagnostics, and explicit failure classification. Publish diagnostics
are masked and do not record Cookie, Token, full URLs, account IDs, item IDs, or
customer content.

The artifact contains no runtime account identifiers, platform identifiers,
Cookie, Token, Gemini key, item IDs, chat IDs, customer messages, or runtime
HMAC values.

## CHG-0018 account credential safety patch

- Base upstream repository: `zhinianboke/xianyu-auto-reply`
- Base pinned SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`
- Applies after: `4c5e1ac-chg0017-reply-identity-allowlist.patch`
- Patch file: `4c5e1ac-chg0018-account-profile-publish-safety.patch`
- SHA256: `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`
- Local patch worktree: `D:/xianyu-upstream-delivery-chg0017`
- Patch parse check: passed with `git apply --numstat --unidiff-zero`
- Patch staged-base apply check: passed with `git apply --check --cached --whitespace=error-all --unidiff-zero`
- Final CHG-0018 targeted tests: 36 passed with the CHG-0018 credential, Profile/publish-readiness, and auto-polish safety suites.
- CHG-0017 regression tests: 58 passed.
- Combined CHG-0017 regression and CHG-0018 targeted tests: 94 passed.
- Full repository tests before final production enablement: 595/595 passed.
- Frontend build: passed with `npm --prefix frontend run build`
- Frontend lint note: `npm run lint` exists, but the upstream frontend checkout has no ESLint config file; recorded as a non-blocking upstream tooling gap.
- Changed files:
  - `backend-web/app/api/routes/cookies.py`
  - `backend-web/app/services/account_service.py`
  - `backend-web/app/services/ai_reply_service.py`
  - `backend-web/app/services/publish_execution_service.py`
  - `backend-web/app/services/xianyu_publisher.py`
  - `common/schemas/account.py`
  - `common/services/cookie_renew_browser_service.py`
  - `common/services/item_service.py`
  - `common/services/publish_execution_service.py`
  - `common/services/xianyu_publish_service.py`
  - `common/utils/item_info_manager.py`
  - `docker-compose.yml`
  - `frontend/src/api/accounts.ts`
  - `frontend/src/pages/accounts/Accounts.tsx`
  - `frontend/src/pages/items/Items.tsx`
  - `frontend/src/pages/polishLogs/PolishBatchDetail.tsx`
  - `frontend/src/types/index.ts`
  - `scheduler/app/services/scheduler/day_switch_task.py`
  - `scheduler/app/services/scheduler/polish_task.py`
  - `tests/test_chg0017_publish_login_submit.py`
  - `tests/test_chg0018_auto_polish_safety.py`
  - `tests/test_chg0018_credential_safety.py`
  - `tests/test_chg0018_profile_publish_readiness.py`
  - `websocket/app/api/routes/internal.py`
  - `websocket/app/services/xianyu/ai_reply_engine.py`
  - `websocket/app/services/xianyu/auto_reply_service.py`
  - `websocket/app/services/xianyu/cookie_token_manager.py`

The patch removes raw `login_password` from ordinary account detail responses,
adds explicit password-clear intent, keeps saved passwords out of the default
account edit form, and prevents `no_credentials` or `bad_credentials` password
refresh failures from disabling an account. Touched refresh logs report Cookie
field counts instead of full Cookie values.

The patch also routes publish execution through authoritative account identity,
loads the latest Cookie inside the existing publisher path, opens the account's
persistent Profile, runs shared read-only preflight before any publish form
mutation in the same context, and reuses the existing captcha concurrency
managers for one browser slot and one account lock.

The auto-polish path now treats only the explicit `SUCCESS::调用成功` response as
confirmed API success. Duplicate responses remain `duplicate_unverified`,
session and token failures remain non-success, unknown responses fail closed,
and only confirmed API success can set `is_polished=true`. Existing polish log
fields store a structured, non-sensitive summary containing `api_code`,
`api_message`, `result_status`, and `attempted_at`. The item and polish-log UI
no longer presents local state as platform readback confirmation.

Controlled execution also supports optional exact `platform_item_ids` scope and
default-compatible `retry_on_token_expiry`. Item-list Token/Cookie rotation is
persisted through the existing account-Cookie merge path so a later polish does
not reload stale Token fields. For explicit Session/Token expiry,
`PolishTaskService` permits at most one existing auth recovery followed by one
final polish retry; no third polish request or unbounded auth-recovery loop is
allowed.

Final production verification used account `2219319284219` with four exact item
IDs. All four returned explicit `SUCCESS::调用成功` on one request each and moved
from local `is_polished=false` to `true`, with zero auth failures, zero unknown
failures, zero other-account requests, and zero out-of-scope requests. The final
production Scheduler is `xianyu-chg0018-scheduler:56d62e2-94c8682`. Global
polish was subsequently re-enabled through the existing scheduled-task
management path while `day_switch` remained enabled; one natural cycle completed
with bounded Session failure handling and Scheduler restart count zero.

## Artifact Format

Git-generated zero-context unified diff.

Generation command:

```text
git diff --cached --binary --full-index --no-ext-diff
--unified=0 --ignore-space-at-eol --src-prefix=a/ --dst-prefix=b/ HEAD
```

Reason:

The pinned upstream source contains unchanged whitespace-bearing context lines.
Including those lines in a vendor patch causes repository whitespace checks to
inspect upstream baseline formatting rather than the recorded target change
itself.

Safety:

- patch hunks are never hand-edited;
- the patch applies only with `--unidiff-zero`;
- clean pinned-SHA apply check is mandatory;
- `--whitespace=error-all` is mandatory;
- applied-source `git diff --check` is mandatory;
- Git blob equivalence must cover every recorded target file;
- exact target file set must match the `Changed files` list for the patch.

## Artifact Generation

Generated from the staged Git diff in a disposable worktree at the pinned
upstream SHA. Patch hunks must not be hand-edited.

## Parseability gate

`git apply --numstat --unidiff-zero <patch>`

## Clean apply gate

`git apply --check --whitespace=error-all --unidiff-zero <patch>`

## Equivalence gate

The staged Git blob IDs after clean application must match the staged Git blob
IDs used to generate the patch for every recorded target file.

## Working-tree note

Raw byte hashes may differ on Windows only because text=auto can expand LF and
CRLF differently. Such a difference is acceptable only when:

- canonical CRLF-to-LF comparison is 12/12;
- BOM and trailing-newline state match;
- no lone CR exists;
- staged Git blob comparison is 12/12.

## Modified upstream files

- `common/services/captcha/manual_verification.py`
- `common/services/captcha/orchestrator.py`
- `websocket/app/core/config.py`
- `websocket/app/services/xianyu/cookie_token_manager.py`
- `tests/test_manual_verification.py`

## Runtime Boundary

The patch adds a default-off `CAPTCHA_MANUAL_ONLY` mode to the upstream captcha
orchestrator. When enabled it opens a visible local browser for the project
owner to complete the official verification page. It does not move the mouse,
type, click, drag, inject trajectories, call remote captcha services, create an
IM implementation, create a Token implementation, create a WebSocket
implementation, create a sender, or create a second automatic-reply executor.

The patch returns only the exact `x5sec` Cookie field for manual verification
and uses upstream `merge_account_cookie_fields` for the automatic-reply Token
path. It does not persist verification URLs, print Cookie values, print Token
values, or alter online chat and automatic-reply Token cache ownership.

## Single-shot and no-auto-retry boundary

The manual listener must run with `AUTO_START_WEBSOCKET=false` and expose only
health/internal control APIs until the project owner explicitly starts a
controlled manual validation. A host websocket process lifetime may open at
most one manual browser. After success, failure, timeout, cancellation, or
unknown redirect, later manual verification calls are consumed and must not open
another browser. If the native Token API still returns platform verification
after the one manual success retry, the patched upstream sets
`manual_verification_not_accepted` and remains disconnected.

## Live defect and fix

Observed live defect marker:
`MANUAL_VERIFICATION_REPEATED_BROWSER_LAUNCH`.

Root causes fixed in this patch:

- `AUTO_START_WEBSOCKET_NOT_DISABLED`
- `EXISTING_X5_COOKIE_FALSE_SUCCESS`
- `MANUAL_BROWSER_NOT_SINGLE_SHOT`
- `MANUAL_LISTENER_LOGS_DISCARDED`

The repaired patch uses a visible isolated temporary browser profile, exact
`x5sec` delta validation, strict `https://h5api.m.goofish.com` URL validation,
single-shot process state, local ignored listener logs, and one native Token
retry after owner-completed manual verification.

## Rollback

Stop the host manual listener, keep Docker websocket stopped, restore the
previous patch artifact from Git, and run the repository validation scripts
before any further live validation. Default replies remain disabled pending
project-owner decision.

## CHG-0018 Auto Reply Session safety follow-up

- Reconstructed base: `64c245b`
- Applies after: `64c245-chg0018-auto-reply-stability-consolidation.patch`
- Patch file: `64c245-chg0018-auto-reply-session-safety-followup.patch`
- SHA256: `8B6BD8F8B4A6DBF44CCC03CD140FC597DD911C11CD501201C80BBE967A5E7991`
- Patch size: 15514 bytes
- Clean apply check: `git apply --check --whitespace=error-all --unidiff-zero` PASS
- Clean post-apply targeted tests: 47/47 PASS

This follow-up closes the 2026-08-12 Auto Reply regression without creating a
second Token, Session, WebSocket, or reply engine. Expected Session lifecycle
states (`no_credentials`, `failed_session_expired`, human QR, and platform
verification) no longer accumulate toward the generic automatic-disable
threshold. Standalone missing/bad credential refresh failures also preserve the
account enabled state, matching CHG-0018 acceptance.

The existing WebSocket status owner now exposes sanitized Token readiness, and
the Backend no longer treats heartbeat connectivity alone as proof that Auto
Reply is ONLINE. ONLINE requires both a connected WebSocket and a current Token;
Session/QR/platform-verification states remain explicit and fail closed.

Runtime and patch evidence:
`changes/active/CHG-0018-account-profile-publish-safety/evidence/20260818-auto-reply-session-safety-repair.md`.

## CHG-0018 Order fetch recovery follow-up

- Reconstructed base: `64c245b`
- Applies after: `64c245-chg0018-auto-reply-stability-consolidation.patch`
- Patch file: `64c245-chg0018-order-fetch-recovery.patch`
- SHA256: `8FC6B31FAE1398AC3A8F67D6C20D986FF506654D0DC9E3EC89837FAA44850F6A`
- Patch size: 3989 bytes
- Clean apply check: `git apply --check --whitespace=error-all --unidiff-zero` PASS
- Clean post-apply targeted tests: 3/3 PASS

This follow-up restores the native order Scheduler path after an operational
regression disabled `fetch_orders`, `fetch_pending_orders`, and
`fetch_refund_orders` and a local Auto Reply patch caused stale PVR metadata to
block order synchronization. The order tasks again use upstream-native Session
cooldown only, and API error results are no longer counted as successful
zero-order fetches.

The three existing order tasks are re-enabled at their prior 600/60/120-second
intervals. No second order crawler, order model, API, queue, worker, or
scheduler executor is added. Current platform `SESSION_EXPIRED` / permission
responses remain explicit account-session blockers rather than being hidden as
local success.

Runtime and patch evidence:
`changes/active/CHG-0018-account-profile-publish-safety/evidence/20260818-order-fetch-recovery.md`.
