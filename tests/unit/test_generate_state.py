from __future__ import annotations

import re
import shutil
from pathlib import Path

from scripts.generate_state import build_project_state, project_state_json, write_project_state
from scripts.repo_utils import (
    discover_active_change,
    extract_change_status,
    load_capabilities,
    next_uncompleted_task,
    parse_tasks,
)

ROOT = Path(__file__).resolve().parents[2]


def copy_state_tree(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    for name in ["changes", "specs", "contracts"]:
        shutil.copytree(ROOT / name, root / name, ignore=shutil.ignore_patterns("__pycache__"))
    (root / "VERSION").write_text((ROOT / "VERSION").read_text(encoding="utf-8"), encoding="utf-8")
    return root


def active_change_dir(root: Path) -> Path:
    active = discover_active_change(root)
    assert active is not None
    return active


def seed_single_active_change(
    root: Path,
    change_id: str = "CHG-0002-test-change",
    status: str = "APPROVED",
) -> Path:
    source = root / "changes" / "archive" / "CHG-0006-xianyu-publish-boundary"
    target = root / "changes" / "active" / change_id
    shutil.copytree(source, target)
    set_change_identity(target, change_id, status)
    return target


def set_change_identity(change_dir: Path, change_id: str, status: str) -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = change_dir / name
        text = path.read_text(encoding="utf-8")
        text = text.replace(change_dir.name, change_id)
        text = re.sub(r"^Status: .+$", f"Status: {status}", text, flags=re.MULTILINE)
        path.write_text(text, encoding="utf-8")


def test_generate_state_reflects_current_repository_sources() -> None:
    state = build_project_state(ROOT)
    assert state["project"] == "XIANYU"
    assert state["version"]
    active = discover_active_change(ROOT)
    if active is None:
        assert state["active_change"] is None
        assert state["tasks"] == {
            "total": 0,
            "completed": 0,
            "next_task": None,
            "items": [],
        }
    else:
        assert state["active_change"] == {
            "id": active.name,
            "status": extract_change_status(active),
            "path": active.relative_to(ROOT).as_posix(),
        }
    assert state["capabilities"]["total"] == len(load_capabilities(ROOT))


def test_chg_0002_test_change_is_discovered_without_source_changes(tmp_path: Path) -> None:
    root = copy_state_tree(tmp_path)
    new = seed_single_active_change(root)

    state = build_project_state(root)
    assert state["active_change"]["id"] == "CHG-0002-test-change"
    assert state["active_change"]["path"] == "changes/active/CHG-0002-test-change"
    assert state["tasks"]["total"] > 0


def test_zero_active_change_generates_null_state(tmp_path: Path) -> None:
    root = copy_state_tree(tmp_path)

    state = build_project_state(root)
    assert state["active_change"] is None
    assert state["tasks"]["total"] == 0
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["next_task"] is None
    assert state["tasks"]["items"] == []


def test_draft_change_is_not_executable(tmp_path: Path) -> None:
    root = copy_state_tree(tmp_path)
    change_dir = seed_single_active_change(root, status="DRAFT")
    tasks_path = change_dir / "tasks.md"
    tasks_path.write_text(
        tasks_path.read_text(encoding="utf-8") + "\n- [ ] T99 Draft-only task\n", encoding="utf-8"
    )

    state = build_project_state(root)
    assert state["active_change"]["status"] == "DRAFT"
    assert state["tasks"]["next_task"] is None


def test_tasks_can_identify_next_uncompleted_task(tmp_path: Path) -> None:
    tasks_path = tmp_path / "tasks.md"
    tasks_path.write_text("- [x] T1 done\n- [ ] T2 next\n", encoding="utf-8")
    tasks = parse_tasks(tasks_path)
    assert next_uncompleted_task(tasks) == "T2 next"


def test_project_state_generation_is_deterministic(tmp_path: Path) -> None:
    root = copy_state_tree(tmp_path)
    first = project_state_json(root)
    second = project_state_json(root)
    assert first == second


def test_write_project_state_twice_is_identical(tmp_path: Path) -> None:
    root = copy_state_tree(tmp_path)
    first_path = write_project_state(root)
    first = first_path.read_text(encoding="utf-8")
    second_path = write_project_state(root)
    second = second_path.read_text(encoding="utf-8")
    assert first == second
