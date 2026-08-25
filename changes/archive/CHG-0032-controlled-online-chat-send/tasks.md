# CHG-0032 Tasks

Change ID: CHG-0032-controlled-online-chat-send
Status: ARCHIVED

- [x] T1 Verify latest remote main equals `3b55fdc2ae33c3f8fdc82a1afd6717e2667501a1`, create the isolated worktree from `origin/main`, and prove the branch is clean.
- [x] T2 Run `python scripts/project_context.py` before development and confirm no prior executable active Change exists on this baseline.
- [x] T3 Create the active CHG-0032 governance record with the required three-line execution contract and zero-action gates.
- [x] T4 Regenerate `generated/PROJECT_STATE.json` with `python scripts/generate_state.py` and verify with `Test-Path`, generated state, and `git status --short`.
- [x] T5 Inspect the exact unique native chat send owner/function/route plus duplicate-send/idempotency and durable-truth behavior.
- [x] T6 Run read-only approved-account readiness checks for masked `280***247`: enabled state, token/session/cookie lineage, platform verification state, WebSocket health/capability, unread/backlog counts, and service/image/restart baseline.
- [x] T7 Search repository/archived evidence and sanitized production conversation metadata only for a counterpart explicitly documented as owner-controlled.
- [x] T8 Return compact GO/NO-GO checkpoint; do not send, deploy, commit, push, Browser, QR, reconnect, AI, publish, sync, account mutate, or read/print credentials.
- [x] T9 Record commander `NO-GO`, `HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`, `MANUAL_CHAT_SENDS=0`, `ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART`, and zero mutation counters.
- [x] T10 Add and run focused archived-evidence tests for chat owner/contract, token/session/readiness, duplicate-send semantics, WebSocket baseline, CHG-0029 regression, duplicate-owner script, security, ruff, diff check, and repository verification; classify only proven pre-existing debt.
- [x] T11 Archive CHG-0032, regenerate project state to active_change/null and next_task/null, review exact diff, stage only CHG-0032 paths, commit, push, open PR, wait checks, normal merge, and verify remote main closure.

## Upstream Capability Audit

Pinned upstream native chat owner will be searched in T5.

## Pinned Upstream Evidence

Pinned upstream SHA `bda1a859df63fa5f24e51398fa80a23490bb6dfc` was inspected. Exact evidence paths:

- `backend-web/app/api/routes/chat_new.py`
- `backend-web/app/services/chat_new/im_client.py`
- `backend-web/app/services/chat_new/im_session_manager.py`
- `backend-web/app/api/routes/message.py`
- `backend-web/app/services/websocket_client.py`
- `websocket/app/api/routes/internal.py`

## T5/T6/T7 Read-Only Result

`CHAT_SEND_OWNER_ROUTE=POST /api/v1/chat-new/send-message/{account_id}`

`CHAT_SEND_OWNER_FUNCTION=backend-web/app/api/routes/chat_new.py::send_message -> backend-web/app/services/chat_new/im_client.py::GoofishImClient.send_text_message`

`CHAT_SEND_LWP=/r/MessageSend/sendByReceiverScope`

`CHAT_SEND_ACCEPTED_IDENTITY=server messageId returned by chat-new route`

`CHAT_SEND_CLIENT_UUID_GENERATED_PER_ATTEMPT=true`

`CHAT_SEND_PRE_SEND_IDEMPOTENCY_KEY_PRESENT=false`

`CHAT_SEND_DUPLICATE_GUARD=ONE_INVOCATION_COMMANDER_GATE_PLUS_POST_SEND_DURABLE_VISIBLE_READBACK_REQUIRED`

`LEGACY_SEND_ROUTES_PRESENT_OUT_OF_SCOPE=true`

`ACCOUNT_READINESS_MASKED=280***247`

`ACCOUNT_ENABLED=true`

`ACCOUNT_ONLINE=true`

`LOGIN_READY=true`

`PLATFORM_CERTIFICATION_REQUIRED=false`

`CHAT_CONVERSATION_READONLY_SUCCESS=true`

`CHAT_TOKEN_SESSION_COOKIE_LINEAGE=PASS_BY_SANITIZED_ACCOUNT_STATUS_AND_CHAT_NEW_CONVERSATION_READ`

`WEBSOCKET_READY=PASS_BY_ACCOUNT_ONLINE_AND_CHAT_NEW_CONVERSATION_READ`

`CONVERSATION_METADATA_ROWS=4`

`UNREAD_TOTAL=0`

`SERVICE_RESTART_COUNTS_ALL_ZERO=true`

`OWNER_CONTROLLED_COUNTERPART_PROVEN=false`

`NO_GO_BLOCKER=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

`CHAT_SENDS=0`

`OWNER_DECISION=NO-GO`

`MANUAL_CHAT_SENDS=0`

`ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART`

`SEND_INVOCATION_EXECUTED=false`

`SEND_READBACK_EXECUTED=false`

## Existing Local Implementation Search

Local chat and archived evidence will be searched narrowly in T5 and T7.

## Reuse Decision

Decision: ADOPT_UPSTREAM

## Duplicate Implementation Risk

No duplicate chat sender is planned.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies chat execution but not this controlled counterpart and commander checkpoint.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing upstream-native online-chat sender.

## Retirement Plan For Overlapping Local Code

No overlapping local code is added.
