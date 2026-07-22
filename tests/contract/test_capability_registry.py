from __future__ import annotations

import json
import re
import subprocess
from collections import Counter
from pathlib import Path, PureWindowsPath

import jsonschema

from scripts.repo_utils import read_yaml

ROOT = Path(__file__).resolve().parents[2]
REGISTRY_PATH = ROOT / "specs" / "CAPABILITY_REGISTRY.yaml"
SCHEMA_PATH = ROOT / "contracts" / "schemas" / "capability-registry.schema.json"
PROJECT_STATE_PATH = ROOT / "generated" / "PROJECT_STATE.json"
CHG_0002 = "CHG-0002-core-application"
VERIFIED_CANDIDATE_SHA = "d11f1afc4564298e8c2709fdb80a41a491dbb1ea"
CORE_CAPABILITIES = {"CAP-CORE-CONFIG", "CAP-CORE-DATABASE", "CAP-HEALTH-MONITOR"}
EXPECTED_CAPABILITY_IDS = {
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
EXPECTED_OWNER_MODULES = {
    "CAP-CORE-CONFIG": "app.core.config",
    "CAP-CORE-DATABASE": "app.core.database",
    "CAP-HEALTH-MONITOR": "app.health",
}
EXPECTED_SPECIFICATIONS = {
    "CAP-CORE-CONFIG": "specs/capabilities/CAP-CORE-CONFIG.md",
    "CAP-CORE-DATABASE": "specs/capabilities/CAP-CORE-DATABASE.md",
    "CAP-HEALTH-MONITOR": "specs/capabilities/CAP-HEALTH-MONITOR.md",
}
EXPECTED_CORE_CAPABILITY_PATHS = {
    "CAP-CORE-CONFIG": {
        "implementation_paths": [
            "app/xianyu_system/core/config.py",
            "app/xianyu_system/application.py",
        ],
        "test_paths": [
            "tests/unit/test_config.py",
            "tests/unit/test_application_factory.py",
            "tests/unit/test_import_safety.py",
            "tests/contract/test_core_runtime.py",
            "tests/contract/test_distribution.py",
            "tests/contract/test_security_boundary.py",
            "changes/active/CHG-0002-core-application/tests/test_acceptance.py",
        ],
    },
    "CAP-CORE-DATABASE": {
        "implementation_paths": [
            "app/xianyu_system/core/database.py",
            "app/xianyu_system/application.py",
            "alembic.ini",
            "migrations/env.py",
            "migrations/script.py.mako",
            "migrations/versions/0001_core_baseline.py",
        ],
        "test_paths": [
            "tests/unit/test_database.py",
            "tests/unit/test_application_factory.py",
            "tests/unit/test_import_safety.py",
            "tests/contract/test_migrations.py",
            "tests/contract/test_core_runtime.py",
            "tests/contract/test_distribution.py",
            "tests/contract/test_security_boundary.py",
            "changes/active/CHG-0002-core-application/tests/test_acceptance.py",
        ],
    },
    "CAP-HEALTH-MONITOR": {
        "implementation_paths": [
            "app/xianyu_system/api/health.py",
            "app/xianyu_system/api/router.py",
            "app/xianyu_system/application.py",
            "contracts/openapi.yaml",
        ],
        "test_paths": [
            "tests/unit/test_health.py",
            "tests/unit/test_application_factory.py",
            "tests/unit/test_import_safety.py",
            "tests/contract/test_health_openapi.py",
            "tests/contract/test_core_runtime.py",
            "tests/contract/test_distribution.py",
            "tests/contract/test_security_boundary.py",
            "changes/active/CHG-0002-core-application/tests/test_acceptance.py",
        ],
    },
}
PRIMARY_IMPLEMENTATION_PATHS = {
    "CAP-CORE-CONFIG": "app/xianyu_system/core/config.py",
    "CAP-CORE-DATABASE": "app/xianyu_system/core/database.py",
    "CAP-HEALTH-MONITOR": "app/xianyu_system/api/health.py",
}
APPROVED_SHARED_PATHS = {
    "app/xianyu_system/application.py",
    "tests/unit/test_application_factory.py",
    "tests/unit/test_import_safety.py",
    "tests/contract/test_core_runtime.py",
    "tests/contract/test_distribution.py",
    "tests/contract/test_security_boundary.py",
    "changes/active/CHG-0002-core-application/tests/test_acceptance.py",
}
FORBIDDEN_PATH_PARTS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    "__pycache__",
    "data",
    "logs",
}
FORBIDDEN_SUFFIXES = {".db", ".sqlite", ".sqlite3", ".log", ".whl"}
GLOB_MARKERS = {"*", "?", "[", "]"}


