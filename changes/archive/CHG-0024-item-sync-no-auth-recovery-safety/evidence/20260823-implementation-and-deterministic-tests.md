# 2026-08-23 CHG-0024 Implementation and Deterministic Tests

Change: CHG-0024-item-sync-no-auth-recovery-safety

## Exact T2 design

SAFE_MODE_NAME=`no_auth_recovery`
SAFE_MODE_TYPE=`bool`
PROPOSED_DEFAULT_VALUE=false
DEFAULT_BEHAVIOR_PRESERVED=true
PUBLIC_CALLER_AUTH_RECOVERY_CONTROL_REQUIRED=false
SAFE_MODE_AUTH_WRITE_COUNT_MODEL=0

PARAMETER_PROPAGATION_CHAIN=`existing /api/v1/items/get-all-from-account route -> ItemService.fetch_all_items_from_account -> _fetch_all_items_from_account_impl -> CALLSITE_1 and _reconcile_missing_active_items -> _confirm_missing_items_authoritatively -> CALLSITE_2`

FUNCTION_SIGNATURE_CHANGE_COUNT=5
FUNCTIONS_REQUIRING_SIGNATURE_CHANGE=`route fetch_all_items_from_account; ItemService.fetch_all_items_from_account; ItemService._fetch_all_items_from_account_impl; ItemService._reconcile_missing_active_items; ItemService._confirm_missing_items_authoritatively`
FUNCTIONS_REQUIRING_LOGIC_ONLY_CHANGE=`same existing owner functions only; _converge_session_for_item_status remains unchanged`
PLANNED_NEW_FUNCTIONS_COUNT=0
PLANNED_NEW_ITEM_OWNER_COUNT=0
PLANNED_NEW_SERVICE_COUNT=0
PLANNED_NEW_ROUTE_COUNT=0
PLANNED_NEW_SCHEDULER_COUNT=0
PLANNED_NEW_WORKER_COUNT=0

ROUTE_CHANGE_REQUIRED=true
ROUTE_NEW_FIELD=`no_auth_recovery` query parameter
ROUTE_NEW_FIELD_IS_ITEM_SPECIFIC=true

The existing request schema file is intentionally not changed. The route accepts an Item-specific query flag with default false. Safe mode fails closed when the route is invoked without a single `cookie_id`; the historical global/multi-account behavior remains unchanged when the flag is false.

## CALLSITE_1 exact contract

CALLSITE_1_CURRENT_EXACT_CODE_LOCATION=`common/services/item_service.py::_fetch_all_items_from_account_impl first-page failure branch`
CALLSITE_1_PROPOSED_BRANCH=`page_number == 1 and _item_failure_needs_session_convergence(message) and not no_auth_recovery`
CALLSITE_1_SAFE_RESULT_SEMANTICS=`skip convergence and fall through to the existing success=False/message failure response; no auth-dependent retry`

## CALLSITE_2 exact contract

CALLSITE_2_CURRENT_EXACT_CODE_LOCATION=`common/services/item_service.py::_confirm_missing_items_authoritatively session_or_verification_required branch, reached from _reconcile_missing_active_items`
CALLSITE_2_EXISTING_PRESERVE_UNKNOWN_MECHANISM=`PLATFORM_STATUS_UNKNOWN + confirmed=false + preserve_previous=true`
CALLSITE_2_RESULT_MODEL_EXTENSION_REQUIRED=false
CALLSITE_2_SAFE_RESULT_SEMANTICS=`skip convergence/reprobe and preserve the prior local platform status; in safe mode _reconcile_missing_active_items does not pre-mark missing items as NOT_IN_ACTIVE_LIST before authoritative confirmation`

This prevents an authentication/verification failure from falsely converting a previously ACTIVE local item into a remotely removed/missing item.

## T3 exact owner patch

PERSISTENCE_MODEL=EXACT_VENDOR_PATCH_OVER_CURRENT_OWNER_PREIMAGE
PATCH_PATH=`vendor/patches/xianyu-auto-reply/chg0024-item-sync-no-auth-recovery-safety.patch`
PATCH_SHA256=`3a34f322be2cd18c789907ba48bc381a76ac513c00a9cfc102aa0252be759471`
PATCH_RUNTIME_FILE_COUNT=2
PATCH_RUNTIME_FILES=`backend-web/app/api/routes/items.py; common/services/item_service.py`
NON_CHG0024_HUNKS=0
GIT_BINARY_PATCH_COUNT=2

PREIMAGE_ITEM_ROUTE_SHA256=`5be558b4c01cc14b99a88dde19c8f8a9c2f890aedbd132f0bc97dbf464a5d78a`
POSTIMAGE_ITEM_ROUTE_SHA256=`80dfc3bd8d9cbf8517ba1f167ea1c7fe49a80daf7218e3541bf0a7e92496d3c0`
PREIMAGE_ITEM_ROUTE_GIT_BLOB=`fb01db4f3f6c05782f8f38f6724d6f12592fea53`
POSTIMAGE_ITEM_ROUTE_GIT_BLOB=`11611b7fb9c5d949e0a3b6f0c238056e4c3f6260`

