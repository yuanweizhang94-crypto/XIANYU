# CHG-0017 Publish Item Identity And Client Validation

## Scope

- Task: CHG-0017-PUBLISH-ITEM-IDENTITY-AND-CLIENT-VALIDATION
- Change: CHG-0017-upstream-native-auto-ai-delivery
- Branch: feat/CHG-0017-upstream-native-auto-ai-delivery
- Governance HEAD: ed6ed1eefddaad92d9e79d17372fa7d00d778f87
- Candidate upstream HEAD: 4c5e1ac5f532c7313365d70409ae115305de8a55
- Secrets, Cookie, Token, full account IDs, full item IDs, request headers, and verification URLs recorded: no

## Upstream Evidence

- Native publish path reused: backend-web/app/services/xianyu_publisher.py
- Native publish execution path reused: common/services/publish_execution_service.py
- Native address resolution reused: common/services/publish_address_service.py
- Native image handling reused: common/services/publish_image_service.py
- Native QR login flow located: backend-web/app/api/routes/qr_login.py, backend-web/app/services/qr_login/manager.py, frontend/src/pages/accounts/Accounts.tsx, frontend/src/api/accounts.ts

## ACCOUNT-A Item Identity

- Previous attempt sync_before_count: 0
- Previous attempt sync_after_count: 1
- Synced item found in local catalog: yes
- Synced item attributed to previous attempt: false
- Actual item created by previous attempt: false
- Duplicate risk from previous attempt: none
- Evidence:
  - ACCOUNT-A native sync returned total_count=0 and items_len=0 before the new publish retest.
  - Existing catalog row first-seen time was earlier than the previous publish attempt window.
  - Existing catalog row title, price, description, and account ownership did not match material_id=1.
- Synced item masked:
  - item_id_hash_prefix: a09b878ffbb4
  - title_hash_prefix: 11ca06291afe
  - description_hash_prefix: 359d7015f316
  - price: masked_nonmatching_price

## ACCOUNT-A Client Validation

- Root cause confirmed: yes
- Root cause: publish description contained emoji that the platform client rejected before final submit.
- Failure classification: platform_client_validation_error
- Blocking field: description
- Blocking message: contains_emoji
- Previous vague classification replaced: platform_validation_error -> platform_client_validation_error
- Fix applied:
  - Added publish text sanitization before form fill.
  - Removed emoji code point ranges before submit.
  - Switched description fill path to Playwright native fill plus input/change/blur dispatch for React state consistency.
  - Classified client-side visible validation texts with no publish request as platform_client_validation_error.

## Non-Submit Gate After Fix

- real_publish_clicked: false
- publish_request_sent: false
- publish_form_rendered: true
- image_upload_complete: true
- description_state_valid: true
- category_selected: true
- price_valid: true
- address_selected: true
- shipping_option_valid: true
- transaction_method_valid: true
- browser_native_validation_passed: true
- react_form_state_valid: true
- publish_button_found: true
- publish_button_enabled: true
- publish_button_trial_click_passed: true
- risk_verification_present: false
- error_text_count: 0
- blocking_text_count: 0

## ACCOUNT-A Real Publish Retest

- attempt_count: 1
- sync_before_count: 0
- duplicate_check: pass
- publish_button_clicked: true
- publish_request_sent: true
- publish_response: success
- publish_response_http_status: captured_by_native_flow
- publish_response_business_code: no_error_code_recorded
- publish_response_message_masked: present
- client_validation_error: false
- sync_after_count: 1
- new_item_detected: true
- new_item_attributed_to_attempt: true
- actual_item_created: true
- item_id_present: true
- item_id_hash_prefix: a7d0fcb3c92d
- duplicate_item_created: false
- publish_retest: pass

## ACCOUNT-B

- login_method: qr_or_official_verification
- native_qr_route_found: true
- frontend_account_management_flow_found: true
- account_b_real_publish: not_run
- account_a_cookie_used_for_account_b: false
- cookie_output: false
- login_session_created: false
- reason: The native /api/v1/qr-login/generate route returns a sensitive QR data URL and generic session. Creating it headlessly would not display the QR to the owner, while printing or saving the QR would expose a login credential. The correct safe owner action is to use the visible upstream account management QR login UI.
- owner_action: Open the local account management page, click Add account -> Scan login, and complete the official QR or verification flow in the visible UI. Do not send Cookie, Token, QR contents, or verification URLs to Codex.

## Code And Tests

- Files modified in this task:
  - D:/xianyu-upstream-delivery-chg0017/backend-web/app/services/xianyu_publisher.py
  - D:/xianyu-upstream-delivery-chg0017/tests/test_chg0017_publish_login_submit.py
- Existing candidate files from previous CHG-0017 stages remain modified and were not reverted.
- Targeted test: D:/xianyu/.venv/Scripts/python.exe -m pytest D:/xianyu-upstream-delivery-chg0017/tests/test_chg0017_publish_login_submit.py -q
- Targeted test result: 12 passed
- Syntax check: pass
- Candidate diff check: pass with LF/CRLF warning only
- validate_change: pass
- verify_repository: 599 passed, 1 existing Starlette/httpx warning, repository verification passed
- frontend_build: not_required

## Runtime

- candidate_compose_project: xianyu_chg0017_candidate
- containers_rebuilt: backend-web
- candidate_image_rebuilt: true
- backend-web image digest: sha256:d724e10de9e5289c6e70c86c57eaea7f3f1c749f227ce786d1ba84c46ce25d53
- backend-web container created: 2026-08-01T15:44:52.038401445Z
- runtime_hotpatched: false
- reproducible_deployment: true
- runtime_container_updated: true
- runtime_code_verified: true
- host source SHA256:
  - xianyu_publisher.py: 1F79AB454D1AB241ABF6A5B06784DDDA2C42E01F1E07D6224242639111A7EAC3
  - publish_execution_service.py: E8E1A70314CA41072708D077D8E12E36E5CEBB3A9D448B40B2795D48B9649E81
- container source SHA256:
  - xianyu_publisher.py: 1F79AB454D1AB241ABF6A5B06784DDDA2C42E01F1E07D6224242639111A7EAC3
  - publish_execution_service.py: E8E1A70314CA41072708D077D8E12E36E5CEBB3A9D448B40B2795D48B9649E81
- container_health: backend-web healthy
- ports:
  - 19000 listening
  - 28089 listening
  - 28090 listening
  - 18090 not listening
  - 8090 not listening

## Security

- plaintext_cookie_exposed: false
- cookie_logged: false
- cookie_committed: false
- cross_account_cookie_used: false
- verification_bypassed: false
- full_item_id_exposed: false
- request_headers_logged: false

## Git And PR

- commit_created: false
- push_performed: false
- PR #26: Draft/Open/Unmerged
- PR #26 HEAD: ed6ed1eefddaad92d9e79d17372fa7d00d778f87
- PR #26 checks: quality success, tests success, security success
- archive_performed: false
- T17 performed: false
