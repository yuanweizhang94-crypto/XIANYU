from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

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
]
FORBIDDEN_ARTIFACT_GLOBS = [
    "*.db",
    "*.sqlite",
    "*.sqlite3",
    "*.log",
    "data/*",
    "logs/*",
]


def run_import_probe(tmp_path: Path, modules: list[str]) -> dict[str, object]:
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
    report = run_import_probe(tmp_path, IMPORT_MODULES)

    assert report["after"]["imported"] == IMPORT_MODULES
    assert report["after"]["cwd_files"] == report["before"]["cwd_files"] == []
    assert report["after"]["root_level"] == report["before"]["root_level"]
    assert report["after"]["root_handlers"] == report["before"]["root_handlers"]
    assert report["after"]["thread_names"] == report["before"]["thread_names"]
    assert report["after"]["connect_attempts"] == []
    assert report["after"]["metadata_tables"] == []
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
