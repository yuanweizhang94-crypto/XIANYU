from __future__ import annotations

import json
import os
import subprocess
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy import inspect, text

from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import (
    BASELINE_REVISION,
    DatabaseResources,
    get_current_revision,
    open_session,
    upgrade_database,
)
from xianyu_system.core.logging import ManagedStreamHandler

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_FASTAPI_ROUTE_PATHS = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}
FORBIDDEN_IMPORT_ARTIFACTS = [
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "alembic.ini",
    "migrations",
    "logs",
]
SUPPORTED_ENV_VARS = [
    "XIANYU_ENVIRONMENT",
    "XIANYU_APP_TITLE",
    "XIANYU_APP_VERSION",
    "XIANYU_DEBUG",
    "XIANYU_LOG_LEVEL",
    "XIANYU_DATABASE_PATH",
    "xianyu_environment",
    "xianyu_app_title",
    "xianyu_app_version",
    "xianyu_debug",
    "xianyu_log_level",
    "xianyu_database_path",
]


def clear_supported_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in SUPPORTED_ENV_VARS:
        monkeypatch.delenv(name, raising=False)


def route_paths(app: FastAPI) -> set[str]:
    return {str(route.path) for route in app.routes}


def project_events(captured: str) -> list[dict[str, object]]:
    records = [json.loads(line) for line in captured.splitlines() if line]
    return [record for record in records if "event" in record]


def test_create_application_returns_fastapi_instance() -> None:
    assert isinstance(create_application(), FastAPI)


def test_repeated_creation_returns_isolated_instances() -> None:
    first = create_application()
    second = create_application()

    assert first is not second
    assert first.state is not second.state


def test_application_metadata_is_stable(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    app = create_application()

    assert app.title == "XIANYU"
    assert app.version == "0.1.0"
    assert app.debug is False


def test_default_application_contains_settings_instance(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    app = create_application()

    assert isinstance(app.state.settings, ApplicationSettings)


def test_default_applications_have_distinct_settings_instances(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clear_supported_environment(monkeypatch)
    first = create_application()
    second = create_application()

    assert first.state.settings is not second.state.settings


def test_supplied_settings_instance_is_stored_on_application_state() -> None:
    supplied_settings = ApplicationSettings(app_title="Supplied XIANYU")

    app = create_application(settings=supplied_settings)

    assert app.state.settings is supplied_settings


def test_supplied_settings_metadata_is_applied_to_fastapi() -> None:
    supplied_settings = ApplicationSettings(
        app_title="TEST APP",
        app_version="9.8.7",
        debug=True,
    )

    app = create_application(settings=supplied_settings)

    assert app.title == "TEST APP"
    assert app.version == "9.8.7"
    assert app.debug is True


def test_environment_can_influence_default_application(monkeypatch: pytest.MonkeyPatch) -> None:
    clear_supported_environment(monkeypatch)
    monkeypatch.setenv("XIANYU_APP_TITLE", "ENV APP")
    monkeypatch.setenv("XIANYU_APP_VERSION", "2.0.0")
    monkeypatch.setenv("XIANYU_DEBUG", "true")

    app = create_application()

    assert app.title == "ENV APP"
    assert app.version == "2.0.0"
    assert app.debug is True


def test_explicit_settings_override_environment_for_application(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    clear_supported_environment(monkeypatch)
    monkeypatch.setenv("XIANYU_APP_TITLE", "ENV APP")
    supplied_settings = ApplicationSettings(app_title="EXPLICIT APP")

    app = create_application(settings=supplied_settings)

    assert app.state.settings is supplied_settings
    assert app.title == "EXPLICIT APP"


def test_application_has_no_custom_business_routes() -> None:
    app = create_application()

    assert route_paths(app) <= DEFAULT_FASTAPI_ROUTE_PATHS
    assert app.openapi()["paths"] == {}
    assert "/health" not in app.openapi()["paths"]
    assert "/" not in route_paths(app)


def test_custom_lifespan_runs_startup_and_shutdown_once(tmp_path: Path) -> None:
    events: list[str] = []

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        events.append("startup")
        yield
        events.append("shutdown")

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "custom.db"),
    )

    with TestClient(app):
        assert events == ["startup"]

    assert events == ["startup", "shutdown"]


def test_settings_injection_preserves_custom_lifespan_behavior(tmp_path: Path) -> None:
    events: list[str] = []
    supplied_settings = ApplicationSettings(
        app_title="LIFESPAN APP",
        database_path=tmp_path / "settings-lifespan.db",
    )

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        events.append("startup")
        yield
        events.append("shutdown")

    app = create_application(lifespan=lifespan, settings=supplied_settings)

    with TestClient(app):
        assert app.state.settings is supplied_settings
        assert events == ["startup"]

    assert events == ["startup", "shutdown"]


def test_lifespan_state_is_isolated_per_application(tmp_path: Path) -> None:
    first_events: list[str] = []
    second_events: list[str] = []

    @asynccontextmanager
    async def first_lifespan(_: FastAPI) -> AsyncIterator[None]:
        first_events.append("first-startup")
        yield
        first_events.append("first-shutdown")

    @asynccontextmanager
    async def second_lifespan(_: FastAPI) -> AsyncIterator[None]:
        second_events.append("second-startup")
        yield
        second_events.append("second-shutdown")

    first = create_application(
        lifespan=first_lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "first.db"),
    )
    second = create_application(
        lifespan=second_lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "second.db"),
    )

    with TestClient(first):
        assert first_events == ["first-startup"]
        assert second_events == []

    assert first_events == ["first-startup", "first-shutdown"]
    assert second_events == []

    with TestClient(second):
        assert first_events == ["first-startup", "first-shutdown"]
        assert second_events == ["second-startup"]

    assert second_events == ["second-startup", "second-shutdown"]


