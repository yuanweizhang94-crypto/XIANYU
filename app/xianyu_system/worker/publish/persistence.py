"""SQLAlchemy projection and Repository for the local Publish boundary."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, cast

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Index, Integer, String, Table, func, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from xianyu_system.core.database import Base
from xianyu_system.worker.publish.domain import (
    PublishDecision,
    PublishDecisionType,
    PublishFailureCategory,
    PublishOutcomeType,
    PublishPersistenceError,
    PublishReasonCode,
    PublishRequestLifecycle,
)

publish_request_table = Table(
    "xianyu_publish_requests",
    Base.metadata,
    Column("request_id", String(36), primary_key=True, nullable=False),
    Column("draft_id", String(36), nullable=False),
    Column("draft_revision", Integer, nullable=False),
    Column("idempotency_key", String(128), nullable=False, unique=True),
    Column("normalized_fingerprint", String(64), nullable=False),
    Column("decision_type", String(32), nullable=False),
    Column("reason_code", String(64), nullable=False),
    Column("request_lifecycle", String(32), nullable=False),
    Column("authorization_state", String(16), nullable=False),
    Column("risk_state", String(16), nullable=False),
    Column("synthetic_fixture", Boolean, nullable=False),
    Column("correlation_id", String(128), nullable=True),
    Column("occurred_at", DateTime(timezone=True), nullable=False),
    CheckConstraint("length(request_id) = 36", name="ck_xianyu_publish_request_id_len"),
    CheckConstraint("length(draft_id) = 36", name="ck_xianyu_publish_request_draft_id_len"),
    CheckConstraint("draft_revision >= 1", name="ck_xianyu_publish_request_revision_positive"),
    CheckConstraint(
        "idempotency_key = trim(idempotency_key) AND "
        "length(idempotency_key) >= 1 AND length(idempotency_key) <= 128",
        name="ck_xianyu_publish_request_idempotency_len",
    ),
    CheckConstraint("length(normalized_fingerprint) = 64", name="ck_xianyu_publish_fingerprint_len"),
    CheckConstraint(
        "decision_type IN ('READY','INVALID_INPUT','UNAUTHORIZED','RISK_BLOCKED','DUPLICATE','CONFLICT','MANUAL_REVIEW')",
        name="ck_xianyu_publish_request_decision",
    ),
    CheckConstraint(
        "request_lifecycle IN ('RECEIVED','VALIDATED','REJECTED','READY','DUPLICATE','CONFLICT','MANUAL_REVIEW')",
        name="ck_xianyu_publish_request_lifecycle",
    ),
    extend_existing=True,
)

publish_audit_event_table = Table(
    "xianyu_publish_audit_events",
    Base.metadata,
    Column("event_id", String(36), primary_key=True, nullable=False),
    Column("event_type", String(32), nullable=False),
    Column("occurred_at", DateTime(timezone=True), nullable=False),
    Column("request_id", String(36), nullable=False),
    Column("draft_id", String(36), nullable=False),
    Column("draft_revision", Integer, nullable=False),
    Column("decision_type", String(32), nullable=False),
    Column("reason_code", String(64), nullable=False),
    Column("failure_category", String(64), nullable=True),
    Column("correlation_id", String(128), nullable=True),
    Column("synthetic_fixture", Boolean, nullable=False),
    CheckConstraint("length(event_id) = 36", name="ck_xianyu_publish_audit_id_len"),
    CheckConstraint("length(request_id) = 36", name="ck_xianyu_publish_audit_request_id_len"),
    CheckConstraint("length(draft_id) = 36", name="ck_xianyu_publish_audit_draft_id_len"),
    CheckConstraint("draft_revision >= 1", name="ck_xianyu_publish_audit_revision_positive"),
    CheckConstraint(
        "event_type = trim(event_type) AND length(event_type) >= 1 AND length(event_type) <= 32",
        name="ck_xianyu_publish_audit_event_type_len",
    ),
    extend_existing=True,
)

publish_attempt_snapshot_table = Table(
    "xianyu_publish_attempt_snapshots",
    Base.metadata,
    Column("attempt_id", String(36), primary_key=True, nullable=False),
    Column("request_id", String(36), nullable=False),
    Column("draft_id", String(36), nullable=False),
    Column("draft_revision", Integer, nullable=False),
    Column("normalized_fingerprint", String(64), nullable=False),
    Column("attempt_number", Integer, nullable=False),
    Column("attempt_state", String(16), nullable=False),
    Column("outcome_type", String(16), nullable=False),
    Column("started_at", DateTime(timezone=True), nullable=False),
    Column("completed_at", DateTime(timezone=True), nullable=True),
    Column("sanitized_error_code", String(64), nullable=True),
    CheckConstraint("length(attempt_id) = 36", name="ck_xianyu_publish_attempt_id_len"),
    CheckConstraint("length(request_id) = 36", name="ck_xianyu_publish_attempt_request_id_len"),
    CheckConstraint("length(draft_id) = 36", name="ck_xianyu_publish_attempt_draft_id_len"),
    CheckConstraint("draft_revision >= 1", name="ck_xianyu_publish_attempt_revision_positive"),
    CheckConstraint("length(normalized_fingerprint) = 64", name="ck_xianyu_publish_attempt_fingerprint_len"),
    CheckConstraint("attempt_number >= 1", name="ck_xianyu_publish_attempt_number_positive"),
    CheckConstraint(
        "attempt_state IN ('NOT_STARTED','IN_PROGRESS','COMPLETED')",
        name="ck_xianyu_publish_attempt_state",
    ),
    CheckConstraint(
        "outcome_type IN ('SUCCEEDED','FAILED','UNKNOWN','CANCELLED')",
        name="ck_xianyu_publish_attempt_outcome",
    ),
    extend_existing=True,
)

Index(
    "ix_xianyu_publish_draft_fingerprint",
    publish_request_table.c.draft_id,
    publish_request_table.c.draft_revision,
    publish_request_table.c.normalized_fingerprint,
)
Index(
    "ix_xianyu_publish_attempt_unknown",
    publish_attempt_snapshot_table.c.draft_id,
    publish_attempt_snapshot_table.c.draft_revision,
    publish_attempt_snapshot_table.c.normalized_fingerprint,
    publish_attempt_snapshot_table.c.outcome_type,
)


class _PublishRequestRecord:
    request_id: str
    draft_id: str
    draft_revision: int
    idempotency_key: str
    normalized_fingerprint: str
    decision_type: str
    reason_code: str
    request_lifecycle: str
    authorization_state: str
    risk_state: str
    synthetic_fixture: bool
    correlation_id: str | None
    occurred_at: datetime


class _PublishAuditEventRecord:
    event_id: str
    event_type: str
    occurred_at: datetime
    request_id: str
    draft_id: str
    draft_revision: int
    decision_type: str
    reason_code: str
    failure_category: str | None
    correlation_id: str | None
    synthetic_fixture: bool


class _PublishAttemptSnapshotRecord:
    attempt_id: str
    request_id: str
    draft_id: str
    draft_revision: int
    normalized_fingerprint: str
    attempt_number: int
    attempt_state: str
    outcome_type: str
    started_at: datetime
    completed_at: datetime | None
    sanitized_error_code: str | None


Base.registry.map_imperatively(_PublishRequestRecord, publish_request_table)
Base.registry.map_imperatively(_PublishAuditEventRecord, publish_audit_event_table)
Base.registry.map_imperatively(_PublishAttemptSnapshotRecord, publish_attempt_snapshot_table)


@dataclass(frozen=True, slots=True)
class StoredPublishDecision:
    request_id: str
    idempotency_key: str
    draft_id: str
    draft_revision: int
    normalized_fingerprint: str
    decision_type: PublishDecisionType
    reason_code: PublishReasonCode


def _stored(record: _PublishRequestRecord) -> StoredPublishDecision:
    return StoredPublishDecision(
        request_id=record.request_id,
        idempotency_key=record.idempotency_key,
        draft_id=record.draft_id,
        draft_revision=record.draft_revision,
        normalized_fingerprint=record.normalized_fingerprint,
        decision_type=PublishDecisionType(record.decision_type),
        reason_code=PublishReasonCode(record.reason_code),
    )


class PublishRepository:
    """Concrete Repository participating in caller-owned Sessions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_idempotency_key(self, idempotency_key: str) -> StoredPublishDecision | None:
        try:
            record = self._session.scalars(
                select(_PublishRequestRecord).where(
                    publish_request_table.c.idempotency_key == idempotency_key
                )
            ).first()
        except SQLAlchemyError:
            raise PublishPersistenceError("Publish persistence operation failed.") from None
        return None if record is None else _stored(record)

    def get_by_draft_fingerprint(
        self,
        *,
        draft_id: str,
        draft_revision: int,
        normalized_fingerprint: str,
    ) -> StoredPublishDecision | None:
        try:
            record = self._session.scalars(
                select(_PublishRequestRecord).where(
                    publish_request_table.c.draft_id == draft_id,
                    publish_request_table.c.draft_revision == draft_revision,
                    publish_request_table.c.normalized_fingerprint == normalized_fingerprint,
                )
            ).first()
        except SQLAlchemyError:
            raise PublishPersistenceError("Publish persistence operation failed.") from None
        return None if record is None else _stored(record)

    def has_unknown_outcome(
        self,
        *,
        draft_id: str,
        draft_revision: int,
        normalized_fingerprint: str,
    ) -> bool:
        try:
            record = self._session.scalars(
                select(_PublishAttemptSnapshotRecord).where(
                    publish_attempt_snapshot_table.c.draft_id == draft_id,
                    publish_attempt_snapshot_table.c.draft_revision == draft_revision,
                    publish_attempt_snapshot_table.c.normalized_fingerprint == normalized_fingerprint,
                    publish_attempt_snapshot_table.c.outcome_type == PublishOutcomeType.UNKNOWN.value,
                )
            ).first()
        except SQLAlchemyError:
            raise PublishPersistenceError("Publish persistence operation failed.") from None
        return record is not None

    def record_decision(
        self,
        *,
        event_id: str,
        decision: PublishDecision,
        request_lifecycle: PublishRequestLifecycle,
        authorization_state: str,
        risk_state: str,
        synthetic_fixture: bool,
        correlation_id: str | None,
        occurred_at: datetime,
        failure_category: PublishFailureCategory | None,
    ) -> None:
        try:
            if decision.normalized_fingerprint is not None:
                request_record = _PublishRequestRecord()
                values: dict[str, Any] = {
                    "request_id": decision.request_id,
                    "draft_id": decision.draft_id,
                    "draft_revision": decision.draft_revision,
                    "idempotency_key": decision.idempotency_key,
                    "normalized_fingerprint": decision.normalized_fingerprint,
                    "decision_type": decision.decision_type.value,
                    "reason_code": decision.reason_code.value,
                    "request_lifecycle": request_lifecycle.value,
                    "authorization_state": authorization_state,
                    "risk_state": risk_state,
                    "synthetic_fixture": synthetic_fixture,
                    "correlation_id": correlation_id,
                    "occurred_at": occurred_at,
                }
                for key, value in values.items():
                    setattr(request_record, key, value)
                self._session.add(request_record)

            audit_record = _PublishAuditEventRecord()
            audit_values = {
                "event_id": event_id,
                "event_type": "DECISION_RECORDED",
                "occurred_at": occurred_at,
                "request_id": decision.request_id,
                "draft_id": decision.draft_id,
                "draft_revision": decision.draft_revision,
                "decision_type": decision.decision_type.value,
                "reason_code": decision.reason_code.value,
                "failure_category": None if failure_category is None else failure_category.value,
                "correlation_id": correlation_id,
                "synthetic_fixture": synthetic_fixture,
            }
            for key, value in audit_values.items():
                setattr(audit_record, key, value)
            self._session.add(audit_record)
            self._session.flush()
        except SQLAlchemyError:
            raise PublishPersistenceError("Publish persistence operation failed.") from None

    def count_requests(self) -> int:
        return cast(int, self._session.scalar(select(func.count()).select_from(publish_request_table)))
