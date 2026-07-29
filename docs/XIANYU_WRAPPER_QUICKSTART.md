# XIANYU Upstream Wrapper Quickstart

This guide is for the local CHG-0009 Wrapper MVP. It assumes the upstream Pilot has already been prepared at `D:/xianyu-upstream-pilot` and the dedicated test account is already logged in.

Secrets stay in the upstream Pilot. Do not copy Cookie, Token, Session, browser Profile data, database passwords, Redis passwords, or administrator passwords into this repository.

## 1. Prepare local config

Copy the example file and keep the copy untracked:

```powershell
cd D:\xianyu
New-Item -ItemType Directory -Force .local
Copy-Item docs\xianyu-upstream.env.example .local\xianyu-upstream.env
```

Default mode is read-only for writes:

```text
XIANYU_WRAPPER_MODE=pilot
XIANYU_REQUIRE_MANUAL_CONFIRMATION=true
XIANYU_ALLOW_LIVE_WRITES=false
```

The Pilot online-chat page uses backend `chat-new` APIs, not the automatic-reply log table. To let the Wrapper read and send through the same online-chat path, the operator may put the local backend API auth header into the untracked `.local\xianyu-upstream.env` file:

```text
XIANYU_UPSTREAM_AUTH_HEADER=Bearer replace-with-local-operator-provided-value
```

The Wrapper never reads browser storage and never prints this value. If this line is absent, it falls back to the older read-only automatic-reply log source.

Only for the supervised authorized test reply, edit `.local\xianyu-upstream.env` locally and set:

```text
XIANYU_ALLOW_LIVE_WRITES=true
```

Do not commit `.local\xianyu-upstream.env`.

## 2. Check upstream health

```powershell
cd D:\xianyu
python -m xianyu_system upstream doctor
python -m xianyu_system upstream account
python -m xianyu_system upstream listener status
```

## 3. Start listener

```powershell
python -m xianyu_system upstream listener start
python -m xianyu_system upstream listener status
```

The command is whitelisted to control only the `xianyu_pilot` `websocket` service. It does not operate MySQL, Redis, backend-web, frontend, sub2api, Docker volumes, or Docker networks.

## 4. View recent messages

For ordinary review, message bodies are redacted:

```powershell
python -m xianyu_system upstream messages --limit 20
```

For the CHG-0009 supervised test marker:

```powershell
python -m xianyu_system upstream messages --match-text "XIANYU-WRAPPER-TEST-001" --limit 20
```

Use the returned `internal_message_id` for the reply command.

## 5. Preview reply safety

Without `--confirm`, the Wrapper refuses to send:

```powershell
python -m xianyu_system upstream reply --message-id <internal-message-id> --text "XIANYU-WRAPPER-ACK-001"
```

With live writes disabled, it also refuses to send even with `--confirm`.

## 6. Send the one authorized test reply

Only after confirming there is exactly one target test message and `.local\xianyu-upstream.env` has `XIANYU_ALLOW_LIVE_WRITES=true`:

```powershell
python -m xianyu_system upstream reply --message-id <internal-message-id> --text "XIANYU-WRAPPER-ACK-001" --confirm
```

`UNKNOWN` means the result is ambiguous. Do not retry automatically. Inspect manually first.

## 7. Stop listener

```powershell
python -m xianyu_system upstream listener stop
python -m xianyu_system upstream listener status
```

## Common issues

- Docker not running: start Docker Desktop and rerun `doctor`.
- Backend health failed: confirm `xianyu_pilot_backend_web` is healthy on `127.0.0.1:18089`.
- Account offline: confirm the dedicated test account remains logged in through the Pilot UI.
- Listener not registered: run `listener start`, then `doctor`.
- Message not found while the Pilot UI shows it: the UI is using the `chat-new` path; add `XIANYU_UPSTREAM_AUTH_HEADER` locally so the Wrapper uses the same online-chat API.
- Duplicate reply blocked: the audit idempotency key already exists; do not resend.
- Upstream API auth failed: provide the local backend API auth header in the untracked `.local\xianyu-upstream.env`, or the Wrapper will fall back to the read-only automatic-reply log source.
- Platform risk, CAPTCHA, face verification, or slider prompt: stop immediately and do not retry.
