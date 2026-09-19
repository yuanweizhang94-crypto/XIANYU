from __future__ import annotations

from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = CHANGE.parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0038-websocket-registration-readiness.patch"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_chg0038_patch_scope_and_registration_gate() -> None:
    text = _text(PATCH)
    changed = [
        line.split(" b/", 1)[1]
        for line in text.splitlines()
        if line.startswith("diff --git a/")
    ]
    assert changed == ["websocket/app/services/xianyu/xianyu_async.py"]
    assert "reg_mid = generate_mid()" in text
    assert "await self._wait_for_registration_response(ws, reg_mid)" in text
    assert "response_mid == reg_mid" in text
    assert "code != 200" in text
    assert "WebSocket registration response timeout" in text


def test_chg0038_preserves_existing_message_and_sync_paths() -> None:
    text = _text(PATCH)
    assert "self.connection_manager.handle_heartbeat_response(message_data)" in text
    assert "self._dispatch_mid_response(message_data)" in text
    assert "self._handle_message_with_semaphore(message_data, ws)" in text
    assert '"/r/SyncStatus/ackDiff"' in text
    for forbidden in (
        "auto_reply_service.py",
        "backend-web/app/services/chat_new/im_client.py",
        "frontend/",
        "cookie_token_manager.py",
    ):
        assert forbidden not in text


def test_chg0038_contract_is_minimal_upstream_patch() -> None:
    proposal = _text(CHANGE / "proposal.md")
    design = _text(CHANGE / "design.md")
    acceptance = _text(CHANGE / "acceptance.md")
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "global WebSocket restart" in proposal
    assert "No new WebSocket owner" in design
    assert "no new parser" in design
    assert "no new reply worker" in design
    assert "registration timeout cannot produce CONNECTED" in acceptance
