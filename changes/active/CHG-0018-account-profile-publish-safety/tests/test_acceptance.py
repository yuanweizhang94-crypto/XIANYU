from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE_ID = "CHG-0018-account-profile-publish-safety"
CHANGE_DIR = ROOT / "changes" / "active" / CHANGE_ID
SUSPENDED_CHG_0017 = ROOT / "changes" / "suspended" / "CHG-0017-upstream-native-auto-ai-delivery"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def project_state() -> dict[str, object]:
    return json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))


def test_chg0018_is_active_implementing_change() -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        text = read(CHANGE_DIR / name)
        assert f"Change ID: {CHANGE_ID}" in text
        assert "Status: IMPLEMENTING" in text

    state = project_state()
    assert state["active_change"] == {
        "id": CHANGE_ID,
        "status": "IMPLEMENTING",
        "path": f"changes/active/{CHANGE_ID}",
    }


def test_chg0017_is_suspended_not_archived_or_merged() -> None:
    assert SUSPENDED_CHG_0017.is_dir()
    tasks = read(SUSPENDED_CHG_0017 / "tasks.md")
    assert "Status: SUSPENDED" in tasks
    assert "suspended_from: IMPLEMENTING" in tasks
    assert "- [ ] T17 Archive and deliver." in tasks
    assert "T17 was not executed" in tasks

    state = project_state()
    suspended = state["suspended_changes"]
    assert isinstance(suspended, list)
    chg0017 = next(item for item in suspended if item["id"] == SUSPENDED_CHG_0017.name)
    assert chg0017["status"] == "SUSPENDED"
    assert chg0017["tasks"]["completed"] == 16
    assert chg0017["tasks"]["total"] == 17
    assert chg0017["tasks"]["next_task"] is None


def test_scope_forbids_parallel_or_production_runtime() -> None:
    proposal = read(CHANGE_DIR / "proposal.md")
    acceptance = read(CHANGE_DIR / "acceptance.md")
    for forbidden in [
        "No database tables",
        "Browser Broker",
        "real account operation",
        "message sending",
        "PR #26 state change",
    ]:
        assert forbidden in proposal or forbidden in acceptance


def test_required_rollback_boundaries_are_recorded() -> None:
    proposal = read(CHANGE_DIR / "proposal.md")
    assert "P0 safety" in proposal
    assert "P1-P4 Profile readiness" in proposal
    assert "tests/vendor patch/evidence" in proposal
