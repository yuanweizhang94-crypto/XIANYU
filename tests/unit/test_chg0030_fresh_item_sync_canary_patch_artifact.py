from __future__ import annotations

import hashlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-controlled-canary.patch"
FOLLOWUP_PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0030-fresh-item-sync-skipped-lock-success-guard.patch"
LOCKED_PATCH_SHA256 = "595AA68FA73505869274642E4D6FD2B12FA38BCBD5106E3B0C4D11962E6A8201"
EXPECTED_PATCH_FILES = {
    "backend-web/app/api/routes/cookies.py",
    "backend-web/app/api/routes/items.py",
    "common/schemas/item.py",
    "tests/test_chg0030_fresh_item_sync_controlled_canary.py",
}
EXPECTED_FOLLOWUP_PATCH_FILES = {
    "backend-web/app/api/routes/cookies.py",
    "backend-web/app/api/routes/items.py",
    "tests/test_chg0030_fresh_item_sync_controlled_canary.py",
}


def _patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def _followup_patch_text() -> str:
    return FOLLOWUP_PATCH.read_text(encoding="utf-8")


def _diff_paths(text: str | None = None) -> set[str]:
    paths: set[str] = set()
    for line in (text if text is not None else _patch_text()).splitlines():
        if line.startswith("diff --git "):
            fields = line.split()
            if len(fields) >= 4 and fields[3].startswith("b/"):
                paths.add(fields[3][2:])
    return paths


def _added_patch_text_for(path_fragment: str, text: str | None = None) -> str:
    in_file = False
    added_lines: list[str] = []
    for line in (text if text is not None else _patch_text()).splitlines():
        if line.startswith("diff --git "):
            in_file = path_fragment in line
            continue
        if in_file and line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
    return "\n".join(added_lines)


def _all_added_patch_text() -> str:
    return "\n".join(
        line[1:]
        for line in _patch_text().splitlines()
        if line.startswith("+") and not line.startswith("+++")
    )


def test_chg0030_patch_artifact_exists_and_is_scoped_to_existing_backend_contracts() -> None:
    assert PATCH.exists(), "CHG-0030 must package an executable vendor patch artifact"
    assert _diff_paths() == EXPECTED_PATCH_FILES
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest().upper() == LOCKED_PATCH_SHA256


def test_chg0030_followup_patch_artifact_exists_and_is_scoped() -> None:
    assert FOLLOWUP_PATCH.exists(), "CHG-0030 skipped-lock guard must be a separate follow-up artifact"
    assert _diff_paths(_followup_patch_text()) == EXPECTED_FOLLOWUP_PATCH_FILES


def test_selected_account_preflight_returns_explicit_fail_closed_item_sync_eligibility() -> None:
    cookies_added = _added_patch_text_for("backend-web/app/api/routes/cookies.py")

    assert '"item_sync"' in cookies_added
    assert '"item_sync_eligible"' in cookies_added
    assert '"fail_closed"' in cookies_added
    assert '"failure_reason"' in cookies_added
    assert '"ACCOUNT_DISABLED"' in cookies_added
    assert '"COOKIE_MISSING"' in cookies_added
    assert '"TOKEN_NOT_READY_OR_UNKNOWN"' in cookies_added
    assert '"CHECKING_STATE_UNKNOWN"' in cookies_added
    assert '"PLATFORM_VERIFICATION_UNKNOWN"' in cookies_added
    assert '"SESSION_COOKIE_LINEAGE_UNKNOWN"' in cookies_added
    assert '"mode": "SELECTED_ACCOUNT_PREFLIGHT"' in cookies_added
    assert "session_maintenance" in cookies_added
    assert "session_cookie_lineage" in cookies_added
    assert "platform_verification" in cookies_added
    assert "account.unb" not in cookies_added
    assert "get_item_list_info" not in cookies_added
    assert "fetch_all_items_from_account" not in cookies_added


def test_item_sync_route_returns_trackable_terminal_and_durable_readback_contract() -> None:
    items_added = _added_patch_text_for("backend-web/app/api/routes/items.py")
    schema_added = _added_patch_text_for("common/schemas/item.py")

    assert "request_id" in schema_added
    assert "operation_id" in items_added
    assert "uuid4" in items_added
    assert '"sync_status"' in items_added
    assert '"terminal"' in items_added
    assert '"durable_readback"' in items_added
    assert '"xy_catalog_items"' in items_added
    assert '"duplicate_count"' in items_added
    assert "select(" in items_added
    assert "func.count" in items_added
    assert "group_by" in items_added
    assert "having" in items_added
    assert "XYCatalogItem" in items_added
    assert "CHG0030_ITEM_SYNC_OPERATION_ACCEPTED" in items_added
    assert "CHG0030_ITEM_SYNC_TERMINAL_READBACK" in items_added
    assert '"retry_allowed": False' in items_added
    assert "ItemService.fetch_all_items_from_account" in items_added
    assert '"duplicate_count": 0' not in items_added
    assert '"checked": success' not in items_added


def test_patch_preserves_single_owner_and_forbidden_side_effect_boundaries() -> None:
    added = _all_added_patch_text()
    forbidden = [
        "async_playwright",
        "launch_persistent_context",
        "page.goto",
        "browser",
        "QRCode",
        "qr_login",
        "send_message",
        "batch-offline",
        "scheduler",
        "worker",
        "create_task(",
        "metadata.create_all",
        "refresh_cookie",
        "refresh_token",
    ]

    assert [term for term in forbidden if term in added] == []


def test_patch_contains_runtime_contract_tests_not_only_markdown_evidence() -> None:
    tests_added = _added_patch_text_for("tests/test_chg0030_fresh_item_sync_controlled_canary.py")

    assert "test_get_all_from_account_durable_readback_measures_db_counts" in tests_added
    assert "test_get_all_from_account_query_failure_is_terminal_unknown" in tests_added
    assert "test_item_sync_preflight_pass_requires_authoritative_facts" in tests_added
    assert "test_item_sync_preflight_fails_closed_on_unknown_lineage_or_token" in tests_added


def test_followup_patch_guards_skipped_lock_and_incomplete_full_list_success() -> None:
    followup = _followup_patch_text()
    items_added = _added_patch_text_for("backend-web/app/api/routes/items.py", followup)
    tests_added = _added_patch_text_for("tests/test_chg0030_fresh_item_sync_controlled_canary.py", followup)

    assert "OWNER_LOCK_OCCUPIED_SKIPPED" in items_added
    assert "FULL_ACTIVE_LIST_NOT_CONFIRMED" in items_added
    assert "owner_lock_skipped" in items_added
    assert "full_active_list_confirmed" in items_added
    assert 'response["success"] = False' in items_added
    assert '"retry_allowed": False' in _patch_text()
    assert '"skipped"' in items_added
    assert "test_skipped_lock_result_is_terminal_unknown_not_success" in tests_added
    assert "test_success_requires_full_active_list_confirmed" in tests_added


def test_followup_patch_exposes_platform_verification_evidence_type_without_new_owner() -> None:
    followup = _followup_patch_text()
    cookies_added = _added_patch_text_for("backend-web/app/api/routes/cookies.py", followup)

    assert '"platform_verification_evidence_type"' in cookies_added
    assert "platform_verification.get(\"evidence_type\")" in cookies_added
    assert "fetch_all_items_from_account" not in cookies_added
    assert "get_item_list_info" not in cookies_added
