# CHG-0004 Design

Status: DRAFT
Change ID: CHG-0004-xianyu-message-boundary

## Design state

No runtime design is approved.

This document records questions, constraints, and candidate boundaries for later review.

## Architecture context

- One worker per Xianyu account.
- One local Profile boundary per account.
- WebSocket is the future message-receiving transport direction.
- Fixed rules take priority over AI fallback.

These directions do not authorize a real transport implementation.

## Proposed terminology

Future review may define:

- Message Event
- Conversation Identifier
- Sender Reference
- Recipient Profile Identifier
- Platform Message Identifier
- Delivery Cursor
- Delivery Attempt
- Acknowledgement
- Duplicate Delivery
- Replay
- Reconnect
- Ordering Boundary
- Synthetic Transport Fixture

No term is final until an approved task records the decision.

## Required decisions before approval

- Exact terminology.
- Profile and account ownership.
- Transport ownership.
- Authentication and credential-resolution ownership.
- Reconnect and backoff.
- Acknowledgement behavior.
- Ordering guarantees.
- Deduplication and idempotency.
- Replay and recovery.
- Persistence and retention.
- Logging and observability.
- Failure classification.
- Testing strategy.
- Migration requirements.
- Import-safety requirements.

## Security constraints

- Never open a real Xianyu WebSocket.
- Never import real credentials, browser Profiles, or customer messages.
- Never bypass platform verification.
- Never infer missing protocol behavior.
- Never share state across Profiles.
- Never log full message content or Secret Material.
- Use Synthetic Fixtures only.
- Fail closed when state is uncertain.

## Current implementation

None.

No `worker.message` runtime package is approved.

No transport, WebSocket, message model, persistence model, Migration, background worker, API, or scheduler behavior is added.

## Approval boundary

No implementation task may begin until CHG-0004 receives explicit project-owner approval.
