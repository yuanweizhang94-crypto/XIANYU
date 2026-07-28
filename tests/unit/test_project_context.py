from __future__ import annotations

import shutil
from pathlib import Path
import re

import pytest

from scripts.project_context import render_context
from scripts.repo_utils import discover_active_change
from scripts.verify_repository import VerificationError, validate_project_state

ROOT = Path(__file__).resolve().parents[2]


def copy_repo_slice(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for name in ["changes", "specs", "contracts", "generated"]:
        shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns("__pycache__"))
    (root / "VERSION").write_text((ROOT / "VERSION").read_text(encoding="utf-8"), encoding="utf-8")
    active_root = root / "changes" / "active"
    if active_root.exists():
        shutil.rmtree(active_root)
    active_root.mkdir(parents=True, exist_ok=True)
    return root


def seed_single_active_change(root: Path, status: str = "APPROVED") -> Path:
    source = root / "changes" / "archive" / "CHG-0006-xianyu-publish-boundary"
    target = root / "changes" / "active" / "CHG-9999-context-test"
    shutil.copytree(source, target)
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = target / name
        text = path.read_text(encoding="utf-8").replace(
            "CHG-0006-xianyu-publish-boundary", target.name
        )
        text = re.sub(r"^Status: .+$", f"Status: {status}", text, flags=re.MULTILINE)
        path.write_text(text, encoding="utf-8")
    return target


def test_project_state_staleness_fails_validation(tmp_path: Path) -> None:
    root = copy_repo_slice(tmp_path)
    (root / "generated" / "PROJECT_STATE.json").write_text('{"project":"STALE"}\n', encoding="utf-8")

    with pytest.raises(VerificationError, match="PROJECT_STATE.json is stale"):
        validate_project_state(root)


def test_project_context_source_has_no_chg_0001_hardcoded_dependency() -> None:
    source = (ROOT / "scripts" / "project_context.py").read_text(encoding="utf-8")
    assert "CHG-0001-project-baseline" not in source
    assert "ADR-0001" not in source
    assert "ADR-0008" not in source


def test_project_context_reports_no_executable_change_when_none(tmp_path: Path) -> None:
    root = copy_repo_slice(tmp_path)
    active = discover_active_change(root)
    assert active is None
    # Give project_context enough git metadata for its runtime git output.
    import subprocess

    subprocess.run(["git", "init"], cwd=root, check=True, text=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", "feat/no-active-change"], cwd=root, check=True, text=True, capture_output=True)

    context = render_context(root)
    assert "active_change: null" in context
    assert "next_task: null" in context
    assert "no approved executable change" in context


def test_project_context_reports_single_executable_active_change(tmp_path: Path) -> None:
    root = copy_repo_slice(tmp_path)
    active = seed_single_active_change(root)
    import subprocess

    subprocess.run(["git", "init"], cwd=root, check=True, text=True, capture_output=True)
    subprocess.run(["git", "checkout", "-b", f"feat/{active.name}"], cwd=root, check=True, text=True, capture_output=True)

    context = render_context(root)
    assert f"active_change: {active.name}" in context
    assert "Active change status: APPROVED" in context
    assert "next_task:" in context
    assert "no approved executable change" not in context
