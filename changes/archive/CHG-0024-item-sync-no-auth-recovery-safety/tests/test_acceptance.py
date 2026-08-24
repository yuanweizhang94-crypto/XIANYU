from hashlib import sha256
from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
PROPOSAL = CHANGE / "proposal.md"
DESIGN = CHANGE / "design.md"
ACCEPTANCE = CHANGE / "acceptance.md"
EVIDENCE = CHANGE / "evidence/20260823-item-sync-no-auth-recovery-capability-audit.md"
RECONCILIATION = CHANGE / "evidence/20260823-source-preimage-authority-reconciliation.md"
IMPLEMENTATION = CHANGE / "evidence/20260823-implementation-and-deterministic-tests.md"
RUNTIME_ACCEPTANCE = CHANGE / "evidence/20260823-runtime-acceptance.md"
ROOT = Path(__file__).resolve().parents[4]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0024-item-sync-no-auth-recovery-safety.patch"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_existing_owner_only_and_reuse_decision_are_locked():
    proposal = read(PROPOSAL)
    design = read(DESIGN)
    assert "CURRENT_ITEM_SYNC_OWNER=`ItemService.fetch_all_items_from_account`" in proposal
    assert "REUSE_DECISION=PATCH_EXISTING_OWNER" in proposal
    assert "EXISTING_OWNER_ONLY=true" in design
    assert "NO_DUPLICATE_OWNER=true" in design


def test_both_auth_recovery_callsites_are_locked():
    proposal = read(PROPOSAL)
    evidence = read(EVIDENCE)
    for text in (proposal, evidence):
        assert "AUTH_RECOVERY_CALLSITE_COUNT=2" in text
        assert "CALLSITE_1=FIRST_PAGE_CATALOG_FAILURE" in text
        assert "CALLSITE_2=MISSING_ITEM_AUTHORITATIVE_RECONCILIATION" in text


def test_default_and_public_caller_contract_are_locked():
    design = read(DESIGN)
    acceptance = read(ACCEPTANCE)
    assert "DEFAULT_BEHAVIOR_PRESERVED=true" in design
    assert "PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false" in design
    assert "DEFAULT_BEHAVIOR_PRESERVED=true" in acceptance
    assert "PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false" in acceptance


def test_remote_listing_mutation_and_unknown_retry_are_forbidden():
    proposal = read(PROPOSAL)
    acceptance = read(ACCEPTANCE)
    assert "REMOTE_LISTING_MUTATION_FORBIDDEN=true" in proposal
    assert "UNKNOWN_NEVER_BLIND_RETRY=true" in proposal
    assert "REMOTE_LISTING_MUTATION_FORBIDDEN=true" in acceptance
    assert "UNKNOWN_NEVER_BLIND_RETRY=true" in acceptance


def test_source_preimage_reconciliation_is_locked():
    text = read(RECONCILIATION)
    assert "SOURCE_PREIMAGE_AUTHORITY_RECONCILED=true" in text
    assert "OLD_AUDIT_HASH_CLASSIFICATION=STALE_AUDIT_PREIMAGE" in text
    assert "AUTHORITATIVE_ITEM_ROUTE_SHA256=`5be558b4c01cc14b99a88dde19c8f8a9c2f890aedbd132f0bc97dbf464a5d78a`" in text
    assert "AUTHORITATIVE_ITEM_SERVICE_SHA256=`5a875adc11adb6b19320206a4e9c34cd63453f9c5f35be482bf055574325b517`" in text
    assert "AUTH_RECOVERY_CALLSITE_COUNT=2" in text


def test_exact_vendor_patch_and_postimage_proof_are_locked():
    raw = PATCH.read_bytes()
    assert sha256(raw).hexdigest() == "3a34f322be2cd18c789907ba48bc381a76ac513c00a9cfc102aa0252be759471"
    assert raw.count(b"GIT binary patch") == 2
    assert raw.count(b"diff --git ") == 2
    text = raw.decode("ascii")
    assert "backend-web/app/api/routes/items.py" in text
    assert "common/services/item_service.py" in text
    for forbidden in ("cookies.py", "cookie_refresh.py", "xianyu_async.py", "chat_new.py", "publisher", "scheduler"):
        assert forbidden not in text


def test_t2_t4_behavior_and_persistence_results_are_recorded_without_live_claims():
    text = read(IMPLEMENTATION)
    acceptance = read(ACCEPTANCE)
    assert "SAFE_MODE_NAME=`no_auth_recovery`" in text
    assert "CHG0024_POSTIMAGE_BEHAVIOR_TESTS=`7/7_PASS`" in text
    assert "PATCH_CLEAN_APPLY=PASS" in text
    assert "PATCH_REPLAY_POSTIMAGE_MATCH=true" in text
    assert "PUBLIC_TOOL_SCHEMA_CHANGED=false" in text
    assert "PRODUCTION_RUNTIME_SOURCE_CHANGED=true_VERIFIED_CHG0024_CANDIDATE" in acceptance
    assert "COMPANY_RUNTIME_SOURCE_CHANGED=true_VERIFIED_T5_MAPPING" in acceptance


def test_t5_t8_runtime_acceptance_is_locked():
    text = read(RUNTIME_ACCEPTANCE)
    acceptance = read(ACCEPTANCE)
    for marker in (
        "CHG0024_RUNTIME_ACCEPTANCE=PASS",
        "ITEM_SYNC_BUSINESS_INVOCATION_COUNT=1",
        "ITEM_SYNC_RESULT=SUCCESS",
        "ITEM_SYNC_SESSION_MAINTAIN_COUNT=0",
        "ITEM_SYNC_SESSION_RENEW_COUNT=0",
        "ITEM_SYNC_COOKIE_REFRESH_COUNT=0",
        "ITEM_SYNC_TOKEN_REFRESH_COUNT=0",
        "ITEM_SYNC_PASSWORD_LOGIN_COUNT=0",
        "ITEM_SYNC_QR_ACTION_COUNT=0",
        "REMOTE_LISTING_CREATE_COUNT=0",
        "REMOTE_LISTING_EDIT_COUNT=0",
        "REMOTE_LISTING_DELETE_COUNT=0",
        "REMOTE_PRICE_CHANGE_COUNT=0",
        "REMOTE_STOCK_CHANGE_COUNT=0",
        "REMOTE_PUBLISH_COUNT=0",
        "NEGATIVE_CONTROL_2221422775489_AFTER_SYNC=`HUMAN_QR_REQUIRED`",
        "NEGATIVE_CONTROL_2221501265279_AFTER_SYNC=`HUMAN_QR_REQUIRED`",
        "QR_FALSE_GREEN_COUNT=0",
        "REAL_MESSAGES_SENT=0",
    ):
        assert marker in text
    assert "CHG0024_RUNTIME_ACCEPTANCE=PASS" in acceptance
    assert "QR_RESTORATION_NOT_YET_PERFORMED=true" in acceptance
