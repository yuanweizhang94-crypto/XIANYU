from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/742fb58-chg0018-item-platform-status-publish-session-followup.patch"
MANIFEST = ROOT / "vendor/patches/xianyu-auto-reply/742fb58-chg0018-item-platform-status-publish-session-followup.json"


def test_followup_patch_manifest_hash_matches() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    canonical = PATCH.read_bytes().replace(b"\r\n", b"\n")
    actual = hashlib.sha256(canonical).hexdigest().upper()
    assert actual == manifest["sha256"]
    assert manifest["temporary_text_edit_included"] is False


def test_followup_patch_requires_raw_platform_status_zero_for_active() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    assert 'normalized_raw_status == "0"' in patch
    assert '"platform_status_reason": "seen_with_active_raw_item_status"' in patch
    assert 'raw_platform_item_status_not_active:' in patch
    assert '"last_seen_active_at": None' in patch


def test_followup_patch_restores_read_only_status_probe_without_old_browser_owner() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    assert "async def probe_account_publish_restriction(" in patch
    assert "detect_publish_account_capability(" in patch
    assert '"probe_mode": "READ_ONLY"' in patch
    assert '"real_products_published": 0' in patch
    assert "preflight_only=True" not in patch


def test_followup_patch_fixes_all_three_undefined_session_refreshes() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    assert patch.count("await session.refresh(account)") == 3
    assert patch.count("await self.session.refresh(account)") == 3


def test_followup_patch_does_not_persist_temporary_text_editor() -> None:
    patch = PATCH.read_text(encoding="utf-8")
    assert "edit_personal_item_text" not in patch
    assert 'items/{item_id}/text' not in patch
