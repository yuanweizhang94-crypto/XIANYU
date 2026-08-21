from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = Path(__file__).resolve().parents[4]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/9cbb372-chg0022-websocket-token-network-classification.patch"


def test_execution_contract_is_minimal_patch_upstream():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "MINIMAL_EXISTING_FUNCTION_TO_CHANGE=`websocket/app/services/xianyu/xianyu_async.py`" in proposal
    assert "WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false" in proposal


def test_vendor_patch_is_exact_single_file_blob_delta():
    text = PATCH.read_text(encoding="utf-8")
    assert text.count("diff --git ") == 1
    assert "diff --git a/websocket/app/services/xianyu/xianyu_async.py b/websocket/app/services/xianyu/xianyu_async.py" in text
    assert "GIT binary patch" in text
    assert "index c89e50da051f404fb14b1c289659db2d20fdde79..9cd039885cc5b89d1f38d1d37d00ec8024654d8a 100644" in text


def test_forbidden_owners_are_not_in_patch():
    text = PATCH.read_text(encoding="utf-8")
    assert "remote_token_api.py" not in text
    assert "im_token_api.py" not in text
    assert "cookie_token_manager.py" not in text


def test_production_evidence_has_executable_gate_results():
    evidence = (CHANGE / "evidence/20260821-production-closure.md").read_text(encoding="utf-8")
    assert "Token refresh/remote Token call count was zero" in evidence
    assert "cache invalidation exactly once" in evidence
    assert "remote Token calls zero" in evidence
    assert "active Token refresh calls zero" in evidence
    assert "WebSocket-only production activation" in evidence
