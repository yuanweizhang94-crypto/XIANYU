# 2026-08-16 Restore upstream-native QR login semantics

## Execution contract

- User outcome: QR login success must persist the authoritative account/Cookie, start or restart the existing Auto Reply WebSocket once, and return success without eagerly authenticating Chat or probing Publisher.
- Confirmed blocker: XIANYU CHG-0018 bound `AccountService.converge_existing_consumers_after_login()` to both normal QR success and shared-QR success. That orchestration invalidated Chat auth state, called Chat `get_or_connect()`, could request a Local Web Token, delegate platform verification, read conversations, probe publish capability, and run a second convergence round.
- Smallest success test: for both QR success paths, Chat connect/token/CAPTCHA/conversation/publish-preflight calls are zero while exactly one of WebSocket start/restart is selected; normal Chat lazy `get_or_connect()` remains outside the QR path.
- Reuse decision: `PATCH_UPSTREAM`. Restore the current upstream route semantics instead of adding another login/session owner.
- Duplicate-development risk: low. No new QR service, Chat manager, Token service, CAPTCHA path, WebSocket manager, Profile owner, Scheduler, or Publisher is introduced.
- Rollback: restore the three pre-deployment Backend files or revert this incremental patch. No database schema or credential migration is involved.

## Current upstream evidence

- Upstream repository: `zhinianboke/xianyu-auto-reply`.
- Current upstream `main` / `HEAD` checked by `git ls-remote`: `bf252be357f5e4261b04ce2b7419c5574aaf1b55`.
- Inspected path at that SHA: `backend-web/app/api/routes/qr_login.py`.
- Native QR success sequence at that SHA: `upsert_account_from_qr` -> existing WebSocket `/start` for a new account or `/restart` for an existing account -> record processed session -> return `扫码登录成功`.
- The inspected upstream QR route does not call Chat invalidation, Chat `get_or_connect`, Chat Token APIs, CAPTCHA, conversation list, publish preflight, or an auth-convergence second round.

## XIANYU regression evidence before repair

- Runtime `backend-web/app/api/routes/qr_login.py` called `converge_existing_consumers_after_login(..., trigger="qr_login_success")` immediately after QR account upsert.
- Runtime `backend-web/app/api/routes/shared_scan.py` called the same orchestration with `trigger="shared_qr_login_success"`.
- Runtime `backend-web/app/services/account_service.py` contained the QR-only convergence owner. A recursive runtime reference check found no callers outside those two QR success paths.
- The previous real QR run demonstrated the consequence: QR success updated the account, then eager Chat auth produced `FAIL_SYS_USER_VALIDATE` and the existing verification path ended at platform verification. No raw challenge URL or credential value is retained in this evidence.

## Minimal repair

- Normal QR route: restore the upstream-native direct WebSocket start/restart continuation after authoritative account/Cookie upsert and remove `auth_convergence` from the QR success response/cache.
- Shared QR route: apply the same post-login consumer semantics: authoritative account/Cookie upsert -> direct WebSocket start/restart -> success. No eager Chat or Publisher work.
- AccountService: remove the QR-only `converge_existing_consumers_after_login` owner, its private implementation, lease, lock, round deadlines, and convergence-only helpers because no runtime callers remain.
- Normal Chat functionality is not modified. Current runtime `backend-web/app/api/routes/chat_new.py` still contains the normal `/connect/{account_id}` path and `get_or_connect()` lazy connection owner.
- Token request shape, Token UA/headers/device ID, CAPTCHA solver, Auto Reply stability fix, WebSocket reconnect fix, PID/zombie handling, and Remote Token policy are untouched.

## Pre-deployment verification

- Modified runtime files: 3 (`qr_login.py`, `shared_scan.py`, `account_service.py`).
- Python compile: PASS for all three modified files.
- Focused runtime source tests against current upstream SHA: `6 passed`.
- Focused assertions for normal QR and shared QR: eager Chat connect calls 0, eager Token calls 0, eager CAPTCHA calls 0, publish preflight calls 0, conversation-list calls 0; one `/start` branch and one `/restart` branch exist under the mutually exclusive new/existing account condition.
- Incremental patch clean-apply against the recopied current production runtime baseline: PASS.
- Normalized content-equivalence after clean apply: 3/3 files match the prepared modified files.
- Incremental patch SHA256: `836D27F71612CF322460412DEBF59A85CD8431B3E0AB77098157E51701C75715`.

## Production validation rule

Deployment validation must not generate or scan a new QR and must not call Chat Connect, Local/Remote Token, or CAPTCHA. Validation is limited to source/route instrumentation, service health, existing Auto Reply connectivity, and post-deploy logs proving no eager QR auth work occurred during this task.
