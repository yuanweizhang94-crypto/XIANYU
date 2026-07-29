from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE_ID = "CHG-0012-validate-upstream-native-multi-account-fixed-template-reply"
CHANGE_DIR = ROOT / "changes" / "active" / CHANGE_ID
CHANGE_FILES = ["proposal.md", "design.md", "tasks.md", "acceptance.md"]


def read_doc(name: str) -> str:
    return (CHANGE_DIR / name).read_text(encoding="utf-8")


def read_change_text() -> str:
    return "\n\n".join(read_doc(name) for name in CHANGE_FILES)


def section(text: str, heading: str) -> str:
    pattern = rf"(?ms)^## {re.escape(heading)}\s*\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, text)
    assert match is not None, f"missing section: {heading}"
    return match.group("body")


def assert_phrases(text: str, phrases: list[str], context: str) -> None:
    missing = [phrase for phrase in phrases if phrase not in text]
    assert not missing, f"{context} missing phrases: {missing}"


def assert_ordered(text: str, phrases: list[str], context: str) -> None:
    positions = []
    missing = []
    for phrase in phrases:
        index = text.find(phrase)
        if index < 0:
            missing.append(phrase)
        positions.append(index)
    assert not missing, f"{context} missing ordered phrases: {missing}"
    assert positions == sorted(positions), f"{context} phrases are not in required order"


def test_chg_0012_draft_documents_exist_and_match_identity() -> None:
    for name in CHANGE_FILES:
        text = read_doc(name)
        assert f"Change ID: {CHANGE_ID}" in text
        assert "Status: DRAFT" in text


def test_chg_0012_uses_pinned_upstream_native_configuration_path() -> None:
    text = read_change_text()
    assert_phrases(
        text,
        [
            "Decision: CONFIGURE_UPSTREAM",
            "bda1a859df63fa5f24e51398fa80a23490bb6dfc",
            "D:/xianyu-upstream-pilot",
            "Xianyu business application and automatic reply execution engine",
            "`D:/xianyu`: safety, governance, operations, and validation control layer",
            "upstream native account UI/API",
            "native WebSocket",
            "native autoreply service",
        ],
        "upstream configuration facts",
    )


def test_chg_0012_documents_sole_executor_and_fail_closed_unknown_executor() -> None:
    text = read_change_text()
    assert_phrases(
        text,
        [
            "The formal sender for this validation is upstream native automatic reply only",
            "Two automatic-reply send executors must never run at the same time",
            "CHG-0010 local worker remains stopped",
            "Stop immediately if any local worker, wrapper-owned sender, or unknown sender appears",
            "Unknown executor state must fail closed",
            "Unknown state = stop, not retry",
        ],
        "sole-executor boundary",
    )


def test_chg_0012_forbids_local_duplicate_implementations() -> None:
    text = read_change_text()
    assert_phrases(
        text,
        [
            "local keyword matcher",
            "local YAML production rules",
            "local autoreply worker extension",
            "local account database",
            "local Cookie vault",
            "local WebSocket parser",
            "local default reply engine",
            "local product-specific reply engine",
            "local image reply executor",
            "local AIReplyEngine",
            "second UI",
            "second API",
            "second production audit",
            "second dedup system",
        ],
        "duplicate implementation prohibitions",
    )


def test_chg_0012_keeps_chg_0010_frozen_and_chg_0015_as_retirement_review() -> None:
    text = read_change_text()
    assert_phrases(
        text,
        [
            "CHG-0010 local autoreply worker remains `FREEZE_AND_DEPRECATE`",
            "It must not be restored as the formal executor",
            "CHG-0015 remains the planned retirement evaluation",
            "evaluate retirement in CHG-0015",
        ],
        "local worker disposition",
    )


def test_chg_0012_two_account_requirements_are_explicit() -> None:
    text = read_change_text()
    assert_phrases(
        text,
        [
            "Use two dedicated test accounts",
            "Record only masked identifiers",
            "Confirm independent login state for account A and account B",
            "Confirm independent WebSocket state for account A and account B",
            "Confirm independent keyword/rule configuration for account A and account B",
            "Use the approved controlled counterpart identity only",
            "Confirm cross-account keyword isolation",
        ],
        "two-account validation requirements",
    )


def test_chg_0012_text_message_cap_has_total_two_account_semantics() -> None:
    cap = section(read_doc("acceptance.md"), "Text-message send cap")
    assert_phrases(
        cap,
        [
            "12 total text messages",
            "across both test accounts",
            "all test cases",
            "not 12 per account",
            "not 12 per test scenario",
            "Inbound messages do not count",
            "Retries, duplicate sends, and abnormal sends count",
            "cap is reached",
            "must not continue",
            "Image sends are excluded",
            "require separate approval",
            "unable to determine whether a message was sent",
            "count it as sent and stop",
        ],
        "text-message cap semantics",
    )


