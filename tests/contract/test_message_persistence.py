from __future__ import annotations

import os
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

import pytest
from alembic.script import ScriptDirectory
from sqlalchemy import DateTime, Integer, String, inspect, text
from sqlalchemy.exc import IntegrityError

from xianyu_system.core.database import (
    build_alembic_config,
    dispose_database,
    downgrade_database,
    get_current_revision,
    initialize_database,
    upgrade_database,
)
from xianyu_system.worker.message.domain import (
    Conversation,
    DeduplicationConflict,
    DeduplicationDecision,
    DeliveryAttempt,
    MessageRecord,
)
from xianyu_system.worker.message.transport import SyntheticMessageDelivery

ROOT = Path(__file__).resolve().parents[2]
ACCOUNT_REVISION = "0002_xianyu_account_boundary"
MESSAGE_REVISION = "0003_xianyu_message_boundary"
ACCOUNT_TABLE = "xianyu_account_profiles"
CONVERSATION_TABLE = "xianyu_message_conversations"
MESSAGE_TABLE = "xianyu_message_records"
ATTEMPT_TABLE = "xianyu_message_delivery_attempts"
MESSAGE_TABLES = {CONVERSATION_TABLE, MESSAGE_TABLE, ATTEMPT_TABLE}
NOW = datetime(2026, 1, 1, 12, 0, tzinfo=UTC)


def create_profile(resources, alias: str = "synthetic-message-profile"):
    from xianyu_system.worker.account.service import AccountService

    return AccountService(resources.session_factory).create_profile(account_alias=alias)


def message_service(resources):
    from xianyu_system.worker.message.service import MessageService

    return MessageService(resources.session_factory)


def delivery(profile_id: str, **overrides: object) -> SyntheticMessageDelivery:
    values = {
        "profile_id": profile_id,
        "account_reference": "synthetic-account-reference",
        "participant_reference": "synthetic-participant",
        "message_content": "synthetic persisted content",
        "received_at": NOW,
        "platform_conversation_identifier": "synthetic-conversation",
        "platform_message_identifier": "synthetic-message",
        "delivery_identity": "synthetic-delivery",
        "platform_timestamp": NOW,
    }
    values.update(overrides)
    return SyntheticMessageDelivery(**values)  # type: ignore[arg-type]


def count_rows(resources, table_name: str) -> int:
    with resources.engine.connect() as connection:
        return int(connection.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one())


def column_map(inspector, table_name: str) -> dict[str, dict[str, object]]:
    return {str(column["name"]): column for column in inspector.get_columns(table_name)}


def assert_column(
    column: dict[str, object],
    *,
    type_class: type[object],
    length: int | None,
    nullable: bool,
    primary_key: bool,
) -> None:
    column_type = column["type"]
    assert isinstance(column_type, type_class)
    if length is not None:
        assert getattr(column_type, "length", None) == length
    assert column["nullable"] is nullable
    assert bool(column["primary_key"]) is primary_key


def assert_unique(inspector, table_name: str, expected_columns: list[str]) -> None:
    unique_sets = {
        tuple(constraint["column_names"])
        for constraint in inspector.get_unique_constraints(table_name)
    }
    assert tuple(expected_columns) in unique_sets


def assert_check_contains(inspector, table_name: str, expected_text: str) -> None:
    checks = " ".join(
        str(constraint.get("sqltext", ""))
        for constraint in inspector.get_check_constraints(table_name)
    )
    assert expected_text in checks


def normalize_sql(sql_text: object) -> str:
    normalized = str(sql_text).lower()
    normalized = normalized.replace('"', "").replace("`", "").replace("[", "").replace("]", "")
    return re.sub(r"\s+", " ", normalized).strip()


def check_constraint_map(inspector, table_name: str) -> dict[str, str]:
    return {
        str(constraint["name"]): normalize_sql(constraint.get("sqltext", ""))
        for constraint in inspector.get_check_constraints(table_name)
    }


def projection_check_constraint_map(table) -> dict[str, str]:
    return {
        str(constraint.name): normalize_sql(constraint.sqltext)
        for constraint in table.constraints
        if constraint.__class__.__name__ == "CheckConstraint"
    }


