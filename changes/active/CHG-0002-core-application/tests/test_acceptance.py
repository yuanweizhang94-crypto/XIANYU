from __future__ import annotations

import io
import json
import logging
import os
import re
import subprocess
import sys
import tomllib
from pathlib import Path

from alembic import command
from alembic.script import ScriptDirectory
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings
from sqlalchemy import inspect, text

from scripts.generate_state import project_state_json
from scripts.repo_utils import parse_tasks, read_yaml
from xianyu_system.api.health import (
    DatabaseHealth,
    HealthResponse,
    SchedulerHealth,
    collect_database_health,
    collect_health,
    collect_scheduler_health,
)
from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.database import (
    BASELINE_REVISION,
    Base,
    DatabaseResources,
    build_alembic_config,
    build_sqlite_url,
    create_database_engine,
    create_session_factory,
    dispose_database,
    downgrade_database,
    get_current_revision,
    initialize_database,
    open_session,
    upgrade_database,
)
from xianyu_system.core.logging import (
    REDACTED_VALUE,
    ManagedStreamHandler,
    StructuredJsonFormatter,
    configure_logging,
    redact_value,
    shutdown_logging,
)
from xianyu_system.core.scheduler import (
    SCHEDULER_TIMEZONE,
    create_scheduler,
    shutdown_scheduler,
    start_scheduler,
)

ROOT = Path(__file__).resolve().parents[4]
CHG_0001 = "CHG-0001-project-baseline"
CHG_0002 = "CHG-0002-core-application"
CORE_CAPABILITIES = {"CAP-CORE-CONFIG", "CAP-CORE-DATABASE", "CAP-HEALTH-MONITOR"}
APPROVED_CORE_RUNTIME = {
    "fastapi",
    "pydantic",
    "pydantic-settings",
    "sqlalchemy",
    "alembic",
    "apscheduler",
    "jinja2",
    "uvicorn",
}
GOVERNANCE_RUNTIME = {"pyyaml", "jsonschema"}
FORBIDDEN_RUNTIME = {
    "redis",
    "celery",
    "psycopg",
    "psycopg2",
    "asyncpg",
    "aiosqlite",
    "django",
    "flask",
    "langchain",
    "playwright",
    "selenium",
    "docker",
    "gunicorn",
}
CHANGE_DOCUMENTS = ["proposal.md", "design.md", "tasks.md", "acceptance.md"]
CORE_DOCUMENTS = ["proposal.md", "design.md", "acceptance.md"]
REPEATED_QUESTION_MARKS = "?" * 3
REPLACEMENT_CHARACTER = chr(0xFFFD)
APPLICATION_MODULES = [
    "app/xianyu_system/application.py",
    "app/xianyu_system/main.py",
]
CONFIGURATION_MODULES = [
    "app/xianyu_system/core/__init__.py",
    "app/xianyu_system/core/config.py",
]
LOGGING_MODULES = [
    "app/xianyu_system/core/logging.py",
]
DATABASE_MODULES = [
    "app/xianyu_system/core/database.py",
]
SCHEDULER_MODULES = [
    "app/xianyu_system/core/scheduler.py",
]
API_MODULES = [
    "app/xianyu_system/api/__init__.py",
    "app/xianyu_system/api/router.py",
    "app/xianyu_system/api/health.py",
]
DEFERRED_CORE_PATHS = [
    "app/xianyu_system/web",
    "app/xianyu_system/domain",
    "app/xianyu_system/web/router.py",
]
MIGRATION_PATHS = [
    "alembic.ini",
    "migrations/README.md",
    "migrations/env.py",
    "migrations/script.py.mako",
    "migrations/versions/__init__.py",
    "migrations/versions/0001_core_baseline.py",
]
FORBIDDEN_ARTIFACT_PATHS = [
    "alembic",
    "templates",
    "static",
    "app/xianyu_system/templates",
    "app/xianyu_system/static",
    "logs",
]
SUPPORTED_ENV_EXAMPLE_KEYS = {
    "XIANYU_ENVIRONMENT",
    "XIANYU_APP_TITLE",
    "XIANYU_APP_VERSION",
    "XIANYU_DEBUG",
    "XIANYU_LOG_LEVEL",
    "XIANYU_DATABASE_PATH",
}
FORBIDDEN_ENV_EXAMPLE_PARTS = {
    "WECOM",
    "AI_",
    "COOKIE",
    "TOKEN",
    "SECRET",
    "PROFILE",
}
FORBIDDEN_SETTING_FIELD_PARTS = {
    "secret",
    "token",
    "cookie",
    "password",
    "credential",
    "profile",
    "wecom",
    "api_key",
    "captcha",
}
DEFAULT_FASTAPI_ROUTE_PATHS = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc", "/health"}


