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
    / "20260819-qr-password-refresh-terminal-guard"
)
PATCH = EVIDENCE / "qr-password-refresh-terminal-guard.patch"
README = EVIDENCE / "README.md"
EXPECTED_PATCH_SHA256 = "f8f318a6ef8278d9c955d1a6d3dfc924add622764ded95261eb09e184db8a9c4"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _locked_patch_sha256(path: Path) -> str:
    data = path.read_bytes().replace(b"\r\n", b"\n").replace(b"\r", b"\n")
    return hashlib.sha256(data).hexdigest()


def test_qr_password_refresh_guard_patch_hash_is_locked() -> None:
    assert _locked_patch_sha256(PATCH) == EXPECTED_PATCH_SHA256


def test_qr_guard_precedes_processing_and_background_login() -> None:
    patch = _text(PATCH)
    predicate = patch.index("is_human_qr_required_for_cookie")
    terminal_return = patch.index('"status": "human_qr_required"', predicate)
    processing = patch.index("password_login_state.start_processing", terminal_return)
    assert predicate < terminal_return < processing


def test_qr_guard_uses_authoritative_cookie_fingerprint_predicate() -> None:
    patch = _text(PATCH)
    assert "account.metadata_json" in patch
    assert 'account.cookie or ""' in patch
    assert '"message": "HUMAN_QR_REQUIRED"' in patch


def test_followup_preserves_existing_recovery_owner() -> None:
    readme = _text(README)
    assert "no new login service" in readme.lower()
    assert "When the authoritative Cookie changes" in readme
    assert "_standalone_password_login = not reached" in readme
