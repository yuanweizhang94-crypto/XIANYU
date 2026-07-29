Change ID: CHG-0010-xianyu-automatic-reply-mvp
Status: IMPLEMENTING
# Acceptance

## Scope gates

- CHG-0009 is merged and archived before CHG-0010 implementation begins.
- CHG-0010 starts from latest `origin/main` on branch `feat/CHG-0010-xianyu-automatic-reply-mvp`.
- No operator workflow requiring per-message message selection, reply typing, or SEND confirmation is implemented.
- CHG-0010 reuses CHG-0009 Wrapper boundaries and does not reimplement Xianyu login, WebSocket, message protocol, send protocol, HTTP client, message model, audit, or idempotency.
- No upstream tracked source under `D:/xianyu-upstream-pilot` is modified or copied.
- Cookie, Token, Session, Authorization values, browser Profiles, administrator passwords, database passwords, Redis passwords, full account identifiers, contact details, and real customer data do not enter Git or committed docs.
- Automatic reply is disabled by default.
- Product publishing, delisting, order, delivery, refund, rating, crawler, promotion, updater, unrelated scheduler, bargaining, refund promises, offline transaction guidance, marketing blasts, and batch messaging are not supported.

## Functional gates

- `python -m xianyu_system autoreply doctor` performs read-only configuration, Pilot, account, listener, and safety checks.
- `start` creates a controlled local background process and does not require the user to keep an interactive terminal open.
- `status` reports running state and non-sensitive counts.
- `stop` stops only the recorded autoreply worker and respects listener ownership.
- `run` supports foreground debug execution.
- Startup watermark prevents replying to historical messages.
- Deterministic rules match in order; fallback is optional and configured.
- The worker replies only when enabled config, live writes, dedicated-test mode, account allowlist, inbound text message, health, login, listener connection, and automation-off gates pass.
- Unsupported message types, outbound messages, safety text, auth failure, unhealthy upstream, account not logged in, listener disconnected, non-allowlisted accounts, rate limit, cooldown, and disabled config fail closed.
- SUCCESS, REJECTED, FAILED, UNKNOWN, and SKIPPED are represented.
- UNKNOWN is never retried automatically.
- SUCCESS and UNKNOWN idempotency records block duplicate sends across restarts.
- Conversation cooldown, per-conversation hourly limit, and per-account hourly limit exist and have finite defaults.
- Runtime state and logs do not include credentials, full message text, full reply text, full account IDs, or full upstream payloads.

## Live supervised validation gates

- Local test config under `.local` enables only the dedicated test account and exact rule for `XIANYU-AUTOREPLY-TEST-20260729-A7P3`.
- Expected automatic reply is `XIANYU-AUTOREPLY-ACK-20260729-A7P3`.
- `doctor`, `start`, and `status` pass before the owner sends the test message.
- The system reaches `WAITING_FOR_OPERATOR_SEND_AUTOREPLY_TEST_MESSAGE` before the owner sends the message.
- After the owner sends one test message, the worker automatically reads it, matches the rule, sends ACK, and records SUCCESS without per-message selection or SEND confirmation.
- Inbound match count is one, rule match count is one, platform ACK count is one, duplicate reply count is zero, extra reply count is zero, historical messages replied is zero, and other conversations affected is zero.
- The worker is stopped after validation, any listener it owns is stopped, test config is restored to disabled, and no unattended autoreply process remains.

## Progress

Completed tasks: 7 / 8
Next task: T8 Publish PR and complete final administration

- T2-T5 implementation evidence: configuration, worker, local process state, CLI, example config, quickstart, and 30 unit tests were added without upstream source changes or credential leakage.


- T6 verification evidence: complete local verification passed, including repository verification, full pytest with warnings as errors, ruff, security scan, mypy for `app/xianyu_system`, `git diff --check`, and default-disabled autoreply CLI doctor/status checks.


- T7 live validation evidence: supervised dedicated-test automatic reply passed with inbound match count = 1, rule match count = 1, automatic reply result = SUCCESS, platform ACK count = 1, duplicate reply count = 0, extra reply count = 0, historical messages replied = 0, other conversations affected = 0, no per-message manual confirmation, worker stopped, owned listener stopped, and local config restored to disabled.