def active_change_dir() -> Path:
    return ROOT / "changes" / "active" / CHG_0002


def status_for(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    return ""


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    return {str(item["id"]): item for item in registry["capabilities"]}


def chg_0002_tasks():
    return parse_tasks(active_change_dir() / "tasks.md")


def pyproject() -> dict[str, object]:
    return tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))


def dependency_name(requirement: str) -> str:
    base = requirement.split(";", 1)[0].strip()
    base = base.split("[", 1)[0]
    for marker in [">=", "<=", "==", "!=", "~=", ">", "<", "="]:
        if marker in base:
            base = base.split(marker, 1)[0]
            break
    return base.strip().lower().replace("_", "-")


def runtime_dependencies() -> list[str]:
    deps = pyproject()["project"]["dependencies"]
    assert isinstance(deps, list)
    return [str(item) for item in deps]


def dev_dependencies() -> list[str]:
    optional = pyproject()["project"]["optional-dependencies"]
    assert isinstance(optional, dict)
    deps = optional["dev"]
    assert isinstance(deps, list)
    return [str(item) for item in deps]


def route_paths(app: FastAPI) -> set[str]:
    return {str(route.path) for route in app.routes}


def project_events(captured: str) -> list[dict[str, object]]:
    records = [json.loads(line) for line in captured.splitlines() if line]
    return [record for record in records if "event" in record]


def test_chg_0001_exists_only_in_archive_with_history_preserved() -> None:
    assert not (ROOT / "changes" / "active" / CHG_0001).exists()
    archive = ROOT / "changes" / "archive" / CHG_0001
    assert archive.is_dir()
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_for(archive / name) == "ARCHIVED"
    assert (archive / "tests" / "test_acceptance.py").is_file()


def test_only_chg_0002_is_active_and_implementing() -> None:
    active_dirs = sorted(path.name for path in (ROOT / "changes" / "active").iterdir() if path.is_dir())
    assert active_dirs == [CHG_0002]
    for name in CHANGE_DOCUMENTS:
        assert status_for(active_change_dir() / name) == "IMPLEMENTING"


def test_chg_0002_core_documents_are_readable_and_complete() -> None:
    expected_headings = {
        "proposal.md": ["## Problem", "## Goal"],
        "design.md": [
            "## Responsibility rules",
            "## T4 implementation decision",
            "## T5 implementation decision",
            "## T6 implementation decision",
            "## T7 implementation decision",
            "## T8 implementation decision",
            "## T9 implementation decision",
            "## T10 implementation decision",
        ],
        "acceptance.md": ["## Final acceptance criteria"],
    }
    for name in CORE_DOCUMENTS:
        text = (active_change_dir() / name).read_text(encoding="utf-8")
        assert REPEATED_QUESTION_MARKS not in text
        assert REPLACEMENT_CHARACTER not in text
        assert status_for(active_change_dir() / name) == "IMPLEMENTING"
        for heading in expected_headings[name]:
            assert heading in text

    acceptance = (active_change_dir() / "acceptance.md").read_text(encoding="utf-8")
    criteria = re.findall(r"^\d+\. ", acceptance, flags=re.MULTILINE)
    assert len(criteria) == 25


