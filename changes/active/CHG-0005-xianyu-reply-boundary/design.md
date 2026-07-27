# CHG-0005 Design

Status: DRAFT
Change ID: CHG-0005-xianyu-reply-boundary

## Design state

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

No term is final until an approved task records the decision.

## Required decisions before approval

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

## Approval boundary

No implementation task may begin until CHG-0005 receives explicit project-owner approval.
