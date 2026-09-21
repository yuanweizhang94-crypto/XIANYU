from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = CHANGE.parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0041-native-chat-runtime-equivalence.patch"


def test_chg0041_runtime_equivalence_contract():
    patch = PATCH.read_text(encoding="utf-8")
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "manager.instances.get(account_id)" in patch
    assert "async def _chat_lwp_request" in patch
    assert "PATCH_REMOVED_LINE_COUNT=0" in acceptance
    assert "CHG0039_RUNTIME_CANDIDATE_MATCH=true" in acceptance


def test_chg0041_does_not_reimplement_enable_lifecycle():
    patch = PATCH.read_text(encoding="utf-8")
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "_update_account_status_and_task" not in patch
    assert "ACCOUNT_ENABLE_RUNTIME_REHYDRATION_MISSING is NOT" not in patch
    assert "CURRENT_RUNTIME_CAPABILITY=STALE_ONLY" in proposal