def test_chg_0002_t10_is_complete_and_t11_is_next() -> None:
    tasks = chg_0002_tasks()
    assert [task.text for task in tasks] == [
        "T1 Archive CHG-0001 and establish CHG-0002 active change",
        "T2 Approve CHG-0002 architecture and dependency boundary",
        "T3 Add approved core application dependencies",
        "T4 Implement application factory and lifespan",
        "T5 Implement typed configuration",
        "T6 Implement structured redacted logging",
        "T7 Implement SQLite WAL and SQLAlchemy infrastructure",
        "T8 Establish Alembic migration baseline",
        "T9 Implement scheduler lifecycle skeleton",
        "T10 Implement health API contract and route",
        "T11 Implement Jinja2 and HTMX web skeleton",
        "T12 Add unit, contract and active-change acceptance tests",
        "T13 Update capability registry implementation and verification paths",
        "T14 Run complete local verification",
        "T15 Push branch and open Draft PR",
    ]
    completed = {task.text.split(" ", 1)[0] for task in tasks if task.completed}
    incomplete = {task.text.split(" ", 1)[0] for task in tasks if not task.completed}
    assert completed == {"T1", "T2", "T3", "T4", "T5", "T6", "T7", "T8", "T9", "T10"}
    assert incomplete == {f"T{index}" for index in range(11, 16)}

    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["tasks"]["next_task"] == "T11 Implement Jinja2 and HTMX web skeleton"


def test_approved_core_dependencies_are_declared_with_dev_httpx_only() -> None:
    runtime = runtime_dependencies()
    runtime_names = {dependency_name(item) for item in runtime}
    dev_names = {dependency_name(item) for item in dev_dependencies()}
    assert runtime_names == GOVERNANCE_RUNTIME | APPROVED_CORE_RUNTIME
    assert "httpx" in dev_names
    assert "httpx" not in runtime_names
    assert runtime_names.isdisjoint(FORBIDDEN_RUNTIME)
    for requirement in runtime:
        name = dependency_name(requirement)
        if name in APPROVED_CORE_RUNTIME:
            assert ">=" in requirement
            assert "<" in requirement


def test_t5_configuration_modules_exist_with_settings_boundary() -> None:
    for relative in CONFIGURATION_MODULES:
        assert (ROOT / relative).is_file()
    assert issubclass(ApplicationSettings, BaseSettings)
    assert ApplicationSettings.model_config["env_prefix"] == "XIANYU_"
    assert ApplicationSettings.model_config["frozen"] is True
    assert ApplicationSettings.model_config["env_file"] is None
    assert set(ApplicationSettings.model_fields) == {
        "environment",
        "app_title",
        "app_version",
        "debug",
        "log_level",
        "database_path",
    }


def test_t5_settings_have_no_sensitive_platform_fields() -> None:
    field_names = set(ApplicationSettings.model_fields)
    assert all(
        forbidden not in field_name
        for field_name in field_names
        for forbidden in FORBIDDEN_SETTING_FIELD_PARTS
    )


def test_application_factory_accepts_and_stores_settings() -> None:
    supplied = ApplicationSettings(app_title="Configured XIANYU", app_version="5.0.0", debug=True)
    app = create_application(settings=supplied)

    assert app.state.settings is supplied
    assert app.title == "Configured XIANYU"
    assert app.version == "5.0.0"
    assert app.debug is True


def test_default_applications_get_distinct_settings_instances() -> None:
    first = create_application()
    second = create_application()

    assert isinstance(first.state.settings, ApplicationSettings)
    assert isinstance(second.state.settings, ApplicationSettings)
    assert first.state.settings is not second.state.settings


def test_t5_imports_do_not_create_database_or_runtime_artifacts(tmp_path: Path) -> None:
    env = os.environ.copy()
    pythonpath_parts = [str(ROOT / "app")]
    if env.get("PYTHONPATH"):
        pythonpath_parts.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(pythonpath_parts)

    result = subprocess.run(
        [sys.executable, "-c", "import xianyu_system.core.config; import xianyu_system.main"],
        cwd=tmp_path,
        env=env,
        check=True,
        text=True,
        capture_output=True,
    )

    assert result.stderr == ""
    for relative in ["data", "logs", ".env"]:
        assert not (tmp_path / relative).exists()
    for pattern in ["*.db", "*.sqlite", "*.sqlite3"]:
        assert list(tmp_path.glob(pattern)) == []


