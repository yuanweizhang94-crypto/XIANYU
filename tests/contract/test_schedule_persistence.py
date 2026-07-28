from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from sqlalchemy import inspect

from xianyu_system.core.database import dispose_database, initialize_database, upgrade_database
from xianyu_system.schedule.persistence import schedule_audit_event_table, schedule_request_table


def test_schedule_tables_are_registered_on_shared_metadata() -> None:
    assert schedule_request_table.name == "xianyu_schedule_requests"
    assert schedule_audit_event_table.name == "xianyu_schedule_audit_events"
    assert schedule_request_table.metadata is schedule_audit_event_table.metadata


def test_schedule_migration_creates_only_local_schedule_tables(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "schedule-contract.db")
    try:
        upgrade_database(resources)
        tables = set(inspect(resources.engine).get_table_names())
        assert "xianyu_schedule_requests" in tables
        assert "xianyu_schedule_audit_events" in tables
        columns = {column["name"] for column in inspect(resources.engine).get_columns("xianyu_schedule_requests")}
        assert {"schedule_id", "publish_request_id", "idempotency_key", "lifecycle", "due_at", "misfire_grace_seconds"} <= columns
    finally:
        dispose_database(resources)


def test_schedule_persistence_contract_uses_utc_fixture_only() -> None:
    assert datetime(2026, 1, 1, tzinfo=UTC).tzinfo is UTC
