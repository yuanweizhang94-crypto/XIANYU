from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/4c5e1ac-chg0020-zidongzhua-market-search.patch"
EXPECTED_SHA256 = "11663707335712BF39748460A44D932BC67384C9E11D0F2AB47CB3A00328800D"


def test_chg0020_patch_hash_is_locked() -> None:
    assert PATCH.exists()
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest().upper() == EXPECTED_SHA256


def test_chg0020_patch_reuses_native_search_and_fails_closed() -> None:
    text = PATCH.read_text(encoding="utf-8")
    assert "common.services.xianyu_search_client import XianyuSearchClient, parse_search_item" in text
    assert '@router.post("/market-items")' in text
    assert "PLATFORM_VERIFICATION_REQUIRED" in text
    assert "FAIL_CLOSED_NO_ACCOUNT_SWITCH" in text
    assert "XianyuSearchClient(" in text
    assert "client.search(" in text
    assert "SliderHandler" not in text
    assert "GoofishCompassService" not in text
    assert "handle_verification" not in text


def test_chg0020_patch_sanitizes_native_raw_data() -> None:
    text = PATCH.read_text(encoding="utf-8")
    assert '"want_count": parsed.get("want_count")' in text
    assert '"view_count": None' in text
    assert '"raw_main"' not in text
    assert '"cookie":' not in text
    assert '"token":' not in text
    assert '"password":' not in text
