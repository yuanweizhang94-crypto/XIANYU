# CHG-0005 Design

Status: APPROVED
Change ID: CHG-0005-xianyu-reply-boundary

## Design state

CHG-0005 has project-owner approval and is now `APPROVED`.

T1 through T5 are complete.

T6 is the next executable task: `T6 Implement only the approved local fixed-script reply boundary`.

T6 has not started in this execution.

T1-T5 design and architecture are approved.

Runtime implementation is not started.

T6 requires a separate explicit owner authorization.

This document records approved design constraints and boundaries for owner review; design approval does not mean implementation completion.

## Architecture context

- CAP-XY-MESSAGE provides a verified local synthetic Message-receiving boundary.
- Fixed rules are intended to precede any future AI fallback.
- Message sending remains a separate, unimplemented boundary.
- WeCom and AI integrations remain separate planned capabilities.

These directions do not authorize implementation.

## Approved terminology baseline

T2 approved these terms for the Phase 1 design:

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

T2 finalizes these terms for the Phase 1 design; later implementation may add code only after separate T6 authorization.

## Decisions approved by T1-T5 before implementation

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

## Approved fixed-rule design boundary

The approved design for a later authorized local boundary may:

- accept Synthetic Fixture input only;
- inspect explicitly approved local Message values;
- evaluate deterministic fixed rules;
- return a local decision value;
- fail closed on ambiguous or unsafe input;
- return no-send or escalation outcomes.

This approved design remains non-runtime. Runtime implementation is not started and requires separate T6 authorization.

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

No Runtime package, rule engine, template engine, Repository, Service, Worker, API, Web UI, Migration, Scheduler Job, WeCom adapter, AI adapter, or sending behavior has been implemented. The planned local `app.reply` design remains unbound until a separate T6 authorization.

T2-T5 approve terminology, matching, authorization, risk, content safety, precedence, fallback, escalation, ownership, persistence, lifecycle, and failure decisions for design review only.

The approved design text remains non-runtime and must not be treated as completed implementation.

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
| No Match | ReplyDecisionType.NO_MATCH | Enum | No lifecycle-eligible rule matches. |
| Conflict | ReplyDecisionType.CONFLICT | Enum | Multiple highest-priority rules match. |
| Escalation | ReplyDecisionType.ESCALATE | Enum | Human-transfer path requested; no message sent. |
| Suppression | ReplyDecisionType.SUPPRESSED | Enum | Sensitive or unsafe content suppresses reply. |
| Synthetic Reply Fixture | SyntheticReplyFixture | Test DTO | Synthetic-only fixture, not customer data. |

### ReplyRule

Fields: `rule_id`, `version`, `name`, `priority`, `conditions`, `template_id`, `template_version`, `lifecycle_state`, `created_at`, `updated_at`, `row_version`.

Invariants:

- `(rule_id, version)` is the immutable rule identity; `rule_id` is a stable rule-family identifier and `version` is the semantic version.
- `name` is non-empty display text.
- only `lifecycle_state == ENABLED` makes a rule eligible for evaluation; no independent persisted `enabled` state exists.
- `priority` is an integer where a smaller value has higher priority.
- `version` is explicit, monotonically increases on semantic changes, and old versions are not overwritten.
- `conditions` is non-empty; conditions combine with AND and belong to one exact `(rule_id, version)`.
- `template_id` and `template_version` must reference a template whose `lifecycle_state == ENABLED` for a `REPLY` result.
- timestamps are persistence metadata, not rule semantics.

### ReplyCondition

Fields: `field`, `operator`, `comparison_value`, `normalization`, `case_sensitive`.

Approved operators for later implementation design: `equals`, `contains`, `starts_with`, and `ends_with`.

Unsupported fields or unsupported operators produce `INVALID_INPUT`; they must not be ignored or treated as no-match. Empty input fields are invalid when the condition targets a required field and no-match only when the field is explicitly optional.

### ReplyTemplate

Fields: `template_id`, `version`, `body`, `variable_allowlist`, `lifecycle_state`.

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
| REPLY | RULE_MATCHED | One lifecycle-eligible highest-priority rule matched and template rendered. |
| NO_MATCH | NO_RULE_MATCHED | No lifecycle-eligible rule matched. |
| CONFLICT | DUPLICATE_HIGHEST_PRIORITY_MATCH | More than one lifecycle-eligible rule matched at the highest priority. |
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


## T3 approved authorization, risk-control, and content-safety boundaries

