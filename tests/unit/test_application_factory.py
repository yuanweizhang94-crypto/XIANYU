from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from xianyu_system.application import APP_TITLE, APP_VERSION, create_application

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


def route_paths(app: FastAPI) -> set[str]:
    return {str(route.path) for route in app.routes}


def test_create_application_returns_fastapi_instance() -> None:
    assert isinstance(create_application(), FastAPI)


def test_repeated_creation_returns_isolated_instances() -> None:
    first = create_application()
    second = create_application()

    assert first is not second
    assert first.state is not second.state


def test_application_metadata_is_stable() -> None:
    app = create_application()

    assert app.title == APP_TITLE == "XIANYU"
    assert app.version == APP_VERSION == "0.1.0"


def test_application_has_no_custom_business_routes() -> None:
    app = create_application()

    assert route_paths(app) <= DEFAULT_FASTAPI_ROUTE_PATHS
    assert app.openapi()["paths"] == {}


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
