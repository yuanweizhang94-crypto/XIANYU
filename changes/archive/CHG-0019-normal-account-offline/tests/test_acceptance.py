from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
CHANGE = ROOT / "changes" / "archive" / "CHG-0019-normal-account-offline"
ARCHIVED_18 = ROOT / "changes" / "archive" / "CHG-0018-account-profile-publish-safety"
ARCHIVED_17 = ROOT / "changes" / "archive" / "CHG-0017-upstream-native-auto-ai-delivery"


def project_state() -> dict[str, object]:
    return json.loads((ROOT / "generated" / "PROJECT_STATE.json").read_text(encoding="utf-8"))


def test_chg0019_is_archived_after_main_merge() -> None:
    active_root = ROOT / "changes" / "active"
    active = sorted(path.name for path in active_root.iterdir() if path.is_dir()) if active_root.exists() else []
    assert active == []
    for name in ("proposal.md", "design.md", "tasks.md", "acceptance.md"):
        text = (CHANGE / name).read_text(encoding="utf-8")
        assert "Status: ARCHIVED" in text
        assert "Change ID: CHG-0019-normal-account-offline" in text

    state = project_state()
    assert state["active_change"] is None
    assert state["tasks"]["total"] == 0
    assert state["tasks"]["completed"] == 0
    assert state["tasks"]["next_task"] is None
    assert state["tasks"]["items"] == []
    assert "suspended_changes" not in state


def test_predecessors_remain_archived_after_main_integration() -> None:
    assert ARCHIVED_17.is_dir()
    assert ARCHIVED_18.is_dir()

    chg17_tasks = (ARCHIVED_17 / "tasks.md").read_text(encoding="utf-8")
    assert "Status: ARCHIVED" in chg17_tasks
    assert "- [x] T17 Archive and deliver." in chg17_tasks

    for name in ("proposal.md", "design.md", "tasks.md", "acceptance.md"):
        text = (ARCHIVED_18 / name).read_text(encoding="utf-8")
        assert "Status: ARCHIVED" in text
        assert "Change ID: CHG-0018-account-profile-publish-safety" in text


def test_chg0019_records_normal_web_offline_safety_boundary() -> None:
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "CURRENT_BACKEND_USES_WRONG_PC_SELLER_OFFSHELF_API" in proposal
    assert "www.goofish.com/item?id=<item_id>" in proposal
    assert "mtop.alibaba.idle.seller.pc.item.batch.offline" in proposal
    assert "Old PC Seller batch-offline source is preserved and not used by the normal-account canary." in acceptance
    assert "No product delete, publish, relist, edit, polish" in acceptance


def test_current_main_integration_patch_is_preserved() -> None:
    patch = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "4c5e1ac-chg0019-main-integration-after-chg0018-t12.patch"
    assert patch.is_file()