def assert_check_semantics(checks: dict[str, str], name: str, fragments: list[str]) -> None:
    assert name in checks
    for fragment in fragments:
        assert fragment in checks[name], (name, fragment, checks[name])


def assert_single_fk(
    foreign_keys: list[dict[str, object]],
    *,
    constrained_columns: list[str],
    referred_table: str,
    referred_columns: list[str],
) -> None:
    assert len(foreign_keys) == 1
    foreign_key = foreign_keys[0]
    assert foreign_key["constrained_columns"] == constrained_columns
    assert foreign_key["referred_table"] == referred_table
    assert foreign_key["referred_columns"] == referred_columns
    assert str(foreign_key.get("options", {}).get("ondelete")).upper() == "RESTRICT"


def test_message_projection_schema_matches_approved_columns_constraints_and_indexes(
    tmp_path: Path,
) -> None:
    from xianyu_system.worker.message.persistence import (
        conversation_table,
        delivery_attempt_table,
        message_table,
    )

    expected = {
        CONVERSATION_TABLE: {
            "conversation_id": (String, 36, False, True),
            "profile_id": (String, 36, False, False),
            "account_reference": (String, 256, False, False),
            "platform_conversation_identifier": (String, 512, True, False),
            "created_at": (DateTime, None, False, False),
        },
        MESSAGE_TABLE: {
            "message_id": (String, 36, False, True),
            "conversation_id": (String, 36, False, False),
            "profile_id": (String, 36, False, False),
            "account_reference": (String, 256, False, False),
            "platform_message_identifier": (String, 512, True, False),
            "delivery_identity": (String, 512, True, False),
            "participant_reference": (String, 512, False, False),
            "message_content": (String, 4096, False, False),
            "received_at": (DateTime, None, False, False),
            "platform_timestamp": (DateTime, None, True, False),
            "deduplication_decision": (String, 16, False, False),
        },
        ATTEMPT_TABLE: {
            "delivery_attempt_id": (String, 36, False, True),
            "message_id": (String, 36, False, False),
            "profile_id": (String, 36, False, False),
            "account_reference": (String, 256, False, False),
            "attempted_at": (DateTime, None, False, False),
            "outcome_class": (String, 16, False, False),
            "reason_code": (String, 64, True, False),
            "attempt_number": (Integer, None, False, False),
            "correlation_identifier": (String, 128, True, False),
        },
    }
    projection_tables = {
        CONVERSATION_TABLE: conversation_table,
        MESSAGE_TABLE: message_table,
        ATTEMPT_TABLE: delivery_attempt_table,
    }
    expected_checks = {
        CONVERSATION_TABLE: {
            "ck_xianyu_message_conversation_id_len": ["length(conversation_id) = 36"],
            "ck_xianyu_message_conversation_profile_len": ["length(profile_id) = 36"],
            "ck_xianyu_message_conversation_account_len": [
                "account_reference = trim(account_reference)",
                "length(account_reference) >= 1",
                "length(account_reference) <= 256",
            ],
            "ck_xianyu_message_conversation_platform_len": [
                "platform_conversation_identifier is null",
                "platform_conversation_identifier = trim(platform_conversation_identifier)",
                "length(platform_conversation_identifier) >= 1",
                "length(platform_conversation_identifier) <= 512",
            ],
        },
        MESSAGE_TABLE: {
            "ck_xianyu_message_record_id_len": ["length(message_id) = 36"],
            "ck_xianyu_message_record_conversation_len": [
                "length(conversation_id) = 36"
            ],
            "ck_xianyu_message_record_profile_len": ["length(profile_id) = 36"],
            "ck_xianyu_message_record_account_len": [
                "account_reference = trim(account_reference)",
                "length(account_reference) >= 1",
                "length(account_reference) <= 256",
            ],
            "ck_xianyu_message_record_platform_len": [
                "platform_message_identifier is null",
                "platform_message_identifier = trim(platform_message_identifier)",
                "length(platform_message_identifier) >= 1",
                "length(platform_message_identifier) <= 512",
            ],
            "ck_xianyu_message_record_delivery_len": [
                "delivery_identity is null",
                "delivery_identity = trim(delivery_identity)",
                "length(delivery_identity) >= 1",
                "length(delivery_identity) <= 512",
            ],
            "ck_xianyu_message_record_participant_len": [
                "participant_reference = trim(participant_reference)",
                "length(participant_reference) >= 1",
                "length(participant_reference) <= 512",
            ],
            "ck_xianyu_message_record_content_len": [
                "length(message_content) >= 1",
                "length(message_content) <= 4096",
                "length(trim(message_content)) >= 1",
            ],
            "ck_xianyu_message_record_dedup_decision": [
                "deduplication_decision in ('new', 'indeterminate')"
            ],
        },
        ATTEMPT_TABLE: {
            "ck_xianyu_message_attempt_id_len": ["length(delivery_attempt_id) = 36"],
            "ck_xianyu_message_attempt_message_len": ["length(message_id) = 36"],
            "ck_xianyu_message_attempt_profile_len": ["length(profile_id) = 36"],
            "ck_xianyu_message_attempt_account_len": [
                "account_reference = trim(account_reference)",
                "length(account_reference) >= 1",
                "length(account_reference) <= 256",
            ],
            "ck_xianyu_message_attempt_outcome": [
                "outcome_class in ('new', 'duplicate', 'indeterminate')"
            ],
            "ck_xianyu_message_attempt_number_positive": ["attempt_number >= 1"],
            "ck_xianyu_message_attempt_reason_len": [
                "reason_code is null",
                "reason_code = trim(reason_code)",
                "length(reason_code) >= 1",
                "length(reason_code) <= 64",
            ],
            "ck_xianyu_message_attempt_correlation_len": [
                "correlation_identifier is null",
                "correlation_identifier = trim(correlation_identifier)",
                "length(correlation_identifier) >= 1",
                "length(correlation_identifier) <= 128",
            ],
        },
    }
    prohibited = {
        "payload",
        "raw_payload",
        "raw_frame",
        "frame",
        "headers",
        "metadata",
        "properties",
        "extras",
        "context",
        "json",
        "blob",
        "binary",
        "attachment",
        "media",
        "cookie",
        "token",
        "secret",
        "session",
        "password",
        "authorization",
        "credential",
        "browser_profile",
        "content_hash",
        "ordering_cursor",
        "reply",
    }
    for table_name, columns in expected.items():
        table = projection_tables[table_name]
        assert list(table.columns.keys()) == list(columns)
        for column_name, (type_class, length, nullable, primary_key) in columns.items():
            column = table.c[column_name]
            assert isinstance(column.type, type_class)
            if length is not None:
                assert column.type.length == length
            assert column.nullable is nullable
            assert column.primary_key is primary_key
        assert prohibited.isdisjoint(set(table.columns.keys()))
        projection_checks = projection_check_constraint_map(table)
        assert set(projection_checks) == set(expected_checks[table_name])
        for check_name, fragments in expected_checks[table_name].items():
            assert_check_semantics(projection_checks, check_name, fragments)

    resources = initialize_database(tmp_path / "schema.db")
    try:
        upgrade_database(resources)
        inspector = inspect(resources.engine)
        assert {
            name for name in inspector.get_table_names() if name.startswith("xianyu_message_")
        } == MESSAGE_TABLES
        for table_name, columns in expected.items():
            reflected = column_map(inspector, table_name)
            assert list(reflected) == list(columns)
            for column_name, (type_class, length, nullable, primary_key) in columns.items():
                assert_column(
                    reflected[column_name],
                    type_class=type_class,
                    length=length,
                    nullable=nullable,
                    primary_key=primary_key,
                )
            assert prohibited.isdisjoint(set(reflected))
            reflected_checks = check_constraint_map(inspector, table_name)
            assert set(reflected_checks) == set(expected_checks[table_name])
            for check_name, fragments in expected_checks[table_name].items():
                assert_check_semantics(reflected_checks, check_name, fragments)
        assert_unique(
            inspector,
            CONVERSATION_TABLE,
            ["conversation_id", "profile_id", "account_reference"],
        )
        assert_unique(
            inspector,
            CONVERSATION_TABLE,
            ["profile_id", "account_reference", "platform_conversation_identifier"],
        )
        assert_unique(
            inspector,
            MESSAGE_TABLE,
            ["message_id", "profile_id", "account_reference"],
        )
        assert_unique(
            inspector,
            MESSAGE_TABLE,
            ["profile_id", "account_reference", "delivery_identity"],
        )
        assert_unique(
            inspector,
            ATTEMPT_TABLE,
            ["message_id", "profile_id", "account_reference", "attempt_number"],
        )
        assert_check_contains(inspector, MESSAGE_TABLE, "deduplication_decision")
        assert_check_contains(inspector, ATTEMPT_TABLE, "attempt_number >= 1")
    finally:
        dispose_database(resources)