def test_env_example_contains_only_current_safe_configuration() -> None:
    lines = (ROOT / ".env.example").read_text(encoding="utf-8").splitlines()
    assignments = [line for line in lines if line and not line.startswith("#")]
    keys = {line.split("=", 1)[0] for line in assignments}
    text = "\n".join(lines).upper()

    assert keys == SUPPORTED_ENV_EXAMPLE_KEYS
    assert len(assignments) == 6
    for forbidden in FORBIDDEN_ENV_EXAMPLE_PARTS:
        assert forbidden not in text


def test_t6_application_has_no_business_or_web_routes() -> None:
    app = create_application()

    assert route_paths(app) <= DEFAULT_FASTAPI_ROUTE_PATHS
    assert set(app.openapi()["paths"]) == {"/health"}
    assert "/" not in route_paths(app)
    for forbidden in ["/ready", "/live", "/metrics", "/status", "/api/health", "/login", "/messages", "/products", "/publish", "/schedule", "/wecom", "/ai", "/accounts"]:
        assert forbidden not in app.openapi()["paths"]


def test_t6_application_sources_avoid_legacy_events_and_server_startup() -> None:
    for relative in APPLICATION_MODULES:
        source = (ROOT / relative).read_text(encoding="utf-8")
        assert ".on_event(" not in source
        assert "uvicorn.run(" not in source


def test_t6_logging_module_exists_with_standard_library_boundaries() -> None:
    for relative in LOGGING_MODULES:
        assert (ROOT / relative).is_file()
    assert issubclass(StructuredJsonFormatter, logging.Formatter)
    assert callable(redact_value)
    assert callable(configure_logging)
    assert callable(shutdown_logging)

    source = (ROOT / "app/xianyu_system/core/logging.py").read_text(encoding="utf-8")
    assert "import logging" in source
    assert "basicConfig(" not in source
    assert "logging.shutdown(" not in source
    assert "FileHandler" not in source
    for forbidden in ["structlog", "python-json-logger", "loguru", "sentry", "opentelemetry"]:
        assert forbidden not in source


def test_t6_logging_redacts_sensitive_fields_and_messages() -> None:
    synthetic = "synthetic" + "-value"
    assert redact_value({"token": synthetic, "safe": "ok"}) == {
        "token": REDACTED_VALUE,
        "safe": "ok",
    }

    stream = io.StringIO()
    logger = configure_logging(level="INFO", logger_name="xianyu.acceptance.logging", stream=stream)
    logger.info(
        "Authorization: Bearer " + synthetic,
        extra={"event": "acceptance", "Cookie": synthetic, "password_policy_enabled": True},
    )
    shutdown_logging(logger)

    line = stream.getvalue().strip()
    data = json.loads(line)
    assert data["event"] == "acceptance"
    assert data["Cookie"] == REDACTED_VALUE
    assert data["password_policy_enabled"] is True
    assert synthetic not in line
    assert REDACTED_VALUE in line


def test_t6_logging_is_configured_only_during_lifespan_and_uses_distinct_loggers(
    tmp_path: Path,
    capsys,
) -> None:
    first = create_application(
        settings=ApplicationSettings(
            environment="test", log_level="INFO", database_path=tmp_path / "first-logging.db"
        )
    )
    second = create_application(
        settings=ApplicationSettings(
            environment="test", log_level="INFO", database_path=tmp_path / "second-logging.db"
        )
    )

    assert not hasattr(first.state, "logger")
    assert not hasattr(second.state, "logger")

    with TestClient(first), TestClient(second):
        assert hasattr(first.state, "logger")
        assert hasattr(second.state, "logger")
        assert first.state.logger.name != second.state.logger.name
        assert any(isinstance(handler, ManagedStreamHandler) for handler in first.state.logger.handlers)

    assert not any(isinstance(handler, ManagedStreamHandler) for handler in first.state.logger.handlers)
    events = [event["event"] for event in project_events(capsys.readouterr().err)]
    assert events.count("application.startup") == 2
    assert events.count("database.ready") == 2
    assert events.count("scheduler.ready") == 2
    assert events.count("scheduler.shutdown") == 2
    assert events.count("database.shutdown") == 2
    assert events.count("application.shutdown") == 2


