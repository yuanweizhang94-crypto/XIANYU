Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: ARCHIVED
# Tasks

- [x] T1 Create proposal.
- [x] T2 Create design.
- [x] T3 Audit latest upstream.
- [x] T4 Record threat model.
- [x] T5 Define acceptance criteria.
- [x] T6 Record project-owner implementation approval.
- [x] T7 Create latest upstream candidate worktree.
- [x] T8 Validate upstream native Token and account connection.
- [x] T9 Validate upstream native WebSocket and sender.
- [x] T10 Configure keyword, AI, and failure fallback.
- [x] T11 Run no-send integration tests.
- [x] T12 Run controlled automatic reply test between two owner-owned accounts.
- [x] T13 Validate restart, reconnect, duplicate protection, and one-click stop.
- [x] T14 Generate redacted delivery report.
- [x] T15 Wait for OWNER GO_LIVE.
- [x] T16 Enable production and observe.
- [x] T17 Archive and deliver.

## Current Progress

Completed tasks: 17 / 17
Next task: null

## Execution Contract

User outcome: Make the existing upstream project's native automatic reply and AI reply usable as soon as safely possible, without continuing local slider research or building a second reply system.
Confirmed blocker: CHG-0016 live manual handoff was not accepted by the platform, while latest upstream contains newer Token and risk-control paths that must be evaluated before delivery.
Smallest success test: Configure and validate only the upstream-native account, Token, WebSocket, keyword/default/AI reply, sender, log, and stop paths with zero non-whitelist sends, then stop at `READY_FOR_GO_LIVE` until owner authorization.

## Current Evidence

- CHG-0016 blocked closeout PR #25 merged by normal merge commit `3da7f6d5f03f692e4f34f2139ecb5d997a2a8195`.
- Main push CI for `3da7f6d5f03f692e4f34f2139ecb5d997a2a8195` completed successfully for quality, tests, and security.
- Latest upstream candidate SHA is `4c5e1ac5f532c7313365d70409ae115305de8a55`.
- Candidate worktree path is `D:/xianyu-upstream-delivery-chg0017`.
- Reuse decision is `CONFIGURE_UPSTREAM`.

## Always Prohibited

- Starting CHG-0010 worker.
- Building or enabling a local sender.
- Building a second Token, WebSocket, IM, AI, keyword, default, or automatic reply implementation.
- Sending messages outside the `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B` whitelist.
- Sending more than 8 automatic test replies during this Change.
- Triggering image send, order, refund, shipping, rating, listing mutation, scan login, relogin, Cookie clearing, or Token clearing.
- Automating platform verification by click, drag, OCR, screenshot analysis, DrissionPage, Selenium, Playwright login automation, real_mouse, or remote solver.
- Printing Cookie, Token, API key, Device ID, UNB, full account ID, full chat/session/item ID, customer message content, or platform verification URL.

## Completed Offline Gate

- Candidate worktree remains clean and detached at the latest audited SHA.
- Upstream has no `test_*.py` or `*_test.py` tests in the candidate tree.
- `git diff --check` passes in the candidate tree.
- `D:/xianyu/.venv/Scripts/python.exe -m compileall -q common websocket backend-web scheduler` passes in the candidate tree.
- No runtime service is started during T3/T7.

## T8 Entry Gate

- Pilot configuration backup metadata exists in ignored `.local`.
- Zero-risk baseline exists in ignored `.local`.
- CHG-0010 is stopped.
- Host manual-listener is stopped.
- Old websocket is stopped.
- Scheduler is stopped.
- No project-owned verification browser is running.
- Active keyword rules are `0`.
- Default reply records are `0`.
- Message filters enabled are `0`.
- Autoreply logs total is `0`.
- AI assistant messages total is `0`.
- AI enabled metadata count is `0`.

## T8 Blocker

Run `CHG17-DELIVERY-20260731T043547Z-H8SE` established the zero-risk baseline
and local backup. The owner then identified `ACCOUNT-A` and
`OWNER_TEST_ACCOUNT_B`; both local ignored aliases resolve to exactly one
database account each and refer to different accounts.