def test_message_migration_is_single_linear_head_and_matches_projection(
    tmp_path: Path,
) -> None:
    script = ScriptDirectory.from_config(build_alembic_config())
    revision = script.get_revision(MESSAGE_REVISION)
    assert script.get_current_head() == MESSAGE_REVISION
    assert script.get_heads() == [MESSAGE_REVISION]
    assert revision is not None
    assert revision.down_revision == ACCOUNT_REVISION
    assert revision.branch_labels in (None, set())
    assert revision.dependencies in (None, ())
    migration = (ROOT / "migrations" / "versions" / "0003_xianyu_message_boundary.py").read_text(
        encoding="utf-8"
    )
    for table_name in MESSAGE_TABLES:
        assert table_name in migration
    for column_name in [
        "conversation_id",
        "message_id",
        "delivery_attempt_id",
        "profile_id",
        "account_reference",
        "delivery_identity",
        "attempt_number",
        "reason_code",
        "correlation_identifier",
    ]:
        assert column_name in migration
    assert 'revision: str = "0003_xianyu_message_boundary"' in migration
    assert "down_revision: str | None = \"0002_xianyu_account_boundary\"" in migration
    assert "branch_labels: str | Sequence[str] | None = None" in migration
    assert "depends_on: str | Sequence[str] | None = None" in migration
    for forbidden in [
        "Base.metadata.create_all",
        "create_all(",
        "requests",
        "httpx",
        "aiohttp",
        "websocket",
        "socket",
        "subprocess",
        "Cookie",
        "Token",
        "Secret",
        "Credential",
        "Endpoint",
        "Seed",
    ]:
        assert forbidden not in migration
    assert migration.count("op.create_table(") == 3
    assert migration.count("op.drop_table(") == 3
    for table_name in MESSAGE_TABLES:
        assert table_name in migration

    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    cli_database_path = tmp_path / "message-cli.db"
    cli_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "alembic.ini",
            "-x",
            f"database_path={cli_database_path}",
            "upgrade",
            "head",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    assert cli_result.returncode == 0
    assert "Traceback" not in cli_result.stderr
    assert cli_database_path.exists()
    cli_resources = initialize_database(cli_database_path)
    try:
        assert get_current_revision(cli_resources) == MESSAGE_REVISION
        inspector = inspect(cli_resources.engine)
        assert set(inspector.get_table_names()) >= MESSAGE_TABLES
    finally:
        dispose_database(cli_resources)

    offline_database_path = tmp_path / "message-offline.db"
    offline_result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "alembic.ini",
            "-x",
            f"database_path={offline_database_path}",
            "upgrade",
            "head",
            "--sql",
        ],
        cwd=ROOT,
        env=env,
        text=True,
        capture_output=True,
    )
    assert offline_result.returncode == 0
    assert not offline_database_path.exists()
    offline_sql = offline_result.stdout.lower()
    assert "0003_xianyu_message_boundary" in offline_sql
    for table_name in MESSAGE_TABLES:
        assert f"create table {table_name}".lower() in offline_sql
    unexpected = [
        path.name
        for path in tmp_path.iterdir()
        if path.name not in {"message-cli.db"}
        and path.name != "message-offline.db"
        and path.suffix.lower() in {".db", ".sqlite", ".log", ".credential"}
    ]
    assert unexpected == []


