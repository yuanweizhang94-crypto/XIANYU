# 2026-08-15 Auto Reply stability consolidation — Upstream verification path restoration

## Scope

This evidence closes the code/runtime portion of the Auto Reply stability correction while preserving the Canary commit gate.

This run did **not** create a second Token system, Session system, WebSocket manager, verification engine, Profile store, Scheduler, queue, worker, or database table. It kept the existing Upstream/XIANYU owners and corrected orchestration around them.

Remote/local governance baseline at start:

- branch: `feat/CHG-0018-account-profile-publish-safety`
- GitHub/local baseline: `c0bbde40936718eb21e7798a54b8eb0983062996`
- active change: `CHG-0018` / `VERIFYING`
- cumulative patch base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- Upstream main re-fetched during this run: `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`

The five historical root dirty files were preserved and were not reset/restored/cleaned.

## New direct runtime evidence that changed the direction

The previous public “去验证” flow ultimately opened the raw official challenge URL in an unrelated desktop Chrome profile. The user observed a generic Taobao re-login page. That observation is **not** authoritative evidence that the XIANYU account Session is invalid: the desktop Chrome profile did not carry the XIANYU account's authenticated Cookie/Profile context.

Root cause:

`EXTERNAL_BROWSER_OPENED_CHALLENGE_WITHOUT_ACCOUNT_AUTH_CONTEXT`

The public raw challenge URL is therefore not an acceptable Auto Reply or Chat manual-verification bridge.

## Reverified Upstream facts

Upstream `origin/main` was re-fetched and read narrowly from the current formal files.

### Classification

`common/services/captcha/token_response.py` classifies both:

- `FAIL_SYS_USER_VALIDATE`
- `RGV587_ERROR`

as Token captcha/risk-control markers.

Token expiry markers such as `FAIL_SYS_TOKEN_EXOIRED` / `FAIL_SYS_TOKEN_EXPIRED` remain a separate self-healable class and are not reclassified as platform verification.

### Official challenge source and auth context

The Upstream Token owner obtains the official verification URL from the Token response `data.url` and passes the current account `CookieTokenManager.self.cookies_str` into the existing verification orchestration.

### Existing automatic verification owner

The existing owner is still `CookieTokenManager`. The current Upstream orchestration is configuration-driven and uses the existing captcha stack, including the configured local engine and optional remote/fallback paths. XIANYU does not add or strengthen a solver in this change.

Current production configuration was read without exposing secrets:

- `captcha.local_slider_disabled=false`
- slider mode: `browser`
- remote captcha configured: `false`
- Token API mode: `remote` (existing local-web-first + optional remote Token fallback semantics)
- WebSocket-specific DrissionPage fallback configuration: `false`
- `BROWSER_HEADLESS=true`

No administrator setting was changed.

## Corrected Auto Reply verification generation semantics

The prior stability patch was intentionally fail-closed but over-corrected one point: once the Token response was classified as platform verification, it prevented even the one configuration-authorized existing Upstream verification flow.

The corrected semantics are now:

1. valid/current Token → existing WebSocket path;
2. normal Token-expired self-heal → existing Set-Cookie/Token retry path;
3. fresh `FAIL_SYS_USER_VALIDATE` / `RGV587` generation → at most one existing Upstream configured verification attempt;
4. successful existing verification → same Cookie owner → same Token owner → Token cache → existing WebSocket owner;
5. failed/config-disabled attempt → `PLATFORM_VERIFICATION_REQUIRED` / stable `WAITING_USER`;
6. while waiting: no unattended Token retry, captcha retry, browser retry, or background Cookie mutation;
7. a user/owner action may explicitly authorize one new generation on the same `CookieTokenManager`; it does not create a second recovery service.

Generation metadata is non-sensitive and reuses the existing account metadata JSON. It stores only state/reason/generation/attempt result timestamps. It never stores Token, Cookie, challenge URL, passwords, QR payloads, or credentials.

Crash/restart behavior is fail-closed:

