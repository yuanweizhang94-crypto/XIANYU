from __future__ import annotations

from collections.abc import Callable
from datetime import UTC, datetime, timedelta
from decimal import Decimal
from pathlib import Path
from uuid import UUID

from sqlalchemy import text

from xianyu_system.core.database import (
    DatabaseResources,
    dispose_database,
    initialize_database,
    upgrade_database,
)
from xianyu_system.schedule.domain import (
    ScheduleDecisionType,
    ScheduleDispatchOutcome,
    ScheduleLifecycle,
    ScheduleRequest,
    ScheduleTriggerType,
)
from xianyu_system.schedule.service import ScheduleService
from xianyu_system.worker.publish.domain import (
    ListingDraft,
    ListingDraftLifecycle,
    PublishAuthorizationState,
    PublishEvaluationContext,
    PublishRequest,
    PublishRiskState,
)
from xianyu_system.worker.publish.service import PublishService

NOW = datetime(2026, 1, 1, 12, tzinfo=UTC)
SCHEDULE_ID = "11111111-1111-1111-1111-111111111111"
PUBLISH_REQUEST_ID = "22222222-2222-2222-2222-222222222222"
DRAFT_ID = "33333333-3333-3333-3333-333333333333"


def fixed_identifier_factory() -> Callable[[], UUID]:
    values = iter(
        UUID(value)
        for value in [
            "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa",
            "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb",
            "cccccccc-cccc-cccc-cccc-cccccccccccc",
            "dddddddd-dddd-dddd-dddd-dddddddddddd",
            "eeeeeeee-eeee-eeee-eeee-eeeeeeeeeeee",
            "ffffffff-ffff-ffff-ffff-ffffffffffff",
            "99999999-9999-9999-9999-999999999999",
            "88888888-8888-8888-8888-888888888888",
        ]
    )
    return lambda: next(values)


def setup_service(tmp_path: Path, now: datetime) -> tuple[ScheduleService, DatabaseResources]:
    resources = initialize_database(tmp_path / "schedule-service.db")
    upgrade_database(resources)
    identifiers = fixed_identifier_factory()
    publish = PublishService(
        resources.session_factory,
        identifier_factory=identifiers,
        clock=lambda: now,
    )
    service = ScheduleService(
        resources.session_factory,
        publish_service=publish,
        identifier_factory=identifiers,
        clock=lambda: now,
    )
    return service, resources


def schedule_request(
    *,
    requested_at: datetime = NOW,
    run_at: datetime | None = None,
    grace_seconds: int = 60,
    idempotency_key: str = "schedule-key",
) -> ScheduleRequest:
    trigger_type = ScheduleTriggerType.IMMEDIATE if run_at is None else ScheduleTriggerType.RUN_AT_UTC
    return ScheduleRequest(
        schedule_id=SCHEDULE_ID,
        publish_request_id=PUBLISH_REQUEST_ID,
        idempotency_key=idempotency_key,
        trigger_type=trigger_type,
        requested_at=requested_at,
        run_at=run_at,
        misfire_grace_seconds=grace_seconds,
        synthetic_fixture=True,
        correlation_id="corr",
    )


def publish_inputs(now: datetime) -> tuple[ListingDraft, PublishRequest, PublishEvaluationContext]:
    draft = ListingDraft(
        draft_id=DRAFT_ID,
        revision=1,
        title="synthetic title",
        description="synthetic description",
        category_reference="synthetic-category",
        price=Decimal("12.34"),
        stock=1,
        location_reference="synthetic-location",
        media_metadata={"fixture": "local"},
        seller_profile_reference="synthetic-profile",
        lifecycle_state=ListingDraftLifecycle.VALIDATED,
        created_at=now,
        updated_at=now,
    )
    request = PublishRequest(
        request_id=PUBLISH_REQUEST_ID,
        draft_id=DRAFT_ID,
        draft_revision=1,
        idempotency_key="publish-key",
        requested_at=now,
        authorization_state=PublishAuthorizationState.AUTHORIZED,
        risk_state=PublishRiskState.CLEAR,
        synthetic_fixture=True,
        correlation_id="corr",
    )
    context = PublishEvaluationContext(
        authorization_state=PublishAuthorizationState.AUTHORIZED,
        risk_state=PublishRiskState.CLEAR,
        synthetic_fixture=True,
        request_time=now,
        local_profile_reference="synthetic-profile",
    )
    return draft, request, context


