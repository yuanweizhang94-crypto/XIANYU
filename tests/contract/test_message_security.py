from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
from sqlalchemy.exc import SQLAlchemyError

from xianyu_system.core.database import (
    dispose_database,
    initialize_database,
    upgrade_database,
)
from xianyu_system.worker.message.domain import MessagePersistenceError
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

ROOT = Path(__file__).resolve().parents[2]
MESSAGE_TEST_PATHS = [
    ROOT / "tests" / "unit" / "test_message_domain.py",
    ROOT / "tests" / "unit" / "test_message_service.py",
    ROOT / "tests" / "unit" / "test_message_worker.py",
    ROOT / "tests" / "contract" / "test_message_persistence.py",
    ROOT / "tests" / "contract" / "test_message_security.py",
    ROOT
    / "changes"
    / "active"
    / "CHG-0004-xianyu-message-boundary"
    / "tests"
    / "test_acceptance.py",
]


def run_isolated_message_python(script: str, tmp_path: Path) -> dict[str, object]:
    env = os.environ.copy()
    pythonpath = [str(ROOT / "app"), str(ROOT)]
    if env.get("PYTHONPATH"):
        pythonpath.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath)
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.stderr == ""
    return json.loads(result.stdout)


def test_message_public_surface_excludes_persistence_and_migration_internals(
    tmp_path: Path,
) -> None:
    report = run_isolated_message_python(
        """
import json
import sys

import xianyu_system.worker.message as message_package
from xianyu_system.worker.message import Conversation, SyntheticMessageDelivery
from xianyu_system.worker.message.domain import Conversation as DomainConversation
from xianyu_system.core.database import Base

public = set(message_package.__all__)
print(json.dumps({
    "conversation_identity": Conversation is DomainConversation,
    "transport_name": SyntheticMessageDelivery.__name__,
    "service_loaded": "xianyu_system.worker.message.service" in sys.modules,
    "persistence_loaded": "xianyu_system.worker.message.persistence" in sys.modules,
    "worker_loaded": "xianyu_system.worker.message.worker" in sys.modules,
    "metadata_tables": sorted(Base.metadata.tables),
    "public": sorted(public),
    "forbidden_public": sorted(public & {
        "MessageRepository",
        "conversation_table",
        "message_table",
        "delivery_attempt_table",
        "upgrade",
        "downgrade",
    }),
}))
""",
        tmp_path,
    )
    assert report["conversation_identity"] is True
    assert report["transport_name"] == "SyntheticMessageDelivery"
    assert report["service_loaded"] is False
    assert report["persistence_loaded"] is False
    assert report["worker_loaded"] is False
    assert report["metadata_tables"] == []
    assert report["forbidden_public"] == []
    for name in [
        "Conversation",
        "MessageService",
        "MessageWorker",
        "SyntheticMessageDelivery",
    ]:
        assert name in report["public"]


