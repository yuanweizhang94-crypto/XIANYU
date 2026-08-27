# CHG-0035 Acceptance

Change ID: CHG-0035-password-login-canonical-recovery
Status: ARCHIVED

## Required Code Acceptance

- Existing password-login path remains the single owner; no second login/session/WebSocket implementation.
- Candidate Cookie must pass existing `safe_mtop_auth_probe` before persistence or WebSocket finalization.
- Canonical `account_id` must be the validated platform `unb`, never a guessed login identifier.
- Missing canonical `unb` fails closed.
- Existing canonical account is updated rather than duplicated and its business fields/relations are preserved.
- New canonical account, when genuinely absent, is created with validated platform `unb`.
- CookieManager receives only validator-produced Cookie material under canonical account id.
- The `validated_cookies` scope/NameError regression is eliminated.

## Required Recovery Acceptance

For `<CANONICAL_ACCOUNT_ID>`:

```text
FINAL_ACCOUNT_LOGIN_READY=true
FINAL_ACCOUNT_ENABLED=true
VALID_SESSION_PRESENT=true
AUTH_CANONICAL_READY=true
COOKIE_VALIDATED=true
PASSWORD_LOGIN_IDENTIFIER=<LOGIN_IDENTIFIER>
CANONICAL_XIANYU_USER_ID=<CANONICAL_ACCOUNT_ID>
WRONG_ACCOUNT_ID_MAPPING_FIXED=true
WEBSOCKET_FINALIZATION_SUCCESS=true
IM_AUTH_READY=true
FACE_VERIFICATION_REPEATED=false
```

The original account's remark/business configuration, item/order/Material/reply/scheduler relations must remain attached to canonical account `<CANONICAL_ACCOUNT_ID>`.

## Duplicate Cleanup Gate

Duplicate `<LOGIN_IDENTIFIER>` cannot be deleted or disabled before canonical recovery is proven. After acceptance, cleanup must be one of:

```text
MERGED
ARCHIVED
DISABLED
DELETED_SAFE
PENDING_SAFE_CLEANUP
```

Hard delete requires all unique business/reference checks to be proven empty and no unmigrated valid Session dependency. Any UNKNOWN -> `PENDING_SAFE_CLEANUP`.

## Runtime Acceptance

- Only required WebSocket component activation.
- Production runtime patched file must match the source candidate hash.
- WebSocket health returns healthy after activation.
- No MySQL/Redis/Frontend/Scheduler restart.
- No new password login/QR/face verification.

## Git Acceptance

- Targeted tests PASS.
- Related regression PASS.
- `python scripts/verify_repository.py` PASS or any unrelated pre-existing global debt is explicitly classified without being absorbed.
- `git diff --check` PASS.
- Exact task files committed once.
- Push without force.
- Remote branch SHA equals local commit SHA; otherwise preserve exact commit and report `PENDING_GITHUB_SYNC=true`.

## Stop Conditions

Any second human verification requirement, canonical identity mismatch, cross-owner mismatch, validator failure on the new Cookie, unknown runtime activation side effect, or unsafe duplicate dependency immediately stops further mutation.

## Final Production Acceptance

```text
PASSWORD_LOGIN_CANONICAL_IDENTITY_RECOVERY=PASS
LOGIN_IDENTIFIER_IS_NOT_CANONICAL_ACCOUNT_ID=true
PASSWORD_LOGIN_CANONICAL_ID_SOURCE=VALIDATED_PLATFORM_IDENTITY
PHONE_CAN_BE_LOGIN_IDENTIFIER=true
PHONE_MUST_NOT_BECOME_ACCOUNT_ID=true
WEBSOCKET_FINALIZATION_USES_VALIDATED_COOKIE=true
UNKNOWN_CANONICAL_ID_FAIL_CLOSED=true
CANONICAL_AUTH_VALID=true
CANONICAL_SESSION_VALID=true
CANONICAL_ACCOUNT_ENABLED=true
CANONICAL_ACCOUNT_ONLINE=true
IM_AUTH_READY=true
WEBSOCKET_CONNECTED_READY=true
FAIL_SYS_SESSION_EXPIRED_AFTER_RECOVERY=false
VALIDATED_COOKIE_SCOPE_NAMEERROR_AFTER_RECOVERY=false
FRONTEND_FRESH_READBACK_RENDERS_ONLINE=true
DUPLICATE_ACCOUNT_CLEANUP_STATUS=DISABLED
DUPLICATE_ACCOUNT_AUTH_OWNER=false
DUPLICATE_ACCOUNT_BUSINESS_ACTIVE=false
DUPLICATE_ACCOUNT_DELETE_PERFORMED=false
PRE_EXISTING_TEST_DEBT_NOT_ABSORBED=true
LOGIN_RECOVERY_COMPLETE=true
```

The duplicate recovery row remains disabled solely as historical recovery/audit evidence. Historical renewal logs are retained. No credential, Cookie, Token, password, verification payload, phone number, or real account identifier is stored in this archive evidence.

## Repository Verification Debt Classification

Post-archive repository verification completed with `631 passed / 3 failed`. The three failures are pre-existing and outside CHG-0035 scope:

```text
PRE_EXISTING_TEST_DEBT_NOT_ABSORBED=true
PRE_EXISTING_FAILURE_1=CHG-0020 historical patch hash lock mismatch
PRE_EXISTING_FAILURE_2=CHG-0030 historical patch hash lock mismatch
PRE_EXISTING_FAILURE_3=isolated-worktree Alembic path constant assumption
CHG0035_TARGETED_TESTS=12_PASSED
CHG0035_RELATED_REGRESSION=29_PASSED
```

No unrelated historical patch artifact or database-path test was modified to make CHG-0035 green.