An isolated latest-upstream candidate runtime was then started with separate
containers and ports. Empty service observation stayed quiet. A single
upstream-native `ACCOUNT-A` start request was accepted, but the account task
remained disconnected and the sanitized Token/risk-control evidence reported
`FAIL_SYS_USER_VALIDATE` plus punish/x5sec validation signals before any
WebSocket connection signal appeared.

Verdict: `PLATFORM_VERIFICATION_REQUIRED`

`ACCOUNT-A` was stopped once, the isolated candidate runtime was stopped, all
candidate ports closed, and a 120 second quiet period completed with zero
autoreply, AI, or send deltas. T8 remains unchecked.

After the owner replied `OWNER_LOGIN_COMPLETED`, the gate was rechecked and a
single additional upstream-native `ACCOUNT-A` start was executed. The task again
remained disconnected, no Token was obtained, and platform verification signals
reappeared. `ACCOUNT-A` and the candidate websocket were stopped, followed by a
120 second quiet period with zero autoreply, AI, or send deltas.

Verdict: `PLATFORM_VERIFICATION_STILL_REQUIRED`

Later owner-authorized live work established that the previous T8 runtime
blocker was no longer the current state: remote Token real request passed,
Token was obtained, `device_id` was obtained, ACCOUNT-A entered native
WebSocket `connected` state, a stable observation completed, browser launches
remained `0`, and T8 sends remained `0`.

T8 is therefore complete. T9 and later tasks remain unchecked until the
upstream-native sender, reply routing, cleanup, and reconnect evidence is
completed.

## T9 Blocker

Run `CHG17-CATALOG-DIRECTION-LIVE-20260731T095918Z-W9IU` recorded the
standardized conclusion from the previous skipped-row audit:

`TEST_MESSAGE_DIRECTION_MISMATCH_AND_ITEM_CATALOG_MISS`

The audit showed one sender identity matching `EXPECTED_B_PLATFORM`, proving
the OWNER_TEST_ACCOUNT_B platform identity mapping is valid. The other four
skipped rows matched `EXPECTED_A_PLATFORM` and are treated as ACCOUNT-A
self-message echoes, not as B identity mapping failures. The single B inbound
record was blocked by `item_not_belong`.

The candidate item catalog sync then returned success with `0` returned items,
`0` saved items, and `0` ACCOUNT-A catalog rows. No TEST_ITEM could be selected
and `check_item_belongs_to_account(ACCOUNT-A, TEST_ITEM)` could not be proven.

Verdict: `LOCAL_ITEM_CATALOG_MISS`

No websocket account task was started during this catalog-direction run, no
test message was sent, and the candidate management runtime was stopped with
ports closed.

This conclusion was later reclassified because upstream
`check_item_belongs_to_account()` only checks local `xy_catalog_items`, not
platform ownership. A local catalog miss must not block account-level keyword
or Gemini AI routing. It must only make item-scoped keyword/default/image/card,
delivery, order, rating, and item-mutation paths ineligible.

## T9 Catalog Fallback Patch

Run `CHG17-CATALOG-FALLBACK-OFFLINE-20260731T102708Z` confirmed:

- Cookie identity and stored UNB matched without printing either value.
- The upstream item-list API returned HTTP 200 and API success.
- The response had no `cardList`, no non-empty alternative item arrays, and
  zero parsed/saved catalog rows.
- Diagnosis: `ITEM_API_RETURNED_EMPTY`.
- Sensitive item-sync logging was patched to remove raw headers, Cookie,
  signed params, request data, data value, response body, account ID, and user
  ID output.
- Automatic reply routing was patched so `item_catalog_missing=true` disables
  only item-scoped paths while approved account-level keyword and Gemini routes
  remain eligible after the CHG-0017 allowlist gate.
- Candidate local tests passed: `18`.
- Patch artifact SHA256:
  `4918E56416B2B0B1993801265BA09D876EACAEED73903A4E4FE44C68240C959A`.

