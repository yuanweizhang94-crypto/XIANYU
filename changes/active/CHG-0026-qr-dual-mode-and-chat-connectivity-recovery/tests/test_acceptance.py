from hashlib import sha256
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[4]
CHANGE = Path(__file__).resolve().parents[1]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0026-qr-dual-mode-and-chat-connectivity-recovery.patch"
EVIDENCE = CHANGE / "evidence/20260824-r5-production-acceptance-and-final-persistence.md"
EXPECTED_PATCH_SHA = "405b762c1fa0256ed5cad80bc1170c771549c2026e6abf69b7ae0805027619e4"
EXPECTED_FILES = {
    "backend-web/_bootstrap.py",
    "backend-web/app/api/routes/chat_new.py",
    "backend-web/app/api/routes/cookies.py",
    "backend-web/app/api/routes/qr_login.py",
    "backend-web/app/services/account_service.py",
    "backend-web/app/services/chat_new/im_client.py",
    "backend-web/app/services/chat_new/im_session_manager.py",
    "common/utils/platform_verification_status.py",
    "frontend/src/api/accounts.ts",
    "frontend/src/api/chatNew.ts",
    "frontend/src/pages/accounts/Accounts.tsx",
    "frontend/src/pages/chat-new/ChatNew.tsx",
}

def test_exact_final_patch_sha_and_scope():
    raw = PATCH.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_PATCH_SHA
    text = raw.decode("ascii")
    files = set(re.findall(r"^diff --git a/(.+?) b/", text, flags=re.M))
    assert files == EXPECTED_FILES
    assert raw.count(b"diff --git ") == 12
    assert raw.count(b"GIT binary patch") == 12

def test_final_patch_binary_attribute_is_locked():
    attrs = (ROOT / "vendor/patches/xianyu-auto-reply/.gitattributes").read_text(encoding="utf-8")
    assert "chg0026-qr-dual-mode-and-chat-connectivity-recovery.patch binary" in attrs

def test_production_acceptance_truth_is_locked():
    text = EVIDENCE.read_text(encoding="utf-8")
    for marker in (
        "PRODUCTION_ACCEPTANCE_FINAL=PASS",
        "CHAT_RUNTIME_SELF_REHYDRATING=true",
        "SESSION_PENDING_CANNOT_FALSE_GREEN=true",
        "PLATFORM_VERIFICATION_REQUIRES_EXPLICIT_EVIDENCE=true",
        "PLATFORM_VERIFICATION_ACCOUNT_SCOPE_STRICT=true",
        "NO_CROSS_ACCOUNT_VERIFICATION_STATE_LEAK=true",
        "R5_STARTUP_CHAT_AUTH_WRITE_COUNT=0",
        "WANGXIA_REGRESSION=false",
        "OUYANG_ACCEPTANCE=PASS",
        "YILONG_ACCEPTANCE=PASS",
        "WANZI_ACCEPTANCE=PASS",
        "ZHOUZHOU_FALSE_ONLINE=false",
    ):
        assert marker in text

def test_deterministic_and_replay_gates_are_locked():
    text = EVIDENCE.read_text(encoding="utf-8")
    for marker in (
        "CHG0026_DETERMINISTIC_TESTS=45/45_PASS",
        "CHG0023_REGRESSION=5/5_PASS",
        "CHG0024_REGRESSION=8/8_PASS",
        "CHG0025_REGRESSION=8/8_PASS",
        "PATCH_APPLY_CHECK=PASS",
        "PATCH_CLEAN_APPLY=PASS",
        "PATCH_REPLAY_POSTIMAGE_MATCH=true",
        "NON_CHG0026_HUNKS=0",
    ):
        assert marker in text

def test_execution_deviations_are_not_hidden():
    text = EVIDENCE.read_text(encoding="utf-8")
    assert "R3_SAME_IMAGE_ACCIDENTAL_RESTART_COUNT=5" in text
    assert "R3_ACCEPTANCE_INVALIDATED=true" in text
    assert "R5_SAME_IMAGE_ACCIDENTAL_RESTART_COUNT=4" in text
    assert "R5_EARLIER_ACCEPTANCE_INVALIDATED=true" in text

def test_historical_yilong_uncertainty_is_explicit_and_non_blocking():
    text = EVIDENCE.read_text(encoding="utf-8")
    assert "YILONG_INITIAL_PVR_PRODUCER=HISTORICAL_FIRST_EVENT_NOT_FULLY_RECONSTRUCTABLE" in text
    assert "YILONG_PLATFORM_VERIFICATION_REQUIRED=false" in text
    assert "YILONG_EXPLICIT_PLATFORM_CHALLENGE_PRESENT=false" in text