def test_t7_database_module_exists_with_sqlalchemy_boundaries(tmp_path: Path) -> None:
    for relative in DATABASE_MODULES:
        assert (ROOT / relative).is_file()

    assert Base.metadata.tables == {}
    url = build_sqlite_url(tmp_path / "acceptance db.sqlite")
    assert url.drivername == "sqlite+pysqlite"
    assert url.database == str((tmp_path / "acceptance db.sqlite").resolve(strict=False))

    engine = create_database_engine(tmp_path / "lazy.db")
    try:
        assert not (tmp_path / "lazy.db").exists()
        factory = create_session_factory(engine)
        assert factory.kw["autoflush"] is False
        assert factory.kw["expire_on_commit"] is False
    finally:
        engine.dispose()

    source = (ROOT / "app/xianyu_system/core/database.py").read_text(encoding="utf-8")
    assert "check_same_thread" in source
    assert "journal_mode=WAL" in source
    assert "foreign_keys=ON" in source
    assert "busy_timeout=5000" in source
    assert "metadata.create_all" not in source
    assert "metadata.drop_all" not in source
    assert "Table(" not in source
    assert "mapped_column(" not in source
    assert "__tablename__" not in source


def test_t7_database_initialization_wal_session_and_empty_schema(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "acceptance.db")
    try:
        assert isinstance(resources, DatabaseResources)
        assert resources.path.is_absolute()
        assert resources.path.exists()
        with resources.engine.connect() as connection:
            assert str(connection.exec_driver_sql("PRAGMA journal_mode").scalar_one()).lower() == "wal"
            assert connection.exec_driver_sql("PRAGMA foreign_keys").scalar_one() == 1
            assert connection.exec_driver_sql("PRAGMA busy_timeout").scalar_one() >= 5000
            tables = connection.exec_driver_sql(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).scalars().all()
            assert [name for name in tables if not str(name).startswith("sqlite_")] == []
        with open_session(resources) as session:
            assert session.execute(text("SELECT 1")).scalar_one() == 1
    finally:
        dispose_database(resources)


def test_t7_database_lifespan_initializes_and_disposes_per_application(
    tmp_path: Path, capsys
) -> None:
    first = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "first-app.db")
    )
    second = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "second-app.db")
    )

    assert not hasattr(first.state, "database")
    with TestClient(first), TestClient(second):
        assert isinstance(first.state.database, DatabaseResources)
        assert isinstance(second.state.database, DatabaseResources)
        assert first.state.database.engine is not second.state.database.engine
        assert first.state.database.path != second.state.database.path

    assert first.state.database is None
    assert second.state.database is None
    events = [event["event"] for event in project_events(capsys.readouterr().err)]
    assert events.count("database.ready") == 2
    assert events.count("scheduler.ready") == 2
    assert events.count("scheduler.shutdown") == 2
    assert events.count("database.shutdown") == 2


def test_t8_alembic_files_and_configuration_are_minimal() -> None:
    for relative in MIGRATION_PATHS:
        assert (ROOT / relative).is_file()

    config_text = (ROOT / "alembic.ini").read_text(encoding="utf-8")
    assert "script_location = %(here)s/migrations" in config_text
    assert "sqlalchemy.url =" in config_text
    assert "data/xianyu.db" not in config_text
    assert "[loggers]" not in config_text
    assert "[handlers]" not in config_text
    assert "[formatters]" not in config_text

    config = build_alembic_config()
    assert config.get_main_option("sqlalchemy.url") == ""
    script = ScriptDirectory.from_config(config)
    assert script.get_heads() == [BASELINE_REVISION]
    assert script.get_revision(BASELINE_REVISION).down_revision is None


def test_t8_alembic_environment_uses_base_metadata_and_shared_connection() -> None:
    env_source = (ROOT / "migrations" / "env.py").read_text(encoding="utf-8")
    baseline_source = (ROOT / "migrations" / "versions" / "0001_core_baseline.py").read_text(
        encoding="utf-8"
    )

    assert "target_metadata = Base.metadata" in env_source
    assert "MetaData(" not in env_source
    assert 'config.attributes.get("connection")' in env_source
    assert "fileConfig(" not in env_source
    assert "logging.config" not in env_source
    assert "engine_from_config" not in env_source
    assert "create_engine" not in env_source
    assert "get_explicit_database_path" in env_source
    assert "database_path" in env_source

    assert f'revision: str = "{BASELINE_REVISION}"' in baseline_source
    assert "down_revision: str | None = None" in baseline_source
    assert "pass" in baseline_source
    for forbidden in [
        "op.create_table",
        "op.drop_table",
        "op.add_column",
        "op.execute",
        "bulk_insert",
        "Table(",
        "__tablename__",
        "mapped_column(",
        "metadata.create_all",
        "metadata.drop_all",
    ]:
        assert forbidden not in baseline_source
    assert Base.metadata.tables == {}


