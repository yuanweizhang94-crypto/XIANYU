# 2026-08-13 Current Production Runtime Manifest

Time baseline: 2026-08-13 (Asia/Taipei / UTC+8)

## Execution contract

User outcome: expose the already-existing authoritative Account Session lifecycle state in the Account UI, repair Scheduler IPv4 health only if its single-instance lifecycle can be proven safe, and record CURRENT_GITHUB vs CURRENT_LOCAL vs CURRENT_RUNTIME without forcing redeployment.

Confirmed blocker: Account UI currently projects WebSocket `online` but not persisted `session_maintenance.state`; Scheduler is healthy on IPv6 `[::1]:8091` but refuses IPv4 `127.0.0.1:8091`, while no authoritative Scheduler compose/runtime manifest is present in the current local deployment directory; GitHub default branch, local feature branch, and production images are intentionally not identical.

Smallest success test: add only an Account API/UI projection of the existing Session state, prove the frontend compiles/builds, preserve zero platform actions; fail closed on Scheduler recreation if its lifecycle manifest cannot be proven; record exact current Git/local/runtime state and health without rebuild/redeploy merely to align SHAs.

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
- CURRENT_LOCAL_SHA: `bad1bb8bf46bec79ac587012dde50de7aab4f516`
- Tracking branch: `origin/feat/CHG-0018-account-profile-publish-safety`
- Tracking SHA: `bad1bb8bf46bec79ac587012dde50de7aab4f516`
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
| frontend | `xianyu_chg0017_frontend` | `xianyu-chg0019-frontend:2b672d2-offline-ui-health` | `127.0.0.1:19000 -> 80` | HTTP 200 / Docker healthy |
| backend_web | `xianyu_chg0017_backend_web` | `xianyu-chg0018-backend-web:category-state-machine-final-20260812` | `127.0.0.1:28089 -> 8089` | `/health` HTTP 200, DB connected |
| websocket | `xianyu_chg0017_websocket` | `xianyu-chg0018-websocket:session-lifecycle-20260812-r2` | `127.0.0.1:28090 -> 8090` | `/health` HTTP 200, DB connected / Docker healthy |
| scheduler | `xianyu_chg0017_scheduler` | `xianyu-chg0018-scheduler:session-lifecycle-20260812` | `127.0.0.1:28091 -> 8091` | IPv6 `[::1]:8091/health` HTTP 200, DB connected; IPv4 host health not working |
| mysql | `xianyu_chg0017_mysql` | `mysql:8.0` | `127.0.0.1:23306 -> 3306` | Docker healthy |
| redis | `xianyu_chg0017_redis` | `redis:7.4-alpine` | `127.0.0.1:26379 -> 6379` | Docker healthy |

All six host ports are listening. SPA route checks returned HTTP 200 for `/login`, `/dashboard`, `/accounts`, and `/items` through the frontend.

## Account Session UI finding

- Actual Account page API: `GET /api/v1/cookies/details/paginated`.
- Existing authoritative lifecycle source: `XYAccount.metadata_json.session_maintenance`.
- Existing production lifecycle states include `REAL_BROWSER_LOGIN_READY`, `SESSION_RENEWING`, `SESSION_RENEW_FAILED`, `HUMAN_QR_REQUIRED`, `PLATFORM_VERIFICATION_REQUIRED`, `COOLDOWN`, and intermediate/pending states.
- Current runtime DB read-only sample contains both `REAL_BROWSER_LOGIN_READY` and non-ready `SESSION_CHECK_PENDING` states; no artificial Session failure was created.
- Minimal source patch was made only in the existing upstream delivery checkout to project `session_state` / `session_state_updated_at` through the Account API and display a new `平台会话` column. No Session backend lifecycle logic was changed.
- TypeScript no-emit check passed and Vite production build passed.
- Production frontend was not replaced because the running image contains multiple generations of static chunks and the local dirty source build cannot be proven byte-equivalent to the currently served frontend outside this change. Whole-dist replacement would violate minimal-change / runtime-first safety.
- Therefore current production Account UI does not yet visibly contain the new `平台会话` column.

## Scheduler IPv4 finding

- Current Scheduler command: `python scheduler/main.py`.
- Current Scheduler executor count inside the container: `1`.
- LISTEN_BEFORE: IPv6 `::` behavior; `[::1]:8091/health` = HTTP 200 and DB connected.
- `127.0.0.1:8091/health` = connection refused inside the container.
- `127.0.0.1:28091/health` is not usable from the host despite the Docker IPv4 port binding.
- Runtime environment does not explicitly set `HOST`; existing `_bootstrap.py` resolves the configured/default host through `resolve_listen_host()`.
- Existing application configuration already supports `HOST=0.0.0.0`; no change to `common/utils/network_utils.py` is necessary or allowed.
- The current `.local/chg0017-candidate/docker-compose.yml` does not define a Scheduler service, and no separate authoritative Scheduler manifest was found in that deployment directory. The current Scheduler container also lacks the compose ownership metadata used by the other formal services.
- Because the authoritative single-instance recreate path cannot be proven, no Scheduler container was stopped, replaced, or created. This is intentionally `BLOCKED` rather than risking a second executor.
- Scheduled task rows remain unchanged: 21 rows, zero duplicate task codes; enabled tasks remain `api_cookie_renew`, `day_switch`, `fetch_items`, `polish`.

## Comparison

- GITHUB_LOCAL_MATCH=false — default-branch SHA `99b81dd...` differs from the local feature-branch SHA `bad1bb8...`.
- LOCAL_RUNTIME_MATCH=false — production images are patched CHG-0018/CHG-0019 runtime builds and runtime Session lifecycle content is not safely reproducible from the current dirty local delivery checkout as one exact build.
- GITHUB_RUNTIME_MATCH=false — current default-branch Git state is not the exact build identity embedded in the running production images.

No rebuild, redeploy, merge, rebase, upstream sync, QR login, Cookie manual refresh, product publish, Material creation, category change, or message send was performed to force these states to match.
