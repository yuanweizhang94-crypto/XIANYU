from __future__ import annotations

from pathlib import Path

import yaml

from scripts.repo_utils import read_yaml, required_repo_paths

ROOT = Path(__file__).resolve().parents[2]


def test_standard_repository_structure_is_complete() -> None:
    missing = [path for path in required_repo_paths() if not (ROOT / path).exists()]
    assert missing == []


def test_adr_files_exist_and_are_accepted() -> None:
    adr_files = sorted((ROOT / "docs" / "adr").glob("ADR-*.md"))
    assert adr_files
    for path in adr_files:
        text = path.read_text(encoding="utf-8")
        assert "## Status" in text
        assert "Accepted" in text


def test_chg_0001_initial_capability_registry_has_ten_capabilities() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    assert len(registry["capabilities"]) == 10


def test_agents_md_has_no_specific_change_identifier() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "CHG-0001" not in text
    assert "project-baseline" not in text


def test_readme_does_not_hardcode_active_change_directory() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "changes/active/CHG-0001-project-baseline/" not in text
    assert "uniquely dynamically discovered active change directory" in text


def test_no_business_dependencies_are_declared() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    forbidden = ["FastAPI", "SQLAlchemy", "APScheduler", "Playwright", "Redis", "Celery", "LangChain"]
    for dependency in forbidden:
        assert dependency not in pyproject


def test_openapi_paths_are_empty() -> None:
    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert openapi["paths"] == {}