- `AUTOMATIC_ATTEMPT_IN_PROGRESS` surviving restart is treated as exhausted/waiting;
- legacy PVR markers are treated as already attempted so one container restart cannot fan out a new attempt across all accounts;
- an explicitly `AUTOMATIC_ATTEMPT_AUTHORIZED` generation is the only restart-safe exception before it is consumed.

## Cache correctness correction found by Canary

The first owner-authorized Canary call appeared to return a Token, but the runtime status showed it came from the previous expired-startup cache. This was correctly rejected as a false recovery.

The final implementation now invalidates the known-unusable Token cache inside the existing Token owner before an owner-authorized verification generation. It also synchronizes the existing `CookieManager.platform_verification_states` restart cache with the authoritative DB metadata so a stale in-memory PVR marker cannot resurrect after Token success.

No user-visible Token/Cookie value was printed or persisted to evidence.

## Scheduler / Cookie owner protection retained

The previous production finding remains authoritative: Scheduler tasks can otherwise become competing Cookie writers while Auto Reply is waiting for platform verification.

The shared existing pause gate now treats these states as background-auth-mutation blocked:

- `PLATFORM_VERIFICATION_REQUIRED`
- `AUTOMATIC_ATTEMPT_AUTHORIZED`
- `AUTOMATIC_ATTEMPT_IN_PROGRESS`

Only the existing `CookieTokenManager` may explicitly opt into the trusted Cookie write during its one bounded verification attempt. Scheduler/session/background writers remain blocked.

Production observation after final deployment:

- each of the six PVR accounts logged repeated Scheduler skip decisions;
- observed skip count in the sampled window: 15 per account;
- observed Scheduler Cookie mutation log count: 0 for all six;
- all six DB Cookie fingerprints stayed unchanged in the stable waiting window.

## Optional remote service semantics retained

Remote Token and remote captcha are optional. The existing remote Token balance-insufficient cooldown/single-flight remains in place.

For the optional remote captcha path, a balance-insufficient result is treated as optional-service unavailability and falls back to the already configured local Upstream path. This does **not** bypass platform verification; it only prevents an optional paid dependency from cutting off the local/manual official path.

`CORE_AUTO_REPLY_DEPENDS_ON_REMOTE_BALANCE=false`.

## Raw external browser challenge removed

`frontend/src/pages/chat-new/ChatNew.tsx` no longer executes:

`window.open(status.verification_url, ...)`

The public platform-verification status deliberately returns an empty public `verification_url`. The challenge URL stays server-side and is passed only through the trusted internal authenticated-browser orchestration.

Accounts continues to reuse the existing “去验证” navigation into ChatNew; Chat and Auto Reply therefore share the same corrected entry rather than each opening a raw URL.

## Authenticated manual browser bridge

No `VerificationBrowserManager`, second Profile store, worker, queue, Scheduler, or new service was created.

A thin method was added to the existing `cookie_renew_browser_service` and the existing internal WebSocket API. Its behavior is:

- use the same per-account canonical Profile path / existing browser locks;
- inject the current authoritative account Cookie;
- navigate the official challenge URL;
- never solve, drag, replay, or synthesize the user challenge;
- the user must perform the official interaction;
- after completion, return only sanitized status and legal Cookie changes to the existing Cookie owner;
- if an authenticated context reaches a login page, run authoritative Session health before deciding whether QR is required.

Production is currently a Linux/headless WebSocket container (`BROWSER_HEADLESS=true`) with no desktop display. In that runtime the bridge deliberately returns:

`AUTHENTICATED_BROWSER_UNAVAILABLE_HEADLESS_RUNTIME`

and does **not** leak/open the raw URL in ordinary desktop Chrome.

This is a current presentation blocker, not a Session/login failure.

## Authoritative Session proof for the Canary

Canary account: `2214313339860`.

A canonical Profile + current authoritative Cookie health check was run without persisting the returned Cookie snapshot. Sanitized result:

- `SESSION_STATE=REAL_BROWSER_LOGIN_READY`
- `SESSION_READY=true`
- `PROFILE_PRESENT=true`
- `VISIBLE_LOGIN_UI=false`
- `VISIBLE_QR=false`
- `VISIBLE_PLATFORM_ERROR=[]`
- Browser health observed a legal Cookie snapshot change, but this diagnostic did not persist it.

