from __future__ import annotations

import re
import shutil
import subprocess
from pathlib import Path

from scripts.repo_utils import VALID_CHANGE_STATUSES
from scripts.repo_utils import discover_active_change
from scripts.validate_change import validate_change

ROOT = Path(__file__).resolve().parents[2]


def copy_change_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "changes", root / "changes", ignore=shutil.ignore_patterns("__pycache__"))
    active_root = root / "changes" / "active"
    if active_root.exists():
        shutil.rmtree(active_root)
    active_root.mkdir(parents=True, exist_ok=True)
    return root


def active_change_dir(root: Path) -> Path:
    active = discover_active_change(root)
    assert active is not None
    return active


def seed_single_active_change(
    root: Path,
    change_id: str = "CHG-9999-validate-test",
    status: str = "APPROVED",
) -> Path:
    source = root / "changes" / "archive" / "CHG-0006-xianyu-publish-boundary"
    target = root / "changes" / "active" / change_id
    shutil.copytree(source, target)
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = target / name
        text = path.read_text(encoding="utf-8").replace(
            "CHG-0006-xianyu-publish-boundary", change_id
        )
        text = re.sub(r"^Status: .+$", f"Status: {status}", text, flags=re.MULTILINE)
        path.write_text(text, encoding="utf-8")
    return target


def replace_status(change_dir: Path, status: str) -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = change_dir / name
        text = path.read_text(encoding="utf-8")
        text = re.sub(r"^Status: .+$", f"Status: {status}", text, flags=re.MULTILINE)
        path.write_text(text, encoding="utf-8")


def test_validate_change_passes_for_current_repo() -> None:
    assert validate_change(ROOT) == []


def test_zero_active_change_is_allowed(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    assert discover_active_change(root) is None
    assert validate_change(root) == []


def test_single_active_change_is_allowed(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    active = seed_single_active_change(root)
    assert discover_active_change(root) == active
    assert validate_change(root) == []


def test_active_change_more_than_one_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    active = seed_single_active_change(root)
    extra = root / "changes" / "active" / "CHG-9999-extra"
    shutil.copytree(active, extra)
    assert any("expected at most one active change" in error for error in validate_change(root))


def test_missing_required_change_file_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    target = seed_single_active_change(root) / "design.md"
    target.unlink()
    assert any("missing change files" in error for error in validate_change(root))


def test_unified_change_status_machine_rejects_old_status(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    change_dir = seed_single_active_change(root)
    replace_status(change_dir, "IN_PROGRESS")
    errors = validate_change(root)
    assert any("invalid change status" in error for error in errors)


def test_merged_or_archived_change_cannot_remain_active(tmp_path: Path) -> None:
    for terminal_status in ["MERGED", "ARCHIVED"]:
        root = copy_change_tree(tmp_path / terminal_status)
        change_dir = seed_single_active_change(root)
        replace_status(change_dir, terminal_status)
        errors = validate_change(root)
        assert any("must not remain in changes/active" in error for error in errors)


def test_all_change_statuses_are_from_unified_machine() -> None:
    for path in (ROOT / "changes" / "active").glob("*/proposal.md"):
        status_line = next(line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("Status:"))
        assert status_line.split(":", 1)[1].strip() in VALID_CHANGE_STATUSES


def test_branch_change_id_mismatch_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    seed_single_active_change(root)
    subprocess.run(["git", "init"], cwd=root, check=True, text=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "feat/CHG-9999-other"], cwd=root, check=True, text=True, capture_output=True)
    errors = validate_change(root)
    assert any("branch change id mismatch" in error for error in errors)


def test_archived_change_is_legal_in_archive(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    active = seed_single_active_change(root)
    archive = root / "changes" / "archive" / active.name
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(active, archive)
    replace_status(archive, "ARCHIVED")
    shutil.rmtree(active)

    assert validate_change(root) == []


def test_non_archived_change_in_archive_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    active = seed_single_active_change(root)
    archive = root / "changes" / "archive" / active.name
    archive.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(active, archive)
    shutil.rmtree(active)

    errors = validate_change(root)
    assert any("archived change must have ARCHIVED status" in error for error in errors)
