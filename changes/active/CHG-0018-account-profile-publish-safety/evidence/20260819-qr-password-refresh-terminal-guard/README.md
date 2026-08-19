# 2026-08-19 QR password-refresh terminal guard

Decision: `PATCH_UPSTREAM`.

## Execution contract

- User outcome: once the exact authoritative Cookie has been evidence-qualified `HUMAN_QR_REQUIRED`, no background Session/Auto Reply caller may keep launching password-login recovery for that same Cookie.
- Confirmed blocker: after the Auto Reply remote self-heal/QR terminal-state fixes, production logs still showed external Session maintenance calling `POST /internal/accounts/{account_id}/password-login-refresh` for the QR-required accounts. Because those Auto Reply instances were not initialized, the route fell through to the existing standalone password-login path.
- Smallest success test: the existing `password-login-refresh` route must check the same authoritative QR predicate before `password_login_state.start_processing()`, background task creation, or standalone password login. QR-required requests must return the stable `HUMAN_QR_REQUIRED` state immediately.

## Repair

The existing route is minimally patched. It reuses `get_account_by_identity()` and `is_human_qr_required_for_cookie()`; no new login service, Session owner, Token owner, table, worker, scheduler, API route, or browser flow is introduced.

For the current exact authoritative Cookie:

```text
HUMAN_QR_REQUIRED
→ password-login-refresh route returns immediately
→ password_login_state.start_processing = not reached
→ _execute_password_login_refresh = not scheduled
→ _standalone_password_login = not reached
→ wait for official QR
```

When the authoritative Cookie changes after a legitimate official login/QR, the fingerprint-qualified QR predicate becomes false and the existing bounded recovery behavior is available again.

## Direct production evidence

Before this follow-up, logs showed for `1034641456` and `2219319284219`:

```text
password-login-refresh request
→ password_login_state.start_processing
→ CookieTokenManager not initialized
→ standalone password login
```

After the route guard and fixed-target WebSocket reload, controlled calls for both accounts returned:

```text
1034641456    message=HUMAN_QR_REQUIRED status=human_qr_required
2219319284219 message=HUMAN_QR_REQUIRED status=human_qr_required
```

Post-call logs showed the route-level refusal and did not show `password_login_state.start_processing` or standalone password login for those controlled calls.

Healthy Auto Reply owners resumed normal heartbeats after reload, including `2196106636`, `2214313339860`, `2217936413500`, and `2221501265279`.

## Validation

- Runtime `py_compile`: PASS for `internal.py`, `cookie_token_manager.py`, and `xianyu_async.py`.
- Fixed-target WebSocket reload: HTTP 200.
- Controlled QR-required route test: 2/2 PASS.
- Rebuildable WebSocket image: `xianyu-chg0018-websocket:auth-cookie-closure-20260819-r4`.
- r4 build: PASS.
- r4 offline `network_mode:none` validation: `HASH_MATCH files=18`, `PY_COMPILE_PASS`, `WRITER_INVENTORY_PASS missing_expected=0 unknown_direct=0`.
- r4 manifest-list digest observed during build: `sha256:20694990c822317ef2b39238cb046493551a4b21d7aca1eb4cf7116c88434fab`.

## Locked artifacts

- Delta patch SHA256: `f8f318a6ef8278d9c955d1a6d3dfc924add622764ded95261eb09e184db8a9c4`.
- Final `websocket/app/api/routes/internal.py` SHA256: `76692905b87cff85476a36c3d9a2f65139ef9a05641ead92dd44859d56e66167`.

## Safety

```text
PRODUCT_ACTIONS=0
PUBLISH_CALLS=0
ITEM_MUTATIONS=0
CUSTOMER_MESSAGES_SENT=0
QR_ACTIONS=0
CAPTCHA_BYPASS=0
AUTOMATIC_PAYMENT=0
CREDENTIAL_SECRET_OUTPUT=0
```

## Repository verification note

- Targeted follow-up + prior remote-self-heal regression tests: `8 passed`.
- Full `python scripts/verify_repository.py`: `653 passed / 14 failed / 1 warning`.
- The 14 failures are the same pre-existing latest-remote baseline group: AI handoff encoding/regression invariant assertions, historical locked patch byte-hash mismatches under Windows checkout normalization, and isolated-worktree Alembic path binding. This follow-up does not modify those baseline files and introduced no additional failure.
- Ordinary staged files pass `git diff --cached --check`. The locked `.patch` artifact itself reports two trailing-whitespace lines because it faithfully preserves the source blank-line indentation; its staged SHA256 exactly matches the locked hash above, so it is retained unchanged under the repository's immutable-patch exception.

This follow-up closes the observed automatic password-login re-entry for evidence-qualified QR accounts. Genuine Session expiry still legitimately requires official QR when the existing bounded official renewal chain cannot restore authentication.