A follow-up read-only Token probe using that canonical Browser Cookie still returned:

- Token absent;
- captcha reason `FAIL_SYS_USER_VALIDATE`;
- Session expired: false;
- local web Token API remained authoritative;
- optional remote failure was present but did not change local classification.

Therefore:

- generic Taobao login from the old raw-browser flow did **not** prove account login expiry;
- the account Session is currently valid;
- QR/password re-login is not justified;
- the platform challenge is genuinely required for Token recovery.

## Real Canary automatic attempt

The final code did not automatically fan out attempts to all six old PVR accounts. Only the Canary was explicitly owner-authorized for a new generation.

Canary automatic path evidence:

- known bad cache invalidated by existing Token owner;
- current production configuration used;
- one existing Upstream Playwright verification flow ran;
- no new solver or mode was enabled;
- the configured Playwright flow did not complete the challenge;
- WebSocket runtime configuration had DrissionPage fallback disabled, so it was not silently enabled;
- generation transitioned to `PLATFORM_VERIFICATION_REQUIRED` with `automatic_attempted=true` and `automatic_result=FAILED_WAITING_USER`.

After entering stable waiting:

- new Token API calls: 0;
- new Playwright attempts: 0;
- new DrissionPage attempts: 0;
- new captcha attempts: 0;
- browser processes at idle: 0;
- zombie processes: 0.

This proves the intended distinction:

- one configured existing Upstream attempt is allowed;
- unattended retry/slider/Cookie storm after failure remains forbidden.

## Non-Canary isolation

The other five PVR accounts were not manually/owner-triggered and did not receive a new automatic generation during deployment. They remained stable PVR/WAITING_USER, did not start Browser work, and retained stable DB Cookie fingerprints.

## Production images and health

Final deployed images in this run are based on the previously verified formal images and were updated by minimal source overlay without pulling external base images:

- WebSocket: `xianyu-chg0018-websocket:upstream-verification-20260815-r2`
- Backend: `xianyu-chg0018-backend-web:upstream-verification-20260815-r1`
- Scheduler: `xianyu-chg0018-scheduler:upstream-verification-20260815-r1`
- Frontend: `xianyu-chg0018-frontend:upstream-verification-20260815-r1`

Health after replacement:

- Backend HTTP 200;
- WebSocket HTTP 200;
- Scheduler HTTP 200;
- Frontend HTTP 200;
- WebSocket `init=true` preserved;
- MySQL/Redis not changed.

Old containers were retained under backup names during the Canary gate so rollback remains possible until final closure.

## Verification performed

- Python compile for changed runtime modules: PASS
- focused Auto Reply restoration tests: 37/37 PASS
- focused Auto Reply + Publish/AI validation regression selection: 54/54 PASS
- Frontend TypeScript/Vite production build: PASS
- `git diff --check`: PASS before production deployment

The source checkout's broad local `tests/` run still reproduces historical CHG-0017 baseline/test-isolation failures unrelated to this change (the previously known Gemini failures plus logger-mock pollution when those files are collected together). They are not attributed to this Auto Reply correction. Formal XIANYU governance repository verification is run separately against the cumulative Patch artifact.

## Side-effect accounting

- `REAL_MESSAGES_SENT=0`
- `REAL_PRODUCTS_PUBLISHED=0`
- `QR_SCANS_TRIGGERED_BY_TEST=0`
- `ONE_USER_PLATFORM_CHALLENGE_CANARY=0` (no user-completed challenge could be presented in the current headless runtime)

The one Canary automatic Upstream existing verification attempt is the only platform challenge execution performed by this correction.

## Final cumulative Patch / repository verification

Final cumulative Patch:

- base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- SHA256: `9910CCDDF695616268A402CFD50937B49BA8C4DF824EB06C8830D3000A72A590`
- size: `530174` bytes
- fresh `git apply --check`: PASS
- fresh actual `git apply`: PASS
- union compared files: 48
- raw byte differences after apply versus final source tree: 0
- CRLF-normalized mismatches: 0

