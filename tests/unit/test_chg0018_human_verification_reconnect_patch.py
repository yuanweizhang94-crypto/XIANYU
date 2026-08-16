from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "b75d63b-chg0018-human-verification-reconnect.patch"
EXPECTED_SHA256 = "B87532B67BDF6B7649DB4FAC85C3B5F90D0F425C699FB59E89C5A613643EF8A2"


def _text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_patch_hash_is_locked() -> None:
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest().upper() == EXPECTED_SHA256


def test_patch_changes_only_the_five_confirmed_runtime_files() -> None:
    text = _text()
    paths = [line.removeprefix("diff --git a/").split(" b/", 1)[0] for line in text.splitlines() if line.startswith("diff --git a/")]
    assert paths == [
        "common/services/cookie_renew_browser_service.py",
        "websocket/app/services/xianyu/cookie_token_manager.py",
        "websocket/app/api/routes/internal.py",
        "backend-web/app/services/websocket_client.py",
        "backend-web/app/api/routes/chat_new.py",
    ]


def test_human_entry_is_allowlisted_fixed_action() -> None:
    text = _text()
    assert '_TARGET_URL' in text
    evidence = (ROOT / "changes" / "active" / "CHG-0018-account-profile-publish-safety" / "evidence" / "20260816-x11-human-entry-auto-reply-reconnect.md").read_text(encoding="utf-8")
    assert "https://www.goofish.com/" in evidence
    assert 'get_account_browser_profile_dir(pure_user_id)' in text
    assert 'human-verification/{account_id}/open' in text
    assert 'human-verification/{account_id}/recheck' in text
    assert '_owned_chat_account(account_id, current_user, db)' in text
    assert 'ACCOUNT_DISABLED' in text
    assert 'PLATFORM_VERIFICATION_REQUIRED_STATE_REQUIRED' in text


def test_caller_has_no_generic_browser_execution_inputs() -> None:
    text = _text()
    added = "\n".join(line[1:] for line in text.splitlines() if line.startswith("+") and not line.startswith("+++"))
    for forbidden in (
        'verification_url: str',
        'profile_path',
        'browser_executable',
        'shell_command',
        'shell_args',
        'proxy: str',
        'cookie_value:',
        'token: str',
    ):
        assert forbidden not in added


def test_open_is_headed_child_only_and_does_not_flip_background_headless() -> None:
    text = _text()
    assert 'child_env["DISPLAY"] = display' in text
    assert '"host.docker.internal:0"' in text
    assert '"human_browser_visible": True' in text
    assert '"waiting_for_real_user_official_verification": True' in text
    assert 'BROWSER_HEADLESS", "").lower() == "false"' not in text


def test_profile_lock_lives_until_human_browser_exits() -> None:
    text = _text()
    wait = text.index('proc.wait()')
    release = text.index('account_browser_lock_manager.release(pure_user_id)', wait)
    slot_release = text.index('concurrency_manager.unregister_instance(pure_user_id)', wait)
    assert wait < release
    assert wait < slot_release


def test_recheck_is_explicit_one_shot_and_does_not_restart_or_auth() -> None:
    text = _text()
    assert 'sync_db_cookie_to_profile=False' in text
    assert '"websocket_restarted": False' in text
    added = "\n".join(line[1:] for line in text.splitlines() if line.startswith("+") and not line.startswith("+++"))
    for forbidden in ('request_im_token_with_fallback(', 'solve_captcha(', 'handle_captcha_verification(', 'restart_account(account_id)', 'get_or_connect(account_id)'):
        assert forbidden not in added


def test_recheck_failure_keeps_pvr_and_success_clears_it() -> None:
    text = _text()
    assert '"platform_verification_cleared": False' in text
    assert '_persist_platform_verification_marker(required=False)' in text
    assert 'metadata.pop("auto_reply_platform_verification", None)' in text


def test_live_websocket_pvr_does_not_destroy_its_current_token() -> None:
    text = _text()
    assert 'if self.current_token and connection_state == "connected":' in text
    assert 'else:\n+            self.current_token = None' in text
