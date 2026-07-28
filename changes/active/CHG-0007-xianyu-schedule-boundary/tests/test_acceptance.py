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


def test_approved_change_has_t7_complete_and_t8_next() -> None:
    tasks = (CHANGE_DIR / "tasks.md").read_text(encoding="utf-8").splitlines()
    task_lines = [line for line in tasks if line.startswith("- [ ] T") or line.startswith("- [x] T")]
    assert len(task_lines) == 9
    assert all(line.startswith("- [x]") for line in task_lines[:7])
    assert all(line.startswith("- [ ]") for line in task_lines[7:])


def test_t8_phase_a_binds_schedule_capability_candidate() -> None:
    registry = yaml.safe_load((ROOT / "specs" / "CAPABILITY_REGISTRY.yaml").read_text(encoding="utf-8"))
    cap = next(item for item in registry["capabilities"] if item["id"] == "CAP-XY-SCHEDULE")
    assert cap["status"] == "implementing"
    assert cap["implementation_paths"]
    assert cap["test_paths"]
    assert cap["active_change"] == CHANGE_ID
    assert cap["last_verified_commit"] is None


def test_draft_project_state_and_runtime_absence() -> None:
    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"]["id"] == CHANGE_ID
    assert state["active_change"]["status"] == "APPROVED"
    assert state["tasks"]["total"] == 9
    assert state["tasks"]["completed"] == 7
    assert state["tasks"]["next_task"] == "T8 Bind capability evidence and complete two-phase verification"
    assert state["capabilities"]["by_status"] == {"planned": 2, "implementing": 1, "verified": 7}
    assert (ROOT / "app" / "xianyu_system" / "schedule").is_dir()
    assert (ROOT / "migrations" / "versions" / "0006_xianyu_schedule_boundary.py").is_file()


def test_t7_permanent_schedule_evidence_exists() -> None:
    expected_paths = [
        "tests/unit/test_schedule_domain.py",
        "tests/unit/test_schedule_fingerprint.py",
        "tests/unit/test_schedule_validation.py",
        "tests/unit/test_schedule_service.py",
        "tests/unit/test_schedule_apscheduler_adapter.py",
        "tests/unit/test_import_safety.py",
        "tests/contract/test_schedule_persistence.py",
        "tests/contract/test_schedule_security.py",
        "tests/contract/test_migrations.py",
    ]
    for relative in expected_paths:
        assert (ROOT / relative).is_file()


def test_t7_scope_still_excludes_real_platform_access() -> None:
    runtime = "\n".join(
        path.read_text(encoding="utf-8").lower()
        for path in (ROOT / "app" / "xianyu_system" / "schedule").glob("*.py")
    )
    for forbidden in ["playwright", "browser profile", "wecom", "openai", "redis", "celery"]:
        assert forbidden not in runtime
