# CHG-0025 Frontend Account-Scoped QR / No-False-Green Implementation

Date: 2026-08-23 Asia/Taipei

FRONTEND_IMPLEMENTATION_COMPLETE=true
QR_FALSE_GREEN_FORBIDDEN=true
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0

The existing Accounts QR modal is reused. `generateQRLogin(targetAccountId)` sends only `target_account_id`. Recovery UI is gated by existing HUMAN_QR/QR_REQUIRED authority; healthy ONLINE accounts do not show recovery-required actions. Modal state binds the target account and session. Expiry stops polling and requires explicit user refresh with the same target. QR status polling remains GET-only.

Protocol `success/already_processed` no longer renders immediate success. It enters bounded read-only authoritative account readback and uses existing CHG0023 business capability truth. Platform verification, HUMAN_QR, expired Session, disconnected, and token-not-ready states remain non-success. Only existing Auto Reply capability ONLINE with `online=true` reaches final success.

FRONTEND_TSC=PASS
FRONTEND_VITE_BUILD=PASS
FRONTEND_DETERMINISTIC_TESTS=18/18_PASS