### Safety evaluation order

A later implementation must evaluate safety gates before attempting rule matching or template rendering:

1. Validate required ReplyEvaluationContext identifiers and ownership projections.
2. Validate authorization state.
3. Validate risk-control state.
4. Validate language support.
5. Validate sensitive-topic and suppression policy.
6. Evaluate deterministic rules only if all previous gates pass.
7. Render a template only for exactly one allowed `REPLY` decision.

### Authorization boundary

Approved authorization states for a reply decision are local, explicit, and fail-closed:

| Authorization state | Decision | Reason code | Notes |
| --- | --- | --- | --- |
| explicitly_authorized | continue evaluation | none | Profile, Account Reference, Conversation, and Message identifiers align. |
| missing | ESCALATE | AUTHORIZATION_UNKNOWN | No reply text is produced. |
| unknown | ESCALATE | AUTHORIZATION_UNKNOWN | No platform behavior is inferred. |
| expired | ESCALATE | AUTHORIZATION_UNKNOWN | Re-authorization is outside CHG-0005. |
| denied | ESCALATE | AUTHORIZATION_UNKNOWN | No retry or bypass is attempted. |
| revoked | ESCALATE | AUTHORIZATION_UNKNOWN | No credential lookup is attempted. |
| verification_required | ESCALATE | AUTHORIZATION_UNKNOWN | Platform verification is not bypassed. |

Authorization data is an input assertion supplied to the reply boundary. The reply boundary does not resolve credentials, access sessions, open browser profiles, or call external systems.

### Risk-control boundary

Approved risk states are deterministic local inputs:

| Risk state | Decision | Reason code | Notes |
| --- | --- | --- | --- |
| allowed | continue evaluation | none | Reply evaluation may proceed. |
| low_risk | continue evaluation | none | No special handling required. |
| unknown | ESCALATE | RISK_UNKNOWN | No reply text is produced. |
| unavailable | ESCALATE | RISK_UNKNOWN | No platform lookup is attempted. |
| pending_review | ESCALATE | RISK_UNKNOWN | Human review is required. |
| throttled | ESCALATE | RISK_UNKNOWN | Sending is outside scope. |
| blocked | SUPPRESSED | SAFETY_SUPPRESSED | No reply text is produced. |

Risk-control data may be recorded as sanitized decision metadata only. It must not include secret material, browser state, raw network payloads, or full message content.

### Content-safety and suppression boundary

Sensitive-topic handling is local and deterministic:

- Sensitive-topic detection runs before template rendering.
- Sensitive-topic matches produce `SUPPRESSED` with `SENSITIVE_TOPIC`.
- Policy-blocked content produces `SUPPRESSED` with `SAFETY_SUPPRESSED`.
- The decision must not include rendered text when suppressed.
- Suppression diagnostics may include policy identifier and sanitized category only.
- No AI Provider, external moderation service, prompt generation, or network check is introduced.

### Escalation and human transfer

Escalation is a local decision value, not a message send:

- Unsupported or unknown language returns `ESCALATE` / `UNSUPPORTED_LANGUAGE`.
- Authorization uncertainty returns `ESCALATE` / `AUTHORIZATION_UNKNOWN`.
- Risk uncertainty returns `ESCALATE` / `RISK_UNKNOWN`.
- Explicit human-transfer configuration returns `ESCALATE` / `HUMAN_TRANSFER_REQUIRED`.
- Escalation records may include sanitized reason codes and stable identifiers only.
- WeCom handoff, customer-service routing, notification, and external delivery remain outside CHG-0005 Phase 1.

### Logging and audit boundary

Allowed audit fields are stable identifiers, rule/template references, decision type, reason code, lifecycle state, and sanitized failure category. Prohibited audit fields include full message text, personal contact details, credential values, Cookie, Token, Secret, Session Material, browser Profile data, raw network payloads, file paths outside the repository, and environment variables.

### T3 non-implementation boundary

T3 approves safety semantics only. It does not create Runtime modules, persistence files, migrations, API routes, workers, schedulers, external clients, credential handlers, browser integrations, sending behavior, Capability binding, or permanent capability evidence.


## T4 approved matching, precedence, fallback, and escalation behavior

### Approved operators

The future evaluator may implement only these operators:

