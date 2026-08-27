# CHG-0035 Password Login Canonical Recovery

Change ID: CHG-0035-password-login-canonical-recovery
Status: ARCHIVED
Created: 2026-08-27
Owner task: account-<CANONICAL_ACCOUNT_ID>-login-recovery
Owner approval: explicit repair instruction supplied by project owner on 2026-08-27.

## User Outcome

User outcome: recover the already-successful password/face login for canonical XIANYU account `<CANONICAL_ACCOUNT_ID>`, keep the phone login identifier separate from canonical identity, restore valid Session/Auth/WebSocket/IM, and prevent recurrence without another login/QR/face verification.

Confirmed blocker: password login persisted the request login identifier as `XYAccount.account_id` even though the validated Cookie identifies canonical `unb=<CANONICAL_ACCOUNT_ID>`; finalization then referenced validator-local `validated_cookies` outside its scope and failed WebSocket startup with `NameError`.

Smallest success test: when `login_identifier != validated Cookie unb` and canonical account already exists, password-login persistence updates that canonical account only, preserves its business fields, creates no phone-keyed canonical account, and passes the validator-produced Cookie to CookieManager; missing canonical `unb` fails closed and validation failure never starts WebSocket.

## Development Precheck

```text
TASK_TYPE=REPAIR
FAILURE_REASON=PASSWORD_LOGIN_PHONE_USED_AS_ACCOUNT_ID + WEBSOCKET_FINALIZATION_VALIDATED_COOKIES_UNDEFINED
RESPONSIBLE_LAYER=XIANYU
CURRENT_UPSTREAM_CAPABILITY=password login + Cookie persistence + QR canonical unb identity + WebSocket CookieManager
CURRENT_LOCAL_CAPABILITY=validated password-login Cookie via safe_mtop_auth_probe + stale-response protections
CURRENT_RUNTIME_CAPABILITY=successful password/face login and validated Cookie acquisition, but wrong account-key persistence and finalization NameError
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=true
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=websocket/app/api/routes/password_login.py::_save_login_result
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=it writes by request account_id instead of validated platform identity and loses validated_cookies scope before CookieManager finalization
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=false
```

## Scope

Allowed:

- patch the existing upstream-native password-login persistence/finalization path only;
- derive canonical account identity from the already validated Cookie's `unb` and fail closed when absent;
- update an existing same-owner canonical account or create it by validated platform `unb` when absent;
- preserve canonical account business configuration while updating only login/auth metadata;
- pass only validator-produced Cookie material to existing CookieManager finalization;
- targeted regression tests for canonical identity and validated-cookie finalization;
- sanitized one-time recovery of the already validated Session/Cookie from duplicate `<LOGIN_IDENTIFIER>` to canonical `<CANONICAL_ACCOUNT_ID>` after read-only validation;
- targeted WebSocket runtime activation and authoritative readback;
- safe duplicate cleanup only after complete acceptance.

Forbidden:

- another password login, QR, face verification, CAPTCHA or second Cookie acquisition;
- raw Cookie/password output or persistence in Git/evidence;
- deleting or disabling canonical account `<CANONICAL_ACCOUNT_ID>`;
- overwriting canonical business config, items, orders, Material, replies or scheduler state;
- deleting duplicate `<LOGIN_IDENTIFIER>` before migration and authoritative recovery acceptance;
- new login service, new Session/Cookie owner, new WebSocket owner or COMPANY business implementation;
- broad refactor, MySQL/Redis restart, other-account changes, publish/message/order actions.

## Upstream capability audit

Upstream password login already exists and is the correct owner. Upstream QR/shared-scan account creation uses validated `unb` as canonical account identity. The password-login path differs by using the caller-provided account id and therefore needs a minimal `PATCH_UPSTREAM` alignment, not a second login implementation.

## Pinned upstream evidence

Pinned upstream/local runtime lineage for this repair is the already-validated password-login preimage with SHA256 `0db14da5fc5440572b69ecae3e122e95c47c19c3bae792c3168f8829549a0551`, currently baked in `xianyu-chg0023-websocket:readiness-contract-20260822-r1`. Current upstream supplies the owner path but not the local auth-cookie safety overlay, so this repair is applied only as a delta on that proven preimage.

## Existing local implementation search

Existing local/runtime capability already provides password login, `safe_mtop_auth_probe`, canonical Cookie validation, stale-response fingerprint protection, `XYAccount`, `TokenCache`, CookieManager and WebSocket finalization. Search found no second login/session owner to reuse and no existing canonical-id correction for password login; the defect is inside the existing `_save_login_result` path.

## Reuse decision

Decision: PATCH_UPSTREAM.

Reuse `safe_mtop_auth_probe`, `XYAccount`, `TokenCache`, existing CookieManager, existing account/session lifecycle, and existing WebSocket task owner. No parallel capability is introduced.

## Duplicate implementation risk

Risk is high if this repair creates a second login, Cookie store, Session owner, account mapping table or WebSocket finalizer. CHG-0035 therefore changes only the existing password-login persistence/finalization behavior and keeps all existing owners.

## Why upstream cannot satisfy the requirement

The current upstream password-login implementation still treats the caller-provided login identifier as `account_id` and does not contain the local validator/fingerprint safety overlay already deployed in production. Direct upstream replacement would regress local safety and would still not safely recover the current canonical account/session binding.

## Approved exception ADR

Not applicable. No `BUILD_LOCAL_EXCEPTION` is requested or authorized.

## Component owner

XIANYU existing password-login / Account / Session / CookieManager path. COMPANY remains transport/runtime infrastructure only.

## Retirement plan for overlapping local code

No overlapping implementation is added, so no retirement migration is required. The duplicate phone-keyed account is data fallout from the defect and is handled only after canonical auth acceptance; it is not retained as a second owner.

## Runtime Lineage

Production WebSocket image before repair: `xianyu-chg0023-websocket:readiness-contract-20260822-r1`.

Production `websocket/app/api/routes/password_login.py` SHA256 before repair: `0db14da5fc5440572b69ecae3e122e95c47c19c3bae792c3168f8829549a0551`.

The exact same file exists in the previously validated local auth-cookie overlay, so the repair must be a minimal delta on that preimage rather than an upstream whole-file replacement.

## Rollback

Code rollback: restore the exact preimage file/image above.

Data rollback safety: do not delete the duplicate before canonical recovery is proven. One-time migration must be atomic, validated, owner-matched, and preserve the old canonical auth material in a reversible protected location/row until post-activation acceptance is complete.

## Stop Conditions

STOP if validated new Cookie is no longer `AUTH_VALID`, canonical `unb` is not `<CANONICAL_ACCOUNT_ID>`, another human verification appears, owner identity mismatches, runtime activation becomes UNKNOWN, or any duplicate-account unique business dependency is discovered that cannot be safely reconciled.
