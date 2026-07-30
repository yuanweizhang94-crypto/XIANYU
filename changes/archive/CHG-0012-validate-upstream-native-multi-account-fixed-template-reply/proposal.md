Change ID: CHG-0012-validate-upstream-native-multi-account-fixed-template-reply
Status: ARCHIVED
# Proposal

## Title

Validate upstream native multi-account fixed-template autoreply

## Owner approval

The project owner authorized creation of the original DRAFT after local notebook verification passed on 2026-07-29.

On 2026-07-30 Asia/Shanghai, the project owner approved controlled live validation for this Change using the matrix in `acceptance.md`. The approved executor is upstream native automatic reply only. The approved trigger path is the pinned upstream online-chat text-message path. The approval does not authorize AI reply, image reply, item/order/refund/shipping/rating operations, local sender creation, CHG-0010 worker startup, or any production enablement using test content.

## Goal

Plan a safe validation and configuration path for pinned upstream native multi-account fixed-template automatic reply. The target product direction is:

- `D:/xianyu-upstream-pilot`: Xianyu business application and automatic reply execution engine.
- `D:/xianyu`: safety, governance, operations, and validation control layer.

The preferred reuse decision for this change is `CONFIGURE_UPSTREAM`: validate and configure upstream native account, keyword, default reply, product-specific reply, pause, delay, filtering, duplicate protection, and logging features without rebuilding them locally.

## Non-goals

- No business code changes in `D:/xianyu`.
- No upstream source modification.
- No WebSocket startup outside the approved CHG-0012 live validation window and approved `websocket` compose service.
- No automatic reply startup outside the approved CHG-0012 live validation window and approved upstream native executor.
- No login, scan-code login, CAPTCHA handling, account addition, item, order, refund, shipping, rating, or platform operation.
- No message sending except approved one-at-a-time controlled text trigger messages between ACCOUNT-A and ACCOUNT-B through the upstream online-chat path.
- No AI provider configuration, AI model call, prompt, context, intent recognition, bargain test, CHG-0013, local keyword matcher, local YAML production rules, local autoreply worker extension, local multi-account scheduler, local account database, local Cookie vault, local WebSocket parser, local default reply engine, local product-specific reply engine, local image reply executor, local AIReplyEngine, second API adapter, second UI, second production audit, or second dedup system.

## Proposed validation scope

When this Change is later approved for execution, the validation plan must cover:

1. Two dedicated test accounts can independently exist through upstream native UI.
2. The two account login states are independent.
3. The two account WebSocket states are independent.
4. Account A and account B use different text keywords.
5. Account A keywords do not trigger account B replies.
6. Account B keywords do not trigger account A replies.
7. Default reply behavior is correct.
8. `reply_once` behavior is correct.
9. Product-specific keyword or default reply behavior is correct.
10. Variable replacement uses only variables actually supported by pinned upstream.
11. Message filtering is effective.
12. Pause automatic reply is effective.
13. Resume automatic reply is effective.
14. Reply delay is effective.
15. Duplicate message protection is effective.
16. Upstream native autoreply logs are complete enough for sanitized audit.
17. Manual intervention pause behavior is as expected.
18. Risk-control or verification state stops validation.
19. Only the upstream native sender runs.
20. The local CHG-0010 worker remains stopped.

Image keyword reply is limited to static audit and configuration availability in this Change. Real image sends are denied for this validation round.

## Approved live validation run

- Run ID: `CHG12-20260730-0237-FE2R`
- Account aliases: `ACCOUNT-A` and `ACCOUNT-B`; full account identifiers must not be written in repository evidence or reports.
- Controlled counterpart: `ACCOUNT-A` and `ACCOUNT-B` are each other's controlled test counterpart.
- TEST-ITEM-1: an existing item owned by `ACCOUNT-B`, referenced only as `TEST-ITEM-1`.
- Test window: starts after the approval PR is merged and local `main` is synced; maximum duration is 4 hours from that synced-main start time.
- Normal target outbound autoreply count: <= 9.
- Hard outbound autoreply cap: 12 total text replies across both accounts and all cases.
- Quiet period: 120 seconds after cleanup.
- Image sends: denied.
- Unknown state: stop, fail closed, no retry.

