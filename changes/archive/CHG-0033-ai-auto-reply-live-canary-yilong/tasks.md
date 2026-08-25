# CHG-0033 Tasks

Change ID: CHG-0033-ai-auto-reply-live-canary-yilong
Status: ARCHIVED

- [x] T1 Verify latest remote main equals `680363c21ca5678f7ceae831294cbb05695d4390`, create the isolated CHG-0033 worktree/branch, and prove the branch is clean before Change creation.
- [x] T2 Run `python scripts/project_context.py` before development and confirm no prior executable active Change exists on this baseline.
- [x] T3 Create the active CHG-0033 governance record with the required three-line execution contract, masked project-owner identity binding, and zero-action gates.
- [x] T4 Regenerate `generated/PROJECT_STATE.json` with `python scripts/generate_state.py` and verify with `Test-Path`, generated active state, and dirty `git status --short`.
- [x] T5 Identify the existing provider/model configuration contract and report only env/key names, configured/present booleans, and a safe credential-injection mechanism; do not use the parent credential.
- [x] T6 Inspect the unique native AI auto-reply owner and exact message receive/generate/send chain; prove deprecated local worker remains off.
- [x] T7 Inspect approved account `280***247` WebSocket/session lineage, token/verification state, and current AI enabled state without account mutation.
- [x] T8 Inspect policy/default/SKU/sensitive-output/frequency/inbound/outbound dedupe facts and whether enabling could process historical real-customer messages.
- [x] T9 Inspect unread/backlog state and sanitized reply activity counts without persisting customer content, full account IDs, full conversation IDs, Cookies, Tokens, Authorization values, Profile secrets, screenshot content, or screenshot hash; live unread zero proof remains gated/not run because conversation readback was not authorized in the final NO-GO path.
- [x] T10 Confirm CHG-0032 no-controlled-counterpart blocker still holds without enumerating additional ordinary conversations.
- [x] T11 Return the GO/NO-GO checkpoint. If no counterpart is proven, record `HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`; no AI enablement, inbound, reply send, message send, deploy, Browser, publish/sync, QR/reconnect, account mutation, commit, or push.

## Read-Only Preflight Result

`REMOTE_MAIN_VERIFIED=680363c21ca5678f7ceae831294cbb05695d4390`

`WORKTREE_HEAD=680363c21ca5678f7ceae831294cbb05695d4390`

`PROJECT_CONTEXT_ACTIVE_CHANGE=CHG-0033-ai-auto-reply-live-canary-yilong`

`PINNED_UPSTREAM_SHA=bda1a859df63fa5f24e51398fa80a23490bb6dfc`

`NATIVE_AI_AUTOREPLY_OWNER=websocket/app/services/xianyu/auto_reply_service.py::AutoReplyService`

`NATIVE_INBOUND_CHAIN=websocket/app/services/xianyu/message_handler.py::MessageHandler.handle_message -> _process_single_message -> xianyu_async.py::on_chat_message -> AutoReplyService.handle_chat_message`

`NATIVE_POLICY_CHAIN=AutoReplyService.handle_chat_message -> system/self/auto-delivery/item-owner/dedup/filter checks -> get_reply`

`NATIVE_REPLY_SELECTION_ORDER=keyword -> ai -> default`

`NATIVE_AI_GENERATION_CHAIN=AutoReplyService.get_ai_reply -> websocket/app/services/xianyu/ai_reply_engine.py::AIReplyEngine.generate_reply`

`NATIVE_SEND_CHAIN=AutoReplyService._send_text_with_separator/send_image_msg -> XianyuAsync send owner`

`CHAT_SEND_OWNER_CARRIED_FROM_CHG0032=POST /api/v1/chat-new/send-message/{account_id} -> GoofishImClient.send_text_message -> /r/MessageSend/sendByReceiverScope`

`DEPRECATED_LOCAL_WORKER_PATH=app/xianyu_system/worker/autoreply`

`DEPRECATED_LOCAL_WORKER_DEFAULT_ENABLED=false`

`DEPRECATED_LOCAL_WORKER_MODE_DEFAULT=disabled`

