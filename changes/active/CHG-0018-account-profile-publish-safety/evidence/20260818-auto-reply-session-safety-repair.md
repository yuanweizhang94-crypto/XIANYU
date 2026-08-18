# 2026-08-18 Auto Reply Session Safety Repair

## Scope

This repair addresses the production regression observed after 2026-08-12 where accounts could still appear WebSocket-online while automatic replies stopped, and QR/login accounts could be disabled after Session expiry when no username/password credentials were configured.

No Publisher, market search, item category, delivery, customer-message sender, or Scheduler behavior was changed.

## Root cause

Production evidence showed two independent defects:

1. Session/Token maintenance classified expected `no_credentials` / `failed_session_expired` states as countable Token failures. Repeated retries could therefore reach the generic Token failure threshold and call `disable_account`, even though CHG-0018 acceptance explicitly requires missing/bad credentials to leave `XYAccount.status` unchanged.
2. Backend account capability rendering treated `websocket_connected` as sufficient proof that Auto Reply was ONLINE. Heartbeat connectivity therefore produced a false-green status even when the current Token/Session was not usable for automatic replies.

The last confirmed normal automatic reply before the incident window was on 2026-08-12. Runtime logs also showed accounts entering automatic-disable paths after Session expiry and later periods with WebSocket traffic but no business-chat processing.

## Repair

The repair keeps all existing owners and paths:

- `CookieTokenManager` remains the only Auto Reply Token/Session owner.
- `CookieManager` remains the existing WebSocket runtime-status owner.
- Backend account capabilities continue to consume the existing WebSocket status API.
- No second Token, Session, WebSocket, sender, or reply engine was created.

Changes:

- `no_credentials`, `failed_session_expired`, `human_qr_required`, and `platform_verification_required` are non-counted auth states and use conservative cooldown instead of accumulating toward automatic disable.
- Session expiry followed by `no_credentials` explicitly sets `last_token_refresh_status=no_credentials`, clears the in-memory Token, and invalidates the stale cached Token without changing account status.
- Standalone password-refresh paths no longer disable the account for missing or bad credentials; they record the failure classification only.
- WebSocket per-account runtime status now exposes sanitized `token_ready` and `token_refresh_status` fields.
- Backend Auto Reply capability queries per-account runtime status even for heartbeat-connected accounts.
- Auto Reply is `ONLINE` only when both WebSocket is connected and the current Token is ready. QR, Session-expired, platform-verification, and connected-without-Token states are exposed explicitly instead of being rendered as false-green ONLINE.

## Runtime validation

After targeted Backend and WebSocket reload on 2026-08-18:

- Backend health: HTTP 200.
- WebSocket service restarted successfully without restarting Scheduler, MySQL, Redis, or Frontend.
- All 6 currently active accounts reported:
  - task running = true
  - WebSocket connected = true
  - token_ready = true
  - no platform-verification-required flag
  - no human-QR-required flag
- All 6 active accounts re-entered `开始监听WebSocket消息` after the WebSocket restart.
- No new `Token获取连续失败...禁用账号` or `账号已自动禁用` event was present in the post-restart validation window.
- No customer message was sent as part of this repair or validation.

## Source tests

Dirty-worktree preservation validation after merging the production runtime baseline:

```text
pytest tests/test_chg0018_auto_reply_session_safety.py \
       tests/test_chg0018_transient_status_convergence.py \
       tests/test_chg0018_consumer_readiness.py \
       tests/test_chg0018_chat_platform_verification_convergence.py \
       tests/test_chg0018_chat_auth_convergence.py -q

73 passed
```

Clean reconstructed consolidation-baseline validation:

```text
pytest tests/test_chg0018_auto_reply_stability_consolidation.py \
       tests/test_chg0018_auto_reply_session_safety.py -q

47 passed
```

## Patch artifact

- Base reconstruction commit: `64c245b` (`temp: reconstruct archived CHG-0017 patch base`)
- Applied baseline first: `64c245-chg0018-auto-reply-stability-consolidation.patch`
- Incremental patch: `vendor/patches/xianyu-auto-reply/64c245-chg0018-auto-reply-session-safety-followup.patch`
- Patch size: 15514 bytes
- SHA256: `8B6BD8F8B4A6DBF44CCC03CD140FC597DD911C11CD501201C80BBE967A5E7991`
- `git diff --cached --check`: PASS
- Clean `git apply --check --whitespace=error-all --unidiff-zero`: PASS
- Clean application: PASS
- Post-apply targeted tests: 47/47 PASS

Recorded target files:

- `backend-web/app/api/routes/cookies.py`
- `tests/test_chg0018_auto_reply_session_safety.py`
- `tests/test_chg0018_auto_reply_stability_consolidation.py`
- `websocket/app/api/routes/internal.py`
- `websocket/app/services/xianyu/cookie_manager.py`
- `websocket/app/services/xianyu/cookie_token_manager.py`
- `websocket/app/services/xianyu/xianyu_async.py`

## Repository verification

Formal-root repository verification was executed after the repair.

```text
python scripts/verify_repository.py
```

The run reached the security scan and was blocked only by three sensitive-pattern findings under the pre-existing untracked `tmp/publish_restore/context/...` tree. Those files existed before this repair and were not deleted, reset, staged, or modified by this task.

A full formal-root pytest run then produced:

```text
637 passed
1 failed: tests/acceptance/test_repository_governance.py::test_security_scan_has_no_findings
failure source: pre-existing tmp/publish_restore security-scan findings only
```

The four apparent baseline failures seen when running the suite from an alternate clean worktree were re-run in the formal `D:/xianyu` root and passed 4/4; three depend on pre-existing local locked-patch updates and one asserts the canonical repository path. Project-state validation passed independently:

```text
PROJECT_STATE=PASS
```

No unrelated pre-existing dirty or temporary files were removed merely to make repository verification green.

## Safety result

```text
AUTO_REPLY_SESSION_SAFETY_REPAIR=PASS
NO_CREDENTIALS_ACCOUNT_DISABLE=false
BAD_CREDENTIALS_ACCOUNT_DISABLE=false
SESSION_EXPECTED_STATES_COUNT_TOWARD_AUTO_DISABLE=false
AUTO_REPLY_HEARTBEAT_FALSE_GREEN=false
NEW_TOKEN_OWNER_CREATED=false
NEW_SESSION_OWNER_CREATED=false
NEW_WEBSOCKET_OWNER_CREATED=false
NEW_AUTO_REPLY_ENGINE_CREATED=false
CUSTOMER_MESSAGES_SENT=0
```
