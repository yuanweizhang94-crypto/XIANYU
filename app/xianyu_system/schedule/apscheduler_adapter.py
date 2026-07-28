"""APScheduler adapter for one-time in-process Schedule wakeups."""

from __future__ import annotations

from collections.abc import Callable
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.date import DateTrigger

from xianyu_system.schedule.domain import ScheduleRequest


def register_one_time_schedule_job(
    scheduler: BackgroundScheduler,
    request: ScheduleRequest,
    dispatch: Callable[[str], None],
) -> str:
    """Register one in-memory DateTrigger wakeup without creating business facts."""
    job_id = f"schedule:{request.schedule_id}"
    scheduler.add_job(
        dispatch,
        trigger=DateTrigger(run_date=request.due_at, timezone="UTC"),
        args=[request.schedule_id],
        id=job_id,
        replace_existing=True,
        misfire_grace_time=request.misfire_grace_seconds,
        max_instances=1,
        coalesce=True,
    )
    return job_id


def remove_schedule_job(scheduler: BackgroundScheduler, schedule_id: str) -> bool:
    """Remove a wakeup job if it exists; repository cancellation remains separate."""
    job_id = f"schedule:{schedule_id}"
    if scheduler.get_job(job_id) is None:
        return False
    scheduler.remove_job(job_id)
    return True


def scheduler_job_run_time(request: ScheduleRequest) -> datetime:
    """Expose the UTC run time used by the adapter for tests and audits."""
    return request.due_at
