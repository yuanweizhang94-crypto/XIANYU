# CHG-0004 Proposal

Status: APPROVED
Change ID: CHG-0004-xianyu-message-boundary

## Purpose

Prepare a formally reviewable boundary for receiving Xianyu customer-inquiry messages without opening a real WebSocket or accessing a real platform account.

## Target capability

- `CAP-XY-MESSAGE`

## Current authorization

The project owner explicitly approved CHG-0004 for controlled, task-by-task execution.

T1 is complete.

T2 is the next executable task, but T2 must be performed in a later, separate execution.

This approval does not authorize final message terminology, runtime implementation, a real WebSocket, external network access, real account access, Cookie or Token handling, customer-message processing, capability binding, Ready-for-review, auto-merge, or merge.


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
- No runtime implementation during the T1 approval transition.
- No runtime implementation before T2-T5 have been completed and their decisions have been formally recorded.

## Security boundary

- Do not bypass platform verification or risk controls.
- Do not guess protocol, permission, credential, acknowledgement, ordering, or reconnect behavior.
- Do not commit or log real message payloads or customer data.
- Use Synthetic Fixtures only.
- Stop when authorization, protocol, ownership, credential, or risk state is uncertain.

## Execution boundary

Only one unfinished task may be executed at a time.

This approval transition completes T1 only.

T2 must not begin in the same execution.

Runtime implementation remains prohibited until T2-T5 have finalized and approved the terminology, transport, security, ordering, persistence, worker ownership, lifecycle, failure, and testing boundaries.
