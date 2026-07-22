from __future__ import annotations

import logging
import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.base import SchedulerAlreadyRunningError
from sqlalchemy import inspect

from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import dispose_database, get_current_revision, initialize_database
from xianyu_system.core.scheduler import (
    SCHEDULER_TIMEZONE,
    create_scheduler,
    shutdown_scheduler,
    start_scheduler,
)

ROOT = Path(__file__).resolve().parents[2]
SCHEDULER_SOURCE = ROOT / "app" / "xianyu_system" / "core" / "scheduler.py"


def scheduler_logger(suffix: str) -> logging.Logger:
    logger = logging.getLogger(f"xianyu.test.scheduler.{suffix}.{id(object())}")
    logger.handlers.clear()
    logger.propagate = False
    return logger


def test_import_has_no_runtime_side_effects(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    script = """
import threading
import xianyu_system.core.scheduler
assert [thread.name for thread in threading.enumerate() if 'APScheduler' in thread.name] == []
"""

    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == ""
    assert result.stderr == ""
    assert not (tmp_path / "data").exists()
    assert not (tmp_path / "logs").exists()
    for pattern in ["*.db", "*.sqlite", "*.sqlite3"]:
        assert list(tmp_path.glob(pattern)) == []


def test_create_scheduler_returns_stopped_background_scheduler_with_memory_store() -> None:
    logger = scheduler_logger("create")

    scheduler = create_scheduler(logger=logger)
    try:
        assert isinstance(scheduler, BackgroundScheduler)
        assert scheduler.running is False
        assert scheduler.timezone == SCHEDULER_TIMEZONE
        assert scheduler.get_jobs() == []
        assert isinstance(scheduler._jobstores["default"], MemoryJobStore)
        assert scheduler._logger is logger
    finally:
        shutdown_scheduler(scheduler)


def test_start_scheduler_starts_without_registering_jobs() -> None:
    scheduler = create_scheduler(logger=scheduler_logger("start"))
    try:
        start_scheduler(scheduler)
        assert scheduler.running is True
        assert scheduler.get_jobs() == []
    finally:
        shutdown_scheduler(scheduler)

    assert scheduler.running is False


def test_shutdown_scheduler_is_safe_for_unstarted_and_repeated_shutdown() -> None:
    scheduler = create_scheduler(logger=scheduler_logger("shutdown"))

    shutdown_scheduler(scheduler)
    assert scheduler.running is False

    start_scheduler(scheduler)
    assert scheduler.running is True
    shutdown_scheduler(scheduler)
    shutdown_scheduler(scheduler)
    assert scheduler.running is False


def test_start_scheduler_propagates_already_running_error() -> None:
    scheduler = create_scheduler(logger=scheduler_logger("already-running"))
    try:
        start_scheduler(scheduler)
        with pytest.raises(SchedulerAlreadyRunningError):
            start_scheduler(scheduler)
    finally:
        shutdown_scheduler(scheduler)


def test_shutdown_scheduler_forwards_wait_flag_and_propagates_failures() -> None:
    stopped = Mock(running=False)
    shutdown_scheduler(stopped, wait=False)
    stopped.shutdown.assert_not_called()

    running = Mock(running=True)
    shutdown_scheduler(running, wait=False)
    running.shutdown.assert_called_once_with(wait=False)

    failing = Mock(running=True)
    failing.shutdown.side_effect = RuntimeError("scheduler shutdown failure")
    with pytest.raises(RuntimeError, match="scheduler shutdown failure"):
        shutdown_scheduler(failing)


def test_scheduler_source_has_no_registered_jobs_or_persistent_job_store() -> None:
    source = SCHEDULER_SOURCE.read_text(encoding="utf-8")

    assert "BackgroundScheduler" in source
    assert "MemoryJobStore" in source
    assert "SCHEDULER_TIMEZONE" in source
    assert "SQLAlchemyJobStore" not in source
    assert "MongoDBJobStore" not in source
    assert "RedisJobStore" not in source
    assert "add_job(" not in source
    assert "scheduled_job(" not in source
    assert "@scheduler" not in source
    assert "atexit" not in source


def test_scheduler_does_not_create_database_tables_or_migration_state(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "scheduler-db.db")
    scheduler = create_scheduler(logger=scheduler_logger("database"))
    try:
        start_scheduler(scheduler)
        shutdown_scheduler(scheduler)

        assert get_current_revision(resources) is None
        assert set(inspect(resources.engine).get_table_names()) == set()
    finally:
        shutdown_scheduler(scheduler)
        dispose_database(resources)


def test_health_endpoint_does_not_mutate_scheduler_or_jobs(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "health-scheduler.db")
    )

    with TestClient(app) as client:
        scheduler = app.state.scheduler
        assert scheduler.running is True
        assert scheduler.get_jobs() == []
        assert client.get("/health").status_code == 200
        assert scheduler.running is True
        assert scheduler.get_jobs() == []


def test_health_api_source_does_not_call_scheduler_mutators() -> None:
    source = (ROOT / "app/xianyu_system/api/health.py").read_text(encoding="utf-8")
    for forbidden in [".add_job(", ".remove_job(", ".remove_all_jobs(", ".pause(", ".resume(", ".start(", ".shutdown("]:
        assert forbidden not in source
