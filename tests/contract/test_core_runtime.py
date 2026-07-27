from __future__ import annotations

import json
import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import Base, DatabaseResources, get_current_revision, open_session
from xianyu_system.core.logging import ManagedStreamHandler
from xianyu_system.web.router import HOME_PATH, HOME_ROUTE_NAME, STATIC_URL_PATH

ROOT = Path(__file__).resolve().parents[2]
BUSINESS_METADATA_TABLES = {
    "xianyu_account_profiles",
    "xianyu_message_conversations",
    "xianyu_message_records",
    "xianyu_message_delivery_attempts",
    "xianyu_reply_templates",
    "xianyu_reply_rules",
    "xianyu_reply_conditions",
    "xianyu_reply_audit_events",
}


def project_events(captured: str) -> list[dict[str, object]]:
    return [json.loads(line) for line in captured.splitlines() if line and "event" in line]


def settings_for(tmp_path: Path, name: str, *, title: str = "XIANYU") -> ApplicationSettings:
    return ApplicationSettings(environment="test", app_title=title, database_path=tmp_path / name)


def assert_runtime_surface(client: TestClient, app: FastAPI, *, service: str = "XIANYU") -> None:
    home = client.get(HOME_PATH)
    assert home.status_code == 200
    assert service in home.text
    assert 'hx-get="/health"' in home.text
    assert client.get("/health").json()["status"] == "ok"
    assert client.get(f"{STATIC_URL_PATH}/styles.css").status_code == 200
    assert client.get(f"{STATIC_URL_PATH}/vendor/htmx.min.js").status_code == 200
    assert set(app.openapi()["paths"]) == {"/health"}
    assert str(app.url_path_for(HOME_ROUTE_NAME)) == HOME_PATH


def test_core_runtime_contract_serves_only_approved_read_surfaces(tmp_path: Path) -> None:
    app = create_application(settings=settings_for(tmp_path, "runtime.db"))

    with TestClient(app) as client:
        assert isinstance(app.state.database, DatabaseResources)
        assert isinstance(app.state.scheduler, BackgroundScheduler)
        assert app.state.scheduler.running is True
        assert app.state.scheduler.get_jobs() == []
        assert get_current_revision(app.state.database) is None
        assert set(Base.metadata.tables) <= BUSINESS_METADATA_TABLES
        assert set(inspect(app.state.database.engine).get_table_names()) == set()
        with app.state.database.engine.connect() as connection:
            assert connection.exec_driver_sql("SELECT 1").scalar_one() == 1
            assert (
                str(connection.exec_driver_sql("PRAGMA journal_mode").scalar_one()).lower() == "wal"
            )
        with open_session(app.state.database) as session:
            assert session.execute(text("SELECT 1")).scalar_one() == 1
        assert_runtime_surface(client, app)

    assert app.state.database is None
    assert app.state.scheduler is None
    assert not any(
        isinstance(handler, ManagedStreamHandler)
        for handler in logging.getLogger(f"xianyu.application.{id(app)}").handlers
    )
    assert not (ROOT / "data" / "xianyu.db").exists()


def test_multiple_application_instances_have_independent_runtime_resources(tmp_path: Path) -> None:
    first = create_application(settings=settings_for(tmp_path, "first.db", title="FIRST CORE"))
    second = create_application(settings=settings_for(tmp_path, "second.db", title="SECOND CORE"))

    with TestClient(first) as first_client, TestClient(second) as second_client:
        assert first is not second
        assert first.state.settings is not second.state.settings
        assert first.state.database is not second.state.database
        assert first.state.database.path != second.state.database.path
        assert first.state.database.engine is not second.state.database.engine
        assert first.state.database.session_factory is not second.state.database.session_factory
        assert first.state.scheduler is not second.state.scheduler
        assert first.state.logger is not second.state.logger
        assert first.state.web_templates is not second.state.web_templates
        assert_runtime_surface(first_client, first, service="FIRST CORE")
        assert_runtime_surface(second_client, second, service="SECOND CORE")


def test_one_application_can_shutdown_while_another_remains_healthy(tmp_path: Path) -> None:
    first = create_application(settings=settings_for(tmp_path, "first-close.db", title="FIRST"))
    second = create_application(settings=settings_for(tmp_path, "second-open.db", title="SECOND"))
    first_client = TestClient(first)
    second_client = TestClient(second)

    try:
        first_client.__enter__()
        second_client.__enter__()
        assert first.state.scheduler.running is True
        assert second.state.scheduler.running is True

        first_client.__exit__(None, None, None)
        assert first.state.scheduler is None
        assert first.state.database is None
        assert second.state.scheduler.running is True
        assert second_client.get("/health").status_code == 200
        with second.state.database.engine.connect() as connection:
            assert connection.exec_driver_sql("SELECT 1").scalar_one() == 1
        assert_runtime_surface(second_client, second, service="SECOND")
    finally:
        second_client.__exit__(None, None, None)

    assert second.state.scheduler is None
    assert second.state.database is None


def test_repeated_lifespan_cycles_leave_no_jobs_handlers_or_default_artifacts(
    tmp_path: Path,
) -> None:
    for index in range(3):
        app = create_application(settings=settings_for(tmp_path, f"cycle-{index}.db"))
        logger_name = f"xianyu.application.{id(app)}"
        with TestClient(app) as client:
            assert client.get("/health").status_code == 200
            assert app.state.scheduler.running is True
            assert app.state.scheduler.get_jobs() == []
            assert get_current_revision(app.state.database) is None
            assert set(inspect(app.state.database.engine).get_table_names()) == set()
        assert app.state.scheduler is None
        assert app.state.database is None
        assert not any(
            isinstance(handler, ManagedStreamHandler)
            for handler in logging.getLogger(logger_name).handlers
        )
    assert not (ROOT / "data" / "xianyu.db").exists()


def test_custom_lifespan_runs_between_project_startup_and_shutdown(tmp_path: Path) -> None:
    observations: list[str] = []

    @asynccontextmanager
    async def custom_lifespan(app: FastAPI) -> AsyncIterator[None]:
        assert app.state.database is not None
        assert app.state.scheduler.running is True
        assert str(app.url_path_for("get_health")) == "/health"
        assert str(app.url_path_for(HOME_ROUTE_NAME)) == HOME_PATH
        observations.append("custom-startup")
        yield
        assert app.state.database is not None
        assert app.state.scheduler.running is True
        observations.append("custom-shutdown")

    app = create_application(
        lifespan=custom_lifespan,
        settings=settings_for(tmp_path, "custom.db"),
    )

    with TestClient(app) as client:
        assert observations == ["custom-startup"]
        assert_runtime_surface(client, app)

    assert observations == ["custom-startup", "custom-shutdown"]


def test_lifecycle_event_order_is_stable(tmp_path: Path, capsys) -> None:
    app = create_application(settings=settings_for(tmp_path, "events.db"))

    with TestClient(app):
        pass

    assert [event["event"] for event in project_events(capsys.readouterr().err)] == [
        "application.startup",
        "database.ready",
        "scheduler.ready",
        "scheduler.shutdown",
        "database.shutdown",
        "application.shutdown",
    ]


def test_runtime_does_not_apply_migrations_or_create_business_tables(tmp_path: Path) -> None:
    app = create_application(settings=settings_for(tmp_path, "no-migration.db"))

    with TestClient(app):
        assert get_current_revision(app.state.database) is None
        assert set(inspect(app.state.database.engine).get_table_names()) == set()
        assert set(Base.metadata.tables) <= BUSINESS_METADATA_TABLES

    assert app.state.database is None
