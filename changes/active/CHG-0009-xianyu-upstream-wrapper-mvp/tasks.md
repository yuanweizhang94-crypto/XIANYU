Change ID: CHG-0009-xianyu-upstream-wrapper-mvp
Status: IMPLEMENTING
# Tasks

- [x] T1 Record owner approval and executable wrapper scope
- [x] T2 Audit pinned upstream localhost API surface
- [x] T3 Define Wrapper contracts, configuration, and safety boundaries
- [x] T4 Implement minimal localhost Wrapper and CLI
- [x] T5 Add unit, contract, security, and acceptance coverage
- [x] T6 Add operator quickstart documentation
- [x] T7 Run complete local verification
- [x] T8 Execute supervised real Wrapper message loop
- [ ] T9 Publish Draft PR and complete final administration

## Current progress

Completed tasks: 8 / 9
Next task: T9 Publish Draft PR and complete final administration

## T1-T6 evidence

Owner approval is recorded. The pinned upstream audit found usable localhost WebSocket internal APIs for health, connection status, account status, and send-message, plus a required `PILOT_READONLY_FALLBACK` for recent inbound messages. The Wrapper is implemented with loopback-only URL validation, fixed Docker Compose listener control, explicit `--confirm`, live-write fail-closed configuration, idempotency audit, UNKNOWN write handling without retry, and redacted CLI output. Operator quickstart is available at `docs/XIANYU_WRAPPER_QUICKSTART.md`.

## T7 evidence

Local verification passed: `python scripts/validate_change.py`, `python -m ruff check .`, `python scripts/security_scan.py`, targeted Wrapper pytest, targeted mypy, CLI help, `git diff --check`, `python scripts/verify_repository.py`, and `python -m pytest -W error`.


## T8 evidence

Live supervised validation passed through the `D:/xianyu` Wrapper. The listener was started and stopped only through the whitelisted Wrapper command for `xianyu_pilot` websocket. The listener API reported healthy and connected, the account state remained logged in, and no platform risk verification was triggered. The corrected unique inbound test message `XIANYU-WRAPPER-TEST-20260729-1544-R9X6` matched exactly once from `CHAT_NEW_API`. The authorized acknowledgement `XIANYU-WRAPPER-ACK-20260729-1544-R9X6` was sent once through the Wrapper and observed exactly once as outbound. A duplicate attempt with identical parameters was rejected locally before a second platform delivery. All credentials remained local in ignored configuration, no authentication values were printed, sub2api remained unaffected, and automated business actions remained disabled.
