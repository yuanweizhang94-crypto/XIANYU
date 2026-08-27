# CHG-0035 Tasks

Change ID: CHG-0035-password-login-canonical-recovery
Status: ARCHIVED

- [x] T1 Refresh XIANYU/COMPANY/ZIDONGZHUA Git/local/runtime minimum bootstrap and classify pre-existing dirty worktrees without modifying them.
- [x] T2 Prove the current successful login outcome, duplicate account creation, canonical platform `unb`, and WebSocket finalization NameError from direct Runtime evidence.
- [x] T3 Protect the scene and prove the duplicate's new Cookie is `AUTH_VALID` while the canonical account Cookie is `SESSION_EXPIRED`, without exposing secrets.
- [x] T4 Prove Runtime source lineage: production `password_login.py` matches the accepted CHG-0023 auth-cookie overlay preimage exactly.
- [x] T5 Create the only executable active CHG-0035 in an isolated worktree based on current `origin/main`.
- [x] T6 Patch existing password-login persistence so validated platform `unb` is canonical account id and validator-produced Cookie survives into existing CookieManager finalization.
- [x] T7 Add targeted regression coverage for canonical identity mapping, existing-account preservation, fail-closed missing identity/validation, and validated-cookie finalization.
- [x] T8 Run targeted tests, related Session/Cookie/WebSocket regression, Python compile, repository verify, and `git diff --check`.
- [x] T9 Revalidate the already successful duplicate Cookie and atomically rebind the existing Session/login metadata to canonical account `<CANONICAL_ACCOUNT_ID>`, preserving original business data and rollback material.
- [x] T10 Build and activate only the fixed WebSocket candidate from the accepted current runtime image; verify exact source/runtime hash and health.
- [x] T11 Read back `xianyu_account_status(<CANONICAL_ACCOUNT_ID>)`, canonical auth, WebSocket/IM via formal `xianyu_chat_connect`, and frontend/account state without another login.
- [x] T12 Recheck duplicate account unique references and perform only a safe merge/archive/disable/delete decision after canonical acceptance; UNKNOWN remains pending.
- [x] T13 Persist sanitized evidence, archive CHG-0035, regenerate project state, commit exact XIANYU task files, push without force, and verify remote SHA.
- [x] T14 STOP with the requested final recovery fields.

## Fixed Human Boundary

```text
PASSWORD_LOGIN_REPEATED=false
QR_REPEATED=false
FACE_VERIFICATION_REPEATED=false
SECOND_COOKIE_ACQUISITION=false
```

## Closure Classification

```text
PRODUCTION_ACCEPTANCE=PASS
DUPLICATE_ACCOUNT_CLEANUP_STATUS=DISABLED
DUPLICATE_ACCOUNT_DELETE_PERFORMED=false
PRE_EXISTING_TEST_DEBT_NOT_ABSORBED=true
HUMAN_ACTION_REQUIRED=false
```
