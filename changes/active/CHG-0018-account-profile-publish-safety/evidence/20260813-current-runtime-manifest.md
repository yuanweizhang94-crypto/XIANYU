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
| frontend | `xianyu_chg0017_frontend` | `xianyu-chg0020-frontend:ui-asset-integrity-20260813` | `127.0.0.1:19000 -> 80` | `/health` HTTP 200 / Docker healthy |
| backend_web | `xianyu_chg0017_backend_web` | `xianyu-chg0018-backend-web:account-session-ui-20260813` | `127.0.0.1:28089 -> 8089` | `/health` HTTP 200, DB connected |
| websocket | `xianyu_chg0017_websocket` | `xianyu-chg0018-websocket:session-lifecycle-20260812-r2` | `127.0.0.1:28090 -> 8090` | `/health` HTTP 200, DB connected / Docker healthy |
| scheduler | `xianyu_chg0017_scheduler` | `xianyu-chg0018-scheduler:session-lifecycle-20260812` | `127.0.0.1:28091 -> 8091` | IPv4 container and host `/health` HTTP 200, DB connected; `HOST=0.0.0.0` |
| mysql | `xianyu_chg0017_mysql` | `mysql:8.0` | `127.0.0.1:23306 -> 3306` | Docker healthy |
| redis | `xianyu_chg0017_redis` | `redis:7.4-alpine` | `127.0.0.1:26379 -> 6379` | Docker healthy |

All six host ports are listening. Final SPA route checks returned HTTP 200 for `/login`, `/dashboard`, `/accounts`, `/product-publish/materials`, `/items`, `/product-publish/single`, `/product-publish/logs`, `/online-chat-new`, `/admin/scheduled-tasks`, `/product-monitor/overview`, `/risk-logs`, `/admin/api-cookie-renew-batches`, `/admin/cookies-refresh-batches`, and `/settings`.

## AUTHORITATIVE_PRODUCTION_RUNTIME_LIFECYCLE

`AUTHORITATIVE_PRODUCTION_RUNTIME_LIFECYCLE=true`. This section is the single current recovery record for the six-service production stack. Historical compose/evidence remains useful as provenance, but must not be used to create an additional parallel production stack.

| Service | Canonical container | Image | Entrypoint / command | Host port | Network / dependency | Restart | Mounts / volumes | Health / required non-sensitive config |
|---|---|---|---|---|---|---|---|---|
| Frontend | `xianyu_chg0017_frontend` | `xianyu-chg0020-frontend:ui-asset-integrity-20260813` | `/docker-entrypoint.sh` -> `nginx -g 'daemon off;'` | `127.0.0.1:19000 -> 80` | `xianyu_chg0017_network`; **required link** `xianyu_chg0017_backend_web:backend-web` | `unless-stopped` | none | Docker health probes `127.0.0.1:80`; host `/health` HTTP 200 |
| Backend | `xianyu_chg0017_backend_web` | `xianyu-chg0018-backend-web:account-session-ui-20260813` | `python backend-web/main.py` | `127.0.0.1:28089 -> 8089` | `xianyu_chg0017_network`; depends on MySQL/Redis by existing runtime configuration | `unless-stopped` | `xianyu_chg0017_backend_logs:/app/backend-web/logs`; `xianyu_chg0017_backup_data:/app/backups`; `xianyu_chg0017_browser_data:/app/browser_data`; `xianyu_chg0017_static_data:/app/static` | `HOST=0.0.0.0`; `/health` HTTP 200 / DB connected |
| WebSocket | `xianyu_chg0017_websocket` | `xianyu-chg0018-websocket:session-lifecycle-20260812-r2` | `python websocket/main.py` | `127.0.0.1:28090 -> 8090` | `xianyu_chg0017_network`; existing MySQL/Redis/session dependencies | `unless-stopped` | `xianyu_chg0017_static_data:/app/static`; `xianyu_chg0017_websocket_logs:/app/websocket/logs`; `xianyu_chg0017_browser_data:/app/browser_data` | `HOST=0.0.0.0`; host `/health` HTTP 200 / DB connected |
| Scheduler | `xianyu_chg0017_scheduler` | `xianyu-chg0018-scheduler:session-lifecycle-20260812` | `python scheduler/main.py` | `127.0.0.1:28091 -> 8091` | `xianyu_chg0017_network`; existing DB/Redis task dependencies | `unless-stopped` | none | `SINGLE_INSTANCE_ONLY=true`; `ACTIVE_SCHEDULER_EXECUTORS_MAX=1`; `HOST=0.0.0.0`; host `/health` HTTP 200 / DB connected |
| MySQL | `xianyu_chg0017_mysql` | `mysql:8.0` | `docker-entrypoint.sh` with existing utf8mb4/time-zone/server limits | `127.0.0.1:23306 -> 3306` | `xianyu_chg0017_network`; aliases `mysql`, `xianyu_chg0017_mysql` | `unless-stopped` | `xianyu_chg0017_mysql_data:/var/lib/mysql` | Docker `mysqladmin ping`; credentials remain runtime secrets and are not recorded here |
| Redis | `xianyu_chg0017_redis` | `redis:7.4-alpine` | `docker-entrypoint.sh` -> existing authenticated Redis configuration with `128mb`, `allkeys-lru`, AOF enabled | `127.0.0.1:26379 -> 6379` | `xianyu_chg0017_network`; aliases `redis`, `xianyu_chg0017_redis` | `unless-stopped` | `xianyu_chg0017_redis_data:/data` | Docker `redis-cli ... ping | grep PONG`; authentication material remains a runtime secret and is not recorded here |

