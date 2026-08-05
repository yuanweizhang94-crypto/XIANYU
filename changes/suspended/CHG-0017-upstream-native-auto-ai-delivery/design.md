Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: SUSPENDED

suspended_from: IMPLEMENTING
suspended_at: 2026-08-05
suspended_reason: Project owner approved prioritizing account credential mis-save, false account disablement, missing account Profile, publish preflight, and browser mutual-exclusion fixes. CHG-0017 code, tests, evidence, and Draft PR remain preserved. T17 was not executed; the Change is incomplete, not archived, and not merged.
resume_condition: Project owner approval after CHG-0018 completion and verification.
# Design

## Execution Contract

User outcome: Make the existing upstream project's native automatic reply and AI reply usable as soon as safely possible, without continuing local slider research or building a second reply system.
Confirmed blocker: CHG-0016 live manual handoff was not accepted by the platform, while latest upstream contains newer Token and risk-control paths that must be evaluated before delivery.
Smallest success test: Configure and validate only the upstream-native account, Token, WebSocket, keyword/default/AI reply, sender, log, and stop paths with zero non-whitelist sends, then stop at `READY_FOR_GO_LIVE` until owner authorization.

## Architecture

CHG-0017 is an upstream-native configuration and validation change.

- `D:/xianyu-upstream-delivery-chg0017` is the latest upstream candidate worktree.
- `D:/xianyu-upstream-pilot` remains the currently pinned Pilot baseline and must not be modified destructively.
- `D:/xianyu` remains the governance and operations repository.
- Runtime message execution must remain in upstream websocket account tasks.
- Backend UI/API configuration must remain in upstream backend-web.
- Local wrapper commands may be used only for health, lifecycle, evidence, backup, and stop checks.

## Native Delivery Path

1. Owner configures or confirms `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B` in upstream native account management.
2. Upstream backend-web stores per-account AI settings in `XYAccount.metadata_json`.
3. Upstream keyword and default reply services manage text reply rules.
4. Upstream websocket account task obtains IM Token using configured Token mode.
5. Upstream websocket receives inbound messages.
6. `AutoReplyService.get_reply()` chooses keyword first, then AI, then default.
7. Upstream `xianyu_instance.send_msg` sends at most one reply per approved inbound test event.
8. Upstream auto-reply and AI tables provide auditable deltas.

## Safety Gate

Before any runtime:

- CHG-0010 is `FROZEN`, `DEPRECATED`, and stopped.
- Docker websocket, scheduler, host manual-listener, and unknown senders are stopped.
- Only `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B` may participate.
- Account AI settings must be explicit and complete before enabling AI.
- Active keyword/default rules must be only the CHG-0017 temporary whitelist rules.
- Message filters and other automation flags must be known.
- Baseline outbound/log/AI counters must be captured without message content.

## Validation Sequence

1. Verify PR #25/CHG-0016 blocked closeout is merged and main CI is green.
2. Create and validate latest upstream candidate worktree.
3. Back up local Pilot configuration into ignored `.local` files without secrets in terminal or Git.
4. Establish zero-risk baseline.
5. Deploy or start only the candidate upstream services required for native delivery.
6. Confirm account, Token, WebSocket, sender, keyword/default, AI, and log paths are native and singular.
7. Run controlled own-account tests with total automatic replies capped at 8.
8. Stop all executors, wait 120 seconds, and verify zero unintended sends or side effects.
9. Record redacted evidence.
10. Stop at `READY_FOR_GO_LIVE`.

## Stop Conditions

Stop immediately on:

- Missing or ambiguous `ACCOUNT-A` or `OWNER_TEST_ACCOUNT_B`.
- Missing AI provider configuration, prompt, model, or test account isolation.
- Any request for platform verification that requires owner action beyond approved scope.
- Any non-whitelist inbound or outbound message.
- Any second sender, second account task, second Token/WebSocket path, or CHG-0010 worker.
- Any item/order/refund/shipping/rating side effect.
- Any need to lower acceptance standards.

## Patch Boundary

`PATCH_UPSTREAM` may be proposed only for a confirmed defect in the latest upstream candidate that prevents safe operation of the upstream-native path. It must be minimal and cannot create a new service, dependency, sender, Token client, WebSocket client, AI worker, or automatic reply worker.

## Catalog Missing Fallback

Latest live evidence showed the upstream item ownership helper only checks the
local catalog table. Therefore a local miss is `LOCAL_ITEM_CATALOG_MISS`, not
platform proof that the item belongs to another account.

The candidate patch handles that state by recording `item_catalog_missing=true`
and continuing only through account-level routes after the CHG-0017 allowlist
gate. Item-scoped keyword/default/image/card/delivery/order/rating/item-mutation
paths are not eligible until the item exists in the local catalog. Gemini AI is
called without item context when the catalog is missing.

Item-list synchronization diagnostics are safe-count logs only: no headers,
Cookie, signed params, request body, response body, account ID, user ID, item
ID, title, URL parameter, Token, or API key may be logged.
