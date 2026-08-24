# CHG-0026 Tasks

Status: ARCHIVED

Change ID: CHG-0026-qr-dual-mode-and-chat-connectivity-recovery

- [x] T1 Fresh-resolve Wang/Zhou identity, read-only production states, causal windows, upstream QR semantics, and other-account baseline.
- [x] T2 Archive completed CHG0025 governance and create CHG0026 precheck without reopening or changing CHG0025 runtime behavior.
- [x] T3 Lock exact current production/source preimages and implement minimal existing-owner QR dual-mode + readiness/status patch.
- [x] T4 Run at least 21 deterministic QR/Chat/WS cases plus targeted regression/security checks.
- [x] T5 Build Backend/Frontend candidates only; keep WebSocket/Scheduler unchanged unless new evidence proves necessary.
- [x] T6 Deploy minimal components and run production acceptance with zero new executor QR create/scan and zero other-account auth writes.
- [x] T7 Persist exact vendor patch/evidence/state and validate repository with only pre-existing debt classified separately.
- [x] T8 Commit/push unique branch, create one PR, classify CI, merge with merge commit when CHG0026-specific gates are clean, and fresh-read main.

T1_COMPLETE=true
T2_COMPLETE=true
T3_COMPLETE=true
T4_COMPLETE=true
T5_COMPLETE=true
T6_COMPLETE=true
T7_COMPLETE=true
T8_COMPLETE=true

NEW_AUTOMATED_QR_CREATE_COUNT=0_REQUIRED
NEW_EXECUTOR_QR_SCAN_COUNT=0_REQUIRED
OTHER_ACCOUNT_AUTH_WRITES=0_REQUIRED
NO_NEW_WEBSOCKET_OWNER=true

PRODUCTION_ACCEPTANCE_FINAL=PASS
PRODUCTION_FREEZE=true
CHG0026_DETERMINISTIC_TESTS=45/45_PASS
CHG0023_REGRESSION=5/5_PASS
CHG0024_REGRESSION=8/8_PASS
CHG0025_REGRESSION=8/8_PASS
NEW_FINAL_PATCH_SHA256=405b762c1fa0256ed5cad80bc1170c771549c2026e6abf69b7ae0805027619e4
