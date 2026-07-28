from __future__ import annotations

from datetime import UTC, datetime

from xianyu_system.schedule.domain import ScheduleRequest
from xianyu_system.schedule.fingerprint import compute_schedule_fingerprint


def make_request(key: str = "key") -> ScheduleRequest:
    return ScheduleRequest(
        schedule_id="11111111-1111-1111-1111-111111111111",
        publish_request_id="22222222-2222-2222-2222-222222222222",
        idempotency_key=key,
        trigger_type="RUN_AT_UTC",
        requested_at=datetime(2026, 1, 1, 12, tzinfo=UTC),
        run_at=datetime(2026, 1, 1, 13, tzinfo=UTC),
        misfire_grace_seconds=60,
        synthetic_fixture=True,
        correlation_id="corr",
    )


def test_schedule_fingerprint_is_stable_and_sensitive_to_semantics() -> None:
    first = compute_schedule_fingerprint(make_request())
    second = compute_schedule_fingerprint(make_request())
    changed = compute_schedule_fingerprint(make_request("other"))

    assert first == second
    assert len(first) == 64
    assert first != changed