def test_main_entry_exposes_fastapi_app_and_factory_remains_reusable() -> None:
    from xianyu_system.application import create_application as imported_factory
    from xianyu_system.main import app

    other = imported_factory()

    assert isinstance(app, FastAPI)
    assert isinstance(other, FastAPI)
    assert app is not other
    assert isinstance(app.state.settings, ApplicationSettings)


def test_application_sources_do_not_use_legacy_event_or_uvicorn_runner() -> None:
    for relative in ["app/xianyu_system/application.py", "app/xianyu_system/main.py"]:
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert ".on_event(" not in source
        assert "uvicorn.run(" not in source


def test_imports_do_not_create_runtime_files(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import xianyu_system.application; import xianyu_system.main",
        ],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stderr == ""
    for pattern in FORBIDDEN_IMPORT_ARTIFACTS:
        assert list(tmp_path.glob(pattern)) == []


def test_create_application_does_not_configure_logging_immediately() -> None:
    app = create_application()

    assert not hasattr(app.state, "logger")


def test_logging_lifespan_adds_logger_and_cleans_managed_handler(tmp_path: Path) -> None:
    settings = ApplicationSettings(log_level="ERROR", database_path=tmp_path / "logging.db")
    app = create_application(settings=settings)

    with TestClient(app):
        assert hasattr(app.state, "logger")
        logger = app.state.logger
        assert logger.level == 40
        assert any(isinstance(handler, ManagedStreamHandler) for handler in logger.handlers)

    assert not any(isinstance(handler, ManagedStreamHandler) for handler in logger.handlers)


def test_application_instances_get_distinct_logger_names(tmp_path: Path) -> None:
    first = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "first-logger.db")
    )
    second = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "second-logger.db")
    )

    with TestClient(first), TestClient(second):
        assert first.state.logger.name != second.state.logger.name


def test_lifespan_emits_structured_startup_and_shutdown_events(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    settings = ApplicationSettings(environment="test", database_path=tmp_path / "events.db")
    app = create_application(settings=settings)

    with TestClient(app):
        pass

    events = project_events(capsys.readouterr().err)
    assert [event["event"] for event in events] == [
        "application.startup",
        "database.ready",
        "scheduler.ready",
        "scheduler.shutdown",
        "database.shutdown",
        "application.shutdown",
    ]
    assert [event["message"] for event in events] == [
        "Application startup",
        "Database ready",
        "Scheduler ready",
        "Scheduler shutdown",
        "Database shutdown",
        "Application shutdown",
    ]
    assert events[0]["environment"] == "test"
    assert events[-1]["environment"] == "test"
    assert events[1]["journal_mode"] == "wal"
    assert events[2]["running"] is True
    assert events[2]["job_count"] == 0
    assert events[2]["timezone"] == "UTC"
    assert events[3]["running"] is False


def test_project_and_custom_lifespan_order_is_composed(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.logger.info("custom startup", extra={"event": "custom.startup"})
        yield
        app.state.logger.info("custom shutdown", extra={"event": "custom.shutdown"})

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "composed.db"),
    )

    with TestClient(app):
        pass

    events = [event["event"] for event in project_events(capsys.readouterr().err)]
    assert events == [
        "application.startup",
        "database.ready",
        "scheduler.ready",
        "custom.startup",
        "custom.shutdown",
        "scheduler.shutdown",
        "database.shutdown",
        "application.shutdown",
    ]


