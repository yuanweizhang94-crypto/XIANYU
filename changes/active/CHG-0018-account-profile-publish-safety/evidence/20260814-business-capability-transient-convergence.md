# CHG-0018 Business Capability Transient Convergence

Date: 2026-08-14

## Scope

Production repair for account business-capability states that could remain `RECOVERING`, `CHECKING`, `SESSION_CHECK_PENDING`, or `PENDING` long after the real operation had ended.

This repair reuses the existing WebSocket manager, Chat readiness, QR auth convergence, Session maintenance metadata, Publisher preflight, and `business_capabilities` response. It does not create a second status system, Scheduler, Session system, Chat system, WebSocket manager, table, Redis state, or worker.

## Starting authority

- Branch: `feat/CHG-0018-account-profile-publish-safety`
- Formal GitHub baseline: `218e7504693a4e43fc1305c55fcaf0ffff972665`
- Vendor Patch base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- Active change: `CHG-0018-account-profile-publish-safety`
- `docs/AI_PROJECT_HANDOFF.md` was not present in the checkout and no content was inferred for it.

## Production root cause before repair

Six enabled production accounts were read without QR login, Chat business authentication, Browser health, or Publish execution.

Observed old effective-state behavior:

- Auto Reply: `WS_RUNNING=true` plus `WS_CONNECTED=false` mapped to `RECOVERING`, even though the API did not expose whether a bounded reconnect operation was active.
- Chat: stored `PENDING`/unrecognized readiness mapped unconditionally to `RECOVERING`. All six enabled accounts had stale `PENDING` readiness.
- Publish: `SESSION_CHECK_PENDING` or publish `PENDING` mapped unconditionally to `CHECKING`. All six enabled accounts had this stale raw state, with timestamps already hours old.
- Frontend rendered Backend `business_capabilities` directly, but normal account-list refresh had no transient-aware polling outside the existing QR-specific 0/2/5/10 second refetch sequence.

Therefore the defect was primarily incorrect Backend effective-state semantics plus missing normal transient-aware frontend polling, not merely browser cache.

Baseline visible transient counts:

- Stuck `RECOVERING`: 11 capability cells (5 Auto Reply + 6 Chat).
- Stuck `CHECKING`: 6 Publish capability cells.

## Minimal repair

### Auto Reply

The existing WebSocket `ConnectionManager` now exposes only runtime facts already owned by that manager:

- `reconnect_active`
- `recovery_started_at`
- `recovery_deadline_at`
- `last_attempt_at`
- `next_retry_at`
- `last_connected_at`
- `last_error`

The recovery deadline is derived from the manager's existing connection open timeout, retry caps, retry jitter, maximum failure counts, and long network cooldown. No separate recovery scheduler is introduced.

Effective state:

- connected -> `ONLINE`
- disconnected + real unexpired reconnect lease -> `RECOVERING`
- disconnected + no active lease or expired lease -> `OFFLINE`
- `auto_recoverable=true` remains independent from `recovery_active`.

### Chat

The Account API continues to use `ImSessionManager.read_only_diagnostic()` only. It never calls `get_or_connect`, Token renewal, Cookie refresh, client replacement, or message send.

Existing QR/auth convergence now records a bounded `recovery_active` lease in its existing `auth_convergence` metadata. The deadline is derived from its existing actual `asyncio.wait_for` bounds: Browser health 180s, Auto Reply restart 30s, status read 5s, Chat connect 90s, Chat conversation metadata read 30s, Publish preflight 90s, with maximum two rounds.

Effective state:

- stored `READY` or existing connected/matching Chat client -> `READY`
- platform verification -> `PLATFORM_VERIFICATION_REQUIRED`
- QR/session-expired Chat auth -> `LOGIN_REQUIRED`
- stored temporary failure -> `TEMPORARY_FAILURE`
- `PENDING` only becomes `RECOVERING` while the bounded auth convergence lease is actually active
- stale/no-active `PENDING` -> `TEMPORARY_FAILURE` with a sanitized reason.

### Publish / Browser Session

Existing Session health/maintain operations now set a `check_active` lease inside existing `metadata_json.session_maintenance` and clear it in `finally`.

Existing owner deadlines are reused:

- Session health: 180s
- enabled Session maintain: 420s

Existing Publisher preflight now sets a `check_active` lease inside `session_maintenance.consumers.publish`, using its existing 90s preflight bound, and clears it in `finally`. Final readiness recording preserves lease metadata while updating the final state.

Effective state:

- real active Session/Publish check -> `CHECKING`
- real active Session renewal -> `RECOVERING`
- stale/no-active `SESSION_CHECK_PENDING` or publish `PENDING` -> `RETRY_LATER` with label `待检查`
- expired operation lease cannot remain `CHECKING`
- QR, platform verification, restriction, cooldown, and READY terminal semantics remain distinct.

### Frontend

The Account page remains Backend-authoritative. Every successful account-list response uses `setAccounts(result.data)` and replaces the prior UI state.

Normal account-list transient-aware polling is now enabled only when Backend returns an actual active operation:

- `auto_reply.recovery_active=true`
- `chat.recovery_active=true`
- `publish.recovery_active=true`
- `publish.check_active=true`