def test_t8_programmatic_upgrade_downgrade_check_and_no_business_tables(tmp_path: Path) -> None:
    resources = initialize_database(tmp_path / "acceptance-migration.db")
    try:
        assert get_current_revision(resources) is None
        upgrade_database(resources)
        assert get_current_revision(resources) == BASELINE_REVISION
        assert set(inspect(resources.engine).get_table_names()) <= {"alembic_version"}
        upgrade_database(resources)
        assert get_current_revision(resources) == BASELINE_REVISION
        with resources.engine.begin() as connection:
            command.check(build_alembic_config(connection=connection))
        downgrade_database(resources)
        assert get_current_revision(resources) is None
        upgrade_database(resources)
        assert get_current_revision(resources) == BASELINE_REVISION
    finally:
        dispose_database(resources)


def test_t8_cli_and_offline_paths_require_explicit_database_path(tmp_path: Path) -> None:
    cli_db = tmp_path / "cli.db"
    cli = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "alembic.ini",
            "-x",
            f"database_path={cli_db}",
            "upgrade",
            "head",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert cli.returncode == 0
    assert cli_db.exists()

    missing = subprocess.run(
        [sys.executable, "-m", "alembic", "-c", "alembic.ini", "upgrade", "head"],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    assert missing.returncode != 0
    assert "database_path" in missing.stdout + missing.stderr
    assert "shared connection" in missing.stdout + missing.stderr

    offline_db = tmp_path / "offline.db"
    offline = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            "alembic.ini",
            "-x",
            f"database_path={offline_db}",
            "upgrade",
            "head",
            "--sql",
        ],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "alembic_version" in offline.stdout
    assert not offline_db.exists()
    assert not (ROOT / "data" / "xianyu.db").exists()


def test_t8_application_startup_does_not_auto_migrate(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "app.db")
    )

    with TestClient(app):
        assert get_current_revision(app.state.database) is None
        assert set(inspect(app.state.database.engine).get_table_names()) == set()

    assert app.state.database is None


def test_t8_migration_files_have_no_sensitive_or_business_data() -> None:
    combined = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (ROOT / "migrations").rglob("*")
        if path.is_file() and "__pycache__" not in path.parts
    )
    for forbidden in [
        "cookie",
        "token",
        "secret",
        "password",
        "customer",
        "message content",
        "phone",
        "email address",
        "real account",
    ]:
        assert forbidden not in combined




def test_t9_scheduler_module_exists_with_in_memory_lifecycle_boundary() -> None:
    for relative in SCHEDULER_MODULES:
        assert (ROOT / relative).is_file()

    logger = logging.getLogger("xianyu.acceptance.scheduler")
    logger.handlers.clear()
    logger.propagate = False
    scheduler = create_scheduler(logger=logger)
    try:
        assert isinstance(scheduler, BackgroundScheduler)
        assert scheduler.running is False
        assert scheduler.timezone == SCHEDULER_TIMEZONE
        assert isinstance(scheduler._jobstores["default"], MemoryJobStore)
        assert scheduler.get_jobs() == []

        start_scheduler(scheduler)
        assert scheduler.running is True
        assert scheduler.get_jobs() == []
    finally:
        shutdown_scheduler(scheduler)

    assert scheduler.running is False


def test_t9_scheduler_source_has_no_jobs_persistence_or_business_logic() -> None:
    source = (ROOT / "app/xianyu_system/core/scheduler.py").read_text(encoding="utf-8")

    assert "BackgroundScheduler" in source
    assert "MemoryJobStore" in source
    assert "UTC" in source
    assert "SQLAlchemyJobStore" not in source
    assert "apscheduler_jobs" not in source
    assert "add_job(" not in source
    assert "scheduled_job(" not in source
    for forbidden in ["xianyu", "wecom", "ai_provider", "playwright", "selenium"]:
        assert forbidden not in source.lower()


