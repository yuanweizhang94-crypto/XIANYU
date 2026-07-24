from __future__ import annotations

import socket
import subprocess
import threading
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
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


def test_message_public_surface_excludes_persistence_internals() -> None:
    import xianyu_system.worker.message as message_package
    from xianyu_system.worker.message import (
        Conversation,
        MessageService as PublicService,
        MessageWorker,
    )
    from xianyu_system.worker.message.domain import Conversation as DomainConversation

    assert Conversation is DomainConversation
    assert PublicService.__name__ == "MessageService"
    assert MessageWorker.__name__ == "MessageWorker"
    assert "MessageRepository" not in message_package.__all__
    assert "conversation_table" not in message_package.__all__


def test_message_sources_have_no_external_integration_or_secret_storage() -> None:
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
    ]:
        assert forbidden not in combined


def test_message_operations_make_no_network_subprocess_home_or_thread_calls(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    blocked_calls: list[str] = []

    def fail(name: str):
        def inner(*_args: object, **_kwargs: object) -> None:
            blocked_calls.append(name)
            raise AssertionError(name)

        return inner

    def blocked_home(cls) -> Path:
        blocked_calls.append("Path.home")
        raise AssertionError("Path.home")

    monkeypatch.setattr(socket, "socket", fail("socket.socket"))
    monkeypatch.setattr(socket, "create_connection", fail("socket.create_connection"))
    monkeypatch.setattr(socket, "getaddrinfo", fail("socket.getaddrinfo"))
    monkeypatch.setattr(subprocess, "Popen", fail("subprocess.Popen"))
    monkeypatch.setattr(threading.Thread, "start", fail("threading.Thread.start"))
    monkeypatch.setattr(Path, "home", classmethod(blocked_home))

    resources = initialize_database(tmp_path / "message-security.db")
    try:
        upgrade_database(resources)
        from xianyu_system.worker.account.service import AccountService
        from xianyu_system.worker.message.service import MessageService

        profile = AccountService(resources.session_factory).create_profile(
            account_alias="synthetic-message-security"
        )
        service = MessageService(resources.session_factory)
        result = service.receive(
            SyntheticMessageDelivery(
                profile_id=profile.profile_id,
                account_reference="synthetic-account-reference",
                participant_reference="synthetic-participant",
                message_content="synthetic safe content",
                received_at=NOW,
                delivery_identity="synthetic-delivery",
            )
        )
        assert service.count_messages() == 1
        assert result.created_message is True
        assert blocked_calls == []
    finally:
        dispose_database(resources)


def test_message_errors_do_not_expose_sensitive_reference_values(
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
            message_content="synthetic-sensitive-content",
            received_at=NOW,
            delivery_identity="synthetic-sensitive-delivery",
        )

        def raise_sqlalchemy_error(self, *args, **kwargs):
            raise SQLAlchemyError(
                "SELECT synthetic-sensitive-content FROM cookie_token_table"
            )

        monkeypatch.setattr(MessageRepository, "add_message", raise_sqlalchemy_error)
        with pytest.raises(MessagePersistenceError) as persistence_error:
            service.receive(delivery)
        error_text = str(persistence_error.value)
        assert "synthetic-sensitive-content" not in error_text
        assert "synthetic-sensitive-delivery" not in error_text
        assert "SELECT" not in error_text
        assert "cookie_token_table" not in error_text
        assert persistence_error.value.__cause__ is None
    finally:
        dispose_database(resources)


def test_message_contract_tests_are_order_independent_with_account_contracts() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    for forbidden in [
        "clear" + "_mappers",
        "Base.metadata" + ".remove",
        "sys.modules" + ".pop",
        "importlib" + ".reload",
        "cleanup_message_metadata" + "_after_module",
    ]:
        assert forbidden not in source
