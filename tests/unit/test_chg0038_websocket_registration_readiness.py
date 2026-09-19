from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0038-websocket-registration-readiness.patch"
CHANGE = ROOT / "changes/active/CHG-0038-websocket-registration-readiness"


def patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_patch_targets_native_websocket_owner_only():
    text = patch_text()
    assert text.count("diff --git ") == 1
    assert (
        "diff --git a/websocket/app/services/xianyu/xianyu_async.py "
        "b/websocket/app/services/xianyu/xianyu_async.py"
    ) in text
    assert "auto_reply_service.py" not in text
    assert "im_client.py" not in text
    assert "frontend/" not in text


def test_registration_requires_matching_success_response():
    text = patch_text()
    assert "reg_mid = generate_mid()" in text
    assert '"mid": reg_mid' in text
    assert "await self._wait_for_registration_response(ws, reg_mid)" in text
    assert "response_mid == reg_mid" in text
    assert "code != 200" in text
    assert "WebSocket registration rejected" in text


def test_registration_timeout_fails_before_connected_readiness():
    text = patch_text()
    assert "asyncio.wait_for(ws.recv(), timeout=remaining)" in text
    assert "WebSocket registration response timeout" in text
    assert text.index("await self._wait_for_registration_response(ws, reg_mid)") < text.index("ackDiff")


def test_early_frames_are_preserved_for_existing_handlers():
    text = patch_text()
    assert "self.connection_manager.handle_heartbeat_response(message_data)" in text
    assert "self._dispatch_mid_response(message_data)" in text
    assert "self._handle_message_with_semaphore(message_data, ws)" in text


def test_ackdiff_remains_after_confirmed_registration():
    text = patch_text()
    assert '"/r/SyncStatus/ackDiff"' in text
    assert "await asyncio.sleep(1)" in text
    assert "连接注册完成" in text


def test_change_contract_preserves_existing_owners():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    design = (CHANGE / "design.md").read_text(encoding="utf-8")
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "global WebSocket restart" in proposal
    assert "No new WebSocket owner" in design
    assert "no new parser" in design
    assert "no new reply worker" in design