Recovery rules:

1. Never create a second Scheduler. Stop the canonical Scheduler and prove active executor count is `0` before recreating it; after start the count must be exactly `1`.
2. Recreate a service only from the current parameters above plus its existing secret-bearing environment, which must be obtained from the live/approved runtime without being copied into evidence.
3. Frontend recreation must preserve the `backend-web` link/network alias; omitting it prevents nginx from resolving its upstream.
4. Backend/Frontend overlay delivery must retain stopped prior containers as rollback points when practical; do not rebuild unrelated services merely to align image names or Git SHAs.
5. MySQL/Redis persistent volumes are authoritative data volumes and are never replaced as part of an application UI/API repair.

## Frontend UI asset integrity repair — 2026-08-13

- `ROOT_CAUSE=CURRENT_FRONTEND_DIST_TAILWIND_UTILITY_TRUNCATION`.
- `ROOT_CAUSE_TYPE=OTHER` — the CSS asset itself existed and had correct `text/css`; the defect was that the served production CSS content was incomplete, not an HTTP 404, lazy-chunk absence, MIME error, SPA HTML fallback, browser-cache-only issue, or Data Analysis source regression.
- Before repair, `xianyu-chg0019-frontend:publish-status-semantics-20260813` served `/assets/index-DkUehgo1.css` at only 19,256 bytes. It contained compiled Tailwind base/theme content but omitted core utilities including `.flex{display:flex}` and `.grid{display:grid}`. This directly collapsed Sidebar/card/layout styling into the observed bare-text vertical UI.
- The same pre-repair runtime already served `DataOverview-BZMTUWsM.js` and its `CartesianChart`, account API, and lucide shared chunks with HTTP 200, JavaScript MIME, non-HTML bodies. Therefore `LAZY_CHUNK_MISSING=false` and `SOURCE_DATA_ANALYSIS_BUG=false`; Data Analysis appeared blank because the shared utility CSS was truncated, not because upstream Data Analysis was absent.
- Narrow source verification on the clean formal replay confirmed `frontend/src/main.tsx` still imports `./styles/globals.css` and `./styles/theme.css`; `App.tsx` still maps `data-analysis/overview` to the existing lazy `DataOverview`; `DataOverview.tsx`, `BrowseDistribution.tsx`, and `api/data_analysis.ts` remain present. Backend OpenAPI still exposes `/api/v1/data-analysis/seller-summary` and `/api/v1/data-analysis/browse-summary`. No Data Analysis business source or Backend route was changed.
- A clean formal replay production build (`existing CHG-0018 -> existing CHG-0019 formal delivery -> Account Session UI -> Publish Status Semantics`) passed TypeScript and Vite build and produced `/assets/index-CUOAPvoN.css` at 132,365 bytes with `.flex{display:flex}` and `.grid{display:grid}`, plus `DataOverview-CKRPofVK.js`, `Accounts-DZSkhUKS.js`, and `PublishLogs-BtxIkREx.js` from the same build.
- The repaired image is `xianyu-chg0020-frontend:ui-asset-integrity-20260813`. It reuses the already-installed nginx/runtime image only as the base, executes `rm -rf /usr/share/nginx/html/*`, then copies the complete clean replay `dist` once. The old frontend container is retained as `xianyu_chg0017_frontend_pre_ui_repair_20260813_1440` for rollback. The canonical container remains `xianyu_chg0017_frontend`, with `127.0.0.1:19000 -> 80`, `xianyu_chg0017_network`, required link `xianyu_chg0017_backend_web:backend-web`, and restart policy `unless-stopped`.
- Post-repair index references `/assets/index-CHEc0Nuw.js` and `/assets/index-CUOAPvoN.css`; both exist, are non-empty, return HTTP 200 with correct MIME, and are not HTML fallback bodies. `DataOverview-CKRPofVK.js` and all of its discovered JS dependencies return HTTP 200 with JavaScript MIME and non-HTML bodies.
- Cache-disabled Playwright render validation used a fresh browser context with local API mocks only; no production platform data request was sent. Dashboard rendered with Sidebar width 224 px, main content starting at x=224, stat card width 148 px, and the page header computed as `display:flex`. Data Analysis rendered `数据总览`, the selected `选择账号` option, `近1天`, `近7天`, `近30天`, and `自定义`; `seller-summary` request count was exactly 0. Account `平台会话` and Publish Log `SUBMITTED/RUNNING/SUCCESS/FAILED/UNKNOWN` semantics also rendered successfully under safe mock data.
- Browser asset acceptance after repair: `FAILED_CSS_REQUESTS=0`, `FAILED_JS_REQUESTS=0`, `CHUNK_LOAD_ERRORS=0`, `CSS_MIME_ERRORS=0`, `JS_MIME_ERRORS=0`, `ASSET_HTML_FALLBACKS=0`, browser console errors=0, page errors=0.
- Deployment rules are now explicit: `FRONTEND_DIST_MUST_BE_SELF_CONSISTENT=true`; `INDEX_AND_ASSETS_SAME_BUILD=true`; `NO_ADDITIVE_MIXED_GENERATION_DIST=true`; `ASSET_VALIDATION_REQUIRES_CONTENT_TYPE_AND_BODY=true`; `SPA_HTTP_200_ALONE_IS_NOT_ACCEPTANCE=true`. Frontend acceptance must verify index-referenced CSS/JS, lazy chunks, MIME/body, core compiled utilities, and actual browser DOM/CSS render before completion.
- No Publisher, Session lifecycle, Cookie/QR logic, Scheduler business logic, Material system, Business Adapter, database schema, category system, real publish, real message send, Material creation, QR flow, Cookie refresh, or seller-summary platform action was triggered by this repair.

