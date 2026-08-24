# CHG-0025 Design

Status: ARCHIVED

Change ID: CHG-0025-web-self-service-qr-account-recovery

## Design intent

Patch the existing QR route and existing Accounts UI only. Do not create a second QR/Login/Session/Cookie/WebSocket/readiness owner.

## Reuse decision

Decision: PATCH_UPSTREAM

The design patches only the existing Backend QR route/account-scope boundary and the existing Frontend Accounts adapter/UI. `qr_login_manager`, Account/Cookie persistence, Session lifecycle, WebSocket lifecycle, and CHG0023 readiness remain the sole existing owners; no second execution owner is created.

## Backend contract

`POST /api/v1/qr-login/generate` becomes account-scoped for website recovery by accepting one required `target_account_id`.

Generation sequence:

```text
authenticated XIANYU user
-> resolve current account ownership scope
-> find target_account_id through existing AccountService
-> reject missing/unauthorized target before QR owner call
-> existing qr_login_manager.generate_qr_code()
-> record session owner user id + target account id
-> return existing qr_code_url + session_id
```

QR_TARGET_ACCOUNT_OWNERSHIP_CHECK=true
QR_ACCOUNT_SCOPE_STRICT=true

Status sequence:

```text
GET /qr-login/status/{session_id}
-> require session owner == current user
-> existing qr_login_manager.get_session_status()
-> ordinary pending/scanned/expired/verification states are read-only
-> on protocol success, lock session
-> re-check session owner + target binding
-> read existing qr_login_manager session cookies
-> extract scanned unb
-> load authoritative target account through existing AccountService
-> require scanned unb to equal target authoritative identity
-> only then call existing AccountService.upsert_account_from_qr
-> require returned account id == target account id
-> only then invoke existing WebSocket restart for that same account
```

No new Session/Account/Cookie/WebSocket owner is introduced.

### Identity rule

For an existing target account, the accepted scanned identity is the existing account's authoritative `unb` when present; where historical rows identify the account directly by the same platform identity, `account_id` is the compatibility identity. The comparison is strict against that target account only; it never searches for and updates another account based on scanned `unb`.

If target identity cannot be proven, fail closed before `upsert_account_from_qr`.

Mismatch response marker:

`QR_IDENTITY_TARGET_MISMATCH`

Mismatch side effects:

```text
AccountService.upsert_account_from_qr calls=0
Cookie persistence calls=0
Session mutation calls=0
WebSocket start/restart calls=0
```

### Session ownership

Unknown session, owner mismatch, or missing target binding fails closed. The previous `SESSION_OWNER.get(session_id, current_user.id)` fallback is removed from the account-scoped recovery path.

Session cleanup removes both owner and target bindings.

### QR refresh

Backend does not auto-regenerate QR. Expiry cleanup keeps normal existing semantics. A new QR is created only by a new explicit Frontend POST carrying the same target account id.

QR_AUTO_REGENERATION=false

## Frontend contract

Reuse the existing QR modal and existing account details/readiness authority.

### Account action visibility

Per-account recovery action is shown only when existing authoritative state indicates human QR recovery, at minimum:

- `browser_session_state === 'HUMAN_QR_REQUIRED'`, or
- existing business capability `auto_reply.state === 'LOGIN_REQUIRED'`, or
- existing publish capability `publish.state === 'QR_REQUIRED'`.

A healthy online account does not show recovery-required UI.

The global “添加新账号 -> 扫码登录” action is removed/disabled from this recovery flow because CHG0025 is for existing account recovery and every QR session must have a target account.

### Modal state

The QR modal stores both:

- `qrTargetAccountId`
- `qrSessionId`

`generateQRLogin(targetAccountId)` sends only the target account id; no Cookie/Token/password is part of the Frontend request.

Explicit refresh calls `generateQRLogin(qrTargetAccountId)` only after the user clicks refresh.

### Polling

Polling remains approximately every two seconds and calls only the existing QR status GET.

QR_STATUS_POLLING_AUTH_WRITE_COUNT=0

Polling must not call generate, Session maintain, Cookie refresh, Token refresh, or password login.

### False-green prevention

QR protocol `success` or `already_processed` does not immediately render final success.

Flow:

```text
protocol success
-> qrStatus=checking_account_status
-> stop QR protocol polling
-> authoritative getAccountDetailsPaginated readback
-> locate qrTargetAccountId
-> apply existing CHG0023 readiness precedence
```

UI final precedence:

1. platform verification blocker
2. HUMAN_QR / no-credentials/login-required blocker
3. expired Session / temporary auth failure
4. connected + token_ready equivalent represented by existing `business_capabilities.auto_reply.state === 'ONLINE'`
5. temporary/offline/checking state

Only blocker-free existing `ONLINE` readiness may set final QR UI `success`.

If readback is not yet ONLINE, keep checking with a bounded read-only account-status polling window. No auth write is triggered by that polling.

## Test design

Deterministic tests must use callable behavior, mocks/spies, or executable extracted logic; pure string-presence assertions are insufficient for the owner safety gates.

Required cases:

1. HUMAN_QR account exposes recovery action.
2. healthy ONLINE account does not expose recovery requirement.
3. QR create carries correct target account.
4. target ownership is checked before QR owner generation.
5. A-account QR cannot update B-account.
6. scanned identity mismatch fails before Account/Cookie owner call.
7. mismatch leaves Session/Cookie/WebSocket owner call counts zero.
8. unknown/non-owner session is rejected.
9. ordinary status polling is read-only.
10. expired does not auto-regenerate.
11. explicit refresh preserves same target account.
12. protocol success does not immediately false-green.
13. platform verification remains a blocker after readback.
14. HUMAN_QR/login-required remains a blocker after readback.
15. final success waits for existing ONLINE authoritative readiness.
16. Frontend generate/status payloads contain no Cookie/Token/password.
17. unauthorized target is rejected before QR generation.
18. other-account auth/login/QR owner writes remain zero in deterministic harness.

## Deployment design

Backend candidate must be based on current accepted image:

`xianyu-chg0024-backend-web:item-sync-no-auth-recovery-20260823-r1`

Frontend candidate must be built from the exact proven current production Frontend source lineage whose deployed artifacts exactly match current production.

WEBSOCKET_REDEPLOY=false
SCHEDULER_REDEPLOY=false

Production acceptance must use synthetic/route/component tests and read-only account baselines only. It must not create or scan a real QR.

## Accepted T4 postimages

- `backend-web/app/api/routes/qr_login.py` SHA256 `674381601ec3dcd7970a64e6ccb5a6ad72bcacb951a33f8c3d9867a097a96b4a`
- `frontend/src/api/accounts.ts` SHA256 `4de4bd8923faf1930832a9df2a60d91a87487f2ab89c942fa1ba27ba5b2b8777`
- `frontend/src/pages/accounts/Accounts.tsx` SHA256 `5b4c9c790c502790c4f0da759698ec218a7ed94aedd509da26a68418f1a0d8ef`
- `frontend/src/types/index.ts` SHA256 `42b851df44745cbdaebf2376bdc2587b4b784ba4b7a7dffc2a71749b3bddc3cd`

The vendor patch is generated only from the four authoritative raw-byte preimages using a `core.autocrlf=false` fixture; no historical cumulative Frontend patch is embedded in CHG0025.
