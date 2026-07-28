from __future__ import annotations

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[4]
CHANGE_ID = "CHG-0007-xianyu-schedule-boundary"
CHANGE_DIR = ROOT / "changes" / "active" / CHANGE_ID


def test_draft_governance_state_is_read_only() -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        text = (CHANGE_DIR / name).read_text(encoding="utf-8")
        assert f"Change ID: {CHANGE_ID}" in text
        assert "Status: APPROVED" in text


def test_draft_has_exactly_nine_unfinished_tasks() -> None:
    tasks = (CHANGE_DIR / "tasks.md").read_text(encoding="utf-8").splitlines()
    task_lines = [line for line in tasks if line.startswith("- [ ] T") or line.startswith("- [x] T")]
    assert len(task_lines) == 9
    assert all(line.startswith("- [x]") for line in task_lines[:5])
    assert all(line.startswith("- [ ]") for line in task_lines[5:])


def test_draft_keeps_schedule_capability_planned_and_unbound() -> None:
    registry = yaml.safe_load((ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8"))
    cap = next(item for item in registry["capabilities"] if item["id"] == "CAP-XY-SCHEDULE")
    assert cap["status"] == "planned"
    assert cap["implementation_paths"] == []
    assert cap["test_paths"] == []
    assert cap["active_change"] is None
    assert cap["last_verified_commit"] is None


def test_draft_project_state_and_runtime_absence() -> None:
    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"]["id"] == CHANGE_ID
    assert state["active_change"]["status"] == "APPROVED"
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 5
    assert state["tasks"]["next_task"] == "T6 Implement the approved local deterministic scheduling boundary."
    assert state["capabilities"]["by_status"] == {"planned": 3, "verified": 7}
    assert not (ROOT / "app" / "xianyu_system" / "schedule").exists()
    assert not (ROOT / "migrations" / "versions" / "0006_xianyu_schedule_boundary.py").exists()
