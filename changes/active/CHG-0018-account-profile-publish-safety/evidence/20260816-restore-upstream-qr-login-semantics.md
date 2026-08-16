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


## Production deployment acceptance

- GitHub repair commit before production mutation: `a6ea58fb374325cd9b69fd2c305d3a9d5d886dd9`; remote branch equality was verified before deployment.
- Deployment changed only the three Backend runtime files owned by the incremental patch: `qr_login.py`, `shared_scan.py`, and `account_service.py`.
- Container-level `py_compile` passed for all three files before Backend restart.
- Backend restart count for this task: 1. Backend health after restart: HTTP 200, database connected.
- WebSocket restart count for this task: 0. Its StartedAt remained `2026-08-16T12:07:29.527576652Z`.
- No QR was generated or scanned during production validation.
- Runtime source instrumentation after deployment: normal QR convergence calls 0; shared-QR convergence calls 0; convergence method definitions 0; QR/shared Chat `get_or_connect` calls 0; Token/cache invalidation calls 0; CAPTCHA calls 0; publish-preflight calls 0; conversation-list calls 0.
- Runtime source instrumentation preserves one normal-QR `/start` branch and one `/restart` branch, and one shared-QR `/start` branch and one `/restart` branch. These are mutually selected by new/existing account state, matching the current upstream post-login continuation.
- Normal Chat lazy connection remains present outside QR: `backend-web/app/api/routes/chat_new.py` still has `/connect/{account_id}` and its existing `get_or_connect()` owner.
- Post-deploy Backend/WebSocket logs contain 0 Chat-connect markers, 0 Local Token markers, 0 CAPTCHA/Baxia markers, 0 Remote Token markers, and 0 QR generation/login markers for this task window.
- Final Auto Reply read-only status: all 6 enabled accounts are `is_connected=true` / `connection_state=connected`; `AUTO_REPLY_ONLINE_COUNT=6`.
- Token-refresh storm regression was not observed; WebSocket was not restarted and no fresh Token API work was initiated by this deployment.

## Final classification

- `QR_HANDLER_UPSTREAM_EQUIVALENT=true`
- `QR_CONVERGENCE_BINDING_REMOVED=true`
- `QR_CHAT_AUTH_EAGER_TRIGGER=false`
- `QR_PUBLISH_PREFLIGHT_EAGER_TRIGGER=false`
- `CHAT_LAZY_CONNECT_PRESERVED=true`
- `AUTO_REPLY_QR_RESTART_PRESERVED=true`
- `QR_SCANS_ADDITIONAL=0`
- `CHAT_CONNECT_COUNT=0`
- `LOCAL_TOKEN_CALL_COUNT=0`
- `CAPTCHA_DELEGATION_COUNT=0`
- `REMOTE_TOKEN_CALLS=0`