| Operator | Semantics | Invalid cases |
| --- | --- | --- |
| `equals` | normalized input equals normalized comparison value | missing input, unsupported field, non-text value |
| `contains` | normalized input contains normalized comparison value | missing input, empty comparison value, unsupported field |
| `starts_with` | normalized input starts with normalized comparison value | missing input, empty comparison value, unsupported field |
| `ends_with` | normalized input ends with normalized comparison value | missing input, empty comparison value, unsupported field |

Regex, wildcard matching, expression evaluation, approximate matching, embedding search, database full-text search, AI classification, network classification, browser inspection, and platform calls are prohibited.

### Normalization and case handling

Normalization is deterministic and explicitly declared per condition:

- `trim`: remove leading and trailing whitespace only.
- `nfkc`: apply Unicode NFKC normalization.
- `casefold`: apply Unicode case folding when `case_sensitive` is false.
- No language-specific locale rules are inferred.
- No punctuation stripping, tokenization, segmentation, spell correction, or semantic rewrite is performed.

A condition with `case_sensitive=true` must not case-fold either side. A condition with `case_sensitive=false` must case-fold both sides after trim and NFKC if those flags are enabled.

### Condition composition

All ReplyCondition objects inside one ReplyRule combine with AND:

- zero conditions is invalid;
- every condition must evaluate true for the rule to match;
- the first invalid condition fails the evaluation as `INVALID_INPUT`;
- false conditions make only that rule non-matching;
- there is no nested group, OR branch, custom function, callback, or script hook.

### Rule eligibility and priority

A rule is eligible only when:

- the rule lifecycle allows evaluation;
- `lifecycle_state == ENABLED`; no independent persisted `enabled` state exists;
- priority is a non-negative integer;
- at least one condition exists;
- the referenced template version exists and has `lifecycle_state == ENABLED`;
- T3 safety gates have already allowed rule evaluation.

Rules are sorted for deterministic evaluation by priority, rule identifier, and version. The sort order is used only to produce stable diagnostics; it must not break conflicts.

### Conflict behavior

If exactly one eligible rule matches at the best priority, the evaluator may render its template and return `REPLY` / `RULE_MATCHED`.

If two or more eligible rules match at the same best priority, the evaluator returns `CONFLICT` / `DUPLICATE_HIGHEST_PRIORITY_MATCH` with no rendered text. The evaluator must not choose by insertion order, update time, name, identifier, template identifier, database row order, or random order.

If lower-priority rules also match while exactly one highest-priority rule matches, the highest-priority rule wins and lower-priority matches are reported only as sanitized diagnostics if needed.

### No-match and invalid-input behavior

No eligible matching rule returns `NO_MATCH` / `NO_RULE_MATCHED` with no rendered text.

Malformed rule or template configuration returns `INVALID_INPUT`; it is not treated as no-match. Invalid input cases include unsupported field, unsupported operator, missing required input, empty required comparison value, missing template, disabled template, missing template variable, forbidden placeholder, unsupported lifecycle state, and non-integer priority.

### Fallback, suppression, and escalation precedence

T3 safety outcomes override matching:

1. `SUPPRESSED` outcomes stop evaluation and return no rendered text.
2. `ESCALATE` outcomes stop evaluation and return no rendered text.
3. `INVALID_INPUT` from context validation stops evaluation and returns no rendered text.
4. Only then can rules be matched.
5. `NO_MATCH` is returned only after eligible rules are evaluated and none match.
6. AI fallback, WeCom transfer, platform delivery, browser automation, Scheduler jobs, and external network behavior are outside this phase.

### Template failure behavior

Template rendering occurs after a single matching rule is selected. Rendering failure returns `INVALID_INPUT` with one of `MISSING_TEMPLATE`, `MISSING_TEMPLATE_VARIABLE`, or `FORBIDDEN_PLACEHOLDER`. It must not fall through to another rule, call AI, send a partial response, or synthesize replacement text.

### T4 non-implementation boundary

T4 approves deterministic behavior only. It does not create Runtime modules, persistence files, migrations, API routes, workers, schedulers, external clients, credential handlers, browser integrations, sending behavior, Capability binding, or permanent capability evidence.


## T5 approved ownership, persistence, lifecycle, and failure architecture

### Capability ownership and module boundary

CAP-XY-REPLY remains planned and unbound in `specs/CAPABILITY_REGISTRY.yaml` during Phase 1. The registry owner module remains `app.reply` as the abstract capability owner.

If T6 is later authorized, the approved local source package is `app/xianyu_system/reply/`. Planned modules are:

