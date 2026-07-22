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

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic_settings import BaseSettings

from scripts.generate_state import project_state_json
from scripts.repo_utils import parse_tasks, read_yaml
from xianyu_system.application import create_application
from xianyu_system.core.config import ApplicationSettings
from xianyu_system.core.logging import (
    REDACTED_VALUE,
    ManagedStreamHandler,
    StructuredJsonFormatter,
    configure_logging,
    redact_value,
    shutdown_logging,
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
DEFERRED_CORE_PATHS = [
    "app/xianyu_system/core/database.py",
    "app/xianyu_system/core/scheduler.py",
    "app/xianyu_system/api",
    "app/xianyu_system/web",
    "app/xianyu_system/domain",
    "app/xianyu_system/api/router.py",
    "app/xianyu_system/api/health.py",
    "app/xianyu_system/web/router.py",
]
FORBIDDEN_ARTIFACT_PATHS = [
    "alembic.ini",
    "migrations",
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
DEFAULT_FASTAPI_ROUTE_PATHS = {"/openapi.json", "/docs", "/docs/oauth2-redirect", "/redoc"}


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


def test_chg_0002_t6_is_complete_and_t7_is_next() -> None:
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
    assert completed == {"T1", "T2", "T3", "T4", "T5", "T6"}
    assert incomplete == {f"T{index}" for index in range(7, 16)}

    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["tasks"]["next_task"] == "T7 Implement SQLite WAL and SQLAlchemy infrastructure"


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


def test_t6_application_has_no_business_or_health_routes() -> None:
    app = create_application()

    assert route_paths(app) <= DEFAULT_FASTAPI_ROUTE_PATHS
    assert app.openapi()["paths"] == {}
    assert "/health" not in app.openapi()["paths"]
    assert "/" not in route_paths(app)


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
    capsys,
) -> None:
    first = create_application(settings=ApplicationSettings(environment="test", log_level="INFO"))
    second = create_application(settings=ApplicationSettings(environment="test", log_level="INFO"))

    assert not hasattr(first.state, "logger")
    assert not hasattr(second.state, "logger")

    with TestClient(first), TestClient(second):
        assert hasattr(first.state, "logger")
        assert hasattr(second.state, "logger")
        assert first.state.logger.name != second.state.logger.name
        assert any(isinstance(handler, ManagedStreamHandler) for handler in first.state.logger.handlers)

    assert not any(isinstance(handler, ManagedStreamHandler) for handler in first.state.logger.handlers)
    events = [json.loads(line)["event"] for line in capsys.readouterr().err.splitlines()]
    assert events.count("application.startup") == 2
    assert events.count("application.shutdown") == 2


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


def test_openapi_contract_still_has_no_business_or_health_paths() -> None:
    import yaml

    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert openapi["paths"] == {}
    assert "/health" not in openapi["paths"]


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
