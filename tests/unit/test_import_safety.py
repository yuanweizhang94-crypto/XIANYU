from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
IMPORT_MODULES = [
    "xianyu_system",
    "xianyu_system.application",
    "xianyu_system.main",
    "xianyu_system.core.config",
    "xianyu_system.core.logging",
    "xianyu_system.core.database",
    "xianyu_system.core.scheduler",
    "xianyu_system.api.router",
    "xianyu_system.api.health",
    "xianyu_system.web.router",
    "xianyu_system.worker.account",
    "xianyu_system.worker.account.domain",
    "xianyu_system.worker.message",
    "xianyu_system.worker.message.domain",
    "xianyu_system.worker.message.transport",
    "xianyu_system.reply",
    "xianyu_system.reply.domain",
]
FORBIDDEN_ARTIFACT_GLOBS = [
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "*.log",
    "data/*",
    "logs/*",
]


def run_import_probe(tmp_path: Path, modules: list[str]) -> dict[str, Any]:
    env = os.environ.copy()
    pythonpath = [str(ROOT / "app"), str(ROOT)]
    if env.get("PYTHONPATH"):
        pythonpath.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath)
    env["XIANYU_DATABASE_PATH"] = str(tmp_path / "env-db-should-not-exist.db")

    script = """
import importlib
import json
import logging
import pathlib
import socket
import sys
import threading

modules = json.loads(sys.argv[1])
cwd = pathlib.Path.cwd()
root_logger = logging.getLogger()
before = {
    "cwd_files": sorted(path.name for path in cwd.iterdir()),
    "root_level": root_logger.level,
    "root_handlers": [id(handler) for handler in root_logger.handlers],
    "thread_names": sorted(thread.name for thread in threading.enumerate()),
}
connect_attempts = []
original_connect = socket.socket.connect


def blocked_connect(self, address):
    connect_attempts.append(repr(address))
    raise AssertionError(f"network connection attempted: {address!r}")


socket.socket.connect = blocked_connect
try:
    imported = [importlib.import_module(name).__name__ for name in modules]
    for name in modules:
        importlib.reload(sys.modules[name])
finally:
    socket.socket.connect = original_connect

from xianyu_system.core.database import Base
from xianyu_system.main import app

after = {
    "account_modules": sorted(
        name
        for name in sys.modules
        if name.startswith("xianyu_system.worker.account")
    ),
    "account_service_loaded": (
        "xianyu_system.worker.account.service" in sys.modules
    ),
    "account_persistence_loaded": (
        "xianyu_system.worker.account.persistence" in sys.modules
    ),
    "account_service_public": (
        "xianyu_system.worker.account" in sys.modules
        and "AccountService"
        in sys.modules["xianyu_system.worker.account"].__all__
    ),
    "message_modules": sorted(
        name
        for name in sys.modules
        if name.startswith("xianyu_system.worker.message")
    ),
    "message_service_loaded": (
        "xianyu_system.worker.message.service" in sys.modules
    ),
    "message_persistence_loaded": (
        "xianyu_system.worker.message.persistence" in sys.modules
    ),
    "message_worker_loaded": (
        "xianyu_system.worker.message.worker" in sys.modules
    ),
    "message_public_surface": (
        "xianyu_system.worker.message" in sys.modules
        and "Conversation"
        in sys.modules["xianyu_system.worker.message"].__all__
        and "MessageService"
        in sys.modules["xianyu_system.worker.message"].__all__
        and "MessageWorker"
        in sys.modules["xianyu_system.worker.message"].__all__
    ),
    "message_conversation_public": (
        "xianyu_system.worker.message" in sys.modules
        and "Conversation"
        in sys.modules["xianyu_system.worker.message"].__all__
    ),
    "message_service_public": (
        "xianyu_system.worker.message" in sys.modules
        and "MessageService"
        in sys.modules["xianyu_system.worker.message"].__all__
    ),
    "message_worker_public": (
        "xianyu_system.worker.message" in sys.modules
        and "MessageWorker"
        in sys.modules["xianyu_system.worker.message"].__all__
    ),
    "message_transport_public": (
        "xianyu_system.worker.message" in sys.modules
        and "SyntheticMessageDelivery"
        in sys.modules["xianyu_system.worker.message"].__all__
    ),
    "reply_modules": sorted(
        name
        for name in sys.modules
        if name.startswith("xianyu_system.reply")
    ),
    "reply_persistence_loaded": (
        "xianyu_system.reply.persistence" in sys.modules
    ),
    "reply_service_loaded": (
        "xianyu_system.reply.service" in sys.modules
    ),
    "reply_public_surface": (
        "xianyu_system.reply" in sys.modules
        and "ReplyDecision"
        in sys.modules["xianyu_system.reply"].__all__
        and "ReplyService"
        in sys.modules["xianyu_system.reply"].__all__
    ),
    "cwd_files": sorted(path.name for path in cwd.iterdir()),
    "root_level": root_logger.level,
    "root_handlers": [id(handler) for handler in root_logger.handlers],
    "thread_names": sorted(thread.name for thread in threading.enumerate()),
    "connect_attempts": connect_attempts,
    "metadata_tables": sorted(Base.metadata.tables),
    "has_database_state": hasattr(app.state, "database"),
    "has_scheduler_state": hasattr(app.state, "scheduler"),
    "has_logger_state": hasattr(app.state, "logger"),
    "has_templates_state": hasattr(app.state, "web_templates"),
    "imported": imported,
}
print(json.dumps({"before": before, "after": after}, sort_keys=True))
"""
    result = subprocess.run(
        [sys.executable, "-c", script, json.dumps(modules)],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stderr == ""
    return json.loads(result.stdout)


def test_core_module_imports_are_runtime_side_effect_free(tmp_path: Path) -> None:
    account_init_path = ROOT / "app" / "xianyu_system" / "worker" / "account" / "__init__.py"
    account_init_bytes = account_init_path.read_bytes()

    assert not account_init_bytes.startswith(b"\xef\xbb\xbf")
    assert account_init_bytes.startswith(
        b'"""Public surface for the local Xianyu account boundary.'
    )
    account_init_bytes.decode("utf-8")
    message_init_path = ROOT / "app" / "xianyu_system" / "worker" / "message" / "__init__.py"
    message_init_bytes = message_init_path.read_bytes()
    assert not message_init_bytes.startswith(b"\xef\xbb\xbf")
    assert message_init_bytes.startswith(b'"""Local synthetic message receiving boundary package.')
    message_init_bytes.decode("utf-8")
    reply_init_path = ROOT / "app" / "xianyu_system" / "reply" / "__init__.py"
    reply_init_bytes = reply_init_path.read_bytes()
    assert not reply_init_bytes.startswith(b"\xef\xbb\xbf")
    assert reply_init_bytes.startswith(
        b'"""Lazy public surface for the local deterministic Reply boundary.'
    )
    reply_init_bytes.decode("utf-8")

    report = run_import_probe(tmp_path, IMPORT_MODULES)

    assert report["after"]["imported"] == IMPORT_MODULES
    assert report["after"]["cwd_files"] == report["before"]["cwd_files"] == []
    assert report["after"]["root_level"] == report["before"]["root_level"]
    assert report["after"]["root_handlers"] == report["before"]["root_handlers"]
    assert report["after"]["thread_names"] == report["before"]["thread_names"]
    assert report["after"]["connect_attempts"] == []
    assert report["after"]["metadata_tables"] == []
    assert report["after"]["account_service_loaded"] is False
    assert report["after"]["account_persistence_loaded"] is False
    assert report["after"]["account_service_public"] is True
    assert "xianyu_system.worker.account" in report["after"]["account_modules"]
    assert "xianyu_system.worker.account.domain" in report["after"]["account_modules"]
    assert "xianyu_system.worker.account.service" not in report["after"]["account_modules"]
    assert "xianyu_system.worker.account.persistence" not in report["after"]["account_modules"]
    assert report["after"]["message_service_loaded"] is False
    assert report["after"]["message_persistence_loaded"] is False
    assert report["after"]["message_worker_loaded"] is False
    assert report["after"]["message_public_surface"] is True
    assert report["after"]["message_conversation_public"] is True
    assert report["after"]["message_service_public"] is True
    assert report["after"]["message_worker_public"] is True
    assert report["after"]["message_transport_public"] is True
    assert "xianyu_system.worker.message" in report["after"]["message_modules"]
    assert "xianyu_system.worker.message.domain" in report["after"]["message_modules"]
    assert "xianyu_system.worker.message.transport" in report["after"]["message_modules"]
    assert "xianyu_system.worker.message.service" not in report["after"]["message_modules"]
    assert "xianyu_system.worker.message.persistence" not in report["after"]["message_modules"]
    assert report["after"]["reply_persistence_loaded"] is False
    assert report["after"]["reply_service_loaded"] is False
    assert report["after"]["reply_public_surface"] is True
    assert "xianyu_system.reply" in report["after"]["reply_modules"]
    assert "xianyu_system.reply.domain" in report["after"]["reply_modules"]
    assert "xianyu_system.reply.persistence" not in report["after"]["reply_modules"]
    assert "xianyu_system.reply.service" not in report["after"]["reply_modules"]
    assert report["after"]["has_database_state"] is False
    assert report["after"]["has_scheduler_state"] is False
    assert report["after"]["has_logger_state"] is False
    assert report["after"]["has_templates_state"] is True


def test_importing_main_ignores_environment_database_path_until_lifespan(tmp_path: Path) -> None:
    env_database = tmp_path / "from-env.db"
    report = run_import_probe(tmp_path, ["xianyu_system.main"])

    assert report["after"]["connect_attempts"] == []
    assert not env_database.exists()
    for pattern in FORBIDDEN_ARTIFACT_GLOBS:
        assert list(tmp_path.glob(pattern)) == []


def test_import_safety_test_file_has_no_skip_or_network_client_escape_hatches() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    forbidden_patterns = [
        "pytest" + ".skip",
        "pytest" + ".xfail",
        "pytest.mark" + ".skip",
        "pytest.mark" + ".xfail",
        "time" + ".sleep",
        "asyncio" + ".sleep",
        "requests" + ".",
        "httpx" + ".get",
        "httpx" + ".post",
        "httpx" + ".put",
        "httpx" + ".patch",
        "httpx" + ".delete",
        "urllib" + ".request",
    ]
    for forbidden in forbidden_patterns:
        assert forbidden not in source