| Planned module | Ownership | Notes |
| --- | --- | --- |
| `app/xianyu_system/reply/__init__.py` | package surface | lazy public exports only |
| `app/xianyu_system/reply/domain.py` | pure Domain | entities, value objects, enums, DTOs, protocol types |
| `app/xianyu_system/reply/evaluator.py` | pure evaluator | deterministic safety and rule evaluation; no SQLAlchemy, FastAPI, network, or file I/O |
| `app/xianyu_system/reply/renderer.py` | pure renderer | fixed-template substitution with allowlisted variables only |
| `app/xianyu_system/reply/mapper.py` | adapter | converts approved Message-boundary values to ReplyEvaluationContext |
| `app/xianyu_system/reply/persistence.py` | SQLAlchemy persistence | ORM projections and Repository implementation only |
| `app/xianyu_system/reply/service.py` | application service | transaction coordination, repository orchestration, and decision return |

No API route, Web UI, Worker loop, Scheduler job, browser adapter, WeCom adapter, AI adapter, message sender, credential resolver, or external client is part of the approved T5 architecture.

### Final domain model

Entities:

- `ReplyRule`: Profile-scoped, Account-scoped, versioned rule. Fields: `rule_id`, `version`, `profile_id`, `account_reference`, `name`, `priority`, `lifecycle_state`, `template_id`, `template_version`, `created_at`, `updated_at`, `row_version`.
- `ReplyTemplate`: Profile-scoped, Account-scoped, versioned fixed-script template. Fields: `template_id`, `profile_id`, `account_reference`, `version`, `name`, `body`, `variable_allowlist`, `lifecycle_state`, `created_at`, `updated_at`, `row_version`.
- `ReplyAuditEvent`: sanitized local decision record. Fields: `event_id`, `profile_id`, `account_reference`, `conversation_id`, `message_id`, `rule_id`, `rule_version`, `template_id`, `template_version`, `decision_type`, `reason_code`, `failure_category`, `created_at`, `correlation_identifier`.

Value Objects:

- `ReplyCondition`: `field`, `operator`, `comparison_value`, `normalization`, `case_sensitive`.
- `ReplyPriority`: non-negative integer; smaller value means higher priority.
- `TemplateVariableName`: allowlisted identifier; no object access or expression execution.
- `ReplyRenderedText`: inert text for a local decision; never a platform send instruction.
- `ReplyAuditIdentifiers`: stable identifiers and correlation reference without full message text.

Enums:

- `ReplyDecisionType`: `REPLY`, `NO_MATCH`, `CONFLICT`, `ESCALATE`, `SUPPRESSED`, `INVALID_INPUT`.
- `ReplyReasonCode`: `RULE_MATCHED`, `NO_RULE_MATCHED`, `DUPLICATE_HIGHEST_PRIORITY_MATCH`, `UNSUPPORTED_LANGUAGE`, `AUTHORIZATION_UNKNOWN`, `RISK_UNKNOWN`, `HUMAN_TRANSFER_REQUIRED`, `SENSITIVE_TOPIC`, `SAFETY_SUPPRESSED`, `MISSING_REQUIRED_INPUT`, `UNSUPPORTED_FIELD`, `UNSUPPORTED_OPERATOR`, `MISSING_TEMPLATE`, `MISSING_TEMPLATE_VARIABLE`, `FORBIDDEN_PLACEHOLDER`, `INVALID_LIFECYCLE_STATE`, `INVALID_PRIORITY`.
- `ReplyLifecycleState`: `DRAFT`, `ENABLED`, `DISABLED`, `ARCHIVED`.
- `ReplyAuthorizationState`: `EXPLICITLY_AUTHORIZED`, `MISSING`, `UNKNOWN`, `EXPIRED`, `DENIED`, `REVOKED`, `VERIFICATION_REQUIRED`.
- `ReplyRiskState`: `ALLOWED`, `LOW_RISK`, `UNKNOWN`, `UNAVAILABLE`, `PENDING_REVIEW`, `THROTTLED`, `BLOCKED`.

DTOs:

- `ReplyEvaluationContext`: Profile, Account, Conversation, Message identifiers, approved content projection, received timestamp, language hint, authorization state, risk state, suppression hints, and synthetic fixture flag.
- `ReplyDecision`: final local decision with decision type, reason code, optional rule/template references, optional rendered text, sanitized escalation or suppression category, and audit identifiers.
- `ReplyEvaluationResult`: internal DTO / Value Object returned by the evaluator with no rendered text, no Session, and no send capability.
- `ReplyRuleSnapshot`: immutable evaluation snapshot containing `rule_id`, `rule_version`, exact condition set, exact template ID/version, priority, lifecycle state, and immutable evaluation data.
- `ReplyTemplateRenderInput`: template body, allowlist, and supplied variables.

