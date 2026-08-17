from __future__ import annotations

from pathlib import Path

from scripts.project_context import render_context, required_reading
from scripts.generate_state import build_project_state

ROOT = Path(__file__).resolve().parents[2]
PATCH_ROOT = ROOT / "vendor" / "patches" / "xianyu-auto-reply"
QR_PATCH = PATCH_ROOT / "07caf4f-chg0018-restore-upstream-qr-login-semantics.patch"
CHAT_PATCH = PATCH_ROOT / "59c64df-chg0018-restore-latest-upstream-chat.patch"
AUTO_REPLY_PATCH = PATCH_ROOT / "64c245-chg0018-auto-reply-stability-consolidation.patch"
HUMAN_RECONNECT_PATCH = PATCH_ROOT / "b75d63b-chg0018-human-verification-reconnect.patch"
PID_REAPER_PATCH = PATCH_ROOT / "64c245-chg0018-websocket-pid-reaper.patch"
HANDOFF = ROOT / "docs" / "AI_PROJECT_HANDOFF.md"
RECOVERY_EVIDENCE = (
    ROOT
    / "changes"
    / "active"
    / "CHG-0018-account-profile-publish-safety"
    / "evidence"
    / "20260817-chat-platform-risk-recovery-success.md"
)


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _patch_added_block(path: Path, source_path: str) -> str:
    text = _text(path)
    marker = f"diff --git a/{source_path} b/{source_path}\n"
    start = text.index(marker)
    end = text.find("\ndiff --git ", start + len(marker))
    block = text[start:] if end < 0 else text[start:end]
    return "\n".join(
        line[1:]
        for line in block.splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def _patch_removed_block(path: Path, source_path: str) -> str:
    text = _text(path)
    marker = f"diff --git a/{source_path} b/{source_path}\n"
    start = text.index(marker)
    end = text.find("\ndiff --git ", start + len(marker))
    block = text[start:] if end < 0 else text[start:end]
    return "\n".join(
        line[1:]
        for line in block.splitlines()
        if line.startswith("-") and not line.startswith("---")
    )


def _assert_qr_added_block_is_lazy(source_path: str) -> None:
    added = _patch_added_block(QR_PATCH, source_path).lower()
    for forbidden in (
        "get_or_connect(",
        "request_im_token",
        "_fetch_im_token",
        "solve_captcha(",
        "captcha/solve",
        "conversation",
        "publish_preflight",
        "probe_account_publish_restriction",
        "converge_existing_consumers_after_login",
    ):
        assert forbidden not in added
    assert "/start" in added
    assert "/restart" in added


def test_qr_success_does_not_connect_chat() -> None:
    _assert_qr_added_block_is_lazy("backend-web/app/api/routes/qr_login.py")
    _assert_qr_added_block_is_lazy("backend-web/app/api/routes/shared_scan.py")


def test_qr_success_does_not_call_token() -> None:
    for path in (
        "backend-web/app/api/routes/qr_login.py",
        "backend-web/app/api/routes/shared_scan.py",
    ):
        added = _patch_added_block(QR_PATCH, path).lower()
        assert "request_im_token" not in added
        assert "_fetch_im_token" not in added
        assert "mark_token_cache_expired" not in added


def test_qr_success_does_not_call_captcha() -> None:
    for path in (
        "backend-web/app/api/routes/qr_login.py",
        "backend-web/app/api/routes/shared_scan.py",
    ):
        added = _patch_added_block(QR_PATCH, path).lower()
        assert "captcha" not in added
        assert "slider" not in added


def test_qr_success_does_not_run_publish_preflight() -> None:
    for path in (
        "backend-web/app/api/routes/qr_login.py",
        "backend-web/app/api/routes/shared_scan.py",
    ):
        added = _patch_added_block(QR_PATCH, path).lower()
        assert "preflight" not in added
        assert "probe_account_publish_restriction" not in added


def test_chat_cache_first() -> None:
    handoff = _text(HANDOFF)
    evidence = _text(
        ROOT
        / "changes"
        / "active"
        / "CHG-0018-account-profile-publish-safety"
        / "evidence"
        / "20260816-restore-latest-upstream-chat.md"
    )
    assert "Chat semantics are lazy and cache-first" in handoff
    assert "client is cache-first and uses the existing upstream Token owner only on cache miss" in evidence
    assert "common/services/im_token_api.py" not in {
        line.removeprefix("diff --git a/").split(" b/", 1)[0]
        for line in _text(CHAT_PATCH).splitlines()
        if line.startswith("diff --git a/")
    }


def test_chat_cache_miss_uses_upstream_token_owner() -> None:
    handoff = _text(HANDOFF)
    evidence = _text(RECOVERY_EVIDENCE)
    assert "cache miss/expired: existing upstream get_or_connect" in handoff
    assert "existing upstream Local Token owner if required" in handoff
    assert "one Local Token owner call" in evidence
    assert "No second Chat state machine, Token owner, Session owner, PVR lifecycle, or verification lifecycle" in evidence


def test_fail_sys_user_validate_is_not_qr_required() -> None:
    handoff = _text(HANDOFF)
    removed = _patch_removed_block(CHAT_PATCH, "backend-web/app/services/chat_new/im_client.py")
    added = _patch_added_block(CHAT_PATCH, "backend-web/app/services/chat_new/im_client.py")
    assert "`FAIL_SYS_USER_VALIDATE` is platform verification, not QR-required evidence" in handoff
    assert "must **not** be directly mapped" in handoff
    assert "_classify_chat_readiness_failure" in removed
    assert "HUMAN_QR_REQUIRED" in removed
    assert "_classify_chat_readiness_failure" not in added


def test_normal_ws_disconnect_does_not_require_qr() -> None:
    handoff = _text(HANDOFF)
    assert "Ordinary Chat/WebSocket disconnect means reconnect, not QR" in handoff
    assert "Do not automatically escalate an ordinary disconnect to `QR_REQUIRED` or `HUMAN_QR_REQUIRED`." in handoff


def test_chat_pvr_does_not_drop_healthy_auto_reply() -> None:
    patch = _text(HUMAN_RECONNECT_PATCH)
    handoff = _text(HANDOFF)
    assert 'if self.current_token and connection_state == "connected":' in patch
    assert "Healthy Auto Reply must survive Chat authentication failure." in handoff


def test_live_ws_maintenance_does_not_refresh_token() -> None:
    patch = _text(AUTO_REPLY_PATCH)
    handoff = _text(HANDOFF)
    assert "test_38_live_websocket_token_blocks_three_minute_proactive_token_refresh" in patch
    assert "test_41_live_token_runtime_does_not_call_token_owner_from_cookie_maintenance" in patch
    assert "Live WebSocket maintenance must not cause a Token-refresh storm." in handoff


def test_chat_connect_single_flight() -> None:
    patch = _text(CHAT_PATCH)
    assert "+        self._lock = asyncio.Lock()" in patch
    assert "+        async with self._lock:" in patch


def test_qr_no_round2_auth_convergence() -> None:
    patch = _text(QR_PATCH)
    handoff = _text(HANDOFF)
    assert "-    async def converge_existing_consumers_after_login(" in patch
    assert "-    async def _converge_existing_consumers_after_login_impl(" in patch
    assert "Round2 auth convergence" in handoff
    for source_path in (
        "backend-web/app/api/routes/qr_login.py",
        "backend-web/app/api/routes/shared_scan.py",
    ):
        assert "converge_existing_consumers_after_login" not in _patch_added_block(QR_PATCH, source_path)


def test_disabled_account_isolation() -> None:
    patch = _text(PID_REAPER_PATCH)
    assert "def test_disabled_accounts_do_not_start_auto_reply" in patch
    assert "DISABLED_READ_ONLY_NO_AUTO_REPLY" in patch
    assert "def test_disabled_account_publish_is_fail_closed_before_publisher" in patch


def test_websocket_init_reaper_configuration() -> None:
    patch = _text(PID_REAPER_PATCH)
    handoff = _text(HANDOFF)
    assert "init: true" in patch
    assert "zombies" in patch.lower()
    assert "`PID1=docker-init`" in handoff
    assert "`zombies=0`" in handoff


def test_all_eight_regression_invariants_are_documented() -> None:
    handoff = _text(HANDOFF)
    for number in range(1, 9):
        assert f"REGRESSION_INVARIANT_{number:02d}" in handoff


def test_project_context_surfaces_authoritative_chat_handoff_and_runtime_state() -> None:
    state = build_project_state(ROOT)
    reading = required_reading(ROOT, state)
    authority_path = (
        "changes/active/CHG-0018-account-profile-publish-safety/runtime_authority.json"
    )
    assert "docs/AI_PROJECT_HANDOFF.md" in reading
    assert authority_path in reading
    assert reading.index("docs/AI_PROJECT_HANDOFF.md") < reading.index(
        "changes/active/CHG-0018-account-profile-publish-safety/acceptance.md"
    )
    context = render_context(ROOT)
    assert "Production runtime code base SHA: 7c4d2828f7b2c2e3f2dd6d79acfe2c9e321521ed" in context
    assert "Upstream authority SHA: bf252be357f5e4261b04ce2b7419c5574aaf1b55" in context
    assert "Current Chat architecture: LATEST_UPSTREAM_NATIVE" in context
    assert "Current Chat recovery status: PROVEN_READY_ON_REAL_CANARY" in context
    assert "QR eager Chat auth: False" in context
    assert "Auto Reply and Chat independent: True" in context
