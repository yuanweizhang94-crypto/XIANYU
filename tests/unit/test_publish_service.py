from __future__ import annotations

import socket
import threading
import time
import uuid
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from xianyu_system.core.database import (
    DatabaseResources,
    dispose_database,
    initialize_database,
    upgrade_database,
)
from xianyu_system.worker.publish.domain import (
    ListingDraft,
    ListingDraftLifecycle,
    PublishAuthorizationState,
    PublishDecisionType,
    PublishEvaluationContext,
    PublishReasonCode,
    PublishRequest,
    PublishRiskState,
)
from xianyu_system.worker.publish.fingerprint import compute_publish_fingerprint
from xianyu_system.worker.publish.service import PublishService

NOW = datetime(2026, 1, 1, tzinfo=UTC)
EVENT_ID = uuid.UUID("00000000-0000-4000-8000-000000000901")
DRAFT_ID = "00000000-0000-4000-8000-000000000101"
REQUEST_ID = "00000000-0000-4000-8000-000000000201"


def draft(**overrides: Any) -> ListingDraft:
    values: dict[str, Any] = {
        "draft_id": DRAFT_ID,
        "revision": 1,
        "title": "synthetic title",
        "description": "synthetic description",
        "category_reference": "synthetic-category",
        "price": Decimal("12.34"),
        "stock": 1,
        "location_reference": "synthetic-location",
        "media_metadata": {"a": "synthetic"},
        "seller_profile_reference": "synthetic-profile",
        "lifecycle_state": ListingDraftLifecycle.VALIDATED,
        "created_at": NOW,
        "updated_at": NOW,
    }
    values.update(overrides)
    return ListingDraft(**values)


def request(**overrides: Any) -> PublishRequest:
    values: dict[str, Any] = {
        "request_id": REQUEST_ID,
        "draft_id": DRAFT_ID,
        "draft_revision": 1,
        "idempotency_key": "idem-key",
        "requested_at": NOW,
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "correlation_id": "corr-id",
    }
    values.update(overrides)
    return PublishRequest(**values)


def context(**overrides: Any) -> PublishEvaluationContext:
    values: dict[str, Any] = {
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "request_time": NOW,
        "local_profile_reference": "synthetic-profile",
    }
    values.update(overrides)
    return PublishEvaluationContext(**values)


def setup_resources(tmp_path: Path) -> DatabaseResources:
    resources = initialize_database(tmp_path / "publish-service.db")
    upgrade_database(resources)
    return resources


def count_rows(resources: DatabaseResources, table_name: str) -> int:
    with resources.engine.connect() as connection:
        return int(connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())


class TrackingSession:
    def __init__(self, wrapped: Session) -> None:
        self.wrapped = wrapped
        self.commit_calls = 0
        self.rollback_calls = 0
        self.close_calls = 0

    def __getattr__(self, name: str) -> Any:
        return getattr(self.wrapped, name)

    def commit(self) -> None:
        self.commit_calls += 1
        self.wrapped.commit()

    def rollback(self) -> None:
        self.rollback_calls += 1
        self.wrapped.rollback()

    def close(self) -> None:
        self.close_calls += 1
        self.wrapped.close()


class BrokenFlushSession:
    def __init__(self) -> None:
        self.rollback_calls = 0
        self.close_calls = 0
        self.commit_calls = 0

    def add(self, _value: object) -> None:
        return None

    def flush(self) -> None:
        raise SQLAlchemyError("forced synthetic persistence failure")

    def rollback(self) -> None:
        self.rollback_calls += 1

    def close(self) -> None:
        self.close_calls += 1

    def commit(self) -> None:
        self.commit_calls += 1


def test_invalid_object_shape_returns_invalid_without_session() -> None:
    service = PublishService(lambda: pytest.fail("session must not be opened"))

    decision = service.evaluate(object(), request(), context())

    assert decision.decision_type == PublishDecisionType.INVALID_INPUT
    assert decision.reason_code == PublishReasonCode.MISSING_REQUIRED_FIELD


