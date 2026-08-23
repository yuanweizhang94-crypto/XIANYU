# CHG-0025 Production Non-QR Activation and Isolation

Date: 2026-08-23 Asia/Taipei

T7_COMPLETE=true
T8_COMPLETE=true
PRODUCTION_DEPLOYED=true
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0
QR_SUCCESS_COUNT=0
PASSWORD_LOGIN_ATTEMPTS=0
REAL_MESSAGES_SENT=0
ADDITIONAL_ITEM_SYNC_INVOCATIONS=0
TOTAL_NEW_T7_ITEM_SYNC_BUSINESS_INVOCATIONS=1

## Backend activation

Existing COMPANY `xianyu_backend_replace_image` transaction owner was used exactly once.
OLD_BACKEND_IMAGE_ID=sha256:923cc15d72900c7f6af3d3bd9a9bd3aeb0bccb80a9ac2af2cf307deea07cf1fb
NEW_BACKEND_IMAGE_ID=sha256:e50e217bd784d3dfbbd857b0f943aed9674c3a63ed02de053ff9dd013c1ef818
BACKEND_REPLACE_OUTCOME=SUCCESS
BACKEND_REPLACE_HEALTH_HTTP=200
BACKEND_SECRET_BINDING_PRESERVED=true
BACKEND_REPLACE_RETRY_COUNT=0

## Frontend activation

No Frontend replace-image lifecycle owner exists. The already-running production Frontend is itself an established static-hotfix runtime. CHG0025 therefore used the same narrow static-artifact model: two new uniquely named compat chunks were copied and byte-verified first; then a single index.html selector update activated the new Accounts chunk. The Frontend container was not restarted and all existing static artifacts remained in place.
FRONTEND_STATIC_DEPLOY_WRITE=SUCCESS
FRONTEND_CONTAINER_RESTART_COUNT=0
ORDERS_IMPORTMAP_PRESERVED=true
ACCOUNTS_IMPORTMAP_ACTIVE=true
FRONTEND_HTTP_INDEX_SHA256=ce6b909ffe05da6b4e9af97f933f751f3bffa41a9df9b290a0abe9d855444e69

## Non-QR acceptance

BACKEND_HEALTH_HTTP=200
WEBSOCKET_HEALTH_HTTP=200
FRONTEND_HEALTH_HTTP=200
QR_GENERATE_REQUEST_BODY_REQUIRED=true
QR_GENERATE_REQUIRED_FIELD=target_account_id
QR_GENERATE_SUCCESS_LOG_COUNT=0
QR_LOGIN_SUCCESS_LOG_COUNT=0
PASSWORD_LOGIN_LOG_COUNT=0
WEBSOCKET_QR_ACCOUNT_START_COUNT=0
WEBSOCKET_QR_ACCOUNT_RESTART_COUNT=0
RECONNECT_LOOP=false
REAL_MESSAGES_SENT=0

WebSocket and Scheduler container StartedAt values were unchanged across CHG0025 deployment, proving no redeploy/restart.

## Account isolation

Pre/post WebSocket main-process status:
- 2804730247: running=true connected=true token_ready=true (unchanged)
- 1951966327: running=true connected=true token_ready=true (unchanged)
- 2214313339860: running=true connected=true token_ready=true (unchanged)
- 2196106636: running=true connected=true token_ready=true (unchanged)
- 2219319284219: running=true connected=false token_ready=false human_qr_required=true (pre-existing blocker unchanged)

The DB `session_maintenance.state` for 1951966327 is `SESSION_CHECK_PENDING` with updated_at `2026-08-23T14:11:04.889423+00:00`, which predates CHG0025 Backend activation at `2026-08-23T14:12:34.569286933Z`; therefore that weak Session-state transition was not caused by CHG0025. Auto Reply transport remained connected/token_ready throughout.

Final controls:
- 2221422775489: status=disabled, authoritative Session=HUMAN_QR_REQUIRED, WebSocket not_started
- 2221501265279: status=disabled, authoritative Session=HUMAN_QR_REQUIRED, WebSocket not_started

OTHER_ACCOUNT_SESSION_WRITE_COUNT=0_CHG0025_DEPLOY_ACTIONS
OTHER_ACCOUNT_COOKIE_WRITE_COUNT=0_CHG0025_DEPLOY_ACTIONS
OTHER_ACCOUNT_TOKEN_WRITE_COUNT=0_CHG0025_DEPLOY_ACTIONS
OTHER_ACCOUNT_LOGIN_ACTION_COUNT=0
OTHER_ACCOUNT_QR_ACTION_COUNT=0
WEB_QR_ACCOUNT_ISOLATION=PASS
OTHER_ACCOUNTS_UNCHANGED=true
WEBSITE_USER_SELF_SCAN_READY=true
