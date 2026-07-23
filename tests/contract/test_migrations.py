from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from unittest.mock import patch

import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from alembic.util.exc import CommandError
from fastapi.testclient import TestClient
from sqlalchemy import inspect, text

from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import (
    ALEMBIC_CONFIG_PATH,
    BASELINE_REVISION,
    MIGRATIONS_PATH,
    build_alembic_config,
    dispose_database,
    downgrade_database,
    get_current_revision,
    initialize_database,
    upgrade_database,
)

ROOT = Path(__file__).resolve().parents[2]
BASELINE_PATH = ROOT / "migrations" / "versions" / "0001_core_baseline.py"
ACCOUNT_REVISION = "0002_xianyu_account_boundary"
ACCOUNT_TABLE = "xianyu_account_profiles"


def table_names(resources) -> set[str]:
    return set(inspect(resources.engine).get_table_names())


def assert_no_business_tables(resources) -> None:
    assert table_names(resources) <= {"alembic_version"}


def assert_account_tables(resources) -> None:
    assert table_names(resources) == {"alembic_version", ACCOUNT_TABLE}


def test_migration_files_exist() -> None:
    for relative in [
        "alembic.ini",
        "migrations/env.py",
        "migrations/script.py.mako",
        "migrations/versions/__init__.py",
        "migrations/versions/0001_core_baseline.py",
        "migrations/versions/0002_xianyu_account_boundary.py",
    ]:
        assert (ROOT / relative).is_file()


def test_alembic_config_parses_without_database_side_effects(tmp_path: Path) -> None:
    config = build_alembic_config()
    second = build_alembic_config()

    assert isinstance(config, Config)
    assert config is not second
    assert Path(config.config_file_name or "") == ALEMBIC_CONFIG_PATH
    assert Path(config.get_main_option("script_location")) == MIGRATIONS_PATH
    assert config.get_main_option("sqlalchemy.url") == ""
    assert not (tmp_path / "side-effect.db").exists()


def test_script_directory_has_single_baseline_head() -> None:
    script = ScriptDirectory.from_config(build_alembic_config())

    assert script.get_current_head() == ACCOUNT_REVISION
    assert script.get_heads() == [ACCOUNT_REVISION]


def test_revision_relationship_is_empty_baseline() -> None:
    script = ScriptDirectory.from_config(build_alembic_config())
    revision = script.get_revision(BASELINE_REVISION)
    account_revision = script.get_revision(ACCOUNT_REVISION)

    assert revision is not None
    assert revision.revision == BASELINE_REVISION
    assert revision.down_revision is None
    assert revision.branch_labels in (None, set())
    assert revision.dependencies in (None, ())
    assert account_revision is not None
    assert account_revision.down_revision == BASELINE_REVISION
    assert account_revision.branch_labels in (None, set())
    assert account_revision.dependencies in (None, ())


def test_baseline_revision_is_static_empty_operation() -> None:
    source = BASELINE_PATH.read_text(encoding="utf-8")

    assert f'revision: str = "{BASELINE_REVISION}"' in source
    assert "down_revision: str | None = None" in source
    assert "pass" in source
    for forbidden in [
        "op.create_table",
        "op.drop_table",
        "op.add_column",
        "op.execute",
        "bulk_insert",
        "__tablename__",
        "mapped_column",
        "Table(",
        "metadata.create_all",
        "metadata.drop_all",
        "alembic.op",
        "sqlalchemy",
    ]:
        assert forbidden not in source


def test_env_uses_base_metadata_and_no_file_config() -> None:
    source = (ROOT / "migrations" / "env.py").read_text(encoding="utf-8")

    assert "target_metadata = Base.metadata" in source
    assert "account_profiles_table" in source
    assert "MetaData(" not in source
    assert "fileConfig(" not in source
    assert "logging.config" not in source


def test_env_uses_shared_connection_without_direct_engine_creation() -> None:
    source = (ROOT / "migrations" / "env.py").read_text(encoding="utf-8")

    assert 'config.attributes.get("connection")' in source
    assert 'config.attributes["connection"]' not in source
    assert "engine_from_config" not in source
    assert "async_engine_from_config" not in source
    assert "create_engine" not in source
    assert "initialize_database" in source


def test_fresh_database_upgrade_creates_only_alembic_version(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "fresh.db")
    try:
        assert get_current_revision(resources) is None
        upgrade_database(resources)
        assert get_current_revision(resources) == ACCOUNT_REVISION
        assert_account_tables(resources)
    finally:
        dispose_database(resources)


def test_upgrade_is_repeatable(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "repeat.db")
    try:
        upgrade_database(resources)
        upgrade_database(resources)
        assert get_current_revision(resources) == ACCOUNT_REVISION
        assert_account_tables(resources)
    finally:
        dispose_database(resources)