Protocols:

- `ReplyRuleRepository`: reads exact rule versions, lists current `ENABLED` rule snapshots, saves new rule versions, performs rule lifecycle transitions, and flushes without commit.
- `ReplyTemplateRepository`: reads exact `ENABLED` template versions, saves new template versions, performs template lifecycle transitions, and flushes without commit.
- `ReplyAuditRepository`: records sanitized audit events and flushes without commit.
- `ReplyEvaluator`: evaluates context and snapshots into an internal `ReplyEvaluationResult` without loading or rendering templates.
- `ReplyTemplateRenderer`: render inert fixed text from allowlisted variables.
- `ReplyContextMapper`: adapt verified Message values into ReplyEvaluationContext without changing CAP-XY-MESSAGE.
- `ReplyDecisionService`: coordinates mapper, repositories, evaluator, renderer, final decision construction, sanitized audit recording, commit, rollback, and error mapping.

### Domain invariants and relationships

- All persisted Reply records are Profile-scoped.
- All persisted Reply records are Account-scoped through `account_reference`.
- ReplyRule identity is `(rule_id, version)` and each rule version references exactly one ReplyTemplate version.
- ReplyCondition rows belong to exactly one rule version through `(rule_id, rule_version)` and are not shared across versions.
- ReplyAuditEvent references Profile, Account, Conversation, Message, and optional exact `(rule_id, rule_version)` identifiers but does not own Message data.
- Approved lifecycle transitions are `DRAFT -> ENABLED`, `ENABLED -> DISABLED`, `DISABLED -> ENABLED`, `DRAFT -> ARCHIVED`, and `DISABLED -> ARCHIVED`; `ARCHIVED` cannot transition to any other state and archived records are immutable.
- `lifecycle_state == ENABLED` is the only evaluation-eligibility source for rules and templates; DRAFT, DISABLED, and ARCHIVED records do not participate in evaluation.
- Template bodies are inert text and may reference only allowlisted variables.
- A rendered ReplyDecision is local output only and is not a send operation.
- Row-version fields support optimistic concurrency; stale updates fail closed.
- Repository errors must be sanitized before surfacing to callers.

### Public interface contract

Planned protocol signatures are design-only and may be implemented only after T6 approval:

```python
class ReplyContextMapper(Protocol):
    def map_message(self, message: object) -> ReplyEvaluationContext: ...

class ReplyRuleRepository(Protocol):
    def list_enabled_snapshots(
        self,
        profile_id: str,
        account_reference: str,
    ) -> Sequence[ReplyRuleSnapshot]: ...
    def get_version(
        self,
        profile_id: str,
        account_reference: str,
        rule_id: str,
        version: int,
    ) -> ReplyRule | None: ...
    def add_version(self, rule: ReplyRule) -> None: ...
    def flush(self) -> None: ...

class ReplyTemplateRepository(Protocol):
    def get_enabled_version(
        self,
        profile_id: str,
        account_reference: str,
        template_id: str,
        version: int,
    ) -> ReplyTemplate | None: ...
    def add_version(self, template: ReplyTemplate) -> None: ...
    def flush(self) -> None: ...

class ReplyAuditRepository(Protocol):
    def record(self, event: ReplyAuditEvent) -> None: ...
    def flush(self) -> None: ...

class ReplyEvaluator(Protocol):
    def evaluate(
        self,
        context: ReplyEvaluationContext,
        snapshots: Sequence[ReplyRuleSnapshot],
    ) -> ReplyEvaluationResult: ...

class ReplyTemplateRenderer(Protocol):
    def render(
        self,
        template: ReplyTemplate,
        variables: Mapping[str, str],
    ) -> ReplyRenderedText: ...

class ReplyDecisionService(Protocol):
    def decide_for_message(self, message: object) -> ReplyDecision: ...
```

Transaction ownership:

- Service owns Session scope, commit, rollback, and error mapping.
- Repository receives an existing Session and must not commit.
- Evaluator and renderer are pure and own no transaction.
- Mapper does not mutate Message records.
- Local CLI, if later approved, may call the Service with synthetic fixture input and print sanitized decision JSON only.

### Database design

