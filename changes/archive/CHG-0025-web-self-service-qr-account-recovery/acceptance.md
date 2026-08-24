# CHG-0025 Acceptance

Status: ARCHIVED

Change ID: CHG-0025-web-self-service-qr-account-recovery

- [x] Exact current production Frontend source authority is proven before implementation.
- [x] Current accepted Backend QR route preimage authority is proven from the running CHG0024 image.
- [x] Existing QR/Login/Account/Cookie/WebSocket owner chain is reused; no parallel owner is designed.
- [x] `QR_ACCOUNT_SCOPE_STRICT=true`: every recovery QR session is bound to one existing target account.
- [x] `QR_TARGET_ACCOUNT_OWNERSHIP_CHECK=true`: unauthorized target is rejected before QR generation.
- [x] Scanned identity is validated against the target account before `AccountService.upsert_account_from_qr`.
- [x] `QR_IDENTITY_TARGET_MISMATCH` leaves Account/Cookie/Session/WebSocket mutation counts at zero.
- [x] Unknown/wrong-owner QR session fails closed; no fallback to current user ownership exists.
- [x] Existing QR polling remains read-only and cannot generate/refresh auth state.
- [x] Expired QR never automatically regenerates.
- [x] Explicit QR refresh preserves the same target account.
- [x] HUMAN_QR account UI exposes a per-account recovery action.
- [x] Healthy ONLINE account does not show a recovery-required action.
- [x] Frontend QR request carries target account only; no Cookie/Token/password material is sent or logged.
- [x] QR protocol success enters authoritative account-status checking instead of immediate UI success.
- [x] Platform verification and HUMAN_QR/login-required states remain blockers after readback.
- [x] Final UI success requires existing authoritative Auto Reply readiness `ONLINE` (the CHG0023 connected + token_ready truth) with no higher-priority blocker.
- [x] Deterministic test suite covers at least the 18 design cases with mocks/spies/executable logic rather than pure string tests.
- [x] Exact vendor patch contains only CHG0025 runtime files and replays to accepted postimages.
- [ ] Backend candidate is based on `xianyu-chg0024-backend-web:item-sync-no-auth-recovery-20260823-r1`.
- [ ] Frontend candidate is based on the exact current production Frontend source lineage.
- [ ] WebSocket and Scheduler are not redeployed.
- [ ] Production health is PASS after component activation.
- [ ] `REAL_QR_CREATE_COUNT=0` for the entire Change.
- [ ] `REAL_QR_SCAN_COUNT=0` for the entire Change.
- [ ] `PASSWORD_LOGIN_ATTEMPTS=0` for the entire Change.
- [ ] `REAL_MESSAGES_SENT=0` for the entire Change.
- [ ] `ADDITIONAL_ITEM_SYNC_INVOCATIONS=0`; total newly authorized T7 Item Sync invocations remains exactly 1.
- [ ] `2221422775489=HUMAN_QR_REQUIRED` at final readback.
- [ ] `2221501265279=HUMAN_QR_REQUIRED` at final readback.
- [ ] Healthy pre-existing accounts have zero Session/connected/token-ready/Auto Reply regressions.
- [ ] Other-account Session/Cookie/Token/Login/QR action counts attributable to CHG0025 are zero.
- [ ] `WEB_QR_ACCOUNT_ISOLATION=PASS`.
- [ ] `OTHER_ACCOUNTS_UNCHANGED=true`.
- [ ] `WEBSITE_USER_SELF_SCAN_READY=true` after production deployment and non-QR acceptance.
- [ ] CHG0025-specific targeted/CI failures are zero before merge.
- [ ] PR is merged with merge commit and fresh main readback contains the exact persisted change.

## Hard stop

Stop if exact production source authority becomes unproven, existing owner cannot be patched account-scoped, target identity cannot be validated before Cookie persistence, any cross-account credential write is possible, production deployment remains UNKNOWN, a healthy other account regresses, secret exposure is detected, or proof requires real QR/password/Item Sync execution.
