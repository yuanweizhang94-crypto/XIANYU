from __future__ import annotations

from pathlib import Path

from scripts.generate_state import build_project_state
from scripts.repo_utils import next_uncompleted_task, parse_tasks

ROOT = Path(__file__).resolve().parents[2]


def test_generate_state_contains_expected_baseline() -> None:
    state = build_project_state(ROOT)
    assert state["project"] == "XIANYU"
    assert state["version"]
    assert state["active_change"]["id"] == "CHG-0001-project-baseline"
    assert state["capabilities"]["total"] == 10


def test_tasks_can_identify_next_uncompleted_task(tmp_path: Path) -> None:
    tasks_path = tmp_path / "tasks.md"
    tasks_path.write_text("- [x] T1 done\n- [ ] T2 next\n", encoding="utf-8")
    tasks = parse_tasks(tasks_path)
    assert next_uncompleted_task(tasks) == "T2 next"