Approved start command:

```powershell
Set-Location D:\xianyu-upstream-pilot
docker compose -f .\.pilot\docker-compose.pilot.yml up -d websocket
```

Approved stop command:

```powershell
Set-Location D:\xianyu-upstream-pilot
docker compose -f .\.pilot\docker-compose.pilot.yml stop websocket
```

## Upstream capability audit

Pinned upstream was searched for UI, API, service, and data model evidence related to the validation scope. Evidence paths include:

- `common/models/xy_account.py` for account status, pause duration, and reply delay fields.
- `common/models/xy_keyword_rule.py` for keyword rules, reply type, item binding, and image URL fields.
- `common/models/default_reply.py` for default reply and `reply_once` data model.
- `common/models/auto_reply_message_log.py` for upstream native autoreply log fields.
- `backend-web/app/api/routes/cookies.py` and `frontend/src/pages/accounts/Accounts.tsx` for account UI/API management.
- `backend-web/app/api/routes/keywords.py`, `backend-web/app/services/keyword_service.py`, `frontend/src/pages/keywords/Keywords.tsx`, and `frontend/src/api/keywords.ts` for keyword configuration.
- `backend-web/app/services/default_reply_service.py`, `common/utils/default_reply_api.py`, and `frontend/src/api/items.ts` for default and item-specific reply configuration.
- `backend-web/app/api/routes/message_filters.py` for message filter configuration.
- `backend-web/app/api/routes/auto_reply_logs.py`, `backend-web/app/services/auto_reply_log_service.py`, and `frontend/src/pages/autoReplyLogs/AutoReplyLogs.tsx` for log review.
- `websocket/app/services/xianyu/connection_manager.py`, `websocket/app/services/xianyu/message_handler.py`, `websocket/app/services/xianyu/auto_reply_service.py`, and `websocket/app/services/xianyu/auto_reply_log_service.py` for native receiving, reply execution, and log updates.

This audit records presence and planned validation only. It does not claim live multi-account autoreply success.

## Pinned upstream evidence

- Upstream path: `D:/xianyu-upstream-pilot`
- Expected SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Actual SHA at DRAFT creation: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Upstream branch state at DRAFT creation: detached HEAD.
- Upstream tracked source modified by this change: no.
- Upstream worktree note: local untracked `.pilot/` exists and was not modified by this change.

## Existing local implementation search

`D:/xianyu` was searched for `autoreply`, `auto reply`, `keyword`, `fallback`, `watermark`, `cooldown`, `rate.limit`, `send_confirmed_reply`, `NormalizedInboundMessage`, `UpstreamClient`, `listener`, `default reply`, and `product-specific` under `app`, `tests`, `docs`, `changes`, and `specs`.

Existing local overlap is limited to governance, wrapper diagnostics, historical CHG-0010 local autoreply worker code, synthetic Account/Message/Reply boundaries, and tests. The current disposition is documented in `docs/LOCAL_COMPONENT_DISPOSITION.md`: CHG-0010 local autoreply worker is `FREEZE_AND_DEPRECATE`, local YAML rules are deprecated, and local wrapper commands are operations/diagnostics only.

## Reuse decision

Decision: CONFIGURE_UPSTREAM

Use upstream native account UI/API, keyword/default/product-specific reply configuration, native WebSocket, native autoreply service, and native autoreply logs. If pinned upstream configuration is insufficient, the documented decision order is:

1. `CONFIGURE_UPSTREAM`
2. Small `PATCH_UPSTREAM` proposal
3. `WRAP_FOR_OPERATIONS`

