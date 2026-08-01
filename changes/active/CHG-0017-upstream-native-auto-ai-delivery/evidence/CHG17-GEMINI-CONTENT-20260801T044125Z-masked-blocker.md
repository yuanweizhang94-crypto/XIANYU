# CHG-0017 Gemini Content Quality Repair Evidence

Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
Run ID: CHG17-GEMINI-CONTENT-20260801T044125Z

## Execution Contract

User outcome: restore safe upstream-native Gemini AI replies so buyer questions receive one complete natural Simplified Chinese customer-service answer.

Confirmed blocker: the affected account had malformed prompt content in practice and the upstream Gemini path could send truncated, first-part-only, Markdown, JSON-like, or English-template output. After repair, the affected account still has zero synced catalog items, so a live product-aware reply cannot be safely re-enabled or tested.

Smallest success test: zero-send Gemini provider tests pass with shared parsing and quality gates; no Xianyu sender invocation occurs; live test continues only after the affected account has an account-scoped catalog item with title, price, description, and product AI prompt.

## Prompt and Provider Findings

- custom_prompt_format: json
- custom_prompt_parse: success
- effective_prompt_source: custom
- custom_prompt_cjk_present_after_repair: true
- provider_type: gemini
- base_url: https://generativelanguage.googleapis.com
- model_name: gemini-3.6-flash
- model_name_has_models_prefix: false
- thinking_config: supported_low
- response_mime_text_plain: supported

## Confirmed Root Causes

- The prior plain-text account prompt could parse-fail and silently fall back to system defaults.
- The affected account prompt content was later found to be JSON-valid but not valid Chinese due to command-pipe encoding corruption; it was rewritten with ASCII Unicode escapes and AI was kept disabled.
- The upstream Gemini parser read only `parts[0]` and did not distinguish thought parts from answer parts.
- The upstream path did not reject `MAX_TOKENS` / `LENGTH` output before sender use.
- The upstream path did not block obvious Markdown, JSON-like, field-name, or English-template output before sender use.
- The native account UI/backend did not reject invalid account-level custom prompt JSON before saving.

## Minimal Patch

- common/services/ai_provider_service.py: shared Gemini parser, truncation detection, plain-text Gemini config, output quality gate, token limits.
- websocket/app/services/xianyu/ai_reply_engine.py: formal Gemini replies reuse the shared parser, plain-text config, low temperature, and one strict retry.
- backend-web/app/services/ai_reply_service.py: account-level custom prompts must be a JSON object with string keys and values.
- frontend/src/pages/accounts/Accounts.tsx: account AI settings reject invalid JSON before save/test.
- tests/test_chg0017_gemini_response_parser.py: parser, truncation, quality gate, and config coverage.
- tests/test_chg0017_ai_prompt_validation.py: backend JSON validation coverage.

## Zero-Send Provider Regression

- gemini_http_status: 200
- gemini_finish_reason: STOP
- gemini_part_count: 1
- gemini_thought_part_count: 0
- gemini_answer_part_count: 1
- first_part_is_final_answer: true
- output_truncated: false
- current_parser_reads_first_part_only: false
- current_max_output_tokens: 1024
- retry_max_output_tokens: 2048
- provider_case_1: pass
- provider_case_2: pass
- provider_case_3: pass
- provider_case_4: pass
- provider_output_language: zh-CN
- provider_output_complete: true
- provider_markdown_leak: 0
- provider_english_template_leak: 0
- provider_sender_invocations: 0
- provider_platform_sends: 0

## Item Catalog Gate

- item_catalog_record: absent
- item_account_match: false
- item_title_present: false
- item_price_present: false
- item_description_present: false
- item_ai_prompt_present: false
- runtime_item_info_complete: false
- upstream_item_sync_success: true
- fetched_count: 0
- saved_count: 0
- item_sync_message_category: empty_from_platform

The upstream-native item sync path was used. It returned success but the
platform response for the affected account contained zero parsed items, so
there was no account-scoped catalog row to save. A catalog row exists for
another local account, but CHG-0017 must not use another account's product
catalog for the affected account.

## Safety State

- affected account AI enabled after repair: false
- legacy AI enabled after repair: false
- sender invocation during provider tests: 0
- platform sends during provider tests: 0
- Cookie printed: no
- Token printed: no
- API key printed: no
- full account ID printed in evidence: no
- customer message body printed: no

## Verdict

AI_REPLY_CONTENT_BLOCKED

- stage: item_catalog_gate_before_live_test
- blocker_code: AFFECTED_ACCOUNT_ITEM_CATALOG_ABSENT
- upstream_ai_function_checked: yes
- code_changes_attempted: yes
- why_codex_cannot_complete: the affected account currently has no account-scoped catalog item, so a product-aware live AI reply cannot meet the acceptance requirement without using the wrong account's product data or fabricating product information.
- minimal_next_action: make the affected account's intended product visible to upstream-native item sync, then rerun the catalog gate and live AI reply test once.