`DEPRECATED_LOCAL_WORKER_LIVE_WRITE_GATED=true`

`SECOND_AI_SENDER_CREATED=false`

`PROVIDER_CONFIG_SOURCE=xy_accounts.metadata.ai_reply_settings`

`PROVIDER_CONFIG_KEYS=ai_enabled,enabled,provider_type,base_url,model_name,api_key,max_discount_percent,max_discount_amount,max_bargain_rounds,custom_prompts,ai_time_range_start,ai_time_range_end`

`PROVIDER_SUPPORTED_TYPES=openai_compatible,anthropic,gemini,dashscope_app`

`PROVIDER_DEFAULT_TYPE=openai_compatible`

`PROVIDER_DEFAULT_MODEL=qwen-plus`

`PROVIDER_CREDENTIAL_KEY=api_key`

`PROVIDER_ENV_OPENAI_API_KEY_PRESENT=false`

`PROVIDER_ENV_DASHSCOPE_API_KEY_PRESENT=false`

`PROVIDER_ENV_GEMINI_API_KEY_PRESENT=false`

`PROVIDER_ENV_GOOGLE_API_KEY_PRESENT=false`

`PROVIDER_ENV_ANTHROPIC_API_KEY_PRESENT=false`

`PROVIDER_ENV_AI_API_KEY_PRESENT=false`

`PROVIDER_ENV_AI_PROVIDER_TYPE_PRESENT=false`

`PROVIDER_ENV_AI_MODEL_NAME_PRESENT=false`

`PROVIDER_ENV_AI_BASE_URL_PRESENT=false`

`ACCOUNT_PROVIDER_TYPE=openai_compatible`

`ACCOUNT_PROVIDER_MODEL_NAME=qwen-plus`

`ACCOUNT_PROVIDER_API_KEY_PRESENT=false`

`ACCOUNT_PROVIDER_BASE_URL_STORED_PRESENT=false`

`ACCOUNT_PROVIDER_BASE_URL_DEFAULT_PRESENT=true`

`ACCOUNT_PROVIDER_REQUIRED_FIELDS_COMPLETE=false`

`ACCOUNT_PROVIDER_MISSING_FIELDS=API地址,API Key`

`PROVIDER_CREDENTIAL_VALUE_PRINTED=false`

`PROVIDER_CREDENTIAL_USED=false`

`PROVIDER_CONFIGURED_PRESENT_BOOLEAN_NOT_PROBED=false`

`SAFE_SENDER_FREE_PROVIDER_VALIDATION_PATH=common/services/ai_provider_service.py::test_ai_connection`

`SAFE_PROVIDER_VALIDATION_PLATFORM_SENDER_FREE=true`

`SAFE_PROVIDER_VALIDATION_WRITES_REPO=false`

`SAFE_PROVIDER_VALIDATION_WRITES_PLATFORM=false`

`PARENT_CREDENTIAL_EPHEMERAL_INJECTION_POSSIBLE=true`

`PARENT_CREDENTIAL_EPHEMERAL_INJECTION_MECHANISM=process_memory_only_call_to_test_ai_connection_or_temp_env_for_one_process_without_logging_or_persistence`

`PROVIDER_CONNECTION_TEST_INVOCATIONS=1`

`PROVIDER_CONNECTION_TEST_SUCCESS=false`

`PROVIDER_CONNECTION_TEST_HTTP_STATUS_CLASS=HTTP_4XX`

`PROVIDER_CONNECTION_TEST_ERROR_CLASS=RuntimeError`

`PROVIDER_CONNECTION_TEST_ELAPSED_MS=261`

`PROVIDER_CONNECTION_TEST_ROW_COUNTS_UNCHANGED=true`

`PROVIDER_CONNECTION_TEST_AUTOREPLY_ENGINE_GENERATE_REPLY_CALLED=false`

`PROVIDER_CONNECTION_TEST_PLATFORM_SENDER_CALLED=false`

`PROVIDER_CONNECTION_TEST_CREDENTIAL_PERSISTED=false`

`POLICY_SYSTEM_SELF_MESSAGE_SKIP=true`

