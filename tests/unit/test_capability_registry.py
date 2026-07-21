from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path

import jsonschema
import pytest

from scripts.repo_utils import read_yaml
from scripts.verify_repository import VerificationError, check_capability_registry

ROOT = Path(__file__).resolve().parents[2]
ALLOWED_CAPABILITY_STATUSES = {"planned", "implementing", "verified", "deprecated"}


def test_capability_registry_schema_and_generic_statuses() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    schema = json.loads((ROOT / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(registry, schema)
    capabilities = registry["capabilities"]
    assert capabilities
    assert {item["status"] for item in capabilities} <= ALLOWED_CAPABILITY_STATUSES


def test_unapproved_capability_status_name_fails_schema() -> None:
    registry = read_yaml(ROOT / "specs" / "CAPABILITY_REGISTRY.yaml")
    schema = json.loads((ROOT / "contracts" / "schemas" / "capability-registry.schema.json").read_text(encoding="utf-8"))
    invalid = deepcopy(registry)
    invalid["capabilities"][0]["status"] = "active"
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.validate(invalid, schema)


def test_planned_capability_bound_to_active_change_fails(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "specs", root / "specs", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "contracts" / "schemas", root / "contracts" / "schemas")
    (root / "app").mkdir(parents=True)
    (root / "worker").mkdir(parents=True)
    (root / "adapters").mkdir(parents=True)

    registry = read_yaml(root / "specs" / "CAPABILITY_REGISTRY.yaml")
    registry["capabilities"][0]["active_change"] = "CHG-0002-test-change"
    import yaml

    (root / "specs" / "CAPABILITY_REGISTRY.yaml").write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )

    with pytest.raises(VerificationError, match="planned capability must not bind active_change"):
        check_capability_registry(root)


def test_generic_capability_registry_allows_more_than_ten_capabilities(tmp_path: Path) -> None:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "specs", root / "specs", ignore=shutil.ignore_patterns("__pycache__"))
    shutil.copytree(ROOT / "contracts" / "schemas", root / "contracts" / "schemas")
    (root / "app").mkdir(parents=True)
    (root / "worker").mkdir(parents=True)
    (root / "adapters").mkdir(parents=True)

    registry = read_yaml(root / "specs" / "CAPABILITY_REGISTRY.yaml")
    registry["capabilities"].append(
        {
            "id": "CAP-EXTRA-GOVERNANCE",
            "name": "Extra governance capability",
            "status": "planned",
            "owner_module": "app.extra_governance",
            "specification": "specs/capabilities/CAP-EXTRA-GOVERNANCE.md",
            "implementation_paths": [],
            "test_paths": [],
            "active_change": None,
            "last_verified_commit": None,
        }
    )
    import yaml

    (root / "specs" / "CAPABILITY_REGISTRY.yaml").write_text(
        yaml.safe_dump(registry, allow_unicode=True, sort_keys=False), encoding="utf-8"
    )
    (root / "specs" / "capabilities" / "CAP-EXTRA-GOVERNANCE.md").write_text(
        "# CAP-EXTRA-GOVERNANCE\n", encoding="utf-8"
    )

    check_capability_registry(root)
