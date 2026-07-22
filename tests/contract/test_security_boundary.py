from __future__ import annotations

import json
import socket
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings

ROOT = Path(__file__).resolve().parents[2]
SYNTHETIC_SECRETS = {
    "UNSUPPORTED_TOKEN": "synthetic-token-value-0001",
    "WECOM_COOKIE": "synthetic-cookie-value-0002",
    "AI_PROVIDER_SECRET": "synthetic-secret-value-0003",
    "BROWSER_PROFILE": "synthetic-profile-value-0004",
}
SAFE_RUNTIME_FILES = [
    "app/xianyu_system/web/templates/base.html",
    "app/xianyu_system/web/templates/index.html",
    "app/xianyu_system/web/static/styles.css",
    "app/xianyu_system/web/static/vendor/htmx.LICENSE.txt",
]
APP_SOURCE_FILES = [
    path
    for path in (ROOT / "app/xianyu_system").rglob("*.py")
    if "__pycache__" not in path.parts
]


def assert_no_synthetic_values(payload: object) -> None:
    text = json.dumps(payload, ensure_ascii=False, default=str) if not isinstance(payload, str) else payload
    for secret in SYNTHETIC_SECRETS.values():
        assert secret not in text


def test_synthetic_credentials_are_not_loaded_or_exposed(monkeypatch: pytest.MonkeyPatch, tmp_path: Path, capsys) -> None:
    for key, value in SYNTHETIC_SECRETS.items():
        monkeypatch.setenv(key, value)
    settings = ApplicationSettings(environment="test", database_path=tmp_path / "safe.db")
    app = create_application(settings=settings)

    assert_no_synthetic_values(settings.model_dump())
    with TestClient(app) as client:
        responses = [
            client.get("/"),
            client.get("/health"),
            client.get("/openapi.json"),
            client.get("/static/styles.css"),
            client.get("/static/vendor/htmx.LICENSE.txt"),
            client.get("/missing-route"),
            client.post("/health"),
        ]
    for response in responses:
        assert_no_synthetic_values(response.text)
        if response.headers.get("content-type", "").startswith("application/json"):
            assert_no_synthetic_values(response.json())
    assert_no_synthetic_values(capsys.readouterr().err)


def test_in_process_routes_do_not_attempt_external_socket_connections(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    attempts: list[str] = []
    original_connect = socket.socket.connect

    def blocked_connect(self: socket.socket, address: object) -> None:
        host = address[0] if isinstance(address, tuple) and address else None
        if host in {"127.0.0.1", "::1", "localhost"}:
            return original_connect(self, address)
        attempts.append(repr(address))
        raise AssertionError(f"external socket attempted: {address!r}")

    monkeypatch.setattr(socket.socket, "connect", blocked_connect)
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "network.db")
    )

    with TestClient(app) as client:
        assert client.get("/").status_code == 200
        assert client.get("/health").status_code == 200
        assert client.get("/static/styles.css").status_code == 200
        assert client.get("/static/vendor/htmx.min.js").status_code == 200

    monkeypatch.setattr(socket.socket, "connect", original_connect)
    assert attempts == []


def test_runtime_http_surface_is_read_only_and_does_not_accept_business_writes(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "readonly.db")
    )

    with TestClient(app) as client:
        for path in ["/", "/health"]:
            for method in ["POST", "PUT", "PATCH", "DELETE"]:
                response = client.request(method, path, json={"payload": "not accepted"})
                assert response.status_code == 405
        assert client.get("/static/").status_code in {404, 405}
        assert client.post("/static/styles.css").status_code in {404, 405}
        assert client.get("/messages").status_code == 404
        assert client.post("/publish").status_code == 404


def test_templates_and_first_party_static_files_have_no_external_or_mutating_dependencies() -> None:
    combined = "\n".join((ROOT / relative).read_text(encoding="utf-8").lower() for relative in SAFE_RUNTIME_FILES)
    for forbidden in [
        "https://",
        "http://",
        "//cdn",
        "unpkg",
        "fonts.googleapis",
        "analytics",
        "document.cookie",
        "localstorage",
        "sessionstorage",
        "hx-post",
        "hx-put",
        "hx-patch",
        "hx-delete",
        "hx-ws",
        "hx-sse",
        "form action=",
    ]:
        assert forbidden not in combined
    assert "hx-get" in combined
    assert "health_path" in combined


def test_core_source_contains_no_external_business_integration_or_scheduler_jobs() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in APP_SOURCE_FILES)
    for forbidden in [
        "playwright",
        "selenium",
        "browser profile",
        "wecom",
        "wechat",
        "openai",
        "langchain",
        "requests" + ".",
        "httpx" + ".",
        "urllib" + ".request",
        "websocket",
        "__tablename__",
        "mapped_column",
        "metadata.create_all",
        "metadata.drop_all",
        "add_job(",
        "scheduled_job(",
        "cookie=",
        "token=",
        "password=",
        "secret=",
    ]:
        assert forbidden not in combined
