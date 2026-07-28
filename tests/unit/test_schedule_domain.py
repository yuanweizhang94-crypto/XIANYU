from __future__ import annotations

from datetime import UTC, datetime

import pytest

from xianyu_system.schedule.domain import InvalidScheduleInput, ScheduleRequest, ScheduleTriggerType


def test_immediate_schedule_uses_requested_at_as_due_time() -> None:
    requested_at = datetime(2026, 1, 1, 12, tzinfo=UTC)
    request = ScheduleRequest(
        schedule_id="11111111-1111-1111-1111-111111111111",
        publish_request_id="22222222-2222-2222-2222-222222222222",
        idempotency_key=" schedule-key ",
        trigger_type=ScheduleTriggerType.IMMEDIATE,
        requested_at=requested_at,
        run_at=None,
        misfire_grace_seconds=60,
        synthetic_fixture=True,
    )

    assert request.idempotency_key == "schedule-key"
    assert request.due_at == requested_at
    assert request.trigger_type == ScheduleTriggerType.IMMEDIATE


def test_run_at_schedule_requires_aware_utc_time() -> None:
    request = ScheduleRequest(
        schedule_id="11111111-1111-1111-1111-111111111111",
        publish_request_id="22222222-2222-2222-2222-222222222222",
        idempotency_key="schedule-key",
        trigger_type="RUN_AT_UTC",
        requested_at=datetime(2026, 1, 1, 12, tzinfo=UTC),
        run_at=datetime(2026, 1, 1, 13, tzinfo=UTC),
        misfire_grace_seconds=0,
        synthetic_fixture=True,
    )

    assert request.due_at == datetime(2026, 1, 1, 13, tzinfo=UTC)


@pytest.mark.parametrize(
    ("trigger_type", "run_at"),
    [("RUN_AT_UTC", None), ("IMMEDIATE", datetime(2026, 1, 1, tzinfo=UTC))],
)
def test_trigger_and_run_at_must_match(trigger_type: str, run_at: datetime | None) -> None:
    with pytest.raises(InvalidScheduleInput):
        ScheduleRequest(
            schedule_id="11111111-1111-1111-1111-111111111111",
            publish_request_id="22222222-2222-2222-2222-222222222222",
            idempotency_key="schedule-key",
            trigger_type=trigger_type,
            requested_at=datetime(2026, 1, 1, 12, tzinfo=UTC),
            run_at=run_at,
            misfire_grace_seconds=60,
            synthetic_fixture=True,
        )


def test_grace_window_is_finite() -> None:
    with pytest.raises(InvalidScheduleInput):
        ScheduleRequest(
            schedule_id="11111111-1111-1111-1111-111111111111",
            publish_request_id="22222222-2222-2222-2222-222222222222",
            idempotency_key="schedule-key",
            trigger_type="IMMEDIATE",
            requested_at=datetime(2026, 1, 1, 12, tzinfo=UTC),
            run_at=None,
            misfire_grace_seconds=3601,
            synthetic_fixture=True,
        )
