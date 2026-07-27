from __future__ import annotations

import builtins
import os
import socket
import subprocess
import threading
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from typing import Any

import pytest

from xianyu_system.core.database import dispose_database, initialize_database, upgrade_database
from xianyu_system.worker.publish.domain import (
    ListingDraft,
    ListingDraftLifecycle,
    PublishAuthorizationState,
    PublishEvaluationContext,
    PublishRequest,
    PublishRiskState,
)
from xianyu_system.worker.publish.service import PublishService

ROOT = Path(__file__).resolve().parents[2]
PUBLISH_ROOT = ROOT / "app" / "xianyu_system" / "worker" / "publish"
NOW = datetime(2026, 1, 1, tzinfo=UTC)
DRAFT_ID = "00000000-0000-4000-8000-000000000101"
REQUEST_ID = "00000000-0000-4000-8000-000000000201"


def source_texts() -> dict[str, str]:
    return {path.name: path.read_text(encoding="utf-8") for path in PUBLISH_ROOT.glob("*.py")}


def draft(**overrides: Any) -> ListingDraft:
    values: dict[str, Any] = {
        "draft_id": DRAFT_ID,
        "revision": 1,
        "title": "synthetic title",
        "description": "synthetic description",
        "category_reference": "synthetic-category",
        "price": Decimal("12.34"),
        "stock": 1,
        "location_reference": "synthetic-location",
        "media_metadata": {"a": "synthetic"},
        "seller_profile_reference": "synthetic-profile",
        "lifecycle_state": ListingDraftLifecycle.VALIDATED,
        "created_at": NOW,
        "updated_at": NOW,
    }
    values.update(overrides)
    return ListingDraft(**values)


def request(**overrides: Any) -> PublishRequest:
    values: dict[str, Any] = {
        "request_id": REQUEST_ID,
        "draft_id": DRAFT_ID,
        "draft_revision": 1,
        "idempotency_key": "idem-key",
        "requested_at": NOW,
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "correlation_id": "corr-id",
    }
    values.update(overrides)
    return PublishRequest(**values)


def context(**overrides: Any) -> PublishEvaluationContext:
    values: dict[str, Any] = {
        "authorization_state": PublishAuthorizationState.AUTHORIZED,
        "risk_state": PublishRiskState.CLEAR,
        "synthetic_fixture": True,
        "request_time": NOW,
        "local_profile_reference": "synthetic-profile",
    }
    values.update(overrides)
    return PublishEvaluationContext(**values)


def test_publish_public_surface_is_lazy_and_excludes_platform_execution() -> None:
    init_source = (PUBLISH_ROOT / "__init__.py").read_text(encoding="utf-8")

    assert "__getattr__" in init_source
    assert "PublishService" in init_source
    for marker in ["publish_listing", "upload_media", "open_browser", "xianyu_client"]:
        assert marker not in init_source


def test_publish_sources_have_no_external_integration_or_sensitive_storage() -> None:
    joined = "\n".join(source_texts().values()).lower()
    forbidden_markers = [
        "playwright",
        "selenium",
        "httpx",
        "aiohttp",
        "websocket",
        "urllib.request",
        "socket.",
        "subprocess",
        "open_browser",
        "upload_media",
        "publish_listing",
        "xianyu_client",
        "browser_profile",
        "session_material",
        "credential_value",
        "api_key",
        "access_token",
        "customer_data",
        "raw_payload",
        "metadata_json",
    ]
    for marker in forbidden_markers:
        assert marker not in joined


def test_publish_migration_has_no_seed_data_platform_calls_or_sensitive_columns() -> None:
    migration = (ROOT / "migrations" / "versions" / "0005_xianyu_publish_boundary.py").read_text(
        encoding="utf-8"
    )
    lowered = migration.lower()
    assert "bulk_insert" not in lowered
    assert "insert(" not in lowered
    for marker in [
        "playwright",
        "httpx",
        "websocket",
        "cookie",
        "token",
        "secret",
        "password",
        "browser profile",
        "raw_payload",
        "listing_text",
        "media_blob",
    ]:
        assert marker not in lowered


def test_publish_operations_make_no_network_subprocess_file_or_thread_calls(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    resources = initialize_database(tmp_path / "publish-security.db")
    upgrade_database(resources)
    before_threads = sorted(thread.name for thread in threading.enumerate())
    connect_attempts: list[object] = []

    def fail_connect(self: socket.socket, address: object) -> None:
        connect_attempts.append(address)
        raise AssertionError(f"network attempted: {address!r}")

    def fail_run(*args: object, **kwargs: object) -> object:
        raise AssertionError("subprocess attempted")

    def fail_open(*args: object, **kwargs: object) -> object:
        raise AssertionError("file access attempted")

    monkeypatch.setattr(socket.socket, "connect", fail_connect)
    monkeypatch.setattr(subprocess, "run", fail_run)
    monkeypatch.setattr(builtins, "open", fail_open)
    monkeypatch.setattr(os, "system", lambda command: pytest.fail(f"system attempted: {command}"))
    try:
        decision = PublishService(resources.session_factory).evaluate(draft(), request(), context())
        assert decision.reason_code.name == "READY_FOR_SEPARATELY_AUTHORIZED_BOUNDARY"
        assert connect_attempts == []
        assert sorted(thread.name for thread in threading.enumerate()) == before_threads
    finally:
        dispose_database(resources)


def test_publish_errors_do_not_expose_payload_values_or_database_details(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "publish-errors.db")
    upgrade_database(resources)
    try:
        decision = PublishService(resources.session_factory).evaluate(
            draft(title="sensitive synthetic title"),
            request(synthetic_fixture=False),
            context(),
        )
        rendered = repr(decision).lower()
        for raw in [
            "sensitive synthetic title",
            "synthetic description",
            "sqlite",
            "select ",
            "raw payload",
        ]:
            assert raw not in rendered
    finally:
        dispose_database(resources)
