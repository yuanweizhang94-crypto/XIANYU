from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic.script import ScriptDirectory
from sqlalchemy import inspect, text
from sqlalchemy.exc import IntegrityError

from xianyu_system.core.database import (
    build_alembic_config,
    dispose_database,
    downgrade_database,
    get_current_revision,
    initialize_database,
    upgrade_database,
)
from xianyu_system.worker.message.domain import DeduplicationDecision
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

ROOT = Path(__file__).resolve().parents[2]
MESSAGE_REVISION = "0003_xianyu_message_boundary"
MESSAGE_TABLES = {
    "xianyu_message_conversations",
    "xianyu_message_records",
    "xianyu_message_delivery_attempts",
}
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


def table_names(resources) -> set[str]:
    return set(inspect(resources.engine).get_table_names())


def create_message(resources) -> None:
    from xianyu_system.worker.account.service import AccountService
    from xianyu_system.worker.message.service import MessageService

    profile = AccountService(resources.session_factory).create_profile(
        account_alias="synthetic-message-profile"
    )
    service = MessageService(resources.session_factory)
    result = service.receive(
        SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference="synthetic-account-reference",
            participant_reference="synthetic-participant",
            message_content="synthetic persisted content",
            received_at=NOW,
            platform_conversation_identifier="synthetic-conversation",
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-delivery",
            platform_timestamp=NOW,
        )
    )
    assert result.deduplication_decision is DeduplicationDecision.NEW


def test_message_projection_schema_matches_approved_three_table_shape(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "schema.db")
    try:
        upgrade_database(resources)
        inspector = inspect(resources.engine)
        assert set(inspector.get_table_names()) >= MESSAGE_TABLES
        assert [column["name"] for column in inspector.get_columns("xianyu_message_conversations")] == [
            "conversation_id",
            "profile_id",
            "account_reference",
            "platform_conversation_identifier",
            "created_at",
        ]
        assert [column["name"] for column in inspector.get_columns("xianyu_message_records")] == [
            "message_id",
            "conversation_id",
            "profile_id",
            "account_reference",
            "platform_message_identifier",
            "delivery_identity",
            "participant_reference",
            "message_content",
            "received_at",
            "platform_timestamp",
            "deduplication_decision",
        ]
        assert [column["name"] for column in inspector.get_columns("xianyu_message_delivery_attempts")] == [
            "delivery_attempt_id",
            "message_id",
            "profile_id",
            "account_reference",
            "attempted_at",
            "outcome_class",
            "reason_code",
            "attempt_number",
            "correlation_identifier",
        ]
    finally:
        dispose_database(resources)


def test_message_migration_lineage_is_single_head_after_account_boundary() -> None:
    script = ScriptDirectory.from_config(build_alembic_config())
    revision = script.get_revision(MESSAGE_REVISION)
    assert script.get_current_head() == MESSAGE_REVISION
    assert script.get_heads() == [MESSAGE_REVISION]
    assert revision is not None
    assert revision.down_revision == "0002_xianyu_account_boundary"
    assert revision.branch_labels in (None, set())
    assert revision.dependencies in (None, ())


def test_fresh_upgrade_and_empty_downgrade_round_trip_message_tables(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "roundtrip.db")
    try:
        assert get_current_revision(resources) is None
        upgrade_database(resources)
        assert get_current_revision(resources) == MESSAGE_REVISION
        assert table_names(resources) >= MESSAGE_TABLES
        downgrade_database(resources)
        assert get_current_revision(resources) is None
        assert MESSAGE_TABLES.isdisjoint(table_names(resources))
        upgrade_database(resources)
        assert get_current_revision(resources) == MESSAGE_REVISION
        assert table_names(resources) >= MESSAGE_TABLES
    finally:
        dispose_database(resources)


def test_nonempty_downgrade_fails_closed_and_preserves_rows(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "nonempty.db")
    try:
        upgrade_database(resources)
        create_message(resources)
        with pytest.raises(RuntimeError):
            downgrade_database(resources)
        assert get_current_revision(resources) == MESSAGE_REVISION
        assert table_names(resources) >= MESSAGE_TABLES
        with resources.engine.connect() as connection:
            assert connection.execute(
                text("SELECT COUNT(*) FROM xianyu_message_records")
            ).scalar_one() == 1
    finally:
        dispose_database(resources)


