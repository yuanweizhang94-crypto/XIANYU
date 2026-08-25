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
- SHA256: `B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111`
- T12 patch builder: isolated disposable worktree; production upstream checkout was not modified.
- Patch parse check: passed with `git apply --numstat --unidiff-zero`.
- Patch strict clean-apply check: passed with `git apply --check --whitespace=error-all --unidiff-zero`.
- Applied source Git-blob equivalence: 27/27 PASS.
- Final CHG-0018 targeted tests: 38 passed with the CHG-0018 credential, Profile/publish-readiness, auto-polish safety, and T11 batch-readiness coverage.
- CHG-0017 regression tests: 58 passed.
- Combined CHG-0017 regression and CHG-0018 targeted tests: 96 passed.
- Full repository tests before final production enablement historically passed 595/595; the current main-based T12 exact final repository validation passed 588/588 and is recorded in the T12 evidence.
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

## CHG-0018 T11 controlled batch publish recovery supplement

- Historical apply base: pre-T12 formal CHG-0018 Patch SHA256 `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`.
- The current T12 formal `4c5e1ac-chg0018-account-profile-publish-safety.patch` already contains this supplement; do not apply the supplement a second time after the current formal Patch.
- Patch file: `4c5e1ac-chg0018-t11-controlled-batch-publish-recovery.patch`
- SHA256: `99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882`
- Changed upstream files: 4
  - `backend-web/app/services/publish_execution_service.py`
  - `backend-web/app/services/xianyu_publisher.py`
  - `tests/test_chg0017_publish_login_submit.py`
  - `tests/test_chg0018_profile_publish_readiness.py`
- The supplement keeps the existing backend Publisher as the sole execution owner, forwards the owner from the database-loaded account row, preserves one persistent Profile context per concrete publish attempt, and adds no service, queue, Profile store, Token system, login system, browser broker, or table.
- Readiness keeps the 60-second maximum wait and classifies `verification_required`, `page_load_timeout`, and `page_structure_mismatch`; legacy `publish_form_not_rendered`, `publish_form_timeout`, `publish_page_load_failed`, and `manual_verification_required` inputs are normalized for compatibility.
- The batch method contains one `publisher.publish_item()` call site and no automatic publish retry loop.
- Clean apply check: PASS on the exact CHG-0017 -> CHG-0018 Git-blob preimage.
- Applied source Git-blob equivalence: 4/4 PASS.
- CHG-0018 targeted suites: 38/38 PASS.
- CHG-0017 regression suites: 58/58 PASS.
- `validate_change.py`: PASS; repository verification: 596/596 PASS with worktree-local module resolution.
- Controlled duplicate check found all four owner-authorized historical failures already formally published and present in the current account catalog, so T11 correctly performed zero new real publish attempts and no production container replacement.

## CHG-0018 T12 formal integration Patch

- T11 historical supplemental SHA256 remains locked at `99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882`.
- T12 regenerated the single formal CHG-0018 Patch from the exact archived CHG-0017 target blobs, the prior CHG-0018 target blobs, and the locked T11 supplement. No hunk was hand-spliced.
- Final formal SHA256: `B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111`.
- Patch parse: PASS; strict clean apply: PASS; applied `git diff --check`: PASS; source Git-blob equivalence: 27/27 PASS.
- A temporary candidate generated with `--ignore-space-at-eol` was discarded before commit because it reconstructed only 13/27 exact target blobs. A second exact text candidate reached 27/27 but was also discarded because historical whitespace-bearing patch lines caused the outer XIANYU repository `git diff --check` to fail.
- The final Patch is generated entirely by Git from the same staged target. In the disposable builder only, `.git/info/attributes` marks the 27 upstream target paths `-diff`, so `git diff --binary --full-index` emits 27 `GIT binary patch` records. That builder-only attribute file is not tracked or delivered. The result preserves 27/27 exact target blobs and does not change business behavior relative to the prior formal Patch followed by the T11 supplement.
- Git binary patch syntax requires a terminating blank separator line. This vendor directory therefore tracks a `.gitattributes` entry that marks only the current formal CHG-0018 Patch as `binary`, allowing the outer XIANYU repository `git diff --check` to treat the generated artifact as opaque data without changing its bytes.
- T12 does not change frontend source or deploy any production runtime.

## CHG-0019 main integration after CHG-0018 T12

Current formal upstream layering for `main` is:

1. `4c5e1ac-chg0017-reply-identity-allowlist.patch` — canonical SHA256 `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`.
2. `4c5e1ac-chg0018-account-profile-publish-safety.patch` — T12 SHA256 `B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111`; this already contains the locked T11 supplement and the supplement must not be applied again.
3. `4c5e1ac-chg0019-main-integration-after-chg0018-t12.patch` — SHA256 `A0A07EA2EC4BC0046CBA39DA478EC9E530E1FBD10A9EEE23F3311D1A38677392`.

