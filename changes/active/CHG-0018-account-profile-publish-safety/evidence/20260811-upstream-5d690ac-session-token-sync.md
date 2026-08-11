# CHG-0018 Upstream 5d690ac Session/Token Minimal Sync Evidence

Date: 2026-08-11
Upstream source: `5d690ac6e77d415b886b1e87b5aaf446f0f29c48`
Local branch: `feat/CHG-0018-account-profile-publish-safety`
Local HEAD at sync start: `44c8ae98ac576f9ab486fae473d56f26480b8868`
Decision: `PATCH_UPSTREAM` by selective transplant; no cherry-pick and no Publisher replacement.

## Scope

Evaluated upstream files:

- `common/services/im_token_api.py`
- `common/services/captcha/token_refetch.py`
- `common/services/remote_token_risk_log_service.py`
- `websocket/app/services/xianyu/cookie_token_manager.py`

Selective implementation result:

- Added unified `is_session_expired_token_result()` handling for local and remote-fallback failure results.
- Added `remote_failure_message` so a remote fallback failure can carry Session-expired evidence without overwriting the original local response body.
- Added separate local/remote Token timing propagation and risk-log formatting.
- Moved Session-expired handling before captcha/slider handling in `CookieTokenManager.refresh_token()`.
- Preserved the existing renew/login owner: Session expiry enters `try_password_login_refresh()`, whose first action is the existing Cookie renew service.
- Preserved CHG-0018 safety: `no_credentials` and bad-credential paths do not disable `XYAccount.status`.

The upstream `5d690ac` no-credentials auto-disable hunk was deliberately not transplanted because it conflicts with the active CHG-0018 credential-safety acceptance boundary.

## Explicit exclusions

No task change was made to:

- `backend-web/app/services/xianyu_publisher.py`
- category selection or category IDs
- publish submit/result logic
- QR-login main flow
- canonical Profile ownership or profile directories
- database schema
- Scheduler source or image
- Frontend source or image
- App/native/mobile handoff

Normal flow remains: first QR login once -> persisted Cookie -> canonical Profile -> Cookie/Session renewal -> Publisher reuse. A second QR is not part of normal publish flow.

## Targeted validation

- Session/Token upstream-sync tests: `10 passed`.
  - healthy Session returns Token without login/slider work;
  - explicit local or remote-fallback Session expiry is recognized;
  - Session expiry reaches the existing renew/login chain before captcha;
  - temporary remote failure is not misclassified as Session expiry;
  - API Cookie renewal success reuses the Session without password/QR login;
  - unrecoverable renewal with no credentials fails closed without disabling the account;
  - local/remote timing fields are recorded separately;
  - Publisher normal flow contains no second-QR step.
- CHG-0018 credential/login-renew safety: `5 passed`.
- CHG-0018 Profile/publish readiness: `7 passed`.
- CHG-0017 publish regression: `17 passed`.
- CHG-0018 auto-polish auth/session safety: `24 passed`.
- Combined scoped regression: `63 passed`.
- Python compile check for all four changed runtime files: passed.
- Governance full pytest matrix: `595 passed`; the repeated Starlette/httpx deprecation warning remains the known warning baseline.
- The monolithic `python scripts/verify_repository.py` wrapper was interrupted twice by the local execution connector returning HTTP 502. Read-only infrastructure checks immediately showed DevSpace/Proxy health and ports `7676`, `7681`, and `20241` listening; no XIANYU business executor was restarted because of the 502.
- The same repository verification was then completed by decomposition: all `595/595` pytest cases passed, and structure/change/capability/schema/OpenAPI/duplicates/security/project-state checks all passed.
- Change acceptance before final evidence update: `8 passed`.

## Vendor patch

Updated the existing CHG-0018 vendor patch only for the current Session/Token owner sections and the new targeted test:

`vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`

SHA256 after Session/Token sync: `756410DB732B654D6A7DB62D9236A7477D1C608C7778AD5779D723308D807D69`

- Patch staged-base apply check passed against the existing CHG-0017 staged base with `git apply --check --cached --whitespace=error-all --unidiff-zero`.
- A direct apply attempt against bare `4c5e1ac5...` is not the project validation model because this CHG-0018 artifact is an incremental patch over the staged CHG-0017 base.

No Publisher/category hunk was introduced by this sync.

