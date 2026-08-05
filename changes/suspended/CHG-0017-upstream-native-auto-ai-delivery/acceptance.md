Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: SUSPENDED

suspended_from: IMPLEMENTING
suspended_at: 2026-08-05
suspended_reason: Project owner approved prioritizing account credential mis-save, false account disablement, missing account Profile, publish preflight, and browser mutual-exclusion fixes. CHG-0017 code, tests, evidence, and Draft PR remain preserved. T17 was not executed; the Change is incomplete, not archived, and not merged.
resume_condition: Project owner approval after CHG-0018 completion and verification.
# Acceptance

## Execution Contract

User outcome: Make the existing upstream project's native automatic reply and AI reply usable as soon as safely possible, without continuing local slider research or building a second reply system.
Confirmed blocker: CHG-0016 live manual handoff was not accepted by the platform, while latest upstream contains newer Token and risk-control paths that must be evaluated before delivery.
Smallest success test: Configure and validate only the upstream-native account, Token, WebSocket, keyword/default/AI reply, sender, log, and stop paths with zero non-whitelist sends, then stop at `READY_FOR_GO_LIVE` until owner authorization.

## Required Acceptance

- CHG-0016 is archived as a blocked manual verification handoff, not as a false live success.
- Latest upstream candidate SHA is recorded and verified before runtime work.
- Reuse decision is `CONFIGURE_UPSTREAM`.
- `PATCH_UPSTREAM` remains a documented exception path only for a confirmed latest-upstream defect.
- `BUILD_LOCAL_EXCEPTION` is absent.
- No second IM, Token, WebSocket, sender, AI worker, or automatic reply worker is created.
- CHG-0010 remains frozen, deprecated, and stopped.
- `CAP-AI-REPLY` is not marked verified by this Change until acceptance evidence justifies a separate registry update.
- Controlled reply validation is limited to `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B`.
- Automatic test replies are capped at 8 total.
- No message is sent to non-whitelist accounts or real customers.
- No item, order, refund, shipping, rating, listing mutation, image send, scan login, relogin, Cookie clearing, or Token clearing occurs.
- Secrets and full identifiers are excluded from terminal output, repository evidence, PR text, and final reports.
- Validation stops at `READY_FOR_GO_LIVE` unless the owner later provides exact authorization `GO_LIVE ACCOUNT-A`.
- The task list includes T1 through T17 covering proposal, design, upstream audit, threat model, acceptance, owner approval, candidate worktree, Token/account validation, WebSocket/sender validation, reply configuration, no-send tests, controlled owner-account tests, restart/reconnect/dedup/stop, redacted report, GO_LIVE wait, production observation, and archive/delivery.

## Runtime Success Criteria

The controlled validation can be marked passed only when all are true:

- Upstream candidate services are healthy.
- Exactly one upstream-native sender is active.
- `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B` are uniquely resolved by alias without printing full IDs.
- AI settings are complete and enabled only for the approved test scope.
- Keyword/default/AI temporary rules are isolated to the approved accounts.
- WebSocket connection is native and stable.
- Reply logs, AI chat logs, and outbound counters match the expected controlled test count.
- Total automatic test replies are at most 8.
- Cleanup stops all executors and the quiet period has zero unexpected deltas.

## Failure Verdicts

- `UPSTREAM_CANDIDATE_STATIC_GATE_FAILED`
- `ZERO_SEND_CONFIGURATION_NOT_ESTABLISHED`
- `OWNER_TEST_ACCOUNT_REQUIRED`
- `AI_PROVIDER_CONFIGURATION_REQUIRED`
- `SAFE_WHITELIST_NOT_ESTABLISHED`
- `SECOND_EXECUTOR_DETECTED`
- `PLATFORM_VERIFICATION_REQUIRED`
- `TEST_MESSAGE_DIRECTION_MISMATCH_AND_ITEM_CATALOG_MISS`
- `LOCAL_ITEM_CATALOG_MISS`
- `ITEM_API_RETURNED_EMPTY`
- `ITEM_RESPONSE_SCHEMA_CHANGED`
- `ITEM_CATALOG_SAVE_FAILED`
- `ACCOUNT_COOKIE_IDENTITY_MISMATCH`
- `UNCONTROLLED_MESSAGE_OBSERVED`
- `READY_FOR_GO_LIVE`
- `DELIVERY_READY`
- `RUNTIME_SAFETY_BLOCK`

## Catalog Missing Acceptance

Local catalog absence is not proof that an item is not owned by ACCOUNT-A.
When `xy_catalog_items` does not contain the inbound `item_id`, the candidate
must record `item_catalog_missing=true`, must not log the full item ID or
message body in the catalog-missing diagnostic, and must not select item-scoped
keyword/default/image/card/delivery/order/rating/item-mutation paths.

After the CHG-0017 receiver/sender allowlist gate passes, account-level text
keyword and Gemini AI routes may remain eligible with no item scope. Non-
whitelist, unknown, system, and own-message inputs must still be denied before
keyword, AI, default, or sender execution.

Item-list sync logging must not print Cookie, `_m_h5_tk`, sign, Authorization,
full account identifiers, user IDs, full request data, full headers, or full
response bodies.

## Delivery Acceptance

Run `CHG17-GO-LIVE-20260731T1431Z` satisfied the operational delivery criteria:

- ACCOUNT-A was configured with Gemini using the upstream AI settings model.
- The API key is present only as a redacted, gitignored local secret and in
  upstream account metadata; it is not recorded in repository evidence.
