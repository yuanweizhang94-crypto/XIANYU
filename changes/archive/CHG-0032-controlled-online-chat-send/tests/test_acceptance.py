from __future__ import annotations

import json
import re
from pathlib import Path


CHANGE_ID = "CHG-0032-controlled-online-chat-send"
MASKED_ACCOUNT = "280***247"
MESSAGE_TEXT = "系统功能测试，请忽略，无需回复。"


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists() and (parent / "changes").exists():
            return parent
    raise AssertionError("repository root not found")


def _change_dir() -> Path:
    root = _repo_root()
    for base in (root / "changes" / "active", root / "changes" / "archive"):
        candidate = base / CHANGE_ID
        if candidate.exists():
            return candidate
    raise AssertionError(f"{CHANGE_ID} not found")


def _text(name: str) -> str:
    return (_change_dir() / name).read_text(encoding="utf-8")


def test_chg0032_contract_and_zero_action_gate_are_recorded() -> None:
    combined = "\n".join(
        _text(name)
        for name in ("proposal.md", "design.md", "tasks.md", "acceptance.md")
    )

    assert "Status: ARCHIVED" in combined
    assert "User outcome: send exactly one harmless controlled message" in combined
    assert "Confirmed blocker: a user-controlled counterpart/conversation" in combined
    assert "Smallest success test: one send invocation" in combined
    assert "REAL_CHAT_SEND_ALLOWED=false" in combined
    assert "COMMANDER_GO_FOR_REAL_CHAT_SEND=false" in combined
    assert f"MESSAGE_TEXT_IF_LATER_AUTHORIZED={MESSAGE_TEXT}" in combined
    assert "GO_FOR_REAL_CHAT_SEND" in combined
    assert "ONLINE_CHAT_REAL_SEND_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART" in combined
    assert "SEND_READBACK_EXECUTED=false" in combined


def test_chg0032_masks_identity_and_does_not_persist_sensitive_artifacts() -> None:
    evidence = (_change_dir() / "evidence" / "20260825-phase2-read-only-chat-preflight.md").read_text(
        encoding="utf-8"
    )
    combined = _text("acceptance.md") + "\n" + evidence

    assert MASKED_ACCOUNT in combined
    assert not re.search(r"\b280\d+247\b", combined)
    assert "SCREENSHOT_COPIED=false" in evidence
    assert "SCREENSHOT_HASHED=false" in evidence
    assert "FULL_ACCOUNT_ID_RECORDED=false" in evidence

    for counter in (
        "MESSAGE_SEND_INVOCATIONS=0",
        "AI_INVOCATIONS=0",
        "BROWSER_INVOCATIONS=0",
        "QR_INVOCATIONS=0",
        "RECONNECT_INVOCATIONS=0",
        "PUBLISH_INVOCATIONS=0",
        "SYNC_INVOCATIONS=0",
        "ACCOUNT_MUTATION_COUNT=0",
        "DEPLOY_INVOCATIONS=0",
        "COMMIT_INVOCATIONS=0",
        "PUSH_INVOCATIONS=0",
        "PRODUCTION_MUTATION_COUNT=0",
        "CHAT_SENDS=0",
    ):
        assert counter in combined


def test_chg0032_generated_state_points_to_active_change() -> None:
    state = json.loads((_repo_root() / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))
    assert state["active_change"] is None
    assert state["tasks"]["total"] == 0
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["next_task"] is None
