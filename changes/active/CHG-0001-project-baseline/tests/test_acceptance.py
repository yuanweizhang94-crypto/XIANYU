from __future__ import annotations

from pathlib import Path

import yaml

from scripts.repo_utils import read_yaml, parse_tasks

ROOT = Path(__file__).resolve().parents[4]
CHANGE_DIR = ROOT / "changes" / "active" / "CHG-0001-project-baseline"


def test_chg_0001_initial_capability_registry_has_ten_capabilities() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    assert len(registry["capabilities"]) == 10


def test_chg_0001_initial_capability_ids_are_expected() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    ids = {item["id"] for item in registry["capabilities"]}
    assert ids == {
        "CAP-CORE-CONFIG",
        "CAP-CORE-DATABASE",
        "CAP-XY-ACCOUNT",
        "CAP-XY-MESSAGE",
        "CAP-XY-REPLY",
        "CAP-XY-PUBLISH",
        "CAP-XY-SCHEDULE",
        "CAP-WECOM-CS",
        "CAP-AI-REPLY",
        "CAP-HEALTH-MONITOR",
    }


def test_chg_0001_all_initial_capabilities_remain_planned() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    capabilities = registry["capabilities"]
    assert {item["status"] for item in capabilities} == {"planned"}
    assert {item["active_change"] for item in capabilities} == {None}
    assert {item["last_verified_commit"] for item in capabilities} == {None}


def test_chg_0001_openapi_paths_are_empty() -> None:
    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert openapi["paths"] == {}


def test_chg_0001_no_business_dependencies_are_declared() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    forbidden = ["FastAPI", "SQLAlchemy", "APScheduler", "Playwright", "Redis", "Celery", "LangChain"]
    for dependency in forbidden:
        assert dependency not in pyproject


def test_chg_0001_initial_adr_files_exist_and_are_accepted() -> None:
    for index in range(1, 9):
        path = ROOT / "docs" / "adr" / f"ADR-{index:04d}.md"
        assert path.exists()
        text = path.read_text(encoding="utf-8")
        assert "## Status" in text
        assert "Accepted" in text


def test_chg_0001_has_no_business_capability_implementation() -> None:
    for relative in ["app/README.md", "worker/README.md", "adapters/README.md"]:
        assert (ROOT / relative).exists()
    source_files = sorted(
        path.relative_to(ROOT).as_posix()
        for directory in [ROOT / "app", ROOT / "worker", ROOT / "adapters"]
        for path in directory.rglob("*.py")
        if ".egg-info" not in path.parts
    )
    assert source_files == ["app/xianyu_system/__init__.py", "worker/__init__.py"]


def test_chg_0001_status_is_verifying() -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        assert "Status: VERIFYING" in (CHANGE_DIR / name).read_text(encoding="utf-8")


def test_chg_0001_all_tasks_are_complete() -> None:
    tasks = parse_tasks(CHANGE_DIR / "tasks.md")
    assert tasks
    assert all(task.completed for task in tasks)
