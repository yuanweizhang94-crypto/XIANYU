# CHG-0036 Final Runtime, Preflight and Archive Closure Evidence

Date: 2026-08-30

## Authority

- `RUNTIME_BUSINESS_SOURCE_SHA=2df208780e556ace2230f0c6ce7d4e7252a33a25`
- PR #52 merged before Runtime closure.
- CHG-0036 regression guard commit `cef03d9478dbfb205ae64052e069cca0991a5583` and updated PR head `180060f22cf80ffb08d90e3c8da0f91ac221b23d` were proven ancestors of `2df208780e556ace2230f0c6ce7d4e7252a33a25`.
- `BUSINESS_RUNTIME_DELTA_AFTER_2DF2087=false` for this archive-only closure.

## Clean replay build authority

Production before CHG-0036 used the Account Status final-main Runtime lineage image `xianyu-chg0018-backend-web:account-status-final-5dd103e-20260829-r2`. Image-history/source fingerprinting proved the Publisher drift first appeared in the `auth-cookie-closure-20260819-r1` image family and was inherited by later Runtime images.

The immutable image `xianyu-chg0018-backend-web:publish-upstream-742fb58-20260817` was proven to contain the pinned canonical Publisher flow with zero forbidden `await session.refresh(account)` references and three `account.cookie = cookies_str` assignments.

The accepted clean candidate was built as an immutable multi-stage replay: retain the already-validated final-main Runtime lineage from the Account Status image, and restore only `backend-web/app/services/publish_execution_service.py` from the immutable pinned-742 canonical image. No file was copied from the running production container. Build-time gates reported:

- `PUBLISH_SERVICE_SHA256=a7294088cdde5aa72fa6dadca90c71f27da0789bd461855cb4b4afb2c67ce687`
- `FORBIDDEN_PATTERN_COUNT=0`
- `CANONICAL_COOKIE_ASSIGN_COUNT=3`
- `CURRENT_OWNER_FILES_PRESENT=true`

Candidate/production image:

`xianyu-chg0018-backend-web:chg0036-clean-replay-2df2087-20260830-r1`

An isolated `network_mode=none` candidate regression run completed with `CHG0036_CANDIDATE_RUNTIME_REGRESSION=PASS` and `REAL_PLATFORM_REQUESTS=0`.

## Backend-only activation

The final clean activation replaced only the Backend container through the guarded atomic replacement procedure. The temporary pre-clean CHG-0036 Backend container was `f5b2577458f7...`; it was retained as rollback under `xianyu_chg0017_backend_web_pre_chg0036_20260830_230318`. The accepted final Backend container is `43aa84929a3c...`.

Post-activation production facts:

- `PRODUCTION_BACKEND_IMAGE=xianyu-chg0018-backend-web:chg0036-clean-replay-2df2087-20260830-r1`
- `PRODUCTION_BACKEND_CONTAINER_ID=43aa84929a3c...`
- `org.opencontainers.image.revision=2df208780e556ace2230f0c6ce7d4e7252a33a25`
- `PRODUCTION_FORBIDDEN_PATTERN_COUNT=0`
- `PRODUCTION_CANONICAL_COOKIE_ASSIGN_COUNT=3`
- `PRODUCTION_CANONICAL_COOKIE_FLOW=PASS`
- `BACKEND_HEALTHY=true`
- network, `127.0.0.1:28089`, restart policy and the four existing Backend volumes were preserved.
- Frontend, WebSocket, Scheduler, MySQL and Redis container identities were proven unchanged by the replacement script.

No compose down, prune, volume deletion, database rebuild or Profile/Cookie/Session purge occurred.

## Read-only smoke

Account Status readback through the formal Backend returned HTTP 200 and authoritative healthy state for sampled enabled accounts, including `LOGIN_READY=true`, `ACCOUNT_ENABLED=true`, `ACCOUNT_ONLINE=true` and `PLATFORM_CERTIFICATION_REQUIRED=false`.

