import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE_ID = "CHG-0017-upstream-native-auto-ai-delivery"
CHANGE_DIR = ROOT / "changes" / "active" / CHANGE_ID
CHANGE_FILES = ["proposal.md", "design.md", "tasks.md", "acceptance.md", "threat-model.md"]


def read_doc(name: str) -> str:
    return (CHANGE_DIR / name).read_text(encoding="utf-8")


def test_change_documents_are_implementing() -> None:
    for name in CHANGE_FILES:
        text = read_doc(name)
        assert f"Change ID: {CHANGE_ID}" in text
        assert "Status: IMPLEMENTING" in text


def test_execution_contract_is_recorded() -> None:
    docs = "\n\n".join(read_doc(name) for name in CHANGE_FILES)
    assert "User outcome:" in docs
    assert "Confirmed blocker:" in docs
    assert "Smallest success test:" in docs
    assert "CHG-0016 live manual handoff was not accepted by the platform" in docs


def test_reuse_decision_is_configure_upstream() -> None:
    docs = "\n\n".join(read_doc(name) for name in CHANGE_FILES)
    assert "Decision: CONFIGURE_UPSTREAM" in docs
    assert "PATCH_UPSTREAM" in docs
    assert "Decision: BUILD_LOCAL_EXCEPTION" not in docs


def test_upstream_candidate_and_native_paths_are_recorded() -> None:
    audit = (CHANGE_DIR / "evidence" / "upstream-audit.md").read_text(encoding="utf-8")
    for required in [
        "4c5e1ac5f532c7313365d70409ae115305de8a55",
        "D:/xianyu-upstream-delivery-chg0017",
        "websocket/app/api/routes/internal.py",
        "websocket/app/services/xianyu/cookie_manager.py",
        "websocket/app/services/xianyu/auto_reply_service.py",
        "websocket/app/services/xianyu/ai_reply_engine.py",
        "backend-web/app/api/routes/ai.py",
        "common/services/im_token_api.py",
        "common/services/remote_token_api.py",
    ]:
        assert required in audit


def test_safety_boundaries_are_explicit() -> None:
    acceptance = read_doc("acceptance.md")
    for required in [
        "No second IM, Token, WebSocket, sender, AI worker, or automatic reply worker is created.",
        "CHG-0010 remains frozen, deprecated, and stopped.",
        "Controlled reply validation is limited to `ACCOUNT-A` and `OWNER_TEST_ACCOUNT_B`.",
        "Automatic test replies are capped at 8 total.",
        "No message is sent to non-whitelist accounts or real customers.",
        "Validation stops at `READY_FOR_GO_LIVE`",
    ]:
        assert required in acceptance


def test_tasks_reflect_required_t1_to_t17_plan() -> None:
    tasks = read_doc("tasks.md")
    for number in range(1, 18):
        assert f"T{number} " in tasks
    assert "- [x] T7 Create latest upstream candidate worktree." in tasks
    assert "- [ ] T8 Validate upstream native Token and account connection." in tasks
    assert "- [ ] T15 Wait for OWNER GO_LIVE." in tasks
    assert "Completed tasks: 7 / 17" in tasks
    assert "Next task: T8 Validate upstream native Token and account connection." in tasks


def test_generated_state_points_to_active_change() -> None:
    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] == {
        "id": CHANGE_ID,
        "status": "IMPLEMENTING",
        "path": f"changes/active/{CHANGE_ID}",
    }
    assert state["tasks"]["total"] == 17
    assert state["tasks"]["completed"] == 7
    assert state["tasks"]["next_task"] == "T8 Validate upstream native Token and account connection."


def test_owner_implementation_approval_is_recorded() -> None:
    proposal = read_doc("proposal.md")
    assert "Project-owner implementation approval:" in proposal
    assert "Do not rebuild existing upstream capabilities." in proposal
    assert "Do not enable production customer replies before `GO_LIVE ACCOUNT-A`." in proposal


def test_owner_test_account_resolution_is_recorded_without_runtime_start() -> None:
    evidence = (
        CHANGE_DIR
        / "evidence"
        / "CHG17-DELIVERY-20260731T043547Z-H8SE-masked-report.md"
    ).read_text(encoding="utf-8")
    assert "OWNER_TEST_ACCOUNT_RESOLVED" in evidence
    assert "`ACCOUNT-A` local alias: resolved" in evidence
    assert "`ACCOUNT-A` database match count: `1`" in evidence
    assert "`OWNER_TEST_ACCOUNT_B` local alias: resolved" in evidence
    assert "`OWNER_TEST_ACCOUNT_B` database match count: `1`" in evidence
    assert "Alias values are distinct: yes" in evidence
    assert "Candidate runtime started: no" in evidence
    assert "Messages sent: `0`" in evidence
    assert "Cookie exposed: no" in evidence
    assert "Token exposed: no" in evidence


def test_t8_platform_verification_blocker_is_recorded_zero_send() -> None:
    evidence = (
        CHANGE_DIR
        / "evidence"
        / "CHG17-DELIVERY-20260731T043547Z-H8SE-T8-platform-verification-required.md"
    ).read_text(encoding="utf-8")
    assert "`PLATFORM_VERIFICATION_REQUIRED`" in evidence
    assert "Account start requests: `1`" in evidence
    assert "Final connection state: disconnected" in evidence
    assert "`FAIL_SYS_USER_VALIDATE`: present" in evidence
    assert "send-message signal: absent" in evidence
    assert "Messages sent by CHG-0017 T8: `0`" in evidence
    assert "T8 remains unchecked" in evidence


def test_t8_owner_login_followup_still_zero_send() -> None:
    evidence = (
        CHANGE_DIR
        / "evidence"
        / "CHG17-DELIVERY-20260731T043547Z-H8SE-T8-owner-login-still-platform-verification.md"
    ).read_text(encoding="utf-8")
    assert "`PLATFORM_VERIFICATION_STILL_REQUIRED`" in evidence
    assert "Remote Token connectivity test: success" in evidence
    assert "Account start requests after owner login: `1`" in evidence
    assert "Token obtained: no" in evidence
    assert "WebSocket connected: false" in evidence
    assert "Messages sent by this attempt: `0`" in evidence
    assert "T8 remains unchecked" in evidence
