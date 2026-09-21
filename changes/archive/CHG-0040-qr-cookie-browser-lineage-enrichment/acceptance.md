# CHG-0040 Acceptance

Change ID: CHG-0040-qr-cookie-browser-lineage-enrichment
Status: ARCHIVED

## Source gates

- Only backend-web/app/services/account_service.py is changed in the business patch.
- Existing CookieRenewBrowserService is reused.
- Browser enrichment occurs before existing-account CAS or new-account insert and commit.
- Enrichment failure performs no Account or Cookie commit.
- Existing safe-MTOP validation remains mandatory.
- Token lifecycle, Auto Reply, Publisher and product configuration are unchanged.

## Deterministic candidate evidence

CANDIDATE_COMPILE=PASS
DYNAMIC_SUCCESS_CASE=PASS
DYNAMIC_SUCCESS_ORDER=canonical_in_memory_merge_then_browser_renew_then_authoritative_commit_ENRICHED
DYNAMIC_NEW_ACCOUNT_CANONICAL_COOKIE_PERSISTED=PASS
DYNAMIC_EXISTING_CANONICAL_PRESERVATION=PASS
DYNAMIC_CAS_EXPECTED_FINGERPRINT=PASS
DYNAMIC_FAIL_CLOSED_CASE=PASS
DYNAMIC_FAIL_CLOSED_DB_COMMIT_COUNT=0

## Runtime preimage

PRODUCTION_BACKEND_SOURCE_MATCH=true for:
- backend-web/app/api/routes/qr_login.py
- backend-web/app/services/account_service.py
- common/services/cookie_renew_browser_service.py
- common/services/account_cookie_service.py

## Session failure evidence

ZHULIN_SESSION_STATE=HUMAN_QR_REQUIRED
ZHULIN_FAILURE_REASON=OFFICIAL_RENEWAL_FAILED_SAFE_MTOP_SESSION_EXPIRED
SIYA_SESSION_STATE=HUMAN_QR_REQUIRED
SIYA_FAILURE_REASON=OFFICIAL_RENEWAL_FAILED_SAFE_MTOP_SESSION_EXPIRED
TARGET_VISIBLE_LOGIN_UI=true
TARGET_USERNAME_PASSWORD_CREDENTIALS=false

CONTROL_SESSION_STATE=REAL_BROWSER_LOGIN_READY
TARGET_COOKIE_FIELD_COUNT=18
CONTROL_COOKIE_FIELD_COUNTS=27,30

## Current recovery gate

PLATFORM_SESSION_HARD_EXPIRED=true
HUMAN_QR_REQUIRED=true
REAL_E2E=PENDING_UNTIL_REPAIRED_QR_RECOVERY

## Production closure

CHG0040_SOURCE_AND_PRODUCTION_CLOSURE=PASS
PRODUCTION_IMAGE=xianyu-chg0040-backend-web:qr-cookie-enrichment-20260921-r3
RUNTIME_CODE_MATCH=true
BACKEND_HEALTH=PASS
FRONTEND_HEALTH=PASS
WEBSOCKET_HEALTH=PASS
SCHEDULER_HEALTH=PASS
COMMIT=d7ec1460c73b51580e494168ab90764c752cab7f
LOCAL_REMOTE_MATCH=true

Affected hard-expired accounts remain deferred to future authorized human QR recovery; this is non-blocking for CHG0040 source/production closure.
