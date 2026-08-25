from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHANGE = ROOT / "changes/archive/CHG-0032-controlled-online-chat-send"
EVIDENCE = CHANGE / "evidence/20260825-phase2-read-only-chat-preflight.md"
CHG0029 = ROOT / "changes/archive/CHG-0029-core-capability-closure"
REQUIRED_DOCS = ("proposal.md", "design.md", "tasks.md", "acceptance.md")


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_chg0032_is_archived_with_counterpart_blocker_and_zero_sends() -> None:
    combined = "\n".join(_text(CHANGE / name) for name in REQUIRED_DOCS) + "\n" + _text(EVIDENCE)
    for name in REQUIRED_DOCS:
        text = _text(CHANGE / name)
        assert "Change ID: CHG-0032-controlled-online-chat-send" in text
        assert "Status: ARCHIVED" in text

    for marker in (
        "OWNER_DECISION=NO-GO",
        "HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART",
        "CONTROLLED_COUNTERPART=false",
        "ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART",
        "MANUAL_CHAT_SENDS=0",
        "CHAT_SENDS=0",
        "MESSAGE_SEND_INVOCATIONS=0",
        "SEND_INVOCATION_EXECUTED=false",
        "SEND_READBACK_EXECUTED=false",
        "REMOTE_VISIBLE_READBACK_EXECUTED=false",
    ):
        assert marker in combined


def test_chg0032_masks_account_and_does_not_persist_sensitive_counterpart_data() -> None:
    combined = _text(CHANGE / "acceptance.md") + "\n" + _text(EVIDENCE)
    assert "280***247" in combined
    assert not re.search(r"\b280\d+247\b", combined)
    assert "FULL_ACCOUNT_ID_RECORDED=false" in combined
    assert "SCREENSHOT_COPIED=false" in combined
    assert "SCREENSHOT_HASHED=false" in combined
    assert "CUSTOMER_CONTENT_PERSISTED=false" in combined
    assert "COUNTERPART_IDS_PERSISTED=false" in combined


def test_chg0032_chat_owner_contract_and_duplicate_send_gate_are_recorded() -> None:
    combined = _text(CHANGE / "tasks.md") + "\n" + _text(EVIDENCE)
    for marker in (
        "CHAT_OWNER_ROUTE=POST /api/v1/chat-new/send-message/{account_id}",
        "CHAT_OWNER_FUNCTION=backend-web/app/api/routes/chat_new.py::send_message -> backend-web/app/services/chat_new/im_client.py::GoofishImClient.send_text_message",
        "CHAT_SEND_LWP=/r/MessageSend/sendByReceiverScope",
        "CHAT_ACCEPTED_IDENTITY=server messageId returned by chat-new route",
        "CHAT_CLIENT_UUID_GENERATED_PER_ATTEMPT=true",
        "CHAT_PRE_SEND_IDEMPOTENCY_KEY_PRESENT=false",
        "CHAT_DUPLICATE_GUARD=ONE_INVOCATION_COMMANDER_GATE_PLUS_POST_SEND_DURABLE_VISIBLE_READBACK_REQUIRED",
        "REMOTE_VISIBLE_READBACK_ROUTE=GET /api/v1/chat-new/messages/{account_id}/{cid}",
    ):
        assert marker in combined


def test_chg0032_token_session_websocket_unread_and_restart_baseline_are_recorded() -> None:
    combined = _text(CHANGE / "acceptance.md") + "\n" + _text(EVIDENCE)
    for marker in (
        "ACCOUNT_ENABLED=true",
        "ACCOUNT_ONLINE=true",
        "LOGIN_READY=true",
        "PLATFORM_VERIFICATION_STATE=false",
        "CHAT_TOKEN_SESSION_COOKIE_LINEAGE=PASS_BY_SANITIZED_ACCOUNT_STATUS_AND_CHAT_NEW_CONVERSATION_READ",
        "WEBSOCKET_HEALTH_CAPABILITY=PASS_BY_ACCOUNT_ONLINE_AND_CHAT_NEW_CONVERSATION_READ",
        "CONVERSATION_METADATA_ROWS=4",
        "UNREAD_TOTAL=0",
        "UNREAD_BACKLOG_BASELINE_TOTAL=0",
        "SERVICE_IMAGE_RESTART_BASELINE=ALL_INSPECTED_XIANYU_SERVICES_RESTARTCOUNT_0",
    ):
        assert marker in combined


def test_chg0029_chat_runtime_regression_evidence_remains_present() -> None:
    evidence = _text(CHG0029 / "evidence/20260825-core-capability-runtime-activation.md")
    for marker in (
        "ONLINE_CHAT_REAL_E2E=READ_ONLY_CONVERSATION_AND_MESSAGE_LIST_PASS_NO_SEND",
        "CHAT_RUNTIME_CONNECTED_QUEUE=3",
        "WEBSOCKET_INTERNAL_CONNECTION_STATS=success_total_instances_7_connected_7_by_state_connected_7",
        "WEBSOCKET_RECONNECT_WINDOW_15M=0",
        "AUTO_REPLY_AI_ENABLED_ACCOUNTS=0",
    ):
        assert marker in evidence


def test_generated_project_state_has_no_active_change_after_archive() -> None:
    state = json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] is None
    assert state["tasks"]["total"] == 0
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["next_task"] is None