Final source `git diff --check`: PASS.

Formal XIANYU governance verification after Patch/Evidence update:

- `python scripts/verify_repository.py`: PASS
- repository tests: `595 passed`

Root dirty isolation remained exact: the same five historical dirty files plus only this Evidence and the cumulative Patch as current formal untracked files.

## Current Canary gate

The code/runtime correction is **not** eligible for final Git Commit yet.

Current blocker:

`AUTHENTICATED_MANUAL_VERIFICATION_PRESENTATION_UNAVAILABLE_IN_HEADLESS_DOCKER`

The Canary Session is valid and QR is not required, but the current Linux/headless WebSocket deployment has no user-visible desktop surface for the canonical account Browser. The corrected code refuses to fall back to ordinary Chrome/raw challenge URL because doing so would recreate the proven context mismatch.

Required final gate remains:

- Canary obtains a Token through the legal existing path or user-completed authenticated official challenge;
- existing WebSocket owner reaches `WS_CONNECTED=true` / `AUTO_REPLY=ONLINE` without unnecessary login or QR;
- only then stage the formal Patch + Evidence, Commit, SSH-443 Push, and verify `LOCAL_COMMIT_SHA == REMOTE_BRANCH_SHA`.

## Final production recovery correction — later evidence supersedes the previous blocker

The earlier manual-verification presentation blocker was **not** the final production root cause. A later production-baseline comparison found that Auto Reply had already been destabilized before the UI/manual-verification work by synchronized proactive Token maintenance.

### Last known good runtime

The last directly reconstructed intervals in which all six target enabled accounts were simultaneously WebSocket-connected on the historical production log were:

- `2026-08-14 01:02:52` to `08:39:27`;
- `2026-08-14 09:25:47` to `09:41:54`;
- `2026-08-14 09:42:00` to `10:23:35`.

Therefore the last directly evidenced 6/6-online boundary is `2026-08-14 10:23:35 +08:00`.

The corresponding WebSocket image was:

`xianyu-chg0018-websocket:session-lifecycle-20260812-r2`

This historical runtime is not representable by one exact Git commit because production used validated image overlays. The runtime manifest itself recorded an observed local source lineage of `bad1bb8bf46bec79ac587012dde50de7aab4f516` while also stating that runtime image identity was not represented by one local Git SHA. No synthetic “last-good commit” is asserted.

### Runtime configuration comparison

No material Auto Reply runtime configuration drift was found between the accepted production architecture and current runtime:

- Token API mode remained local-web-first with optional remote fallback (`token.api_mode=remote` in the existing setting semantics);
- `captcha.local_slider_disabled=false`;
- slider mode remained `browser`;
- no account proxy was configured for any of the six target accounts;
- Scheduler remained one container with `api_cookie_renew=true` at 3600 seconds;
- `token_renewal=false`, `cookies_refresh=false`, `login_renew=false`;
- no second Token/Session/Scheduler owner existed.

`AUTO_REPLY_RUNTIME_CONFIG_DIFF=NO_PRIMARY_ROOT_CAUSE_CONFIG_DRIFT`.

### Mass PVR root cause

The six accounts did **not** have a natural synchronized Token-cache expiry.

Their pre-event cache-expiry timestamps were spread over roughly nine hours, from `2026-08-13 15:10:21` through `2026-08-14 00:25:52`.

`MASS_EXPIRY_CLUSTER=false`.

However, the existing WebSocket `TokenManager.cookie_refresh_loop` used a hardcoded 180-second maintenance interval. When its timer elapsed it called the same `XianyuAsync.refresh_token()` authentication owner even while a WebSocket Token could still be serving live traffic. On an ordinary failed maintenance refresh, the old implementation also waited five seconds and immediately called `refresh_token()` a second time.

Historical persistent logs show the resulting real Token API volume over roughly 21 hours was hundreds of calls per account (approximately 325–426 API requests per target account), with many cross-account bursts in the same minute.

