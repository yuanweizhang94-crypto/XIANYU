from __future__ import annotations

import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
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
REQUIRED_DEV = {"pytest", "ruff", "mypy", "httpx"}
FORBIDDEN_DEPENDENCIES = {
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
VERSION_TOKEN_PATTERN = re.compile(r"(?:>=|<=|==|!=|~=|>|<)\s*([^,;\s]+)")
PRE_RELEASE_PATTERN = re.compile(r"(?i)(?:a|b|rc|dev)\d+")


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


def test_runtime_dependencies_match_approved_chg_0002_boundary() -> None:
    names = {dependency_name(item) for item in runtime_dependencies()}
    assert names == GOVERNANCE_RUNTIME | APPROVED_CORE_RUNTIME


def test_dev_dependencies_include_httpx_without_runtime_leakage() -> None:
    runtime_names = {dependency_name(item) for item in runtime_dependencies()}
    dev_names = {dependency_name(item) for item in dev_dependencies()}
    assert dev_names >= REQUIRED_DEV
    assert "httpx" not in runtime_names


def test_core_runtime_dependencies_have_safe_version_bounds() -> None:
    requirements = {dependency_name(item): item for item in runtime_dependencies()}
    for name in sorted(APPROVED_CORE_RUNTIME):
        requirement = requirements[name]
        assert ">=" in requirement, f"{name} must declare a minimum version"
        assert "<" in requirement, f"{name} must declare a next-major upper bound"
        assert "*" not in requirement, f"{name} must not use wildcard versions"
        assert "@" not in requirement, f"{name} must not use direct URLs"
        assert "git+" not in requirement.lower(), f"{name} must not use git URLs"
        assert not re.search(r"(?:^|[\s,])(?:\.|/|[A-Za-z]:\\)", requirement), (
            f"{name} must not use local paths"
        )
        version_tokens = VERSION_TOKEN_PATTERN.findall(requirement)
        assert all(PRE_RELEASE_PATTERN.search(token) is None for token in version_tokens), (
            f"{name} must not use prerelease versions"
        )


def test_forbidden_dependencies_are_not_declared() -> None:
    declared = {dependency_name(item) for item in runtime_dependencies() + dev_dependencies()}
    forbidden = declared & FORBIDDEN_DEPENDENCIES
    assert forbidden == set(), f"forbidden dependencies declared: {sorted(forbidden)}"
