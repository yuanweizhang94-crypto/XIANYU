from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/9cbb372-chg0022-websocket-token-network-classification.patch"
CHANGE = ROOT / "changes/active/CHG-0022-websocket-token-network-classification"


def patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_patch_targets_existing_websocket_owner_only():
    text = patch_text()
    assert text.count("diff --git ") == 1
    assert "diff --git a/websocket/app/services/xianyu/xianyu_async.py b/websocket/app/services/xianyu/xianyu_async.py" in text
    assert "remote_token_api.py" not in text
    assert "im_token_api.py" not in text
    assert "cookie_token_manager.py" not in text


def test_patch_is_exact_git_binary_blob_delta():
    text = patch_text()
    assert "GIT binary patch" in text
    assert "index c89e50da051f404fb14b1c289659db2d20fdde79..9cd039885cc5b89d1f38d1d37d00ec8024654d8a 100644" in text


def test_change_contract_keeps_network_auth_scope_minimal():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "MINIMAL_EXISTING_FUNCTION_TO_CHANGE=`websocket/app/services/xianyu/xianyu_async.py` existing reconnect exception branch only." in proposal
    assert "WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false" in proposal
    assert "FORBIDDEN_CHANGE_SCOPE=Token TTL" in proposal


def test_production_evidence_records_executable_network_recovery():
    evidence = (CHANGE / "evidence/20260821-production-closure.md").read_text(encoding="utf-8")
    assert "pre-connect DNS/gaierror entered the network path" in evidence
    assert "Token refresh/remote Token call count was zero" in evidence
    assert "the next connection succeeded with the same Token" in evidence


def test_production_evidence_records_bounded_explicit_auth_rejection():
    evidence = (CHANGE / "evidence/20260821-production-closure.md").read_text(encoding="utf-8")
    assert "two Token attempts total (initial + one bounded expiry retry)" in evidence
    assert "cache invalidation exactly once" in evidence
    assert "network-backoff path false" in evidence


def test_qr_and_maintenance_invariants_are_recorded():
    evidence = (CHANGE / "evidence/20260821-production-closure.md").read_text(encoding="utf-8")
    assert "remote Token calls zero" in evidence
    assert "password login calls zero" in evidence
    assert "CAPTCHA calls zero" in evidence
    assert "existing Token reused" in evidence
    assert "active Token refresh calls zero" in evidence
