# CHG-0032 Design

Change ID: CHG-0032-controlled-online-chat-send
Status: ARCHIVED

## Design Intent

Prepare, but do not execute, one controlled online-chat send from approved account 艺龙, recorded only as masked `280***247`, to a counterpart proven by explicit evidence to be owner-controlled. If counterpart control cannot be proven, fail closed as `HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`.

## Execution Order

1. Verify the clean isolated worktree, branch, HEAD, and latest remote main.
2. Create the active Change record and regenerate `generated/PROJECT_STATE.json`.
3. Verify active record existence with `Test-Path`, generated state, and `git status --short`.
4. Inspect only the exact native chat owner/function/route, idempotency and durable-truth path.
5. Run read-only approved-account readiness checks: enabled state, chat token/session/cookie lineage, platform verification state, WebSocket health/capability, unread/backlog counts, service/image/restart baseline.
6. Search only repository/archived evidence and sanitized production conversation metadata for a counterpart explicitly documented as owner-controlled.
7. Return a compact GO/NO-GO checkpoint. Do not send without exact later `GO_FOR_REAL_CHAT_SEND`.

## Gate Contract

```text
COMMANDER_GO_FOR_REAL_CHAT_SEND=false
REAL_CHAT_SEND_ALLOWED=false
MESSAGE_SEND_INVOCATIONS=0
TARGET_COUNTERPART_CONTROL=UNPROVEN
GO_RECOMMENDED=false
ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART
SEND_INVOCATION_EXECUTED=false
SEND_READBACK_EXECUTED=false
```

## Expected Native Owner

The only allowed later send path is:

```text
existing upstream-native online-chat account selection
-> existing backend chat route/service
-> existing Token/session/WebSocket owner
-> existing native send function
-> durable outbound log/readback
```

The exact source path and function names are Phase 2 read-only evidence outputs.

## Identity Binding

The project owner supplied direct identity authorization plus an external sensitive screenshot for masked account `280***247`. The screenshot itself, its hash, and the full account id must not be copied, persisted, committed, or printed in repository/final output.

## Rollback

Before real send, rollback is removal of the CHG-0032 active record and regeneration of `generated/PROJECT_STATE.json`. No production rollback is required because Phase 2 performs no production mutation.

## Closure Decision

Commander decision is `NO-GO`: `HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`.
T5/T6/T7 completed read-only, but the real send, message-id acceptance,
remote/counterpart visible readback, and terminal durable acceptance remain
unexecuted because the hard gate requires an explicitly proven
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

No second chat sender, Token owner, Session owner, WebSocket owner, account owner, durable-truth source, scheduler, Browser path, or AI/autoreply executor may be introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream satisfies send execution; CHG-0032 only supplies the controlled business checkpoint and evidence record.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing upstream-native online-chat sender via its backend route/service.

## Retirement Plan For Overlapping Local Code

No overlapping production code is planned.