`POLICY_AUTO_DELIVERY_TRIGGER_SKIP_AUTOREPLY=true`

`POLICY_ITEM_BELONGS_TO_ACCOUNT_GATE=true`

`POLICY_SKIP_REPLY_FILTER=xy_message_filters.filter_type=skip_reply`

`POLICY_SKIP_NOTIFY_FILTER=xy_message_filters.filter_type=skip_notify`

`POLICY_MESSAGE_EXPIRE_DEFAULT_SECONDS=3600`

`POLICY_INBOUND_MESSAGE_ID_DEDUPE=true`

`POLICY_AUTOREPLY_DEDUPE_KEY=chat_id_plus_send_message`

`POLICY_REPLY_DELAY_ACCOUNT_FIELD=xy_accounts.reply_delay_seconds`

`POLICY_KEYWORD_PRIORITY=item_keyword_then_common_keyword`

`POLICY_REPLY_SELECTION_ORDER=keyword_then_ai_then_default`

`POLICY_DEFAULT_REPLY_SCOPE=item_then_account`

`POLICY_DEFAULT_REPLY_ONCE_SUPPORTED=true`

`POLICY_DEFAULT_REPLY_API_SESSION_LOCK=true`

`POLICY_AI_ORDERED_USER_BLOCK_FIELD=xy_accounts.ai_reply_block_ordered_users`

`POLICY_AI_HISTORY_CONTEXT_LIMIT=20`

`POLICY_AI_RECENT_MESSAGE_CUTOFF_SECONDS=6_when_skip_wait_else_25`

`POLICY_AI_CHAT_LOCK_PER_CHAT=true`

`POLICY_AI_CHAT_LOCK_EXPIRE_SECONDS=7200`

`POLICY_AI_SENSITIVE_OUTPUT_FILTER_NOT_PROVEN=true`

`ENABLING_HISTORICAL_UNREAD_PROCESSING_RISK=UNPROVEN_CURRENT_RUNTIME_DB_PREFLIGHT_NOT_COMPLETED`

`ACCOUNT_CURRENT_AI_ENABLED_FLAG=false`

`ACCOUNT_ENABLED=true`

`ACCOUNT_STATUS_ACTIVE=true`

`ACCOUNT_COOKIE_PRESENT=true`

`ACCOUNT_COOKIE_PARSE_SUCCESS=true`

`ACCOUNT_COOKIE_UNB_PRESENT=true`

`ACCOUNT_LAST_LOGIN_AT_PRESENT=true`

`ACCOUNT_LAST_REFRESH_AT_PRESENT=true`

`ACCOUNT_WEBSOCKET_STATUS_HTTP_2XX=true`

`ACCOUNT_WEBSOCKET_STATUS_SUCCESS=true`

`ACCOUNT_WEBSOCKET_CONNECTED=true`

`ACCOUNT_TOKEN_VALUE_PRINTED=false`

`ACCOUNT_COOKIE_VALUE_PRINTED=false`

`ACCOUNT_PLATFORM_VERIFICATION_STATE=NOT_REPORTED_BY_SANITIZED_STATUS_ENDPOINT`

`DEFAULT_REPLY_ENABLED_TOTAL=11`

`DEFAULT_REPLY_ACCOUNT_ENABLED=0`

`DEFAULT_REPLY_ITEM_ENABLED=11`

`DEFAULT_REPLY_API_ENABLED=0`

`DEFAULT_REPLY_ONCE_ENABLED=0`

`DEFAULT_REPLY_ONCE_RECORDS=0`

`KEYWORD_ACTIVE_TOTAL=0`

`KEYWORD_ITEM_ACTIVE=0`

`KEYWORD_COMMON_ACTIVE=0`

`KEYWORD_IMAGE_ACTIVE=0`

`SKIP_REPLY_FILTER_ENABLED=0`

`SKIP_NOTIFY_FILTER_ENABLED=0`

`ORDERED_USER_ORDER_ROWS=0`

`AUTO_REPLY_LOGS_TOTAL=4`

`AUTO_REPLY_LOGS_24H=0`

