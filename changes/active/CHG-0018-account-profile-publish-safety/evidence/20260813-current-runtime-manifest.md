# 2026-08-13 Current Production Runtime Manifest

Time baseline: 2026-08-13 (Asia/Taipei / UTC+8)

## Execution contract

User outcome: expose the already-existing authoritative Account Session lifecycle state in the Account UI, repair Scheduler IPv4 health only if its single-instance lifecycle can be proven safe, and record CURRENT_GITHUB vs CURRENT_LOCAL vs CURRENT_RUNTIME without forcing redeployment.

Original observation before this closeout: Account UI projected WebSocket `online` but not persisted `session_maintenance.state`; Scheduler was healthy on IPv6 `[::1]:8091` but refused IPv4 `127.0.0.1:8091`; the local candidate compose did not contain the Scheduler service; GitHub default branch, local feature branch, and production images were intentionally not identical.

Closeout outcome: the Account projection was deployed through the existing formal patch/replay chain; the Scheduler's retained single-instance replacement lifecycle was recovered from historical runtime/evidence and reused with only `HOST=0.0.0.0`; Git/local/runtime identity differences remain recorded rather than being forcibly aligned.

Reuse decision: `PATCH_UPSTREAM` for the Account API/UI projection and `CONFIGURE_UPSTREAM` only if a safe Scheduler lifecycle is found. No new Session service, Scheduler, Publisher, Profile manager, database table, queue, or business execution path is permitted.

## CURRENT_GITHUB

- Default branch: `main`
- CURRENT_GITHUB_SHA: `99b81dd94931b0d2c6bf043d2bd1c625aeb94c08`
- `AGENTS.md` blob: `478007e8da67cd28a52ae21ebe23f03d1548524a`
- `docs/AI_PROJECT_HANDOFF.md` blob: `c2e7c30cf8726c872cf80be6c390d5c4adfff797`
- `README.md` blob: `2f87144af982476ae318fbb4e5392c56398a98d4`

## CURRENT_LOCAL

- Checkout: `D:\xianyu`
- CURRENT_LOCAL_BRANCH: `feat/CHG-0018-account-profile-publish-safety`
- OBSERVED_LOCAL_SHA_BEFORE_MANIFEST_COMMIT: `bad1bb8bf46bec79ac587012dde50de7aab4f516`
- MANIFEST_COMMIT_SHA: `720db6c82071ecf5daed6a0322ec658985f98399`
- CURRENT_LOCAL_SHA_AFTER_MANIFEST_COMMIT: `720db6c82071ecf5daed6a0322ec658985f98399`
- SHA semantics: the first value is the source HEAD observed while the original manifest was being written; the second is the commit that first added this manifest; the third is the real local HEAD observed at the start of this correction run after that manifest commit. A later closeout commit that updates this document is recorded separately as the run's final commit and does not retroactively change these three historical observations.
- Tracking branch: `origin/feat/CHG-0018-account-profile-publish-safety`
- Tracking SHA observed before this correction commit: `720db6c82071ecf5daed6a0322ec658985f98399`
- Pre-existing dirty files before this task:
  - `changes/active/CHG-0018-account-profile-publish-safety/acceptance.md`
  - `changes/active/CHG-0018-account-profile-publish-safety/proposal.md`
  - `changes/active/CHG-0018-account-profile-publish-safety/tasks.md`
  - `generated/PROJECT_STATE.json`
  - `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`
- Those pre-existing changes were not reset, overwritten, or folded into this task.

## CURRENT_RUNTIME

| Service | Container | Image | Host port | Current health |
|---|---|---|---|---|
| frontend | `xianyu_chg0017_frontend` | `xianyu-chg0019-frontend:account-session-ui-20260813` | `127.0.0.1:19000 -> 80` | `/health` HTTP 200 |
| backend_web | `xianyu_chg0017_backend_web` | `xianyu-chg0018-backend-web:account-session-ui-20260813` | `127.0.0.1:28089 -> 8089` | `/health` HTTP 200, DB connected |
| websocket | `xianyu_chg0017_websocket` | `xianyu-chg0018-websocket:session-lifecycle-20260812-r2` | `127.0.0.1:28090 -> 8090` | `/health` HTTP 200, DB connected / Docker healthy |
| scheduler | `xianyu_chg0017_scheduler` | `xianyu-chg0018-scheduler:session-lifecycle-20260812` | `127.0.0.1:28091 -> 8091` | IPv4 container and host `/health` HTTP 200, DB connected; `HOST=0.0.0.0` |
| mysql | `xianyu_chg0017_mysql` | `mysql:8.0` | `127.0.0.1:23306 -> 3306` | Docker healthy |
| redis | `xianyu_chg0017_redis` | `redis:7.4-alpine` | `127.0.0.1:26379 -> 6379` | Docker healthy |

All six host ports are listening. SPA route checks returned HTTP 200 for `/login`, `/dashboard`, `/accounts`, and `/items` through the frontend.

## Account Session UI finding

