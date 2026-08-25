# CHG-0032 Acceptance

Change ID: CHG-0032-controlled-online-chat-send
Status: ARCHIVED

## Required Phase 2 Acceptance

- CHG-0032 is the only active Change in the isolated worktree.
- The Change records the three-line execution contract:
  - User outcome: send exactly one harmless controlled message through the existing unique native chat owner from the approved account 艺龙 to a proven user-controlled counterpart.
  - Confirmed blocker: a user-controlled counterpart/conversation and acceptance-grade token/session/durable-readback evidence must be proven; ordinary customers must never receive the canary.
  - Smallest success test: one send invocation, one message id, outbound durable truth plus remote/counterpart visible readback, zero duplicate or unrelated sends.
- `REAL_CHAT_SEND_ALLOWED=false` until the commander later sends exact `GO_FOR_REAL_CHAT_SEND`.
- Message text, if later authorized, is exactly `系统功能测试，请忽略，无需回复。`
- No Cookie/Token/JWT/Authorization/password/API key/private key/Profile secret/customer content/full account ID/screenshot copy/screenshot hash is printed or committed.
- No send, deploy, commit, push, Browser, QR, reconnect, AI enablement, inbound automation, publish, sync, account mutation, or credential access occurs in Phase 2.

## Current Gate State

`COMMANDER_GO_FOR_REAL_CHAT_SEND=false`

`REAL_CHAT_SEND_ALLOWED=false`

`APPROVED_ACCOUNT_MASKED=280***247`

`APPROVED_ACCOUNT_IDENTITY_BINDING=PROJECT_OWNER_SCREENSHOT_ASSERTION_EXTERNAL_NOT_PERSISTED`

`OWNER_CONTROLLED_COUNTERPART_PROVEN=false`

`CONTROLLED_COUNTERPART=false`

`CHAT_OWNER_PROVEN=true`

`ACCOUNT_CHAT_READINESS=PASS_READ_ONLY`

`GO_RECOMMENDED=false`

`NO_GO_BLOCKER=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

`FINAL_CHECKPOINT=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

`MESSAGE_SEND_INVOCATIONS=0`

`CHAT_SENDS=0`

`CONVERSATION_METADATA_ROWS=4`

`UNREAD_TOTAL=0`

`CUSTOMER_CONTENT_PERSISTED=false`

`COUNTERPART_IDS_PERSISTED=false`

`AI_INVOCATIONS=0`

`BROWSER_INVOCATIONS=0`

`QR_INVOCATIONS=0`

`RECONNECT_INVOCATIONS=0`

`PUBLISH_INVOCATIONS=0`

`SYNC_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

`OWNER_DECISION=NO-GO`

`MANUAL_CHAT_SENDS=0`

`ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART`

`SEND_INVOCATION_EXECUTED=false`

`SEND_READBACK_EXECUTED=false`

`REMOTE_VISIBLE_READBACK_EXECUTED=false`

## T5/T6/T7 Read-Only Result

The exact existing native online-chat send owner is `POST /api/v1/chat-new/send-message/{account_id}` in `backend-web/app/api/routes/chat_new.py`, which calls `backend-web/app/services/chat_new/im_client.py::GoofishImClient.send_text_message` and sends through `/r/MessageSend/sendByReceiverScope`.

The route returns the server `messageId`; the client generates a fresh UUID per attempt and has no caller-supplied pre-send idempotency key. Therefore any later acceptance requires exactly one commander-authorized invocation plus post-send remote visible readback through `GET /api/v1/chat-new/messages/{account_id}/{cid}`. No later send is authorized in this phase.

Sanitized read-only account and conversation checks for masked account `280***247` showed account enabled, online, login ready, platform certification not required, conversation read succeeded, four sanitized conversation metadata rows, unread total zero, and inspected XIANYU service restart counts all zero.

Repository/archive evidence proves historical `ACCOUNT-A`/`ACCOUNT-B` controlled counterpart use, but no collected durable provenance binds those aliases or any current sanitized production conversation to masked account `280***247`. Current conversation metadata cannot prove control by name, recency, content, or ordinary existence. Final result: `HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`; `CHAT_SENDS=0`.

## Commander Phase 2 Closure

Commander decision: `NO-GO`.

`HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART=true`

`MANUAL_CHAT_SENDS=0`

`ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART`

T5/T6/T7 completed read-only. The real send, message-id acceptance,
remote/counterpart visible readback, and terminal durable acceptance remain
intentionally unexecuted because the hard gate requires an explicitly proven
owner-controlled counterpart before any send.

## Upstream Capability Audit

Same as proposal.

## Pinned Upstream Evidence

Same as proposal.

## Existing Local Implementation Search

Same as proposal.

## Reuse Decision

Decision: ADOPT_UPSTREAM

## Duplicate Implementation Risk

No duplicate chat sender is accepted.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies send execution but not this pre-send commander checkpoint.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing upstream-native online-chat sender.

## Retirement Plan For Overlapping Local Code

No overlapping local code is introduced.