def test_t9_application_lifespan_starts_and_stops_scheduler_in_order(
    tmp_path: Path, capsys
) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "scheduler-app.db")
    )

    assert not hasattr(app.state, "scheduler")
    with TestClient(app):
        assert isinstance(app.state.scheduler, BackgroundScheduler)
        assert app.state.scheduler.running is True
        assert app.state.scheduler.get_jobs() == []
        assert get_current_revision(app.state.database) is None

    assert app.state.scheduler is None
    assert app.state.database is None
    events = [event["event"] for event in project_events(capsys.readouterr().err)]
    assert events == [
        "application.startup",
        "database.ready",
        "scheduler.ready",
        "scheduler.shutdown",
        "database.shutdown",
        "application.shutdown",
    ]


def test_t9_scheduler_does_not_create_database_tables_or_migration_state(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "scheduler-db.db")
    )

    with TestClient(app):
        assert get_current_revision(app.state.database) is None
        assert set(inspect(app.state.database.engine).get_table_names()) == set()


def test_t9_schedule_capability_remains_planned_and_unbound() -> None:
    capability = registry_by_id()["CAP-XY-SCHEDULE"]

    assert capability["status"] == "planned"
    assert capability["active_change"] is None
    assert capability["last_verified_commit"] is None



def test_t10_api_modules_and_health_models_exist() -> None:
    for relative in API_MODULES:
        assert (ROOT / relative).is_file()
    assert HealthResponse.model_fields.keys() == {
        "status",
        "service",
        "version",
        "environment",
        "database",
        "scheduler",
    }
    assert DatabaseHealth.model_fields.keys() == {"status", "connected", "journal_mode"}
    assert SchedulerHealth.model_fields.keys() == {"status", "running", "job_count", "timezone"}


def test_t10_health_endpoint_returns_200_and_safe_local_state(tmp_path: Path) -> None:
    settings = ApplicationSettings(environment="test", database_path=tmp_path / "acceptance-health.db")
    app = create_application(settings=settings)

    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "status": "ok",
            "service": settings.app_title,
            "version": settings.app_version,
            "environment": "test",
            "database": {"status": "ok", "connected": True, "journal_mode": "wal"},
            "scheduler": {"status": "ok", "running": True, "job_count": 0, "timezone": "UTC"},
        }
        assert get_current_revision(app.state.database) is None
        assert set(inspect(app.state.database.engine).get_table_names()) == set()
        assert app.state.scheduler.get_jobs() == []

    body = json.dumps(data).lower()
    assert str(settings.database_path).lower() not in body
    for forbidden in ["cookie", "token", "secret", "password", "credential", "account", "customer", "traceback", "exception"]:
        assert forbidden not in body


def test_t10_health_degraded_behavior_outside_lifespan_and_component_failures(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "degraded.db")
    )

    outside = collect_health(app)
    assert outside.status == "degraded"
    assert outside.database.status == "unavailable"
    assert outside.scheduler.status == "unavailable"

    assert collect_database_health(None) == DatabaseHealth(
        status="unavailable", connected=False, journal_mode=None
    )
    assert collect_scheduler_health(None) == SchedulerHealth(
        status="unavailable", running=False, job_count=0, timezone="UTC"
    )


def test_t10_health_route_is_get_only_and_has_expected_runtime_openapi(tmp_path: Path) -> None:
    app = create_application(
        settings=ApplicationSettings(environment="test", database_path=tmp_path / "openapi-health.db")
    )

    with TestClient(app) as client:
        assert client.get("/health").status_code == 200
        assert client.post("/health").status_code == 405
        assert client.put("/health").status_code == 405
        assert client.delete("/health").status_code == 405

    schema = app.openapi()
    assert set(schema["paths"]) == {"/health"}
    operation = schema["paths"]["/health"]["get"]
    assert operation["operationId"] == "get_health"
    assert {"200", "503"} <= set(operation["responses"])
    assert operation.get("parameters", []) == []
    assert "security" not in schema
    assert "securitySchemes" not in schema.get("components", {})


