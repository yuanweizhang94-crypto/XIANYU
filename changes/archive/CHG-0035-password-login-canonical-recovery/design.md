# CHG-0035 Design

Change ID: CHG-0035-password-login-canonical-recovery
Status: ARCHIVED

## Execution Contract

User outcome: recover the already-successful login into canonical account `<CANONICAL_ACCOUNT_ID>` with no repeated human verification.

Confirmed blocker: request/login identifier `<LOGIN_IDENTIFIER>` was persisted as `account_id` although the validated Cookie returns `unb=<CANONICAL_ACCOUNT_ID>`; finalization then referenced `validated_cookies` outside its validator scope.

Smallest success test: validated platform `unb` owns persistence and CookieManager startup, existing canonical business fields survive, phone-keyed duplicate creation is impossible, and missing/invalid validated identity fails closed.

## Existing Owner And Identity Model

The existing password-login route remains the owner. The correct canonical identity is the platform identity contained in the validated Cookie (`unb`). This is consistent with existing QR/shared-scan account persistence, where `unb` selects or creates the canonical `XYAccount`.

```text
INPUT_LOGIN_IDENTIFIER=phone/email/other login credential identifier
VALIDATED_COOKIE_UNB=platform canonical user identity
CANONICAL_ACCOUNT_ID=VALIDATED_COOKIE_UNB
```

The two values may be equal but equality is never assumed.

## Minimal Code Design

`_save_login_result` will:

1. Run existing `safe_mtop_auth_probe` on the candidate Cookie.
2. Require `status == AUTH_VALID`.
3. Take the validator-returned Cookie string as the only Cookie eligible for persistence/finalization.
4. Parse `unb` from that validated Cookie and require a non-empty canonical id.
5. Query/lock `XYAccount.account_id == canonical_account_id`.
6. Reject cross-owner ownership.
7. If canonical exists, update only auth/login fields and preserve business configuration/relations.
8. If canonical does not exist, create it with `account_id=canonical_account_id`, never the login identifier.
9. Invalidate TokenCache by canonical `unb`.
10. Return `is_new_account`, `canonical_account_id`, and the validator-produced Cookie out of the async save scope.
11. Call existing CookieManager using the canonical account id and validator-produced Cookie only.
12. Persist password-login session success with canonical account id.

No raw `cookies_str` fallback is allowed after validator success except inside the validator normalization step already used by the existing safety overlay.

## Concurrency / Stale Write Safety

The existing pre-login authoritative fingerprint remains applicable when the requested `account_id` already equals the validated canonical id. For the mismatch case, canonical identity is not trusted until validation returns `unb`; the canonical row is then locked before mutation. Cross-owner collision remains fail-closed.

No automatic deletion/merge of a noncanonical request-id row occurs inside normal password login. Duplicate cleanup remains an explicit post-recovery operation because it may contain audit/runtime state.

## One-Time Data Recovery Design

Current sanitized facts:

- canonical row `<CANONICAL_ACCOUNT_ID>` exists and carries original business config;
- its current Cookie probes `SESSION_EXPIRED`;
- duplicate row `<LOGIN_IDENTIFIER>` was created at the successful password-login timestamp;
- duplicate Cookie probes `AUTH_VALID` and returns canonical `unb=<CANONICAL_ACCOUNT_ID>`;
- both rows have the same owner;
- duplicate has no discovered items/orders/replies/business relations; one scheduled cookie-renew log is an audit/runtime log.

Recovery must run atomically and internally without printing secret values:

1. Re-read and lock both rows.
2. Re-run `safe_mtop_auth_probe` on duplicate Cookie inside the recovery transaction flow.
3. Require `AUTH_VALID`, `unb=<CANONICAL_ACCOUNT_ID>`, same owner, canonical row present.
4. Preserve canonical business fields and relations unchanged.
5. Move the validated auth/login metadata to canonical row.
6. Preserve the pre-recovery canonical Cookie in the duplicate row as rollback material while leaving duplicate otherwise non-business-active only after final acceptance.
7. Commit atomically.
8. Activate fixed WebSocket runtime and let existing CookieManager/WebSocket lifecycle consume canonical DB auth.
9. Prove canonical auth + IM/WebSocket success before any duplicate cleanup.

## Duplicate Cleanup Design

After complete canonical recovery, inspect references again. Prefer archive/disable if available. Hard delete is permitted only when all unique business and relation checks are zero/false and the runtime no longer depends on the duplicate. If any condition is UNKNOWN, cleanup remains `PENDING_SAFE_CLEANUP`.

## Runtime Activation

Only the WebSocket component contains the target code defect. Build a candidate from the currently running accepted WebSocket image and overlay only the patched `password_login.py` plus any self-contained targeted test artifact needed for build verification. Recreate only the fixed allowlisted WebSocket target through existing COMPANY infrastructure, preserving current runtime config/secrets without reading them.

Backend, Frontend, Scheduler, MySQL, Redis and other accounts are not restarted.

## Tests

Required code regression cases:

1. phone/login identifier differs from platform `unb`, canonical existing -> update canonical, no phone account create;
2. canonical absent -> create by platform `unb`, not login identifier;
3. login identifier equals platform `unb` -> compatible existing behavior;
4. validated platform `unb` missing -> fail closed;
5. validator success -> existing CookieManager receives validator-produced Cookie and canonical id;
6. validator failure/missing validated Cookie -> WebSocket finalization does not start;
7. no `validated_cookies` NameError regression.

Required repository gates: targeted tests, related regression, Python compile, `python scripts/verify_repository.py`, `git diff --check`.

## Security

No Cookie, Token, password, Authorization, QR/face payload or browser Profile secret is written into Change evidence, tests, Git history or user-visible output.