The approved future physical schema uses explicit relational tables, not generic JSON storage. No table is created in Phase 1.

#### `xianyu_reply_templates`

| Column | Type | Null | Constraint |
| --- | --- | --- | --- |
| `template_id` | String(36) | no | primary identity component |
| `profile_id` | String(36) | no | FK to `xianyu_account_profiles.profile_id` |
| `account_reference` | String(256) | no | trimmed, 1..256 |
| `version` | Integer | no | positive |
| `name` | String(120) | no | trimmed, 1..120 |
| `body` | String(2000) | no | non-blank, 1..2000 |
| `variable_allowlist` | String(512) | no | comma-separated allowlisted variable names only |
| `lifecycle_state` | String(16) | no | DRAFT, ENABLED, DISABLED, ARCHIVED |
| `created_at` | DateTime(timezone=True) | no | UTC |
| `updated_at` | DateTime(timezone=True) | no | UTC |
| `row_version` | Integer | no | positive optimistic concurrency value |

Keys and constraints:

- Primary key: `template_id`, `version`.
- Unique: `profile_id`, `account_reference`, `name`, `version`.
- FK: `profile_id` restricts deletion of Account Profile while templates exist.
- Checks: identifier lengths, trimmed text, positive version, positive row_version, lifecycle enum, body length, allowlist length.
- Indexes: `profile_id`, `account_reference`, `lifecycle_state`; `profile_id`, `account_reference`, `template_id`, `version`.

#### `xianyu_reply_rules`

| Column | Type | Null | Constraint |
| --- | --- | --- | --- |
| `rule_id` | String(36) | no | composite primary key component |
| `version` | Integer | no | composite primary key component and immutable semantic version |
| `profile_id` | String(36) | no | FK to Account Profile |
| `account_reference` | String(256) | no | trimmed, 1..256 |
| `name` | String(120) | no | trimmed, 1..120 |
| `priority` | Integer | no | zero or positive |
| `lifecycle_state` | String(16) | no | DRAFT, ENABLED, DISABLED, ARCHIVED |
| `template_id` | String(36) | no | FK component to ReplyTemplate |
| `template_version` | Integer | no | FK component to ReplyTemplate |
| `created_at` | DateTime(timezone=True) | no | UTC |
| `updated_at` | DateTime(timezone=True) | no | UTC |
| `row_version` | Integer | no | positive optimistic concurrency value |

Keys and constraints:

- Primary key: `rule_id`, `version`.
- Unique: `profile_id`, `account_reference`, `name`, `version`.
- FK: `profile_id` restricts deletion of Account Profile while rules exist.
- FK: `template_id`, `template_version` restricts deletion of referenced templates while rules exist.
- Checks: identifier lengths, trimmed name/account reference, non-negative priority, positive version, positive row_version, lifecycle enum.
- Indexes: `profile_id`, `account_reference`, `lifecycle_state`, `priority`; `template_id`, `template_version`; `rule_id`, `version` for composite foreign keys.

#### `xianyu_reply_conditions`

| Column | Type | Null | Constraint |
| --- | --- | --- | --- |
| `condition_id` | String(36) | no | primary key |
| `rule_id` | String(36) | no | FK component to ReplyRule |
| `rule_version` | Integer | no | FK component to ReplyRule semantic version |
| `sequence_number` | Integer | no | positive and unique per rule |
| `field_name` | String(64) | no | approved ReplyEvaluationContext field |
| `operator` | String(16) | no | equals, contains, starts_with, ends_with |
| `comparison_value` | String(512) | no | non-blank |
| `normalization` | String(64) | no | explicit normalization flags |
| `case_sensitive` | Boolean | no | explicit |

Keys and constraints:

- Primary key: `condition_id`.
- Unique: `rule_id`, `rule_version`, `sequence_number`.
- FK: `rule_id`, `rule_version` restricts deletion of the exact rule version while conditions exist unless an explicit delete workflow removes conditions first.
- Checks: identifier lengths, positive sequence, supported operator enum, non-blank comparison value, supported field enum, supported normalization flags.
- Indexes: `rule_id`, `rule_version`, `sequence_number`; `field_name`, `operator`.

#### `xianyu_reply_audit_events`

