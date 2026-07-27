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
