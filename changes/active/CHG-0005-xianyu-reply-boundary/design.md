# CHG-0005 Design

Status: APPROVED
Change ID: CHG-0005-xianyu-reply-boundary

## Design state

CHG-0005 has project-owner approval and is now `APPROVED`.

T1 is complete.

T2 is the next executable task: `T2 Finalize reply rule, template, and decision terminology`.

T2 has not started in this execution.

No Runtime design is approved.

This document records questions, constraints, and candidate boundaries for later review.

## Architecture context

- CAP-XY-MESSAGE provides a verified local synthetic Message-receiving boundary.
- Fixed rules are intended to precede any future AI fallback.
- Message sending remains a separate, unimplemented boundary.
- WeCom and AI integrations remain separate planned capabilities.

These directions do not authorize implementation.

## Proposed terminology

Future review may define:

- Reply Rule
- Reply Template
- Match Input
- Match Condition
- Rule Priority
- Reply Decision
- No Match
- Ambiguous Match
- Conflict
- Escalation
- Human Transfer
- Suppression
- Content Safety Decision
- Synthetic Reply Fixture

No term is final until a later approved task records the decision.

## Required decisions before later task approval

- Exact Reply Rule and Reply Template terminology.
- Whether a Reply Decision contains text, a template reference, or both.
- Allowed Message-boundary input fields.
- Profile and Account ownership.
- Rule priority and deterministic precedence.
- Multiple-match conflict behavior.
- No-match behavior.
- Unsupported-language behavior.
- Escalation and human-transfer behavior.
- Sensitive-topic suppression.
- Authorization and risk-control ownership.
- Content-safety ownership.
- Rule lifecycle and versioning.
- Persistence requirements.
- Audit and observability requirements.
- Error classification.
- Import-safety requirements.
- Testing strategy.
- Migration requirements.
- API and Worker ownership boundaries.

## Candidate fixed-rule boundary

A future approved local boundary may:

- accept Synthetic Fixture input only;
- inspect explicitly approved local Message values;
- evaluate deterministic fixed rules;
- return a local decision value;
- fail closed on ambiguous or unsafe input;
- return no-send or escalation outcomes.

This candidate description is not approved Runtime design.

## Security constraints

- Never access a real Xianyu account.
- Never send a real or synthetic platform message.
- Never use real customer content in tests.
- Never store Cookie, Token, Secret, Session Material, Password, or browser state.
- Never call an external network service.
- Never call WeCom or an AI Provider.
- Never bypass verification or risk controls.
- Never guess a response for an unsupported or uncertain case.
- Never log full customer content or sensitive values.
- Use Synthetic Fixtures only.
- Fail closed.

## Current implementation

None.

No `app.reply`, `worker.reply`, rule engine, template engine, Repository, Service, Worker, API, Web UI, Migration, Scheduler Job, WeCom adapter, AI adapter, or sending behavior is approved.

All terminology, matching, authorization, risk, content safety, precedence, fallback, escalation, ownership, persistence, lifecycle, and failure decisions still require approval in later tasks.

The candidate design text remains non-runtime and must not be treated as approved implementation design.

## Approval boundary

Project-owner approval for CHG-0005 is recorded by T1.

No implementation task may begin until the required later design and boundary tasks are completed.

No implementation path, module, database table, Migration, API, Worker, Service, Repository, Scheduler, WeCom behavior, or AI behavior is added by T1.

## T2 approved terminology and data contract

### Final terminology mapping

| Candidate term | Approved term | Classification | Notes |
| --- | --- | --- | --- |
| Reply Rule | ReplyRule | Entity | Versioned local deterministic rule. |
| Match Condition | ReplyCondition | Value Object | One predicate against an approved input field. |
| Reply Template | ReplyTemplate | Entity | Versioned fixed-script body with variable allowlist. |
| Match Input | ReplyEvaluationContext | DTO | Reply-side input adapted from local Message values. |
| Reply Decision | ReplyDecision | DTO / Value Object | Evaluation result; no send side effect. |
| Rule Priority | ReplyRule.priority | Value Object field | Integer; lower value means higher priority. |
| No Match | ReplyDecisionType.NO_MATCH | Enum | No enabled rule matches. |
| Conflict | ReplyDecisionType.CONFLICT | Enum | Multiple highest-priority rules match. |
| Escalation | ReplyDecisionType.ESCALATE | Enum | Human-transfer path requested; no message sent. |
| Suppression | ReplyDecisionType.SUPPRESSED | Enum | Sensitive or unsafe content suppresses reply. |
| Synthetic Reply Fixture | SyntheticReplyFixture | Test DTO | Synthetic-only fixture, not customer data. |