def test_t10_health_source_has_no_external_write_migration_or_scheduler_mutation_code() -> None:
    combined = "\n".join((ROOT / relative).read_text(encoding="utf-8") for relative in API_MODULES)
    for forbidden in [
        "requests.",
        "httpx.",
        "urllib.",
        "socket.",
        "playwright",
        "selenium",
        "wecom",
        "openai",
        "initialize_database",
        "create_database_engine",
        "create_session_factory",
        "upgrade_database",
        "command.upgrade",
        "metadata.create_all",
        "INSERT ",
        "UPDATE ",
        "DELETE ",
        "CREATE TABLE",
        ".add_job(",
        ".remove_job(",
        ".remove_all_jobs(",
    ]:
        assert forbidden not in combined


def test_t10_health_contract_and_runtime_schema_are_semantically_consistent() -> None:
    import yaml

    contract = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    runtime = create_application().openapi()
    assert set(contract["paths"]) == set(runtime["paths"]) == {"/health"}
    contract_operation = contract["paths"]["/health"]["get"]
    runtime_operation = runtime["paths"]["/health"]["get"]
    assert contract_operation["operationId"] == runtime_operation["operationId"] == "get_health"
    assert {"200", "503"} <= set(contract_operation["responses"])
    assert {"200", "503"} <= set(runtime_operation["responses"])
    for name in ["HealthResponse", "DatabaseHealth", "SchedulerHealth"]:
        assert name in contract["components"]["schemas"]
        assert name in runtime["components"]["schemas"]


def test_deferred_core_modules_and_artifacts_are_not_created() -> None:
    for relative in DEFERRED_CORE_PATHS + FORBIDDEN_ARTIFACT_PATHS:
        assert not (ROOT / relative).exists()
    tracked = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.splitlines()
    forbidden_suffixes = (".db", ".sqlite", ".sqlite3")
    assert [path for path in tracked if path.endswith(forbidden_suffixes)] == []
    ignored_runtime = {".mypy_cache", ".venv", "__pycache__"}
    project_database_files = [
        path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.suffix in forbidden_suffixes
        and ignored_runtime.isdisjoint(path.relative_to(ROOT).parts)
    ]
    assert project_database_files == []


def test_openapi_contract_has_only_health_path_and_no_business_paths() -> None:
    import yaml

    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert set(openapi["paths"]) == {"/health"}
    operation = openapi["paths"]["/health"]["get"]
    assert operation["operationId"] == "get_health"
    assert set(operation["responses"]) == {"200", "503"}
    assert "security" not in openapi
    assert "securitySchemes" not in openapi.get("components", {})
    for forbidden in ["/", "/ready", "/live", "/metrics", "/status", "/api/health", "/login", "/messages", "/products", "/publish", "/schedule", "/wecom", "/ai", "/accounts"]:
        assert forbidden not in openapi["paths"]


def test_core_capabilities_are_implementing_and_none_are_verified() -> None:
    registry = registry_by_id()
    assert {str(item["status"]) for item in registry.values() if item["id"] in CORE_CAPABILITIES} == {
        "implementing"
    }
    for cap_id in CORE_CAPABILITIES:
        capability = registry[cap_id]
        assert capability["active_change"] == CHG_0002
        assert capability["last_verified_commit"] is None
    assert all(capability["status"] != "verified" for capability in registry.values())


def test_other_capabilities_remain_planned_and_unbound() -> None:
    registry = registry_by_id()
    for cap_id, capability in registry.items():
        if cap_id in CORE_CAPABILITIES:
            continue
        assert capability["status"] == "planned"
        assert capability["active_change"] is None
        assert capability["last_verified_commit"] is None


def test_project_state_matches_current_repository() -> None:
    actual = (ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8")
    assert actual == project_state_json(ROOT)


def test_branch_name_matches_active_change_id() -> None:
    current_branch = subprocess.run(
        ["git", "branch", "--show-current"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    branch = current_branch or os.environ.get("GITHUB_HEAD_REF", "")
    match = re.search(r"CHG-\d{4}-[A-Za-z0-9_.-]+", branch)
    assert match is not None
    assert match.group(0) == CHG_0002
