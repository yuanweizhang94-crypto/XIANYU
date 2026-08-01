# CHG-0017 Account Catalog Alignment Evidence

Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
Run ID: CHG17-ACCOUNT-CATALOG-ALIGNMENT-20260801T055428Z

## Scope

This run continued PR #26 without creating a new Change, branch, PR, sender,
Token client, WebSocket runtime, AI worker, or Gemini Provider.

No Cookie, Token, API key, full account ID, database primary key, item ID,
chat ID, customer message body, or full AI reply body is recorded here.

## Account Alias Resolution

- account_ai_alias: ACCOUNT-AI
- account_catalog_alias: ACCOUNT-CATALOG
- account_ws_alias: ACCOUNT-CATALOG
- ai_and_catalog_same_account: false
- ws_and_catalog_same_account: true
- ws_and_ai_same_account: false

Root cause:

`AFFECTED_ACCOUNT_ITEM_CATALOG_ABSENT` was reclassified as
`AFFECTED_ACCOUNT_IDENTITY_MISMATCH`. The Gemini configuration was on
ACCOUNT-AI, while the visible product catalog row belonged to ACCOUNT-CATALOG.
ACCOUNT-CATALOG's native WebSocket task was already running and connected.

## Catalog Gate

- catalog_record_present: true
- catalog_title_present: true
- catalog_price_present: true
- catalog_description_present: true
- catalog_ai_prompt_present: true
- runtime_account_pk_source: current_websocket_account_db_pk
- runtime_item_id_source: current_message_item_id
- runtime_catalog_account_match: true
- runtime_catalog_item_match: true
- runtime_item_info_complete: true

Runtime query equivalence:

`XYCatalogItem.account_pk == current_account.id`

and

`XYCatalogItem.item_id == current_message_item_id`

## Configuration Action

Using upstream-native `AIReplySettingsService.update_settings`, the existing
Gemini configuration was applied to ACCOUNT-CATALOG without copying the whole
metadata object and without changing catalog ownership.

- provider_type: gemini
- base_url: https://generativelanguage.googleapis.com
- model_name: gemini-3.6-flash
- api_key: present_redacted
- account_custom_prompt_parse: success
- product_ai_prompt_format: plain_text
- ACCOUNT-AI AI state after alignment: disabled
- ACCOUNT-CATALOG AI state before live test: disabled

## Zero-Send Product Context Regression

- provider_item_case_1: pass
- provider_item_case_2: pass
- provider_item_case_3: pass
- provider_item_case_4: pass
- provider_item_context_used: true
- provider_output_language: zh-CN
- provider_output_complete: true
- provider_markdown_leak: 0
- provider_template_leak: 0
- provider_json_leak: 0
- provider_sender_invocations: 0
- provider_platform_sends: 0

## Controlled Live Test

ACCOUNT-CATALOG AI was enabled only after catalog gate and zero-send product
context regression passed. One owner-controlled buyer account sent exactly one
official Xianyu message into the existing product conversation.

- inbound_messages_sent: 1
- reply_strategy: ai
- assistant_created: 1
- send_status: success
- sender_invocations: 1
- platform_sends: 1
- item_context_used: true
- reply_language: zh-CN
- reply_complete: true
- template_leak: 0
- markdown_leak: 0
- json_leak: 0
- duplicate_sends: 0
- non_whitelist_sends: 0
- proactive_customer_sends: 0

## Final Runtime State

- ACCOUNT-CATALOG account_task: running
- ACCOUNT-CATALOG websocket: connected
- ACCOUNT-CATALOG ai_enabled: true
- duplicate_executor_count: 0
- PR #26 state: Draft, Open, Unmerged

## Verdict

AI_REPLY_CONTENT_READY

stage=CHG0017_ACCOUNT_CATALOG_ALIGNED

remaining_blockers=none
