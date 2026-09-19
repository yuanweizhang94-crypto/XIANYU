from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "patch_chatnew_spinner_convergence_20260919.py"


def _module():
    spec = importlib.util.spec_from_file_location("spinner_fix", SCRIPT)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_case_1_runtime_connected_overrides_stale_checking() -> None:
    m = _module()
    account = {
        "status": "active",
        "connected": False,
        "runtime_connected": True,
        "chat_state": "SESSION_CHECKING",
    }
    assert m.status_label(account) == "已连接"
    normalized = m.normalize_account(account)
    assert normalized["connected"] is True
    assert normalized["chat_state"] == "READY"


def test_case_2_refresh_already_connected_stays_connected() -> None:
    m = _module()
    account = {
        "status": "active",
        "connected": True,
        "runtime_connected": True,
        "chat_state": "READY",
    }
    assert m.status_label(account) == "已连接"
    assert m.normalize_account(account)["connected"] is True


def test_case_3_accounts_do_not_share_state() -> None:
    m = _module()
    connected = {
        "status": "active",
        "connected": True,
        "runtime_connected": True,
        "chat_state": "READY",
    }
    login = {
        "status": "active",
        "connected": False,
        "runtime_connected": False,
        "chat_state": "LOGIN_REQUIRED",
    }
    assert m.status_label(connected) == "已连接"
    assert m.status_label(login) == "需登录"
    assert m.normalize_account(login)["chat_state"] == "LOGIN_REQUIRED"


def test_case_4_prior_empty_conversation_cache_fix_is_required() -> None:
    m = _module()
    synthetic = m.CACHEFIX_REQUIRED_SNIPPET
    for old, _new in m.REPLACEMENTS:
        synthetic += old
    fixed = m.transform_text(synthetic)
    assert m.CACHEFIX_REQUIRED_SNIPPET in fixed


def test_case_5_human_qr_login_required_is_terminal() -> None:
    m = _module()
    account = {
        "status": "active",
        "connected": False,
        "runtime_connected": False,
        "connection_state": "disconnected",
        "token_ready": False,
        "chat_state": "LOGIN_REQUIRED",
    }
    assert m.status_label(account) == "需登录"
    assert m.should_auto_connect(account) is False


def test_case_6_error_timeout_is_terminal_not_spinner() -> None:
    m = _module()
    for state, label in [
        ("TEMPORARY_FAILURE", "暂不可用"),
        ("CONNECTION_FAILED", "连接失败"),
        ("RATE_LIMITED", "请求频繁"),
    ]:
        account = {
            "status": "active",
            "connected": False,
            "runtime_connected": False,
            "chat_state": state,
        }
        assert m.status_label(account) == label
        assert "正在" not in m.status_label(account)


def test_case_7_chat_connected_never_auto_connects_again() -> None:
    m = _module()
    account = {
        "status": "active",
        "connected": True,
        "runtime_connected": True,
        "connection_state": "connected",
        "token_ready": True,
        "chat_state": "READY",
    }
    assert m.should_auto_connect(account) is False


def test_case_8_native_ready_chat_missing_connects_at_most_once() -> None:
    m = _module()
    account = {
        "status": "active",
        "connected": False,
        "runtime_connected": False,
        "connection_state": "connected",
        "token_ready": True,
        "chat_state": "CONNECTION_FAILED",
    }
    assert m.should_auto_connect(account) is True
    assert m.should_auto_connect(account, already_attempted=True) is False
    assert m.should_auto_connect(account, connect_inflight=True) is False


def test_disabled_account_never_renders_checking_spinner() -> None:
    m = _module()
    account = {
        "status": "disabled",
        "connected": False,
        "runtime_connected": False,
        "chat_state": "SESSION_CHECKING",
    }
    assert m.status_label(account) == "已禁用"
    assert m.should_auto_connect(account) is False


def test_patch_fails_closed_on_wrong_or_duplicate_preimage() -> None:
    m = _module()
    with pytest.raises(ValueError):
        m.transform_text("missing locked preimage")

    synthetic = m.CACHEFIX_REQUIRED_SNIPPET
    for old, _new in m.REPLACEMENTS:
        synthetic += old
    duplicate = synthetic + m.REPLACEMENTS[0][0]
    with pytest.raises(ValueError):
        m.transform_text(duplicate)