| Column | Type | Null | Constraint |
| --- | --- | --- | --- |
| `event_id` | String(36) | no | primary key |
| `profile_id` | String(36) | no | FK to Account Profile |
| `account_reference` | String(256) | no | trimmed, 1..256 |
| `conversation_id` | String(36) | no | message identifier projection |
| `message_id` | String(36) | no | message identifier projection |
| `rule_id` | String(36) | yes | populated only when applicable |
| `rule_version` | Integer | yes | required when `rule_id` is populated |
| `template_id` | String(36) | yes | populated only when applicable |
| `template_version` | Integer | yes | populated only when applicable |
| `decision_type` | String(16) | no | ReplyDecisionType |
| `reason_code` | String(64) | no | ReplyReasonCode |
| `failure_category` | String(64) | yes | sanitized category only |
| `created_at` | DateTime(timezone=True) | no | UTC |
| `correlation_identifier` | String(128) | yes | sanitized correlation only |

Keys and constraints:

- Primary key: `event_id`.
- FK: `profile_id` restricts deletion of Account Profile while audit events exist.
- Optional FK: `rule_id`, `rule_version` restricts deletion of the exact rule version when populated.
- Optional composite FK: `template_id`, `template_version` restricts deletion when populated.
- Checks: identifier lengths, trimmed account reference, rule_id/rule_version all-or-none pairing, supported decision enum, reason-code length, sanitized failure and correlation lengths.
- Indexes: `profile_id`, `account_reference`, `message_id`; `rule_id`, `rule_version`; `decision_type`, `reason_code`; `created_at`.

Prohibited stored data across all tables:

- full message text in audit rows;
- credential values;
- Cookie, Token, Secret, Password, Session Material, or browser Profile state;
- raw network payloads;
- external-service responses;
- arbitrary JSON, BLOB, metadata, extras, context, payload, or key-value extension columns.

### Migration plan

If T6 is later authorized, the planned migration is `migrations/versions/0004_xianyu_reply_boundary.py` with `down_revision = "0003_xianyu_message_boundary"`.

Upgrade order:

1. Create `xianyu_reply_templates`.
2. Create `xianyu_reply_rules` with composite primary key `(rule_id, version)`.
3. Create indexes needed by composite foreign keys.
4. Create `xianyu_reply_conditions` with composite foreign key `(rule_id, rule_version)`.
5. Create `xianyu_reply_audit_events` with optional composite foreign key `(rule_id, rule_version)`.
6. Add remaining indexes after table creation.
7. Add no seed data and run no external lookup.

Downgrade order:

1. Fail closed if reply tables contain rows unless an explicitly approved empty-downgrade path is used.
2. Drop indexes in reverse creation order.
3. Drop `xianyu_reply_audit_events`.
4. Drop `xianyu_reply_conditions`.
5. Drop `xianyu_reply_rules`.
6. Drop `xianyu_reply_templates`.
7. Preserve Account and Message tables and data.

Rollback risks and compatibility checks:

- Existing Account and Message migrations must remain present and unchanged.
- Foreign keys must not cascade-delete Account, Conversation, Message, Rule, or Template data.
- Empty downgrade must prove Account and Message rows are preserved.
- Non-empty downgrade must preserve revision, tables, and rows when it fails closed.
- Application startup must not auto-run migrations.
- Migration tests must use synthetic local databases only.

Migration created in Phase 1: no.

### Failure boundary

Failures return local decision or sanitized exception classes only:

- missing required context: `INVALID_INPUT` / `MISSING_REQUIRED_INPUT`;
- unsupported field or operator: `INVALID_INPUT` / `UNSUPPORTED_FIELD` or `UNSUPPORTED_OPERATOR`;
- invalid lifecycle or priority: `INVALID_INPUT` / `INVALID_LIFECYCLE_STATE` or `INVALID_PRIORITY`;
- missing template or template whose lifecycle is not `ENABLED`: `INVALID_INPUT` / `MISSING_TEMPLATE`;
- template variable failure: `INVALID_INPUT` / `MISSING_TEMPLATE_VARIABLE` or `FORBIDDEN_PLACEHOLDER`;
- duplicate highest-priority match: `CONFLICT` / `DUPLICATE_HIGHEST_PRIORITY_MATCH`;
- no matching rule: `NO_MATCH` / `NO_RULE_MATCHED`;
- authorization uncertainty: `ESCALATE` / `AUTHORIZATION_UNKNOWN`;
- risk uncertainty: `ESCALATE` / `RISK_UNKNOWN`;
- blocked or sensitive content: `SUPPRESSED` / `SAFETY_SUPPRESSED` or `SENSITIVE_TOPIC`.

