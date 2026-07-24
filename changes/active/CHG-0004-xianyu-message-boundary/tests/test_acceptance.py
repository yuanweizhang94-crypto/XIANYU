from __future__ import annotations

import importlib
import json
import socket
import subprocess
import threading
from datetime import UTC, datetime
from pathlib import Path
from uuid import UUID

import pytest
import yaml
from alembic.script import ScriptDirectory

ROOT = Path(__file__).resolve().parents[4]
ACTIVE = ROOT / "changes" / "active"
ARCHIVE = ROOT / "changes" / "archive"

CHG_0002 = ARCHIVE / "CHG-0002-core-application"
CHG_0003 = ARCHIVE / "CHG-0003-xianyu-account-boundary"
CHG_0004 = ACTIVE / "CHG-0004-xianyu-message-boundary"

ACCOUNT_CAPABILITY = "CAP-XY-ACCOUNT"
MESSAGE_CAPABILITY = "CAP-XY-MESSAGE"
ACCOUNT_VERIFIED_CANDIDATE_SHA = "2aab941cb7f713d7e46675789c47971a2c79c564"
ACCOUNT_ARCHIVED_ACCEPTANCE = (
    "changes/archive/CHG-0003-xianyu-account-boundary/"
    "tests/test_acceptance.py"
)
ACCOUNT_ACTIVE_ACCEPTANCE = (
    "changes/active/CHG-0003-xianyu-account-boundary/"
    "tests/test_acceptance.py"
)
MESSAGE_PACKAGE = ROOT / "app" / "xianyu_system" / "worker" / "message"
MESSAGE_MIGRATION = ROOT / "migrations" / "versions" / "0003_xianyu_message_boundary.py"