`SYNCHRONIZED_TOKEN_REFRESH_STORM=true`.

The first concentrated local platform-verification responses for the six accounts appeared around `2026-08-14 03:26–03:28`, when local web Token calls returned `FAIL_SYS_USER_VALIDATE` / `RGV587_ERROR`. The optional remote fallback sometimes returned conflicting `FAIL_SYS_SESSION_EXPIRED` results and the old maintenance path then expanded into Cookie/browser/password renewal attempts and a five-second second Token attempt.

The critical destructive behavior was that a proactive maintenance failure could clear `current_token` and invalidate the Token cache even though the already-established WebSocket was still usable. Once that happened, a later ordinary network disconnect or container recreation could no longer use the existing Token for direct reconnect and instead fell into full authentication/PVR.

This is the direct production regression mechanism.

### Deployment amplification

WebSocket recreation synchronized per-instance maintenance clocks and therefore amplified the latent problem.

A directly reconstructed example:

- at approximately `09:25:47`, all six accounts reconnected from database startup cache after process recreation;
- around `09:31:52–09:32:52`, the synchronized maintenance wave drove those accounts back into Token API requests/PVR;
- the same pattern repeated around later restart/network windows.

`DEPLOYMENT_TRIGGERED_TOKEN_REFRESH_WAVE=true` as an amplifier, not as a claim that container recreation itself creates platform risk.

### Remote Token role

The optional remote Token service was genuinely used during the last-known-good period. For example, the Canary used remote fallback successfully around `2026-08-14 13:15` after the local web Token path failed; a refreshed cache was stored and the account remained online. Later, balance-insufficient responses appeared across accounts beginning around `13:29–13:33`.

Therefore:

- `LAST_KNOWN_GOOD_REMOTE_TOKEN_USED=true`;
- remote Token fallback historically masked some local Token/PVR failures;
- remote balance exhaustion exposed the underlying local refresh/PVR problem but did not create the 3-minute refresh storm;
- `CORE_AUTO_REPLY_DEPENDS_ON_REMOTE_BALANCE=false` remains the required architecture.

### Proxy / IP policy

All six target accounts currently have `proxy_type=none` and no configured per-account proxy. HTTP Token and WebSocket paths therefore share the same direct-routing policy.

`HTTP_WS_IP_POLICY_CONSISTENT=true` at the configured-policy level.

Historical public egress-IP change is not proven by available logs, so no unsupported “IP changed” root cause is asserted.

## Minimal production fix

No configuration change and no new subsystem were required.

`FIX_TYPE=MINIMAL_REVERT+MINIMAL_PATCH`.

Three narrow corrections were made on the existing owners:

1. **Live WebSocket Token wins over proactive maintenance.** `TokenManager._execute_cookie_refresh()` now skips Token API refresh while an in-memory Token is serving a `connected`, `connecting`, or `reconnecting` WebSocket. The real connection/authentication owner still handles genuine disconnect/auth failures.
2. **One proactive maintenance attempt maximum per cycle.** The five-second immediate second authentication attempt was removed. An offline maintenance cycle can call the existing Token owner at most once.
3. **Startup cache behavior restored.** A historical PVR metadata marker retains reason/generation but no longer sets the process into `platform_verification_required` before the Upstream expired-startup cache gets its existing one-time chance to reconnect. If that cache cannot establish the WebSocket, the same `CookieTokenManager` reads the same marker and can still fail closed to PVR without repeating automatic verification.

The Account business-capability projection was also corrected so a real `WS_CONNECTED=true` is reported as `AUTO_REPLY=ONLINE`; a historical background PVR marker cannot override current live business usability. When the WebSocket is not connected, PVR remains visible and fail-closed.

No raw external challenge behavior was restored. No captcha capability was expanded.

## Production Canary and restart acceptance

Production images for the final recovery:

- Backend: `xianyu-chg0018-backend-web:auto-reply-refresh-storm-fix-20260815-r1`;
- WebSocket: `xianyu-chg0018-websocket:auto-reply-refresh-storm-fix-20260815-r2`.