def test_custom_lifespan_exception_still_cleans_project_handler(tmp_path: Path) -> None:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        raise RuntimeError("custom shutdown failure")

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "exception.db"),
    )

    with pytest.raises(RuntimeError), TestClient(app):
        pass

    assert not any(isinstance(handler, ManagedStreamHandler) for handler in app.state.logger.handlers)


def test_importing_main_does_not_emit_logs_or_create_files(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    result = subprocess.run(
        [sys.executable, "-c", "import xianyu_system.main"],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == ""
    assert result.stderr == ""
    assert not (tmp_path / "logs").exists()
    for pattern in ["*.log", "*.db", "*.sqlite", "*.sqlite3"]:
        assert list(tmp_path.glob(pattern)) == []



def test_create_application_does_not_create_database_immediately(tmp_path: Path) -> None:
    path = tmp_path / "not-created.db"
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=path)
    )

    assert not path.exists()
    assert not hasattr(app.state, "database")


def test_database_lifespan_initializes_session_and_cleans_up(tmp_path: Path) -> None:
    path = tmp_path / "lifespan.db"
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=path)
    )

    assert not hasattr(app.state, "database")
    with TestClient(app):
        assert isinstance(app.state.database, DatabaseResources)
        assert path.exists()
        with app.state.database.engine.connect() as connection:
            assert str(connection.exec_driver_sql("PRAGMA journal_mode").scalar_one()).lower() == "wal"
        with open_session(app.state.database) as session:
            assert session.execute(text("SELECT 1")).scalar_one() == 1

    assert app.state.database is None
    path.unlink()
    assert not path.exists()


def test_create_application_does_not_create_or_start_scheduler_immediately(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "not-started.db")
    )

    assert not hasattr(app.state, "scheduler")


def test_scheduler_lifespan_starts_and_stops_with_no_jobs(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "scheduler.db")
    )

    with TestClient(app):
        assert isinstance(app.state.scheduler, BackgroundScheduler)
        assert app.state.scheduler.running is True
        assert app.state.scheduler.get_jobs() == []

    assert app.state.scheduler is None


def test_application_instances_use_isolated_scheduler_resources(tmp_path: Path) -> None:
    first = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "first-scheduler.db")
    )
    second = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "second-scheduler.db")
    )

    with TestClient(first), TestClient(second):
        assert first.state.scheduler is not second.state.scheduler
        assert first.state.scheduler.running is True
        assert second.state.scheduler.running is True
        assert first.state.scheduler.get_jobs() == []
        assert second.state.scheduler.get_jobs() == []


def test_custom_lifespan_can_use_scheduler_during_startup_and_shutdown(tmp_path: Path) -> None:
    events: list[str] = []

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        assert app.state.scheduler.running is True
        assert app.state.scheduler.get_jobs() == []
        events.append("custom-startup-scheduler-ready")
        yield
        assert app.state.scheduler.running is True
        assert app.state.scheduler.get_jobs() == []
        events.append("custom-shutdown-scheduler-ready")

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "custom-scheduler.db"),
    )

    with TestClient(app):
        assert events == ["custom-startup-scheduler-ready"]

    assert events == ["custom-startup-scheduler-ready", "custom-shutdown-scheduler-ready"]
    assert app.state.scheduler is None


def test_application_startup_does_not_automatically_create_scheduler_tables(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "scheduler-tables.db")
    )

    with TestClient(app):
        assert get_current_revision(app.state.database) is None
        assert set(inspect(app.state.database.engine).get_table_names()) == set()
        assert app.state.scheduler.get_jobs() == []

    assert app.state.database is None
    assert app.state.scheduler is None


def test_custom_lifespan_can_use_database_during_startup_and_shutdown(tmp_path: Path) -> None:
    events: list[str] = []

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        with open_session(app.state.database) as session:
            assert session.execute(text("SELECT 1")).scalar_one() == 1
        events.append("custom-startup-db-ready")
        yield
        with open_session(app.state.database) as session:
            assert session.execute(text("SELECT 1")).scalar_one() == 1
        events.append("custom-shutdown-db-ready")

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "custom-db.db"),
    )

    with TestClient(app):
        assert events == ["custom-startup-db-ready"]

    assert events == ["custom-startup-db-ready", "custom-shutdown-db-ready"]
    assert app.state.database is None


