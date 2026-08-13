# CHG-0018 Consumer Readiness Convergence

Date: 2026-08-13

## Execution Contract

User outcome: Account management must show Auto Reply, Browser Session, Online Chat, and Product Publish as separate states so operators do not confuse WebSocket online with Chat or Publish readiness.

Confirmed blocker: `/api/v1/cookies/details/paginated` only exposed the legacy `online` field, while `metadata_json.session_maintenance` had no consumer readiness projection. The UI collapsed multiple meanings into one online/session display.

Smallest success test: The paginated account payload contains independent readiness fields, the account table renders four separate columns, and live read-only probes update Chat readiness without sending messages or publishing items.

## Upstream And Reuse Decision

Reuse decision: `PATCH_UPSTREAM`.

Upstream evidence:
- Pinned upstream runtime baseline remains commit `64c245bc85ac56e34339fa056b0e291a16a3843b` for the local patch-check source tree.
- Newer upstream main was checked on 2026-08-13: `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`.
- Existing local upstream path owners were preserved: Account API route, Chat IM client/session manager, shared publish service, and Account table frontend.

Duplicate-development assessment:
- No new session table, service, scheduler, worker, login owner, publisher owner, or WebSocket owner was added.
- Consumer readiness is written only under existing `metadata_json.session_maintenance.consumers`.
- Existing `online` remains the auto-reply/WebSocket compatibility field.

Rollback:
- Revert runtime overlays for:
  - `/app/backend-web/app/api/routes/cookies.py`
  - `/app/backend-web/app/services/chat_new/im_client.py`
  - `/app/backend-web/app/services/chat_new/im_session_manager.py`
  - `/app/common/services/xianyu_publish_service.py`
- Restore frontend from `/tmp/html-backup-chg0018-consumer-readiness-20260813`.

## Implemented Scope

Backend:
- `/api/v1/cookies/details/paginated` now includes:
  - `auto_reply_state`
  - `browser_session_state`
  - `browser_session_updated_at`
  - `chat_state`
  - `chat_updated_at`
  - `chat_reason`
  - `publish_state`
  - `publish_updated_at`
  - `publish_reason`
- Chat conversation reads record `chat=READY` on successful read and `chat=TEMPORARY_FAILURE` on connection failure.
- QR Cookie rotation invalidates old Chat/Publish readiness by setting both consumers to `PENDING`.
- Publish preflight-only calls record `publish` readiness when invoked.

Frontend:
- Account table now renders separate columns:
  - Auto Reply
  - Browser Session
  - Online Chat
  - Product Publish

## Verification

Targeted tests:
- `python -m pytest tests\test_chg0018_consumer_readiness.py -q`
  - Result: `6 passed`
- `python -m pytest tests\test_chg0018_chat_auth_convergence.py -q`
  - Result: `3 passed`
- Combined result after metadata-string compatibility fix:
  - `python -m pytest tests\test_chg0018_consumer_readiness.py tests\test_chg0018_chat_auth_convergence.py -q`
  - Result: `9 passed`

Syntax/build:
- Runtime backend py_compile passed for patched files.
- Source py_compile passed for patched backend/common files.
- Frontend `npm run build` passed after `npm ci`.
- Built frontend account chunk: `Accounts-BTP7WR_C.js`.

Deployment:
- Backend files overlaid into `xianyu_chg0017_backend_web`.
- Frontend dist overlaid into `xianyu_chg0017_frontend`.
- Restarted backend only.
- Did not restart MySQL, Redis, Scheduler, or WebSocket.

Health:
- `http://127.0.0.1:28089/docs` returned 200.
- `http://127.0.0.1:19000/` returned 200.
- Backend `/docs` and `/openapi.json` returned 200 inside container.
- Backend logs after restart showed no `Traceback`, `SyntaxError`, `Chat readiness记录失败`, `Publish readiness记录失败`, or `consumer readiness pending record failed`.

Live sanitized projection:
- `bb45f1714e65`: Auto Reply `READY`, Browser Session `HUMAN_QR_REQUIRED`, Chat `READY` with reason `conversation_read_success`, Publish `HUMAN_QR_REQUIRED`.
- `0a0bb16c7292`: Auto Reply `READY`, Browser Session `PENDING`, Chat `TEMPORARY_FAILURE` with reason `chat_connect_failed`, Publish `PENDING`.
- `85fd9bf496fd`: Auto Reply `READY`, Browser Session `PENDING`, Chat `TEMPORARY_FAILURE` with reason `chat_connect_failed`, Publish `PENDING`.

Safety:
- Chat probes were conversation-list reads only.
- Send count during this closeout: 0.
- Publish log rows during this closeout window: 0.
- QR scans during this closeout: 0.
- Cookie/Token plaintext was not printed.

Browser DOM note:
- Browser plugin setup was attempted for `http://127.0.0.1:19000/accounts`, but the Node browser-control channel returned only execution metadata and did not return `nodeRepl.write` output. DOM assertions were therefore validated through deployed frontend assets and backend projection instead of reported browser DOM text.