Scheduler, Frontend, MySQL, Redis, named volumes, canonical browser Profile volume, and database schema were not changed.

After the WebSocket r2 restart, **all six enabled target accounts zero-touch recovered through the existing expired-startup Token-cache path**:

- `WS_CONNECTED=true` for 6/6;
- `token_refresh_state=success_from_expired_startup_cache` for 6/6;
- `platform_verification_required=false` for 6/6 runtime owners;
- `human_qr_required=false` for 6/6;
- user verification actions: 0;
- QR scans: 0;
- Cookie clears: 0.

Canary: `2214313339860`.

`CANARY_ZERO_TOUCH_RECOVERY=true`.

`CANARY_AUTO_REPLY_ONLINE=true`.

The other five accounts recovered only as a normal consequence of the WebSocket production restart; no individual manual/verification action was performed on them.

## Post-recovery stability window

The final runtime was observed across three complete 180-second maintenance cycles.

For **each** of the six target accounts:

- `maintenance_live_skip=3`;
- Token API requests after final restart: 0;
- new PVR responses: 0;
- captcha starts: 0;
- WebSocket exits: 0.

All six database Cookie fingerprints were byte-stable across the window. Browser processes at idle: 0. Zombie processes: 0.

Two non-Canary controls (`2219319284219` and `2196106636`) received no manual action and showed the same zero Token-request / stable-Cookie / zero-browser behavior.

Scheduler continued to fail closed on the existing historical PVR metadata marker and did not rotate background Cookie state.

Therefore:

- `NO_RETRY_STORM=true`;
- `BACKGROUND_COOKIE_ROTATION=0`;
- `NON_CANARY_COOKIE_ROTATION=0`;
- `MAX_TOKEN_REFRESH_PER_ACCOUNT=1` per maintenance cycle, with the existing per-instance single-flight lock still limiting concurrent owner refresh to one;
- `CONTAINER_RESTART_CACHE_PATH=PASS` by direct production evidence.

## Golden-path regression status

- `VALID_TOKEN_GOLDEN_PATH=PASS`: live/current Token no longer receives unnecessary 3-minute proactive refresh and current WebSocket remains online.
- `RENEWED_TOKEN_GOLDEN_PATH=PASS`: existing successful renewed/remote-optional Token path is unchanged; focused regression selection passes.
- `TOKEN_EXPIRED_SELF_HEAL_PATH=PASS`: `FAIL_SYS_TOKEN_EXPIRED` / `FAIL_SYS_TOKEN_EXOIRED` remains a distinct bounded retry path and is not reclassified as PVR.
- `NORMAL_WS_RECONNECT_PATH=PASS`: network disconnect handling still uses the existing direct reconnect path and does not call Token refresh merely because `ConnectionClosed` occurred; historical 6/6 production evidence also shows direct reconnection from `09:41:54` to `09:42:00` without this new maintenance path being involved.
- `CONTAINER_RESTART_CACHE_PATH=PASS`: direct final production restart recovered 6/6 through the existing startup cache.

## Final focused verification update

After the final regression cleanup:

- Auto Reply stability tests: `42/42 PASS`;
- Auto Reply + Publish-login + AI-prompt isolated regression selection: `59/59 PASS`;
- Reply-allowlist isolated regression: `22/22 PASS`;
- merged collection reproduces the known logger-mock test-isolation contamination only; isolated reply-allowlist is green;
- Python compile: PASS;
- `git diff --check`: PASS.

## Final cumulative Patch update

The cumulative Patch was regenerated from the same source base:

- base: `64c245bc85ac56e34339fa056b0e291a16a3843b`;
- SHA256: `A73E12E74F564B9244C22C6D95AFC980FFD0E066BE41555835375E36A00149FA`;
- size: `537757` bytes;
- fresh `git apply --check`: PASS;
- fresh actual `git apply`: PASS;
- compared files: 48;
- byte differences between fresh-applied tree and final source tree: 0.

The previous “manual authenticated-browser presentation is required before Commit” conclusion is superseded by this later production evidence. The business recovered without user verification, QR, Cookie clear, or captcha execution.
