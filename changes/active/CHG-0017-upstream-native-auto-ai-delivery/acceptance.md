Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
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
