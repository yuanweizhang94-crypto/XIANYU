# CHG-0005 Proposal

Status: ARCHIVED
Change ID: CHG-0005-xianyu-reply-boundary

## Purpose

Prepare a formally reviewable boundary for selecting local fixed-script reply decisions without sending a real Xianyu message or accessing a real platform account.

## Target capability

- `CAP-XY-REPLY`

## Current authorization

The project owner has explicitly approved CHG-0005.

This approval completes T1 and moves CHG-0005 to `APPROVED`.

T1 through T5 are complete.

T6 is the next executable task: `T6 Implement only the approved local fixed-script reply boundary`.

T6 has not started in this execution.

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

T1 through T5 are complete.

T6 is next and has not started.

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


## T3 safety boundary approval record

T3 approves the reply-side authorization, risk-control, content-safety, suppression, and human-transfer boundary for later implementation.

Approved safety decisions:

- A fixed-script reply may be evaluated only after explicit local authorization is present for the Profile, Account Reference, Conversation, and Message identifiers in the ReplyEvaluationContext.
- Missing, unknown, expired, denied, revoked, verification-required, or otherwise uncertain authorization fails closed as `ESCALATE` with `AUTHORIZATION_UNKNOWN`.
- Risk state must be locally available and explicitly non-blocked before a `REPLY` result is allowed.
- Unknown, unavailable, pending-review, throttled, blocked, or platform-risk states fail closed as `ESCALATE` with `RISK_UNKNOWN` unless a configured suppression rule requires `SUPPRESSED`.
- Sensitive-topic policy is evaluated before template rendering. Sensitive or disallowed topics produce `SUPPRESSED` with `SENSITIVE_TOPIC` and no rendered text.
- Unsupported or unknown language produces `ESCALATE` with `UNSUPPORTED_LANGUAGE`.
- Explicit human-transfer configuration produces `ESCALATE` with `HUMAN_TRANSFER_REQUIRED`.
- Audit records may include identifiers, decision type, reason code, rule reference, template reference, timestamps, and sanitized failure category; they must not include full customer message text, credentials, browser state, or secret material.

T3 does not authorize Runtime implementation, persistence, Capability binding, Ready for review, Reviewer request, Auto-merge, or Merge.


## T4 matching behavior approval record

T4 approves deterministic matching semantics for the future local fixed-script reply evaluator.

Approved matching decisions:

- Supported condition operators are `equals`, `contains`, `starts_with`, and `ends_with` only.
- Conditions in one ReplyRule combine with AND; there is no OR, regex, script execution, fuzzy matching, semantic search, AI scoring, or external lookup.
- Normalization is explicit per condition and limited to trim, Unicode NFKC, and optional case folding.
- Case-sensitive and case-insensitive behavior must be explicitly configured; no implicit locale guessing is allowed.
- Only enabled rules and enabled templates participate in evaluation.
- Smaller integer `priority` values have higher priority.
- Multiple enabled rules may share a priority, but if more than one highest-priority matching rule exists the result is `CONFLICT` with `DUPLICATE_HIGHEST_PRIORITY_MATCH`.
- No enabled match returns `NO_MATCH` with `NO_RULE_MATCHED`.
- Unsupported field/operator, blank required input, missing template, missing variable, or forbidden placeholder returns `INVALID_INPUT`.
- Safety suppression and escalation gates approved in T3 take precedence over matching and rendering.

T4 does not authorize Runtime implementation, persistence, Capability binding, Ready for review, Reviewer request, Auto-merge, or Merge.


## T5 architecture approval record

T5 approves the Phase 1 design for future local fixed-script reply ownership, domain model, public interfaces, persistence shape, lifecycle, migration plan, and verification matrix.

Approved architecture decisions:

