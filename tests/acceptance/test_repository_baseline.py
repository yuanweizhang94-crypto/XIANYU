from __future__ import annotations

from pathlib import Path

import yaml

from scripts.repo_utils import required_repo_paths

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


def test_no_business_dependencies_are_declared() -> None:
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    forbidden = ["FastAPI", "SQLAlchemy", "APScheduler", "Playwright", "Redis", "Celery", "LangChain"]
    for dependency in forbidden:
        assert dependency not in pyproject


def test_openapi_paths_are_empty() -> None:
    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert openapi["paths"] == {}
