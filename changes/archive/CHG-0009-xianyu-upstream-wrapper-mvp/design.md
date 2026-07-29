Change ID: CHG-0009-xianyu-upstream-wrapper-mvp
Status: ARCHIVED
# Design

## Architecture

`D:/xianyu` owns business rules, manual confirmation, idempotency, audit records, CLI entry points, and normalized Wrapper objects. `D:/xianyu-upstream-pilot` owns login, Cookie, Token, Session, WebSocket, and Xianyu protocol details.

The Wrapper talks to localhost-only upstream HTTP APIs where available. If message observation has no HTTP API, a strictly read-only Pilot fallback may read non-credential database columns and must be marked `PILOT_READONLY_FALLBACK`. Sending replies must use an upstream send API and must never forge database rows.

## Minimal operations

- `health()`
- `get_account_status()`
- `listener_status()`
- `start_listener()`
- `stop_listener()`
- `list_recent_inbound_events()`
- `send_confirmed_reply()`

## Data objects

- `UpstreamHealth`
- `UpstreamAccountStatus`
- `NormalizedInboundMessage`
- `ConfirmedReplyRequest`
- `UpstreamActionResult`

These objects must not contain Cookie, Token, Session, Authorization headers, browser Profile paths, complete decrypted payloads, unnecessary contact identity data, or complete platform credentials.

## Listener control

If no upstream listener start/stop HTTP API exists, the Wrapper may use a fixed whitelist local operator that executes only:

- `docker compose --project-name xianyu_pilot --env-file D:/xianyu-upstream-pilot/.pilot/.env.pilot -f D:/xianyu-upstream-pilot/.pilot/docker-compose.pilot.yml up -d websocket`
- `docker compose --project-name xianyu_pilot --env-file D:/xianyu-upstream-pilot/.pilot/.env.pilot -f D:/xianyu-upstream-pilot/.pilot/docker-compose.pilot.yml stop websocket`

The operator must not accept arbitrary compose paths or service names, must not use shell string concatenation, and must not operate mysql, redis, backend-web, frontend, sub2api, volumes, networks, `down`, `rm`, or `prune`.

## Safety and result semantics

Read calls may use finite retries. Write calls must not auto-retry on timeout, disconnect, or unparseable response. Write results are `SUCCESS`, `REJECTED`, `FAILED`, or `UNKNOWN`. `UNKNOWN` must not be retried automatically.

Reply idempotency must include account reference, conversation reference, inbound message reference, and reply intent. Duplicate reply attempts must be rejected before calling upstream.

## Progress

Completed tasks: 6 / 9
Next task: T7 Run complete local verification