- CAP-XY-REPLY remains a planned `app.reply` capability until a later implementation task registers evidence.
- A future implementation may create a local package under `app/xianyu_system/reply/` that is independent of SQLAlchemy and FastAPI at the Domain layer.
- Future persistence must use the existing Core database, Session, Alembic, and explicit migration boundaries.
- Future rule evaluation is local, deterministic, synchronous, and side-effect free until a separate sending capability exists.
- Future Service code owns transaction coordination; Repository code flushes but does not commit.
- Future rule and template records are Profile-scoped and Account-scoped through existing Account and Message identifiers.
- Future Migration is planned as `0004_xianyu_reply_boundary`, after `0003_xianyu_message_boundary`, but no migration file is created in Phase 1.
- Future tests must cover Domain, Service, Persistence Contract, Security Contract, Import Safety, Migrations, Capability Registry, and archived acceptance evidence before CAP-XY-REPLY can become verified.

T5 completes Phase 1 design approval only. T6 implementation, runtime files, database migration files, dependency changes, workflow changes, Capability binding, Ready for review, Reviewer request, Auto-merge, and Merge remain unauthorized.


## Owner Design Review corrective record

The Owner Design Review corrective pass resolves Phase 1 design ambiguities without changing task completion state.

Corrective decisions:

- `ReplyRule` identity is `(rule_id, version)`.
- `rule_id` is the stable rule-family identifier; `version` is the immutable semantic rule version.
- `ReplyCondition` belongs to one exact rule version through `(rule_id, rule_version)`.
- `ReplyAuditEvent` records `rule_version` whenever `rule_id` is recorded so audits identify the exact rule version that produced a decision.
- Rule and Template eligibility is derived only from `lifecycle_state == ENABLED`; there is no independent persisted `enabled` field.
- `ARCHIVED` records are permanently immutable and cannot return to another lifecycle state.
- Rule, Template, and Audit repository responsibilities are separated.
- `ReplyEvaluator` returns an internal `ReplyEvaluationResult` without rendered text and without database, template, audit, network, AI, WeCom, browser, credential, or send behavior.
- `ReplyDecisionService` owns orchestration, template loading, rendering, final `ReplyDecision` construction, sanitized audit recording, commit, and rollback.

T1-T5 design and architecture are approved. Runtime implementation is not started. T6 requires a separate explicit owner authorization.

CAP-XY-REPLY remains planned and unbound. No Runtime, Migration, Capability evidence, dependency, workflow, Ready transition, reviewer request, auto-merge, or merge is authorized by this corrective pass.

## T6 implementation record

T6 is implemented under the approved local fixed-script reply boundary. The runtime package `app/xianyu_system/reply/` and migration `migrations/versions/0004_xianyu_reply_boundary.py` now exist. The implementation remains local and deterministic: no CLI, API, Web UI, worker loop, scheduler, sender, Xianyu client, browser adapter, WeCom adapter, AI adapter, credential resolver, external network behavior, or message sending behavior is introduced.

CAP-XY-REPLY intentionally remains `planned` and unbound during T6: implementation paths, test paths, `active_change`, and `last_verified_commit` are not registered until T8.

## T7 permanent evidence record

T7 adds permanent Reply unit, contract, security, import-safety, migration, runtime, and active acceptance evidence. The tests cover Domain invariants, deterministic evaluation, fixed-script rendering, Message-to-Reply mapping, Service transaction ownership, persistence constraints, migration behavior, audit sanitization, and prohibited external behavior.

CAP-XY-REPLY still intentionally remains `planned` and unbound after T7: implementation paths, test paths, `active_change`, and `last_verified_commit` remain empty/null until the T8 evidence candidate and verification record. T8 is the next task; T9, PR Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, and CHG-0006 remain unauthorized.

## T8 evidence candidate record

T8 Phase A registers CAP-XY-REPLY as `implementing` for the evidence candidate. The registry records the exact eight implementation paths and twelve test paths approved for CHG-0005. `active_change` is `CHG-0005-xianyu-reply-boundary`; `last_verified_commit` remains null until the Candidate commit is created, pushed, and verified locally and by GitHub Actions.

