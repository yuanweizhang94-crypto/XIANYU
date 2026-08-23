# CHG-0025 Backend Account-Scope Implementation

Date: 2026-08-23 Asia/Taipei

BACKEND_IMPLEMENTATION_COMPLETE=true
QR_ACCOUNT_SCOPE_STRICT=true
QR_TARGET_ACCOUNT_OWNERSHIP_CHECK=true
QR_SESSION_TARGET_IMMUTABLE=true
QR_IDENTITY_PREWRITE_GUARD=true
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0

The existing `qr_login_manager` remains the sole QR owner. `/qr-login/generate` requires `target_account_id`, checks ownership before QR-owner generation, and stores immutable server-side `session_id -> owner + target` metadata. `/status/{session_id}` rejects unknown/wrong-owner sessions and no longer falls back to `current_user.id`.

On synthetic protocol success the scanned `unb` is compared against the target account's authoritative identity and exact target row before `AccountService.upsert_account_from_qr`. A mismatch returns `QR_IDENTITY_TARGET_MISMATCH`; deterministic spy counters prove Account/Cookie/Session/WebSocket writes are zero on mismatch.

BACKEND_POSTIMAGE_SHA256=674381601ec3dcd7970a64e6ccb5a6ad72bcacb951a33f8c3d9867a097a96b4a
BACKEND_DETERMINISTIC_TESTS=10/10_PASS
