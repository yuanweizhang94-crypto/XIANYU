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

from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
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


def test_custom_lifespan_runs_startup_and_shutdown_once() -> None:
    events: list[str] = []

    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        events.append("startup")
        yield
        events.append("shutdown")

    app = create_application(lifespan=lifespan)

    with TestClient(app):
        assert events == ["startup"]

    assert events == ["startup", "shutdown"]


def test_settings_injection_preserves_custom_lifespan_behavior() -> None:
    events: list[str] = []
    supplied_settings = ApplicationSettings(app_title="LIFESPAN APP")

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


def test_lifespan_state_is_isolated_per_application() -> None:
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

    first = create_application(lifespan=first_lifespan)
    second = create_application(lifespan=second_lifespan)

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


def test_logging_lifespan_adds_logger_and_cleans_managed_handler() -> None:
    settings = ApplicationSettings(log_level="ERROR")
    app = create_application(settings=settings)

    with TestClient(app):
        assert hasattr(app.state, "logger")
        logger = app.state.logger
        assert logger.level == 40
        assert any(isinstance(handler, ManagedStreamHandler) for handler in logger.handlers)

    assert not any(isinstance(handler, ManagedStreamHandler) for handler in logger.handlers)


def test_application_instances_get_distinct_logger_names() -> None:
    first = create_application()
    second = create_application()

    with TestClient(first), TestClient(second):
        assert first.state.logger.name != second.state.logger.name


def test_lifespan_emits_structured_startup_and_shutdown_events(capsys: pytest.CaptureFixture[str]) -> None:
    settings = ApplicationSettings(environment="test")
    app = create_application(settings=settings)

    with TestClient(app):
        pass

    events = [json.loads(line) for line in capsys.readouterr().err.splitlines()]
    assert [event["event"] for event in events] == [
        "application.startup",
        "application.shutdown",
    ]
    assert [event["message"] for event in events] == [
        "Application startup",
        "Application shutdown",
    ]
    assert all(event["environment"] == "test" for event in events)


def test_project_and_custom_lifespan_order_is_composed(capsys: pytest.CaptureFixture[str]) -> None:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        app.state.logger.info("custom startup", extra={"event": "custom.startup"})
        yield
        app.state.logger.info("custom shutdown", extra={"event": "custom.shutdown"})

    app = create_application(lifespan=lifespan)

    with TestClient(app):
        pass

    events = [json.loads(line)["event"] for line in capsys.readouterr().err.splitlines()]
    assert events == [
        "application.startup",
        "custom.startup",
        "custom.shutdown",
        "application.shutdown",
    ]


def test_custom_lifespan_exception_still_cleans_project_handler() -> None:
    @asynccontextmanager
    async def lifespan(_: FastAPI) -> AsyncIterator[None]:
        yield
        raise RuntimeError("custom shutdown failure")

    app = create_application(lifespan=lifespan)

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