T8 is not complete in this candidate record. Tasks remain 7 / 9 and the next task remains T8 until the Verification Record records the real Candidate SHA. No runtime, migration, test, dependency, workflow, PR metadata, Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, or CHG-0006 behavior is changed by this evidence registration.


## T8 verification record

T8 Phase B verifies CAP-XY-REPLY evidence against Candidate SHA `5724d164619c64e93295595b3acdd1429d24e3e0`. The exact eight implementation paths and twelve test paths registered in Phase A remain unchanged. CAP-XY-REPLY is now `verified`; `active_change` is null; `last_verified_commit` records `5724d164619c64e93295595b3acdd1429d24e3e0`.

Tasks are now 8 / 9. T9 Complete final PR administration is the next executable task. PR Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, CHG-0006, real Xianyu access, message sending, WeCom integration, AI Provider integration, browser profile use, credential resolution, dependency changes, and workflow changes remain unauthorized.


## T9 Ready candidate preparation

CHG-0005 is moved to `VERIFYING` for final PR review preparation. T1 through T8 remain complete and T9 remains incomplete until the Ready transition and final administration record are completed.

The actual T9 Ready Candidate SHA will be the real Phase A commit created after local verification; no placeholder or pre-T9 SHA is recorded as the Ready Candidate.

CAP-XY-REPLY remains verified, `active_change` remains null, and `last_verified_commit` remains the T8 Evidence Candidate SHA `5724d164619c64e93295595b3acdd1429d24e3e0`. Implementation and evidence paths are frozen.

PR #5 remains Draft until the Ready Candidate passes final CI. No Reviewer request, auto-merge, merge, close, branch deletion, archive, CHG-0006 creation, runtime expansion, dependency change, workflow change, real Xianyu access, message sending, WeCom integration, AI Provider integration, browser Profile access, or Credential access is authorized by this preparation record.


## T9 final PR administration result

- T1 through T9 are complete.
- CHG-0005 remains `VERIFYING` while PR #5 is under review.
- T9 Ready Candidate SHA is `365cce3ef6574974c1cee1bb676fe8c1ad8ad4e3`.
- PR #5 successfully changed from Draft to Ready for review.
- PR #5 remains open and unmerged.
- No Reviewer was manually requested.
- Auto-merge is not enabled.
- CAP-XY-REPLY remains verified with Evidence Candidate SHA `5724d164619c64e93295595b3acdd1429d24e3e0`.
- Implementation and evidence paths remain unchanged and frozen.
- CHG-0005 remains under `changes/active/` and is not archived.
- No merge, close, branch deletion, archive, CHG-0006 creation, runtime expansion, migration semantic change, dependency change, workflow change, real Xianyu access, message sending, WeCom integration, AI Provider integration, browser Profile access, Credential access, Cookie, Token, Secret, Session Material, or real customer-data access occurred.
- Merge requires separate explicit authorization against the exact current PR head.

## Archive transition record

PR #5: merged.

Merged feature HEAD: `c4f7a3a3d14e34e5ebdaf6abd79587d45137f587`.

Merge commit: `f00156045d75e632d71ade640a85a4c522568158`.

Merge method: normal two-parent merge commit.

Merged-main quality/tests/security: success.

CHG-0005 is complete and archived. CAP-XY-REPLY remains `verified`; its Evidence Candidate remains `5724d164619c64e93295595b3acdd1429d24e3e0`.

This archive transition does not re-verify CAP-XY-REPLY, does not modify Runtime behavior, and does not change the eight registered implementation paths. The twelve verification paths are preserved; only the CHG-0005 acceptance evidence path moved from `changes/active/` to `changes/archive/`.

This archive transition does not authorize real message sending, Xianyu access, publishing, browser automation, WeCom integration, AI Provider integration, credential access, external network behavior, or real data access.