The CHG-0019 main-integration Patch is a Git-generated incremental layer from the exact current T12 target to the reviewed CHG-0019 hardened target. Its three-way base is the historical pre-T12 CHG-0018 target (`94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD`); OURS is that base plus the locked T11 supplement, and THEIRS is that base plus the historical CHG-0019 formal-delivery and PR #28 hardening layers. Git completed the merge cleanly, including the overlapping `backend-web/app/services/xianyu_publisher.py`, with no manual business-conflict resolution.

Validation for the current layer: Patch parse PASS, strict clean apply PASS, applied `git diff --check` PASS, and final source Git-tree equivalence PASS. The exact replay chain `PINNED -> CHG-0017 -> CHG-0018 T12 -> CHG-0019 main-integration` reproduces the merged target. CHG-0019 targeted tests pass 47/47, CHG-0018/T11 targeted regressions pass 38/38, CHG-0017 regressions pass 58/58, frontend offline UI tests pass 27/27, frontend lint passes, and frontend build passes. No new real canary or production deployment is part of this integration.

Historical CHG-0019 artifacts are retained for audit and are **HISTORICAL / SUPERSEDED_FOR_CURRENT_MAIN_LAYERING**:

- `4c5e1ac-chg0019-normal-account-offline-backend-verified.patch` — historical canonical SHA256 `1CF41E1889872CE0030B5FBA58301C4FE3FE9E11C8C2437E146527B4075D3FB9`.
- `4c5e1ac-chg0019-normal-account-offline-formal-delivery.patch` — historical canonical SHA256 `410308F81A2484C469694E8790E9C9C689DEDAEF5C73AB0D67DD3518D557C3CF`.
- `4c5e1ac-chg0019-pr28-review-success-classification-hardening.patch` — historical canonical SHA256 `B4F9673CF486EC57FF235BAF97182066703FE6D2E4EE7910A3828AC769A1C912`.

These historical files are not deleted or rewritten. They remain evidence of the originally reviewed CHG-0019 delivery; the new main-integration Patch is the only current CHG-0019 layer applied after the B379 T12 CHG-0018 Patch.

## CHG-0028 selected-account on-demand publish capability patch

- Runtime preimage source: read-only extraction from `xianyu-chg0027-backend-web:session-transient-classification-20260824-r1`.
- Patch file: `chg0028-selected-account-on-demand-capability.patch`
- SHA256: `CED451293701C53475E23F9B87DF205AB97AFDD0B3696D35A4D9C8675BC4E490`
- Patch builder: `D:/xianyu-worktrees/_chg0028_patch_builder_runtime`; production runtime was not modified.
- Patch parse check: passed with `git apply --numstat --unidiff-zero`.
- Patch clean-apply check: passed against a clean committed runtime preimage copy with `git apply --check --whitespace=error-all --unidiff-zero`.
- Patch-included deterministic tests: 11/11 passed with `python -m pytest tests/test_chg0028_selected_account_on_demand_capability.py -q`.
- Changed upstream/runtime files:
  - `backend-web/app/api/routes/_exports.py`
  - `backend-web/app/api/routes/cookies.py`
  - `backend-web/app/api/routes/product_publish_capability.py`
  - `tests/test_chg0028_selected_account_on_demand_capability.py`

This patch implements the owner-approved CHG-0028 `SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY` contract. It registers the selected-account route `/product-publish/accounts/{account_id}/capability`, which uses the existing `detect_publish_account_capability` helper and current account Cookie for an explicit on-demand check. The Accounts/global overview no longer represents an unprobed Publisher capability as a stuck persisted readiness defect; it returns `state=NOT_CHECKED`, `mode=ON_DEMAND`, and `checked=false`.

The patch-included behavior tests use dependency stubs and `AsyncMock` to assert the selected-account route calls the existing helper exactly once with the current account Cookie, returns `READY` only on current success, classifies transient failures as retryable `RETRY_LATER`, classifies account-invalid failures as non-retryable `ACCOUNT_INVALID`, and performs no session/database writes. The helper is the existing thin loader in `common/services/xianyu_publish_service.py`, which dispatches to `PublishAccountCapabilityService.detect`; CHG-0028 does not introduce a replacement capability service.

The patch does not create a lineage-aware writer, persistent `consumers.publish` producer, readiness table, scheduler/background probe, Browser gate, COMPANY-side truth source, or second Publisher owner. It does not call MTop from account-list polling and does not perform real publish, item mutation, QR/login, reconnect, Browser, Item Sync, message, account-state, container, or production configuration actions.

## CHG-0030 controlled Fresh Item Sync canary patch

- Runtime preimage source: disposable full runtime-source baseline from `D:/xianyu-chg0026-source` with the CHG-0028 runtime patch applied over the current CHG-0024/CHG-0027/CHG-0028/CHG-0029 stack.
- Clean apply base: `8c2723e552bb9f797c73b6c497858bc314549877`.
- Patch file: `chg0030-fresh-item-sync-controlled-canary.patch`
- SHA256: `595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201`
- Patch builder: `D:/xianyu-worktrees/_chg0030_full_runtime_base_tmp`; production runtime was not modified.
- Patch replay: `D:/xianyu-worktrees/_chg0030_patch_replay2_tmp`; strict clean-apply check passed with `git apply --check --whitespace=error-all --unidiff-zero`.
- Patch-included deterministic tests plus CHG-0028 runtime regression: 15/15 passed with `python -m pytest tests/test_chg0028_selected_account_on_demand_capability.py tests/test_chg0030_fresh_item_sync_controlled_canary.py -q`.
- Changed upstream/runtime files:
  - `common/schemas/item.py`
  - `backend-web/app/api/routes/cookies.py`
  - `backend-web/app/api/routes/items.py`
  - `tests/test_chg0030_fresh_item_sync_controlled_canary.py`

