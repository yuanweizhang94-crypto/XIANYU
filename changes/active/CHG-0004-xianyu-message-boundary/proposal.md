# CHG-0004 Proposal

Status: DRAFT
Change ID: CHG-0004-xianyu-message-boundary

## Purpose

Prepare a formally reviewable boundary for receiving Xianyu customer-inquiry messages without opening a real WebSocket or accessing a real platform account.

## Target capability

- `CAP-XY-MESSAGE`

## Current authorization

This change is DRAFT only.

The project owner has authorized creation of the change proposal but has not approved implementation.

No CHG-0004 task may execute while the change remains DRAFT.

## Goals

- Define canonical terminology for message events, conversations, delivery cursors, acknowledgements, and duplicate delivery.
- Define ownership between Profile, account boundary, and a future per-account message worker.
- Define synthetic transport and adapter contracts.
- Define ordering, deduplication, replay, reconnect, and idempotency boundaries.
- Define fail-closed behavior.
- Define future persistence and observability questions.
- Define acceptance criteria before implementation.

## Non-goals

- No real Xianyu WebSocket connection.
- No external network request.
- No real Xianyu login.
- No Cookie, Token, Secret, Session Material, browser Profile, customer data, or platform credential.
- No message sending or automated reply.
- No background worker.
- No Scheduler Job.
- No database table or Migration.
- No Repository or Service.
- No API or web UI.
- No dependency addition.
- No capability binding.
- No implementation before explicit approval.

## Security boundary

- Do not bypass platform verification or risk controls.
- Do not guess protocol, permission, credential, acknowledgement, ordering, or reconnect behavior.
- Do not commit or log real message payloads or customer data.
- Use Synthetic Fixtures only.
- Stop when authorization, protocol, ownership, credential, or risk state is uncertain.

## Approval boundary

Moving this change beyond DRAFT requires separate explicit project-owner authorization.

Draft preparation does not authorize T1, runtime implementation, Ready for review, auto-merge, or merge.