### ReplyRule

Fields: `rule_id`, `name`, `enabled`, `priority`, `version`, `conditions`, `template_id`, `template_version`, `lifecycle_state`, `created_at`, `updated_at`.

Invariants:

- `rule_id` is stable and repository-unique.
- `name` is non-empty display text.
- `enabled` must be true before a rule can be evaluated.
- `priority` is an integer where a smaller value has higher priority.
- `version` is explicit and monotonically increases on semantic changes.
- `conditions` is non-empty; conditions combine with AND.
- `template_id` and `template_version` must reference an enabled template for a `REPLY` result.
- timestamps are persistence metadata, not rule semantics.

### ReplyCondition

Fields: `field`, `operator`, `comparison_value`, `normalization`, `case_sensitive`.

Approved operators for later implementation design: `equals`, `contains`, `starts_with`, and `ends_with`.

Unsupported fields or unsupported operators produce `INVALID_INPUT`; they must not be ignored or treated as no-match. Empty input fields are invalid when the condition targets a required field and no-match only when the field is explicitly optional.

### ReplyTemplate

Fields: `template_id`, `version`, `body`, `variable_allowlist`, `enabled`, `lifecycle_state`.

The body is inert text. Rendering substitutes only allowlisted variables. Missing variables, forbidden placeholders, object-property access, expression execution, file access, environment access, and network access all fail closed as `INVALID_INPUT`.

### ReplyDecision

Fields: `decision_type`, `reason_code`, `rule_id`, `template_id`, `template_version`, `rendered_text`, `escalation_reason`, `suppression_reason`, `audit_identifiers`.

Allowed null fields:

- `rule_id`, `template_id`, `template_version`, and `rendered_text` are populated only for `REPLY`.
- `escalation_reason` is populated only for `ESCALATE`.
- `suppression_reason` is populated only for `SUPPRESSED`.
- `audit_identifiers` may be empty but must never include full customer message text.

### ReplyEvaluationContext

Allowed input values are reply-side copies or normalized projections of approved local Message-boundary values, such as profile identifier, account identifier, conversation identifier, platform message identifier, content text, received timestamp, language hint, and synthetic fixture metadata.

The reply boundary must define a mapper rather than changing CAP-XY-MESSAGE. If a different shape is needed, the mapper owns the conversion and failure semantics.

### Reason codes

Approved initial reason codes:

| Decision type | Reason code | Meaning |
| --- | --- | --- |
| REPLY | RULE_MATCHED | One enabled highest-priority rule matched and template rendered. |
| NO_MATCH | NO_RULE_MATCHED | No enabled rule matched. |
| CONFLICT | DUPLICATE_HIGHEST_PRIORITY_MATCH | More than one enabled rule matched at the highest priority. |
| ESCALATE | UNSUPPORTED_LANGUAGE | Language is unsupported or unknown. |
| ESCALATE | AUTHORIZATION_UNKNOWN | Authorization state is missing or uncertain. |
| ESCALATE | RISK_UNKNOWN | Risk state is missing or uncertain. |
| ESCALATE | HUMAN_TRANSFER_REQUIRED | Configuration requires human transfer. |
| SUPPRESSED | SENSITIVE_TOPIC | Sensitive-topic policy suppresses reply. |
| INVALID_INPUT | MISSING_REQUIRED_INPUT | Required context field is missing or blank. |
| INVALID_INPUT | UNSUPPORTED_FIELD | A condition references an unsupported field. |
| INVALID_INPUT | UNSUPPORTED_OPERATOR | A condition uses an unsupported operator. |
| INVALID_INPUT | MISSING_TEMPLATE | Referenced template is missing or disabled. |
| INVALID_INPUT | MISSING_TEMPLATE_VARIABLE | Rendering lacks a required allowlisted variable. |
| INVALID_INPUT | FORBIDDEN_PLACEHOLDER | Template contains a placeholder outside the allowlist. |

T2 approves terminology and contracts only. It does not create Runtime modules, persistence, migrations, API, workers, services, repositories, or Capability binding.
