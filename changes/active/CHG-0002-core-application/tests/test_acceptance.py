from __future__ import annotations

import json
import os
import re
import subprocess
import tomllib
from pathlib import Path

from scripts.generate_state import project_state_json
from scripts.repo_utils import parse_tasks, read_yaml

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
CORE_DOCUMENTS = ["proposal.md", "design.md", "acceptance.md"]
REPEATED_QUESTION_MARKS = "?" * 3
REPLACEMENT_CHARACTER = chr(0xFFFD)
PLANNED_CORE_MODULES = [
    "app/xianyu_system/main.py",
    "app/xianyu_system/application.py",
    "app/xianyu_system/core/__init__.py",
    "app/xianyu_system/core/config.py",
    "app/xianyu_system/core/logging.py",
    "app/xianyu_system/core/database.py",
    "app/xianyu_system/core/scheduler.py",
    "app/xianyu_system/api/__init__.py",
    "app/xianyu_system/api/router.py",
    "app/xianyu_system/api/health.py",
    "app/xianyu_system/web/__init__.py",
    "app/xianyu_system/web/router.py",
    "app/xianyu_system/domain/__init__.py",
]
FORBIDDEN_ALEMBIC_PATHS = ["alembic.ini", "migrations", "alembic"]


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
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_for(active_change_dir() / name) == "IMPLEMENTING"


def test_chg_0002_core_documents_are_readable_and_complete() -> None:
    expected_headings = {
        "proposal.md": ["## Problem", "## Goal"],
        "design.md": ["## Responsibility rules"],
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


def test_chg_0002_t3_is_complete_and_t4_is_next() -> None:
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
    assert completed == {"T1", "T2", "T3"}
    assert incomplete == {f"T{index}" for index in range(4, 16)}

    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["tasks"]["next_task"] == "T4 Implement application factory and lifespan"


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


def test_t3_does_not_create_core_runtime_modules_or_artifacts() -> None:
    for relative in PLANNED_CORE_MODULES:
        assert not (ROOT / relative).exists()
    for relative in FORBIDDEN_ALEMBIC_PATHS:
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


def test_openapi_still_has_no_business_or_health_paths() -> None:
    import yaml

    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert openapi["paths"] == {}
    assert "/health" not in openapi["paths"]


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
