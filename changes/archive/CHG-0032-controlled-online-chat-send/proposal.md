# CHG-0032 Controlled Online Chat Send

Change ID: CHG-0032-controlled-online-chat-send
Status: ARCHIVED
Created: 2026-08-25
Owner task: chg0032_single_writer

## User Outcome

User outcome: send exactly one harmless controlled message through the existing unique native chat owner from the approved account 艺龙 to a proven user-controlled counterpart.

Confirmed blocker: a user-controlled counterpart/conversation and acceptance-grade token/session/durable-readback evidence must be proven; ordinary customers must never receive the canary.

Smallest success test: one send invocation, one message id, outbound durable truth plus remote/counterpart visible readback, zero duplicate or unrelated sends.

## Scope

Allowed scope:

- isolated worktree work under `D:/xianyu-worktrees/CHG-0032-controlled-online-chat-send`;
- active Change governance/evidence creation and generated state via `python scripts/generate_state.py`;
- narrow read-only inspection of the unique native chat send owner/function/route, idempotency and durable truth;
- read-only account/chat readiness checks for the approved account, recorded only as masked `280***247`;
- read-only repository, archived-evidence, and sanitized production-conversation metadata search for an explicitly documented owner-controlled counterpart;
- compact GO/NO-GO checkpoint only.

Forbidden scope:

- modifying `D:/xianyu` or any COMPANY dirty checkout;
- message send before the exact later commander token `GO_FOR_REAL_CHAT_SEND`;
- Browser, QR, reconnect, AI enablement, inbound automation, publish, sync, account mutation, credential access, credential logging, deploy, restart, commit, or push;
- inferring owner control from ordinary conversations, nicknames, recency, or message text;
- persisting customer content, full account IDs, full conversation IDs, Cookies, Tokens, Authorization values, Profile secrets, screenshot content, screenshot hashes, or private identifiers;
- creating a second chat sender, Token owner, Session owner, WebSocket owner, account owner, durable-truth model, scheduler, or COMPANY-side business owner.

## Phase 2 Decision State

`COMMANDER_GO_FOR_REAL_CHAT_SEND=false`

`REAL_CHAT_SEND_ALLOWED=false`

`APPROVED_ACCOUNT_MASKED=280***247`

`APPROVED_ACCOUNT_IDENTITY_BINDING=PROJECT_OWNER_SCREENSHOT_ASSERTION_EXTERNAL_NOT_PERSISTED`

`MESSAGE_TEXT_IF_LATER_AUTHORIZED=系统功能测试，请忽略，无需回复。`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_INVOCATIONS=0`

`BROWSER_INVOCATIONS=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

`OWNER_DECISION=NO-GO`

`MANUAL_CHAT_SENDS=0`

`ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART`

`NO_GO_BLOCKER=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

`SEND_INVOCATION_EXECUTED=false`

`SEND_READBACK_EXECUTED=false`

## Upstream Capability Audit

The native chat capability must be reused. Phase 2 will verify the exact current owner/function/route in the pinned upstream/local runtime source before any GO can be considered.

Expected ownership class:

```text
existing upstream-native online chat path
-> existing backend chat route/service
-> existing IM/WebSocket Token/session owner
-> existing native send function
-> existing outbound durable log/readback
```

No replacement sender or local protocol implementation is authorized.

## Pinned Upstream Evidence

Pinned upstream checkout to inspect: `D:/xianyu-upstream-pilot`.

Pinned upstream SHA must be recorded from the checkout during Phase 2 read-only owner verification. Static paths to verify are limited to upstream chat route/service/sender and models directly owning online chat send and durable logs.

## Existing Local Implementation Search

The local repository records identify the final product direction as upstream-first native online chat. Phase 2 will inspect only the narrow local and archived evidence needed to prove the exact owner, idempotency and owner-controlled counterpart state.

## Reuse Decision

Decision: ADOPT_UPSTREAM

CHG-0032 does not implement chat sending. If a later GO is issued, it may use only the existing unique native chat owner after every gate passes.

## Duplicate Implementation Risk

Risk is low while this phase remains read-only and any later send uses the single existing native owner. Risk becomes high if a temporary send script, direct protocol call, second sender, second Token/session/WebSocket owner, Browser automation, AI/autoreply enablement, or COMPANY-side business truth source is introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the chat send capability. It does not by itself certify that the target conversation is owner-controlled or produce this commander checkpoint. CHG-0032 supplies only governance and read-only evidence around the existing owner.

## Approved Exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not authorized.

## Component Owner

The chat send business owner remains the existing upstream-native online-chat sender and its backend route/service. COMPANY, if later used, remains transport only.

## Retirement Plan For Overlapping Local Code

No overlapping local code is added.
