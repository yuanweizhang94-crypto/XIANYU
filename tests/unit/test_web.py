from __future__ import annotations

import base64
import hashlib
import os
import subprocess
import sys
from pathlib import Path

from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.testclient import TestClient
from starlette.routing import Mount

from xianyu_system.api.health import HEALTH_PATH
from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.web.router import (
    HOME_PATH,
    HOME_ROUTE_NAME,
    STATIC_PATH,
    STATIC_ROUTE_NAME,
    STATIC_URL_PATH,
    TEMPLATES_PATH,
    WEB_PACKAGE_PATH,
    create_templates,
    register_web,
    router,
)

ROOT = Path(__file__).resolve().parents[2]
HTMX_PATH = STATIC_PATH / "vendor" / "htmx.min.js"
HTMX_LICENSE_PATH = STATIC_PATH / "vendor" / "htmx.LICENSE.txt"
HTMX_SHA384 = "H5SrcfygHmAuTDZphMHqBJLc3FhssKjG7w/CeCpFReSfwBWDTKpkzPP8c+cLsK+V"
FORBIDDEN_WEB_TERMS = [
    "login",
    "account",
    "products",
    "messages",
    "publish",
    "schedule",
    "wecom",
    "openai",
    "playwright",
    "selenium",
    "cookie",
    "token",
    "secret",
    "password",
]


def route_paths(app: FastAPI) -> set[str]:
    return {str(route.path) for route in app.routes if hasattr(route, "path")}


def home_route(app: FastAPI) -> APIRoute:
    routes = [route for route in app.routes if isinstance(route, APIRoute) and route.path == HOME_PATH]
    assert len(routes) == 1
    return routes[0]


def static_mount(app: FastAPI) -> Mount:
    mounts = [route for route in app.routes if isinstance(route, Mount) and route.path == STATIC_URL_PATH]
    assert len(mounts) == 1
    return mounts[0]


def test_web_package_paths_are_package_relative_and_existing(monkeypatch) -> None:
    monkeypatch.chdir(ROOT.parent)

    assert WEB_PACKAGE_PATH.is_absolute()
    assert TEMPLATES_PATH.is_dir()
    assert STATIC_PATH.is_dir()
    assert TEMPLATES_PATH.parent == WEB_PACKAGE_PATH
    assert STATIC_PATH.parent == WEB_PACKAGE_PATH
    assert WEB_PACKAGE_PATH.name == "web"
    assert WEB_PACKAGE_PATH.parent.name == "xianyu_system"
    assert not (ROOT / "templates").exists()
    assert not (ROOT / "static").exists()
    assert not (ROOT / "app/xianyu_system/templates").exists()
    assert not (ROOT / "app/xianyu_system/static").exists()


def test_web_router_defines_only_home_route_and_public_exports() -> None:
    assert HOME_PATH == "/"
    assert STATIC_URL_PATH == "/static"
    assert STATIC_ROUTE_NAME == "static"
    assert HOME_ROUTE_NAME == "home"
    routes = [route for route in router.routes if isinstance(route, APIRoute)]
    assert len(routes) == 1
    assert routes[0].path == HOME_PATH
    assert routes[0].methods == {"GET"}
    assert routes[0].include_in_schema is False
    assert routes[0].name == HOME_ROUTE_NAME


def test_create_templates_returns_isolated_autoescaping_environments() -> None:
    first = create_templates()
    second = create_templates()

    assert isinstance(first, Jinja2Templates)
    assert isinstance(second, Jinja2Templates)
    assert first is not second
    assert first.env is not second.env
    rendered = first.env.from_string("{{ value }}").render(value="<Core>")
    assert "&lt;Core&gt;" in rendered
    assert "<Core>" not in rendered


def test_register_web_adds_isolated_templates_static_mount_and_home_route() -> None:
    first = create_application()
    second = create_application()

    assert isinstance(first.state.web_templates, Jinja2Templates)
    assert isinstance(second.state.web_templates, Jinja2Templates)
    assert first.state.web_templates is not second.state.web_templates
    assert first.state.web_templates.env is not second.state.web_templates.env

    first_mount = static_mount(first)
    second_mount = static_mount(second)
    assert first_mount is not second_mount
    assert isinstance(first_mount.app, StaticFiles)
    assert isinstance(second_mount.app, StaticFiles)
    assert first_mount.name == STATIC_ROUTE_NAME
    assert first_mount.app is not second_mount.app
    assert first_mount.app.directory == str(STATIC_PATH)
    assert first_mount.app.html is False
    assert first_mount.app.follow_symlink is False
    assert home_route(first).include_in_schema is False
    assert route_paths(first) >= {HOME_PATH, STATIC_URL_PATH, HEALTH_PATH}
    assert set(first.openapi()["paths"]) == {HEALTH_PATH}


