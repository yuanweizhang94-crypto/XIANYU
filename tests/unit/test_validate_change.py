from __future__ import annotations

import shutil
from pathlib import Path

from scripts.validate_change import validate_change

ROOT = Path(__file__).resolve().parents[2]


def copy_change_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "changes", root / "changes")
    return root


def test_validate_change_passes_for_current_repo() -> None:
    assert validate_change(ROOT) == []


def test_active_change_more_than_one_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    extra = root / "changes" / "active" / "CHG-9999-extra"
    extra.mkdir(parents=True)
    assert any("exactly one active change" in error for error in validate_change(root))


def test_missing_required_change_file_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    target = root / "changes" / "active" / "CHG-0001-project-baseline" / "design.md"
    target.unlink()
    assert any("missing change files" in error for error in validate_change(root))
