from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
CHANGE = ROOT / "changes/archive/CHG-0033-ai-auto-reply-live-canary-yilong"
EVIDENCE = CHANGE / "evidence/20260825-read-only-ai-autoreply-preflight.md"


def _combined_text() -> str:
    return "\n".join(
        [
            (CHANGE / "proposal.md").read_text(encoding="utf-8"),
            (CHANGE / "tasks.md").read_text(encoding="utf-8"),
            (CHANGE / "acceptance.md").read_text(encoding="utf-8"),
            EVIDENCE.read_text(encoding="utf-8"),
        ]
    )


def test_chg0033_records_native_ai_autoreply_owner_chain() -> None:
    text = _combined_text()
    for marker in (
        "NATIVE_AI_AUTOREPLY_OWNER=websocket/app/services/xianyu/auto_reply_service.py::AutoReplyService",
        "NATIVE_INBOUND_CHAIN=websocket/app/services/xianyu/message_handler.py::MessageHandler.handle_message -> _process_single_message -> xianyu_async.py::on_chat_message -> AutoReplyService.handle_chat_message",
        "NATIVE_AI_GENERATION_CHAIN=AutoReplyService.get_ai_reply -> websocket/app/services/xianyu/ai_reply_engine.py::AIReplyEngine.generate_reply",
        "DEPRECATED_LOCAL_WORKER_DEFAULT_ENABLED=false",
        "SECOND_AI_SENDER_CREATED=false",
    ):
        assert marker in text


def test_chg0033_records_provider_contract_without_secret_use() -> None:
    text = _combined_text()
    for marker in (
        "PROVIDER_CONFIG_SOURCE=xy_accounts.metadata.ai_reply_settings",
        "PROVIDER_CREDENTIAL_KEY=api_key",
        "ACCOUNT_PROVIDER_TYPE=openai_compatible",
        "ACCOUNT_PROVIDER_MODEL_NAME=qwen-plus",
        "ACCOUNT_PROVIDER_API_KEY_PRESENT=false",
        "PROVIDER_CREDENTIAL_VALUE_PRINTED=false",
        "PROVIDER_CREDENTIAL_USED=false",
        "SAFE_SENDER_FREE_PROVIDER_VALIDATION_PATH=common/services/ai_provider_service.py::test_ai_connection",
        "PARENT_CREDENTIAL_EPHEMERAL_INJECTION_POSSIBLE=true",
    ):
        assert marker in text


def test_chg0033_records_single_sender_free_provider_connection_test() -> None:
    text = _combined_text()
    for marker in (
        "PROVIDER_CONNECTION_TEST_INVOCATIONS=1",
        "PROVIDER_CONNECTION_TEST_SUCCESS=false",
        "PROVIDER_CONNECTION_TEST_HTTP_STATUS_CLASS=HTTP_4XX",
        "PROVIDER_CONNECTION_TEST_ERROR_CLASS=RuntimeError",
        "PROVIDER_CONNECTION_TEST_ROW_COUNTS_UNCHANGED=true",
        "PROVIDER_CONNECTION_TEST_AUTOREPLY_ENGINE_GENERATE_REPLY_CALLED=false",
        "PROVIDER_CONNECTION_TEST_PLATFORM_SENDER_CALLED=false",
        "PROVIDER_CONNECTION_TEST_CREDENTIAL_PERSISTED=false",
    ):
        assert marker in text


def test_chg0033_records_sanitized_account_policy_and_activity_facts() -> None:
    text = _combined_text()
    for marker in (
        "ACCOUNT_CURRENT_AI_ENABLED_FLAG=false",
        "ACCOUNT_WEBSOCKET_CONNECTED=true",
        "DEFAULT_REPLY_ENABLED_TOTAL=11",
        "KEYWORD_ACTIVE_TOTAL=0",
        "SKIP_REPLY_FILTER_ENABLED=0",
        "AUTO_REPLY_LOGS_TOTAL=4",
        "AUTO_REPLY_AI_STRATEGY_TOTAL=0",
        "AI_CHAT_MESSAGES_TOTAL=0",
        "UNREAD_BACKLOG_CURRENT=NOT_AVAILABLE_FROM_DB_OR_STATUS_WITHOUT_CONVERSATION_READ",
    ):
        assert marker in text


def test_chg0033_fails_closed_on_counterpart_and_runtime_probe_blockers() -> None:
    text = _combined_text()
    for marker in (
        "CHG0032_CONTROLLED_COUNTERPART=false",
        "OWNER_CONTROLLED_COUNTERPART_PROVEN=false",
        "TECHNICAL_READINESS=NO_GO_SOURCE_CHAIN_READY_ACCOUNT_CONNECTED_PROVIDER",
        "CODE_DEFECT_REPAIR_NEEDED=false",
        "CONFIG_ACTION_REQUIRED_BEFORE_LIVE=true",
        "NO_GO_BLOCKER=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART",
        "FINAL_CHECKPOINT=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART",
    ):
        assert marker in text


def test_chg0033_final_closure_records_no_go_and_zero_mutation() -> None:
    closure = (CHANGE / "evidence" / "20260825-final-no-go-closure.md").read_text(
        encoding="utf-8"
    )
    for marker in (
        "COMMANDER_FINAL_DECISION=NO-GO",
        "AI_AUTO_REPLY_LIVE_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART_AND_PROVIDER_READINESS",
        "ADDITIONAL_BLOCKER_PROVIDER=PROVIDER_CREDENTIAL_HTTP_4XX",
        "ADDITIONAL_BLOCKER_BACKLOG=UNREAD_ZERO_NOT_PROVEN",
        "AI_ENABLEMENT_INVOCATIONS=0",
        "AI_PROVIDER_INVOCATIONS=1",
        "AI_REPLY_SEND_INVOCATIONS=0",
        "CONFIG_PERSISTENCE_COUNT=0",
        "PRODUCTION_MUTATION_COUNT=0",
        "CREDENTIAL_VALUE_RECORDED=false",
        "CREDENTIAL_HASH_RECORDED=false",
    ):
        assert marker in closure
