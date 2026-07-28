from __future__ import annotations

from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from xianyu_system.core.database import (
    DatabaseResources,
    dispose_database,
    downgrade_database,
    get_current_revision,
    initialize_database,
    upgrade_database,
)
from xianyu_system.worker.publish.domain import (
    ListingDraft,
    ListingDraftLifecycle,
    PublishAuthorizationState,
    PublishDecision,
    PublishDecisionType,
    PublishEvaluationContext,
    PublishReasonCode,
    PublishRequest,
    PublishRequestLifecycle,
    PublishRiskState,
)
from xianyu_system.worker.publish.fingerprint import compute_publish_fingerprint
from xianyu_system.worker.publish.persistence import (
    PublishRepository,
    publish_attempt_snapshot_table,
    publish_audit_event_table,
    publish_request_table,
)
from xianyu_system.worker.publish.service import PublishService

NOW = datetime(2026, 1, 1, tzinfo=UTC)
PUBLISH_REVISION = "0005_xianyu_publish_boundary"
REPLY_REVISION = "0004_xianyu_reply_boundary"
DRAFT_ID = "00000000-0000-4000-8000-000000000101"
REQUEST_ID = "00000000-0000-4000-8000-000000000201"
EVENT_ID = "00000000-0000-4000-8000-000000000301"
PUBLISH_TABLES = {
    "xianyu_publish_requests",
    "xianyu_publish_audit_events",
    "xianyu_publish_attempt_snapshots",
}


def setup_resources(tmp_path: Path) -> DatabaseResources:
    resources = initialize_database(tmp_path / "publish-contract.db")
    upgrade_database(resources)
    return resources


def count_rows(resources: DatabaseResources, table_name: str) -> int:
    with resources.engine.connect() as connection:
        return int(connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())


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


def assert_integrity_failure(resources: DatabaseResources, statement: str, params: dict[str, Any]) -> None:
    with pytest.raises(IntegrityError), resources.engine.begin() as connection:
        connection.execute(text(statement), params)


def test_publish_tables_columns_constraints_and_indexes(tmp_path: Path) -> None:
    assert set(PUBLISH_TABLES) == {
        publish_request_table.name,
        publish_audit_event_table.name,
        publish_attempt_snapshot_table.name,
    }
    for prohibited in ["title", "description", "listing_text", "media_blob", "raw_payload"]:
        assert prohibited not in publish_request_table.c
        assert prohibited not in publish_audit_event_table.c
        assert prohibited not in publish_attempt_snapshot_table.c
    assert "credential" not in " ".join(publish_request_table.c.keys()).lower()

    resources = setup_resources(tmp_path)
    try:
        assert get_current_revision(resources) == PUBLISH_REVISION
        inspector = inspect(resources.engine)
        assert set(inspector.get_table_names()) >= PUBLISH_TABLES
        request_checks = {c["name"] for c in inspector.get_check_constraints("xianyu_publish_requests")}
        attempt_checks = {
            c["name"] for c in inspector.get_check_constraints("xianyu_publish_attempt_snapshots")
        }
        request_indexes = {i["name"] for i in inspector.get_indexes("xianyu_publish_requests")}
        attempt_indexes = {
            i["name"] for i in inspector.get_indexes("xianyu_publish_attempt_snapshots")
        }
        assert "ck_xianyu_publish_request_decision" in request_checks
        assert "ck_xianyu_publish_request_lifecycle" in request_checks
        assert "ck_xianyu_publish_attempt_outcome" in attempt_checks
        assert "ix_xianyu_publish_draft_fingerprint" in request_indexes
        assert "ix_xianyu_publish_attempt_unknown" in attempt_indexes
        for table_name in PUBLISH_TABLES:
            assert inspector.get_foreign_keys(table_name) == []
    finally:
        dispose_database(resources)