def test_message_sources_have_no_external_integration_or_sensitive_storage() -> None:
    package = ROOT / "app" / "xianyu_system" / "worker" / "message"
    filenames = sorted(path.name for path in package.glob("*.py"))
    assert filenames == [
        "__init__.py",
        "domain.py",
        "persistence.py",
        "service.py",
        "transport.py",
        "worker.py",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8").lower() for path in package.glob("*.py"))
    for forbidden in [
        "websocket",
        "requests.",
        "httpx.",
        "urllib.request",
        "playwright",
        "selenium",
        "credential store",
        "browser profile",
        "reply sender",
        "scheduler.add_job",
        "threading.thread(",
        "subprocess.",
    ]:
        assert forbidden not in combined


def test_message_operations_make_no_network_subprocess_home_or_thread_calls(
    tmp_path: Path,
) -> None:
    report = run_isolated_message_python(
        f"""
import json
import pathlib
import socket
import subprocess
import threading
from datetime import UTC, datetime

blocked_calls = []

def fail(name):
    def inner(*_args, **_kwargs):
        blocked_calls.append(name)
        raise AssertionError(name)
    return inner

def blocked_home(cls):
    blocked_calls.append("Path.home")
    raise AssertionError("Path.home")

from xianyu_system.core.database import dispose_database, initialize_database, upgrade_database
from xianyu_system.worker.account.service import AccountService
from xianyu_system.worker.message.service import MessageService
from xianyu_system.worker.message.transport import SyntheticMessageDelivery
from xianyu_system.worker.message.worker import MessageWorker

socket.socket = fail("socket.socket")
socket.create_connection = fail("socket.create_connection")
socket.getaddrinfo = fail("socket.getaddrinfo")
subprocess.run = fail("subprocess.run")
subprocess.Popen = fail("subprocess.Popen")
pathlib.Path.home = classmethod(blocked_home)
threading.Thread.start = fail("threading.Thread.start")

resources = initialize_database(pathlib.Path({str(tmp_path / "isolated-message.db")!r}))
try:
    upgrade_database(resources)
    profile = AccountService(resources.session_factory).create_profile(
        account_alias="synthetic-isolated-message"
    )
    service = MessageService(resources.session_factory)
    worker = MessageWorker(
        profile_id=profile.profile_id,
        account_reference="synthetic-account-reference",
        service=service,
    )
    worker.start()
    result = worker.receive(
        SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference="synthetic-account-reference",
            participant_reference="synthetic-participant",
            message_content="synthetic isolated content",
            received_at=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
            delivery_identity="synthetic-isolated-delivery",
        )
    )
    worker.stop()
    print(json.dumps({{
        "blocked_calls": blocked_calls,
        "created_message": result.created_message,
        "messages": service.count_messages(),
        "worker_state": worker.state.value,
    }}))
finally:
    dispose_database(resources)
""",
        tmp_path,
    )
    assert report["blocked_calls"] == []
    assert report["created_message"] is True
    assert report["messages"] == 1
    assert report["worker_state"] == "STOPPED"


def test_message_errors_do_not_expose_content_identifiers_or_database_details(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    resources = initialize_database(tmp_path / "message-errors.db")
    try:
        upgrade_database(resources)
        from xianyu_system.worker.account.service import AccountService
        from xianyu_system.worker.message.persistence import MessageRepository
        from xianyu_system.worker.message.service import MessageService

        profile = AccountService(resources.session_factory).create_profile(
            account_alias="synthetic-message-errors"
        )
        service = MessageService(resources.session_factory)
        delivery = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference="synthetic-account-reference",
            participant_reference="synthetic-participant",
            message_content="synthetic-hidden-content",
            received_at=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
            delivery_identity="synthetic-hidden-delivery",
        )

        def raise_sqlalchemy_error(self, *args, **kwargs):
            raise SQLAlchemyError(
                "SELECT synthetic-hidden-content FROM synthetic_storage_table"
            )

        monkeypatch.setattr(MessageRepository, "add_message", raise_sqlalchemy_error)
        with pytest.raises(MessagePersistenceError) as persistence_error:
            service.receive(delivery)
        error_text = str(persistence_error.value)
        assert "synthetic-hidden-content" not in error_text
        assert "synthetic-hidden-delivery" not in error_text
        assert "SELECT" not in error_text
        assert "synthetic_storage_table" not in error_text
        assert persistence_error.value.__cause__ is None
    finally:
        dispose_database(resources)


def test_message_tests_use_only_synthetic_fixtures_and_no_global_cleanup_escape_hatches() -> None:
    combined = "\n".join(path.read_text(encoding="utf-8") for path in MESSAGE_TEST_PATHS)
    for required in [
        "synthetic",
        "SyntheticMessageDelivery",
        "MessageWorker",
        "MessageRepository",
    ]:
        assert required in combined
    for forbidden in [
        "clear" + "_mappers",
        "Base.metadata" + ".remove",
        "sys.modules" + ".pop",
        "importlib" + ".reload",
        "cleanup_message_metadata" + "_after_module",
        "pytest" + ".skip",
        "pytest" + ".xfail",
        "time" + ".sleep",
        "asyncio" + ".sleep",
        "real " + "Xianyu",
        "browser " + "Profile",
        "Credential " + "Store",
    ]:
        assert forbidden not in combined
