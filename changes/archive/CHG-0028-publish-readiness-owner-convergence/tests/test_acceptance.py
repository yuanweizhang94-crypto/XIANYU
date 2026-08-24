import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE = Path(__file__).resolve().parents[1]
ARCHIVED_CHG0027 = ROOT / "changes/archive/CHG-0027-session-transient-classification-qr-cooldown-lineage"
EVIDENCE = CHANGE / "evidence/20260824-t1-t3-read-only-owner-audit-and-stop-decision.md"
REQUIRED_DOCS = ("proposal.md", "design.md", "tasks.md", "acceptance.md")


def test_change_is_archived_and_has_consistent_identity():
    expected_id = "Change ID: CHG-0028-publish-readiness-owner-convergence"
    for name in REQUIRED_DOCS:
        text = (CHANGE / name).read_text(encoding="utf-8")
        assert expected_id in text
        assert "Status: ARCHIVED" in text


def test_scope_locks_publisher_readiness_and_excludes_browser_followup():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "PUBLISH_READINESS_LAZY_PENDING_NO_READY_PRODUCER" in proposal
    assert "AUTHORIZED_BROWSER_CANNOT_RENDER_FIXED_LOCAL_XIANYU_FRONTEND" in proposal
    assert "remains owned outside this Change" in proposal
    assert "OWNER_APPROVAL_RECEIVED=true" in proposal
    assert "OWNER_APPROVED_SCOPE=PUBLISHER_READINESS_ONLY" in proposal
    assert "BROWSER_SCOPE_INCLUDED=false" in proposal
    assert "CHG0028_OWNER_CONTRACT_DECISION=APPROVED__SELECTED_ACCOUNT_ON_DEMAND_CAPABILITY" in proposal
    assert "GLOBAL_PERSISTED_PUBLISH_READINESS=DEPRECATED" in proposal
    assert "LINEAGE_AWARE_READINESS_WRITER=NOT_AUTHORIZED" in proposal


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


def test_t1_t3_evidence_proves_missing_transition_and_stop_boundary():
    evidence = EVIDENCE.read_text(encoding="utf-8")
    required = (
        "T1_READ_ONLY_OWNER_AUDIT=PASS",
        "T2_DETERMINISTIC_LAZY_PENDING_REPRODUCTION=PASS",
        "T3_REUSE_DECISION=PATCH_UPSTREAM",
        "T3_EXECUTION_DECISION=STOP",
        "detect_publish_account_capability success",
        "session_maintenance.consumers.publish.state=READY",
        "ADOPT_UPSTREAM_AS_IS=INSUFFICIENT",
        "NEW_READINESS_WRITER_OR_CONTRACT_DECISION_REQUIRED=true",
        "REAL_PRODUCTS_PUBLISHED=0",
        "PRODUCTION_ACCOUNT_MUTATION_COUNT=0",
        "BROWSER_INVOCATION_COUNT=0",
    )
    for marker in required:
        assert marker in evidence


def test_implementation_is_unblocked_by_selected_account_contract():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    tasks = (CHANGE / "tasks.md").read_text(encoding="utf-8")
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "Execution decision: CONTINUE_SELECTED_ACCOUNT_ON_DEMAND" in proposal
    assert "IMPLEMENTATION_AUTHORIZED=true" in proposal
    assert "- [x] T3 Finalized `REUSE_DECISION=PATCH_UPSTREAM` with `EXECUTION_DECISION=STOP`" in tasks
    assert "- [x] T4 UNBLOCKED" in tasks
    assert "STOP_ACCEPTANCE=PASS" in acceptance
    assert "T4_STATUS=UNBLOCKED_AND_COMPLETE" in acceptance


def test_generated_state_reports_implementing_next_task():
    state = json.loads((ROOT / "generated/PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] == {
        "id": "CHG-0029-core-capability-closure",
        "status": "IMPLEMENTING",
        "path": "changes/active/CHG-0029-core-capability-closure",
    }
    assert state["tasks"]["total"] >= 6
    assert state["tasks"]["next_task"].startswith("T5")


def test_github_merge_closure_is_recorded():
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    tasks = (CHANGE / "tasks.md").read_text(encoding="utf-8")
    assert "`PR_MERGED=true`" in acceptance
    assert "`MERGE_COMMIT_SHA=4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89`" in acceptance
    assert "- [x] T8 Persist exact evidence" in tasks