def test_fresh_upgrade_creates_exact_message_tables_and_foreign_keys(
    tmp_path: Path,
) -> None:
    from xianyu_system.worker.message.persistence import (
        conversation_table,
        delivery_attempt_table,
        message_table,
    )

    projection_fks = {
        CONVERSATION_TABLE: list(conversation_table.foreign_key_constraints),
        MESSAGE_TABLE: list(message_table.foreign_key_constraints),
        ATTEMPT_TABLE: list(delivery_attempt_table.foreign_key_constraints),
    }
    projection_expectations = {
        CONVERSATION_TABLE: (
            ["profile_id"],
            [f"{ACCOUNT_TABLE}.profile_id"],
        ),
        MESSAGE_TABLE: (
            ["conversation_id", "profile_id", "account_reference"],
            [
                f"{CONVERSATION_TABLE}.conversation_id",
                f"{CONVERSATION_TABLE}.profile_id",
                f"{CONVERSATION_TABLE}.account_reference",
            ],
        ),
        ATTEMPT_TABLE: (
            ["message_id", "profile_id", "account_reference"],
            [
                f"{MESSAGE_TABLE}.message_id",
                f"{MESSAGE_TABLE}.profile_id",
                f"{MESSAGE_TABLE}.account_reference",
            ],
        ),
    }
    for table_name, (columns, referred_columns) in projection_expectations.items():
        assert len(projection_fks[table_name]) == 1
        projection_fk = projection_fks[table_name][0]
        assert list(projection_fk.column_keys) == columns
        assert [str(element.column) for element in projection_fk.elements] == referred_columns
        assert str(projection_fk.ondelete).upper() == "RESTRICT"

    resources = initialize_database(tmp_path / "fresh.db")
    try:
        assert get_current_revision(resources) is None
        upgrade_database(resources)
        assert get_current_revision(resources) == MESSAGE_REVISION
        inspector = inspect(resources.engine)
        assert {
            name for name in inspector.get_table_names() if name.startswith("xianyu_message_")
        } == MESSAGE_TABLES
        conversation_fks = inspector.get_foreign_keys(CONVERSATION_TABLE)
        message_fks = inspector.get_foreign_keys(MESSAGE_TABLE)
        attempt_fks = inspector.get_foreign_keys(ATTEMPT_TABLE)
        assert_single_fk(
            conversation_fks,
            constrained_columns=["profile_id"],
            referred_table=ACCOUNT_TABLE,
            referred_columns=["profile_id"],
        )
        assert_single_fk(
            message_fks,
            constrained_columns=["conversation_id", "profile_id", "account_reference"],
            referred_table=CONVERSATION_TABLE,
            referred_columns=["conversation_id", "profile_id", "account_reference"],
        )
        assert_single_fk(
            attempt_fks,
            constrained_columns=["message_id", "profile_id", "account_reference"],
            referred_table=MESSAGE_TABLE,
            referred_columns=["message_id", "profile_id", "account_reference"],
        )
    finally:
        dispose_database(resources)