- The provider test passed before WebSocket account start and performed zero
  sender or platform sends.
- Context, duplicate protection, stop, reconnect, and rollback checks passed
  using the upstream-native account task, WebSocket, AI engine, sender, and
  official OWNER_TEST_ACCOUNT_B IM send path.
- Final state is ACCOUNT-A running and connected with AI enabled.
- Active keyword rules are `0`, enabled default replies are `0`, and
  non-whitelist successful reply sends are `0`.
- Candidate backend health is reachable on `/health`.
- PR #26 remains Draft, Open, and Unmerged; no merge authorization was used.

Run `CHG17-NATIVE-UI-20260731T150428Z` satisfied the native management UI
delivery criteria:

- `http://127.0.0.1:19000` is served by the CHG-0017 candidate frontend, not
  the old Pilot frontend.
- The frontend same-origin `/api` proxy resolves to the candidate backend on
  the candidate Docker network.
- The candidate frontend, backend, MySQL, Redis, and WebSocket all use the same
  candidate runtime.
- Account management shows ACCOUNT-A enabled and online from the upstream
  WebSocket service state.
- Online chat connects ACCOUNT-A through the upstream native `chat-new` IM
  session manager, and the IM connection failure previously seen through the
  old Pilot UI is resolved.
- Online chat sessions are available after selecting ACCOUNT-A; no message was
  sent by this UI validation.
- AI switch, AI settings, provider, base URL, API key, model, prompt, keyword
  management, reply logs, and system service status controls are verified as
  upstream-native UI paths.
- The Gemini model remains `gemini-3.6-flash` without a `models/` prefix.
- No duplicate sender, IM runtime, Token runtime, WebSocket runtime, AI
  provider, or automatic reply worker was created.

Run `CHG17-MULTI-ACCOUNT-20260731T160511Z` satisfied the upstream-native
multi-account delivery criteria:

- ACCOUNT-B root cause was task not started, not missing login or invalid
  Cookie.
- Both account records were enabled and mapped to separate account rows.
- Both account tasks were running and WebSocket-connected after the native
  start path and after candidate WebSocket service restart.
- `AUTO_START_WEBSOCKET=true` restored all enabled accounts through upstream
  `CookieManager.start_all_tasks`.
- The CHG-0017 reply gate no longer hardcodes ACCOUNT-A / OWNER_TEST_ACCOUNT_B
  as the only production runtime participants; wildcard receiver/sender values
  are supported while explicit validation allowlists remain available.
- Per-account stop/start controls were validated in both directions without
  stopping the other account.
- Account management showed both account rows enabled and online.
- Online chat listed both accounts as online without sending a message.
- ACCOUNT-A AI remained enabled and Gemini-configured.
- ACCOUNT-B AI remained disabled / not configured, and ACCOUNT-B successful
  sends remained `0`.
- No second IM, Token, WebSocket, sender, AI worker, automatic reply worker,
  Redis state system, frontend page, or multi-account manager was created.

Run `CHG17-FINAL-DELIVERY-20260801T060801Z` records the non-archive final
delivery report for PR #26:

- PR #26 remains Draft, Open, and Unmerged at exact HEAD
  `60c330c31edddc28eae6bb6e1e7748b64a96289a`.
- Upstream-native account tasks, IM Token acquisition, WebSocket connection,
  reply decisioning, Gemini AI invocation, sender, logs, account settings,
  online chat, and management UI remain the reused delivery path.
- The added fixes are limited to the CHG-0017 safety patch boundary:
  allowlist fail-closed handling, catalog-miss account-level fallback, redacted
  item-sync diagnostics, Gemini parser/quality gates, and account catalog
  alignment through upstream-native AI settings service.
- Product context is available for the effective production AI account:
  catalog row, title, price, description/detail, and product AI prompt are
  present, and runtime item information is complete.
- The prior catalog blocker is classified as
  `AFFECTED_ACCOUNT_IDENTITY_MISMATCH`; after alignment, ACCOUNT-CATALOG is
  the effective production AI account.
- Provider product-context tests, controlled live AI reply, targeted acceptance
  tests, change validation, repository verification, and PR CI all passed.
- Current online boundary: ACCOUNT-CATALOG task running, WebSocket connected,
  AI enabled, active keyword rules `0`, enabled default replies `0`.
- Rollback remains the upstream-native AI disable plus account-task stop path.
- T17 remains unchecked because archive and merge are not authorized.

Run `CHG17-LAPTOP-SOURCE-SYNC-20260805T035232Z` records the production laptop
source synchronization into existing Draft PR #26:

- Runtime containers were inspected only and remained protected from stop,
  restart, rebuild, or recreate operations.
- No platform action, account task action, product publish, AI provider call, or
  message send occurred during the synchronization.
- The PR branch was fast-forwarded to remote head
  `2c1058fd5c0a9f1a572b578faf913df16e2cbd2b` before applying the laptop source
  artifact.
- The vendor patch artifact was regenerated from the candidate upstream staged
  diff and covers `12` target files, including the final product publish login
  and submit-path fixes.
- Patch SHA256 is
  `14820F96672A67E5B63EB22C8A5A3F1C0C16F8002E5514FB956EF5FBB8BC3329`.
- Clean apply, applied-source diff check, and staged blob equivalence passed.
- Targeted offline tests passed: `58`.
- Only masked Markdown evidence is submitted to Git.
- PR #26 remains Draft, Open, and Unmerged; T17 remains unchecked.
