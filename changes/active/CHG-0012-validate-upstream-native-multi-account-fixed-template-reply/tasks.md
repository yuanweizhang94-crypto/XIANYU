Change ID: CHG-0012-validate-upstream-native-multi-account-fixed-template-reply
Status: DRAFT
# Tasks

- [ ] T1 Complete owner approval matrix.
- [ ] T2 Define total two-account text-message cap.
- [ ] T3 Add uncertainty-based fail-closed stop conditions.
- [ ] T4 Define verifiable native autoreply stop criteria.
- [ ] T5 Define verifiable WebSocket stop criteria.
- [ ] T6 Define no-further-send confirmation.
- [ ] T7 Define stop-command failure behavior.
- [ ] T8 Check scheduler/restart/reconnect reactivation risk.
- [ ] T9 Define masked evidence and report requirements.
- [ ] T10 Strengthen acceptance tests.
- [ ] T11 Run all repository validation.

## Current progress

Completed tasks: 0 / 11
Next task: None while status is DRAFT.

## DRAFT-only allowed work

- Documentation.
- Static code audit.
- Configuration audit.
- Upstream UI/API/service/data model search.
- Safety test plan.
- Reuse decision.
- Duplicate-risk analysis.
- Component ownership and retirement plan.

## Prohibited in DRAFT

- Business code changes.
- Upstream source changes.
- WebSocket startup.
- Native autoreply startup.
- Local worker startup.
- Real account addition.
- Scan login.
- CAPTCHA or verification flow.
- Platform message sending.
- Item, order, refund, shipping, or rating operations.
- Commit, push, PR creation, or GitHub state changes.

## Upstream capability audit

T1 and T2 must use pinned upstream static evidence for account, keyword, default reply, product-specific reply, message filter, pause, delay, duplicate protection, WebSocket, native sender, and log surfaces.

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
