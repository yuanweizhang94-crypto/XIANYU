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
- SHA256: `8FA58C8F2674EE7A16C36689F962612DC1619C211ACAA390105778A64CD20EEE`
- Local patch worktree: `D:/xianyu-upstream-delivery-chg0017`
- Patch parse check: passed with `git apply --numstat --unidiff-zero`
- Patch staged-base apply check: passed with `git apply --check --cached --whitespace=error-all --unidiff-zero`
- Targeted tests: passed with `python -m pytest tests/test_chg0018_credential_safety.py -q`
- Frontend build: passed with `npm run build`
- Changed files:
  - `backend-web/app/api/routes/cookies.py`
  - `backend-web/app/services/account_service.py`
  - `backend-web/app/services/xianyu_publisher.py`
  - `common/schemas/account.py`
  - `common/services/publish_execution_service.py`
  - `common/services/xianyu_publish_service.py`
  - `frontend/src/api/accounts.ts`
  - `frontend/src/pages/accounts/Accounts.tsx`
  - `frontend/src/types/index.ts`
  - `websocket/app/api/routes/internal.py`
  - `websocket/app/services/xianyu/cookie_token_manager.py`
  - `tests/test_chg0018_credential_safety.py`
  - `tests/test_chg0018_profile_publish_readiness.py`

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
