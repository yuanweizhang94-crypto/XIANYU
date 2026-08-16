from __future__ import annotations

import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor" / "patches" / "xianyu-auto-reply" / "59c64df-chg0018-restore-latest-upstream-chat.patch"
EXPECTED_SHA256 = "3325CCBB263E968486A2804EA816E6B1E18FB8F2DB6C45F3FE9D1A4F19D01F72"


def _patch() -> str:
    return PATCH.read_text(encoding="utf-8")


def _changed_paths() -> list[str]:
    return [
        line.removeprefix("diff --git a/").split(" b/", 1)[0]
        for line in _patch().splitlines()
        if line.startswith("diff --git a/")
    ]


def test_patch_hash_is_locked() -> None:
    assert hashlib.sha256(PATCH.read_bytes()).hexdigest().upper() == EXPECTED_SHA256


def test_patch_changes_only_chat_restore_and_required_shared_files() -> None:
    assert _changed_paths() == [
        "backend-web/app/api/routes/chat_new.py",
        "backend-web/app/api/routes/chat_customer_order.py",
        "backend-web/app/services/chat_new/im_client.py",
        "backend-web/app/services/chat_new/im_session_manager.py",
        "backend-web/app/api/routes/cookies.py",
        "backend-web/app/services/websocket_client.py",
        "common/utils/cookie_refresh.py",
        "websocket/app/api/routes/internal.py",
        "common/services/cookie_renew_browser_service.py",
        "frontend/src/api/chatNew.ts",
        "frontend/src/pages/chat-new/ChatNew.tsx",
        "frontend/src/pages/chat-new/CustomerOrdersPanel.tsx",
        "frontend/src/types/index.ts",
    ]


def test_old_xianyu_chat_pvr_and_diagnostic_gate_are_removed() -> None:
    text = _patch()
    assert '-        result = await asyncio.wait_for(manager.read_only_diagnostic(account_id)' in text
    assert '-        elif chat_state == "PLATFORM_VERIFICATION_REQUIRED":' in text
    assert '-            effective_chat_state = "PLATFORM_VERIFICATION_REQUIRED"' in text
    assert "-            accounts.find((a) => a.account_id === activeAccountId)?.chat_state === 'PLATFORM_VERIFICATION_REQUIRED' ? (" in text
    assert '+        await manager.get_or_connect(account_id)' in text


def test_chat_owned_files_restore_upstream_simple_lazy_connect_shape() -> None:
    text = _patch()
    assert '-from app.services.chat_new.im_session_manager import CHAT_CONNECT_DEADLINE_SECONDS, ChatConnectError' in text
    assert '-    async def read_only_diagnostic(self, account_id: str)' in text
    assert '-    async def invalidate_auth_consumers(self, account_id: str' in text
    assert '-async def _record_chat_readiness(' in text
    assert '-    auth_convergence_fingerprint,' in text
    assert '+        connected_ids = manager.get_connected_account_ids()' in text


def test_frontend_restores_upstream_lazy_connect_without_pvr_rendering() -> None:
    text = _patch()
    assert '-export type ChatBusinessState =' in text
    assert '-  const [connectingIds, setConnectingIds]' in text
    assert '-    } else if (acc.chat_state === \'PLATFORM_VERIFICATION_REQUIRED\') {' in text
    assert '+    setConnectingId(accountId)' in text
    assert '       await handleConnect(acc.account_id)' in text


def test_manual_human_verification_chat_wrapper_is_removed() -> None:
    text = _patch()
    assert '-    async def open_human_verification(self, account_id: str)' in text
    assert '-@router.post("/accounts/{account_id}/human-verification/open")' in text
    assert '-    async def open_human_verification(self, account_id: str)' in text or '-    async def open_human_verification(self, account_id: str) -> dict[str, Any]:' in text
    assert '+@router.post("/accounts/{account_id}/human-verification/open")' not in text


def test_shared_account_serializer_uses_only_live_upstream_chat_runtime() -> None:
    text = _patch()
    assert '+    connected_ids = set(get_im_session_manager().get_connected_account_ids())' in text
    assert '+        "chat_state": "READY" if chat_connected else "WAITING_CONNECT",' in text
    assert '+        source="latest_upstream_chat_runtime",' in text
    assert '+        state="PLATFORM_VERIFICATION_REQUIRED"' not in text


def test_latest_upstream_customer_order_surface_is_included() -> None:
    text = _patch()
    assert '+            "card_only_delivered": bool(order.card_only_delivered),' in text
    assert '+  card_only_delivered: boolean' in text
    assert "order.card_only_delivered ? '卡券已发送' : '发卡发货'" in text


def test_patch_does_not_touch_token_request_owner_qr_or_auto_reply_files() -> None:
    paths = set(_changed_paths())
    assert "common/services/im_token_api.py" not in paths
    assert "backend-web/app/api/routes/qr_login.py" not in paths
    assert "backend-web/app/api/routes/shared_scan.py" not in paths
    assert "backend-web/app/services/account_service.py" not in paths
    assert "websocket/app/services/xianyu/xianyu_async.py" not in paths
    assert "websocket/app/services/xianyu/cookie_token_manager.py" not in paths
    assert "websocket/app/services/xianyu/connection_manager.py" not in paths
