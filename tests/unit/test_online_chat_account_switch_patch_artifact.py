from __future__ import annotations

import hashlib
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/online-chat-account-switch-convergence-20260829.patch"
EXPECTED_SHA256 = "750a3963646ac566765c676ff521eca1b7bb10db6ee91510c045c6561f047c0e"
EXPECTED_PATCH_FILES = {
    "frontend/src/pages/chat-new/ChatNew.tsx",
    "tests/test_online_chat_account_switch_convergence.py",
}


def _patch_bytes() -> bytes:
    return PATCH.read_bytes()


def _patch_text() -> str:
    return _patch_bytes().decode("utf-8")


def _git_apply_numstat() -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "apply", "--numstat", "--unidiff-zero", str(PATCH)],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def _numstat_paths(stdout: str) -> set[str]:
    paths: set[str] = set()
    for line in stdout.splitlines():
        fields = line.split("\t")
        if len(fields) == 3:
            paths.add(fields[2])
    return paths


def _added_patch_text_for(path_fragment: str) -> str:
    in_file = False
    added_lines: list[str] = []
    for line in _patch_text().splitlines():
        if line.startswith("diff --git "):
            in_file = path_fragment in line
            continue
        if in_file and line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line[1:])
    return "\n".join(added_lines)


def test_patch_sha_and_scope_are_locked_to_chat_frontend_only() -> None:
    assert hashlib.sha256(_patch_bytes()).hexdigest() == EXPECTED_SHA256
    result = _git_apply_numstat()
    assert result.returncode == 0, f"stdout={result.stdout}\nstderr={result.stderr}"
    assert _numstat_paths(result.stdout) == EXPECTED_PATCH_FILES


def test_every_account_switch_reloads_conversations_even_when_cache_exists() -> None:
    added = _added_patch_text_for("ChatNew.tsx")
    assert "const activateAccountContext = useCallback" in added
    assert "loadConversations(activeAccountId)" in added
    assert "可以先恢复当前账号缓存，但每次账号切换都必须重新读取当前账号会话真值" in added


def test_stale_conversation_message_and_order_responses_are_guarded() -> None:
    added = _added_patch_text_for("ChatNew.tsx")
    for marker in (
        "accountContextGenerationRef",
        "conversationRequestGenerationRef",
        "messageRequestGenerationRef",
        "orderRequestGenerationRef",
        "activeAccountIdRef.current === accountId",
        "activeCidRef.current === cid",
        "if (!isCurrentRequest()) return",
    ):
        assert marker in added


def test_account_switch_clears_visible_old_account_context() -> None:
    added = _added_patch_text_for("ChatNew.tsx")
    for marker in (
        "setConversations([])",
        "setActiveCid('')",
        "setMessages([])",
        "setCustomerOrders([])",
        "setOrderDetail(null)",
        "setInputText('')",
        "setPendingImage((current)",
    ):
        assert marker in added


def test_regression_tests_cover_switch_back_empty_account_and_rapid_race() -> None:
    tests_added = _added_patch_text_for("tests/test_online_chat_account_switch_convergence.py")
    for test_name in (
        "test_account_switch_always_reloads_current_account_conversations",
        "test_account_switch_clears_old_visible_chat_context_before_new_account_render",
        "test_conversation_response_requires_selected_account_and_latest_generation",
        "test_empty_or_changed_conversation_response_cannot_leave_invalid_old_chat_selected",
        "test_message_and_customer_order_responses_are_scoped_to_current_account_context",
        "test_rapid_a_b_c_late_a_or_b_response_cannot_overwrite_c",
        "test_switch_back_c_to_a_requires_a_new_request_and_accepts_only_new_a_response",
        "test_account_without_conversations_replaces_old_account_rows_with_empty_list",
    ):
        assert test_name in tests_added


def test_patch_does_not_touch_backend_websocket_scheduler_or_business_send_apis() -> None:
    text = _patch_text()
    for forbidden_path in (
        "backend-web/",
        "websocket/",
        "scheduler/",
        "common/",
    ):
        assert f"diff --git a/{forbidden_path}" not in text
    added = _added_patch_text_for("ChatNew.tsx")
    assert "send-message" not in added
    assert "send-image" not in added
    assert "product-publish" not in added
    assert "batch-offline" not in added
