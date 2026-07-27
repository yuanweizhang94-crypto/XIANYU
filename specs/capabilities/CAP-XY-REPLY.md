# CAP-XY-REPLY

## Purpose

Define fixed-script reply boundary without sending real messages.

## Requirements

- Status remains planned.
- Define behavior and boundaries only.
- Do not implement runtime code before a later approved change.

## Scenarios

- Serve as requirement and acceptance input.
- Serve as ownership input for duplicate capability checks.

## Failure behavior

- Stop when permission, credential, specification, or risk state is uncertain.
- Do not guess missing business behavior.

## Security boundaries

- Do not hold real Cookie, Token, Secret, customer data, or browser credentials.
- Do not bypass platform verification or risk controls.

## Out of scope

- Runtime implementation is out of scope for CHG-0001.
- External platform or account access is out of scope for CHG-0001.

## Verification

- The capability exists in the registry with status planned.
- The specification path is unique.
- No conflicting implementation path exists.

## CHG-0005 Phase 1 design status

CHG-0005 approves design documentation only. The capability remains `planned` in the registry and remains unbound.

### T2 approved terminology

- `ReplyRule`: versioned local deterministic rule.
- `ReplyCondition`: deterministic field/operator/value predicate.
- `ReplyTemplate`: fixed-script body with variable allowlist and explicit version.
- `ReplyEvaluationContext`: reply-side DTO adapted from approved local Message-boundary values.
- `ReplyDecision`: deterministic evaluation output with no send side effect.
- `ReplyDecisionType`: `REPLY`, `NO_MATCH`, `CONFLICT`, `ESCALATE`, `SUPPRESSED`, `INVALID_INPUT`.
- `ReplyReasonCode`: stable machine-readable explanation.

### T2 data contract boundary

The Reply boundary may consume only approved local Message values through a mapper. It must not change CAP-XY-MESSAGE semantics or register implementation evidence during Phase 1.

No runtime code, persistence code, API, worker, migration, external platform client, WeCom integration, AI Provider, browser profile access, credential access, or message sending is implemented by this design record.


### T3 approved safety boundary

- Reply evaluation requires explicit local authorization for Profile, Account Reference, Conversation, and Message identifiers.
- Missing, unknown, expired, denied, revoked, or verification-required authorization returns `ESCALATE` with `AUTHORIZATION_UNKNOWN`.
- Risk state must be explicitly allowed or low risk before any `REPLY` decision can be returned.
- Unknown, unavailable, pending-review, throttled, or blocked risk states fail closed as escalation or suppression.
- Sensitive-topic and policy-blocked content suppresses replies before template rendering.
- Unsupported language and configured human transfer produce escalation decisions only.
- Audit evidence is identifier- and reason-code based; full message text, credentials, browser state, raw network payloads, and secret material are prohibited.

T3 remains design-only and registers no runtime, migration, or verification evidence.


### T4 approved matching semantics

- Supported operators are limited to `equals`, `contains`, `starts_with`, and `ends_with`.
- Conditions combine with AND only.
- Normalization is explicit and deterministic: trim, NFKC, and optional case folding.
- Smaller integer priority values are higher priority.
- Multiple matches at the best priority produce `CONFLICT` with `DUPLICATE_HIGHEST_PRIORITY_MATCH`.
- No eligible matching rule produces `NO_MATCH` with `NO_RULE_MATCHED`.
- Unsupported fields, operators, missing templates, forbidden placeholders, missing variables, and malformed configuration produce `INVALID_INPUT`.
- Suppression and escalation decisions are evaluated before matching and rendering.

T4 remains design-only and registers no runtime, migration, or verification evidence.


### T5 approved architecture boundary

- Capability owner remains `app.reply`; registry status remains planned and unbound during Phase 1.
- Future local package may be `app/xianyu_system/reply/` only after T6 authorization.
- Domain layer must remain independent of SQLAlchemy and FastAPI.
- Future persistence must use existing Core SQLAlchemy Session and Alembic boundaries.
- Future Service owns commit and rollback; Repository flushes without commit.
- Future evaluator and renderer are pure deterministic local components.
- Future tables are planned as `xianyu_reply_templates`, `xianyu_reply_rules`, `xianyu_reply_conditions`, and `xianyu_reply_audit_events`.
- Future migration is planned as `0004_xianyu_reply_boundary` after `0003_xianyu_message_boundary`; it is not created in Phase 1.
- Future verification must include Domain, Evaluator, Renderer, Mapper, Service, Persistence Contract, Migration Contract, Security, Import Safety, Capability Registry, active acceptance, and archived acceptance evidence.

No runtime, migration, dependency, workflow, registry binding, or verification evidence path is registered by T5.


### Owner Design Review corrective boundary

- T1-T5 design and architecture are approved.
- Runtime implementation is not started.
- T6 requires a separate explicit owner authorization.
- ReplyRule identity is `(rule_id, version)`.
- ReplyCondition rows reference exact rule versions through `(rule_id, rule_version)`.
- ReplyAuditEvent may reference a rule, but when it does it records both `rule_id` and `rule_version`.
- Rule and Template designs have no independent persisted `enabled` column.
- `lifecycle_state == ENABLED` is the only evaluation-eligibility source for both rules and templates.
- `ARCHIVED` records are permanently immutable and cannot transition to another lifecycle state.
- `ReplyRuleRepository`, `ReplyTemplateRepository`, and `ReplyAuditRepository` have separated responsibilities and may flush but must not commit.
- `ReplyEvaluator` returns internal `ReplyEvaluationResult`; it does not query the database, load templates, render templates, write audit events, or create final rendered decisions.
- `ReplyDecisionService` owns orchestration, exact template loading, rendering, final `ReplyDecision` construction, sanitized audit recording, commit, rollback, and fail-closed error mapping.
- Planned migration `0004_xianyu_reply_boundary` remains design-only with `down_revision = "0003_xianyu_message_boundary"`.
- No migration is created in Phase 1.

CAP-XY-REPLY remains planned and unbound with no implementation paths, test paths, active_change, or last_verified_commit.

### T6 implemented local boundary

T6 implements the approved local deterministic Reply runtime package and migration without registering capability evidence yet. The package is `app/xianyu_system/reply/` and contains pure Domain, Evaluator, Renderer, Mapper, Persistence, and Service boundaries. Migration `0004_xianyu_reply_boundary` creates local Template, Rule, Condition, and sanitized Audit tables after the verified Message migration.

The implementation does not send messages, does not access Xianyu, does not integrate WeCom or AI, does not open browser profiles, does not resolve credentials, does not create API/Web UI/worker/scheduler/sender behavior, and does not modify CAP-XY-MESSAGE semantics. CAP-XY-REPLY remains `planned`, with no registered implementation paths, test paths, active_change, or last_verified_commit until T8.

### T7 permanent evidence

T7 adds permanent tests for the local deterministic Reply boundary: Domain, Evaluator, Renderer, Mapper, Service, Persistence Contract, Security Contract, Import Safety, Migration, Runtime compatibility, Capability Registry planned-state assertions, and active acceptance. The capability remains `planned` and unbound until T8 registers exact evidence paths and verifies the candidate commit.