def test_repository_flushes_without_committing_and_round_trips_profile_ownership(
    tmp_path: Path,
) -> None:
    from xianyu_system.worker.message.persistence import MessageRepository

    resources = initialize_database(tmp_path / "repository.db")
    try:
        upgrade_database(resources)
        profile = create_profile(resources)
        session = resources.session_factory()
        commit_calls = 0

        def count_commit() -> None:
            nonlocal commit_calls
            commit_calls += 1
            raise AssertionError("Repository must not commit")

        session.commit = count_commit  # type: ignore[method-assign]
        repository = MessageRepository(session)
        conversation = Conversation(
            conversation_id="00000000-0000-4000-8000-000000000401",
            profile_id=profile.profile_id,
            account_reference="synthetic-account-reference",
            platform_conversation_identifier="synthetic-conversation",
            created_at=NOW,
        )
        message = MessageRecord(
            message_id="00000000-0000-4000-8000-000000000402",
            conversation_id=conversation.conversation_id,
            profile_id=profile.profile_id,
            account_reference=conversation.account_reference,
            platform_message_identifier="synthetic-message",
            delivery_identity="synthetic-delivery",
            participant_reference="synthetic-participant",
            message_content="synthetic repository content",
            received_at=NOW,
            platform_timestamp=NOW,
            deduplication_decision=DeduplicationDecision.NEW,
        )
        attempt = DeliveryAttempt(
            delivery_attempt_id="00000000-0000-4000-8000-000000000403",
            message_id=message.message_id,
            profile_id=profile.profile_id,
            account_reference=conversation.account_reference,
            attempted_at=NOW,
            outcome_class=DeduplicationDecision.NEW,
            reason_code="NEW",
            attempt_number=1,
            correlation_identifier="synthetic-correlation",
        )
        try:
            repository.add_conversation(conversation)
            repository.add_message(message)
            repository.add_delivery_attempt(attempt)
            assert commit_calls == 0
            assert repository.count_conversations() == 1
            assert repository.count_messages() == 1
            assert repository.count_delivery_attempts() == 1
            assert repository.get_conversation_by_platform_identifier(
                profile_id=profile.profile_id,
                account_reference=conversation.account_reference,
                platform_conversation_identifier="synthetic-conversation",
            ) == conversation
            round_tripped = repository.get_message_by_delivery_identity(
                profile_id=profile.profile_id,
                account_reference=conversation.account_reference,
                delivery_identity="synthetic-delivery",
            )
            assert round_tripped == message
            assert round_tripped is not None
            assert round_tripped.received_at.tzinfo is UTC
            assert repository.next_attempt_number(
                message_id=message.message_id,
                profile_id=profile.profile_id,
                account_reference=conversation.account_reference,
            ) == 2
            session.rollback()
        finally:
            session.close()
        assert commit_calls == 0
        assert count_rows(resources, CONVERSATION_TABLE) == 0
        assert count_rows(resources, MESSAGE_TABLE) == 0
        assert count_rows(resources, ATTEMPT_TABLE) == 0
    finally:
        dispose_database(resources)


