Change ID: CHG-0009-xianyu-upstream-wrapper-mvp
Status: ARCHIVED
# Acceptance

## Scope gates

- CHG-0008 is merged and archived before CHG-0009 implementation begins.
- CHG-0009 starts from latest `origin/main`.
- No upstream source code is copied into `D:/xianyu`.
- Cookie, Token, Session, Authorization values, browser Profiles, administrator passwords, database passwords, and Redis passwords do not enter Git or committed docs.
- Wrapper uses localhost-only controlled interfaces by default.
- Non-loopback upstream URLs are rejected by default.
- Live writes are disabled by default and require explicit local configuration plus `--confirm`.
- Listener control can only start or stop the `xianyu_pilot` websocket service.
- No scheduler, crawler, promotion, updater, automatic reply, automatic delivery, product publishing, product delisting, order, refund, or rating operation is enabled.

## Functional gates

- Wrapper health succeeds against a healthy upstream Pilot.
- Account status maps to a non-sensitive logged-in state.
- Listener status can report running/stopped without touching unrelated services.
- The CLI can start and stop the websocket listener through the whitelist operator.
- Recent inbound events can be listed and normalized.
- Sending a reply without `--confirm` is rejected.
- Sending a reply when live writes are disabled is rejected.
- A target message must be unique before sending.
- A duplicate idempotency key is rejected.
- Timeout or ambiguous write result maps to `UNKNOWN` and is not retried.
- Explicit upstream rejection maps to `REJECTED`.
- Successful reply writes an audit record without credentials or message-body logs.

## Live supervised validation gates

- Test message `XIANYU-WRAPPER-TEST-20260729-1544-R9X6` is read exactly once by the Wrapper from `CHAT_NEW_API`.
- Reply `XIANYU-WRAPPER-ACK-20260729-1544-R9X6` is sent exactly once through `D:/xianyu` Wrapper after explicit authorization.
- Platform delivery count is one and the observed acknowledgement direction is outbound.
- Duplicate reply attempt is blocked locally before a second platform send.
- Automatic additional reply is false.
- No credential leakage occurs.
- sub2api remains unaffected.
- WebSocket listener is stopped after validation.

## Progress

Completed tasks: 9 / 9
Next task: Ready for project-owner review

## Implementation evidence

- T1 owner approval and executable scope are recorded.
- T2 pinned upstream localhost API audit is recorded in `D:/xianyu-upstream-pilot/.pilot/wrapper-api-audit.md` and summarized in this change.
- T3 Wrapper contracts, configuration, and safety boundaries are implemented with fail-closed defaults.
- T4 minimal Wrapper and CLI are implemented under `app/xianyu_system/worker/upstream_wrapper/` and `app/xianyu_system/__main__.py`.
- T5 unit coverage verifies loopback-only URLs, health, account status mapping, message normalization, listener whitelist, no-confirm rejection, live-write-disabled rejection, uniqueness, idempotency, UNKNOWN, REJECTED, and read-only fallback failures.
- T6 operator quickstart is documented in `docs/XIANYU_WRAPPER_QUICKSTART.md`.

- T8 supervised live Wrapper validation passed: listener controlled through `D:/xianyu` Wrapper, live WebSocket connectivity was confirmed, the corrected unique inbound test message matched once from `CHAT_NEW_API`, the confirmed Wrapper reply succeeded once, the duplicate attempt was rejected locally, credentials remained local, no automatic actions occurred, sub2api remained unaffected, and the listener was stopped afterward.

- T9 Draft PR administration completed: PR #10 was created, branch was pushed, GitHub Actions `quality`, `tests`, and `security` passed, the PR was transitioned to Ready for review, and CHG-0009 remains unmerged for project-owner review.
