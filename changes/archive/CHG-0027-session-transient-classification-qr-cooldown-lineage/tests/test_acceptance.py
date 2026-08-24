from hashlib import sha256
from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[4]
CHANGE = Path(__file__).resolve().parents[1]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0027-session-transient-classification-qr-cooldown-lineage.patch"
EVIDENCE = CHANGE / "evidence/20260824-scoped-production-acceptance-and-formal-persistence.md"
EXPECTED_PATCH_SHA = "e3f42b96dd7bedc833a0e44f0397626ef48e133a57c463ae6e0ef5e193249b31"
EXPECTED_FILES = {
    "backend/backend-web/app/api/routes/chat_new.py",
    "backend/backend-web/app/api/routes/cookies.py",
    "backend/backend-web/app/services/chat_new/im_session_manager.py",
    "backend/common/utils/cookie_refresh.py",
    "scheduler/common/services/item_delete_service.py",
    "scheduler/common/services/order_service.py",
    "scheduler/common/services/rate_service.py",
    "scheduler/common/services/xianyu_mtop.py",
    "scheduler/common/utils/cookie_refresh.py",
    "scheduler/scheduler/app/services/scheduler/fetch_items_task.py",
    "scheduler/scheduler/app/services/scheduler/fetch_orders_task.py",
    "scheduler/scheduler/app/services/scheduler/login_renew_task.py",
    "scheduler/scheduler/app/services/scheduler/polish_task.py",
    "scheduler/scheduler/app/services/scheduler/rate_task.py",
    "scheduler/scheduler/app/services/scheduler/red_flower_task.py",
    "scheduler/scheduler/app/services/scheduler/redelivery_task.py",
}


def test_exact_final_patch_sha_and_component_specific_scope():
    raw = PATCH.read_bytes()
    assert sha256(raw).hexdigest() == EXPECTED_PATCH_SHA
    text = raw.decode("ascii")
    files = set(re.findall(r"^diff --git a/(.+?) b/", text, flags=re.M))
    assert files == EXPECTED_FILES
    assert raw.count(b"diff --git ") == 16
    assert raw.count(b"GIT binary patch") == 16


def test_final_patch_binary_attribute_is_locked():
    attrs = (ROOT / "vendor/patches/xianyu-auto-reply/.gitattributes").read_text(encoding="utf-8")
    assert "chg0027-session-transient-classification-qr-cooldown-lineage.patch binary" in attrs


def test_scoped_acceptance_and_followups_are_truthfully_locked():
    text = EVIDENCE.read_text(encoding="utf-8")
    for marker in (
        "CHG0027_SCOPED_PRODUCTION_ACCEPTANCE=PASS",
        "DEFECT_A_ACCEPTANCE=PASS",
        "DEFECT_B_ACCEPTANCE=PASS",
        "ACCOUNT_RUNTIME_OVERALL_ACCEPTANCE=PARTIAL__FOLLOWUP_REQUIRED",
        "PUBLISH_CAPABILITY_FINAL_ACCEPTANCE=SYNTHETIC_CAPABILITY_PASS__READINESS_CONVERGENCE_FOLLOWUP_REQUIRED",
        "WEBSITE_UI_FINAL_ACCEPTANCE=STATIC_RUNTIME_WIRING_PASS__REAL_BROWSER_RENDER_BLOCKED",
        "FOLLOWUP_DEFECTS_EXPLICITLY_PERSISTED=true",
    ):
        assert marker in text
    assert "ACCOUNT_RUNTIME_OVERALL_ACCEPTANCE=PASS" not in text
    assert "WEBSITE_UI_FINAL_ACCEPTANCE=PASS" not in text


def test_runtime_matrix_and_no_side_effect_boundary_are_locked():
    text = EVIDENCE.read_text(encoding="utf-8")
    for marker in (
        "ZHOUZHOU_CURRENT_COOKIE_VALIDATION=AUTH_VALID",
        "ZHOUZHOU_SESSION_EXPIRED_EXPLICIT_EVIDENCE=false",
        "ZHOUZHOU_FALSE_SESSION_EXPIRED_FIXED=true",
        "MINGSHUAI_SESSION_STUCK=false",
        "HUAWEI_SESSION_STUCK=false",
        "YILONG_SESSION_STUCK=false",
        "STUCK_SESSION_CHECKING_COUNT=0",
        "REAL_MESSAGES_SENT=0",
        "REAL_PRODUCTS_PUBLISHED=0",
        "REAL_PRODUCTS_MODIFIED=0",
        "NEW_ITEM_SYNC_INVOCATION_COUNT=0",
    ):
        assert marker in text


def test_deterministic_lineage_and_replay_gates_are_locked():
    text = EVIDENCE.read_text(encoding="utf-8")
    for marker in (
        "CHG0027_DETERMINISTIC_TESTS=18/18_PASS",
        "CHG0026_RELEVANT_REGRESSION=45/45_PASS",
        "BACKEND_COOKIE_REFRESH_PREIMAGE_SHA256=eb9f4abdc03ac6f2852d8efd3e1b4523fc502e0374d507f0f42c445ca31d9d65",
        "SCHEDULER_COOKIE_REFRESH_PREIMAGE_SHA256=829810f1183a281cd94b2d239be188a8cd1b82a31e5437403a8357259063ed04",
        "PRE_EXISTING_RUNTIME_PY_DRIFT_COUNT=19",
        "PRESERVE_COMPONENT_SPECIFIC_PREIMAGE=true",
        "PATCH_APPLY_CHECK=PASS",
        "PATCH_CLEAN_APPLY=PASS",
        "PATCH_REPLAY_POSTIMAGE_MATCH=true",
        "NON_CHG0027_HUNKS=0",
    ):
        assert marker in text