def count_rows(resources: DatabaseResources, table_name: str) -> int:
    with resources.engine.connect() as connection:
        return int(connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())


def schedule_lifecycle(resources: DatabaseResources) -> str:
    with resources.engine.connect() as connection:
        return str(connection.execute(text("SELECT lifecycle FROM xianyu_schedule_requests")).scalar_one())


def test_schedule_idempotency_and_dispatch_success(tmp_path: Path) -> None:
    service, resources = setup_service(tmp_path, NOW)
    try:
        accepted = service.schedule(schedule_request())
        replay = service.schedule(
            schedule_request(idempotency_key="schedule-key")
        )
        draft, publish_request, publish_context = publish_inputs(NOW)
        dispatched = service.dispatch_due(
            schedule_id=SCHEDULE_ID,
            draft=draft,
            publish_request=publish_request,
            publish_context=publish_context,
        )

        assert accepted.decision_type == ScheduleDecisionType.ACCEPTED
        assert replay.decision_type == ScheduleDecisionType.DUPLICATE
        assert dispatched.outcome == ScheduleDispatchOutcome.DISPATCHED
        assert dispatched.lifecycle == ScheduleLifecycle.DISPATCHED
        assert dispatched.publish_decision_type == "READY"
        assert schedule_lifecycle(resources) == "DISPATCHED"
        assert count_rows(resources, "xianyu_schedule_requests") == 1
        assert count_rows(resources, "xianyu_publish_requests") == 1
        assert count_rows(resources, "xianyu_publish_attempt_snapshots") == 0
    finally:
        dispose_database(resources)


def test_schedule_conflict_and_cancellation_are_local_only(tmp_path: Path) -> None:
    service, resources = setup_service(tmp_path, NOW)
    try:
        accepted = service.schedule(schedule_request())
        conflict = service.schedule(
            schedule_request(
                run_at=NOW + timedelta(minutes=5),
                idempotency_key="schedule-key",
            )
        )
        cancelled = service.cancel(schedule_id=SCHEDULE_ID, reason="project owner cancelled")
        not_due = service.dispatch_due(
            schedule_id=SCHEDULE_ID,
            draft=publish_inputs(NOW)[0],
            publish_request=publish_inputs(NOW)[1],
            publish_context=publish_inputs(NOW)[2],
        )

        assert accepted.decision_type == ScheduleDecisionType.ACCEPTED
        assert conflict.decision_type == ScheduleDecisionType.CONFLICT
        assert cancelled.outcome == ScheduleDispatchOutcome.CANCELLED
        assert cancelled.lifecycle == ScheduleLifecycle.CANCELLED
        assert not_due.outcome == ScheduleDispatchOutcome.NOT_DUE
        assert schedule_lifecycle(resources) == "CANCELLED"
        assert count_rows(resources, "xianyu_publish_requests") == 0
    finally:
        dispose_database(resources)


def test_misfire_moves_to_misfired_without_publish_call(tmp_path: Path) -> None:
    due_at = NOW - timedelta(minutes=10)
    service, resources = setup_service(tmp_path, NOW)
    try:
        decision = service.schedule(
            schedule_request(
                requested_at=NOW - timedelta(minutes=15),
                run_at=due_at,
                grace_seconds=30,
            )
        )
        result = service.dispatch_due(
            schedule_id=SCHEDULE_ID,
            draft=publish_inputs(NOW)[0],
            publish_request=publish_inputs(NOW)[1],
            publish_context=publish_inputs(NOW)[2],
        )

        assert decision.decision_type == ScheduleDecisionType.ACCEPTED
        assert result.outcome == ScheduleDispatchOutcome.MISFIRED
        assert result.lifecycle == ScheduleLifecycle.MISFIRED
        assert schedule_lifecycle(resources) == "MISFIRED"
        assert count_rows(resources, "xianyu_publish_requests") == 0
    finally:
        dispose_database(resources)
