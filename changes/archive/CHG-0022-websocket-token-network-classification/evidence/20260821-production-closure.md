# CHG-0022 production closure evidence — 2026-08-21

Status: VERIFYING

Change ID: CHG-0022-websocket-token-network-classification

## Scope gate

Two residual CHG-0018 evidence files were still physically under `changes/active` on task base `f06a81e82ea6ca7717ce9d4abe77d18dccaa8855` even though CHG-0018 itself was archived. On an isolated task-base worktree, adding a CHG-0022 active Change without moving those files caused `validate_change.py` to report `expected at most one active change, found 2`. Therefore moving only those two evidence files, unchanged, back under the already-archived CHG-0018 evidence directory is a hard current-governance prerequisite for CHG-0022 rather than unrelated archive cleanup.

No CHG-0018 content repair and no CHG-0020 repair were performed.

## Repository verifier equivalence

A clean task-base worktree containing only the required CHG-0018 evidence relocation, with no CHG-0022 patch, and the patched CHG-0022 worktree both produced the same verifier failure:

`missing archived change files for CHG-0020-zidongzhua-market-search: design.md, tasks.md`

Therefore:

- `VERIFY_FAILURE_PRE_EXISTING=true`
- `CHG0022_NEW_VERIFY_FAILURES=0`
- `REPOSITORY_VERIFY=BLOCKED_BY_PROVEN_PRE_EXISTING_UNRELATED_GOVERNANCE_FAILURE`

## Executable behavior tests

The reconnect patch was exercised with an executable `XianyuAsync.main()` fault harness:

- pre-connect DNS/gaierror entered the network path;
- existing Token remained unchanged;
- Token refresh/remote Token call count was zero;
- network backoff executed once;
- short-disconnect accounting was not invoked before a real connection;
- the next connection succeeded with the same Token.

The current production `CookieTokenManager.refresh_token()` method was executed in a separate isolated process with all external I/O monkeypatched and an explicit `FAIL_SYS_TOKEN_EXPIRED` response:

- auth failure classified true;
- two Token attempts total (initial + one bounded expiry retry);
- cache invalidation exactly once after the bounded retry failed;
- password login calls zero;
- network-backoff path false.

The current production `CookieTokenManager.refresh_token()` was also executed with synthetic authoritative `HUMAN_QR_REQUIRED` metadata:

- remote Token calls zero;
- password login calls zero;
- CAPTCHA calls zero;
- Token cache invalidation zero;
- returned fail-closed without a loop.

The current production `TokenManager._execute_cookie_refresh()` was executed with a connected live Token:

- existing Token reused;
- active Token refresh calls zero;
- maintenance timestamp advanced normally.

## Immutable runtime image

Current production authority was re-read immediately before build and deployment:

- container: `xianyu_chg0017_websocket`
- base image tag: `xianyu-chg0018-websocket:recent-regression-cleanup-20260815-r1`
- base image ID: `sha256:1a4c12ff465faf2ec8e3b107a0f1344ca117624b5b9d9aaf9862ee275565fed2`
- pre-change `xianyu_async.py` SHA256: `fe795325e14050957b01714c26dffa135479f3d182df39301f6a9ad5fdb77797`

The normal Dockerfile build path failed before image creation because the Dockerfile frontend could not be fetched from Docker Hub. No production state changed. The image was then built fully offline from the exact current image by creating a stopped temporary container, replacing only `/app/websocket/app/services/xianyu/xianyu_async.py`, verifying Docker diff contained only that file plus parent-directory metadata changes, and committing an immutable image.

Final image:

- tag: `xianyu-chg0022-websocket:token-network-classification-20260821-r1`
- image ID: `sha256:397793b22b2cfae4c3c1c6ed962e51d762174043f9bf3629c3db60944022e30c`
- post-change file SHA256: `9e085fac9e4d5030a9b0ddc329e50434e23ea243dffdf3cc1161696ffd6a4fd5`
- candidate/runtime `py_compile`: PASS
- new image config equals base image config: true

A stopped pre-create dry run verified the replacement configuration matched current production for environment fingerprint, mounts, network, ports, restart policy, command, Docker init, healthcheck, workdir and labels; image identity was the sole intended delta.

## WebSocket-only production activation

Only `xianyu_chg0017_websocket` was stopped, removed and recreated using the CHG-0022 image. Existing named volumes, network, environment, ports and command were retained.

Post-deployment:

- HTTP `/health`: 200;
- WebSocket container running;
- restart count: 0;
- runtime source SHA equals the expected post-change SHA;
- runtime compile: PASS;
- Frontend, Backend, Scheduler, MySQL and Redis container IDs remained unchanged.

## Account and Token readback

All seven active Auto Reply account tasks are currently `running=true`, `is_connected=true`, `connection_state=connected`, with current heartbeat responses.

Four accounts use valid cache state `success_from_cache`. Three accounts use the existing `success_from_expired_startup_cache` path and also connected successfully. For those three, authoritative Browser Session metadata was independently read from the database and still remains `HUMAN_QR_REQUIRED` with the existing official-renewal failure reason. No QR, password or CAPTCHA action was taken. This preserves the existing separation between Browser Session readiness and Auto Reply WebSocket usability.

Post-deployment log readback observed:

- remote Token start: 0;
- remote Token success: 0;
- Token cache invalidation/clear: 0;
- network reconnect-loop marker: 0;
- repeated heartbeat success;
- healthy maintenance explicitly skipped active Token refresh.

No natural DNS outage occurred in this production observation window, so the production claim is `NO_NEW_STORM_OBSERVED`; live DNS-outage Canary is not claimed. Fault behavior is proven by the isolated executable tests above.

## Safety

- real messages sent: 0
- real product mutations: 0
- QR actions: 0
- COMPANY code changes: 0
- JZAI code changes: 0
- real payment actions: 0
