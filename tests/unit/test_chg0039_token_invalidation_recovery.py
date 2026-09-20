from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0039-token-invalidation-recovery.patch"
CHANGE = ROOT / "changes/active/CHG-0039-token-invalidation-recovery"


def patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_patch_targets_only_existing_token_cache_owner():
    text = patch_text()
    assert text.count("diff --git ") == 1
    assert (
        "diff --git a/websocket/app/services/xianyu/cookie_token_manager.py "
        "b/websocket/app/services/xianyu/cookie_token_manager.py"
    ) in text
    assert "auto_reply_service.py" not in text
    assert "xianyu_async.py" not in text
    assert "frontend/" not in text


def test_explicit_invalidation_marker_wins_over_expired_fallback():
    text = patch_text()
    assert "explicitly_invalidated = bool(" in text
    assert "cache.expire_at == cache.renew_expire_at == cache.updated_at" in text
    assert "Token缓存存在显式失效标记，按未命中处理" in text
    assert "return None" in text
    removed = [
        line
        for line in text.splitlines()
        if line.startswith("-") and not line.startswith("---")
    ]
    assert removed == []


def test_natural_expired_cache_fallback_is_not_removed():
    text = patch_text()
    design = (CHANGE / "design.md").read_text(encoding="utf-8")
    assert "allow_expired=True" in text
    assert "Preserve natural allow_expired startup fallback unchanged." in design
    removed = [
        line
        for line in text.splitlines()
        if line.startswith("-") and not line.startswith("---")
    ]
    assert removed == []


def test_change_contract_is_account_level_and_not_global():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    design = (CHANGE / "design.md").read_text(encoding="utf-8")
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "GLOBAL_TOKEN_INVALIDATION=false" in proposal
    assert "GLOBAL_WEBSOCKET_RESTART=false" in proposal
    assert "No new Token owner" in design
    assert "No new WebSocket owner" in design