Direct local rewrite is forbidden.

## Duplicate implementation risk

Duplicate risk is high if `D:/xianyu` adds a second account system, Cookie vault, WebSocket parser, keyword matcher, default reply engine, product-specific reply engine, image reply executor, delay executor, pause scheduler, dedup system, production reply log, local worker, local UI, local API adapter, or AI reply system. This Change must prevent those duplicate paths and validate upstream-native ownership first.

## Why upstream cannot satisfy the requirement

Not applicable at DRAFT time. Pinned upstream appears to contain the required native account, keyword, default reply, product-specific reply, WebSocket, filtering, delay, pause, duplicate-protection, and log surfaces. The Change exists to validate and configure those upstream capabilities, not to prove an upstream gap.

## Approved exception ADR

Not applicable. No `BUILD_LOCAL_EXCEPTION` is requested or allowed by this DRAFT.

## Component owner

- Business application, login/session handling, WebSocket, message parsing, keyword/default/product-specific reply execution, reply delay, pause, duplicate protection, image reply execution, and production reply logs: pinned upstream deployment at `D:/xianyu-upstream-pilot`.
- Safety gate, owner approval checklist, sole-executor verification, redacted validation report, stop/rollback checklist, and repository governance: `D:/xianyu`.

## Retirement plan for overlapping local code

CHG-0010 local autoreply worker remains `FREEZE_AND_DEPRECATE`. It may be used only as historical evidence or later owner-approved controlled diagnostic comparison. It must not be restored as the formal executor. CHG-0015 remains the planned retirement evaluation after CHG-0012 and CHG-0013 validation.

## Closeout summary

CHG-0012 is archived without production activation. The feature was not judged failed. Live validation was blocked by the platform verification precondition:

`PLATFORM_MANUAL_VERIFICATION_CAPABILITY_GAP`

The final acceptance verdict is:

`BLOCKED_BY_PLATFORM_VERIFICATION_GAP`

Validated evidence:

- Pinned upstream identity was confirmed at `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.
- Pinned upstream remained detached at the approved pilot checkout.
- Multi-account configuration isolation has static upstream evidence.
- Upstream native fixed-template reply capability exists in source evidence.
- The websocket service can be built, started, and health checked.
- Backend-to-websocket control URL mismatch was confirmed and corrected in the local pilot `.pilot` configuration.
- Account tasks can be created.
- CHG-0010 local worker remained stopped.
- No second sender was observed.
- Safety caps, cleanup flow, and fail-closed handling were effective.
- No attempted validation produced an automatic reply.
- Repository verification passed after closeout.

Unverified live capabilities:

- Keyword reply live result.
- Account isolation live result.
- Default reply.
- `reply_once`.
- Product-specific reply.
- Variables.
- Filtering.
- Pause/resume.
- Delay.
- Duplicate protection.
- Live logs.
- Production activation.

Root cause:

- The upstream IM Token API returned an official platform verification requirement.
- The account login itself remained valid; there was no evidence requiring relogin.
- Pinned upstream only provides automated slider handling through browser automation, DrissionPage, real_mouse, or remote solver paths.
- Current safety authorization forbids automated solving and remote solving.
- Pinned upstream, latest upstream, and local historical research did not contain a reusable pure manual verification handoff.
- Therefore CHG-0012 live validation cannot continue until an independent manual verification handoff Change is designed, approved, and implemented.

Final runtime safety state:

- Websocket remains stopped.
- Port 18090 is not listening.
- Scheduler remains stopped.
- Local worker reports `running=False`.
- CHG12 keyword rules: 0.
- CHG12 filters: 0.
- Enabled default replies: 0.
- Autoreply logs: 0.
- ACCOUNT-A processing risk rows: 0.
- Browser/captcha automation process count: 0.
- Messages sent by CHG-0012 validation: 0.
- Upstream tracked source remained unchanged.
