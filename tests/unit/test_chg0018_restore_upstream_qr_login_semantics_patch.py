from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "07caf4f-chg0018-restore-upstream-qr-login-semantics.patch"
EXPECTED_SHA256 = "836D27F71612CF322460412DEBF59A85CD8431B3E0AB77098157E51701C75715"


def _text() -> str:
    return PATCH.read_text(encoding="utf-8")


def _added_for(path: str) -> str:
    text = _text()
    marker = f"diff --git a/{path} b/{path}\n"
    start = text.index(marker)
    next_diff = text.find("\ndiff --git ", start + len(marker))
    block = text[start:] if next_diff < 0 else text[start:next_diff]
    return "\n".join(
        line[1:] for line in block.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def test_patch_hash_is_locked() -> None:
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest().upper() == EXPECTED_SHA256


def test_patch_changes_only_qr_routes_and_qr_only_convergence_owner() -> None:
    paths = [
        line.removeprefix("diff --git a/").split(" b/", 1)[0]
        for line in _text().splitlines()
        if line.startswith("diff --git a/")
    ]
    assert paths == [
        "backend-web/app/api/routes/qr_login.py",
        "backend-web/app/api/routes/shared_scan.py",
        "backend-web/app/services/account_service.py",
    ]
    assert all("chat_new.py" not in path for path in paths)
    assert all("im_token_api.py" not in path for path in paths)
    assert all("captcha" not in path.lower() for path in paths)


def _assert_no_eager_auth_or_publish(added: str) -> None:
    lowered = added.lower()
    for forbidden in (
        "converge_existing_consumers_after_login",
        "get_or_connect(",
        "mark_token_cache_expired",
        "request_im_token",
        "_fetch_im_token",
        "solve_captcha(",
        "run_slider_verification",
        "captcha/solve",
        "probe_account_publish_restriction",
        "list_conversations",
        "/conversations/",
    ):
        assert forbidden.lower() not in lowered


def test_normal_qr_success_restores_upstream_native_post_login_semantics() -> None:
    added = _added_for("backend-web/app/api/routes/qr_login.py")
    _assert_no_eager_auth_or_publish(added)
    assert "get_http_client" in added
    assert added.count('/start"') == 1
    assert added.count('/restart"') == 1
    assert 'if is_new_account:' in added
    assert '"cookie_value": cookies_str' in added
    assert '"user_id": owner_id' in added
    assert '"auth_convergence"' not in added


def test_shared_qr_success_has_same_lazy_consumer_semantics() -> None:
    added = _added_for("backend-web/app/api/routes/shared_scan.py")
    _assert_no_eager_auth_or_publish(added)
    assert "get_http_client" in added
    assert added.count('/start"') == 1
    assert added.count('/restart"') == 1
    assert 'if is_new:' in added
    assert '"cookie_value": cookies_str' in added
    assert '"user_id": owner_id' in added
    assert '"auth_convergence"' not in added


def test_qr_only_convergence_owner_is_deleted_not_replaced() -> None:
    text = _text()
    added = _added_for("backend-web/app/services/account_service.py")
    assert "converge_existing_consumers_after_login" not in added
    assert "AUTH_CONVERGENCE_" not in added
    assert "_auth_convergence_locks" not in added
    assert "_set_auth_convergence_lease" not in added
    assert "-    async def converge_existing_consumers_after_login(" in text
    assert "-    async def _converge_existing_consumers_after_login_impl(" in text


def test_patch_does_not_modify_token_request_shape_or_captcha_solver() -> None:
    text = _text()
    for forbidden_path in (
        "common/services/im_token_api.py",
        "common/services/captcha/",
        "websocket/app/services/xianyu/cookie_token_manager.py",
        "websocket/app/services/xianyu/token_manager.py",
    ):
        assert f"diff --git a/{forbidden_path}" not in text
