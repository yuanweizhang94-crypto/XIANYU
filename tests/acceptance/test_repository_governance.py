from __future__ import annotations

import json
import re
import shutil
import tomllib
from pathlib import Path

import jsonschema
import yaml

from scripts.generate_state import project_state_json
from scripts.repo_utils import find_active_changes, read_yaml, required_repo_paths
from scripts.security_scan import scan as security_scan

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_ADR_STATUSES = {"Proposed", "Accepted", "Superseded", "Deprecated", "Rejected"}


def pytest_testpaths() -> list[str]:
    data = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    return list(data["tool"]["pytest"]["ini_options"]["testpaths"])


def test_standard_repository_structure_is_complete() -> None:
    missing = [path for path in required_repo_paths() if not (ROOT / path).exists()]
    assert missing == []


def test_agents_md_has_no_specific_change_identifier() -> None:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    assert "CHG-0001" not in text
    assert "project-baseline" not in text


def test_readme_does_not_hardcode_active_change_directory() -> None:
    text = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "changes/active/CHG-0001-project-baseline/" not in text
    assert "uniquely dynamically discovered active change directory" in text


def test_changes_active_has_at_most_one_active_change() -> None:
    assert len(find_active_changes(ROOT)) <= 1


def test_pytest_default_testpaths_include_tests_and_active_changes_only() -> None:
    testpaths = pytest_testpaths()
    assert "tests" in testpaths
    assert "changes/active" in testpaths
    assert "changes/archive" not in testpaths


def test_current_active_change_specific_tests_are_discoverable() -> None:
    active_changes = find_active_changes(ROOT)
    for change_dir in active_changes:
        tests_dir = change_dir / "tests"
        assert tests_dir.is_dir()
        assert sorted(tests_dir.glob("test_*.py"))


def test_archived_change_tests_are_preserved_but_outside_default_collection(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    active_tests = root / "changes" / "active" / "CHG-9999-example" / "tests"
    active_tests.mkdir(parents=True)
    (active_tests / "test_acceptance.py").write_text("def test_example():\n    assert True\n", encoding="utf-8")

    archive_target = root / "changes" / "archive" / "CHG-9999-example"
    archive_target.parent.mkdir(parents=True)
    shutil.move(str(active_tests.parent), archive_target)

    assert (archive_target / "tests" / "test_acceptance.py").exists()
    assert "changes/archive" not in pytest_testpaths()


def test_permanent_governance_tests_do_not_keep_temporary_acceptance_locks() -> None:
    source = Path(__file__).read_text(encoding="utf-8")
    forbidden_snippets = [
        "len(" + 'registry["capabilities"]' + ") == 10",
        "openapi" + '["paths"]' + " == {}",
        "dependency" + " not in pyproject",
        "assert " + '"Accepted"' + " in text",
        "Status: " + 'VERIFYING" in',
    ]
    for snippet in forbidden_snippets:
        assert snippet not in source


def test_archived_status_exists_only_in_changes_archive() -> None:
    for change_file in (ROOT / "changes").glob("**/*.md"):
        if "Status: ARCHIVED" not in change_file.read_text(encoding="utf-8"):
            continue
        relative = change_file.relative_to(ROOT).as_posix()
        assert relative.startswith("changes/archive/")


def test_project_state_matches_generated_state() -> None:
    actual = (ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8")
    assert actual == project_state_json(ROOT)


def test_capability_registry_schema_is_valid() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    schema = json.loads((ROOT / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(registry, schema)
    assert registry["capabilities"]


def test_openapi_structure_is_valid() -> None:
    openapi = yaml.safe_load((ROOT / "contracts" / "openapi.yaml").read_text(encoding="utf-8"))
    assert isinstance(openapi, dict)
    assert openapi.get("openapi") == "3.1.0"
    assert isinstance(openapi.get("info"), dict)
    assert isinstance(openapi.get("paths"), dict)


def test_adr_files_have_required_structure_and_allowed_status() -> None:
    adr_files = sorted((ROOT / "docs" / "adr").glob("ADR-*.md"))
    assert adr_files
    for path in adr_files:
        text = path.read_text(encoding="utf-8")
        assert re.match(r"# ADR-\d{4}: .+", text.splitlines()[0])
        for heading in ["## Status", "## Context", "## Decision", "## Consequences"]:
            assert heading in text
        status_index = text.splitlines().index("## Status")
        status = next(line.strip() for line in text.splitlines()[status_index + 1 :] if line.strip())
        assert status in ALLOWED_ADR_STATUSES


def test_security_scan_has_no_findings() -> None:
    assert security_scan(ROOT) == []
