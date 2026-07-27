from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from xianyu_system.api import health as health_module
from xianyu_system.api.health import (
    DatabaseHealth,
    HealthResponse,
    SchedulerHealth,
    collect_database_health,
    collect_health,
    collect_scheduler_health,
)
from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import get_current_revision, upgrade_database

MESSAGE_TABLES = {
    "xianyu_message_conversations",
    "xianyu_message_records",
    "xianyu_message_delivery_attempts",
}
REPLY_TABLES = {
    "xianyu_reply_templates",
    "xianyu_reply_rules",
    "xianyu_reply_conditions",
    "xianyu_reply_audit_events",
}

EXPECTED_TOP_LEVEL = {"status", "service", "version", "environment", "database", "scheduler"}
EXPECTED_DATABASE = {"status", "connected", "journal_mode"}
EXPECTED_SCHEDULER = {"status", "running", "job_count", "timezone"}
SENSITIVE_MARKERS = [
    "cookie",
    "token",
    "secret",
    "password",
    "credential",
    "account",
    "customer",
    "browser",
    "traceback",
    "exception",
]


def test_health_endpoint_returns_ok_response_with_strict_safe_fields(tmp_path: Path) -> None:
    settings = ApplicationSettings(environment="test", database_path=tmp_path / "health.db")
    app = create_application(settings=settings)

    with TestClient(app) as client:
        response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/json")
    data = response.json()
    assert set(data) == EXPECTED_TOP_LEVEL
    assert set(data["database"]) == EXPECTED_DATABASE
    assert set(data["scheduler"]) == EXPECTED_SCHEDULER
    assert data == {
        "status": "ok",
        "service": settings.app_title,
        "version": settings.app_version,
        "environment": "test",
        "database": {"status": "ok", "connected": True, "journal_mode": "wal"},
        "scheduler": {"status": "ok", "running": True, "job_count": 0, "timezone": "UTC"},
    }
    body = json.dumps(data).lower()
    assert str(settings.database_path).lower() not in body
    for marker in SENSITIVE_MARKERS:
        assert marker not in body


def test_health_endpoint_degrades_database_without_exception_details(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = ApplicationSettings(environment="test", database_path=tmp_path / "db-degraded.db")
    app = create_application(settings=settings)

    def unavailable_database(_resources):
        return DatabaseHealth(status="unavailable", connected=False, journal_mode=None)

    monkeypatch.setattr(health_module, "collect_database_health", unavailable_database)

    with TestClient(app) as client:
        response = client.get("/health")

    data = response.json()
    assert response.status_code == 503
    assert data["status"] == "degraded"
    assert data["database"] == {"status": "unavailable", "connected": False, "journal_mode": None}
    assert data["scheduler"] == {"status": "ok", "running": True, "job_count": 0, "timezone": "UTC"}
    assert "synthetic" not in json.dumps(data).lower()
    assert str(settings.database_path).lower() not in json.dumps(data).lower()


def test_health_endpoint_degrades_scheduler_without_mutating_database(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    settings = ApplicationSettings(
        environment="test", database_path=tmp_path / "scheduler-degraded.db"
    )
    app = create_application(settings=settings)

    def unavailable_scheduler(_scheduler):
        return SchedulerHealth(status="unavailable", running=False, job_count=0, timezone="UTC")

    monkeypatch.setattr(health_module, "collect_scheduler_health", unavailable_scheduler)

    with TestClient(app) as client:
        before_revision = get_current_revision(app.state.database)
        before_tables = set(inspect(app.state.database.engine).get_table_names())
        response = client.get("/health")
        after_revision = get_current_revision(app.state.database)
        after_tables = set(inspect(app.state.database.engine).get_table_names())

    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "degraded"
    assert data["scheduler"] == {
        "status": "unavailable",
        "running": False,
        "job_count": 0,
        "timezone": "UTC",
    }
    assert before_revision == after_revision is None
    assert before_tables == after_tables == set()


def test_collect_health_outside_lifespan_returns_structured_degraded(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "outside.db")
    )

    health = collect_health(app)

    assert isinstance(health, HealthResponse)
    assert health.status == "degraded"
    assert health.database == DatabaseHealth(
        status="unavailable", connected=False, journal_mode=None
    )
    assert health.scheduler == SchedulerHealth(
        status="unavailable", running=False, job_count=0, timezone="UTC"
    )


def test_collect_database_health_is_read_only_and_uses_existing_engine(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "readonly.db")
    )

    with TestClient(app):
        resources = app.state.database
        before_revision = get_current_revision(resources)
        before_tables = set(inspect(resources.engine).get_table_names())
        with resources.engine.connect() as connection:
            before_wal = connection.exec_driver_sql("PRAGMA journal_mode").scalar_one()
        with patch("xianyu_system.api.health.DatabaseResources"):
            health = collect_database_health(resources)
        after_revision = get_current_revision(resources)
        after_tables = set(inspect(resources.engine).get_table_names())
        with resources.engine.connect() as connection:
            after_wal = connection.exec_driver_sql("PRAGMA journal_mode").scalar_one()

    assert health == DatabaseHealth(status="ok", connected=True, journal_mode="wal")
    assert before_revision == after_revision is None
    assert before_tables == after_tables == set()
    assert str(before_wal).lower() == str(after_wal).lower() == "wal"


