from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE = ROOT / "changes/archive/CHG-0035-password-login-canonical-recovery"
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0035-password-login-canonical-recovery.patch"


def test_chg0035_active_change_declares_fixed_repair_scope() -> None:
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")

    assert "TASK_TYPE=REPAIR" in proposal
    assert "MINIMAL_EXISTING_FUNCTION_TO_CHANGE=websocket/app/api/routes/password_login.py::_save_login_result" in proposal
    assert "another password login" in proposal
    assert "Canonical `account_id` must be the validated platform `unb`" in acceptance


def test_chg0035_patch_artifact_exists_and_is_single_owner_delta() -> None:
    text = PATCH.read_text(encoding="utf-8")

    assert text.count("diff --git ") == 1
    assert "websocket/app/api/routes/password_login.py" in text
    assert "canonical_account_id" in text
    assert "manager_already_finalized" in text
    assert "canonical_account_id = account_id" not in text
