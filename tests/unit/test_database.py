from __future__ import annotations

import importlib
import os
import subprocess
import sys
from pathlib import Path
from typing import cast
from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi.testclient import TestClient
from alembic.config import Config
from alembic.util.exc import CommandError
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from xianyu_system.application import create_application
from xianyu_system.core import database
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import (
    ALEMBIC_CONFIG_PATH,
    BASELINE_REVISION,
    MIGRATIONS_PATH,
    Base,
    DatabaseResources,
    build_alembic_config,
    build_sqlite_url,
    create_database_engine,
    dispose_database,
    downgrade_database,
    get_current_revision,
    initialize_database,
    open_session,
    resolve_database_path,
    upgrade_database,
)

ROOT = Path(__file__).resolve().parents[2]


def test_import_has_no_file_side_effects(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    subprocess.run(
        [sys.executable, "-c", "import xianyu_system.core.database"],
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


def test_resolve_database_path_handles_relative_absolute_and_spaces(tmp_path: Path) -> None:
    relative = Path("nested folder") / "test db.sqlite"
    resolved_relative = resolve_database_path(relative)
    assert resolved_relative.is_absolute()
    assert resolved_relative.name == "test db.sqlite"
    assert not (Path.cwd() / "nested folder").exists()

    absolute = tmp_path / "absolute folder" / "absolute db.sqlite3"
    resolved_absolute = resolve_database_path(absolute)
    assert resolved_absolute == absolute.resolve(strict=False)
    assert not absolute.exists()
    assert not absolute.parent.exists()


def test_build_sqlite_url_uses_driver_and_resolved_database_path(tmp_path: Path) -> None:
    path = tmp_path / "folder with spaces" / "url db.sqlite"
    url = build_sqlite_url(path)

    assert url.drivername == "sqlite+pysqlite"
    assert url.database == str(path.resolve(strict=False))
    assert "folder with spaces" in str(url)
    assert not path.exists()


def test_create_database_engine_does_not_create_file_until_connection(tmp_path: Path) -> None:
    path = tmp_path / "engine.db"
    engine = create_database_engine(path)
    try:
        assert not path.exists()
    finally:
        engine.dispose()


def test_initialize_database_creates_parent_file_engine_and_session_factory(tmp_path: Path) -> None:
    path = tmp_path / "nested" / "test.db"

    resources = initialize_database(path)
    try:
        assert path.parent.is_dir()
        assert path.is_file()
        assert resources.path == path.resolve(strict=False)
        assert isinstance(resources.engine, Engine)
        assert isinstance(resources.session_factory, sessionmaker)
    finally:
        dispose_database(resources)


def test_initialize_database_enables_wal_mode(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "wal.db")
    try:
        with resources.engine.connect() as connection:
            assert str(connection.exec_driver_sql("PRAGMA journal_mode").scalar_one()).lower() == "wal"
    finally:
        dispose_database(resources)


def test_sqlite_foreign_keys_are_enabled(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "foreign.db")
    try:
        with resources.engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
    finally:
        dispose_database(resources)


def test_sqlite_busy_timeout_is_configured(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "busy.db")
    try:
        with resources.engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA busy_timeout").scalar_one() >= 5000
    finally:
        dispose_database(resources)


def test_open_session_executes_select_one(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "session.db")
    try:
        with open_session(resources) as session:
            assert session.execute(text("SELECT 1")).scalar_one() == 1
    finally:
        dispose_database(resources)


def test_open_session_closes_session() -> None:
    mock_session = Mock(spec=Session)
    factory = Mock(return_value=mock_session)
    resources = DatabaseResources(
        path=Path("mock.db"),
        engine=cast(Engine, Mock()),
        session_factory=cast(sessionmaker[Session], factory),
    )

    with open_session(resources) as session:
        assert session is mock_session

    mock_session.close.assert_called_once_with()


def test_open_session_propagates_exceptions_and_closes_without_commit() -> None:
    mock_session = Mock(spec=Session)
    factory = Mock(return_value=mock_session)
    resources = DatabaseResources(
        path=Path("mock.db"),
        engine=cast(Engine, Mock()),
        session_factory=cast(sessionmaker[Session], factory),
    )

    with pytest.raises(RuntimeError, match="synthetic failure"), open_session(resources):
        raise RuntimeError("synthetic failure")

    mock_session.close.assert_called_once_with()
    mock_session.commit.assert_not_called()


def test_open_session_does_not_auto_commit() -> None:
    mock_session = Mock(spec=Session)
    factory = Mock(return_value=mock_session)
    resources = DatabaseResources(
        path=Path("mock.db"),
        engine=cast(Engine, Mock()),
        session_factory=cast(sessionmaker[Session], factory),
    )

    with open_session(resources):
        pass

    mock_session.commit.assert_not_called()
    mock_session.close.assert_called_once_with()


def test_base_metadata_is_empty_and_database_has_no_business_tables(tmp_path: Path) -> None:
    assert set(Base.metadata.tables) <= {"xianyu_account_profiles"}
    resources = initialize_database(tmp_path / "empty.db")
    try:
        with resources.engine.connect() as connection:
            names = connection.exec_driver_sql(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).scalars().all()
        assert [name for name in names if not str(name).startswith("sqlite_")] == []
    finally:
        dispose_database(resources)


def test_repeated_initialization_isolated_resources(tmp_path: Path) -> None:
    first = initialize_database(tmp_path / "first.db")
    second = initialize_database(tmp_path / "second.db")
    try:
        assert first is not second
        assert first.engine is not second.engine
        assert first.session_factory is not second.session_factory
        assert first.path != second.path
    finally:
        dispose_database(first)
        dispose_database(second)


def test_dispose_database_allows_temp_file_cleanup(tmp_path: Path) -> None:
    path = tmp_path / "dispose.db"
    resources = initialize_database(path)
    dispose_database(resources)

    path.unlink()
    assert not path.exists()


def test_dispose_database_is_repeatable(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "repeat-dispose.db")
    dispose_database(resources)
    dispose_database(resources)


def test_initialize_database_rejects_existing_directory(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="existing directory"):
        initialize_database(tmp_path)


def test_initialize_database_disposes_engine_when_validation_fails(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    fake_engine = Mock(spec=Engine)
    fake_context = MagicMock()
    fake_context.__enter__.side_effect = RuntimeError("validation failed")
    fake_engine.connect.return_value = fake_context
    monkeypatch.setattr(database, "create_database_engine", lambda _path: fake_engine)
    monkeypatch.setattr(database, "create_session_factory", lambda _engine: cast(sessionmaker[Session], Mock()))

    with pytest.raises(RuntimeError, match="validation failed"):
        initialize_database(Path("synthetic.db"))

    fake_engine.dispose.assert_called_once_with()


def test_project_engine_pragmas_do_not_pollute_external_engine(tmp_path: Path) -> None:
    project = initialize_database(tmp_path / "project.db")
    external = create_engine(f"sqlite:///{tmp_path / 'external.db'}")
    try:
        with project.engine.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
        with external.connect() as connection:
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 0
    finally:
        dispose_database(project)
        external.dispose()


def test_database_module_contains_no_business_schema_construction() -> None:
    source = (ROOT / "app/xianyu_system/core/database.py").read_text(encoding="utf-8")

    assert "metadata.create_all" not in source
    assert "metadata.drop_all" not in source
    assert "Table(" not in source
    assert "mapped_column(" not in source
    assert "__tablename__" not in source
    assert importlib.import_module("xianyu_system.core.database") is database


def test_alembic_paths_are_repository_constants() -> None:
    assert ALEMBIC_CONFIG_PATH == ROOT / "alembic.ini"
    assert MIGRATIONS_PATH == ROOT / "migrations"
    assert BASELINE_REVISION == "0001_core_baseline"


def test_build_alembic_config_is_isolated_and_has_no_side_effects(tmp_path: Path) -> None:
    config = build_alembic_config()
    second = build_alembic_config()

    assert isinstance(config, Config)
    assert config is not second
    assert Path(config.config_file_name or "") == ALEMBIC_CONFIG_PATH
    assert Path(config.get_main_option("script_location")) == MIGRATIONS_PATH
    assert config.get_main_option("sqlalchemy.url") == ""
    assert not (tmp_path / "config.db").exists()


def test_build_alembic_config_stores_shared_connection(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "config-connection.db")
    try:
        with resources.engine.connect() as connection:
            config = build_alembic_config(connection=connection)
            assert config.attributes["connection"] is connection
    finally:
        dispose_database(resources)


def test_get_current_revision_returns_none_before_migration(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "unmigrated.db")
    try:
        assert get_current_revision(resources) is None
        assert set(Base.metadata.tables) <= {"xianyu_account_profiles"}
    finally:
        dispose_database(resources)


def test_upgrade_and_downgrade_database_manage_empty_baseline(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "baseline.db")
    try:
        upgrade_database(resources, revision=BASELINE_REVISION)
        assert get_current_revision(resources) == BASELINE_REVISION
        assert set(inspect(resources.engine).get_table_names()) <= {"alembic_version"}

        downgrade_database(resources)
        assert get_current_revision(resources) is None
        assert set(inspect(resources.engine).get_table_names()) <= {"alembic_version"}
    finally:
        dispose_database(resources)


def test_migration_api_does_not_create_second_engine_or_dispose_resources_engine(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "shared-engine.db")
    try:
        with patch("xianyu_system.core.database.create_database_engine") as create_engine_mock:
            upgrade_database(resources)
            downgrade_database(resources)
        create_engine_mock.assert_not_called()
        with resources.engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1
    finally:
        dispose_database(resources)


def test_migration_failure_propagates_and_engine_remains_usable(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "bad-revision.db")
    try:
        with pytest.raises(CommandError):
            upgrade_database(resources, revision="not_a_revision")
        with resources.engine.connect() as connection:
            assert connection.execute(text("SELECT 1")).scalar_one() == 1
        assert get_current_revision(resources) is None
    finally:
        dispose_database(resources)


def test_application_sources_do_not_auto_run_migrations() -> None:
    for relative in ["app/xianyu_system/application.py", "app/xianyu_system/main.py"]:
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert "command.upgrade" not in source
        assert "upgrade_database" not in source


def test_scheduler_is_not_persisted_through_database_job_store() -> None:
    database_source = (ROOT / "app/xianyu_system/core/database.py").read_text(encoding="utf-8")
    scheduler_source = (ROOT / "app/xianyu_system/core/scheduler.py").read_text(encoding="utf-8")

    assert "apscheduler" not in database_source.lower()
    assert "SQLAlchemyJobStore" not in scheduler_source
    assert "apscheduler_jobs" not in scheduler_source
    assert "create_all" not in scheduler_source


def test_health_endpoint_uses_existing_database_engine_without_writes(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "health-db.db")
    )

    with TestClient(app) as client:
        resources = app.state.database
        engine = resources.engine
        before_revision = get_current_revision(resources)
        before_tables = set(inspect(engine).get_table_names())
        with patch("xianyu_system.core.database.create_database_engine") as create_engine_mock:
            assert client.get("/health").status_code == 200
        after_revision = get_current_revision(resources)
        after_tables = set(inspect(engine).get_table_names())
        assert resources.engine is engine

    create_engine_mock.assert_not_called()
    assert before_revision == after_revision is None
    assert before_tables == after_tables == set()
