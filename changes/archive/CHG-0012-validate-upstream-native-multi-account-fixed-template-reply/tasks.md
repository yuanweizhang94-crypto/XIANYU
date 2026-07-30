Change ID: CHG-0012-validate-upstream-native-multi-account-fixed-template-reply
Status: ARCHIVED
# Tasks

- [x] T1 Complete owner approval matrix.
- [x] T2 Define total two-account text-message cap.
- [x] T3 Add uncertainty-based fail-closed stop conditions.
- [x] T4 Define verifiable native autoreply stop criteria.
- [x] T5 Define verifiable WebSocket stop criteria.
- [x] T6 Define no-further-send confirmation.
- [x] T7 Define stop-command failure behavior.
- [x] T8 Check scheduler/restart/reconnect reactivation risk.
- [x] T9 Define masked evidence and report requirements.
- [x] T10 Strengthen acceptance tests.
- [x] T11 Run all repository validation.

## Current progress

Completed tasks: 11 / 11
Next task: null

## APPROVED allowed work

- Documentation and generated project state updates for the approved validation matrix.
- Static code audit and runtime safety gates.
- Upstream native UI/API configuration of temporary test rules after approval PR merge.
- Starting and stopping only the approved pinned upstream `websocket` compose service.
- One-at-a-time controlled text trigger messages between ACCOUNT-A and ACCOUNT-B through the upstream online-chat path.
- Redacted evidence capture, cleanup, quiet period, and validation report.

## Always prohibited

- Business code changes.
- Upstream source changes.
- WebSocket startup outside the approved command and approved validation window.
- Native autoreply startup outside the approved upstream native executor.
- Local worker startup.
- Real account addition.
- Scan login.
- CAPTCHA or verification flow.
- Platform message sending outside the approved online-chat trigger path and approved cap.
- Item, order, refund, shipping, or rating operations.
- AI reply, image reply, prompt/context reply, bargain, or CHG-0013 implementation.

## Upstream capability audit

T1 and T2 must use pinned upstream static evidence for account, keyword, default reply, product-specific reply, message filter, pause, delay, duplicate protection, WebSocket, native sender, and log surfaces.

## Approved run

- Run ID: `CHG12-20260730-0237-FE2R`
- Test accounts: `ACCOUNT-A` and `ACCOUNT-B`
- Controlled counterpart: accounts are mutual controlled counterparts.
- TEST-ITEM-1: existing item owned by `ACCOUNT-B`.
- Trigger path: `frontend/src/pages/chat-new/ChatNew.tsx` -> `frontend/src/api/chatNew.ts` -> `POST /api/v1/chat-new/send-message/{account_id}` -> `IMClient.send_text_message`.
- Start command: `Set-Location D:\xianyu-upstream-pilot; docker compose -f .\.pilot\docker-compose.pilot.yml up -d websocket`
- Stop command: `Set-Location D:\xianyu-upstream-pilot; docker compose -f .\.pilot\docker-compose.pilot.yml stop websocket`
- Quiet period: 120 seconds.
- Normal target outbound count: <= 9.
- Hard cap: 12 total outbound text autoreplies.

## Pinned upstream evidence

- Pinned path: `D:/xianyu-upstream-pilot`
- Pinned SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- DRAFT creation observed detached HEAD at the pinned SHA.

## Existing local implementation search

Local overlap to keep frozen: CHG-0009 wrapper diagnostics, CHG-0010 local autoreply worker, local YAML rule example, local idempotency/audit evidence, and synthetic local Account/Message/Reply boundaries.

## Reuse decision

Decision: CONFIGURE_UPSTREAM

## Duplicate implementation risk

Tasks must not introduce a second production sender, second matcher, second UI/API, second account store, local Cookie vault, local WebSocket parser, local delay/pause/dedup engine, or local image executor.

## Why upstream cannot satisfy the requirement

Not applicable. The tasks are designed to validate and configure upstream native behavior.

## Approved exception ADR

Not applicable. No local exception is requested.

## Component owner

Upstream owns native business execution. `D:/xianyu` owns safety gates, evidence, and governance.

## Retirement plan for overlapping local code

Keep CHG-0010 `FREEZE_AND_DEPRECATE`; evaluate retirement in CHG-0015 after CHG-0012 and CHG-0013.

## Closeout tasks

- [x] T12 Record message service restart did not recover live validation.
- [x] T13 Record websocket running with accounts disconnected before token recovery.
- [x] T14 Record token-path diagnostic conclusion.
- [x] T15 Record native token stage report.
- [x] T16 Record online-chat and token verification report.
- [x] T17 Record manual verification capability audit.
- [x] T18 Confirm runtime stop state.
- [x] T19 Archive CHG-0012 with `BLOCKED_BY_PLATFORM_VERIFICATION_GAP`.

## Final closeout status

CHG-0012 is archived because live validation is blocked by `PLATFORM_MANUAL_VERIFICATION_CAPABILITY_GAP`.

This closeout did not:

- Start websocket.
- Start scheduler.
- Start CHG-0010 local worker.
- Start browser automation.
- Request a platform Token.
- Log in any account.
- Send any message.
- Modify upstream tracked source.
- Add business implementation.
