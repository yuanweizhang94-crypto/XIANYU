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
    active_root = root / "changes" / "active"
    if active_root.exists():
        shutil.rmtree(active_root)
    active_root.mkdir(parents=True, exist_ok=True)
    suspended_root = root / "changes" / "suspended"
    if suspended_root.exists():
        shutil.rmtree(suspended_root)
    suspended_root.mkdir(parents=True, exist_ok=True)
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


def seed_suspended_change(
    root: Path,
    change_id: str = "CHG-0003-suspended-test",
) -> Path:
    source = root / "changes" / "archive" / "CHG-0006-xianyu-publish-boundary"
    target = root / "changes" / "suspended" / change_id
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    set_change_identity(target, change_id, "SUSPENDED")
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        path = target / name
        text = path.read_text(encoding="utf-8").rstrip()
        text += (
            "\nsuspended_from: IMPLEMENTING"
            "\nsuspended_at: 2026-08-05T00:00:00Z"
            "\nsuspended_reason: test suspension"
            "\nresume_condition: owner approval"
            "\n"
        )
        path.write_text(text, encoding="utf-8")
    return target


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
    assert isinstance(state["suspended_changes"], list)


def test_chg_0002_test_change_is_discovered_without_source_changes(tmp_path: Path) -> None:
    root = copy_state_tree(tmp_path)
    seed_single_active_change(root)

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


def test_suspended_changes_are_listed_without_becoming_active(tmp_path: Path) -> None:
    root = copy_state_tree(tmp_path)
    suspended = seed_suspended_change(root)

    state = build_project_state(root)
    assert state["active_change"] is None
    assert state["tasks"]["total"] == 0
    assert state["suspended_changes"] == [
        {
            "id": suspended.name,
            "status": "SUSPENDED",
            "path": f"changes/suspended/{suspended.name}",
            "suspended_from": "IMPLEMENTING",
            "suspended_at": "2026-08-05T00:00:00Z",
            "suspended_reason": "test suspension",
            "resume_condition": "owner approval",
            "tasks": {
                "total": len(parse_tasks(suspended / "tasks.md")),
                "completed": sum(1 for task in parse_tasks(suspended / "tasks.md") if task.completed),
                "next_task": None,
                "items": [
                    {"text": task.text, "completed": task.completed}
                    for task in parse_tasks(suspended / "tasks.md")
                ],
            },
        }
    ]


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