T9/T10/T11 remain unchecked until controlled live validation proves the native
sender, keyword, Gemini, cleanup, and reconnect behavior with zero
non-whitelist sends.

## READY_FOR_GO_LIVE Boundary

The Change stopped at `READY_FOR_GO_LIVE` after controlled validation.
Production enablement then received the exact owner text:

`GO_LIVE ACCOUNT-A`

## T9-T16 Delivery Evidence

Run `CHG17-GO-LIVE-20260731T1431Z` completed the remaining controlled
validation and production enablement on the existing CHG-0017 branch and
Draft PR #26 without creating a new Change, branch, PR, sender, Token client,
WebSocket runtime, or AI provider.

- Upstream-native websocket service: healthy.
- ACCOUNT-A native task: running and connected.
- OWNER_TEST_ACCOUNT_B official IM send path: connected and used for test
  inbound messages.
- Gemini provider settings: `provider_type=gemini`,
  `base_url=https://generativelanguage.googleapis.com`,
  `model_name=gemini-3.6-flash`, API key present and redacted.
- Zero-send provider test: passed with sender invocation `0` and platform
  send `0`.
- Context test: passed, `context_used=true`, one AI reply success.
- Duplicate test: passed, two official B messages produced one successful
  reply and one duplicate skip.
- Stop test: passed, ACCOUNT-A stopped, one official B message produced zero
  autoreply and zero AI deltas, then ACCOUNT-A recovered.
- Reconnect test: passed, ACCOUNT-A reconnected and one AI reply succeeded.
- Rollback drill: passed, AI was temporarily disabled and ACCOUNT-A/websocket
  stopped with zero deltas, then restored to production running state.
- Final production state: ACCOUNT-A running, websocket connected, AI enabled.
- Active keyword rules: `0`; enabled default replies: `0`; enabled filters:
  `0`.
- Non-whitelist successful reply sends: `0`.
- PR #26 remains Draft, Open, and Unmerged as required.

T17 remains unchecked because final archive/merge was not authorized in this
run. The operational delivery state is `DELIVERY_READY`.

## Laptop Source Sync Evidence

Run `CHG17-LAPTOP-SOURCE-SYNC-20260805T035232Z` records the source
synchronization from the production laptop into existing Draft PR #26.

- Production containers were inspected only and were not stopped, restarted,
  rebuilt, or recreated.
- No account task, scheduler, CHG-0010 worker, platform verification, product
  publish, AI provider call, or message send was triggered during the sync.
- Local branch was fast-forwarded to remote PR head
  `2c1058fd5c0a9f1a572b578faf913df16e2cbd2b` before applying laptop source
  artifacts.
- Vendor patch artifact was regenerated from the candidate upstream staged
  diff at pinned base `4c5e1ac5f532c7313365d70409ae115305de8a55`.
- Patch SHA256 is
  `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`.
- Patch target count is `12`; clean apply, applied diff check, and staged blob
  equivalence passed `12/12`.
- Targeted offline tests passed: `58`.
- Only masked Markdown evidence is eligible for Git; raw screenshots, raw JSON
  browser summaries, logs, Cookie, Token, API keys, full account IDs, full item
  IDs, chat IDs, and customer messages remain excluded.
- PR #26 remains Draft, Open, and Unmerged.
- T17 remains unchecked because archive and merge are not authorized.

## Native UI Delivery Evidence

Run `CHG17-NATIVE-UI-20260731T150428Z` resolved the owner-facing native UI
runtime mismatch without modifying upstream business code. The URL
`http://127.0.0.1:19000` had been served by the old Pilot frontend, whose
same-origin nginx proxy resolved `backend-web:8089` on the Pilot network. The
already-working CHG-0017 production chain was running in the separate candidate
backend, MySQL, Redis, and WebSocket containers.