def test_downgrade_to_base_then_upgrade_again(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "downgrade.db")
    try:
        upgrade_database(resources)
        downgrade_database(resources)
        assert get_current_revision(resources) is None
        assert_no_business_tables(resources)
        upgrade_database(resources)
        assert get_current_revision(resources) == ACCOUNT_REVISION
        assert_account_tables(resources)
    finally:
        dispose_database(resources)


def test_alembic_check_passes_after_upgrade(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "check.db")
    try:
        upgrade_database(resources)
        with resources.engine.begin() as connection:
            command.check(build_alembic_config(connection=connection))
    finally:
        dispose_database(resources)


def test_cli_upgrade_requires_explicit_path_and_creates_no_default_database(tmp_path: Path) -> None:
    database_path = tmp_path / "cli.db"
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
    resources = initialize_database(database_path)
    try:
        assert get_current_revision(resources) == ACCOUNT_REVISION
        assert_account_tables(resources)
    finally:
        dispose_database(resources)
    assert not (ROOT / "data" / "xianyu.db").exists()


def test_cli_missing_path_fails_without_default_database() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", "upgrade", "head"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    assert result.returncode != 0
    output = result.stdout + result.stderr
    assert "database_path" in output
    assert "shared connection" in output
    assert not (ROOT / "data" / "xianyu.db").exists()


def test_offline_sql_does_not_create_database_file(tmp_path: Path) -> None:
    database_path = tmp_path / "offline.db"
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
            "--sql",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    assert not database_path.exists()
    assert "alembic_version" in result.stdout
    assert "CREATE TABLE" in result.stdout.upper()
    assert ACCOUNT_TABLE in result.stdout
    assert ACCOUNT_TABLE in result.stdout
    for forbidden in ["cookie", "token", "password", "browser", "customer", "reply", "schedule"]:
        assert forbidden not in result.stdout.lower()


def test_import_and_config_resolution_have_no_file_side_effects(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)
    script = "from xianyu_system.core.database import build_alembic_config; build_alembic_config()"

    subprocess.run(
        [sys.executable, "-c", script],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert not (tmp_path / "data").exists()
    assert not (tmp_path / "logs").exists()
    for pattern in ["*.db", "*.sqlite", "*.sqlite3"]:
        assert list(tmp_path.glob(pattern)) == []


def test_application_does_not_automatically_run_migrations(tmp_path: Path) -> None:
    path = tmp_path / "app.db"
    app = create_application(settings=ApplicationSettings(environment="test", database_path=path))

    with TestClient(app):
        assert path.exists()
        assert get_current_revision(app.state.database) is None
        assert "alembic_version" not in table_names(app.state.database)
        assert_no_business_tables(app.state.database)

    assert app.state.database is None


def test_migration_api_uses_existing_engine_and_propagates_failure(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "failure.db")
    try:
        with patch("xianyu_system.core.database.create_database_engine") as create_engine_mock:
            with pytest.raises(CommandError):
                upgrade_database(resources, revision="missing_revision")
            create_engine_mock.assert_not_called()
        with resources.engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1
        assert_no_business_tables(resources)
    finally:
        dispose_database(resources)


def test_migration_directory_contains_no_business_or_sensitive_data() -> None:
    forbidden_terms = [
        "cookie",
        "token",
        "secret",
        "password",
        "customer",
        "message content",
        "phone",
        "email address",
        "real account",
    ]
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (ROOT / "migrations").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )

    for term in forbidden_terms:
        assert term not in combined


def test_scheduler_adds_no_migration_revision_or_scheduler_table_names() -> None:
    revision_files = sorted((ROOT / "migrations" / "versions").glob("*.py"))
    scheduler_source = (ROOT / "app/xianyu_system/core/scheduler.py").read_text(encoding="utf-8")

    assert [path.name for path in revision_files] == [
        "0001_core_baseline.py",
        "0002_xianyu_account_boundary.py",
        "__init__.py",
    ]
    assert "SQLAlchemyJobStore" not in scheduler_source
    assert "apscheduler_jobs" not in scheduler_source
    assert "op.create_table" not in scheduler_source


def test_health_api_does_not_run_migrations_or_add_revisions(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "health-migration.db")
    )

    with TestClient(app) as client:
        resources = app.state.database
        assert get_current_revision(resources) is None
        assert client.get("/health").status_code == 200
        assert get_current_revision(resources) is None
        assert set(inspect(resources.engine).get_table_names()) == set()

    revision_files = sorted(path.name for path in (ROOT / "migrations" / "versions").glob("*.py"))
    assert revision_files == [
        "0001_core_baseline.py",
        "0002_xianyu_account_boundary.py",
        "__init__.py",
    ]
    source = (ROOT / "app/xianyu_system/api/health.py").read_text(encoding="utf-8")
    for forbidden in ["upgrade_database", "downgrade_database", "command.upgrade", "alembic", "op.create_table"]:
        assert forbidden not in source
