from __future__ import annotations

from datetime import UTC, datetime
import logging

from xianyu_system.core.scheduler import create_scheduler, shutdown_scheduler, start_scheduler
from xianyu_system.schedule.apscheduler_adapter import register_one_time_schedule_job, remove_schedule_job
from xianyu_system.schedule.domain import ScheduleRequest


def test_adapter_registers_single_date_trigger_job_without_business_state() -> None:
    request = ScheduleRequest(
        schedule_id="11111111-1111-1111-1111-111111111111",
        publish_request_id="22222222-2222-2222-2222-222222222222",
        idempotency_key="key",
        trigger_type="RUN_AT_UTC",
        requested_at=datetime(2026, 1, 1, 12, tzinfo=UTC),
        run_at=datetime(2026, 1, 1, 13, tzinfo=UTC),
        misfire_grace_seconds=60,
        synthetic_fixture=True,
    )
    scheduler = create_scheduler(logger=logging.getLogger("schedule-adapter-test"))
    try:
        start_scheduler(scheduler)
        job_id = register_one_time_schedule_job(scheduler, request, lambda schedule_id: None)
        assert job_id == "schedule:11111111-1111-1111-1111-111111111111"
        assert scheduler.get_job(job_id) is not None
        assert remove_schedule_job(scheduler, request.schedule_id) is True
        assert remove_schedule_job(scheduler, request.schedule_id) is False
    finally:
        shutdown_scheduler(scheduler)