The old Pilot frontend was stopped, the upstream-built CHG-0017 candidate
frontend was started on `127.0.0.1:19000`, and the frontend was attached to the
candidate Docker network. The local runtime compose file remains under
gitignored `.local/`.

Validated owner-facing upstream-native pages and controls:

- Account management shows ACCOUNT-A enabled and online from the candidate
  WebSocket state.
- Online chat connects ACCOUNT-A through the upstream native `chat-new` IM
  session manager and loads sessions without sending a message.
- System settings shows backend service and message service online.
- AI settings modal exposes the upstream native AI switch, provider, base URL,
  API key, model, prompt, test, and save controls.
- Keyword management and automatic reply log pages open through the candidate
  frontend/backend pair.

PR #26 remains Draft, Open, and Unmerged. T17 remains unchecked because archive
and final merge are still outside the current authorization.

## Native Multi-Account Delivery Evidence

Run `CHG17-MULTI-ACCOUNT-20260731T160511Z` verified the upstream-native
multi-account automatic-reply runtime without creating a second manager,
sender, Token flow, WebSocket runtime, AI worker, or frontend page.

Findings and changes:

- ACCOUNT-B was logged in and enabled, but its automatic-reply account task had
  not been started. Cookie existence was not treated as WebSocket connection.
- Upstream `CookieManager` already supports loading enabled accounts and
  starting one task per account through the native start/status/stop APIs.
- The candidate compose was corrected locally to `AUTO_START_WEBSOCKET=true`
  so service restart restores all enabled accounts from the candidate DB.
- The CHG-0017 reply gate patch was minimally corrected to support `*` in
  receiver and sender allowlist values. Explicit allowlists still fail closed,
  and empty, unknown, system, and own-message inputs remain rejected.
- ACCOUNT-A and ACCOUNT-B both recovered to `running` and `connected` after
  service restart.
- Single-account stop/start isolation passed in both directions: stopping one
  account did not stop the other.
- The account management page showed both rows enabled and online from the
  candidate runtime.
- The online chat page exposed both accounts as online without sending a
  message.
- ACCOUNT-A remains production-running with Gemini AI enabled.
- ACCOUNT-B remains AI-disabled / not configured and produced zero successful
  sends.

Runtime verdict: `MULTI_ACCOUNT_NATIVE_READY`.

## Gemini Content Quality Blocker

Run `CHG17-GEMINI-CONTENT-20260801T044125Z` repaired the confirmed Gemini
content-quality defects without creating a new Provider, sender, Token flow,
WebSocket runtime, or AI worker.

- Shared Gemini response parser now ignores thought parts, merges all final
  text parts, checks `finishReason`, and rejects truncated output.
- Formal AI replies and Provider tests use the same parser and output quality
  gate.
- Gemini requests use verified plain text response mode, low thinking
  configuration, lower customer-service temperature, and one bounded retry.
- Account-level custom prompts are validated as JSON objects in the native
  backend service and account UI; product-level AI prompts remain plain text.
- Zero-send Provider regression passed four buyer-question classes with sender
  invocation `0` and platform sends `0`.
- The affected account AI remains disabled because the upstream-native item
  sync returned success with `0` parsed/saved catalog items for that account.

T17 remains unchecked. CHG-0017 cannot be archived as content-ready until the
affected account has an account-scoped catalog item and the live AI reply test
can prove product-aware Simplified Chinese output with zero duplicate or
non-whitelist sends.

## Account Catalog Alignment and AI Content Ready Evidence

Run `CHG17-ACCOUNT-CATALOG-ALIGNMENT-20260801T055428Z` reclassified the prior
catalog blocker as an account identity mismatch rather than an item-sync code
defect.

- ACCOUNT-AI held the Gemini configuration, while ACCOUNT-CATALOG held the
  visible product catalog row.
- ACCOUNT-CATALOG's native WebSocket task was already running and connected.
- Gemini settings were applied to ACCOUNT-CATALOG through upstream-native
  `AIReplySettingsService.update_settings`; catalog ownership was not copied or
  modified.