def test_repository_flushes_without_independent_commit(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "repository.db")
    try:
        upgrade_database(resources)
        create_message(resources)
        with resources.engine.connect() as connection:
            assert connection.execute(
                text("SELECT COUNT(*) FROM xianyu_message_conversations")
            ).scalar_one() == 1
            assert connection.execute(
                text("SELECT COUNT(*) FROM xianyu_message_records")
            ).scalar_one() == 1
            assert connection.execute(
                text("SELECT COUNT(*) FROM xianyu_message_delivery_attempts")
            ).scalar_one() == 1
    finally:
        dispose_database(resources)


def test_repository_round_trip_preserves_deduplication_and_stable_attempt_order(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "round-trip.db")
    try:
        upgrade_database(resources)
        from xianyu_system.worker.account.service import AccountService
        from xianyu_system.worker.message.service import MessageService

        profile = AccountService(resources.session_factory).create_profile(
            account_alias="synthetic-round-trip"
        )
        service = MessageService(resources.session_factory)
        delivery = SyntheticMessageDelivery(
            profile_id=profile.profile_id,
            account_reference="synthetic-account-reference",
            participant_reference="synthetic-participant",
            message_content="synthetic persisted content",
            received_at=NOW,
            platform_conversation_identifier="synthetic-conversation",
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-delivery",
            platform_timestamp=NOW,
        )
        first = service.receive(delivery)
        second = service.receive(delivery)
        assert first.message_id == second.message_id
        assert second.deduplication_decision is DeduplicationDecision.DUPLICATE
        with resources.engine.connect() as connection:
            attempts = connection.execute(
                text(
                    "SELECT attempt_number, outcome_class "
                    "FROM xianyu_message_delivery_attempts "
                    "ORDER BY attempt_number"
                )
            ).all()
        assert attempts == [(1, "NEW"), (2, "DUPLICATE")]
    finally:
        dispose_database(resources)


def test_database_enforces_profile_account_delivery_and_attempt_constraints(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "constraints.db")
    try:
        upgrade_database(resources)
        create_message(resources)
        with resources.engine.begin() as connection:
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009999', "
                        "'missing-conversation-id-000000000000', "
                        "'00000000-0000-4000-8000-000000000101', "
                        "'synthetic-account-reference', 'synthetic-participant', "
                        "'synthetic content', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) "
                        "SELECT '00000000-0000-4000-8000-000000008888', "
                        "message_id, profile_id, account_reference, "
                        "'2026-01-01 00:00:00', 'CONFLICT', 2 "
                        "FROM xianyu_message_records LIMIT 1"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) "
                        "SELECT '00000000-0000-4000-8000-000000007777', "
                        "message_id, profile_id, account_reference, "
                        "'2026-01-01 00:00:00', 'DUPLICATE', 0 "
                        "FROM xianyu_message_records LIMIT 1"
                    )
                )
    finally:
        dispose_database(resources)


def test_message_migration_cli_and_offline_sql_have_no_default_database_or_sensitive_terms(
    tmp_path: Path,
) -> None:
    database_path = tmp_path / "cli-message.db"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "alembic.ini",
            "-x",
            f"database_path={database_path}",
            "upgrade",
            "head",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert result.returncode == 0
    assert database_path.exists()
    offline_path = tmp_path / "offline-message.db"
    offline = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "alembic.ini",
            "-x",
            f"database_path={offline_path}",
            "upgrade",
            "head",
            "--sql",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert not offline_path.exists()
    assert "xianyu_message_conversations" in offline.stdout
    assert "xianyu_message_records" in offline.stdout
    assert "xianyu_message_delivery_attempts" in offline.stdout
    lowered = offline.stdout.lower()
    for forbidden in ["cookie", "token", "password", "browser", "customer", "reply", "schedule"]:
        assert forbidden not in lowered