## Remaining-function acceptance closeout

- Material: production GET list and detail APIs returned HTTP 200 with 15 existing materials; all 15 image reference lists parse, none are empty, and no direct local reference is missing. No material was created.
- Publish page: production route and existing account/material APIs are healthy; the page uses the existing `publishSingle` API and existing Publisher chain. Required pre-submit validation exists for account, title, description, positive price, and at least one image. Final publish was not retriggered.
- Publish log: production API returned 216 historical rows; persisted status counts include success/failed/publishing and there are zero persisted `success` rows without `item_id`/`item_url`. The UI now maps legacy storage values to canonical display semantics (`pending -> SUBMITTED`, `publishing -> RUNNING`, `failed -> FAILED`) and fail-closes a `success` row without item evidence to `UNKNOWN`.
- Business Adapter publish status: a new regression was found after Backend restart. Historical in-memory batch status expires with HTTP 200 / `success=false`, while persistent publish logs still contain the terminal result. The existing `xianyu_publish_status` resolver now falls back read-only to Publish Log by `batch_id`; five historical failed operations resolve to `FAILED` with their stored failure reasons, and an existing successful operation continues to resolve `SUCCESS` only with authoritative item/sync evidence. No publish was retriggered.
- Message: production Chat account API returned HTTP 200 with 11 accounts. Current Chat IM manager has 0 explicitly connected accounts; read paths fail closed with `账号未连接，请先连接`, and send path cannot report success without an existing connected client. No connection/send mutation was triggered.
- Session maintenance: Account API/UI still exposes persisted session state. Current natural state counts are `REAL_BROWSER_LOGIN_READY=3`, `SESSION_CHECK_PENDING=6`, `UNKNOWN=2`; maintenance task rows remain 21 with zero duplicate task codes. No QR, slider, manual refresh, or forced expiry was triggered.
- Other UI: Scheduled Tasks, Product Monitor overview, Risk Control, API Cookie Renew logs, Browser Refresh logs, and System Settings production APIs returned HTTP 200; corresponding production frontend bundles/routes are present. Empty Product Monitor datasets are a valid current data state, not a page failure.

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

## Acceptance closeout change boundary

This run changed only the following functional artifacts:

- Upstream delivery source delta: `frontend/src/pages/product-publish/PublishLogs.tsx` (canonical status presentation only).
- XIANYU formal vendor delta: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-publish-status-semantics-closeout.patch`.
- Local execution Business Adapter runtime source: `D:\TikTok_Auto\devspace_proxy\proxy.cjs` (read-only historical publish-log fallback when batch status has expired).
- Local execution installation record: `D:\tmp\company-local-execution-tool\INSTALLATION_MANIFEST.json` (updated Proxy hash and publish-status semantics evidence).
- This existing production runtime manifest.

No Publisher core source, Session lifecycle source, database schema, Scheduler business logic, Message sender, category state machine, Material system, or new execution owner was created or changed.

## Closeout validation

- Repository verification: `python scripts/verify_repository.py` = PASS (`595 passed`, repository verification passed).
- Session delta staged diff check: PASS.
- Production HTTP: frontend 200, backend 200, websocket 200, Account/Login/Dashboard/Items SPA routes 200.
- Production Account bundle contains `平台会话`; running Backend Account route contains `session_state` and `session_state_updated_at`.
- Scheduler IPv4: container `127.0.0.1:8091/health` 200; host `127.0.0.1:28091/health` 200; DB connected; active executors 1.
- Real products published by this closeout: 0. Real messages sent by this closeout: 0. QR triggers: 0. Manual Cookie refresh triggers: 0.
