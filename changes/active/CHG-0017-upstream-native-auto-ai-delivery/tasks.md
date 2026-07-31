Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
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
- [ ] T17 Archive and deliver.

## Current Progress

Completed tasks: 16 / 17
Next task: T17 Archive and deliver.

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
