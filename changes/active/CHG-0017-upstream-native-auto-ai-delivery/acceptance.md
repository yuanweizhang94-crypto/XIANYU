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
- `ACCOUNT_A_ITEM_CATALOG_REQUIRED`
- `UNCONTROLLED_MESSAGE_OBSERVED`
- `READY_FOR_GO_LIVE`
- `RUNTIME_SAFETY_BLOCK`
