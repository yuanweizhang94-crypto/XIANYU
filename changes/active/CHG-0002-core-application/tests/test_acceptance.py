from __future__ import annotations

import re
import os
import subprocess
import tomllib
from pathlib import Path

from scripts.generate_state import project_state_json
from scripts.repo_utils import parse_tasks, read_yaml

ROOT = Path(__file__).resolve().parents[4]
CHG_0001 = "CHG-0001-project-baseline"
CHG_0002 = "CHG-0002-core-application"
CORE_CAPABILITIES = {"CAP-CORE-CONFIG", "CAP-CORE-DATABASE", "CAP-HEALTH-MONITOR"}
RUNTIME_DEPENDENCIES = {"fastapi", "sqlalchemy", "alembic", "apscheduler", "jinja2"}
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


def status_for(path: Path) -> str:
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("Status:"):
            return line.split(":", 1)[1].strip()
    return ""


def registry_by_id() -> dict[str, dict[str, object]]:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    return {str(item["id"]): item for item in registry["capabilities"]}


def test_chg_0001_exists_only_in_archive_with_history_preserved() -> None:
    assert not (ROOT / "changes" / "active" / CHG_0001).exists()
    archive = ROOT / "changes" / "archive" / CHG_0001
    assert archive.is_dir()
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_for(archive / name) == "ARCHIVED"
    assert (archive / "tests" / "test_acceptance.py").is_file()


def test_only_chg_0002_is_active_and_approved() -> None:
    active_dirs = sorted(path.name for path in (ROOT / "changes" / "active").iterdir() if path.is_dir())
    assert active_dirs == [CHG_0002]
    active = ROOT / "changes" / "active" / CHG_0002
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert status_for(active / name) == "APPROVED"


def test_chg_0002_preparation_tasks_are_scoped_to_t1_and_t2() -> None:
    tasks = parse_tasks(ROOT / "changes" / "active" / CHG_0002 / "tasks.md")
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
    assert completed == {"T1", "T2"}


def test_core_capabilities_are_implementing_and_bound_to_chg_0002() -> None:
    registry = registry_by_id()
    for cap_id in CORE_CAPABILITIES:
        capability = registry[cap_id]
        assert capability["status"] == "implementing"
        assert capability["active_change"] == CHG_0002
        assert capability["last_verified_commit"] is None


def test_other_capabilities_remain_planned_and_unbound() -> None:
    registry = registry_by_id()
    for cap_id, capability in registry.items():
        if cap_id in CORE_CAPABILITIES:
            continue
        assert capability["status"] == "planned"
        assert capability["active_change"] is None
        assert capability["last_verified_commit"] is None


def test_preparation_does_not_add_core_runtime_dependencies_or_code() -> None:
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = {str(item).split("[", 1)[0].split(">", 1)[0].split("=", 1)[0].lower() for item in pyproject.get("project", {}).get("dependencies", [])}
    assert dependencies.isdisjoint(RUNTIME_DEPENDENCIES)
    for relative in PLANNED_CORE_MODULES:
        assert not (ROOT / relative).exists()


def test_openapi_still_has_no_business_paths() -> None:
    import yaml

    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert openapi["paths"] == {}


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
