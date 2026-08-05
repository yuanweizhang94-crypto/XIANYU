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


def test_chg0018_is_active_verifying_change() -> None:
    for name in ["proposal.md", "design.md", "tasks.md", "acceptance.md"]:
        text = read(CHANGE_DIR / name)
        assert f"Change ID: {CHANGE_ID}" in text
        assert "Status: VERIFYING" in text

    state = project_state()
    assert state["active_change"] == {
        "id": CHANGE_ID,
        "status": "VERIFYING",
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


def test_p0_credential_safety_result_is_recorded() -> None:
    tasks = read(CHANGE_DIR / "tasks.md")
    acceptance = read(CHANGE_DIR / "acceptance.md")
    patch = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "4c5e1ac-chg0018-account-profile-publish-safety.patch"

    assert "- [x] T1 Implement P0 credential safety and false-disable prevention." in tasks
    assert "- [x] T2 Run P0 targeted tests and commit the P0 boundary." in tasks
    assert "Raw `login_password` is removed" in acceptance
    assert "8FA58C8F2674EE7A16C36689F962612DC1619C211ACAA390105778A64CD20EEE" in acceptance
    assert patch.is_file()


def test_profile_publish_readiness_result_is_recorded() -> None:
    tasks = read(CHANGE_DIR / "tasks.md")
    acceptance = read(CHANGE_DIR / "acceptance.md")

    for task in [
        "T3 Implement P1 persistent Profile publish readiness.",
        "T4 Implement P2 Profile initialization and repair boundaries.",
        "T5 Implement P3 shared read-only publish preflight.",
        "T6 Implement P4 canonical browser lock usage for publish readiness paths.",
        "T7 Run P1-P4 targeted tests and commit the Profile readiness boundary.",
    ]:
        assert f"- [x] {task}" in tasks
    assert "preflight_publish_form()" in acceptance
    assert "`profile_missing` and `browser_busy`" in acceptance
    assert "one global slot and one account lock" in acceptance


def test_final_validation_evidence_is_recorded() -> None:
    tasks = read(CHANGE_DIR / "tasks.md")
    acceptance = read(CHANGE_DIR / "acceptance.md")
    evidence = CHANGE_DIR / "evidence" / "20260805-final-validation.md"

    assert "- [x] T8 Generate CHG-0018 patch artifact, evidence, and full validation." in tasks
    assert "Combined upstream targeted and regression tests: 68 passed." in acceptance
    assert "Frontend build: passed with `npm run build`." in acceptance
    assert "non-blocking upstream tooling gap" in acceptance
    assert evidence.is_file()
    evidence_text = read(evidence)
    assert "CHG-0018 Final Validation Evidence" in evidence_text
    assert "Production operations executed: none" in evidence_text
    assert "PR #26 state changed: no" in evidence_text
    assert "Remote branch: `origin/feat/CHG-0018-account-profile-publish-safety`" in evidence_text
    assert "`quality`: success" in evidence_text
    assert "`tests`: success" in evidence_text
    assert "`security`: success" in evidence_text