This patch keeps `ItemService.fetch_all_items_from_account` as the only Fresh Item Sync business owner. The selected-account route still performs exactly one owner call. After the owner returns, the route performs read-only `xy_catalog_items` queries scoped to the selected account, measures duplicate groups under the runtime `uk_cat_account_item (account_id, item_id)` durable key contract, reconciles response item IDs, and fails closed to terminal `UNKNOWN` with `retry_allowed=false` if readback is unavailable or unreconciled.

The patch adds sanitized backend log events `CHG0030_ITEM_SYNC_OPERATION_ACCEPTED`, `CHG0030_ITEM_SYNC_TERMINAL_READBACK`, and `CHG0030_ITEM_SYNC_PREFLIGHT_STATUS` so the first canary invocation identity and terminal durable-readback result remain recoverable from container logs even when the current COMPANY adapter strips extension response fields.

The account-status capability returns explicit selected-account Item Sync eligibility only when disabled state, cookie presence, checking state, platform-verification result, session-cookie lineage, and token readiness are authoritative and passing. Unknown facts fail closed. The patch does not add auth recovery, retry, queue/status ledger, DB truth model, scheduler, worker, browser/CDP/UI path, Item Sync owner, publish/edit/offline/delete path, message path, account mutation, or production deployment.

## CHG-0030 skipped-lock success guard follow-up patch

- Applies after: `chg0030-fresh-item-sync-controlled-canary.patch`
- Clean apply base: `8c2723e552bb9f797c73b6c497858bc314549877` plus locked CHG-0030 r1 patch `595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201`
- Patch file: `chg0030-fresh-item-sync-skipped-lock-success-guard.patch`
- SHA256: `1FC5597EEC8FB0060EBA6551D4F98407649EB0FA0675BDC4CA5574D0362B9DC6`
- Patch builder: `D:/xianyu-worktrees/_chg0030_r1_followup_builder_tmp`; production runtime was not modified.
- Patch replay: `D:/xianyu-worktrees/_chg0030_two_patch_replay_20260825111651`; strict clean-apply check passed with `git apply --check --whitespace=error-all --unidiff-zero` for r1 and this follow-up in order.
- Patch-included deterministic tests plus CHG-0028 runtime regression: 17/17 passed with `python -m pytest tests/test_chg0030_fresh_item_sync_controlled_canary.py tests/test_chg0028_selected_account_on_demand_capability.py -q`.
- Changed upstream/runtime files:
  - `backend-web/app/api/routes/cookies.py`
  - `backend-web/app/api/routes/items.py`
  - `tests/test_chg0030_fresh_item_sync_controlled_canary.py`

This follow-up does not alter the locked r1 patch. It treats an owner lock result with `skipped=true` as terminal `UNKNOWN`, sets `success=false`, keeps `retry_allowed=false`, records `OWNER_LOCK_OCCUPIED_SKIPPED`, and prevents `durable_readback.checked=true` or `reconciled=true` for that path. It also requires `full_active_list_confirmed=true` for Fresh Item Sync `SUCCESS`; a capped or otherwise incomplete owner result fails closed as `FULL_ACTIVE_LIST_NOT_CONFIRMED`.

The follow-up preserves `ItemService.fetch_all_items_from_account` as the only Fresh Item Sync owner, preserves the Redis lock behavior, performs no second invocation, and adds no queue, ledger, table, worker, scheduler, browser path, account mutation, publish/edit/offline/delete path, or message path. It also exposes sanitized `platform_verification_evidence_type` in selected-account Item Sync preflight facts and logs so `source=none` is observable as authoritative only when the classifier supplies an evidence type and `required=false`.

## Artifact Format

Historical text artifacts use Git-generated zero-context unified diffs. The T12 current formal CHG-0018 Patch uses Git-generated binary patch records for exact source preservation.

Historical zero-context generation command:

```text
git diff --cached --binary --full-index --no-ext-diff
--unified=0 --ignore-space-at-eol --src-prefix=a/ --dst-prefix=b/ HEAD
```

T12 current formal generation command uses the same staged target and `--binary --full-index`; the disposable builder marks only its target paths `-diff` in local `.git/info/attributes` before running `git diff`. No repository `.gitattributes` change is introduced.

Reason:

The pinned historical source includes whitespace-only blob differences. Ignoring those differences breaks exact blob equivalence, while emitting them as ordinary text makes the outer repository patch artifact fail `git diff --check`. Git binary patch records preserve the exact blobs without either problem.

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
