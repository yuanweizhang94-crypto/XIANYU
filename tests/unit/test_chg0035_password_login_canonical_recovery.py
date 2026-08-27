from __future__ import annotations

import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0035-password-login-canonical-recovery.patch"
TARGET = "websocket/app/api/routes/password_login.py"


def _patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def _added_text() -> str:
    return "\n".join(
        line[1:]
        for line in _patch_text().splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def _removed_text() -> str:
    return "\n".join(
        line[1:]
        for line in _patch_text().splitlines()
        if line.startswith("-") and not line.startswith("---")
    )


def test_patch_is_parseable_and_scoped_to_password_login_only() -> None:
    result = subprocess.run(
        ["git", "apply", "--numstat", "--unidiff-zero", str(PATCH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )

    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    rows = [line.split("\t") for line in result.stdout.splitlines() if line.strip()]
    assert len(rows) == 1
    assert rows[0][2] == TARGET
    assert int(rows[0][0]) < 120
    assert int(rows[0][1]) < 120


def test_case_1_phone_identifier_updates_existing_canonical_account() -> None:
    added = _added_text()

    assert "canonical_account_id = str(parsed_cookies.get('unb') or '').strip()" in added
    assert "XYAccount.account_id == canonical_account_id" in added
    assert "existing_account.cookie = validated_cookies" in added
    assert "account_id=canonical_account_id" in added
    assert "account_id=account_id" not in added


def test_case_2_missing_canonical_account_creates_validated_unb_not_login_identifier() -> None:
    added = _added_text()
    removed = _removed_text()

    assert "canonical账号确实不存在时" in added
    assert "account_id=canonical_account_id" in added
    assert "unb=canonical_account_id" in added
    assert "account_id=account_id" in removed


def test_case_3_identifier_equal_to_canonical_identity_remains_compatible() -> None:
    added = _added_text()

    assert "account_id == canonical_account_id" in added
    assert "expected_authoritative_fingerprint" in added
    assert "current_fp != expected_authoritative_fingerprint" in added
    assert "密码登录结果已过期" not in added  # existing failure contract remains context, not a new bypass


def test_case_4_missing_validated_unb_fails_closed_without_phone_fallback() -> None:
    added = _added_text()

    assert "if not canonical_account_id:" in added
    assert "密码登录Cookie缺少canonical unb" in added
    assert "拒绝使用登录账号猜测account_id" in added
    assert "parsed_cookies.get('unb') or account_id" not in added
    assert "canonical_account_id = account_id" not in added


def test_case_5_duplicate_completion_is_idempotent_for_db_token_and_session_restart() -> None:
    added = _added_text()

    assert "candidate_fp = cookie_fingerprint(validated_cookies)" in added
    assert "auth_material_changed = current_fp != candidate_fp" in added
    assert "if record_changed:" in added
    assert "跳过重复DB写入" in added
    assert "if canonical_account_id and auth_material_changed:" in added
    assert "manager_already_finalized" in added
    assert "manager_current_fp == candidate_fp and task_status.get(\"running\")" in added
    assert "elif not auth_material_changed and manager_already_finalized:" in added
    assert "跳过重复Session restart" in added


def test_validated_cookie_survives_save_scope_into_cookie_manager_finalization() -> None:
    added = _added_text()

    assert "return is_new_account, canonical_account_id, validated_cookies, auth_material_changed" in added
    assert (
        "is_new_account, canonical_account_id, validated_cookies, auth_material_changed = "
        "new_loop.run_until_complete(save_to_db())"
    ) in added
    assert "manager.add_cookie(canonical_account_id, validated_cookies, user_id)" in added
    assert "manager.update_cookie(canonical_account_id, validated_cookies, user_id)" in added
    assert "password_login_sessions[session_id]['account_id'] = canonical_account_id" in added


def test_validation_failure_guard_is_preserved_before_websocket_finalization() -> None:
    added = _added_text()
    removed = _removed_text()

    assert 'if probe.get("status") != "AUTH_VALID":' not in removed
    assert "密码登录Cookie未通过Publisher-equivalent登录态验证" not in removed
    assert "manager_current_fp = cookie_fingerprint(manager.cookies.get(canonical_account_id, \"\"))" in added


def test_name_error_regression_returns_validated_cookie_into_caller_scope() -> None:
    added = _added_text()
    removed = _removed_text()

    assert "validated_cookies = str(probe.get(\"cookies_str\") or cookies_str)" not in removed
    assert "return is_new_account, canonical_account_id, validated_cookies, auth_material_changed" in added
    assert "new_loop.run_until_complete(save_to_db())" in added
    assert "manager.add_cookie(canonical_account_id, validated_cookies, user_id)" in added
    assert "manager.update_cookie(canonical_account_id, validated_cookies, user_id)" in added
    assert "try/except Exception: pass" not in added


def test_login_identifier_is_never_promoted_to_canonical_account_id() -> None:
    added = _added_text()

    forbidden = [
        "canonical_account_id = account_id",
        "canonical_account_id = account",
        "parsed_cookies.get('unb') or account_id",
        "parsed_cookies.get('unb') or account",
        "XYAccount.account_id == account_id",
    ]
    assert [term for term in forbidden if term in added] == []
