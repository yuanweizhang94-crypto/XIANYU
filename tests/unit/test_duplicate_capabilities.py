from __future__ import annotations

import shutil
from pathlib import Path

import yaml

from scripts.detect_duplicate_capabilities import detect_duplicate_capabilities

ROOT = Path(__file__).resolve().parents[2]


def copy_registry_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "specs", root / "specs")
    (root / "app").mkdir()
    (root / "worker").mkdir()
    (root / "adapters").mkdir()
    return root


def test_duplicate_capability_id_fails(tmp_path: Path) -> None:
    root = copy_registry_tree(tmp_path)
    registry_path = root / "specs" / "CAPABILITY_REGISTRY.yaml"
    registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    registry["capabilities"][1]["id"] = registry["capabilities"][0]["id"]
    registry_path.write_text(yaml.safe_dump(registry, allow_unicode=True), encoding="utf-8")
    assert any("duplicate capability id" in error for error in detect_duplicate_capabilities(root))


def test_account_specific_filename_fails(tmp_path: Path) -> None:
    root = copy_registry_tree(tmp_path)
    bad_file = root / "worker" / "publisher_account_1.py"
    bad_file.write_text("# forbidden\n", encoding="utf-8")
    assert any("account-specific" in error for error in detect_duplicate_capabilities(root))


def test_current_registry_has_no_duplicates() -> None:
    assert detect_duplicate_capabilities(ROOT) == []
