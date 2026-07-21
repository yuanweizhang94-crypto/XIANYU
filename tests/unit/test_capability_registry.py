from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from scripts.repo_utils import read_yaml

ROOT = Path(__file__).resolve().parents[2]


def test_capability_registry_schema_and_statuses() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    schema = json.loads((ROOT / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(registry, schema)
    capabilities = registry["capabilities"]
    assert len(capabilities) == 10
    assert {item["status"] for item in capabilities} == {"planned"}


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