def test_register_web_can_be_called_on_plain_app_once() -> None:
    app = FastAPI()
    app.state.settings = ApplicationSettings(environment="test")

    register_web(app)

    assert isinstance(app.state.web_templates, Jinja2Templates)
    assert static_mount(app).app.directory == str(STATIC_PATH)
    assert home_route(app).path == HOME_PATH
    assert app.openapi()["paths"] == {}


def test_home_renders_safe_core_page_without_auto_health_probe(tmp_path: Path, monkeypatch) -> None:
    calls: list[str] = []

    def fake_collect_health(_: FastAPI) -> None:
        calls.append("health")

    monkeypatch.setattr("xianyu_system.api.health.collect_health", fake_collect_health)
    app = create_application(
        settings=ApplicationSettings(
            environment="test",
            app_title="<XIANYU Core>",
            app_version="2.0.10",
            database_path=tmp_path / "home.db",
        )
    )

    with TestClient(app) as client:
        response = client.get(HOME_PATH)
        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html; charset=utf-8")
        body = response.text
        assert "&lt;XIANYU Core&gt;" in body
        assert "<XIANYU Core>" not in body
        assert "2.0.10" in body
        assert "test" in body
        assert '/static/styles.css' in body
        assert '/static/vendor/htmx.min.js' in body
        assert f'hx-get="{HEALTH_PATH}"' in body
        assert 'hx-trigger="click"' in body
        assert "Health not requested." in body
        assert "cdn.jsdelivr" not in body
        assert "unpkg" not in body
        assert "fonts.googleapis" not in body
        assert "|safe" not in body
        assert calls == []


def test_home_route_accepts_only_get_and_stays_out_of_openapi(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "methods.db")
    )

    with TestClient(app) as client:
        assert client.get(HOME_PATH).status_code == 200
        assert client.post(HOME_PATH).status_code == 405
        assert client.put(HOME_PATH).status_code == 405
        assert client.patch(HOME_PATH).status_code == 405
        assert client.delete(HOME_PATH).status_code == 405
        assert client.get(HEALTH_PATH).status_code == 200

    assert set(app.openapi()["paths"]) == {HEALTH_PATH}


def test_static_assets_are_served_locally_with_license(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "static.db")
    )

    with TestClient(app) as client:
        css = client.get("/static/styles.css")
        js = client.get("/static/vendor/htmx.min.js")
        license_response = client.get("/static/vendor/htmx.LICENSE.txt")
        directory = client.get("/static/")

    assert css.status_code == 200
    assert js.status_code == 200
    assert license_response.status_code == 200
    assert directory.status_code in {404, 405}
    assert "body" in css.text
    assert "BSD 2-Clause" in license_response.text


def test_htmx_asset_is_pinned_unmodified_and_referenced_by_sri() -> None:
    digest = base64.b64encode(hashlib.sha384(HTMX_PATH.read_bytes()).digest()).decode()
    base = (TEMPLATES_PATH / "base.html").read_text(encoding="utf-8")
    script = HTMX_PATH.read_text(encoding="utf-8")

    assert digest == HTMX_SHA384
    assert f"sha384-{HTMX_SHA384}" in base
    assert 'version:"2.0.10"' in script
    assert HTMX_LICENSE_PATH.is_file()
    assert "BSD 2-Clause" in HTMX_LICENSE_PATH.read_text(encoding="utf-8")


def test_templates_and_css_reference_no_external_resources_or_mutating_htmx() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            TEMPLATES_PATH / "base.html",
            TEMPLATES_PATH / "index.html",
            STATIC_PATH / "styles.css",
        ]
    )
    assert "https://" not in combined
    assert "http://" not in combined
    assert "//cdn" not in combined
    assert "unpkg" not in combined
    assert "fonts.googleapis" not in combined
    assert "@import" not in combined
    assert "|safe" not in combined
    for forbidden in ["hx-post", "hx-put", "hx-patch", "hx-delete", "hx-ws", "hx-sse"]:
        assert forbidden not in combined
    assert 'hx-get="{{ health_path }}"' in combined


def test_web_source_has_no_infrastructure_or_business_access() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in [
            ROOT / "app/xianyu_system/web/__init__.py",
            ROOT / "app/xianyu_system/web/router.py",
            TEMPLATES_PATH / "base.html",
            TEMPLATES_PATH / "index.html",
        ]
    )
    for forbidden in [
        "initialize_database",
        "create_database_engine",
        "upgrade_database",
        "downgrade_database",
        "open_session",
        "add_job",
        "remove_job",
        "requests.",
        "httpx.",
        "urllib.",
        "socket.",
    ]:
        assert forbidden not in combined
    for forbidden in FORBIDDEN_WEB_TERMS:
        assert forbidden not in combined


def test_importing_web_modules_has_no_runtime_file_or_service_side_effects(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    result = subprocess.run(
        [sys.executable, "-c", "import xianyu_system.web; import xianyu_system.web.router"],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stdout == ""
    assert result.stderr == ""
    assert list(tmp_path.glob("*.db")) == []
    assert not (tmp_path / "logs").exists()