def status_of(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    raise AssertionError(f"No status line found in {path}")


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = yaml.safe_load(
        (ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(
            encoding="utf-8"
        )
    )
    return {str(item["id"]): item for item in registry["capabilities"]}


def test_completed_changes_are_archived_with_history_preserved() -> None:
    assert not (ACTIVE / "CHG-0002-core-application").exists()
    assert not (ACTIVE / "CHG-0003-xianyu-account-boundary").exists()
    for change_dir in [CHG_0002, CHG_0003]:
        assert change_dir.is_dir()
        for name in [
            "proposal.md",
            "design.md",
            "tasks.md",
            "acceptance.md",
        ]:
            assert status_of(change_dir / name) == "ARCHIVED"
        assert (change_dir / "tests" / "test_acceptance.py").is_file()


def test_chg_0004_is_the_only_approved_active_change() -> None:
    active_dirs = sorted(path.name for path in ACTIVE.iterdir() if path.is_dir())
    assert active_dirs == ["CHG-0004-xianyu-message-boundary"]
    for name in [
        "proposal.md",
        "design.md",
        "tasks.md",
        "acceptance.md",
    ]:
        assert status_of(CHG_0004 / name) == "APPROVED"


def test_chg_0004_t6_implements_only_local_synthetic_message_boundary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    task_lines = [
        line
        for line in (CHG_0004 / "tasks.md").read_text(
            encoding="utf-8"
        ).splitlines()
        if line.startswith("- [")
    ]
    assert len(task_lines) == 9
    assert all(line.startswith("- [x]") for line in task_lines[:6])
    assert all(line.startswith("- [ ]") for line in task_lines[6:])

    state = json.loads(
        (ROOT / "generated" / "PROJECT_STATE.json").read_text(
            encoding="utf-8"
        )
    )
    assert state["tasks"]["completed"] == 6
    assert state["tasks"]["next_task"] == (
        "T7 Add unit, contract, security, and active-change acceptance tests"
    )

    assert sorted(path.name for path in MESSAGE_PACKAGE.glob("*.py")) == [
        "__init__.py",
        "domain.py",
        "persistence.py",
        "service.py",
        "transport.py",
        "worker.py",
    ]
    for forbidden in [
        "client.py",
        "websocket.py",
        "network.py",
        "listener.py",
        "consumer.py",
        "daemon.py",
        "scheduler.py",
        "tasks.py",
        "background.py",
        "provider.py",
        "credential.py",
        "browser.py",
        "api.py",
        "router.py",
        "schemas.py",
        "handlers.py",
        "plugins.py",
        "events.py",
        "event_bus.py",
        "unit_of_work.py",
        "base_repository.py",
    ]:
        assert not (MESSAGE_PACKAGE / forbidden).exists()

    assert MESSAGE_MIGRATION.is_file()
    migration_source = MESSAGE_MIGRATION.read_text(encoding="utf-8")
    assert 'revision: str = "0003_xianyu_message_boundary"' in migration_source
    assert 'down_revision: str | None = "0002_xianyu_account_boundary"' in migration_source
    assert "create_all" not in migration_source

    proposal = (CHG_0004 / "proposal.md").read_text(encoding="utf-8")
    design = (CHG_0004 / "design.md").read_text(encoding="utf-8")
    acceptance = (CHG_0004 / "acceptance.md").read_text(encoding="utf-8")
    assert "T1 through T6 are complete." in proposal
    assert "T7 is the next executable task" in proposal
    assert "## T6 acceptance criteria" in acceptance
    assert "The local package `xianyu_system.worker.message` exists." in design

    def fail_side_effect(*_args: object, **_kwargs: object) -> None:
        raise AssertionError("external side effect is not approved")

    monkeypatch.setattr(socket, "socket", fail_side_effect)
    monkeypatch.setattr(socket, "create_connection", fail_side_effect)
    monkeypatch.setattr(socket, "getaddrinfo", fail_side_effect)
    monkeypatch.setattr(subprocess, "Popen", fail_side_effect)
    monkeypatch.setattr(threading.Thread, "start", fail_side_effect)

    from xianyu_system.core.database import (
        Base,
        dispose_database,
        initialize_database,
        upgrade_database,
    )

    before_tables = set(Base.metadata.tables)
    importlib.import_module("xianyu_system.worker.message.domain")
    message_package = importlib.import_module("xianyu_system.worker.message")
    from xianyu_system.worker.message import Conversation
    from xianyu_system.worker.message.domain import Conversation as DomainConversation

    assert Conversation is DomainConversation
    assert message_package.Conversation is DomainConversation
    assert set(Base.metadata.tables) == before_tables

    resources = initialize_database(tmp_path / "synthetic-message.db")
    try:
        upgrade_database(resources)
        from sqlalchemy import inspect
        from xianyu_system.worker.account.service import AccountService
        from xianyu_system.worker.message.domain import (
            DeduplicationConflict,
            DeduplicationDecision,
            InvalidMessageInput,
            InvalidWorkerTransition,
            MessageAuthorizationViolation,
            MessageInternalError,
            MessagePersistenceError,
            MessageProtocolViolation,
            MessageRiskViolation,
            ProfileOwnershipViolation,
            WorkerLifecycleState,
        )
        from xianyu_system.worker.message.service import MessageService
        from xianyu_system.worker.message.transport import SyntheticMessageDelivery
        from xianyu_system.worker.message.worker import (
            AUTOMATIC_PROCESSING_RETRIES,
            AUTOMATIC_RECONNECT_ATTEMPTS,
            MessageWorker,
        )

        table_names = set(inspect(resources.engine).get_table_names())
        assert {
            "xianyu_message_conversations",
            "xianyu_message_records",
            "xianyu_message_delivery_attempts",
        } <= table_names

        profile = AccountService(resources.session_factory).create_profile(
            account_alias="synthetic-account"
        )
        account_reference = "synthetic-account-reference"
        ids = iter(
            [
                UUID("00000000-0000-4000-8000-000000000101"),
                UUID("00000000-0000-4000-8000-000000000102"),
                UUID("00000000-0000-4000-8000-000000000103"),
                UUID("00000000-0000-4000-8000-000000000104"),
                UUID("00000000-0000-4000-8000-000000000105"),
                UUID("00000000-0000-4000-8000-000000000106"),
                UUID("00000000-0000-4000-8000-000000000107"),
                UUID("00000000-0000-4000-8000-000000000108"),
            ]
        )

        def next_id() -> UUID:
            return next(ids)

        def now() -> datetime:
            return datetime(2026, 1, 1, tzinfo=UTC)

        service = MessageService(
            resources.session_factory,
            identifier_factory=next_id,
            clock=now,
        )
        worker = MessageWorker(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            service=service,
        )
        assert worker.state is WorkerLifecycleState.STOPPED
        worker.start()
        assert worker.state is WorkerLifecycleState.RUNNING

        delivery = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            participant_reference="synthetic-participant",
            message_content="synthetic local text",
            received_at=now(),
            platform_conversation_identifier="synthetic-conversation",
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-delivery",
        )
        result = worker.receive(delivery)
        assert result.deduplication_decision is DeduplicationDecision.NEW
        assert service.count_conversations() == 1
        assert service.count_messages() == 1
        assert service.count_delivery_attempts() == 1

        duplicate = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            participant_reference="synthetic-participant",
            message_content="synthetic local text",
            received_at=datetime(2026, 1, 1, 0, 1, tzinfo=UTC),
            platform_conversation_identifier="synthetic-conversation",
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-delivery",
        )
        duplicate_result = worker.receive(duplicate)
        assert duplicate_result.deduplication_decision is DeduplicationDecision.DUPLICATE
        assert service.count_conversations() == 1
        assert service.count_messages() == 1
        assert service.count_delivery_attempts() == 2

        conversation_conflict = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            participant_reference="synthetic-participant",
            message_content="synthetic local text",
            received_at=now(),
            platform_conversation_identifier="synthetic-other-conversation",
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-delivery",
        )
        with pytest.raises(DeduplicationConflict):
            worker.receive(conversation_conflict)
        assert worker.state is WorkerLifecycleState.BLOCKED
        assert service.count_conversations() == 1
        assert service.count_messages() == 1
        assert service.count_delivery_attempts() == 2
        with pytest.raises(InvalidWorkerTransition):
            worker.stop()
        assert worker.state is WorkerLifecycleState.BLOCKED

        worker.reset()
        worker.start()
        content_conflict = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            participant_reference="synthetic-participant",
            message_content="synthetic changed text",
            received_at=now(),
            platform_conversation_identifier="synthetic-conversation",
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-delivery",
        )
        with pytest.raises(DeduplicationConflict):
            worker.receive(content_conflict)
        assert worker.state is WorkerLifecycleState.BLOCKED
        assert service.count_conversations() == 1
        assert service.count_messages() == 1
        assert service.count_delivery_attempts() == 2
        with pytest.raises(InvalidWorkerTransition):
            worker.stop()
        assert worker.state is WorkerLifecycleState.BLOCKED

        worker.reset()
        worker.start()
        indeterminate = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            participant_reference="synthetic-participant",
            message_content="synthetic no identity",
            received_at=now(),
        )
        indeterminate_result = worker.receive(indeterminate)
        assert (
            indeterminate_result.deduplication_decision
            is DeduplicationDecision.INDETERMINATE
        )
        assert service.count_messages() == 2
        assert service.count_delivery_attempts() == 3

        with pytest.raises(InvalidMessageInput):
            SyntheticMessageDelivery(
                profile_id=profile.profile_id,
                account_reference=account_reference,
                participant_reference="synthetic-participant",
                message_content="   ",
                received_at=now(),
            )
        assert worker.state is WorkerLifecycleState.RUNNING

        cross_profile = SyntheticMessageDelivery(
            profile_id="00000000-0000-4000-8000-999999999999",
            account_reference=account_reference,
            participant_reference="synthetic-participant",
            message_content="synthetic cross profile",
            received_at=now(),
        )
        with pytest.raises(ProfileOwnershipViolation):
            worker.receive(cross_profile)
        assert worker.state is WorkerLifecycleState.BLOCKED
        assert service.count_messages() == 2
        assert service.count_delivery_attempts() == 3
        with pytest.raises(InvalidWorkerTransition):
            worker.stop()
        assert worker.state is WorkerLifecycleState.BLOCKED

        worker.reset()
        worker.start()
        worker.stop()
        assert worker.state is WorkerLifecycleState.STOPPED
        assert AUTOMATIC_RECONNECT_ATTEMPTS == 0
        assert AUTOMATIC_PROCESSING_RETRIES == 0

        class FakeService:
            def __init__(self, failure: Exception) -> None:
                self.failure = failure

            def receive(
                self,
                _delivery: SyntheticMessageDelivery,
            ):
                raise self.failure

        valid_fake_delivery = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            participant_reference="synthetic-participant",
            message_content="synthetic fake service",
            received_at=now(),
        )
        invalid_input_worker = MessageWorker(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            service=FakeService(InvalidMessageInput()),
        )
        invalid_input_worker.start()
        with pytest.raises(InvalidMessageInput):
            invalid_input_worker.receive(valid_fake_delivery)
        assert invalid_input_worker.state is WorkerLifecycleState.RUNNING
        invalid_input_worker.stop()
        assert invalid_input_worker.state is WorkerLifecycleState.STOPPED

        blocked_failures = [
            MessageAuthorizationViolation(),
            MessageRiskViolation(),
            MessageProtocolViolation(),
            DeduplicationConflict(),
        ]
        for failure in blocked_failures:
            blocked_worker = MessageWorker(
                profile_id=profile.profile_id,
                account_reference=account_reference,
                service=FakeService(failure),
            )
            blocked_worker.start()
            with pytest.raises(type(failure)):
                blocked_worker.receive(valid_fake_delivery)
            assert blocked_worker.state is WorkerLifecycleState.BLOCKED
            with pytest.raises(InvalidWorkerTransition):
                blocked_worker.stop()
            assert blocked_worker.state is WorkerLifecycleState.BLOCKED
            blocked_worker.reset()
            assert blocked_worker.state is WorkerLifecycleState.STOPPED

        failed_failures = [
            MessagePersistenceError(),
            MessageInternalError(),
        ]
        for failure in failed_failures:
            failed_worker = MessageWorker(
                profile_id=profile.profile_id,
                account_reference=account_reference,
                service=FakeService(failure),
            )
            failed_worker.start()
            with pytest.raises(type(failure)):
                failed_worker.receive(valid_fake_delivery)
            assert failed_worker.state is WorkerLifecycleState.FAILED
            with pytest.raises(InvalidWorkerTransition):
                failed_worker.stop()
            assert failed_worker.state is WorkerLifecycleState.FAILED
            failed_worker.reset()
            assert failed_worker.state is WorkerLifecycleState.STOPPED

        unexpected_worker = MessageWorker(
            profile_id=profile.profile_id,
            account_reference=account_reference,
            service=FakeService(RuntimeError("synthetic unexpected failure")),
        )
        unexpected_worker.start()
        with pytest.raises(MessageInternalError):
            unexpected_worker.receive(valid_fake_delivery)
        assert unexpected_worker.state is WorkerLifecycleState.FAILED
        with pytest.raises(InvalidWorkerTransition):
            unexpected_worker.stop()
        assert unexpected_worker.state is WorkerLifecycleState.FAILED
        unexpected_worker.reset()
        assert unexpected_worker.state is WorkerLifecycleState.STOPPED
    finally:
        dispose_database(resources)