No failure path sends a message, calls WeCom, calls AI, opens a browser, reads credentials, performs external network I/O, starts a background thread, registers a Scheduler job, creates an API route, or writes full message text to audit records.

### Test matrix

Future implementation must add permanent evidence before verification:

| Layer | Required evidence |
| --- | --- |
| Unit Domain | entity validation, `(rule_id, version)` identity, lifecycle transitions, priority ordering, rule conflict semantics, reason-code mapping |
| Unit Evaluator | safety gate order, operator semantics, normalization, case handling, AND composition, no-match, invalid-input behavior |
| Unit Renderer | allowlist-only rendering, missing variables, forbidden placeholders, inert text, no expression execution |
| Unit Mapper | approved Message-to-Reply projection, missing required identifiers, no mutation of Message semantics |
| Unit Service | transaction ownership, repository orchestration, rollback, sanitized errors, audit-event recording |
| Contract Persistence | exact tables, columns, composite rule PK, condition/audit composite FKs, lifecycle-only eligibility, constraints, indexes, row-version checks, no prohibited columns |
| Contract Migration | upgrade head, downgrade empty path, non-empty downgrade fail-closed, lineage from 0003, offline SQL scan |
| Contract Capability Registry | planned-to-verified evidence paths only after complete implementation verification |
| Security | no credentials, no browser state, no external network, no WeCom, no AI, no message sending, no full message text in audit |
| Import Safety | package and Domain imports do not import persistence, register ORM metadata, create engines, start workers, or open files |
| Active Acceptance | T6 implementation boundary must be separately authorized and cannot start during Phase 1 |
| Archived Acceptance | CHG-0005 evidence preserved under archive only after PR merge and explicit transition |


### Owner review corrective architecture

The Owner Design Review corrective pass supersedes conflicting Phase 1 text and locks the following design semantics:

- `ReplyRule` identity is `(rule_id, version)`.
- `rule_id` is a stable rule-family identifier; `version` is the immutable semantic version.
- `row_version` is only optimistic concurrency metadata for an unpublished row and never replaces semantic `version`.
- Conditions reference exact rule versions with `(rule_id, rule_version)` and cannot be shared as mutable rows across versions.
- Audit events include nullable `rule_version`; when `rule_id` is populated, `rule_version` is also required.
- Rule and Template records have no independent persisted `enabled` column.
- `lifecycle_state == ENABLED` is the only source of evaluation eligibility.
- `ARCHIVED` records are permanently immutable and cannot transition to any other state.
- Rule, Template, and Audit repositories are separate responsibilities.
- `ReplyEvaluator` returns an internal `ReplyEvaluationResult` with no rendered text and no side effects.
- `ReplyDecisionService` loads exact templates, invokes rendering, creates final `ReplyDecision`, records sanitized audit events, and owns transaction commit/rollback.
- T1-T5 design and architecture are approved; Runtime implementation is not started; T6 requires separate explicit owner authorization.

### T5 non-implementation boundary

T5 completes design approval only. It creates no Runtime package, module, migration, table, repository, service, worker, API, Web UI, Scheduler job, external adapter, dependency, workflow, Capability Registry binding, or permanent evidence path. T6 is the next task and has not started.

## T6 implementation record

T6 is implemented under the approved local fixed-script reply boundary. The runtime package `app/xianyu_system/reply/` and migration `migrations/versions/0004_xianyu_reply_boundary.py` now exist. The implementation remains local and deterministic: no CLI, API, Web UI, worker loop, scheduler, sender, Xianyu client, browser adapter, WeCom adapter, AI adapter, credential resolver, external network behavior, or message sending behavior is introduced.

CAP-XY-REPLY intentionally remains `planned` and unbound during T6: implementation paths, test paths, `active_change`, and `last_verified_commit` are not registered until T8.

## T7 permanent evidence record

T7 adds permanent Reply unit, contract, security, import-safety, migration, runtime, and active acceptance evidence. The tests cover Domain invariants, deterministic evaluation, fixed-script rendering, Message-to-Reply mapping, Service transaction ownership, persistence constraints, migration behavior, audit sanitization, and prohibited external behavior.

CAP-XY-REPLY still intentionally remains `planned` and unbound after T7: implementation paths, test paths, `active_change`, and `last_verified_commit` remain empty/null until the T8 evidence candidate and verification record. T8 is the next task; T9, PR Ready transition, reviewer request, auto-merge, merge, archive, branch deletion, and CHG-0006 remain unauthorized.