def registry() -> dict[str, object]:
    data = read_yaml(REGISTRY_PATH)
    assert isinstance(data, dict)
    return data


def capabilities_by_id() -> dict[str, dict[str, object]]:
    return {str(item["id"]): item for item in registry()["capabilities"]}


def project_state_capabilities_by_id() -> dict[str, dict[str, object]]:
    state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
    return {str(item["id"]): item for item in state["capabilities"]["items"]}


def ensure_verified_candidate_commit_is_available() -> None:
    candidate_ref = f"{VERIFIED_CANDIDATE_SHA}^{{commit}}"
    exists = subprocess.run(["git", "cat-file", "-e", candidate_ref], cwd=ROOT)
    if exists.returncode != 0:
        subprocess.run(
            ["git", "fetch", "--no-tags", "--depth=1000", "origin", "feat/CHG-0002-core-application"],
            cwd=ROOT,
            check=True,
            text=True,
            capture_output=True,
        )
    subprocess.run(["git", "cat-file", "-e", candidate_ref], cwd=ROOT, check=True)

    direct_ancestor = subprocess.run(["git", "merge-base", "--is-ancestor", VERIFIED_CANDIDATE_SHA, "HEAD"], cwd=ROOT)
    if direct_ancestor.returncode == 0:
        return

    subprocess.run(
        ["git", "fetch", "--no-tags", "--depth=1000", "origin", "feat/CHG-0002-core-application"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    fetched_head = subprocess.run(
        ["git", "rev-parse", "FETCH_HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()
    subprocess.run(["git", "merge-base", "--is-ancestor", VERIFIED_CANDIDATE_SHA, fetched_head], cwd=ROOT, check=True)
    head_parents = subprocess.run(
        ["git", "show", "-s", "--format=%P", "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.split()
    assert fetched_head == subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip() or fetched_head in head_parents

def all_registered_paths(capability: dict[str, object]) -> list[str]:
    return [str(path) for path in capability["implementation_paths"] + capability["test_paths"]]


def assert_safe_registry_path(relative_path: str) -> None:
    assert relative_path
    assert not Path(relative_path).is_absolute()
    assert not PureWindowsPath(relative_path).is_absolute()
    assert not relative_path.startswith("./")
    assert "\\" not in relative_path
    assert ".." not in relative_path.split("/")
    assert ":" not in relative_path
    assert not any(marker in relative_path for marker in GLOB_MARKERS)
    path = Path(relative_path)
    assert FORBIDDEN_PATH_PARTS.isdisjoint(path.parts)
    assert path.suffix not in FORBIDDEN_SUFFIXES
    resolved = (ROOT / relative_path).resolve()
    assert resolved.is_relative_to(ROOT.resolve())
    assert resolved.is_file()


def test_capability_registry_schema_is_valid() -> None:
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(registry(), schema)


def test_core_capability_registry_paths_match_exact_t13_mapping() -> None:
    items = capabilities_by_id()
    for cap_id, expected in EXPECTED_CORE_CAPABILITY_PATHS.items():
        capability = items[cap_id]
        assert capability["implementation_paths"] == expected["implementation_paths"]
        assert capability["test_paths"] == expected["test_paths"]


def test_registered_paths_exist_are_files_and_are_safe_repository_relative_paths() -> None:
    for cap_id in CORE_CAPABILITIES:
        for relative_path in all_registered_paths(capabilities_by_id()[cap_id]):
            assert_safe_registry_path(relative_path)


def test_registry_path_responsibilities_are_separated() -> None:
    for cap_id in CORE_CAPABILITIES:
        capability = capabilities_by_id()[cap_id]
        for relative_path in capability["implementation_paths"]:
            assert not relative_path.startswith(("tests/", "changes/", "generated/"))
        for relative_path in capability["test_paths"]:
            assert relative_path.startswith((
                "tests/",
                "changes/active/CHG-0002-core-application/tests/",
            ))
            assert not relative_path.startswith("app/")


def test_capability_spec_documents_match_registry_paths_and_t14_status() -> None:
    items = capabilities_by_id()
    for cap_id in CORE_CAPABILITIES:
        spec_text = (ROOT / EXPECTED_SPECIFICATIONS[cap_id]).read_text(encoding="utf-8")
        for relative_path in all_registered_paths(items[cap_id]):
            assert f"`{relative_path}`" in spec_text
        assert "deferred to T13" not in spec_text
        assert "Registry implementation and test paths remain deferred to T13" not in spec_text
        assert "## T13 registry decision" in spec_text
        assert "## T14 verification decision" in spec_text
        assert VERIFIED_CANDIDATE_SHA in spec_text
        assert "registry status is now `verified`" in spec_text
        assert "verification remains deferred" not in spec_text.lower()
        assert "last_verified_commit" in spec_text


def test_core_capability_statuses_are_verified_with_candidate_commit() -> None:
    items = capabilities_by_id()
    assert re.fullmatch(r"[0-9a-f]{40}", VERIFIED_CANDIDATE_SHA)
    ensure_verified_candidate_commit_is_available()
    for cap_id in CORE_CAPABILITIES:
        capability = items[cap_id]
        assert capability["status"] == "verified"
        assert capability["active_change"] is None
        assert capability["last_verified_commit"] == VERIFIED_CANDIDATE_SHA


def test_other_capabilities_remain_planned_empty_and_unbound() -> None:
    items = capabilities_by_id()
    for cap_id, capability in items.items():
        if cap_id in CORE_CAPABILITIES:
            continue
        assert capability["status"] == "planned"
        assert capability["implementation_paths"] == []
        assert capability["test_paths"] == []
        assert capability["active_change"] is None
        assert capability["last_verified_commit"] is None
    assert items["CAP-XY-SCHEDULE"]["status"] == "planned"
    assert items["CAP-XY-SCHEDULE"]["implementation_paths"] == []
    assert items["CAP-XY-SCHEDULE"]["test_paths"] == []


def test_capability_id_set_and_stable_metadata_are_preserved() -> None:
    items = capabilities_by_id()
    assert set(items) == EXPECTED_CAPABILITY_IDS
    for cap_id in CORE_CAPABILITIES:
        assert items[cap_id]["owner_module"] == EXPECTED_OWNER_MODULES[cap_id]
        assert items[cap_id]["specification"] == EXPECTED_SPECIFICATIONS[cap_id]
        assert items[cap_id]["name"] in {
            "Core configuration",
            "Core database",
            "Health monitor",
        }


def test_project_state_matches_registry_paths_and_status_counts() -> None:
    registry_items = capabilities_by_id()
    state_items = project_state_capabilities_by_id()
    assert set(state_items) == set(registry_items)
    for cap_id in CORE_CAPABILITIES:
        assert state_items[cap_id]["implementation_paths"] == registry_items[cap_id]["implementation_paths"]
        assert state_items[cap_id]["test_paths"] == registry_items[cap_id]["test_paths"]
        assert state_items[cap_id]["status"] == "verified"
        assert state_items[cap_id]["active_change"] is None
        assert state_items[cap_id]["last_verified_commit"] == VERIFIED_CANDIDATE_SHA
    state = json.loads(PROJECT_STATE_PATH.read_text(encoding="utf-8"))
    assert state["capabilities"]["by_status"] == {"planned": 7, "verified": 3}


def test_path_lists_have_no_duplicates_and_shared_paths_are_approved() -> None:
    cross_capability_paths: list[str] = []
    for cap_id in CORE_CAPABILITIES:
        capability = capabilities_by_id()[cap_id]
        for key in ["implementation_paths", "test_paths"]:
            paths = [str(path) for path in capability[key]]
            assert len(paths) == len(set(paths))
            cross_capability_paths.extend(paths)
    duplicates = {path for path, count in Counter(cross_capability_paths).items() if count > 1}
    assert duplicates <= APPROVED_SHARED_PATHS


def test_primary_owner_implementation_paths_are_first_and_owner_modules_unchanged() -> None:
    items = capabilities_by_id()
    for cap_id, primary_path in PRIMARY_IMPLEMENTATION_PATHS.items():
        assert items[cap_id]["implementation_paths"][0] == primary_path
        assert items[cap_id]["owner_module"] == EXPECTED_OWNER_MODULES[cap_id]
