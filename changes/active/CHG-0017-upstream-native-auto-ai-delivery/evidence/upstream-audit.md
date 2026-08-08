Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
# Upstream Audit

## Candidate

- Repository: `zhinianboke/xianyu-auto-reply`
- Pilot path: `D:/xianyu-upstream-pilot`
- Candidate path: `D:/xianyu-upstream-delivery-chg0017`
- Prior pinned SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Latest observed upstream SHA: `4c5e1ac5f532c7313365d70409ae115305de8a55`

## Commits Since Prior Pin

- `ebd10da` upstream Token/slider related update
- `3a75ce9` upstream follow-up
- `1c1e1cb` upstream bug fix
- `62c8914` upstream bug fix
- `fbeea7a` Token API mode settings update
- `7ae9be5` Token acquisition optimization
- `4c5e1ac` validation improvement

## Native Paths

- `README.md` describes automatic reply, AI reply, online chat, multi-account management, and websocket service responsibility.
- `websocket/app/api/routes/internal.py` exposes native account lifecycle and status routes plus native `send-message`.
- `websocket/app/services/xianyu/cookie_manager.py` owns account task loading, start, stop, and connection status.
- `websocket/app/services/xianyu/auto_reply_service.py` owns keyword, AI, default reply decisioning and sends through upstream `send_msg`.
- `websocket/app/services/xianyu/ai_reply_engine.py` owns runtime AI reply generation.
- `backend-web/app/api/routes/ai.py` and `backend-web/app/services/ai_reply_service.py` own per-account AI settings.
- `common/services/im_token_api.py`, `common/services/token_api_mode.py`, and `common/services/remote_token_api.py` own IM Token acquisition modes.
- `common/models/xy_account.py`, `common/models/xy_keyword_rule.py`, `common/models/default_reply.py`, `common/models/auto_reply_message_log.py`, and `common/models/ai_chat_message.py` provide the account/rule/log tables.

## Decision

Decision: CONFIGURE_UPSTREAM

Latest upstream has the relevant native components. CHG-0017 must configure and validate them rather than duplicate them locally.

## Pending Evidence

- Pilot configuration backup metadata.
- Zero-risk baseline.
- Controlled validation evidence.
- Cleanup and quiet-period audit.

## Candidate Offline Gate

- Candidate worktree remained detached at `4c5e1ac5f532c7313365d70409ae115305de8a55`.
- Candidate worktree status was clean.
- No upstream `test_*.py` or `*_test.py` files were present.
- `git diff --check` passed.
- Python compile gate passed for `common`, `websocket`, `backend-web`, and `scheduler`.
- Runtime services started during this gate: `0`.
