from __future__ import annotations

import re
from pathlib import Path


CHANGE_ID = "CHG-0034-fixed-target-browser-ui"
FINAL_PASS = "PASS_WITH_NONFATAL_CHART_WARNINGS"
HISTORICAL_BLOCKER = "HUMAN_BLOCKED_EXTERNAL_CAPTCHA_NETWORK"


def _repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "AGENTS.md").exists() and (parent / "changes").exists():
            return parent
    raise AssertionError("repository root not found")


def _change_dir() -> Path:
    root = _repo_root()
    for base in (root / "changes" / "active", root / "changes" / "archive"):
        candidate = base / CHANGE_ID
        if candidate.exists():
            return candidate
    raise AssertionError(f"{CHANGE_ID} not found")


def _text(name: str) -> str:
    return (_change_dir() / name).read_text(encoding="utf-8")


def _closure() -> str:
    return _evidence("20260826-authenticated-browser-ui-acceptance.md")


def _historical_captcha_checkpoint() -> str:
    return _evidence("20260825-final-browser-ui-captcha-network-blocker.md")


def _evidence(name: str) -> str:
    return (
        _change_dir()
        / "evidence"
        / name
    ).read_text(encoding="utf-8")


def test_chg0034_records_final_authenticated_pass_as_primary_outcome() -> None:
    combined = "\n".join(
        _text(name)
        for name in ("proposal.md", "design.md", "tasks.md", "acceptance.md")
    )
    closure = _closure()

    assert "Status: ARCHIVED" in _text("proposal.md")
    assert "Status: ARCHIVED" in _text("design.md")
    assert "Status: ARCHIVED" in _text("tasks.md")
    assert "Status: ARCHIVED" in _text("acceptance.md")
    assert FINAL_PASS in combined
    assert FINAL_PASS in closure
    assert HISTORICAL_BLOCKER not in closure
    assert "USER_AUTHENTICATED_SESSION_AVAILABLE=true" in combined
    assert "USER_AUTHENTICATED_SESSION_AVAILABLE=true" in closure
    assert "AGENT_CREATED_AUTHENTICATED_SESSION=false" in combined
    assert "NO_BUSINESS_CODE_DEFECT_PROVEN=true" in combined
    assert "BUSINESS_RUNTIME_PATCHES=0" in combined
    assert "SECOND_OWNER_CREATED=false" in combined
    assert "CREDENTIAL_FAILURE_CLASSIFICATION=false" in combined


def test_chg0034_records_fixed_target_runtime_and_assets() -> None:
    acceptance = _text("acceptance.md")
    closure = _closure()
    combined = acceptance + "\n" + closure

    for marker in (
        "FIXED_TARGET_URL=http://127.0.0.1:19000/",
        "DOCUMENT_TITLE=闲鱼自动回复管理系统",
        "RUNTIME_MAIN_BUNDLE_SHA256=86f8d7b597ceafdcc20a36f59a4834a2f2932d05fa054a98410f9c529e714d6f",
        "RUNTIME_CSS_SHA256=ce943d8848b339c7c2ae380a2d7f50ff3ad25dd53581421c4d8a9464699124f3",
        "FRONTEND_IMAGE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2",
        "BACKEND_IMAGE=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2",
        "WEBSOCKET_IMAGE=xianyu-chg0023-websocket:readiness-contract-20260822-r1",
    ):
        assert marker in combined


def test_chg0034_records_authenticated_page_counts_and_statuses() -> None:
    combined = _text("acceptance.md") + "\n" + _closure()

    for marker in (
        "AUTHENTICATED_PAGES_ENTERED=8",
        "DASHBOARD_NONBLANK=true",
        "DASHBOARD_ACCOUNT_COUNT=12",
        "DASHBOARD_ENABLED_ACCOUNT_COUNT=9",
        "DASHBOARD_ONLINE_ACCOUNT_COUNT=9",
        "DASHBOARD_TODAY_REPLY_COUNT=0",
        "ACCOUNTS_ROW_COUNT=12",
        "SELECTED_ACCOUNT_MASKED_ID=280***247",
        "SELECTED_ACCOUNT_ENABLED=true",
        "SELECTED_ACCOUNT_ONLINE=true",
        "SELECTED_ACCOUNT_CHAT_AVAILABLE=true",
        "SELECTED_ACCOUNT_PUBLISH_CAPABILITY=按需检查",
        "SELECTED_ACCOUNT_DETAIL_VISITED_READ_ONLY=true",
        "SELECTED_ACCOUNT_DETAIL_CANCEL_USED=true",
        "ITEMS_TOTAL_COUNT=39",
        "ITEMS_CURRENT_PAGE_ROW_COUNT=20",
        "ITEMS_LOADING_OR_ERROR_VISIBLE=false",
        "PUBLISH_LOGS_TOTAL_COUNT=339",
        "PUBLISH_LOGS_CURRENT_PAGE_ROW_COUNT=20",
        "PUBLISH_LOGS_LOADING_OR_ERROR_VISIBLE=false",
        "ONLINE_CHAT_PAGE_NONBLANK=true",
        "ONLINE_CHAT_SEND_INPUT_PRESENT=true",
        "ONLINE_CHAT_QUICK_PHRASE_INPUT_PRESENT=true",
        "ONLINE_CHAT_CONNECTED_SIGNAL_COUNT=6",
        "ONLINE_CHAT_DISCONNECTED_SIGNAL_COUNT=2",
        "AUTO_REPLY_RULE_ROW_COUNT=2",
        "SCHEDULED_TASKS_ROW_COUNT=21",
        "SCHEDULED_TASKS_LOADING_OR_ERROR_VISIBLE=false",
    ):
        assert marker in combined


