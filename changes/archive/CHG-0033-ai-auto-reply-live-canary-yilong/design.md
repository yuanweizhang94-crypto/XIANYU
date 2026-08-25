# CHG-0033 Design

Change ID: CHG-0033-ai-auto-reply-live-canary-yilong
Status: ARCHIVED

## Execution Contract

User outcome: safely enable AI auto-reply only for the approved 艺龙 account and prove exactly one safe reply to one owner-controlled inbound canary, keeping AI enabled only after PASS.

Confirmed blocker: CHG-0032 proved no current counterpart is durably owner-controlled; AI enablement must also prove no historical/unread real-customer backlog, unique native owner, provider readiness, policies and dedupe.

Smallest success test: exactly one controlled inbound and one AI reply with durable/visible readback, zero duplicate or unrelated replies; otherwise zero enablement/send.

## Read-Only Phase Design

The pre-GO design is evidence-only. It creates a real active Change, regenerates project state, and performs only narrow sender-free readiness checks. It must not mutate runtime state, enable AI, send a message, deploy, use Browser, access the supplied credential, commit, or push.

Required evidence:

- latest `origin/main` equals `680363c21ca5678f7ceae831294cbb05695d4390`;
- CHG-0032 is archived on the baseline and CHG-0033 is the legal next active Change;
- active Change exists under `changes/active/CHG-0033-ai-auto-reply-live-canary-yilong`;
- provider/model configuration contract lists only env/key names, configured/present booleans, and the safe credential-injection mechanism;
- exact native AI auto-reply owner and receive/generate/send chain are identified;
- deprecated local worker remains off;
- approved account state, WebSocket/session lineage, token/verification state, current AI enablement state, backlog/unread counts, policies/defaults/SKU/sensitive-output/frequency/inbound/outbound dedupe, and sanitized reply activity counts are recorded without secrets or customer content;
- CHG-0032 no-controlled-counterpart blocker is confirmed without enumerating additional ordinary conversations.

If no owner-controlled counterpart exists, the result is `HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART` regardless of technical readiness.

## Mutation Phase Design

No mutation phase was authorized or executed. The live canary remains gated/not run because the commander issued Phase 3 `NO-GO` with `HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`, `PROVIDER_CREDENTIAL_HTTP_4XX`, and `UNREAD_ZERO_NOT_PROVEN`.

`AI_AUTO_REPLY_LIVE_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART_AND_PROVIDER_READINESS`

## Upstream Capability Audit

Pinned upstream implementation must be searched before any design expansion or validation beyond the read-only preflight. The decision order remains: adopt upstream, configure upstream, patch upstream, wrap for operations, then build local exception only with explicit approval.

## Pinned Upstream Evidence

Pinned upstream checkout to inspect: `D:/xianyu-upstream-pilot`. Pinned SHA must be recorded before any runtime validation.

## Existing Local Implementation Search

Local searches are limited to existing AI auto-reply owners, provider contract, enablement state, policies, dedupe, backlog behavior, deprecated workers, and archived CHG-0032 blocker evidence.

## Reuse Decision

Decision: ADOPT_UPSTREAM

## Duplicate Implementation Risk

No duplicate AI auto-reply sender, worker, provider adapter, token owner, or durable-truth model may be introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream can execute auto-reply but cannot independently prove commander-controlled canary ownership, backlog safety, and keep-enabled-only-after-PASS acceptance.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing upstream-native AI auto-reply owner.

## Retirement Plan For Overlapping Local Code

No overlapping production code is added.