def test_service_persists_new_duplicate_indeterminate_and_conflict_atomically(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "service-atomic.db")
    try:
        upgrade_database(resources)
        profile = create_profile(resources)
        service = message_service(resources)
        first = service.receive(delivery(profile.profile_id))
        duplicate = service.receive(
            delivery(
                profile.profile_id,
                received_at=datetime(2026, 1, 1, 12, 1, tzinfo=UTC),
                correlation_identifier="synthetic-second-correlation",
            )
        )
        indeterminate = service.receive(
            delivery(
                profile.profile_id,
                delivery_identity=None,
                platform_message_identifier="synthetic-message",
                message_content="synthetic indeterminate content",
            )
        )
        assert first.deduplication_decision is DeduplicationDecision.NEW
        assert duplicate.deduplication_decision is DeduplicationDecision.DUPLICATE
        assert duplicate.message_id == first.message_id
        assert indeterminate.deduplication_decision is DeduplicationDecision.INDETERMINATE
        assert indeterminate.message_id != first.message_id
        before_counts = (
            count_rows(resources, CONVERSATION_TABLE),
            count_rows(resources, MESSAGE_TABLE),
            count_rows(resources, ATTEMPT_TABLE),
        )
        with pytest.raises(DeduplicationConflict):
            service.receive(
                delivery(profile.profile_id, message_content="synthetic changed content")
            )
        with pytest.raises(DeduplicationConflict):
            service.receive(
                delivery(
                    profile.profile_id,
                    platform_conversation_identifier="synthetic-other-conversation",
                )
            )
        assert (
            count_rows(resources, CONVERSATION_TABLE),
            count_rows(resources, MESSAGE_TABLE),
            count_rows(resources, ATTEMPT_TABLE),
        ) == before_counts
        with resources.engine.connect() as connection:
            content = connection.execute(
                text(
                    "SELECT message_content FROM xianyu_message_records "
                    "WHERE delivery_identity = 'synthetic-delivery'"
                )
            ).scalar_one()
        assert content == "synthetic persisted content"
    finally:
        dispose_database(resources)


