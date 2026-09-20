from __future__ import annotations

from pathlib import Path


CHANGE = Path(__file__).resolve().parents[1]
ROOT = CHANGE.parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0039-token-invalidation-recovery.patch"


def _text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_chg0039_patch_scope_and_explicit_invalidation_gate() -> None:
    text = _text(PATCH)
    changed = [
        line.split(" b/", 1)[1]
        for line in text.splitlines()
        if line.startswith("diff --git a/")
    ]
    assert changed == ["websocket/app/services/xianyu/cookie_token_manager.py"]
    assert "explicitly_invalidated = bool(" in text
    assert "cache.expire_at == cache.renew_expire_at == cache.updated_at" in text
    assert "Token缓存存在显式失效标记，按未命中处理" in text


def test_chg0039_preserves_existing_owners_and_normal_fallback() -> None:
    text = _text(PATCH)
    proposal = _text(CHANGE / "proposal.md")
    design = _text(CHANGE / "design.md")
    assert "allow_expired=True" in text
    assert "Decision: PATCH_UPSTREAM" in proposal
    assert "GLOBAL_WEBSOCKET_RESTART=false" in proposal
    assert "No new Token owner" in design
    assert "No new WebSocket owner" in design


def test_chg0039_runtime_acceptance_remains_pending_real_inbound() -> None:
    acceptance = _text(CHANGE / "acceptance.md")
    assert "TOKEN_CHANGED=true" in acceptance
    assert "REGISTRATION_ACK=PASS" in acceptance
    assert "REAL_E2E_STABILITY=PENDING_REAL_INBOUND" in acceptance
