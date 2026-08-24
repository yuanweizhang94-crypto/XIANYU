# CHG-0027 Acceptance

Status: ARCHIVED

Change ID: CHG-0027-session-transient-classification-qr-cooldown-lineage

- [x] `SAFE_MTOP_NETWORK_ERROR + SESSION_RENEW_FAILED` does not produce Session expired/login/PVR.
- [x] Explicit `SAFE_MTOP_SESSION_EXPIRED` still blocks.
- [x] Explicit `FAIL_SYS_SESSION_EXPIRED` still blocks.
- [x] Explicit credential-invalid/login-required still fails closed.
- [x] Newer AUTH_VALID overrides stale transient-failure rendering.
- [x] WS connected/token-ready cannot override explicit expired evidence.
- [x] Auto Reply transient auth state renders checking/temporary, not Session expired or forced ONLINE.
- [x] Chat transient auth state renders checking/temporary, not LOGIN_REQUIRED.
- [x] Publisher auth capability recomputes from fresh authoritative truth and still fails closed on real HQR/PVR/expired.
- [x] Session-expired cooldown remains active for the same Cookie lineage within TTL.
- [x] New authoritative QR Cookie lineage invalidates the old Session-expired cooldown for that account.
- [x] Account A lineage change does not mutate account B cooldown.
- [x] Unrelated rate-limit/platform-verification/CAPTCHA/password-error cooldown/blockers are not cleared.
- [x] Scheduler restart cannot resurrect a stale pre-QR Session-expired cooldown.
- [x] Failed QR/CAS without authoritative Cookie change cannot clear the old cooldown early.
- [x] CHG0026 QR dual-mode/platform-verification/pending-no-false-green/Chat self-rehydration contracts regress cleanly.
- [x] Zhou fresh current Cookie is `AUTH_VALID`; no rescan/manual reconnect is performed.
- [x] All enabled accounts receive final Session/Auto Reply/Chat/Publish audit.
- [x] Synthetic Auto Reply routing/isolation passes with mocked outbound and `REAL_MESSAGES_SENT=0`.
- [x] Synthetic Publisher routing/isolation passes with mocked submit and `REAL_PRODUCTS_PUBLISHED=0` / `REAL_PRODUCTS_MODIFIED=0`.
- [x] Frontend static bundle/runtime wiring and four-second conditional polling contract match Backend truth; authorized real-browser rendering is explicitly split as an infrastructure follow-up.
- [x] `NEW_ITEM_SYNC_INVOCATION_COUNT=0`.
- [x] CHG0027 scoped production acceptance passes before formal Git freeze/delivery.

TRANSIENT_RENEW_FAILURE_IS_NOT_FATAL=true
EXPLICIT_SESSION_EXPIRED_STILL_BLOCKS=true
NEWER_AUTH_VALID_OVERRIDES_STALE_TRANSIENT_FAILURE=true
SESSION_FATAL_CLASSIFICATION_SINGLE_SEMANTICS=true
QR_SUCCESS_INVALIDATES_PREVIOUS_SESSION_EXPIRED_COOLDOWN=true
SESSION_EXPIRED_COOLDOWN_SCOPE_STRICT=true
COOLDOWN_INVALIDATION_ACCOUNT_SCOPE_STRICT=true
STALE_COOLDOWN_CANNOT_RESURRECT_AFTER_RESTART=true

DEFECT_A_ACCEPTANCE=PASS
DEFECT_B_ACCEPTANCE=PASS
CHG0027_SCOPED_PRODUCTION_ACCEPTANCE=PASS
ACCOUNT_RUNTIME_OVERALL_ACCEPTANCE=PARTIAL__FOLLOWUP_REQUIRED
PUBLISH_CAPABILITY_FINAL_ACCEPTANCE=SYNTHETIC_CAPABILITY_PASS__READINESS_CONVERGENCE_FOLLOWUP_REQUIRED
WEBSITE_UI_FINAL_ACCEPTANCE=STATIC_RUNTIME_WIRING_PASS__REAL_BROWSER_RENDER_BLOCKED
PRODUCTION_FREEZE=true
FOLLOWUP_DEFECTS_EXPLICITLY_PERSISTED=true