def test_message_capability_remains_planned_and_unbound_after_t6() -> None:
    registry = registry_by_id()
    account = registry[ACCOUNT_CAPABILITY]
    assert account["status"] == "verified"
    assert account["active_change"] is None
    assert account["last_verified_commit"] == ACCOUNT_VERIFIED_CANDIDATE_SHA
    assert ACCOUNT_ARCHIVED_ACCEPTANCE in account["test_paths"]
    assert ACCOUNT_ACTIVE_ACCEPTANCE not in account["test_paths"]

    account_spec = (
        ROOT / "specs" / "capabilities" / "CAP-XY-ACCOUNT.md"
    ).read_text(encoding="utf-8")
    assert ACCOUNT_ARCHIVED_ACCEPTANCE in account_spec
    assert ACCOUNT_ACTIVE_ACCEPTANCE not in account_spec

    message = registry[MESSAGE_CAPABILITY]
    assert message["status"] == "planned"
    assert message["owner_module"] == "worker.message"
    assert message["implementation_paths"] == []
    assert message["test_paths"] == []
    assert message["active_change"] is None
    assert message["last_verified_commit"] is None

    message_spec = (
        ROOT / "specs" / "capabilities" / "CAP-XY-MESSAGE.md"
    ).read_text(encoding="utf-8")
    assert "without opening a real WebSocket" in message_spec
    assert "Status remains planned." in message_spec
    assert MESSAGE_PACKAGE.is_dir()
    assert MESSAGE_MIGRATION.is_file()

    script = ScriptDirectory.from_config(
        __import__("xianyu_system.core.database", fromlist=["build_alembic_config"])
        .build_alembic_config()
    )
    assert script.get_current_head() == "0003_xianyu_message_boundary"
