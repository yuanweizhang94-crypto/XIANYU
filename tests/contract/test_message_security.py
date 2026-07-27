from __future__ import annotations

import json
import os
import re
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
from xianyu_system.worker.message.domain import (
    DeduplicationDecision,
    MessagePersistenceError,
)
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
    / "archive"
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
from xianyu_system.core.database import Base

public = set(message_package.__all__)
initial_service_loaded = "xianyu_system.worker.message.service" in sys.modules
initial_persistence_loaded = "xianyu_system.worker.message.persistence" in sys.modules
initial_worker_loaded = "xianyu_system.worker.message.worker" in sys.modules
metadata_tables_initial = sorted(Base.metadata.tables)
Conversation = message_package.Conversation
from xianyu_system.worker.message.domain import Conversation as DomainConversation
SyntheticMessageDelivery = message_package.SyntheticMessageDelivery
MessageService = message_package.MessageService
MessageWorker = message_package.MessageWorker
print(json.dumps({
    "initial_service_loaded": initial_service_loaded,
    "initial_persistence_loaded": initial_persistence_loaded,
    "initial_worker_loaded": initial_worker_loaded,
    "metadata_tables_initial": metadata_tables_initial,
    "conversation_identity": Conversation is DomainConversation,
    "transport_name": SyntheticMessageDelivery.__name__,
    "service_name": MessageService.__name__,
    "worker_name": MessageWorker.__name__,
    "domain_loaded_after_domain_access": "xianyu_system.worker.message.domain" in sys.modules,
    "transport_loaded_after_transport_access": "xianyu_system.worker.message.transport" in sys.modules,
    "service_loaded_after_service_access": "xianyu_system.worker.message.service" in sys.modules,
    "persistence_loaded_after_service_access": "xianyu_system.worker.message.persistence" in sys.modules,
    "worker_loaded_after_worker_access": "xianyu_system.worker.message.worker" in sys.modules,
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
    assert report["initial_service_loaded"] is False
    assert report["initial_persistence_loaded"] is False
    assert report["initial_worker_loaded"] is False
    assert report["metadata_tables_initial"] == []
    assert report["conversation_identity"] is True
    assert report["transport_name"] == "SyntheticMessageDelivery"
    assert report["service_name"] == "MessageService"
    assert report["worker_name"] == "MessageWorker"
    assert report["domain_loaded_after_domain_access"] is True
    assert report["transport_loaded_after_transport_access"] is True
    assert report["service_loaded_after_service_access"] is True
    assert report["persistence_loaded_after_service_access"] is True
    assert report["worker_loaded_after_worker_access"] is True
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
from sqlalchemy import text

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
from xianyu_system.worker.message.domain import (
    DeduplicationConflict,
    DeduplicationDecision,
    WorkerLifecycleState,
)
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

    def row_counts():
        with resources.engine.connect() as connection:
            return {{
                "conversations": int(
                    connection.execute(
                        text(
                            "SELECT COUNT(*) "
                            "FROM xianyu_message_conversations"
                        )
                    ).scalar_one()
                ),
                "messages": int(
                    connection.execute(
                        text(
                            "SELECT COUNT(*) "
                            "FROM xianyu_message_records"
                        )
                    ).scalar_one()
                ),
                "attempts": int(
                    connection.execute(
                        text(
                            "SELECT COUNT(*) "
                            "FROM xianyu_message_delivery_attempts"
                        )
                    ).scalar_one()
                ),
            }}

    def synthetic_delivery(**overrides):
        values = dict(
            profile_id=profile.profile_id,
            account_reference="synthetic-account-reference",
            participant_reference="synthetic-participant",
            message_content="synthetic isolated content",
            received_at=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
            platform_conversation_identifier="synthetic-conversation",
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-isolated-delivery",
            platform_timestamp=datetime(2026, 1, 1, 12, 0, tzinfo=UTC),
        )
        values.update(overrides)
        return SyntheticMessageDelivery(**values)

    worker.start()
    new_result = worker.receive(synthetic_delivery())
    duplicate_result = worker.receive(
        synthetic_delivery(
            received_at=datetime(2026, 1, 1, 12, 1, tzinfo=UTC),
            correlation_identifier="synthetic-duplicate-correlation",
        )
    )
    indeterminate_result = worker.receive(
        synthetic_delivery(
            delivery_identity=None,
            platform_message_identifier="synthetic-indeterminate-message",
            message_content="synthetic isolated indeterminate content",
        )
    )
    content_conflict_blocked = False
    before_content_conflict = row_counts()
    try:
        worker.receive(synthetic_delivery(message_content="synthetic changed content"))
    except DeduplicationConflict:
        content_conflict_blocked = worker.state is WorkerLifecycleState.BLOCKED
    after_content_conflict = row_counts()
    worker.reset()
    worker.start()
    conversation_conflict_blocked = False
    before_conversation_conflict = row_counts()
    try:
        worker.receive(
            synthetic_delivery(
                platform_conversation_identifier="synthetic-other-conversation"
            )
        )
    except DeduplicationConflict:
        conversation_conflict_blocked = worker.state is WorkerLifecycleState.BLOCKED
    after_conversation_conflict = row_counts()
    worker.reset()
    worker.start()
    worker.stop()
    print(json.dumps({{
        "blocked_calls": blocked_calls,
        "new_decision": new_result.deduplication_decision.value,
        "duplicate_decision": duplicate_result.deduplication_decision.value,
        "indeterminate_decision": indeterminate_result.deduplication_decision.value,
        "created_message": new_result.created_message,
        "duplicate_created_message": duplicate_result.created_message,
        "indeterminate_created_message": indeterminate_result.created_message,
        "content_conflict_blocked": content_conflict_blocked,
        "conversation_conflict_blocked": conversation_conflict_blocked,
        "before_content_conflict": before_content_conflict,
        "after_content_conflict": after_content_conflict,
        "before_conversation_conflict": before_conversation_conflict,
        "after_conversation_conflict": after_conversation_conflict,
        "conversations": row_counts()["conversations"],
        "messages": service.count_messages(),
        "attempts": row_counts()["attempts"],
        "worker_state": worker.state.value,
    }}))
finally:
    dispose_database(resources)
""",
        tmp_path,
    )
    assert report["blocked_calls"] == []
    assert report["new_decision"] == "NEW"
    assert report["duplicate_decision"] == "DUPLICATE"
    assert report["indeterminate_decision"] == "INDETERMINATE"
    assert report["created_message"] is True
    assert report["duplicate_created_message"] is False
    assert report["indeterminate_created_message"] is True
    assert report["content_conflict_blocked"] is True
    assert report["conversation_conflict_blocked"] is True
    assert report["before_content_conflict"] == report["after_content_conflict"]
    assert report["before_conversation_conflict"] == report["after_conversation_conflict"]
    assert report["before_content_conflict"] == {
        "conversations": 1,
        "messages": 2,
        "attempts": 3,
    }
    assert report["after_conversation_conflict"] == {
        "conversations": 1,
        "messages": 2,
        "attempts": 3,
    }
    assert report["conversations"] == 1
    assert report["messages"] == 2
    assert report["attempts"] == 3
    assert report["worker_state"] == "STOPPED"
    assert report["new_decision"] == DeduplicationDecision.NEW.value
    assert report["duplicate_decision"] == DeduplicationDecision.DUPLICATE.value
    assert report["indeterminate_decision"] == DeduplicationDecision.INDETERMINATE.value


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
    def fail_without_value(path: Path | str, category: str) -> None:
        raise AssertionError(f"{path}: {category}")

    def contains_forbidden_phrase(scan_lower: str, phrases: list[str]) -> bool:
        return any(phrase in scan_lower for phrase in phrases)

    email_pattern = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")
    plus_phone_pattern = re.compile(
        r"(?<![\w+])"
        r"\+"
        r"(?=[\d(])"
        r"(?=(?:\D*\d){8,})"
        r"(?:[\d\s().-])+"
        r"(?!\w)"
    )
    long_number_pattern = re.compile(r"(?<![-\w])\d{11,}(?![-\w])")
    scanner_static_evidence = ("(?:\\D*\\d){8,}", "\\d{11,}")
    assert scanner_static_evidence
    credential_patterns = [
        (
            "bearer",
            re.compile("bear" + r"er\s+\S+", re.IGNORECASE),
        ),
        (
            "authorization-header",
            re.compile("author" + r"ization\s*:\s*\S+", re.IGNORECASE),
        ),
        (
            "api-key",
            re.compile("api" + r"[_-]?key\s*=", re.IGNORECASE),
        ),
        (
            "credential-access",
            re.compile("access" + r"[_-]?token\b", re.IGNORECASE),
        ),
        (
            "credential-refresh",
            re.compile("refresh" + r"[_-]?token\b", re.IGNORECASE),
        ),
        (
            "credential-session",
            re.compile("session" + r"[_-]?cookie\b", re.IGNORECASE),
        ),
        (
            "password",
            re.compile("pass" + r"word\s*=", re.IGNORECASE),
        ),
        (
            "secret",
            re.compile("sec" + r"ret\s*=", re.IGNORECASE),
        ),
    ]
    forbidden_phrases = [
        "real " + "customer",
        "customer " + "message",
        "customer " + "data",
        "raw " + "frame",
        "raw" + "_frame",
        "production " + "account",
        "production" + "-account",
        "live " + "account",
        "live" + "-account",
        "real " + "xianyu account",
        "real" + "-xianyu-account",
        "real " + "account",
        "real" + "-account",
    ]
    cleanup_escape_hatches = [
        "clear" + "_mappers",
        "Base.metadata" + ".remove",
        "sys.modules" + ".pop",
        "importlib" + ".reload",
        "del Base.metadata" + ".tables",
        "cleanup_message_metadata" + "_after_module",
        "pytest" + ".skip",
        "pytest" + ".xfail",
        "time" + ".sleep",
        "asyncio" + ".sleep",
    ]

    positive_email = "synthetic-user" + "@" + "example.invalid"
    assert email_pattern.search(positive_email)
    positive_plus_phones = [
        "+" + "12345678",
        "+" + "1 234 567 890",
        "+" + "1-234-567-890",
        "+" + "(123) 456 7890",
        "+" + "86 138 0013 8000",
    ]
    for value in positive_plus_phones:
        assert plus_phone_pattern.search(value)
    positive_long_number = "12345" + "678901"
    assert len(positive_long_number) == 11
    assert long_number_pattern.search(positive_long_number)
    assert long_number_pattern.search("00000000-0000-4000-8000-000000000101") is None
    credential_positive_controls = [
        "bear" + "er synthetic-value",
        "author" + "ization: synthetic-value",
        "api" + "_key=synthetic",
        "api" + "-key=synthetic",
        "access" + "_token",
        "access" + "-token",
        "refresh" + "_token",
        "refresh" + "-token",
        "session" + "_cookie",
        "session" + "-cookie",
        "pass" + "word=synthetic",
        "sec" + "ret=synthetic",
    ]
    for value in credential_positive_controls:
        assert any(pattern.search(value) for _, pattern in credential_patterns), value
    phrase_positive_controls = []
    for phrase in forbidden_phrases:
        phrase_positive_controls.extend(
            [
                ("unquoted", phrase),
                ("quoted_single", "'" + phrase + "'"),
                ("quoted_double", '"' + phrase + '"'),
                ("embedded", "synthetic-prefix " + phrase + " synthetic-suffix"),
            ]
        )
    for _, value in phrase_positive_controls:
        assert contains_forbidden_phrase(value.lower(), forbidden_phrases)

    decoded_by_path = {}
    for path in MESSAGE_TEST_PATHS:
        assert path.is_file()
        raw = path.read_bytes()
        assert not raw.startswith(b"\xef\xbb\xbf")
        source = raw.decode("utf-8")
        assert "synthetic" in source
        decoded_by_path[path] = source

    combined = "\n".join(decoded_by_path.values())
    for required in [
        "synthetic",
        "SyntheticMessageDelivery",
        "MessageWorker",
        "MessageRepository",
    ]:
        assert required in combined

    for path, source in decoded_by_path.items():
        scan_source = source
        scan_lower = scan_source.lower()
        if email_pattern.search(scan_source):
            fail_without_value(path, "email")
        if plus_phone_pattern.search(scan_source):
            fail_without_value(path, "plus-phone")
        if long_number_pattern.search(scan_source):
            fail_without_value(path, "standalone-long-number")
        if re.search(r"1[3-9]\d{9}", scan_source):
            fail_without_value(path, "phone-like-number")
        for category, pattern in credential_patterns:
            if pattern.search(scan_source):
                fail_without_value(path, category)
        if contains_forbidden_phrase(scan_lower, forbidden_phrases):
            fail_without_value(path, "forbidden-phrase")
        for escape_hatch in cleanup_escape_hatches:
            if escape_hatch in scan_source:
                fail_without_value(path, "cleanup-escape-hatch")
