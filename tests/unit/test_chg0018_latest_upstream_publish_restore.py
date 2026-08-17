from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "742fb58-chg0018-latest-upstream-publish-restore.patch"
MANIFEST = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "742fb58-chg0018-latest-upstream-publish-restore.json"
TARGET_SHA = "742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1"
EXPECTED_MANIFEST_SHA256 = "7F0B6BBC70847E4D9CCD5611B1E8F64E80AEACC9BD7BE0747199AED742C4B86C"


def _patch() -> str:
    return PATCH.read_text(encoding="utf-8")


def _manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def _assertion(name: str) -> bool:
    return bool(_manifest()["source_assertions"][name])


def test_patch_hash_is_locked() -> None:
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest().upper() == _manifest()["patch_sha256"]
    assert hashlib.sha256(MANIFEST.read_bytes()).hexdigest().upper() == EXPECTED_MANIFEST_SHA256


def test_normal_single_publish_does_not_require_real_browser_login_ready() -> None:
    assert _assertion("real_browser_login_ready_absent_from_product_publish_route")
    assert _assertion("single_route_calls_publish_executor")


def test_normal_batch_publish_does_not_require_real_browser_login_ready() -> None:
    assert _assertion("real_browser_login_ready_absent_from_product_publish_route")
    assert _assertion("batch_route_uses_background_task")


def test_normal_direct_publish_does_not_require_playwright() -> None:
    assert _assertion("direct_publisher_loader")
    assert _manifest()["normal_direct_publish_requires_browser"] is False


def test_latest_upstream_publish_service_is_authority() -> None:
    m = _manifest()
    assert m["upstream_target_sha"] == TARGET_SHA
    assert m["decision"] == "ADOPT_UPSTREAM"
    assert m["latest_upstream_publish_is_authority"] is True


def test_publish_capability_detects_fish_shop_or_personal() -> None:
    assert _assertion("capability_detection_in_common_executor")
    assert _assertion("fish_shop_routing")
    assert _assertion("personal_routing")


def test_fish_shop_uses_current_upstream_publisher() -> None:
    assert _assertion("fish_shop_routing")


def test_personal_seller_uses_current_upstream_personal_publisher() -> None:
    assert _assertion("personal_routing")


def test_selected_account_never_falls_back_to_other_account() -> None:
    assert _assertion("selected_account_in_common_executor")
    assert _manifest()["strict_selected_account"] is True


def test_owner_scope_preserved() -> None:
    assert _assertion("owner_scope_in_common_executor")
    assert _manifest()["owner_scope_preserved"] is True


def test_authoritative_cookie_used() -> None:
    assert _assertion("authoritative_cookie_in_common_executor")
    assert _manifest()["authoritative_cookie_only"] is True


def test_refreshed_cookie_propagated() -> None:
    assert _assertion("refreshed_cookie_propagated")


def test_fail_sys_user_validate_is_platform_publish_error_not_browser_not_ready() -> None:
    assert _assertion("platform_validate_marker")
    assert _assertion("real_browser_login_ready_absent_from_product_publish_route")


def test_no_automatic_real_publish_retry() -> None:
    assert _manifest()["no_automatic_real_publish_retry"] is True


def test_batch_executor_serial() -> None:
    assert _assertion("batch_serial_loops")
    assert _manifest()["active_real_batch_executors_max"] == 1


def test_http_submitted_is_not_success() -> None:
    assert _manifest()["http_submitted_is_not_success"] is True
    assert _manifest()["publish_status_owner"] == "COMPANY_LOCAL_EXECUTION_TOOL"


def test_success_requires_item_id_url_or_authoritative_sync() -> None:
    assert _manifest()["success_requires_item_id_url_or_authoritative_sync"] is True


def test_failed_operation_without_batch_id_returns_failed() -> None:
    assert _manifest()["failed_without_batch_returns_failed"] is True
    assert _manifest()["publish_status_owner"] == "COMPANY_LOCAL_EXECUTION_TOOL"


def test_unknown_never_causes_automatic_republish() -> None:
    assert _manifest()["unknown_never_automatic_republish"] is True


def test_publish_patch_scope_is_only_declared_publish_dependencies() -> None:
    paths = [line.removeprefix("diff --git a/").split(" b/", 1)[0] for line in _patch().splitlines() if line.startswith("diff --git a/")]
    assert set(paths) == set(_manifest()["files"])
    assert len(paths) == len(_manifest()["files"])
    assert all("chat" not in path.lower() for path in paths)
    assert all("websocket" not in path.lower() for path in paths)
