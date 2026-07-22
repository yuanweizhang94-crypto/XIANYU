from __future__ import annotations

import logging
from datetime import UTC, tzinfo

from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler

SCHEDULER_TIMEZONE: tzinfo = UTC


def create_scheduler(*, logger: logging.Logger) -> BackgroundScheduler:
    """Create a stopped in-memory scheduler for one application instance."""
    return BackgroundScheduler(
        jobstores={"default": MemoryJobStore()},
        timezone=SCHEDULER_TIMEZONE,
        daemon=True,
        logger=logger,
    )


def start_scheduler(scheduler: BackgroundScheduler) -> None:
    """Start the scheduler without registering any jobs."""
    scheduler.start()


def shutdown_scheduler(scheduler: BackgroundScheduler, *, wait: bool = True) -> None:
    """Shut down a running scheduler and tolerate already-stopped schedulers."""
    if scheduler.running:
        scheduler.shutdown(wait=wait)


__all__ = [
    "SCHEDULER_TIMEZONE",
    "create_scheduler",
    "shutdown_scheduler",
    "start_scheduler",
]
