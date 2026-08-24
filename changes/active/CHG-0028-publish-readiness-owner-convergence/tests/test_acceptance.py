import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE = Path(__file__).resolve().parents[1]
ARCHIVED_CHG0027 = ROOT / "changes/archive/CHG-0027-session-transient-classification-qr-cooldown-lineage"
REQUIRED_DOCS = ("proposal.md", "design.md", "tasks.md", "acceptance.md")


def test_change_is_approved_and_has_consistent_identity():
    expected_id = "Change ID: CHG-0028-publish-readiness-owner-convergence"
    for name in REQUIRED_DOCS:
        text = (CHANGE / name).read_text(encoding="utf-8")
        assert expected_id in text
        assert "Status: APPROVED" in text


def test_scope_locks_publisher_readiness_and_excludes_browser_followup():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "PUBLISH_READINESS_LAZY_PENDING_NO_READY_PRODUCER" in proposal
    assert "AUTHORIZED_BROWSER_CANNOT_RENDER_FIXED_LOCAL_XIANYU_FRONTEND" in proposal
    assert "remains owned outside this Change" in proposal
    assert "OWNER_APPROVAL_RECEIVED=true" in proposal
    assert "OWNER_APPROVED_SCOPE=PUBLISHER_READINESS_ONLY" in proposal
    assert "BROWSER_SCOPE_INCLUDED=false" in proposal


def test_safety_and_no_parallel_owner_invariants_are_explicit():
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    for marker in (
        "REAL_MESSAGES_SENT=0",
        "REAL_PRODUCTS_PUBLISHED=0",
        "REAL_PRODUCTS_MODIFIED=0",
        "NEW_ITEM_SYNC_INVOCATION_COUNT=0",
        "QR_LOGIN_INVOCATION_COUNT=0",
        "MANUAL_RECONNECT_INVOCATION_COUNT=0",
        "PRODUCTION_ACCOUNT_MUTATION_COUNT=0",
    ):
        assert marker in acceptance
    assert "no second readiness owner" in acceptance


def test_chg0027_is_archived_without_changing_its_evidence():
    for name in REQUIRED_DOCS:
        assert "Status: ARCHIVED" in (ARCHIVED_CHG0027 / name).read_text(encoding="utf-8")
    evidence = (
        ARCHIVED_CHG0027
        / "evidence/20260824-scoped-production-acceptance-and-formal-persistence.md"
    ).read_text(encoding="utf-8")
    assert "CHG0027_SCOPED_PRODUCTION_ACCEPTANCE=PASS" in evidence
    assert "FOLLOWUP_DEFECT_1=PUBLISH_READINESS_LAZY_PENDING_NO_READY_PRODUCER" in evidence


def test_generated_state_reports_approved_next_task():
    state = json.loads((ROOT / "generated/PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] == {
        "id": "CHG-0028-publish-readiness-owner-convergence",
        "status": "APPROVED",
        "path": "changes/active/CHG-0028-publish-readiness-owner-convergence",
    }
    assert state["tasks"]["total"] == 8
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["next_task"].startswith("T1 ")