def test_database_constraints_enforce_scope_lengths_decisions_and_attempt_numbers(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "constraints.db")
    try:
        upgrade_database(resources)
        profile = create_profile(resources)
        other_profile = create_profile(resources, "synthetic-other-profile")
        service = message_service(resources)
        service.receive(delivery(profile.profile_id))
        service.receive(
            delivery(
                profile.profile_id,
                delivery_identity=None,
                platform_message_identifier="synthetic-message",
                message_content="synthetic first null delivery",
            )
        )
        service.receive(
            delivery(
                profile.profile_id,
                delivery_identity=None,
                platform_message_identifier="synthetic-message",
                message_content="synthetic second null delivery",
            )
        )
        service.receive(
            delivery(
                other_profile.profile_id,
                account_reference="synthetic-other-account-reference",
                delivery_identity="synthetic-delivery",
            )
        )
        nullable_platform = service.receive(
            delivery(
                profile.profile_id,
                platform_conversation_identifier=None,
                platform_message_identifier=None,
                delivery_identity="synthetic-null-platform-delivery",
                message_content="synthetic nullable platform identifiers",
            )
        )
        assert nullable_platform.deduplication_decision is DeduplicationDecision.NEW
        assert count_rows(resources, MESSAGE_TABLE) == 5
        with resources.engine.begin() as connection:
            conversation_id = connection.execute(
                text(
                    "SELECT conversation_id FROM xianyu_message_conversations "
                    "WHERE account_reference = 'synthetic-account-reference' LIMIT 1"
                )
            ).scalar_one()
            message_id = connection.execute(
                text(
                    "SELECT message_id FROM xianyu_message_records "
                    "WHERE delivery_identity = 'synthetic-delivery' "
                    "AND account_reference = 'synthetic-account-reference' LIMIT 1"
                )
            ).scalar_one()
            assert (
                connection.execute(
                    text(
                        "SELECT COUNT(*) FROM xianyu_message_records "
                        "WHERE delivery_identity = 'synthetic-delivery'"
                    )
                ).scalar_one()
                == 2
            )
            assert (
                connection.execute(
                    text(
                        "SELECT COUNT(*) FROM xianyu_message_records "
                        "WHERE platform_message_identifier IS NULL"
                    )
                ).scalar_one()
                >= 1
            )
            connection.execute(
                text(
                    "INSERT INTO xianyu_message_delivery_attempts "
                    "(delivery_attempt_id, message_id, profile_id, "
                    "account_reference, attempted_at, outcome_class, "
                    "reason_code, attempt_number, correlation_identifier) VALUES "
                    "('00000000-0000-4000-8000-000000009000', "
                    f"'{message_id}', '{profile.profile_id}', "
                    "'synthetic-account-reference', '2026-01-01 00:00:00', "
                    "'DUPLICATE', NULL, 2, NULL)"
                )
            )
            assert (
                connection.execute(
                    text(
                        "SELECT COUNT(*) FROM xianyu_message_delivery_attempts "
                        "WHERE reason_code IS NULL AND correlation_identifier IS NULL"
                    )
                ).scalar_one()
                == 1
            )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_conversations "
                        "(conversation_id, profile_id, account_reference, created_at) "
                        "VALUES ('00000000-0000-4000-8000-000000009101', "
                        f"'{profile.profile_id}', "
                        "'   ', '2026-01-01 00:00:00')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_conversations "
                        "(conversation_id, profile_id, account_reference, "
                        "platform_conversation_identifier, created_at) "
                        "VALUES ('00000000-0000-4000-8000-000000009102', "
                        f"'{profile.profile_id}', 'synthetic-account-reference', "
                        "'   ', '2026-01-01 00:00:00')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_conversations "
                        "(conversation_id, profile_id, account_reference, created_at) "
                        "VALUES ('00000000-0000-4000-8000-000000009001', "
                        "'00000000-0000-4000-8000-000000009999', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009103', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'   ', 'synthetic-participant', "
                        "'synthetic content', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009002', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'synthetic-wrong-account', 'synthetic-participant', "
                        "'synthetic content', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009104', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '   ', "
                        "'synthetic content', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009105', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        f"'synthetic-account-reference', '{('p' * 513)}', "
                        "'synthetic content', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009003', "
                        f"'{conversation_id}', '{other_profile.profile_id}', "
                        "'synthetic-account-reference', 'synthetic-participant', "
                        "'synthetic content', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "platform_message_identifier, participant_reference, "
                        "message_content, received_at, deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009106', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '   ', "
                        "'synthetic-participant', 'synthetic content', "
                        "'2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "delivery_identity, participant_reference, message_content, "
                        "received_at, deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009107', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '   ', "
                        "'synthetic-participant', 'synthetic content', "
                        "'2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009004', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', 'synthetic-participant', "
                        "'   ', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009005', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', 'synthetic-participant', "
                        f"'{('x' * 4097)}', '2026-01-01 00:00:00', 'NEW')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_records "
                        "(message_id, conversation_id, profile_id, account_reference, "
                        "participant_reference, message_content, received_at, "
                        "deduplication_decision) VALUES "
                        "('00000000-0000-4000-8000-000000009006', "
                        f"'{conversation_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', 'synthetic-participant', "
                        "'synthetic content', '2026-01-01 00:00:00', 'DUPLICATE')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009007', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        "'CONFLICT', 2)"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009108', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        "'DUPLICATE', -1)"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009008', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        "'DUPLICATE', 0)"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009109', "
                        f"'{message_id}', '{other_profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        "'DUPLICATE', 3)"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009110', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-wrong-account', '2026-01-01 00:00:00', "
                        "'DUPLICATE', 3)"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "reason_code, attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009111', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        f"'DUPLICATE', '{('r' * 65)}', 3)"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "reason_code, attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009112', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        "'DUPLICATE', '   ', 3)"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number, correlation_identifier) VALUES "
                        "('00000000-0000-4000-8000-000000009113', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        f"'DUPLICATE', 3, '{('c' * 129)}')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number, correlation_identifier) VALUES "
                        "('00000000-0000-4000-8000-000000009114', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        "'DUPLICATE', 3, '   ')"
                    )
                )
            with pytest.raises(IntegrityError):
                connection.execute(
                    text(
                        "INSERT INTO xianyu_message_delivery_attempts "
                        "(delivery_attempt_id, message_id, profile_id, "
                        "account_reference, attempted_at, outcome_class, "
                        "attempt_number) VALUES "
                        "('00000000-0000-4000-8000-000000009115', "
                        f"'{message_id}', '{profile.profile_id}', "
                        "'synthetic-account-reference', '2026-01-01 00:00:00', "
                        "'DUPLICATE', 2)"
                    )
                )
    finally:
        dispose_database(resources)


