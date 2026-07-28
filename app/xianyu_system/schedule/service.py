"""Application service for local deterministic one-time Schedule dispatch."""

from __future__ import annotations

import uuid
from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from typing import Any, cast
from uuid import UUID

from sqlalchemy.orm import Session

from xianyu_system.schedule.domain import (
    ScheduleDecision,
    ScheduleDecisionType,
    ScheduleDispatchOutcome,
    ScheduleDispatchResult,
    ScheduleLifecycle,
    SchedulePersistenceError,
    ScheduleRequest,
)
from xianyu_system.schedule.fingerprint import compute_schedule_fingerprint
from xianyu_system.schedule.persistence import ScheduleRepository
from xianyu_system.schedule.validation import ScheduleValidator
from xianyu_system.worker.publish.domain import (
    ListingDraft,
    PublishDecisionType,
    PublishEvaluationContext,
    PublishRequest,
)
from xianyu_system.worker.publish.service import PublishService


def utc_clock() -> datetime:
    """Return an aware UTC timestamp."""
    return datetime.now(UTC)


class ScheduleService:
    """Local-only schedule service with caller-owned database sessions."""

    def __init__(
        self,
        session_factory: Callable[[], Session],
        *,
        publish_service: PublishService,
        identifier_factory: Callable[[], UUID] = uuid.uuid4,
        clock: Callable[[], datetime] = utc_clock,
        validator: ScheduleValidator | None = None,
    ) -> None:
        self._session_factory = session_factory
        self._publish_service = publish_service
        self._identifier_factory = identifier_factory
        self._clock = clock
        self._validator = validator or ScheduleValidator()

    def schedule(self, request: object) -> ScheduleDecision:
        validation = self._validator.validate(request)
        if not validation.is_valid or not isinstance(request, ScheduleRequest):
            return ScheduleDecision(
                schedule_id="00000000-0000-0000-0000-000000000000",
                publish_request_id="00000000-0000-0000-0000-000000000000",
                idempotency_key="invalid-shape",
                decision_type=ScheduleDecisionType.INVALID_INPUT,
                lifecycle=ScheduleLifecycle.FAILED,
                due_at=None,
                normalized_fingerprint=None,
                reason="invalid schedule input",
            )
        fingerprint = validation.normalized_fingerprint or compute_schedule_fingerprint(request)
        session: Session | None = None
        try:
            session = self._session_factory()
            repository = ScheduleRepository(session)
            existing = repository.get_by_idempotency_key(request.idempotency_key)
            if existing is not None:
                session.rollback()
                decision_type = (
                    ScheduleDecisionType.DUPLICATE
                    if existing.normalized_fingerprint == fingerprint
                    else ScheduleDecisionType.CONFLICT
                )
                return ScheduleDecision(
                    schedule_id=existing.schedule_id,
                    publish_request_id=existing.publish_request_id,
                    idempotency_key=existing.idempotency_key,
                    decision_type=decision_type,
                    lifecycle=existing.lifecycle,
                    due_at=existing.due_at,
                    normalized_fingerprint=fingerprint,
                    reason="idempotency replay" if decision_type == ScheduleDecisionType.DUPLICATE else "idempotency conflict",
                )
            decision = ScheduleDecision(
                schedule_id=request.schedule_id,
                publish_request_id=request.publish_request_id,
                idempotency_key=request.idempotency_key,
                decision_type=ScheduleDecisionType.ACCEPTED,
                lifecycle=ScheduleLifecycle.PENDING,
                due_at=request.due_at,
                normalized_fingerprint=fingerprint,
                reason=None,
            )
            repository.add_schedule(
                event_id=str(self._identifier_factory()),
                decision=decision,
                request_values={
                    "schedule_id": request.schedule_id,
                    "publish_request_id": request.publish_request_id,
                    "idempotency_key": request.idempotency_key,
                    "trigger_type": request.trigger_type.value,
                    "lifecycle": ScheduleLifecycle.PENDING.value,
                    "normalized_fingerprint": fingerprint,
                    "requested_at": request.requested_at,
                    "due_at": request.due_at,
                    "misfire_grace_seconds": request.misfire_grace_seconds,
                    "synthetic_fixture": request.synthetic_fixture,
                    "correlation_id": request.correlation_id,
                    "claimed_at": None,
                    "completed_at": None,
                    "reason": None,
                },
                occurred_at=self._clock(),
            )
            session.commit()
            return decision
        except SchedulePersistenceError:
            if session is not None:
                session.rollback()
            return ScheduleDecision(
                schedule_id=request.schedule_id,
                publish_request_id=request.publish_request_id,
                idempotency_key=request.idempotency_key,
                decision_type=ScheduleDecisionType.MANUAL_REVIEW,
                lifecycle=ScheduleLifecycle.NEEDS_MANUAL_REVIEW,
                due_at=request.due_at,
                normalized_fingerprint=fingerprint,
                reason="schedule persistence failure",
            )
        finally:
            if session is not None:
                session.close()

    def cancel(self, *, schedule_id: str, reason: str) -> ScheduleDispatchResult:
        session: Session | None = None
        try:
            session = self._session_factory()
            result = ScheduleRepository(session).cancel_pending(
                event_id=str(self._identifier_factory()),
                schedule_id=schedule_id,
                occurred_at=self._clock(),
                reason=reason[:256],
            )
            session.commit()
            return result
        except SchedulePersistenceError:
            if session is not None:
                session.rollback()
            return ScheduleDispatchResult(schedule_id, ScheduleDispatchOutcome.MANUAL_REVIEW, ScheduleLifecycle.NEEDS_MANUAL_REVIEW, reason="schedule persistence failure")
        finally:
            if session is not None:
                session.close()

    def dispatch_due(
        self,
        *,
        schedule_id: str,
        draft: ListingDraft,
        publish_request: PublishRequest,
        publish_context: PublishEvaluationContext,
    ) -> ScheduleDispatchResult:
        now = self._clock()
        session: Session | None = None
        try:
            session = self._session_factory()
            repository = ScheduleRepository(session)
            claimed = repository.claim_due(
                event_id=str(self._identifier_factory()),
                schedule_id=schedule_id,
                now=now,
            )
            if claimed is None:
                session.rollback()
                return ScheduleDispatchResult(schedule_id, ScheduleDispatchOutcome.NOT_DUE, None, reason="not due or unavailable")
            if now > claimed.due_at + timedelta(seconds=claimed.misfire_grace_seconds):
                repository.complete_claimed(
                    event_id=str(self._identifier_factory()),
                    schedule_id=schedule_id,
                    lifecycle=ScheduleLifecycle.MISFIRED,
                    occurred_at=now,
                    reason="misfire grace elapsed",
                )
                session.commit()
                return ScheduleDispatchResult(schedule_id, ScheduleDispatchOutcome.MISFIRED, ScheduleLifecycle.MISFIRED, reason="misfire grace elapsed")
            session.commit()
        except SchedulePersistenceError:
            if session is not None:
                session.rollback()
            return ScheduleDispatchResult(schedule_id, ScheduleDispatchOutcome.MANUAL_REVIEW, ScheduleLifecycle.NEEDS_MANUAL_REVIEW, reason="schedule persistence failure")
        finally:
            if session is not None:
                session.close()

        publish_decision = self._publish_service.evaluate(draft, publish_request, publish_context)
        if publish_decision.decision_type == PublishDecisionType.READY:
            lifecycle = ScheduleLifecycle.DISPATCHED
            outcome = ScheduleDispatchOutcome.DISPATCHED
            reason = None
        else:
            lifecycle = ScheduleLifecycle.NEEDS_MANUAL_REVIEW
            outcome = ScheduleDispatchOutcome.MANUAL_REVIEW
            reason = "publish decision requires manual review"
        session = None
        try:
            session = self._session_factory()
            ScheduleRepository(session).complete_claimed(
                event_id=str(self._identifier_factory()),
                schedule_id=schedule_id,
                lifecycle=lifecycle,
                occurred_at=self._clock(),
                reason=reason,
            )
            session.commit()
        except SchedulePersistenceError:
            if session is not None:
                session.rollback()
            return ScheduleDispatchResult(schedule_id, ScheduleDispatchOutcome.MANUAL_REVIEW, ScheduleLifecycle.NEEDS_MANUAL_REVIEW, reason="schedule completion persistence failure")
        finally:
            if session is not None:
                session.close()
        return ScheduleDispatchResult(
            schedule_id=schedule_id,
            outcome=outcome,
            lifecycle=lifecycle,
            publish_decision_type=cast(PublishDecisionType, publish_decision.decision_type).value,
            reason=reason,
        )

    def count_schedules(self) -> int:
        session = self._session_factory()
        try:
            return ScheduleRepository(session).count_schedules()
        finally:
            session.close()