def test_collect_database_health_converts_probe_failures_to_unavailable() -> None:
    resources = Mock()
    resources.engine.connect.side_effect = RuntimeError("synthetic database failure")

    health = collect_database_health(resources)

    assert health == DatabaseHealth(status="unavailable", connected=False, journal_mode=None)


def test_collect_database_health_requires_wal_and_select_one() -> None:
    resources = Mock()
    context = Mock()
    connection = Mock()
    context.__enter__ = Mock(return_value=connection)
    context.__exit__ = Mock(return_value=None)
    resources.engine.connect.return_value = context
    connection.exec_driver_sql.side_effect = [
        Mock(scalar_one=Mock(return_value=1)),
        Mock(scalar_one=Mock(return_value="delete")),
    ]

    health = collect_database_health(resources)

    assert health == DatabaseHealth(status="unavailable", connected=False, journal_mode=None)


def test_collect_scheduler_health_is_read_only_and_job_free(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "scheduler.db")
    )

    with TestClient(app):
        scheduler = app.state.scheduler
        assert isinstance(scheduler, BackgroundScheduler)
        before_running = scheduler.running
        before_jobs = scheduler.get_jobs()
        health = collect_scheduler_health(scheduler)
        after_running = scheduler.running
        after_jobs = scheduler.get_jobs()

    assert health == SchedulerHealth(status="ok", running=True, job_count=0, timezone="UTC")
    assert before_running is True
    assert after_running is True
    assert before_jobs == after_jobs == []


def test_collect_scheduler_health_handles_absent_stopped_and_failing_scheduler() -> None:
    assert collect_scheduler_health(None) == SchedulerHealth(
        status="unavailable", running=False, job_count=0, timezone="UTC"
    )

    stopped = Mock(running=False)
    stopped.get_jobs.return_value = []
    assert collect_scheduler_health(stopped) == SchedulerHealth(
        status="unavailable", running=False, job_count=0, timezone="UTC"
    )

    failing = Mock()
    type(failing).running = property(lambda _self: (_ for _ in ()).throw(RuntimeError("boom")))
    assert collect_scheduler_health(failing) == SchedulerHealth(
        status="unavailable", running=False, job_count=0, timezone="UTC"
    )


def test_health_endpoint_does_not_run_migrations_or_write_database(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "migration.db")
    )

    with TestClient(app) as client:
        resources = app.state.database
        upgrade_database(resources)
        before_revision = get_current_revision(resources)
        before_tables = set(inspect(resources.engine).get_table_names())
        client.get("/health")
        after_revision = get_current_revision(resources)
        after_tables = set(inspect(resources.engine).get_table_names())
        with resources.engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1

    assert before_revision == after_revision == "0004_xianyu_reply_boundary"
    assert (
        before_tables
        == after_tables
        == {"alembic_version", "xianyu_account_profiles", *MESSAGE_TABLES, *REPLY_TABLES}
    )


def test_health_endpoint_does_not_modify_logger_handlers_or_scheduler_jobs(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "effects.db")
    )

    with TestClient(app) as client:
        root_handlers = list(__import__("logging").getLogger().handlers)
        logger_handlers = list(app.state.logger.handlers)
        scheduler = app.state.scheduler
        assert scheduler.running is True
        response = client.get("/health")
        assert response.status_code == 200
        assert list(__import__("logging").getLogger().handlers) == root_handlers
        assert list(app.state.logger.handlers) == logger_handlers
        assert scheduler.running is True
        assert scheduler.get_jobs() == []


def test_health_route_allows_only_get_and_declares_no_parameters(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "methods.db")
    )

    with TestClient(app) as client:
        assert client.post("/health").status_code == 405
        assert client.put("/health").status_code == 405
        assert client.delete("/health").status_code == 405
        operation = app.openapi()["paths"]["/health"]["get"]

    assert operation["operationId"] == "get_health"
    assert operation.get("parameters", []) == []
    assert {"200", "503"} <= set(operation["responses"])
