from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PATCH = ROOT / "vendor/patches/xianyu-auto-reply/chg0041-native-chat-runtime-equivalence.patch"
CHANGE = ROOT / "changes/archive/CHG-0041-native-chat-runtime-equivalence"
CHG39 = ROOT / "vendor/patches/xianyu-auto-reply/chg0039-token-invalidation-recovery.patch"
CHG40 = ROOT / "vendor/patches/xianyu-auto-reply/chg0040-qr-cookie-browser-lineage-enrichment.patch"


def patch_text() -> str:
    return PATCH.read_text(encoding="utf-8")


def test_scope_is_only_existing_native_owner_rpc_files():
    text = patch_text()
    assert text.count("diff --git ") == 2
    assert "websocket/app/api/routes/internal.py" in text
    assert "websocket/app/services/xianyu/xianyu_async.py" in text
    assert "backend-web/app/api/routes/cookies.py" not in text
    assert "auto_reply_service.py" not in text
    assert "scheduler/" not in text


def test_patch_is_additive_and_contains_required_rpc_surface():
    text = patch_text()
    removed = [line for line in text.splitlines() if line.startswith("-") and not line.startswith("---")]
    assert removed == []
    for marker in (
        'chat/conversations',
        'chat/messages/{cid}',
        'chat/send-text',
        'chat/send-image',
        'chat/recall',
        "async def _chat_lwp_request",
        "async def get_chat_conversations",
        "async def get_chat_messages",
        "async def send_chat_text_message",
        "async def send_chat_image_message",
        "async def recall_chat_message",
    ):
        assert marker in text


def test_shared_owner_only_no_parallel_socket_or_manager():
    text = patch_text()
    assert "get_manager()" in text
    assert "manager.instances.get(account_id)" in text
    assert "connection_manager.ws" in text
    assert "websockets.connect" not in text
    assert "CookieManager(" not in text
    assert "ImSessionManager(" not in text


def test_change_records_runtime_stale_only_not_new_enable_architecture():
    proposal = (CHANGE / "proposal.md").read_text(encoding="utf-8")
    assert "CURRENT_LOCAL_CAPABILITY=EXISTS" in proposal
    assert "CURRENT_RUNTIME_CAPABILITY=STALE_ONLY" in proposal
    assert "NEW_IMPLEMENTATION_ALLOWED=false" in proposal
    assert "FIX_CLASS=RUNTIME_EQUIVALENCE_RESTORATION" in proposal


def test_chg0039_explicit_invalidation_regression_is_preserved():
    text = CHG39.read_text(encoding="utf-8")
    assert "explicitly_invalidated" in text
    assert "allow_expired=True" in text


def test_chg0040_canonical_browser_enrichment_regression_is_preserved():
    text = CHG40.read_text(encoding="utf-8")
    assert "cookie_renew_browser_service.renew(cookies, browser_account_id)" in text
    assert "QR_COOKIE_BROWSER_ENRICHMENT_FAILED" in text


def test_acceptance_records_dynamic_candidate_and_real_first_divergence():
    acceptance = (CHANGE / "acceptance.md").read_text(encoding="utf-8")
    assert "NATIVE_CHAT_ROUTES=PASS" in acceptance
    assert "NATIVE_CHAT_SHARED_LWP_OWNER=PASS" in acceptance
    assert "PRE_FIX_NATIVE_CHAT_RPC_HTTP_STATUS=404" in acceptance
    assert "REGISTRATION_ACK=PASS" in acceptance
