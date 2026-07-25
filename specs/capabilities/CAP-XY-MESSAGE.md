# CAP-XY-MESSAGE

## Purpose

Define the local synthetic Xianyu message receiving boundary without opening a real WebSocket or connecting to any external platform.

## Current implementation change

Active change: CHG-0004-xianyu-message-boundary.

Registry status: implementing.

Last verified commit: unset until T8 complete verification.

The local boundary has been implemented by CHG-0004 T6 and covered by CHG-0004 T7. T8 registers these exact evidence paths as the Evidence Candidate before complete verification.

## Registered implementation paths

- `app/xianyu_system/worker/message/__init__.py`
- `app/xianyu_system/worker/message/domain.py`
- `app/xianyu_system/worker/message/transport.py`
- `app/xianyu_system/worker/message/service.py`
- `app/xianyu_system/worker/message/persistence.py`
- `app/xianyu_system/worker/message/worker.py`
- `migrations/versions/0003_xianyu_message_boundary.py`

## Registered verification paths

- `tests/unit/test_message_domain.py`
- `tests/unit/test_message_service.py`
- `tests/unit/test_message_worker.py`
- `tests/unit/test_import_safety.py`
- `tests/contract/test_message_persistence.py`
- `tests/contract/test_message_security.py`
- `tests/contract/test_migrations.py`
- `tests/contract/test_core_runtime.py`
- `tests/contract/test_capability_registry.py`
- `changes/active/CHG-0004-xianyu-message-boundary/tests/test_acceptance.py`

## Implemented local boundary

- Conversation is local, Profile-scoped, and Account-scoped.
- Message Record is local, append-only for approved receipt outcomes, and Profile-scoped.
- Delivery Attempt records local receipt attempts without external acknowledgements.
- Profile and Account scope are enforced before processing.
- Deduplication decisions are `NEW`, `DUPLICATE`, `INDETERMINATE`, and `CONFLICT`.
- `NEW` creates one Conversation, Message Record, and Delivery Attempt as needed.
- `DUPLICATE` reuses the existing Message Record and records another Delivery Attempt.
- `INDETERMINATE` creates a separate Message Record rather than silently discarding input.
- `CONFLICT` fails closed and rolls back without overwriting existing data.
- Message Service owns transaction commit and rollback.
- Repository methods flush without committing.
- The Worker is synchronous and requires explicit start and stop.
- Migration 0003 defines the approved local Message tables.

## T8 evidence candidate

The capability remains implementing.

last_verified_commit remains unset.

The Candidate SHA will be the commit that registers these exact evidence paths.

A separate verification-record commit will record that Candidate SHA after complete verification.

## Requirements

- Preserve exactly seven implementation paths and ten verification paths.
- Keep every path repository-relative, concrete, safe, duplicate-free, and existing.
- Keep the local boundary synthetic and Profile-scoped.
- Keep permanent Message test count at 42.
- Keep full collection at 322.

## Failure behavior

- Stop when permission, credential, specification, verification, or risk state is uncertain.
- Do not mark the capability verified until complete verification and Candidate CI pass.
- Do not set last_verified_commit before the verification-record phase.
- Do not guess missing business behavior.

## Security boundaries

- Do not hold real Cookie, Token, Secret, customer data, or browser credentials.
- Do not bypass platform verification or risk controls.
- Do not open a real WebSocket, network connection, browser Profile, or real account session.
- Do not send messages, create automatic replies, schedule processing, expose an API, or expose a Web UI.

## Out of scope

- real WebSocket
- real network
- real account access
- Cookie/Token/Secret handling
- browser Profile
- message sending
- automatic reply
- Scheduler
- API
- Web UI
- background processing thread
- automatic reconnect
- automatic processing retry

## Verification

- Registry status is implementing in the Evidence Candidate.
- active_change is `CHG-0004-xianyu-message-boundary` in the Evidence Candidate.
- last_verified_commit remains unset until T8 complete verification succeeds.
- Complete verification must run on the committed Candidate SHA.
- GitHub Actions must pass for the Candidate before verification is recorded.
