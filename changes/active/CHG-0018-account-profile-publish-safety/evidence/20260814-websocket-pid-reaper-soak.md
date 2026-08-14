# WebSocket PID reaper / Session maintenance bounded-resource closure — 2026-08-14

## Scope

- Reuse decision: `PATCH_UPSTREAM`.
- Confirmed blocker only: repeated canonical Browser Session health/maintenance caused WebSocket container PID growth until all enabled WebSocket connections became disconnected.
- No Publisher, Session architecture, WebSocket manager, Cookie value, QR/login flow, message sender, product action, Scheduler owner, database schema, or Profile data was replaced.
- This turn's actual implementation delta is limited to Docker Compose WebSocket `init: true` plus focused regression coverage.

## Direct runtime root-cause evidence

Before the fix, the same production WebSocket container had already reproduced the historical failure pattern:

- Historical recurrence: approximately `20051` Docker PIDs and approximately `2.83 GiB` memory; stop/start of the same container returned it to a small baseline.
- Current controlled pre-fix baseline before this repair: Docker `2443` PIDs and `868.9 MiB`.
- `/proc` classification immediately before the fix: `2303` zombies; `2314` Chrome-family processes in the namespace.
- Zombie names: `chrome=1373`, `chrome_crashpad=918`, `chrome-headless=12`.
- All `2303/2303` zombies had `PPID=1`.
- Container PID 1 was the Python WebSocket process; Docker `HostConfig.Init=<nil>`.
- A single read-only canonical Browser health check changed zombie count `2027 -> 2044`, i.e. one correctly completed browser lifecycle still left 17 unreaped Chrome-family children.

Root cause: Chromium/Crashpad grandchildren exited after Playwright page/context/driver cleanup, were reparented to container PID 1, and were not reaped because the WebSocket container ran Python directly as PID 1 without Docker init/tini. The primary leak was zombie reaping, not live Chromium instances remaining open.

`PID_DOMINANT_PROCESS=chrome/chrome_crashpad zombies`

`CHILD_PROCESS_PARENT=container PID1 python`

`ZOMBIE_PROCESS_ROOT_CAUSE=CONTAINER_PID1_NOT_REAPING_EXITED_CHROMIUM_GRANDCHILDREN`

## Existing lifecycle / overlap verification

The current production Scheduler and WebSocket lifecycle were inspected before changing anything:

- `api_cookie_renew` is the single production Session maintenance owner.
- Interval remains `3600s`.
- Scheduler uses one module-global `ApiCookieRenewTaskService` with an `asyncio.Lock` single-flight guard.
- The scheduler loop awaits `execute()` to finish and only then sleeps the configured interval; it does not fire-and-forget a second batch.
- Accounts are processed serially.
- Session maintain/health uses one direct `aiohttp.ClientSession` POST per account; there is no generic HTTP retry loop around `/internal/session/maintain` or `/internal/session/health`.
- Active maintain client timeout remains 420 seconds; disabled read-only health remains 180 seconds.
- Canonical Browser health and browser renew both use the existing `AccountBrowserLockManager` plus existing global browser slot. Production `MAX_CAPTCHA_CONCURRENT=1`.
- Both `_sync_check_real_browser_login` and `_sync_browser_renew` already use `finally` to close page/context/Playwright and release account lock/global slot on success, exception, and eventual completion after caller cancellation.
- `run_browser_task` uses the bounded browser thread pool rather than unlimited threads.
- Disabled accounts remain health-only and never call the existing auto-reply start path.

Therefore no second lock system, Scheduler, Session system, or WebSocket manager was added.

## Minimal repair

`docker-compose.yml` WebSocket service now sets:

`init: true`

This uses Docker's built-in init/reaper as PID 1. It does not delete or replace `browser_data/user_<account_id>` persistent Profile data. It does not change the WebSocket image, application command, Cookie data, DB schema, or business logic.

Production was recreated using the exact existing WebSocket image/config/volumes/network/ports with the sole runtime addition `--init`. Scheduler, Backend, Frontend, MySQL, Redis, and Docker Desktop were not restarted.

After cutover:

- `HostConfig.Init=true`
- PID 1: `docker-init`
- baseline: `7` PIDs, `117.4 MiB`
- container-internal zombie count: `0`
- Chromium process count at idle: `0`

## Controlled runtime soak

The soak used the existing canonical Browser health implementation against every current non-deleted account, serially, without persisting returned browser Cookie changes back to the account database. It exercises the same Playwright/Chromium process lifecycle used by Session health/maintenance.

Cycle 1, 11 accounts:

- PIDs: `7 -> peak 153 -> 7`
- Memory: `117.1 MiB -> peak 640.9 MiB -> 135 MiB`
- end zombies/chromium/playwright drivers: `0/0/0`

Cycle 2, 11 accounts:

- PIDs: `7 -> peak 153 -> 7`
- Memory: `134.3 MiB -> peak 639.5 MiB -> 142.6 MiB`
- end zombies/chromium/playwright drivers: `0/0/0`
- Session observations: 4 `REAL_BROWSER_LOGIN_READY`, 6 `HUMAN_QR_REQUIRED`, 1 `COOLDOWN`

Cycle 3, 11 accounts:

- PIDs: `8 -> peak 283 -> 8`
- Memory: `149.5 MiB -> peak 1031.2 MiB -> 158.3 MiB`
- end zombies/chromium/playwright drivers: `0/0/0`
- Session observations: 3 `REAL_BROWSER_LOGIN_READY`, 5 `HUMAN_QR_REQUIRED`, 3 `COOLDOWN`

The peak is transient browser work; the end-of-cycle PID baseline does not climb. No orphan/zombie growth was observed across three full all-account cycles.

`PID_GROWTH_BOUNDED=true`

`MEMORY_GROWTH_BOUNDED=true`

`ORPHAN_PROCESS_GROWTH=false`

## WebSocket recovery and disabled-account isolation

A controlled enabled-account WebSocket recovery used only the existing manager path:

- before: `running=true`, `connected=true`
- after existing stop: `running=false`, `connected=false`
- after existing start: `running=true`, `connected=true`

No container restart, QR scan, relogin, message send, product action, or Cookie write was used for this recovery.

All disabled accounts remained `running=false`, `connected=false` after the repair/soak.

`AUTO_REPLY_RECOVERY_WITHOUT_RESTART=true`

`DISABLED_ACCOUNT_BUSINESS_ISOLATION_PRESERVED=true`

`HUMAN_QR_REQUIRED` remains a Browser Session state and is independent from WebSocket auto-reply connectivity.

## Focused validation

Clean cumulative patch verification from base `64c245bc85ac56e34339fa056b0e291a16a3843b`:

- Patch clean apply check: PASS.
- Patch apply: PASS.
- Focused tests: `51 passed`.
- Source diff check: PASS.
- Cumulative patch file count: 30.
- Content equivalence ignoring CRLF: PASS.
- Byte equivalence: `CRLF_DIFF_ONLY` for one file.

Vendor patch:

`vendor/patches/xianyu-auto-reply/64c245-chg0018-websocket-pid-reaper.patch`

SHA256:

`A87FA6CA1CDE2073A1C063A2B962FA40B163B62101E41E390C2EFD32DF8DF85A`

## Side effects

- Real products published: 0
- Real products relisted: 0
- Real products offlined: 0
- Real messages sent: 0
- QR scans triggered: 0
- Relogins triggered: 0
- Account Cookie values intentionally modified by this task: 0
- Profile directories deleted: 0
- New Scheduler created: false
- New Session system created: false
- New WebSocket manager created: false