- Actual Account page API: `GET /api/v1/cookies/details/paginated`.
- Existing authoritative lifecycle source: `XYAccount.metadata_json.session_maintenance`.
- Existing production lifecycle states include `REAL_BROWSER_LOGIN_READY`, `SESSION_RENEWING`, `SESSION_RENEW_FAILED`, `HUMAN_QR_REQUIRED`, `PLATFORM_VERIFICATION_REQUIRED`, `COOLDOWN`, and intermediate/pending states.
- Current runtime DB read-only sample contains both `REAL_BROWSER_LOGIN_READY` and non-ready `SESSION_CHECK_PENDING` states; no artificial Session failure was created.
- Minimal source patch projects `session_state` / `session_state_updated_at` through the existing Account API and displays a new `平台会话` column. No Session backend lifecycle logic was changed.
- The Session-only delta was isolated on a clean CHG-0018 replay base and recorded as `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-session-ui-production.patch` (SHA-256 `0F02DB0ABE8B7365F816CA1CCFAD6ED58480356A79EAFB418FD1E658CA201CAE`).
- Safe production replay used the existing formal chain `CHG-0018 patch -> CHG-0019 formal-delivery patch -> Account Session UI delta`, rather than building the dirty delivery checkout directly.
- Python syntax check, TypeScript no-emit check, Vite production build, Session-delta `git apply --check`, and delta `git diff --check` passed.
- Backend deployment is an overlay of the previously running `xianyu-chg0018-backend-web:category-state-machine-final-20260812` image that replaces only `/app/backend-web/app/api/routes/cookies.py`.
- Frontend deployment is an overlay of the previously running `xianyu-chg0019-frontend:2b672d2-offline-ui-health` image that replaces only the static `dist` produced from the formal replay. Its required `backend-web` link alias was preserved when the production frontend container was recreated.
- Production evidence after deployment: frontend/backend/websocket health HTTP 200; `/accounts`, `/login`, `/dashboard`, and `/items` HTTP 200; the served Account bundle contains the literal `平台会话`; the running Backend route contains `session_state` / `session_state_updated_at`.
- Current read-only account state counts are `REAL_BROWSER_LOGIN_READY=3`, `SESSION_CHECK_PENDING=6`, `UNKNOWN=2`, proving both READY and non-READY samples without manufacturing Session failure.

## Scheduler IPv4 finding

- Current Scheduler command: `python scheduler/main.py`.
- Current Scheduler executor count inside the container: `1`.
- LISTEN_BEFORE: IPv6 `::` behavior; `[::1]:8091/health` = HTTP 200 and DB connected.
- `127.0.0.1:8091/health` = connection refused inside the container.
- `127.0.0.1:28091/health` is not usable from the host despite the Docker IPv4 port binding.
- Runtime environment does not explicitly set `HOST`; existing `_bootstrap.py` resolves the configured/default host through `resolve_listen_host()`.
- Existing application configuration already supports `HOST=0.0.0.0`; no change to `common/utils/network_utils.py` is necessary or allowed.
- The current `.local/chg0017-candidate/docker-compose.yml` still does not define Scheduler and is not treated as the Scheduler lifecycle authority.
- The authoritative replacement lifecycle was recovered from the retained stopped Scheduler container chain (`pre_wsurl_fix`, `pre_session_lifecycle`, and earlier rollback containers) together with CHG-0018 Scheduler-only deployment evidence. These show the established lifecycle: stop the unique active Scheduler first, retain it under a rollback name, then create the replacement with the same image/runtime parameters and the canonical container name.
- Before repair the active executor count was exactly `1`. The old Scheduler was stopped and executor count reached `0` before any replacement was created. The replacement was then created from the exact current inspect parameters with only `HOST=0.0.0.0` added and started; active executor count returned to exactly `1`.
- Current Scheduler image remains `xianyu-chg0018-scheduler:session-lifecycle-20260812`; no Scheduler application source or scheduled-task row was changed.
- AFTER: container `127.0.0.1:8091/health` = HTTP 200 and DB connected; host `127.0.0.1:28091/health` = HTTP 200 and DB connected.
- Scheduled task rows remain unchanged at 21, duplicate task codes remain 0, and enabled tasks remain `api_cookie_renew`, `day_switch`, `fetch_items`, `polish`.

## Comparison

- GITHUB_LOCAL_MATCH=false — default-branch SHA `99b81dd...` differs from the local feature-branch lineage whose observed post-manifest HEAD is `720db6c...`.
- LOCAL_RUNTIME_MATCH=false — production now intentionally includes the Account Session UI overlay images plus the existing CHG-0018/CHG-0019 runtime chain; image identity is not represented by one local Git SHA.
- GITHUB_RUNTIME_MATCH=false — current default-branch Git state is not the exact build identity embedded in the running production images.

The closeout performed only the required Backend/Frontend Account UI overlays and the single-instance Scheduler configuration replacement. No whole-environment rebuild, merge, rebase, upstream sync, QR login, Cookie manual refresh, product publish, Material creation, category change, or message send was performed.

## Closeout validation

- Repository verification: `python scripts/verify_repository.py` = PASS (`595 passed`, repository verification passed).
- Session delta staged diff check: PASS.
- Production HTTP: frontend 200, backend 200, websocket 200, Account/Login/Dashboard/Items SPA routes 200.
- Production Account bundle contains `平台会话`; running Backend Account route contains `session_state` and `session_state_updated_at`.
- Scheduler IPv4: container `127.0.0.1:8091/health` 200; host `127.0.0.1:28091/health` 200; DB connected; active executors 1.
- Real products published by this closeout: 0. Real messages sent by this closeout: 0. QR triggers: 0. Manual Cookie refresh triggers: 0.