def test_application_instances_use_isolated_database_resources(tmp_path: Path) -> None:
    first = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "first-app.db")
    )
    second = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "second-app.db")
    )

    with TestClient(first), TestClient(second):
        assert first.state.database is not second.state.database
        assert first.state.database.engine is not second.state.database.engine
        assert first.state.database.session_factory is not second.state.database.session_factory
        assert first.state.database.path != second.state.database.path


def test_custom_lifespan_exception_still_disposes_database(tmp_path: Path) -> None:
    path = tmp_path / "custom-failure.db"

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        raise RuntimeError("custom shutdown failure")

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=path),
    )

    with pytest.raises(RuntimeError), TestClient(app):
        pass

    assert app.state.database is None
    path.unlink()
    assert not path.exists()


def test_database_initialization_failure_cleans_logging_and_skips_custom_lifespan(
    tmp_path: Path,
) -> None:
    events: list[str] = []

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        events.append("custom-startup")
        yield
        events.append("custom-shutdown")

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path),
    )

    with pytest.raises(ValueError), TestClient(app):
        pass

    assert events == []
    assert app.state.database is None
    assert not any(isinstance(handler, ManagedStreamHandler) for handler in app.state.logger.handlers)


def test_scheduler_start_failure_disposes_database_and_skips_custom_lifespan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    events: list[str] = []
    path = tmp_path / "scheduler-start-failure.db"

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        events.append("custom-startup")
        yield
        events.append("custom-shutdown")

    def fail_start(_: BackgroundScheduler) -> None:
        raise RuntimeError("scheduler start failure")

    monkeypatch.setattr("xianyu_system.application.start_scheduler", fail_start)
    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=path),
    )

    with pytest.raises(RuntimeError, match="scheduler start failure"), TestClient(app):
        pass

    assert events == []
    assert app.state.database is None
    assert app.state.scheduler is None
    assert not any(isinstance(handler, ManagedStreamHandler) for handler in app.state.logger.handlers)
    path.unlink()
    assert not path.exists()


def test_scheduler_shutdown_failure_still_disposes_database_and_logging(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = tmp_path / "scheduler-shutdown-failure.db"

    def fail_shutdown(_: BackgroundScheduler) -> None:
        raise RuntimeError("scheduler shutdown failure")

    monkeypatch.setattr("xianyu_system.application.shutdown_scheduler", fail_shutdown)
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=path),
    )

    with pytest.raises(RuntimeError, match="scheduler shutdown failure"), TestClient(app):
        assert app.state.scheduler.running is True

    assert app.state.database is None
    assert app.state.scheduler is None
    assert not any(isinstance(handler, ManagedStreamHandler) for handler in app.state.logger.handlers)
    path.unlink()
    assert not path.exists()


def test_importing_main_does_not_create_default_database_file(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    subprocess.run(
        [sys.executable, "-c", "import xianyu_system.main"],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert not (tmp_path / "data").exists()
    for pattern in ["*.db", "*.sqlite", "*.sqlite3"]:
        assert list(tmp_path.glob(pattern)) == []


def test_application_startup_does_not_automatically_run_alembic(tmp_path: Path) -> None:
    path = tmp_path / "no-auto-migration.db"
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=path)
    )

    with TestClient(app):
        assert path.exists()
        assert get_current_revision(app.state.database) is None
        with app.state.database.engine.connect() as connection:
            tables = connection.exec_driver_sql(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).scalars().all()
        assert "alembic_version" not in set(tables)

    assert app.state.database is None


def test_custom_lifespan_can_explicitly_run_alembic_upgrade(tmp_path: Path) -> None:
    events: list[str] = []

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        assert get_current_revision(app.state.database) is None
        upgrade_database(app.state.database)
        assert get_current_revision(app.state.database) == BASELINE_REVISION
        events.append("explicit-migration")
        yield
        assert get_current_revision(app.state.database) == BASELINE_REVISION

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "explicit.db"),
    )

    with TestClient(app):
        assert events == ["explicit-migration"]

    assert app.state.database is None


def test_explicit_migration_does_not_break_logging_lifespan(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        upgrade_database(app.state.database)
        app.state.logger.info("migration complete", extra={"event": "migration.complete"})
        yield

    app = create_application(
        lifespan=lifespan,
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "logging-migration.db"),
    )

    with TestClient(app):
        pass

    events = [event["event"] for event in project_events(capsys.readouterr().err)]
    assert events == [
        "application.startup",
        "database.ready",
        "scheduler.ready",
        "migration.complete",
        "scheduler.shutdown",
        "database.shutdown",
        "application.shutdown",
    ]
