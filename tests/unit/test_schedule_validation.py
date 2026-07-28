from __future__ import annotations

from datetime import UTC, datetime

from xianyu_system.schedule.domain import ScheduleRequest
from xianyu_system.schedule.validation import ScheduleValidator


def test_validator_accepts_normalized_schedule_request() -> None:
    request = ScheduleRequest(
        schedule_id="11111111-1111-1111-1111-111111111111",
        publish_request_id="22222222-2222-2222-2222-222222222222",
        idempotency_key="key",
        trigger_type="IMMEDIATE",
        requested_at=datetime(2026, 1, 1, 12, tzinfo=UTC),
        run_at=None,
        misfire_grace_seconds=60,
        synthetic_fixture=True,
    )

    result = ScheduleValidator().validate(request)

    assert result.is_valid is True
    assert result.normalized_fingerprint is not None
    assert result.issues == ()


def test_validator_rejects_wrong_shape_without_side_effects() -> None:
    result = ScheduleValidator().validate(object())

    assert result.is_valid is False
    assert result.normalized_fingerprint is None
    assert result.issues[0].field == "request"