PREIMAGE_ITEM_SERVICE_SHA256=`5a875adc11adb6b19320206a4e9c34cd63453f9c5f35be482bf055574325b517`
POSTIMAGE_ITEM_SERVICE_SHA256=`bdcb41ec1eac703836f0711f53eb18e938724174b2f40c849eac744cb7786225`
PREIMAGE_ITEM_SERVICE_GIT_BLOB=`e9961e6dc38a1e518c0c073aa017f6ed2062a535`
POSTIMAGE_ITEM_SERVICE_GIT_BLOB=`3fff8394c9d12cbd5df204b870675e1a2eec4401`

Normalized human-readable diff audit: route = 2 hunks / 7 changed lines; ItemService = 10 hunks / 42 changed lines. No Session/Cookie/Token/WebSocket/Chat/Publisher/Scheduler owner is part of the artifact.

PATCH_APPLY_CHECK=PASS
PATCH_CLEAN_APPLY=PASS
PATCH_REPLAY_POSTIMAGE_MATCH=true

## T4 behavior tests

The behavior harness imported the exact postimage ItemService with only infrastructure/model dependencies stubbed and used mock/spy controls against the actual postimage methods.

TEST_1=`default_mode_preserves_existing_convergence_behavior` PASS; convergence calls=1 for a modeled session-expired first-page failure.
TEST_2=`safe_mode_first_page_auth_failure_never_calls_convergence` PASS; convergence calls=0.
TEST_3=`safe_mode_first_page_failure_has_no_auth_dependent_retry` PASS; remote page-fetch calls=1.
TEST_4=`safe_mode_missing_item_session_required_never_calls_convergence` PASS; convergence calls=0 and prior platform status preserved.
TEST_5=`safe_mode_missing_item_unconfirmed_never_marks_local_item_missing` PASS; local prior ACTIVE state preserved.
TEST_6=`safe_mode_human_qr_model_auth_writes_zero` PASS; modeled QR-required message causes convergence/auth-owner calls=0.
TEST_7=`changed_owner_has_no_remote_listing_mutation_calls` PASS.
TEST_8=`binary vendor patch clean replay produces exact postimages` PASS.

DEFAULT_MODE_REGRESSION=PASS
SAFE_MODE_TESTS=PASS
PATCH_REPLAY=PASS
BEHAVIOR_TESTS_REQUIRED=true
PATCH_PERSISTENCE_TESTS_REQUIRED=true

## COMPANY T5 decision and source persistence

COMPANY_T5_REQUIRED=true
PUBLIC_TOOL_SCHEMA_CHANGED=false
THIN_ADAPTER_ONLY=true
NO_NEW_TOOL=true
NO_NEW_OWNER=true

The existing `xianyu_item_sync` public schema remains exactly `account_id`, `page_size`, and `max_pages`. The trusted mapping alone is changed to call `/api/v1/items/get-all-from-account?no_auth_recovery=true`.

COMPANY_RUNTIME_AUTHORITY_BASE=`777897b859c7e05cb1fed58a713ad73d04041b9b`
COMPANY_T5_SOURCE_COMMIT=`c2cbaae2e658c371a950db56a4ac1cad4e7e2bce`
COMPANY_T5_SOURCE_REMOTE_MATCH=true
COMPANY_T5_RUNTIME_ACTIVATED=false

## Backend candidate

CANDIDATE_IMAGE=`xianyu-chg0024-backend-web:item-sync-no-auth-recovery-20260823-r1`
CANDIDATE_IMAGE_ID=`sha256:923cc15d72900c7f6af3d3bd9a9bd3aeb0bccb80a9ac2af2cf307deea07cf1fb`
CANDIDATE_CONFIG_DIGEST=`sha256:6e7b485b4b81a5986e14843b54c3c3e8211892614417d09c348e40b3a040dc8d`
CANDIDATE_BASE_LAYER_PREFIX_MATCH=true
CANDIDATE_BASE_LAYER_COUNT=85
CANDIDATE_LAYER_COUNT=87
CANDIDATE_TARGET_POSTIMAGES_MATCH=true
CHG0023_COOKIES_OWNER_PRESERVED=true
SESSION_COOKIE_OWNER_FILES_PRESERVED=true

## Predeploy gates completed so far

CHG0024_POSTIMAGE_BEHAVIOR_TESTS=`7/7_PASS`
CHG0023_READINESS_REGRESSION=`5/5_PASS`
CHG0022_ARCHIVED_REGRESSION=`4/4_PASS`
SECURITY_SCAN=PASS
DUPLICATE_CAPABILITY_VALIDATION=PASS
NO_SECRET_EXPOSURE=true

At this evidence point no Backend replacement, Item Sync, QR action, real message, Session maintain, Cookie refresh, or Token refresh has been performed by CHG-0024.