Polling interval: 4 seconds, read-only Account GET only. It stops automatically when all active flags are false. It does not call QR login, Chat connect/auth, Browser health, or Publish. The existing QR-specific 0/2/5/10 second refetch remains unchanged.

Tooltip now exposes `recovery_active`, `check_active`, and `deadline_at`. Real `RECOVERING`/`CHECKING` uses blue status styling; terminal waiting/failure states remain yellow/red/orange/gray according to existing semantics.

## Offline verification

- Python compile for changed Backend/Common/WebSocket modules: PASS.
- Focused CHG-0018 tests: `177 passed`.
- New transient-convergence behavior tests: included in the 177 focused passes.
- Frontend production build: PASS (`tsc && vite build`, 2685 modules transformed).
- Source `git diff --check`: PASS.

## Clean-base Vendor Patch verification

- Patch base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- Patch file count: 37.
- Patch SHA256: `6AC54BCC10D57F18B006D043D745B102459323CDEFD8423E7FD1C1BBA77DA10F`
- Clean `git apply --check`: PASS.
- Fresh clean-base apply: PASS.
- Focused tests after fresh patch apply: `177 passed`.
- `CONTENT_EQUIVALENCE_IGNORING_CRLF=PASS`.
- `PATCH_BYTE_EQUIVALENCE=CRLF_DIFF_ONLY` (2 files; content-equivalent).

## Production deployment

Only changed services were deployed:

- Backend: changed
- Frontend: changed
- WebSocket: changed
- Scheduler: unchanged
- MySQL: unchanged
- Redis: unchanged

Post-deploy health:

- Frontend HTTP 200
- Backend HTTP 200
- WebSocket HTTP 200
- Scheduler HTTP 200
- Scheduler executor process count: 1
- WebSocket PID1: `docker-init`

## Production read-only acceptance

No QR scan, Chat business authentication, Browser health, Session maintain, or Publish preflight was triggered by status acceptance.

All six current enabled accounts converged to these effective states:

| Account | Auto Reply | recovery_active | Chat | recovery_active | Publish | check_active |
|---|---|---:|---|---:|---|---:|
| 1034641456 | ONLINE | false | TEMPORARY_FAILURE | false | RETRY_LATER (`待检查`) | false |
| 2196106636 | ONLINE | false | TEMPORARY_FAILURE | false | RETRY_LATER (`待检查`) | false |
| 2214313339860 | ONLINE | false | TEMPORARY_FAILURE | false | RETRY_LATER (`待检查`) | false |
| 2217936413500 | ONLINE | false | TEMPORARY_FAILURE | false | RETRY_LATER (`待检查`) | false |
| 2219319284219 | ONLINE | false | TEMPORARY_FAILURE | false | RETRY_LATER (`待检查`) | false |
| 2858469041 | ONLINE | false | TEMPORARY_FAILURE | false | RETRY_LATER (`待检查`) | false |

The Chat result is intentionally not upgraded by a network auth call: the stored readiness is `PENDING`, no auth convergence is active, and no existing matching Chat client is present in the read-only acceptance process. `TEMPORARY_FAILURE` is therefore the truthful effective state until normal Chat business activity or a future authorized auth convergence records READY.

The Publish result is intentionally not upgraded by Browser/Publisher activity: stored Session/Publish state is pending but there is no current check lease. `待检查` is therefore truthful until the existing Session/Publisher owner actually runs.

Final invalid transient counts:

- Auto Reply `RECOVERING` without active task: 0
- Chat `RECOVERING` without active task: 0
- Publish `CHECKING` without active task: 0
- Stuck `RECOVERING` count after repair: 0
- Stuck `CHECKING` count after repair: 0

Read-only acceptance side effects, measured before/after the status read:

- Account Cookie fingerprints unchanged: true
- Chat/Auto-Reply token-cache metadata unchanged: true
- Publish log count delta: 0
- Auto Reply message log count delta: 0
- QR scans triggered by test: 0
- Real products published/relisted/offlined by test: 0
- Real messages sent: 0

## Frontend authority / refresh acceptance

The production bundle contains the new `recovery_active` and `check_active` fields and active-operation tooltip text. The initial Account page load and every later refetch replace UI rows directly from the Backend payload; there is no `window.location.reload()` or permanent optimistic `RECOVERING/CHECKING` store.

An authenticated interactive browser session was deliberately not harvested or forged for this acceptance, so no browser credential/token was read. F5 consistency is guaranteed by the deployed code path and production bundle: first render after API completion uses Backend effective state, and any actual transient operation is polled every 4 seconds until its active flag becomes false.

## Resource regression

After existing scheduled Browser work completed naturally:

- WebSocket zombies: 0
- Chromium processes idle: 0
- Playwright driver processes idle: 0
- WebSocket PID1: `docker-init`

No live Browser process was killed to obtain the idle result.

## Preserved CHG-0018 boundaries

- Single-QR consumer convergence: preserved by focused regression tests.
- Chat read-only diagnostic purity: preserved.
- WebSocket PID reaper: preserved.
- Disabled-account business isolation: preserved.
- Disabled-account item visibility: preserved.
- No new Scheduler/status/session/chat system: preserved.
- No DB schema change.

## Security / evidence boundary

This evidence intentionally contains no Cookie values, Token values, Authorization headers, QR payloads, passwords, API keys, private keys, customer messages, or browser Profile contents.
