from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE_ID = "CHG-0018-account-profile-publish-safety"
CHANGE_DIR = ROOT / "changes" / "active" / CHANGE_ID
ARCHIVED_CHG_0017 = ROOT / "changes" / "archive" / "CHG-0017-upstream-native-auto-ai-delivery"
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


def test_chg0017_is_archived_after_predecessor_merge() -> None:
    assert ARCHIVED_CHG_0017.is_dir()
    assert not SUSPENDED_CHG_0017.exists()
    tasks = read(ARCHIVED_CHG_0017 / "tasks.md")
    assert "Status: ARCHIVED" in tasks
    assert "- [x] T17 Archive and deliver." in tasks
    assert "Completed tasks: 17 / 17" in tasks


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
    assert "F15F2161213EE7CD8B952D3DD475DEA18BA12F56570E332CE4711BD87D6350E2" in acceptance
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
    assert "- [x] T9 Complete CANARY-A01 UI/Profile/preflight runtime verification and native auto-polish canary hardening." in tasks
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


def test_t11_t12_final_batch_publish_recovery_delivery_is_recorded() -> None:
    tasks = read(CHANGE_DIR / "tasks.md")
    t11_evidence = CHANGE_DIR / "evidence" / "20260809-t11-controlled-real-batch-publish-recovery.md"
    t12_evidence = CHANGE_DIR / "evidence" / "20260809-t12-final-validation-and-ci.md"
    supplement = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "4c5e1ac-chg0018-t11-controlled-batch-publish-recovery.patch"
    formal_patch = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "4c5e1ac-chg0018-account-profile-publish-safety.patch"
    attributes = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / ".gitattributes"
    readme = read(ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "README.md")

    assert "- [x] T11 Fix real batch publish Profile runtime, readiness classification, and duplicate-safe retry path." in tasks
    assert "- [x] T12 Return CHG-0018 to VERIFYING after real batch publish recovery evidence, repository validation, and CI." in tasks
    assert t11_evidence.is_file()
    t11_text = read(t11_evidence)
    assert "AUTHORIZED_FAILED_RECORDS=4" in t11_text
    assert "FAILED_RECORDS_RECOVERED=4" in t11_text
    assert "NOT_PUBLISHED_CONFIRMED=0" in t11_text
    assert "ALREADY_PUBLISHED_SKIPPED=4" in t11_text
    assert "REAL_PUBLISH_ATTEMPTS=0" in t11_text
    assert "SECOND_EXECUTOR_RUNNING=false" in t11_text
    assert "CHG0018_T11_COMPLETE=true" in t11_text
    assert "T12 remains explicitly incomplete" in t11_text

    assert t12_evidence.is_file()
    t12_text = read(t12_evidence)
    assert "ALREADY_PUBLISHED_SKIPPED=4" in t12_text
    assert "NOT_PUBLISHED_CONFIRMED=0" in t12_text
    assert "REAL_PUBLISH_ATTEMPTS=0" in t12_text
    assert "must not be described as four new real publish successes" in t12_text
    assert "B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111" in t12_text

    assert supplement.is_file()
    assert formal_patch.is_file()
    assert attributes.is_file()
    assert "4c5e1ac-chg0018-account-profile-publish-safety.patch binary" in read(attributes)
    assert "99FDB0B8688AE0D45D1B2725D1DC7AFE1C883424F5B3C245F532DA8FC3535882" in readme
    assert "B379A7286D10EF1988361940AB9DB6C84AF0D0BB50D13F6910B52011BB0BD111" in readme


def test_runtime_profile_preflight_auto_polish_evidence_is_recorded() -> None:
    tasks = read(CHANGE_DIR / "tasks.md")
    acceptance = read(CHANGE_DIR / "acceptance.md")
    evidence = CHANGE_DIR / "evidence" / "20260805-runtime-profile-preflight-auto-polish.md"

    assert "- [x] T9 Complete CANARY-A01 UI/Profile/preflight runtime verification and native auto-polish canary hardening." in tasks
    assert "- [x] T10 Return CHG-0018 to VERIFYING after scoped runtime evidence and repository validation." in tasks
    assert "Real polish canary executed: yes" in acceptance
    assert "Other accounts polished: 0" in acceptance
    assert "Scheduler enabled tasks: `day_switch,fetch_items,polish`" in acceptance
    assert evidence.is_file()
    evidence_text = read(evidence)
    assert "Target alias: `CANARY-A01`" in evidence_text
    assert "Explicit canary target success delta: 1" in evidence_text
    assert "Other accounts polished during observation: 0" in evidence_text
    assert "Synthetic messages sent: 0" in evidence_text
    assert "Products published: 0" in evidence_text
    assert "Sensitive data recorded: no" in evidence_text