## Production deployment

Deployment used image overlays on the already deployed production images so unrelated dirty-worktree files were not pulled into the runtime images.

- Backend: `xianyu-chg0018-backend-web:44c8ae9-session-5d690ac`
  - overlaid only `im_token_api.py`, `token_refetch.py`, and `remote_token_risk_log_service.py`.
- WebSocket: `xianyu-chg0018-websocket:44c8ae9-session-5d690ac`
  - overlaid the same three shared Token files plus `cookie_token_manager.py`.

Both overlay images passed isolated `py_compile` before deployment. Current runtime inspection confirms `xianyu_chg0017_backend_web` and `xianyu_chg0017_websocket` are the only XIANYU services with the new Session/Token image tags; their existing named volumes, network, ports, and service identities remain in use.

Post-deployment evidence:

- Backend `/health`: HTTP 200.
- WebSocket `/health`: HTTP 200 and Docker health `healthy`.
- Runtime import confirms `is_session_expired_token_result()` is available in both services.
- Synthetic runtime checks in both services classify a healthy result as non-expired and explicit `FAIL_SYS_SESSION_EXPIRED` as expired; Backend also recognizes the same explicit expiry carried only in `remote_failure_message`.
- Runtime WebSocket source places `is_session_expired_token_result(api_result)` at line 1237 and the later captcha check at line 1269, so explicit Session expiry is handled first.
- Runtime WebSocket source preserves CHG-0018 no-disable behavior for both `no_credentials` and bad-credential paths.
- MySQL container identity unchanged.
- Redis container identity unchanged.
- Scheduler container identity unchanged.
- Frontend container identity unchanged.
- No volumes deleted.

## Post-deployment read-only account-lifecycle audit

A read-only production audit was completed after deployment without QR scan, login refresh, account mutation, product action, container restart, or Scheduler configuration change.

Observed production state:

- `xy_accounts`: 11 total accounts, 8 active.
- All 11 accounts use the QR-oriented login path and have non-empty persisted Cookie state; only 1 account currently has complete username/password credentials, so password login is not the normal renewal owner.
- Canonical browser Profile state is present for all 11 accounts; active accounts are `8/8` complete and inactive accounts are `3/3` complete.
- Backend and WebSocket continue to share the existing `xianyu_chg0017_browser_data` named volume, so Profile ownership survives the Session/Token container replacement.
- After the WebSocket deployment restart, all 8 active accounts matched a current Token cache entry and established WebSocket connections without QR login or password login.
- During the observed post-restart window, all 8 active connections continued producing heartbeats with no observed Session-expiry event, Token-refresh failure, or WebSocket disconnect.
- The WebSocket-owned Cookie/Token maintenance loop remained active after restart and completed refresh cycles without observed failure in the audit window.
- Historical login-renew records show 14 successful browser renewals across 4 distinct accounts during the preceding 7-day window. A traced Session-expiry event showed the intended chain: existing canonical Profile browser renewal -> Cookie merge/writeback -> cached Token invalidation -> new Token acquisition/cache -> subsequent WebSocket heartbeats, while password login was skipped.
- The 8 active accounts all had current Token-cache entries at audit time, with the nearest expiry still several hours away. Therefore the newly deployed `5d690ac` Session-expiry branch has not yet naturally fired in production after this deployment; it remains covered by targeted tests and runtime synthetic checks while awaiting a natural expiry event.

Scheduler ownership audit:

- `login_renew=false`
- `api_cookie_renew=false`
- `token_renewal=false`
- `cookies_refresh=false`
- No executions of those four Scheduler renewal tasks were observed after the deployment restart.
- This is the desired current ownership model: WebSocket owns normal Cookie/Token maintenance. The four Scheduler renewal tasks must not be enabled merely for validation because that would create a second renewal executor against the same accounts/Profile state.

Follow-up observation:

- Runtime WebSocket logs still include overly detailed Token response/value logging on some refresh paths. No real Token value was copied into this repository or evidence. This is a separate log-redaction hardening item and does not change the verified renewal ownership or current runtime behavior.

## Operational safety

Real product actions: 0.
Products created/edited/offlined: 0.
Publisher files changed by this sync: 0.
Category files changed by this sync: 0.
QR login flow changes: 0.
Database schema changes: 0.
App handoff additions: 0.