def test_ready_persists_local_request_and_audit_without_attempt_or_platform(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    resources = setup_resources(tmp_path)
    tracking: TrackingSession | None = None
    before_threads = sorted(thread.name for thread in threading.enumerate())
    connect_attempts: list[object] = []

    def session_factory() -> TrackingSession:
        nonlocal tracking
        tracking = TrackingSession(resources.session_factory())
        return tracking

    def fail_connect(self: socket.socket, address: object) -> None:
        connect_attempts.append(address)
        raise AssertionError(f"network attempted: {address!r}")

    def fail_sleep(seconds: float) -> None:
        raise AssertionError(f"sleep attempted: {seconds}")

    monkeypatch.setattr(socket.socket, "connect", fail_connect)
    monkeypatch.setattr(time, "sleep", fail_sleep)
    try:
        decision = PublishService(
            session_factory,
            identifier_factory=lambda: EVENT_ID,
            clock=lambda: NOW,
        ).evaluate(draft(), request(), context())

        assert decision.decision_type == PublishDecisionType.READY
        assert decision.reason_code == PublishReasonCode.READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY
        assert decision.normalized_fingerprint is not None
        assert count_rows(resources, "xianyu_publish_requests") == 1
        assert count_rows(resources, "xianyu_publish_audit_events") == 1
        assert count_rows(resources, "xianyu_publish_attempt_snapshots") == 0
        assert tracking is not None
        assert tracking.commit_calls == 1
        assert tracking.rollback_calls == 0
        assert tracking.close_calls == 1
        with resources.engine.connect() as connection:
            request_row = connection.execute(text("SELECT * FROM xianyu_publish_requests")).mappings().one()
            audit_row = connection.execute(text("SELECT * FROM xianyu_publish_audit_events")).mappings().one()
        assert request_row["decision_type"] == "READY"
        assert request_row["reason_code"] == "READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY"
        assert audit_row["event_id"] == str(EVENT_ID)
        assert str(audit_row["occurred_at"]).startswith("2026-01-01")
        assert connect_attempts == []
        assert sorted(thread.name for thread in threading.enumerate()) == before_threads
    finally:
        dispose_database(resources)


def test_idempotency_replay_does_not_create_request_attempt_or_overwrite(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        service = PublishService(resources.session_factory, identifier_factory=lambda: EVENT_ID, clock=lambda: NOW)
        first = service.evaluate(draft(), request(), context())
        replay = service.evaluate(
            draft(),
            request(request_id="00000000-0000-4000-8000-000000000202"),
            context(),
        )

        assert first.decision_type == PublishDecisionType.READY
        assert replay.reason_code == PublishReasonCode.IDEMPOTENCY_REPLAY
        assert replay.normalized_fingerprint == first.normalized_fingerprint
        assert count_rows(resources, "xianyu_publish_requests") == 1
        assert count_rows(resources, "xianyu_publish_attempt_snapshots") == 0
    finally:
        dispose_database(resources)


def test_idempotency_conflict_does_not_overwrite_existing_request(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        service = PublishService(resources.session_factory)
        first = service.evaluate(draft(), request(), context())
        conflict = service.evaluate(
            draft(title="changed title"),
            request(request_id="00000000-0000-4000-8000-000000000203"),
            context(),
        )

        assert conflict.decision_type == PublishDecisionType.CONFLICT
        assert conflict.reason_code == PublishReasonCode.IDEMPOTENCY_CONFLICT
        assert count_rows(resources, "xianyu_publish_requests") == 1
        with resources.engine.connect() as connection:
            stored = connection.execute(
                text("SELECT normalized_fingerprint FROM xianyu_publish_requests")
            ).scalar_one()
        assert stored == first.normalized_fingerprint
    finally:
        dispose_database(resources)


def test_duplicate_draft_fingerprint_does_not_create_attempt(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        service = PublishService(resources.session_factory)
        service.evaluate(draft(), request(), context())
        duplicate = service.evaluate(
            draft(),
            request(
                request_id="00000000-0000-4000-8000-000000000204",
                idempotency_key="different-key",
            ),
            context(),
        )

        assert duplicate.decision_type == PublishDecisionType.DUPLICATE
        assert duplicate.reason_code == PublishReasonCode.DUPLICATE_DRAFT
        assert count_rows(resources, "xianyu_publish_requests") == 1
        assert count_rows(resources, "xianyu_publish_attempt_snapshots") == 0
    finally:
        dispose_database(resources)


def test_unknown_historical_outcome_requires_manual_review_without_retry(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    unknown_draft = draft(draft_id="00000000-0000-4000-8000-000000000105")
    unknown_request = request(
        request_id="00000000-0000-4000-8000-000000000205",
        draft_id=unknown_draft.draft_id,
        idempotency_key="unknown-key",
    )
    unknown_context = context()
    fingerprint = compute_publish_fingerprint(unknown_draft, unknown_request, unknown_context)
    try:
        with resources.engine.begin() as connection:
            connection.execute(
                text(
                    "INSERT INTO xianyu_publish_attempt_snapshots "
                    "(attempt_id, request_id, draft_id, draft_revision, normalized_fingerprint, "
                    "attempt_number, attempt_state, outcome_type, started_at, completed_at, "
                    "sanitized_error_code) "
                    "VALUES (:attempt_id, :request_id, :draft_id, 1, :fingerprint, 1, "
                    "'COMPLETED', 'UNKNOWN', :started_at, :completed_at, 'UNKNOWN_OUTCOME')"
                ),
                {
                    "attempt_id": "00000000-0000-4000-8000-000000000305",
                    "request_id": "00000000-0000-4000-8000-000000000999",
                    "draft_id": unknown_draft.draft_id,
                    "fingerprint": fingerprint,
                    "started_at": NOW.isoformat(),
                    "completed_at": NOW.isoformat(),
                },
            )
        decision = PublishService(resources.session_factory).evaluate(
            unknown_draft, unknown_request, unknown_context
        )

        assert decision.decision_type == PublishDecisionType.MANUAL_REVIEW
        assert decision.reason_code == PublishReasonCode.UNKNOWN_PREVIOUS_OUTCOME
        assert count_rows(resources, "xianyu_publish_attempt_snapshots") == 1
        assert count_rows(resources, "xianyu_publish_requests") == 1
    finally:
        dispose_database(resources)


def test_persistence_failure_rolls_back_closes_and_never_returns_ready() -> None:
    broken = BrokenFlushSession()
    service = PublishService(lambda: broken)

    decision = service.evaluate(
        draft(), request(synthetic_fixture=False), context(synthetic_fixture=True)
    )

    assert decision.decision_type == PublishDecisionType.MANUAL_REVIEW
    assert decision.reason_code == PublishReasonCode.MANUAL_REVIEW_REQUIRED
    assert broken.rollback_calls == 1
    assert broken.close_calls == 1
    assert broken.commit_calls == 0


def test_session_is_rolled_back_and_closed_for_replay_conflict_and_duplicate(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    sessions: list[TrackingSession] = []

    def session_factory() -> TrackingSession:
        session = TrackingSession(resources.session_factory())
        sessions.append(session)
        return session

    try:
        service = PublishService(session_factory)
        service.evaluate(draft(), request(), context())
        service.evaluate(draft(), request(request_id="00000000-0000-4000-8000-000000000206"), context())
        service.evaluate(
            draft(title="changed title"),
            request(request_id="00000000-0000-4000-8000-000000000207"),
            context(),
        )
        service.evaluate(
            draft(),
            request(
                request_id="00000000-0000-4000-8000-000000000208",
                idempotency_key="duplicate-key",
            ),
            context(),
        )

        assert [session.commit_calls for session in sessions] == [1, 0, 0, 0]
        assert [session.rollback_calls for session in sessions] == [0, 1, 1, 1]
        assert [session.close_calls for session in sessions] == [1, 1, 1, 1]
    finally:
        dispose_database(resources)


def test_service_has_no_platform_or_scheduler_surface() -> None:
    source = Path("app/xianyu_system/worker/publish/service.py").read_text(encoding="utf-8")
    forbidden = [
        "platform_adapter",
        "xianyu_client",
        "publish_listing",
        "upload_media",
        "scheduler",
        "login",
        "Thread(",
        "sleep(",
    ]
    for marker in forbidden:
        assert marker not in source
