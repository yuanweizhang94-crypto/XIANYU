# CHG-0005 Proposal

Status: APPROVED
Change ID: CHG-0005-xianyu-reply-boundary

## Purpose

Prepare a formally reviewable boundary for selecting local fixed-script reply decisions without sending a real Xianyu message or accessing a real platform account.

## Target capability

- `CAP-XY-REPLY`

## Current authorization

The project owner has explicitly approved CHG-0005.

This approval completes T1 and moves CHG-0005 to `APPROVED`.

T2 is the next executable task: `T2 Finalize reply rule, template, and decision terminology`.

T2 has not started in this execution.

Every later task still requires separate execution with strict task boundaries.

This approval does not authorize Runtime implementation.

This approval does not authorize Capability binding.

This approval does not authorize real Xianyu message sending.

This approval does not authorize external network access, real account access, Credential, Cookie, Token, Secret, Session Material, browser Profile, or customer-data access.

This approval does not authorize Ready for review, Reviewer request, Auto-merge, or Merge.

## Goals

- Define terminology for reply rules, templates, match inputs, decisions, no-match outcomes, escalation, and human transfer.
- Define how a future local fixed-script rule may consume approved local Message-boundary values.
- Define deterministic rule precedence and conflict handling.
- Define authorization, risk-control, content-safety, and fail-closed boundaries.
- Define future ownership, persistence, lifecycle, and failure questions.
- Define acceptance criteria before implementation.
- Preserve fixed rules as the first decision layer before any future AI fallback.

## Non-goals

- No real Xianyu message sending.
- No automatic reply delivery.
- No real account access.
- No real customer data.
- No Cookie, Token, Secret, Session Material, or browser Profile.
- No external network request.
- No Xianyu WebSocket.
- No WeCom integration.
- No AI Provider.
- No prompt generation.
- No browser automation.
- No API or Web UI.
- No database table or Migration.
- No Repository, Service, Worker, Scheduler Job, or background process.
- No dependency addition.
- No capability binding.
- No implementation before explicit approval.

## Security boundary

- Use Synthetic Fixtures only.
- Do not commit or log real customer messages, personal information, credentials, or Secret Material.
- Do not send a message.
- Do not infer permission, authorization, risk, or platform behavior.
- Do not bypass platform verification or risk controls.
- Do not generate a reply when authorization, ownership, rule match, content safety, or risk state is uncertain.
- Fail closed on ambiguous, conflicting, missing, or unsupported input.

## Approval boundary

CHG-0005 is approved for sequenced task execution only.

T1 is complete.

T2 is next and has not started.

Runtime implementation, Capability binding, Ready for review, Reviewer request, Auto-merge, and Merge remain unauthorized until separately approved by the project owner.

## T2 terminology approval record

T2 finalizes the reply-domain vocabulary and local data contract for CHG-0005.

Approved domain terms:

- `ReplyRule`: a versioned local rule that can be enabled, disabled, drafted, or archived.
- `ReplyCondition`: one deterministic predicate inside a rule; all conditions in one rule combine with AND.
- `ReplyTemplate`: a versioned fixed-script body plus an explicit variable allowlist.
- `ReplyEvaluationContext`: a reply-side DTO derived from approved local Message-boundary values.
- `ReplyDecision`: the deterministic output of local evaluation; it never sends a platform message.
- `ReplyDecisionType`: one of `REPLY`, `NO_MATCH`, `CONFLICT`, `ESCALATE`, `SUPPRESSED`, or `INVALID_INPUT`.
- `ReplyReasonCode`: a stable machine-readable explanation for the decision.

Message-to-Reply adaptation is owned by the future reply boundary. It may consume only approved local Message values and must not modify CAP-XY-MESSAGE semantics.

T2 does not authorize Runtime implementation, persistence, Capability binding, Ready for review, Reviewer request, Auto-merge, or Merge.
