"""SQLAlchemy persistence for local deterministic Schedule facts."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, cast

from sqlalchemy import Boolean, CheckConstraint, Column, DateTime, Index, Integer, String, Table, func, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from xianyu_system.core.database import Base
from xianyu_system.schedule.domain import (
    ScheduleDecision,
    ScheduleDispatchOutcome,
    ScheduleDispatchResult,
    ScheduleLifecycle,
    SchedulePersistenceError,
)

schedule_request_table = Table(
    "xianyu_schedule_requests",
    Base.metadata,
    Column("schedule_id", String(36), primary_key=True, nullable=False),
    Column("publish_request_id", String(36), nullable=False),
    Column("idempotency_key", String(128), nullable=False, unique=True),
    Column("trigger_type", String(16), nullable=False),
    Column("lifecycle", String(32), nullable=False),
    Column("normalized_fingerprint", String(64), nullable=False),
    Column("requested_at", DateTime(timezone=True), nullable=False),
    Column("due_at", DateTime(timezone=True), nullable=False),
    Column("misfire_grace_seconds", Integer, nullable=False),
    Column("synthetic_fixture", Boolean, nullable=False),
    Column("correlation_id", String(128), nullable=True),
    Column("claimed_at", DateTime(timezone=True), nullable=True),
    Column("completed_at", DateTime(timezone=True), nullable=True),
    Column("reason", String(256), nullable=True),
    CheckConstraint("length(schedule_id) = 36", name="ck_xianyu_schedule_id_len"),
    CheckConstraint("length(publish_request_id) = 36", name="ck_xianyu_schedule_publish_id_len"),
    CheckConstraint(
        "idempotency_key = trim(idempotency_key) AND length(idempotency_key) >= 1 AND length(idempotency_key) <= 128",
        name="ck_xianyu_schedule_idempotency_len",
    ),
    CheckConstraint("trigger_type IN ('IMMEDIATE','RUN_AT_UTC')", name="ck_xianyu_schedule_trigger"),
    CheckConstraint(
        "lifecycle IN ('PENDING','CLAIMED','DISPATCHED','CANCELLED','MISFIRED','FAILED','NEEDS_MANUAL_REVIEW')",
        name="ck_xianyu_schedule_lifecycle",
    ),
    CheckConstraint("length(normalized_fingerprint) = 64", name="ck_xianyu_schedule_fingerprint_len"),
    CheckConstraint("misfire_grace_seconds >= 0 AND misfire_grace_seconds <= 3600", name="ck_xianyu_schedule_grace_range"),
    extend_existing=True,
)

schedule_audit_event_table = Table(
    "xianyu_schedule_audit_events",
    Base.metadata,
    Column("event_id", String(36), primary_key=True, nullable=False),
    Column("schedule_id", String(36), nullable=False),
    Column("event_type", String(32), nullable=False),
    Column("occurred_at", DateTime(timezone=True), nullable=False),
    Column("from_lifecycle", String(32), nullable=True),
    Column("to_lifecycle", String(32), nullable=False),
    Column("reason", String(256), nullable=True),
    CheckConstraint("length(event_id) = 36", name="ck_xianyu_schedule_audit_id_len"),
    CheckConstraint("length(schedule_id) = 36", name="ck_xianyu_schedule_audit_schedule_id_len"),
    CheckConstraint(
        "event_type = trim(event_type) AND length(event_type) >= 1 AND length(event_type) <= 32",
        name="ck_xianyu_schedule_audit_event_type_len",
    ),
    extend_existing=True,
)

Index("ix_xianyu_schedule_due_pending", schedule_request_table.c.lifecycle, schedule_request_table.c.due_at)
Index("ix_xianyu_schedule_publish", schedule_request_table.c.publish_request_id)


class _ScheduleRequestRecord:
    schedule_id: str
    publish_request_id: str
    idempotency_key: str
    trigger_type: str
    lifecycle: str
    normalized_fingerprint: str
    requested_at: datetime
    due_at: datetime
    misfire_grace_seconds: int
    synthetic_fixture: bool
    correlation_id: str | None
    claimed_at: datetime | None
    completed_at: datetime | None
    reason: str | None


class _ScheduleAuditEventRecord:
    event_id: str
    schedule_id: str
    event_type: str
    occurred_at: datetime
    from_lifecycle: str | None
    to_lifecycle: str
    reason: str | None


Base.registry.map_imperatively(_ScheduleRequestRecord, schedule_request_table)
Base.registry.map_imperatively(_ScheduleAuditEventRecord, schedule_audit_event_table)


@dataclass(frozen=True, slots=True)
class StoredSchedule:
    schedule_id: str
    publish_request_id: str
    idempotency_key: str
    lifecycle: ScheduleLifecycle
    normalized_fingerprint: str
    due_at: datetime
    misfire_grace_seconds: int


def _stored(record: _ScheduleRequestRecord) -> StoredSchedule:
    return StoredSchedule(
        schedule_id=record.schedule_id,
        publish_request_id=record.publish_request_id,
        idempotency_key=record.idempotency_key,
        lifecycle=ScheduleLifecycle(record.lifecycle),
        normalized_fingerprint=record.normalized_fingerprint,
        due_at=_as_utc(record.due_at),
        misfire_grace_seconds=record.misfire_grace_seconds,
    )


def _as_utc(value: datetime) -> datetime:
    if value.tzinfo is None:
        return value.replace(tzinfo=UTC)
    return value.astimezone(UTC)


class ScheduleRepository:
    """Concrete repository participating in caller-owned Sessions."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def get_by_idempotency_key(self, idempotency_key: str) -> StoredSchedule | None:
        try:
            record = self._session.scalars(select(_ScheduleRequestRecord).where(schedule_request_table.c.idempotency_key == idempotency_key)).first()
        except SQLAlchemyError:
            raise SchedulePersistenceError("Schedule persistence operation failed.") from None
        return None if record is None else _stored(record)

    def add_schedule(self, *, event_id: str, decision: ScheduleDecision, request_values: dict[str, Any], occurred_at: datetime) -> None:
        try:
            record = _ScheduleRequestRecord()
            for key, value in request_values.items():
                setattr(record, key, value)
            self._session.add(record)
            self._add_audit(event_id=event_id, schedule_id=decision.schedule_id, event_type="SCHEDULE_ACCEPTED", occurred_at=occurred_at, from_lifecycle=None, to_lifecycle=ScheduleLifecycle.PENDING, reason=decision.reason)
            self._session.flush()
        except SQLAlchemyError:
            raise SchedulePersistenceError("Schedule persistence operation failed.") from None

    def cancel_pending(self, *, event_id: str, schedule_id: str, occurred_at: datetime, reason: str) -> ScheduleDispatchResult:
        try:
            result = cast(
                Any,
                self._session.execute(
                update(schedule_request_table)
                .where(schedule_request_table.c.schedule_id == schedule_id, schedule_request_table.c.lifecycle == ScheduleLifecycle.PENDING.value)
                .values(lifecycle=ScheduleLifecycle.CANCELLED.value, completed_at=occurred_at, reason=reason)
                ),
            )
            if result.rowcount != 1:
                return ScheduleDispatchResult(schedule_id, ScheduleDispatchOutcome.NOT_FOUND, None, reason="not pending")
            self._add_audit(event_id=event_id, schedule_id=schedule_id, event_type="SCHEDULE_CANCELLED", occurred_at=occurred_at, from_lifecycle=ScheduleLifecycle.PENDING, to_lifecycle=ScheduleLifecycle.CANCELLED, reason=reason)
            self._session.flush()
            return ScheduleDispatchResult(schedule_id, ScheduleDispatchOutcome.CANCELLED, ScheduleLifecycle.CANCELLED, reason=reason)
        except SQLAlchemyError:
            raise SchedulePersistenceError("Schedule persistence operation failed.") from None

    def claim_due(self, *, event_id: str, schedule_id: str, now: datetime) -> StoredSchedule | None:
        try:
            record = self._session.scalars(select(_ScheduleRequestRecord).where(schedule_request_table.c.schedule_id == schedule_id)).first()
            now_utc = _as_utc(now)
            if record is None or record.lifecycle != ScheduleLifecycle.PENDING.value or _as_utc(record.due_at) > now_utc:
                return None
            result = cast(
                Any,
                self._session.execute(
                update(schedule_request_table)
                .where(schedule_request_table.c.schedule_id == schedule_id, schedule_request_table.c.lifecycle == ScheduleLifecycle.PENDING.value, schedule_request_table.c.due_at <= now_utc)
                .values(lifecycle=ScheduleLifecycle.CLAIMED.value, claimed_at=now_utc)
                ),
            )
            if result.rowcount != 1:
                return None
            self._add_audit(event_id=event_id, schedule_id=schedule_id, event_type="SCHEDULE_CLAIMED", occurred_at=now, from_lifecycle=ScheduleLifecycle.PENDING, to_lifecycle=ScheduleLifecycle.CLAIMED, reason=None)
            self._session.flush()
            stored = _stored(record)
            return StoredSchedule(
                schedule_id=stored.schedule_id,
                publish_request_id=stored.publish_request_id,
                idempotency_key=stored.idempotency_key,
                lifecycle=ScheduleLifecycle.CLAIMED,
                normalized_fingerprint=stored.normalized_fingerprint,
                due_at=stored.due_at,
                misfire_grace_seconds=stored.misfire_grace_seconds,
            )
        except SQLAlchemyError:
            raise SchedulePersistenceError("Schedule persistence operation failed.") from None

    def complete_claimed(self, *, event_id: str, schedule_id: str, lifecycle: ScheduleLifecycle, occurred_at: datetime, reason: str | None) -> None:
        try:
            self._session.execute(
                update(schedule_request_table)
                .where(schedule_request_table.c.schedule_id == schedule_id, schedule_request_table.c.lifecycle == ScheduleLifecycle.CLAIMED.value)
                .values(lifecycle=lifecycle.value, completed_at=occurred_at, reason=reason)
            )
            self._add_audit(event_id=event_id, schedule_id=schedule_id, event_type="SCHEDULE_COMPLETED", occurred_at=occurred_at, from_lifecycle=ScheduleLifecycle.CLAIMED, to_lifecycle=lifecycle, reason=reason)
            self._session.flush()
        except SQLAlchemyError:
            raise SchedulePersistenceError("Schedule persistence operation failed.") from None

    def count_schedules(self) -> int:
        return cast(int, self._session.scalar(select(func.count()).select_from(schedule_request_table)))

    def _add_audit(self, *, event_id: str, schedule_id: str, event_type: str, occurred_at: datetime, from_lifecycle: ScheduleLifecycle | None, to_lifecycle: ScheduleLifecycle, reason: str | None) -> None:
        audit = _ScheduleAuditEventRecord()
        values = {
            "event_id": event_id,
            "schedule_id": schedule_id,
            "event_type": event_type,
            "occurred_at": occurred_at,
            "from_lifecycle": None if from_lifecycle is None else from_lifecycle.value,
            "to_lifecycle": to_lifecycle.value,
            "reason": reason,
        }
        for key, value in values.items():
            setattr(audit, key, value)
        self._session.add(audit)
