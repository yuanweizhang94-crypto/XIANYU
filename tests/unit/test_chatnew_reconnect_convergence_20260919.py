from __future__ import annotations

import importlib.util
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "patch_chatnew_reconnect_convergence_20260919.py"


def _module():
    spec = importlib.util.spec_from_file_location("chat_reconnect_fix", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _ready_missing_chat():
    return {
        "status": "active",
        "connected": False,
        "runtime_connected": False,
        "connection_state": "connected",
        "token_ready": True,
        "chat_state": "CONNECTION_FAILED",
    }


def test_connected_account_never_reconnects() -> None:
    m = _module()
    a = _ready_missing_chat()
    a["connected"] = True
    assert not m.should_auto_connect(a, now_ms=30_000)


def test_runtime_connected_account_never_reconnects() -> None:
    m = _module()
    a = _ready_missing_chat()
    a["runtime_connected"] = True
    assert not m.should_auto_connect(a, now_ms=30_000)


def test_native_not_ready_does_not_reconnect() -> None:
    m = _module()
    a = _ready_missing_chat()
    a["connection_state"] = "reconnecting"
    assert not m.should_auto_connect(a, now_ms=30_000)


def test_terminal_login_states_do_not_reconnect() -> None:
    m = _module()
    for state in ("LOGIN_REQUIRED", "PLATFORM_VERIFICATION_REQUIRED", "SESSION_EXPIRED"):
        a = _ready_missing_chat()
        a["chat_state"] = state
        assert not m.should_auto_connect(a, now_ms=30_000)


def test_missing_chat_owner_reconnects_after_cooldown() -> None:
    m = _module()
    a = _ready_missing_chat()
    assert not m.should_auto_connect(a, last_attempt_ms=20_000, now_ms=30_000)
    assert m.should_auto_connect(a, last_attempt_ms=10_000, now_ms=30_000)


def test_later_disconnect_after_prior_success_can_recover_again() -> None:
    m = _module()
    a = _ready_missing_chat()
    assert m.should_auto_connect(a, last_attempt_ms=10_000, now_ms=30_001)


def test_inflight_request_blocks_duplicate_connect() -> None:
    m = _module()
    assert not m.should_auto_connect(_ready_missing_chat(), now_ms=30_000, inflight=True)


def test_transform_preserves_previous_convergence_fixes() -> None:
    m = _module()
    synthetic = m.REQUIRED_SPINNER_FIX + m.REQUIRED_CACHE_FIX + m.OLD_REF + m.OLD_EFFECT
    fixed = m.transform_text(synthetic)
    assert m.REQUIRED_SPINNER_FIX in fixed
    assert m.REQUIRED_CACHE_FIX in fixed
    assert m.OLD_REF not in fixed
    assert "autoChatRetryAt" in fixed


def test_transform_fails_closed() -> None:
    m = _module()
    with pytest.raises(ValueError):
        m.transform_text("missing production preimage")
