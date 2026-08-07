from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE = ROOT / "changes" / "active" / "CHG-0019-normal-account-offline"
SUSPENDED_18 = ROOT / "changes" / "suspended" / "CHG-0018-account-profile-publish-safety"


def test_chg0019_is_only_verifying_active_change() -> None:
    active = sorted(path.name for path in (ROOT / "changes" / "active").iterdir() if path.is_dir())
    assert active == ["CHG-0019-normal-account-offline"]
    for name in ("proposal.md", "design.md", "tasks.md", "acceptance.md"):
        text = (CHANGE / name).read_text(encoding="utf-8")
        assert "Status: VERIFYING" in text
        assert "Change ID: CHG-0019-normal-account-offline" in text


def test_chg0018_is_suspended_without_production_rollback() -> None:
    reason = (
        "Production verification complete; local closeout commit exists, but remote GitHub branch "
        "synchronization remains unresolved. Suspended to allow CHG-0019 execution. Production "
        "CHG-0018 behavior remains enabled and unchanged."
    )
    for name in ("proposal.md", "design.md", "tasks.md", "acceptance.md"):
        text = (SUSPENDED_18 / name).read_text(encoding="utf-8")
        assert "Status: SUSPENDED" in text
        assert f"SUSPEND_REASON={reason}" in text


def test_chg0019_records_normal_web_offline_safety_boundary() -> None:
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "CURRENT_BACKEND_USES_WRONG_PC_SELLER_OFFSHELF_API" in proposal
    assert "www.goofish.com/item?id=<item_id>" in proposal
    assert "mtop.alibaba.idle.seller.pc.item.batch.offline" in proposal
    assert "Old PC Seller batch-offline source is preserved and not used by the normal-account canary." in acceptance
    assert "No product delete, publish, relist, edit, polish" in acceptance