def test_chg0034_records_all_primary_ai_toggles_closed() -> None:
    combined = _text("acceptance.md") + "\n" + _closure()

    for marker in (
        "PRIMARY_AI_REPLY_TOGGLE_COUNT=12",
        "PRIMARY_AI_REPLY_ENABLED_COUNT=0",
        "PRIMARY_AI_REPLY_ALL_CLOSED=true",
        "PRIMARY_AI_REPLY_TOGGLE_CLICKS=0",
    ):
        assert marker in combined


def test_chg0034_records_nonfatal_chart_warnings_without_fatal_errors() -> None:
    combined = _text("acceptance.md") + "\n" + _closure()

    for marker in (
        "ROOT_HEAD_STATUS=200",
        "SAME_ORIGIN_HEALTH_STATUS=200",
        "DIRECT_WEBSOCKET_HEALTH_STATUS=200",
        "FINAL_DASHBOARD_NONFATAL_CHART_WARNING_COUNT=2",
        "FINAL_DASHBOARD_CHART_WARNING_DIMENSIONS=-1",
        "FINAL_FATAL_CONSOLE_ERROR_COUNT=0",
    ):
        assert marker in combined


def test_chg0034_allows_captcha_blocker_only_as_superseded_chronology() -> None:
    historical = _historical_captcha_checkpoint()
    final = _closure()
    acceptance = _text("acceptance.md")

    assert HISTORICAL_BLOCKER in historical
    assert "CHECKPOINT_SUPERSEDED=true" in historical
    assert "SUPERSEDED_BY=20260826-authenticated-browser-ui-acceptance.md" in historical
    assert "CAPTCHA_NETWORK_BLOCKER_CHECKPOINT_SUPERSEDED=true" in final
    assert "CAPTCHA_NETWORK_BLOCKER_CHECKPOINT_SUPERSEDED=true" in acceptance
    assert HISTORICAL_BLOCKER not in final


def test_chg0034_preserves_secret_challenge_and_screenshot_limits() -> None:
    combined = (
        _text("acceptance.md")
        + "\n"
        + _closure()
        + "\n"
        + _historical_captcha_checkpoint()
    )

    for marker in (
        "CREDENTIAL_VALUES_RECORDED=false",
        "FULL_CHALLENGE_ID_RECORDED=false",
        "CHALLENGE_URLS_RECORDED=false",
        "LOCAL_DIAGNOSTIC_SCREENSHOT_COMMITTED=false",
        "FULL_LOGIN_SCREENSHOT_REFERENCED=false",
        "FALLBACK_PASSWORD_SUBMITTED=false",
        "FALLBACK_PASSWORD_VALIDATED=false",
        "USER_AUTHORIZED_ONE_CAPTCHA_CHALLENGE=true",
        "phase4-geetest-network-timeout.png",
    ):
        assert marker in combined

    forbidden_paths = (
        "geetest-failed-attempt.png",
        "geetest-canvas.png",
    )
    assert not any(path in combined for path in forbidden_paths)
    assert "USER_AUTHORIZED_ONE_CAPTCHA_SOLVE_ATTEMPT" not in combined
    assert not re.search(r"challenge[_-]?id\s*[:=]\s*[A-Za-z0-9_-]{12,}", combined)


def test_chg0034_records_zero_business_and_platform_mutations() -> None:
    combined = _text("acceptance.md") + "\n" + _closure()

    for counter in (
        "CAPTCHA_BYPASS_ATTEMPTS=0",
        "CAPTCHA_REFRESH_ATTEMPTS=0",
        "API_LOGIN_BYPASS_ATTEMPTS=0",
        "PUBLISH_INVOCATIONS=0",
        "ITEM_MUTATION_COUNT=0",
        "ITEM_SYNC_INVOCATIONS=0",
        "MESSAGE_SEND_INVOCATIONS=0",
        "AI_ENABLEMENT_INVOCATIONS=0",
        "ACCOUNT_MUTATION_COUNT=0",
        "QR_INVOCATIONS=0",
        "RECONNECT_INVOCATIONS=0",
        "ORDER_ACTION_INVOCATIONS=0",
        "PURCHASE_ACTION_INVOCATIONS=0",
        "DEPLOY_INVOCATIONS=0",
        "PLATFORM_WRITE_ACTIONS=0",
    ):
        assert counter in combined
