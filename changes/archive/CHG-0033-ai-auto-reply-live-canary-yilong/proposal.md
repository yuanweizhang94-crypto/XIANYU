# CHG-0033 AI Auto-Reply Live Canary Yilong

Change ID: CHG-0033-ai-auto-reply-live-canary-yilong
Status: ARCHIVED
Created: 2026-08-25
Owner task: chg0033_single_writer

## User Outcome

User outcome: safely enable AI auto-reply only for the approved 艺龙 account and prove exactly one safe reply to one owner-controlled inbound canary, keeping AI enabled only after PASS.

Confirmed blocker: CHG-0032 proved no current counterpart is durably owner-controlled; AI enablement must also prove no historical/unread real-customer backlog, unique native owner, provider readiness, policies and dedupe.

Smallest success test: exactly one controlled inbound and one AI reply with durable/visible readback, zero duplicate or unrelated replies; otherwise zero enablement/send.

## Scope

Allowed scope before commander GO:

- isolated worktree work under `D:/xianyu-worktrees/CHG-0033-ai-auto-reply-live-canary-yilong`;
- active Change governance/evidence creation and generated state via `python scripts/generate_state.py`;
- narrow read-only inspection of the unique native AI auto-reply owner and message receive/generate/send chain;
- read-only provider/model configuration contract discovery that reports only env/key names plus configured/present booleans and a safe injection mechanism;
- read-only approved-account readiness checks for masked `280***247`;
- read-only policy/default/SKU/sensitive-output/frequency/inbound/outbound dedupe and historical/unread backlog checks;
- sender-free provider validation only after the safe plan and provider slot are returned, and only if it cannot invoke any platform sender and no secret is logged.

Forbidden scope before commander GO:

- modifying `D:/xianyu` or any COMPANY dirty checkout;
- AI enablement, inbound canary, AI reply send, message send, deploy, Browser, publish/sync, QR/reconnect, account mutation, commit, or push;
- using, seeking, printing, or persisting the separately supplied parent AI credential;
- copying, hashing, or committing the project-owner screenshot or full approved account ID;
- enumerating ordinary conversations beyond the narrow CHG-0032 blocker confirmation;
- creating a second sender, AI delivery owner, Token/session/WebSocket owner, account owner, durable-truth model, scheduler, or COMPANY-side business owner.

## Phase 3 Decision State

`COMMANDER_GO_FOR_AI_LIVE_CANARY=false`

`AI_ENABLEMENT_ALLOWED=false`

`AI_REPLY_SEND_ALLOWED=false`

`APPROVED_ACCOUNT_MASKED=280***247`

`APPROVED_ACCOUNT_IDENTITY_BINDING=PROJECT_OWNER_SCREENSHOT_ASSERTION_EXTERNAL_NOT_PERSISTED`

`PARENT_AI_CREDENTIAL_PROVIDED_EXTERNALLY=true`

`PARENT_AI_CREDENTIAL_USED=false`

`PARENT_AI_CREDENTIAL_PRINTED=false`

`PARENT_AI_CREDENTIAL_PERSISTED=false`

`AI_ENABLEMENT_INVOCATIONS=0`

`AI_PROVIDER_INVOCATIONS=0`

`AI_REPLY_SEND_INVOCATIONS=0`

`PLATFORM_SEND_INVOCATIONS=0`

`BROWSER_INVOCATIONS=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

`OWNER_DECISION=PENDING_READ_ONLY_PREFLIGHT`

## Commander Phase 3 Closure

Commander final decision: `NO-GO`.

`AI_AUTO_REPLY_LIVE_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART_AND_PROVIDER_READINESS`

`PRIMARY_BLOCKER=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

`ADDITIONAL_BLOCKER_PROVIDER=PROVIDER_CREDENTIAL_HTTP_4XX`

`ADDITIONAL_BLOCKER_BACKLOG=UNREAD_ZERO_NOT_PROVEN`

`AI_REMAINED_DISABLED=true`

`AI_ENABLEMENT_INVOCATIONS=0`

`AI_PROVIDER_INVOCATIONS=1`

`AI_PROVIDER_INVOCATION_MODE=SENDER_FREE_CONNECTION_TEST_ONLY`

`AI_REPLY_SEND_INVOCATIONS=0`

`PLATFORM_SEND_INVOCATIONS=0`

`INBOUND_CANARY_MESSAGES=0`

`UNRELATED_CONVERSATIONS_ENUMERATED=0`

`CONFIG_PERSISTENCE_COUNT=0`

`PRODUCTION_MUTATION_COUNT=0`

`CREDENTIAL_VALUE_RECORDED=false`

`CREDENTIAL_HASH_RECORDED=false`

`FINAL_CHECKPOINT=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

## Upstream Capability Audit

The native AI auto-reply capability must be reused. Phase 3 must verify the exact current owner/function/route for message receive, AI generate, send, enablement state, policies, dedupe, backlog behavior, and durable/visible readback before any GO can be considered.

## Pinned Upstream Evidence

Pinned upstream checkout to inspect: `D:/xianyu-upstream-pilot`.

Pinned upstream SHA must be recorded during read-only owner verification. Static paths to verify are limited to upstream AI auto-reply configuration, message receive, generation, send, policy, dedupe, and durable-log/readback owners.

## Existing Local Implementation Search

Local and archived records identify upstream-first native online chat and auto-reply as the formal direction. Phase 3 will inspect only the narrow local and archived evidence required for the exact owner, provider contract, policy/dedupe/backlog gates, and the CHG-0032 no-controlled-counterpart blocker.

## Reuse Decision

Decision: ADOPT_UPSTREAM

CHG-0033 does not implement AI auto-reply. If a later GO is issued, it may use only the existing unique native AI auto-reply owner after every gate passes.

## Duplicate Implementation Risk

Risk is low while this phase remains read-only and any later canary uses the single existing native owner. Risk becomes high if a temporary sender, direct protocol call, second AI worker, second Token/session/WebSocket owner, Browser automation, manual credential persistence, or COMPANY-side business truth source is introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the AI auto-reply capability. It does not by itself certify this commander checkpoint: owner-controlled inbound canary, backlog safety, provider readiness, policy/dedupe gates, zero duplicate/unrelated replies, and keep-enabled-only-after-PASS decision.

## Approved Exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not authorized.

## Component Owner

The AI auto-reply business owner remains the existing upstream-native auto-reply owner and its backend route/service/worker chain.

## Retirement Plan For Overlapping Local Code

No overlapping local code is added.
