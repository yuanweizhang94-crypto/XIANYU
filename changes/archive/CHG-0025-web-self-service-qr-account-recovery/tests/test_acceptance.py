from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[4]
CHANGE = Path(__file__).resolve().parents[1]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0025-web-self-service-qr-account-recovery.patch"
EXPECTED_PATCH_SHA = "f3ecaf30603ec593521fcc84b0cce5dac92d0da45da0514ddcf8d577ab6fe8e8"
EXPECTED_FILES = {
    "backend-web/app/api/routes/qr_login.py",
    "frontend/src/api/accounts.ts",
    "frontend/src/pages/accounts/Accounts.tsx",
    "frontend/src/types/index.ts",
}


def patch_text():
    return PATCH.read_text(encoding="utf-8", errors="replace")


def test_exact_patch_sha():
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest() == EXPECTED_PATCH_SHA


def test_patch_scope_is_exactly_four_owner_ui_files():
    files = set(re.findall(r"^diff --git a/(.+?) b/", patch_text(), flags=re.M))
    assert files == EXPECTED_FILES


def test_backend_account_scope_contract_persisted():
    text = patch_text()
    for marker in ["SESSION_TARGET_ACCOUNT", "target_account_id", "QR_IDENTITY_TARGET_MISMATCH"]:
        assert marker in text
    added = "\n".join(line[1:] for line in text.splitlines() if line.startswith("+") and not line.startswith("+++"))
    assert "SESSION_OWNER.get(session_id, current_user.id)" not in added


def test_frontend_account_scoped_generate_persisted():
    text = patch_text()
    assert "generateQRLogin" in text
    assert "target_account_id" in text


def test_no_new_owner_files_in_patch():
    text = patch_text()
    assert "app/services/qr_login" not in text
    assert "common/services" not in text
    assert "websocket/" not in text


def test_deterministic_evidence_is_green_without_real_qr():
    text = (CHANGE / "evidence/20260823-deterministic-tests-and-exact-patch-replay.md").read_text(encoding="utf-8")
    for marker in [
        "BACKEND_DETERMINISTIC_TESTS=10/10_PASS",
        "FRONTEND_DETERMINISTIC_TESTS=18/18_PASS",
        "PATCH_REPLAY_POSTIMAGE_MATCH=true",
        "REAL_QR_CREATE_COUNT=0",
        "REAL_QR_SCAN_COUNT=0",
    ]:
        assert marker in text


def test_source_authority_stays_locked():
    text = (CHANGE / "evidence/20260823-source-authority-reconciliation.md").read_text(encoding="utf-8")
    assert "FRONTEND_CURRENT_PRODUCTION_SOURCE_AUTHORITY_PROVEN=true" in text
    assert "BACKEND_QR_ROUTE_PREIMAGE_AUTHORITY_PROVEN=true" in text


def test_exactly_once_item_sync_lock_persisted():
    text = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "TOTAL_NEW_T7_ITEM_SYNC_BUSINESS_INVOCATIONS=1_REQUIRED" in text
    assert "ADDITIONAL_ITEM_SYNC_INVOCATIONS=0_REQUIRED" in text