- Catalog gate passed with an account-scoped product row, price, description,
  and product AI prompt.
- Zero-send product-context Provider regression passed four buyer-question
  classes with sender invocation `0` and platform sends `0`.
- Controlled live test used one owner-controlled buyer message and produced one
  successful AI reply for ACCOUNT-CATALOG.
- Live reply was Simplified Chinese, complete by the quality gate, and had no
  template, Markdown, JSON, duplicate, non-whitelist, or proactive-customer
  send leak.

Runtime verdict: `AI_REPLY_CONTENT_READY`.

T17 remains unchecked until separate archive/closeout authorization is given.

## Final Delivery Report Without Archive

Run `CHG17-FINAL-DELIVERY-20260801T060801Z` generated the requested final
delivery report while keeping PR #26 Draft, Open, and Unmerged.

- Upstream reuse: account tasks, IM Token, WebSocket, reply decisioning, Gemini
  Provider call, sender, logs, account settings, online chat, and management UI
  remain upstream-native.
- Added fix points: receiver/sender allowlist hardening, catalog-miss
  account-level fallback, redacted item-sync diagnostics, Gemini parser and
  reply quality gate, and ACCOUNT-CATALOG Gemini settings alignment through
  upstream `AIReplySettingsService.update_settings`.
- AI chain: Gemini on `https://generativelanguage.googleapis.com` with
  `gemini-3.6-flash`, API key present only as redacted evidence, valid JSON
  account custom prompts, and plain-text product AI prompt.
- Product context: catalog row, title, price, description/detail, and product
  AI prompt are present for the effective production AI account.
- Account mapping: prior item-catalog blocker is reclassified as
  `AFFECTED_ACCOUNT_IDENTITY_MISMATCH`; ACCOUNT-CATALOG is now the effective
  production AI account without changing product ownership.
- Tests: targeted acceptance passed, change validation passed, repository
  verification passed, and PR #26 quality/tests/security CI passed at exact
  HEAD `60c330c31edddc28eae6bb6e1e7748b64a96289a`.
- Current boundary: ACCOUNT-CATALOG task running, WebSocket connected, AI
  enabled, active keyword rules `0`, enabled default replies `0`, PR #26 still
  Draft/Open/Unmerged.
- Rollback: disable ACCOUNT-CATALOG AI through upstream-native settings, stop
  that account task, and confirm no new successful reply sends after stop.

Delivery report verdict: `CHG0017_DELIVERY_REPORT_READY`.

T17 remains unchecked because the owner explicitly did not authorize archive or
merge in this run.

## PR #26 Final Governance Authorization

On 2026-08-08 the project owner explicitly authorized CHG-0017 governance
closeout, exact-head validation, normal push, PR #26 Ready transition after
green CI, normal merge, and post-merge T17/archive synchronization.

Pre-merge boundary:

- Change status is `VERIFYING`.
- Completed tasks remain `16 / 17`.
- T17 remains unchecked until PR #26 is actually merged.
- No runtime, account, message, product, login, Docker, database, Redis, CHG-0018
  T11/T12, PR #28, or CHG-0019 business-code action is authorized by this
  governance closeout.
- Archive is post-merge only for this successful delivery path.

OWNER_CLOSEOUT_AND_MERGE_AUTHORIZATION_RECORDED=true
PR_READY_AUTHORIZED_AFTER_GREEN_CI=true
T17_POST_MERGE_ONLY=true

## Post-merge T17 closeout

PR #26 merged successfully on 2026-08-08 as merge commit
`6b2c233c6176620ca38fd7bab84366f57d6034f6`. The exact pre-merge head
`f2752244561bd3eadb3ff930ecd3f68efb8374b4` passed the final acceptance,
upstream-targeted, repository verification, and GitHub quality/tests/security
checks. T17 is complete. This archive closeout performs no new platform,
account, message, product, login, Docker, database, Redis, CHG-0018 T11/T12,
PR #28, or CHG-0019 business-code action.

T17_COMPLETED=true
PR26_MERGED=true
