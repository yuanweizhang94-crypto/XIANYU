# CHG-0026 Acceptance

Status: VERIFYING

Change ID: CHG-0026-qr-dual-mode-and-chat-connectivity-recovery

- [x] Recovery QR requires target account and preserves all CHG0025 identity/ownership pre-write guards.
- [x] Recovery session cannot switch/downgrade to add-new mode.
- [x] Add-new QR allows no target, binds current authenticated user, and has immutable server-side mode.
- [x] Add-new preserves upstream same-owner update-existing else create-new semantics.
- [x] Add-new rejects scanned identity already owned by another XIANYU user before auth/WebSocket writes.
- [x] Global Add Account QR entry is restored and routes to ADD_NEW_ACCOUNT without generating a real QR during acceptance.
- [x] Existing-account QR recovery UI remains target-scoped and safe.
- [x] Expired QR never implicitly regenerates; explicit refresh preserves mode/target.
- [x] Canonical platform/HQR/session blockers outrank stale WebSocket connected/token-ready status.
- [x] Bare SESSION_CHECK_PENDING is checking/transitional and cannot false-green ONLINE.
- [x] Platform verification requires account-scoped explicit evidence; stale markers clear under newer settled truth.
- [x] Auth-valid connection-down state is distinct from auth-recovery-required.
- [x] Online Chat account list exposes authoritative blocker/connection state instead of generic disconnected only.
- [x] Wang was not rescanned or manually reconnected; R5 startup lifecycle automatically rehydrated Chat and conversations read succeeded.
- [x] Zhou was not scanned or manually reconnected; fresh auth-valid truth was accepted and R5 startup lifecycle automatically rehydrated Chat.
- [x] Ouyang stale persisted PVR no longer blocks healthy Chat.
- [x] Yilong current explicit platform challenge is absent, PVR is false, and conversations read succeeds; retained history cannot fully reconstruct its first historical PVR event.
- [x] Wanzi retains a real FAIL_SYS_USER_VALIDATE/RGV explicit platform-verification blocker and is not bypassed.
- [x] Other enabled accounts have zero Session/Cookie/Login writes attributable to CHG0026 Chat lifecycle and no false ONLINE/PVR regression.
- [x] WebSocket and Scheduler were not redeployed by CHG0026 R5.
- [x] `NEW_AUTOMATED_QR_CREATE_COUNT=0` and `NEW_EXECUTOR_QR_SCAN_COUNT=0`.
- [x] Deterministic source tests are `45/45_PASS`; CHG0023/24/25 regressions are `5/5`, `8/8`, `8/8` PASS.
- [x] Exact cumulative vendor patch applies cleanly, replays exact postimages, and contains exactly 12 approved runtime files.
- [ ] CHG0026-specific CI is clean before merge.
- [ ] PR merges with merge commit and fresh main readback contains exact persisted patch.

PRODUCTION_ACCEPTANCE_FINAL=PASS
CHAT_RUNTIME_PERSISTED=false
CHAT_RUNTIME_SELF_REHYDRATING=true
SESSION_PENDING_CANNOT_FALSE_GREEN=true
PLATFORM_VERIFICATION_REQUIRES_EXPLICIT_EVIDENCE=true
PLATFORM_VERIFICATION_ACCOUNT_SCOPE_STRICT=true
NO_CROSS_ACCOUNT_VERIFICATION_STATE_LEAK=true
UNKNOWN_CANNOT_ESCALATE_TO_PLATFORM_VERIFICATION=true
STALE_PLATFORM_VERIFICATION_BLOCKER_CLEARS=true
R5_STARTUP_CHAT_AUTH_WRITE_COUNT=0
OTHER_ACCOUNT_AUTH_REGRESSION_COUNT=0
NEW_FINAL_PATCH_SHA256=405b762c1fa0256ed5cad80bc1170c771549c2026e6abf69b7ae0805027619e4

## Hard stop

No further production write is permitted after acceptance freeze. Git/formal persistence must stop if patch bytes drift, scope expands, CHG0026-specific CI fails, or mergeability is false.