def test_chg_0012_owner_approval_matrix_contains_all_required_fields() -> None:
    matrix = section(read_doc("acceptance.md"), "Required owner-approved live matrix")
    assert_phrases(
        matrix,
        [
            "Test account A masked identifier",
            "Test account B masked identifier",
            "Controlled counterpart identity",
            "Test time window",
            "Test keywords",
            "Expected reply for each test case",
            "Expected send count for each test case",
            "Total approved text-message send cap",
            "Native autoreply start command",
            "Native autoreply stop command",
            "Native WebSocket start command",
            "Native WebSocket stop command",
            "Rollback method",
            "Masked log/evidence location",
            "Risk stop conditions",
            "Sole-executor confirmation",
            "Image-send approval, when applicable",
            "not a generic counterpart label",
            "explicit start and end time or an approved time period",
            "Missing any required field blocks validation from starting",
        ],
        "owner-approved live matrix",
    )


def test_chg_0012_risk_stops_include_uncertainty_and_platform_risks() -> None:
    risk = section(read_doc("acceptance.md"), "Risk stop conditions")
    assert_phrases(
        risk,
        [
            "fail closed",
            "CAPTCHA",
            "Slider verification",
            "Face verification",
            "Device verification",
            "Risk-control warning",
            "Unknown login state",
            "Unknown account state",
            "Unknown WebSocket state",
            "Unknown sender identity",
            "Unknown recipient identity",
            "More than one possible send executor",
            "Unexpected reply content",
            "Unexpected target account or item",
            "Reply loop",
            "Batch trigger",
            "Duplicate or repeated send",
            "Sensitive information exposure",
            "Unable to determine whether a message was sent",
            "Unable to determine whether the stop command took effect",
            "Unable to confirm native autoreply is stopped",
            "Unable to confirm native WebSocket is stopped",
            "Unable to confirm the local CHG-0010 worker remains stopped",
            "Message count reaches or may have exceeded the approved cap",
            "Unknown state = stop, not retry",
            "repeated starts",
            "repeated stops",
            "relogin",
            "automatic retries",
            "continued sends",
        ],
        "risk stop conditions",
    )


def test_chg_0012_stop_and_rollback_are_verifiable_and_ordered() -> None:
    stop = section(read_doc("design.md"), "Stop and rollback plan")
    assert_ordered(
        stop,
        [
            "Block initiation of any new test case",
            "Record the current approved and observed send count",
            "Issue the approved native autoreply stop command",
            "Verify native autoreply is stopped using an approved observable criterion",
            "Issue the approved native WebSocket stop command",
            "Verify native WebSocket is stopped using an approved observable criterion",
            "Verify no scheduler, restart policy, supervisor, or container policy",
            "Verify CHG-0010 local worker remains stopped",
            "Verify no second or unknown send executor exists",
            "Disable or remove only the approved test rules",
            "approved quiet period and confirm no further outbound message occurs",
            "Preserve masked evidence",
            "Generate the masked validation report",
        ],
        "normal stop sequence",
    )
    assert_phrases(
        stop,
        [
            "Native autoreply stopped",
            "Approved process/service/container status shows stopped or disabled",
            "No active autoreply worker is present",
            "No approved rule execution can begin",
            "Native WebSocket stopped",
            "shows disconnected or stopped",
            "No reconnect loop is active",
            "No scheduler or restart policy will reconnect it",
            "No further message can send",
            "No active sender executor",
            "No queued approved test message remains",
            "Approved quiet period completes with no new outbound message",
            "No automatic restart or reconnect occurs",
            "CHG-0010 worker stopped",
            "Repository status command reports `running=False`",
            "No matching worker process exists",
            "`STOP_STATE_UNKNOWN`",
            "Do not issue another test message",
            "Do not start another executor",
            "Do not retry platform actions automatically",
            "Docker restart policy",
            "Compose restart policy",
            "Windows scheduled task",
            "Background launcher",
            "Autoreconnect loop",
            "must not start or must terminate immediately",
            "must not create a new supervisor, monitor, or second control system",
            "Do not delete production data",
            "Do not clean unknown data",
            "Do not modify upstream source code",
            "Do not enable a local substitute executor",
            "Do not automatically continue testing",
        ],
        "verifiable stop and rollback criteria",
    )