def test_empty_message_downgrade_and_reupgrade_succeed(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "empty-downgrade.db")
    try:
        upgrade_database(resources)
        profile = create_profile(resources)
        assert count_rows(resources, ACCOUNT_TABLE) == 1
        downgrade_database(resources, revision="0002_xianyu_account_boundary")
        assert get_current_revision(resources) == ACCOUNT_REVISION
        assert ACCOUNT_TABLE in inspect(resources.engine).get_table_names()
        assert MESSAGE_TABLES.isdisjoint(set(inspect(resources.engine).get_table_names()))
        assert count_rows(resources, ACCOUNT_TABLE) == 1
        with resources.engine.connect() as connection:
            alias = connection.execute(
                text(
                    "SELECT account_alias FROM xianyu_account_profiles "
                    "WHERE profile_id = :profile_id"
                ),
                {"profile_id": profile.profile_id},
            ).scalar_one()
        assert alias == "synthetic-message-profile"
        upgrade_database(resources)
        assert get_current_revision(resources) == MESSAGE_REVISION
        assert set(inspect(resources.engine).get_table_names()) >= MESSAGE_TABLES
        assert count_rows(resources, ACCOUNT_TABLE) == 1
    finally:
        dispose_database(resources)


def test_nonempty_message_downgrade_fails_closed_and_preserves_data_and_revision(
    tmp_path: Path,
) -> None:
    resources = initialize_database(tmp_path / "nonempty-downgrade.db")
    try:
        upgrade_database(resources)
        profile = create_profile(resources)
        service = message_service(resources)
        service.receive(delivery(profile.profile_id))
        before_counts = (
            count_rows(resources, ACCOUNT_TABLE),
            count_rows(resources, CONVERSATION_TABLE),
            count_rows(resources, MESSAGE_TABLE),
            count_rows(resources, ATTEMPT_TABLE),
        )
        with pytest.raises(RuntimeError):
            downgrade_database(resources, revision="0002_xianyu_account_boundary")
        assert get_current_revision(resources) == MESSAGE_REVISION
        assert set(inspect(resources.engine).get_table_names()) >= MESSAGE_TABLES
        assert (
            count_rows(resources, ACCOUNT_TABLE),
            count_rows(resources, CONVERSATION_TABLE),
            count_rows(resources, MESSAGE_TABLE),
            count_rows(resources, ATTEMPT_TABLE),
        ) == before_counts
    finally:
        dispose_database(resources)