`ACCOUNT_STATUS_SMOKE_PASS=true`.

Chat smoke was intentionally read-only. The pre-clean temporary Backend startup evidence already showed natural Chat rehydration gaps (`ready=0` with eligible accounts skipped where cached Token was unavailable). After final clean activation, read-only conversation calls remained reachable through the Backend with HTTP 200 but sampled accounts reported `账号未连接`. No reconnect, login, Cookie refresh or account-state mutation was performed. No Backend 5xx, crash or import error was observed.

Therefore:

- `CHAT_READ_ONLY_SMOKE_RESULT=PASS_WITH_PRE_EXISTING_ACCOUNT_CONNECTION_STATE`
- `CHAT_RUNTIME_REGRESSION=false`

The natural disconnected IM state is not treated as a CHG-0036 Publisher regression.

## Material 94 hard-blocked production Runtime dry-run

The current production `PublishExecutorService` was exercised with real Material 94 read-only data while capability, Publisher transport, sync and persistence boundaries were replaced in-process with hard blockers/stubs. No MTOP/Goofish publish transport was allowed.

Result:

- `MATERIAL_94_RUNTIME_DRY_RUN=PASS`
- `PUBLISHER_BOUNDARY_REACHED=true`
- `SESSION_NAMEERROR_REPRODUCED=false`
- `SUCCESS_COUNT=0`
- `FAILED_COUNT=1`
- `ITEM_ID=None`
- `REAL_PUBLISH_HTTP_REQUEST_COUNT=0`
- `REAL_ITEM_CREATE_COUNT=0`
- `BLOCKED_TRANSPORT_ITEM_ID_NONE=true`

Production PublishLog readback found zero records for the dry-run batch and zero persisted SUCCESS rows.

`NO_FALSE_PUBLISH_SUCCESS=true`.

## Materials 94-103 read-only preflight

All ten Materials were read from production data without mutation. Each Material 94-103 was present, not deleted, priced at 135, had at least one image, had a non-empty category and valid quantity, and passed the configured prohibited-term check.

`ALL_MATERIAL_94_103_PREFLIGHT_PASS=true`.

No Material content was changed.

## Cross-account isolation

A three-account production Runtime dry-run used fully stubbed external transport and distinct refreshed capability cookies. Observed Publisher inputs remained account-scoped:

- account a -> refreshed-a-c-a
- account b -> refreshed-b-c-b
- account c -> refreshed-c-c-c

Result:

- `THREE_ACCOUNT_COOKIE_ISOLATION_PASS=true`
- `CROSS_ACCOUNT_SESSION_LEAK=false`
- `REAL_PUBLISH_HTTP_REQUEST_COUNT=0`
- `REAL_ITEM_CREATE_COUNT=0`

## Safety invariants

- `BUSINESS_SOURCE_LOGIC_CHANGED=false`
- `REAL_XIANYU_PUBLISH_EXECUTED=false`
- `MATERIALS_PUBLISHED_THIS_CHANGE=0`
- `ITEMS_CREATED_THIS_CHANGE=0`
- `AUTO_REPLY_CHANGED=false`
- `MESSAGE_SENT=false`
- `ORDER_CHANGED=false`
- `ACCOUNT_STATE_CHANGED=false`
- `MYSQL_DATA_LOSS=false`
- `REDIS_DATA_LOSS=false`
- `COOKIE_LOST=false`
- `SESSION_LOST=false`
- `PROFILE_LOST=false`

## Closure conclusion

`SOURCE_REGRESSION_CLOSURE_PASS=true`

`GITHUB_SOURCE_CLOSURE_PASS=true`

`RUNTIME_CLOSURE_PASS=true`

`MATERIAL_94_RUNTIME_PREFLIGHT_PASS=true`

`ALL_MATERIAL_94_103_PREFLIGHT_PASS=true`

`PUBLISHER_READY_FOR_FUTURE_CANARY=true`

This only means a future separately authorized single-item real canary may be attempted. No real canary is authorized or executed by this Change.
