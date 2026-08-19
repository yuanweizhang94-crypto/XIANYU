from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EVIDENCE = (
    ROOT
    / "changes"
    / "active"
    / "CHG-0018-account-profile-publish-safety"
    / "evidence"
    / "20260819-auto-reply-remote-selfheal"
)
PATCH = EVIDENCE / "websocket-auto-reply-remote-selfheal.patch"
README = EVIDENCE / "README.md"
EXPECTED_PATCH_SHA256 = "a4723e6596b171e3d241d060b28b805dc69a57ad2db6383516fa8a6a974457e9"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _locked_patch_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def test_remote_selfheal_patch_hash_is_locked() -> None:
    assert _locked_patch_sha256(PATCH) == EXPECTED_PATCH_SHA256


def test_remote_selfheal_requires_safe_mtop_before_remote() -> None:
    patch = _text(PATCH)
    helper_start = patch.index("async def _try_platform_verification_remote_recovery")
    probe_index = patch.index("safe_mtop_auth_probe", helper_start)
    auth_valid_index = patch.index('auth_status != "AUTH_VALID"', probe_index)
    remote_index = patch.index("_try_remote_token_fallback", auth_valid_index)
    assert helper_start < probe_index < auth_valid_index < remote_index


def test_remote_selfheal_is_rate_limited_and_does_not_write_cookie() -> None:
    patch = _text(PATCH)
    readme = _text(README)
    assert "PLATFORM_VERIFICATION_REMOTE_RETRY_SECONDS = 180" in patch
    assert "sleep_duration = 60" in patch
    assert "authoritative Cookie is never written" in readme
    assert "Authoritative Cookie writes from this new path: 0" in readme


def test_session_expiry_and_qr_remain_fail_closed() -> None:
    patch = _text(PATCH)
    readme = _text(README)
    assert 'if auth_status == "SESSION_EXPIRED"' in patch
    assert 'return "SESSION_EXPIRED"' in patch
    assert "HUMAN_QR_REQUIRED" in readme
    assert "never reaches the remote-only path" in readme