`AUTO_REPLY_SUCCESS_TOTAL=2`

`AUTO_REPLY_FAILED_TOTAL=0`

`AUTO_REPLY_SKIPPED_TOTAL=2`

`AUTO_REPLY_AI_STRATEGY_TOTAL=0`

`AUTO_REPLY_AI_STRATEGY_24H=0`

`AUTO_REPLY_SEND_SUCCESS_TOTAL=2`

`AUTO_REPLY_SEND_UNKNOWN_TOTAL=2`

`AI_CHAT_MESSAGES_TOTAL=0`

`AI_CHAT_USER_MESSAGES_TOTAL=0`

`AI_CHAT_ASSISTANT_MESSAGES_TOTAL=0`

`UNREAD_BACKLOG_CURRENT=NOT_AVAILABLE_FROM_DB_OR_STATUS_WITHOUT_CONVERSATION_READ`

`CHG0032_CONTROLLED_COUNTERPART=false`

`OWNER_CONTROLLED_COUNTERPART_PROVEN=false`

`TECHNICAL_READINESS=NO_GO_SOURCE_CHAIN_READY_ACCOUNT_CONNECTED_PROVIDER_CONFIG_INCOMPLETE_UNREAD_ZERO_NOT_PROVEN`

`CODE_DEFECT_REPAIR_NEEDED=false`

`CONFIG_ACTION_REQUIRED_BEFORE_LIVE=true`

`CONFIG_ACTION_REASON=ACCOUNT_AI_PROVIDER_API_KEY_AND_BASE_URL_NOT_CURRENTLY_COMPLETE`

`FINAL_CHECKPOINT=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

## Commander Phase 3 Closure

`COMMANDER_FINAL_DECISION=NO-GO`

`AI_AUTO_REPLY_LIVE_ACCEPTANCE=BLOCKED_NO_CONTROLLED_COUNTERPART_AND_PROVIDER_READINESS`

`PRIMARY_BLOCKER=HUMAN_BLOCKED_NO_CONTROLLED_COUNTERPART`

`ADDITIONAL_BLOCKER_PROVIDER=PROVIDER_CREDENTIAL_HTTP_4XX`

`ADDITIONAL_BLOCKER_BACKLOG=UNREAD_ZERO_NOT_PROVEN`

`LIVE_CANARY_ENABLEMENT=GATED_NOT_RUN`

`LIVE_CANARY_INBOUND=GATED_NOT_RUN`

`LIVE_CANARY_AI_REPLY=GATED_NOT_RUN`

`LIVE_CANARY_DURABLE_VISIBLE_READBACK=GATED_NOT_RUN`

`AI_REMAINED_DISABLED=true`

`AI_ENABLEMENT_INVOCATIONS=0`

`AI_PROVIDER_INVOCATIONS=1`

`AI_PROVIDER_INVOCATION_MODE=SENDER_FREE_CONNECTION_TEST_ONLY`

`AI_REPLY_SEND_INVOCATIONS=0`

`PLATFORM_SEND_INVOCATIONS=0`

`INBOUND_CANARY_MESSAGES=0`

`UNRELATED_CONVERSATIONS_ENUMERATED=0`

`CONFIG_PERSISTENCE_COUNT=0`

`PRODUCTION_MUTATION_COUNT=0`

`CREDENTIAL_VALUE_RECORDED=false`

`CREDENTIAL_HASH_RECORDED=false`

## Upstream Capability Audit

Pinned upstream native AI auto-reply owner will be searched during T6.

## Pinned Upstream Evidence

Pinned upstream checkout: `D:/xianyu-upstream-pilot`. Pinned SHA will be recorded during read-only owner verification.

## Existing Local Implementation Search

Local and archived evidence will be searched narrowly during T5 through T10.

## Reuse Decision

Decision: ADOPT_UPSTREAM

## Duplicate Implementation Risk

No duplicate AI auto-reply path is planned.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies auto-reply execution but not this controlled canary and commander checkpoint.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing upstream-native AI auto-reply owner.

## Retirement Plan For Overlapping Local Code

No overlapping local code is added.
