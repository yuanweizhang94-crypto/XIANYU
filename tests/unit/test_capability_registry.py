from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import jsonschema
import pytest

from scripts.repo_utils import read_yaml
from scripts.verify_repository import VerificationError, check_capability_registry

ROOT = Path(__file__).resolve().parents[2]


def test_capability_registry_schema_and_statuses() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    schema = json.loads((ROOT / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(registry, schema)
    capabilities = registry["capabilities"]
    assert len(capabilities) == 10
    assert {item["status"] for item in capabilities} == {"planned"}
    assert {item["active_change"] for item in capabilities} == {None}
    assert {item["last_verified_commit"] for item in capabilities} == {None}


def test_capability_ids_are_expected() -> None:
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


def test_unapproved_capability_status_name_fails_schema() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    schema = json.loads((ROOT / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8"))
    invalid = deepcopy(registry)
    invalid["capabilities"][0]["status"] = "active"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid, schema)


def test_planned_capability_bound_to_active_change_fails(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    (root / "specs").mkdir(parents=True)
    (root / "contracts" / "schemas").mkdir(parents=True)
    (root / "specs" / "capabilities").mkdir(parents=True)
    registry_text = (ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8")
    (root / "specs" / "CAPABILITY_REGISTRY.yaml").write_text(registry_text, encoding="utf-8")
    schema_text = (ROOT / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8")
    (root / "contracts" / "schemas" / "capability-registry.schema.json").write_text(schema_text, encoding="utf-8")
    for spec in (ROOT / "specs" / "capabilities").glob("*.md"):
        (root / "specs" / "capabilities" / spec.name).write_text(spec.read_text(encoding="utf-8"), encoding="utf-8")

    registry = read_yaml(root / "specs" / "CAPABILITY_REGISTRY.yaml")
    registry["capabilities"][0]["active_change"] = "CHG-0002-test-change"
    import yaml

    (root / "specs" / "CAPABILITY_REGISTRY.yaml").write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )

    with pytest.raises(VerificationError, match="planned capability must not bind active_change"):
        check_capability_registry(root)