def test_repository_flushes_without_commit_and_round_trips_decisions(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        session = resources.session_factory()
        commit_calls = 0

        def count_commit() -> None:
            nonlocal commit_calls
            commit_calls += 1

        session.commit = count_commit
        repository = PublishRepository(session)
        local_draft = draft()
        local_request = request()
        local_context = context()
        fingerprint = compute_publish_fingerprint(local_draft, local_request, local_context)
        decision = PublishDecision(
            decision_type=PublishDecisionType.READY,
            reason_code=PublishReasonCode.READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY,
            draft_id=local_request.draft_id,
            draft_revision=local_request.draft_revision,
            request_id=local_request.request_id,
            idempotency_key=local_request.idempotency_key,
            normalized_fingerprint=fingerprint,
            manual_review_reason=None,
            audit_identifiers=(local_request.request_id,),
        )
        repository.record_decision(
            event_id=EVENT_ID,
            decision=decision,
            request_lifecycle=PublishRequestLifecycle.READY,
            authorization_state=PublishAuthorizationState.AUTHORIZED.value,
            risk_state=PublishRiskState.CLEAR.value,
            synthetic_fixture=True,
            correlation_id="corr-id",
            occurred_at=NOW,
            failure_category=None,
        )

        assert commit_calls == 0
        assert repository.count_requests() == 1
        assert repository.get_by_idempotency_key("idem-key") is not None
        assert repository.get_by_draft_fingerprint(
            draft_id=DRAFT_ID, draft_revision=1, normalized_fingerprint=fingerprint
        ) is not None
        session.rollback()
        session.close()
        assert count_rows(resources, "xianyu_publish_requests") == 0
    finally:
        dispose_database(resources)


def test_service_persists_ready_invalid_and_manual_review_audits(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        service = PublishService(resources.session_factory)
        ready = service.evaluate(draft(), request(), context())
        invalid = service.evaluate(
            draft(draft_id="00000000-0000-4000-8000-000000000102"),
            request(
                request_id="00000000-0000-4000-8000-000000000202",
                draft_id="00000000-0000-4000-8000-000000000102",
                idempotency_key="invalid-key",
                synthetic_fixture=False,
            ),
            context(),
        )
        denied = service.evaluate(
            draft(draft_id="00000000-0000-4000-8000-000000000103"),
            request(
                request_id="00000000-0000-4000-8000-000000000203",
                draft_id="00000000-0000-4000-8000-000000000103",
                idempotency_key="denied-key",
                authorization_state=PublishAuthorizationState.DENIED,
            ),
            context(authorization_state=PublishAuthorizationState.DENIED),
        )

        assert ready.decision_type == PublishDecisionType.READY
        assert invalid.decision_type == PublishDecisionType.INVALID_INPUT
        assert denied.decision_type == PublishDecisionType.UNAUTHORIZED
        assert count_rows(resources, "xianyu_publish_requests") == 1
        assert count_rows(resources, "xianyu_publish_audit_events") == 3
        with resources.engine.connect() as connection:
            audit_columns = connection.execute(text("SELECT * FROM xianyu_publish_audit_events")).mappings().all()
        serialized = " ".join(str(dict(row)) for row in audit_columns).lower()
        for prohibited in ["synthetic title", "synthetic description", "media_metadata"]:
            assert prohibited not in serialized
    finally:
        dispose_database(resources)


def test_database_constraints_enforce_local_invariants(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        base_request = {
            "request_id": REQUEST_ID,
            "draft_id": DRAFT_ID,
            "draft_revision": 1,
            "idempotency_key": "idem-key",
            "normalized_fingerprint": "a" * 64,
            "decision_type": "READY",
            "reason_code": "READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY",
            "request_lifecycle": "READY",
            "authorization_state": "AUTHORIZED",
            "risk_state": "CLEAR",
            "synthetic_fixture": True,
            "correlation_id": "corr-id",
            "occurred_at": NOW.isoformat(),
        }
        insert_request = """
        INSERT INTO xianyu_publish_requests
        (request_id, draft_id, draft_revision, idempotency_key, normalized_fingerprint,
         decision_type, reason_code, request_lifecycle, authorization_state, risk_state,
         synthetic_fixture, correlation_id, occurred_at)
        VALUES
        (:request_id, :draft_id, :draft_revision, :idempotency_key, :normalized_fingerprint,
         :decision_type, :reason_code, :request_lifecycle, :authorization_state, :risk_state,
         :synthetic_fixture, :correlation_id, :occurred_at)
        """
        with resources.engine.begin() as connection:
            connection.execute(text(insert_request), base_request)
        for key, value in [
            ("request_id", "bad"),
            ("draft_id", "bad"),
            ("draft_revision", 0),
            ("idempotency_key", " padded "),
            ("normalized_fingerprint", "short"),
            ("decision_type", "PUBLISHED"),
            ("request_lifecycle", "PUBLISHED"),
        ]:
            params = dict(base_request)
            params["request_id"] = "00000000-0000-4000-8000-000000000401"
            params["idempotency_key"] = "key-" + str(key)
            params[key] = value
            assert_integrity_failure(resources, insert_request, params)

        attempt = {
            "attempt_id": "00000000-0000-4000-8000-000000000501",
            "request_id": REQUEST_ID,
            "draft_id": DRAFT_ID,
            "draft_revision": 1,
            "normalized_fingerprint": "b" * 64,
            "attempt_number": 1,
            "attempt_state": "NOT_STARTED",
            "outcome_type": "UNKNOWN",
            "started_at": NOW.isoformat(),
            "completed_at": None,
            "sanitized_error_code": "UNKNOWN_OUTCOME",
        }
        insert_attempt = """
        INSERT INTO xianyu_publish_attempt_snapshots
        (attempt_id, request_id, draft_id, draft_revision, normalized_fingerprint,
         attempt_number, attempt_state, outcome_type, started_at, completed_at,
         sanitized_error_code)
        VALUES
        (:attempt_id, :request_id, :draft_id, :draft_revision, :normalized_fingerprint,
         :attempt_number, :attempt_state, :outcome_type, :started_at, :completed_at,
         :sanitized_error_code)
        """
        with resources.engine.begin() as connection:
            connection.execute(text(insert_attempt), attempt)
        for key, value in [
            ("attempt_id", "bad"),
            ("attempt_number", 0),
            ("attempt_state", "STARTED"),
            ("outcome_type", "LIVE"),
            ("normalized_fingerprint", "short"),
        ]:
            params = dict(attempt)
            params["attempt_id"] = "00000000-0000-4000-8000-000000000502"
            params[key] = value
            assert_integrity_failure(resources, insert_attempt, params)
    finally:
        dispose_database(resources)


def test_empty_publish_downgrade_and_nonempty_downgrade_fail_closed(tmp_path: Path) -> None:
    resources = setup_resources(tmp_path)
    try:
        downgrade_database(resources, revision=REPLY_REVISION)
        assert get_current_revision(resources) == REPLY_REVISION
        assert PUBLISH_TABLES.isdisjoint(set(inspect(resources.engine).get_table_names()))
        upgrade_database(resources)
        assert get_current_revision(resources) == PUBLISH_REVISION
        service = PublishService(resources.session_factory)
        service.evaluate(draft(), request(), context())
        with pytest.raises(RuntimeError):
            downgrade_database(resources, revision=REPLY_REVISION)
        assert get_current_revision(resources) == PUBLISH_REVISION
        assert count_rows(resources, "xianyu_publish_requests") == 1
    finally:
        dispose_database(resources)
