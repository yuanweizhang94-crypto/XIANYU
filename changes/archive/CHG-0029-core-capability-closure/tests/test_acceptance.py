import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE = Path(__file__).resolve().parents[1]
ARCHIVED_CHG0028 = ROOT / "changes/archive/CHG-0028-publish-readiness-owner-convergence"
REQUIRED_DOCS = ("proposal.md", "design.md", "tasks.md", "acceptance.md")


def test_chg0029_is_archived_with_contract():
    active_dirs = [path.name for path in (ROOT / "changes/active").iterdir() if path.is_dir()]
    assert active_dirs == []

    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "User outcome: automatic reply, online chat, and product publish" in proposal
    assert "Confirmed blocker: production containers are running older component images" in proposal
    assert "Smallest success test: source/patch deterministic tests pass" in proposal


def test_required_docs_have_consistent_identity_and_status():
    expected = "Change ID: CHG-0029-core-capability-closure"
    for name in REQUIRED_DOCS:
        text = (CHANGE / name).read_text(encoding="utf-8")
        assert expected in text
        assert "Status: ARCHIVED" in text


def test_chg0028_is_archived_after_pr41_merge():
    for name in REQUIRED_DOCS:
        text = (ARCHIVED_CHG0028 / name).read_text(encoding="utf-8")
        assert "Change ID: CHG-0028-publish-readiness-owner-convergence" in text
        assert "Status: ARCHIVED" in text
    acceptance = (ARCHIVED_CHG0028 / "acceptance.md").read_text(encoding="utf-8")
    assert "`PR_MERGED=true`" in acceptance
    assert "`MERGE_COMMIT_SHA=4ba50db5c83aa3d3f06345b0f7bcf6192f9cfd89`" in acceptance


def test_safety_boundaries_are_explicit():
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    for marker in (
        "REAL_MESSAGES_SENT=0",
        "REAL_PRODUCTS_PUBLISHED=0",
        "REAL_PRODUCTS_MODIFIED=0",
        "ITEM_SYNC_INVOCATION_COUNT=0",
        "QR_LOGIN_INVOCATION_COUNT=0",
        "MANUAL_RECONNECT_INVOCATION_COUNT=0",
        "BROWSER_INVOCATION_COUNT=0",
        "GLOBAL_PERSISTED_PUBLISH_READINESS_WRITER_CREATED=0",
        "DIRTY_CHG0018_TOUCHED=0",
    ):
        assert marker in acceptance


def test_chg0028_patch_hash_boundary_is_locked():
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "Git blob/LF bytes" in acceptance
    assert "CED451293701C53475E23F9B87DF205AB97AFDD0B3696D35A4D9C8675BC4E490" in acceptance


def test_project_state_points_to_chg0029():
    state = json.loads((ROOT / "generated/PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] is None
    assert state["tasks"]["total"] == 0
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["next_task"] is None


def test_github_merge_closure_is_recorded():
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    evidence = (CHANGE / "evidence/20260825-core-capability-runtime-activation.md").read_text(
        encoding="utf-8"
    )
    for marker in (
        "`PR_NUMBER=42`",
        "`PR_MERGED=true`",
        "`MERGE_COMMIT_SHA=fe1b184c9d32c9d94721320702b5d6b0c55fe169`",
        "SCOPED_CI_SECURITY=PASS",
        "GLOBAL_CI_DEBT_ABSORBED=NO",
    ):
        assert marker in acceptance or marker in evidence


def test_runtime_acceptance_evidence_includes_connected_chat_read_and_queue():
    evidence = (CHANGE / "evidence/20260825-core-capability-runtime-activation.md").read_text(
        encoding="utf-8"
    )
    required = (
        "CONVERSATION_CONNECTED_CANDIDATES=3",
        "CONVERSATION_SUCCESS_TRUE=3",
        "CONVERSATION_SAMPLE_COUNT=5",
        "MESSAGE_LIST_HTTP=200",
        "CHAT_RUNTIME_CONNECTED_QUEUE=3",
        "BACKEND_R2_STARTUP_REHYDRATION=eligible=4,ready=3,skipped=3",
        "CHAT_STARTUP_NOT_READY_REASON_FOR_REMAINING_ELIGIBLE=cached_chat_token_unavailable",
        "CHAT_SELF_REHYDRATION=PASS_FOR_VALID_CACHED_TOKEN__3_READY_1_FAIL_CLOSED_NO_CACHE",
        "WEBSOCKET_INTERNAL_CONNECTION_STATS=success_total_instances_7_connected_7_by_state_connected_7",
        "WEBSOCKET_RECONNECT_WINDOW_15M=0",
        "AUTO_REPLY_AI_ENABLED_ACCOUNTS=0",
        "AUTO_REPLY_CURRENT_CONFIG=NO_REAL_AUTO_REPLY_BECAUSE_AI_ENABLED_0_OF_12",
        "AUTO_REPLY_BUSINESS_CAPABILITY_COHORT=ONLINE_4__CHECKING_2__PLATFORM_VERIFICATION_REQUIRED_1__DISABLED_5",
        "AUTO_REPLY_WORKER_BACKLOG_OBSERVED=false",
        "ONLINE_CHAT_BUSINESS_CAPABILITY=READY_3__CONNECTING_NO_CACHED_TOKEN_1__CHECKING_2__PLATFORM_VERIFICATION_REQUIRED_1__DISABLED_5",
        "PUBLISH_BUSINESS_CAPABILITY=NOT_CHECKED_ON_DEMAND_7__DISABLED_5",
        "ONLINE_CHAT_REAL_E2E=READ_ONLY_CONVERSATION_AND_MESSAGE_LIST_PASS_NO_SEND",
    )
    for marker in required:
        assert marker in evidence
    assert "CHAT_CONNECTED_HASHES=" not in evidence
    assert "CONVERSATION_SAMPLE_ACCOUNT_HASH=" not in evidence
