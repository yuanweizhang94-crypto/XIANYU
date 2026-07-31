Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
# Proposal

## Title

Deliver upstream-native automatic and AI reply with controlled go-live gating

## Execution Contract

User outcome: Make the existing upstream project's native automatic reply and AI reply usable as soon as safely possible, without continuing local slider research or building a second reply system.
Confirmed blocker: CHG-0016 live manual handoff was not accepted by the platform, while latest upstream contains newer Token and risk-control paths that must be evaluated before delivery.
Smallest success test: Configure and validate only the upstream-native account, Token, WebSocket, keyword/default/AI reply, sender, log, and stop paths with zero non-whitelist sends, then stop at `READY_FOR_GO_LIVE` until owner authorization.

## Problem

The repository must move from local manual-verification repair work back to the product goal: usable Xianyu native automatic reply and AI reply. CHG-0016 closed as a blocked manual handoff because the platform did not accept the owner-only verification result. Continuing to research or automate slider handling would not deliver the business outcome.

Latest upstream has changed since the pinned Pilot SHA and now includes Token API mode, remote Token fallback, risk-control logging, and updated websocket Token handling. CHG-0017 must assess and configure that upstream-native delivery path before any live reply validation.

## Goal

- Use the latest audited upstream candidate as the delivery candidate.
- Preserve upstream ownership of account login state, IM Token acquisition, WebSocket connection, message parsing, automatic reply decisioning, AI model invocation, message sending, and reply logs.
- Use `D:/xianyu` only for governance, safety gates, configuration backup, deployment control, redacted evidence, and stop/rollback procedures.
- Validate keyword, default, and AI replies only between `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B`, capped at 8 automatic test replies total.
- Stop at `READY_FOR_GO_LIVE` after successful validation and wait for explicit owner text `GO_LIVE ACCOUNT-A`.

## Non-Goals

- No second Token client, WebSocket implementation, IM client, sender, AI worker, automatic reply worker, UI, database, or reply engine.
- No CHG-0010 worker startup or resurrection.
- No slider automation, click/drag automation, OCR, screenshot capture of verification contents, DrissionPage, Selenium, Playwright login automation, real_mouse, remote solver, or platform bypass.
- No real customer message send, non-whitelist send, item/order/refund/shipping/rating operation, image send, scan login, account relogin, Cookie clearing, Token clearing, or secret printing.
- No `CAP-AI-REPLY` verified status update until live acceptance explicitly supports it in a separate approved closeout.

## Upstream Capability Audit

Latest upstream was checked from `origin/main` of `D:/xianyu-upstream-pilot` and a detached candidate worktree:

- Candidate path: `D:/xianyu-upstream-delivery-chg0017`
- Candidate SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`
- Prior pinned Pilot SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Latest upstream commits since pinned include Token/risk-control related work: `ebd10da`, `3a75ce9`, `1c1e1cb`, `62c8914`, `fbeea7a`, `7ae9be5`, `4c5e1ac`.

Native evidence:

- Feature description: `README.md` lists automatic reply, AI reply, online chat, multi-account management, and the websocket service as the Xianyu connection/message processing service.
- Account task control: `websocket/app/api/routes/internal.py` exposes native account `start`, `stop`, `status`, `connection-stats`, and `send-message` routes.
- WebSocket runtime: `websocket/app/services/xianyu/cookie_manager.py` loads enabled accounts and starts/stops upstream account tasks.
- Reply decision order: `websocket/app/services/xianyu/auto_reply_service.py` resolves replies in keyword, AI, then default order.
- Native sender: `websocket/app/services/xianyu/auto_reply_service.py` sends through the upstream `xianyu_instance.send_msg` path.
- AI configuration: `backend-web/app/api/routes/ai.py`, `backend-web/app/services/ai_reply_service.py`, and `websocket/app/services/xianyu/ai_reply_engine.py` store per-account AI settings in `XYAccount.metadata_json`.
- Token modes: `common/services/im_token_api.py`, `common/services/token_api_mode.py`, `common/services/remote_token_api.py`, and settings UI/API provide web and remote Token acquisition paths.
- Safety data model: `common/models/xy_account.py` contains account automation flags including AI, scheduled redelivery/rate, auto polish, red flower, close order, delivery settings, and ordered-user AI blocking.

## Pinned Upstream Evidence

- Pinned Pilot path: `D:/xianyu-upstream-pilot`.
- Pinned Pilot SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.
- Latest candidate path: `D:/xianyu-upstream-delivery-chg0017`.
- Latest candidate SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`.
- Pinned Pilot remains evidence for prior blocked CHG-0012 and CHG-0016 results.
- Latest candidate is the delivery candidate for this Change and must not be represented as already deployed until runtime validation proves it.

## Existing Local Implementation Search

Existing local overlap remains limited to governance, wrapper lifecycle/status commands, synthetic local domain boundaries, historical CHG-0010 local worker code, tests, and archived evidence. CHG-0010 remains frozen, deprecated, and stopped. No local account store, Token vault, WebSocket parser, AI engine, keyword matcher, default reply engine, or sender may become the delivery path.

## Reuse Decision

Decision: CONFIGURE_UPSTREAM

Use latest upstream-native capabilities and configure them for the local Pilot. `PATCH_UPSTREAM` is allowed only if latest upstream has a specific missing safety or operations defect that blocks the smallest delivery path. `BUILD_LOCAL_EXCEPTION` is forbidden for this Change.

## Duplicate Implementation Risk

Duplicate risk is high if this work adds local alternatives for Token acquisition, WebSocket connection, message parsing, AI provider calls, keyword/default matching, outbound send, reply logs, or account orchestration. Any such path must be rejected and recorded as out of scope.

## Why Upstream Cannot Satisfy The Requirement

Not applicable as the primary decision. Latest upstream appears to contain the required native account, Token, WebSocket, keyword, default, AI, sender, and log paths. CHG-0017 exists to configure and validate those paths. If a later task proves a specific upstream safety or operations defect, that evidence must be recorded before any `PATCH_UPSTREAM` work.

## Approved Exception ADR

Not applicable. This Change does not request or allow `BUILD_LOCAL_EXCEPTION`.

## Component Owner

- Upstream backend-web owns account, rule, AI settings, and authenticated management APIs.
- Upstream websocket owns IM Token acquisition, account tasks, WebSocket connection, message parsing, reply decisioning, and sending.
- Upstream database models own account/rule/log persistence.
- `D:/xianyu` owns governance, safety gates, redacted evidence, lifecycle checks, and stop/rollback procedure only.

## Retirement Plan For Overlapping Local Code

CHG-0010 remains frozen, deprecated, and stopped. Any local helper used by CHG-0017 must remain operational control only and must not become a business executor. If latest upstream validation succeeds, later governance may retire unused local overlap in a separate approved Change.

## Owner Approvals

The owner has authorized:

- Project-owner implementation approval: Proceed with upstream-native automatic and AI reply delivery. Do not rebuild existing upstream capabilities. Do not enable production customer replies before `GO_LIVE ACCOUNT-A`.
- CHG-0016 blocked closeout.
- CHG-0017 creation for upstream-native auto/AI delivery.
- Latest upstream candidate audit.
- Controlled own-account reply validation with a hard cap of 8 automatic test replies.
- Stopping at `READY_FOR_GO_LIVE` before production enablement.

The owner has not authorized:

- Non-whitelist customer sends.
- Production automatic reply enablement.
- Creating a successor Change after CHG-0017.
- Marking AI production-ready without CHG-0017 acceptance evidence.
