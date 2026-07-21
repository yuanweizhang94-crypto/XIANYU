from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

from scripts.repo_utils import VALID_CHANGE_STATUSES
from scripts.validate_change import validate_change

ROOT = Path(__file__).resolve().parents[2]


def copy_change_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    shutil.copytree(ROOT / "changes", root / "changes", ignore=shutil.ignore_patterns("__pycache__"))
    return root


def replace_status(change_dir: Path, status: str) -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = change_dir / name
        text = path.read_text(encoding="utf-8")
        text = text.replace("Status: VERIFYING", f"Status: {status}")
        text = text.replace("Status: APPROVED", f"Status: {status}")
        path.write_text(text, encoding="utf-8")


def test_validate_change_passes_for_current_repo() -> None:
    assert validate_change(ROOT) == []


def test_zero_active_change_is_allowed(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    shutil.rmtree(root / "changes" / "active" / "CHG-0001-project-baseline")
    assert validate_change(root) == []


def test_active_change_more_than_one_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    extra = root / "changes" / "active" / "CHG-9999-extra"
    shutil.copytree(root / "changes" / "active" / "CHG-0001-project-baseline", extra)
    assert any("expected at most one active change" in error for error in validate_change(root))


def test_missing_required_change_file_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    target = root / "changes" / "active" / "CHG-0001-project-baseline" / "design.md"
    target.unlink()
    assert any("missing change files" in error for error in validate_change(root))


def test_unified_change_status_machine_rejects_old_status(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    change_dir = root / "changes" / "active" / "CHG-0001-project-baseline"
    replace_status(change_dir, "IN_PROGRESS")
    errors = validate_change(root)
    assert any("invalid change status" in error for error in errors)


def test_merged_or_archived_change_cannot_remain_active(tmp_path: Path) -> None:
    for terminal_status in ["MERGED", "ARCHIVED"]:
        root = copy_change_tree(tmp_path / terminal_status)
        change_dir = root / "changes" / "active" / "CHG-0001-project-baseline"
        replace_status(change_dir, terminal_status)
        errors = validate_change(root)
        assert any("must not remain in changes/active" in error for error in errors)


def test_all_change_statuses_are_from_unified_machine() -> None:
    for path in (ROOT / "changes" / "active").glob("*/proposal.md"):
        status_line = next(line for line in path.read_text(encoding="utf-8").splitlines() if line.startswith("Status:"))
        assert status_line.split(":", 1)[1].strip() in VALID_CHANGE_STATUSES


def test_branch_change_id_mismatch_fails(tmp_path: Path) -> None:
    root = copy_change_tree(tmp_path)
    subprocess.run(["git", "init"], cwd=root, check=True, text=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "feat/CHG-9999-other"], cwd=root, check=True, text=True, capture_output=True)
    errors = validate_change(root)
    assert any("branch change id mismatch" in error for error in errors)


def test_chg_0001_status_is_verifying() -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = ROOT / "changes" / "active" / "CHG-0001-project-baseline" / name
        assert "Status: VERIFYING" in path.read_text(encoding="utf-8")
