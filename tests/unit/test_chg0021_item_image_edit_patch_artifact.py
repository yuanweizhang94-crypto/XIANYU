from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/742fb58-chg0021-zidongzhua-item-image-edit.patch"
EXPECTED_SHA256 = "C4BD334F9CAA4AC2BDE156440544D5C5A817B8E2665CB3E5A597F0135A3170B7"


def test_chg0021_patch_hash_is_locked() -> None:
    assert PATCH.exists()
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest().upper() == EXPECTED_SHA256


def test_chg0021_patch_reuses_official_existing_item_edit_path() -> None:
    text = PATCH.read_text(encoding="utf-8")
    assert 'EDIT_DETAIL_API = "mtop.idle.pc.idleitem.editDetail"' in text
    assert 'EDIT_API = "mtop.idle.pc.idleitem.edit"' in text
    assert "upload_publish_image(" in text
    assert "retry_network_errors=False" in text
    assert "authoritative_readback_confirmed" in text
    assert '_image_compare_key' in text
    assert 'alicdn.com/' in text


def test_chg0021_patch_is_image_only_and_fail_closed() -> None:
    text = PATCH.read_text(encoding="utf-8")
    assert '@router.post("/items/{item_id}/images"' in text
    assert '@router.get("/items/{item_id}/images"' in text
    assert '"imageInfoDOList"' in text
    assert 'UNKNOWN' in text
    assert '禁止自动重试' in text
    assert '/static/uploads/products/' in text
    assert '当前图片编辑薄适配仅支持普通卖家账号' in text
    assert 'execute_single_publish' not in text
    assert 'SliderHandler' not in text
