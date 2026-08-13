# CHG-0018 Chat Auth Convergence Evidence

Date: 2026-08-13

## Contract

User outcome: after one successful QR login, Chat New must not reuse a stale in-memory IM client or stale `chat_{unb}` Token cache while the authoritative DB Cookie has rotated.

Confirmed blocker: production Backend already runs the QR-to-canonical-Profile Session lifecycle hook, but `ImSessionManager.get_or_connect()` still returned any connected `GoofishImClient` without comparing it to the latest authoritative DB Cookie. A QR Cookie rotation could therefore leave Chat New using an old `cookies_str`, old parsed Cookie map, old Token, and old device context.

Smallest success test: record a one-way Cookie fingerprint on Chat client creation; on `get_or_connect()`, reread the DB Cookie and reuse only if the fingerprint matches; after QR success, disconnect/remove any old Chat client and mark the existing `chat_{unb}` Token cache expired without deleting rows.

## Implementation

Reuse decision: `PATCH_UPSTREAM`.

Changed existing owners only:

- `backend-web/app/services/chat_new/im_session_manager.py`
- `backend-web/app/services/chat_new/im_client.py`
- `backend-web/app/api/routes/qr_login.py`
- `backend-web/app/api/routes/shared_scan.py`
- `common/utils/cookie_refresh.py`
- `tests/test_chg0018_chat_auth_convergence.py`

The patch adds no service, queue, database table, schema field, second Token cache, second Chat client stack, second QR flow, second Browser Profile, Publisher rewrite, or message send path.

## Verification

- Upstream current remote main confirmed as `c5d969fbd3a4d52c6c8c86fd55058e9d4add8f72`.
- Runtime Backend image before this patch still contained `if client.is_connected: return client` in `backend-web/app/services/chat_new/im_session_manager.py`.
- Focused tests in `D:\xianyu-chg0018-t12-patchcheck`: `python -m pytest tests/test_chg0017_publish_login_submit.py tests/test_chg0018_chat_auth_convergence.py -q` -> `15 passed`.
- Syntax check in `D:\xianyu-chg0018-t12-patchcheck`: `python -m py_compile backend-web/app/services/chat_new/im_session_manager.py backend-web/app/services/chat_new/im_client.py backend-web/app/api/routes/qr_login.py backend-web/app/api/routes/shared_scan.py common/utils/cookie_refresh.py` -> passed.
- Incremental vendor patch reverse-check in `D:\xianyu-chg0018-t12-patchcheck`: `git apply --reverse --check D:\xianyu\vendor\patches\xianyu-auto-reply\64c245-chg0018-chat-auth-convergence.patch` -> passed.
- Incremental vendor patch parse in `D:\xianyu`: `git apply --numstat --unidiff-zero vendor\patches\xianyu-auto-reply\64c245-chg0018-chat-auth-convergence.patch` -> passed.
- Governance acceptance in `D:\xianyu`: `python -m pytest changes\active\CHG-0018-account-profile-publish-safety\tests\test_acceptance.py -q` -> `8 passed`.
- Repository verification in `D:\xianyu`: `python scripts\verify_repository.py` -> `595 passed, 1 warning`; repository verification passed.
- Production Backend overlay deployed to existing image `xianyu-chg0018-backend-web:account-session-ui-20260813`; the image already contained the CHG-0018 `cookie_fingerprint()` helper, so the final runtime overlay changed only Chat client/session manager and QR success hooks.
- Runtime compile in `xianyu_chg0017_backend_web`: patched Chat manager, Chat client, QR route, shared-QR route, and existing `cookie_refresh.py` all passed `python -m py_compile`.
- Runtime marker check confirmed `auth_fingerprint`, `invalidate_auth_consumers`, and `cookie_fingerprint` are present in the deployed Backend container.
- Host health checks after overlay: Frontend `http://127.0.0.1:19000` -> `200`; Backend `http://127.0.0.1:28089/health` -> `200`; WebSocket `http://127.0.0.1:28090/health` -> `200`; Scheduler `http://127.0.0.1:28091/health` -> `200`.
- Runtime backup exists at `/app/backups/chg0018-chat-auth-convergence-20260813` inside `xianyu_chg0017_backend_web` for the five touched Backend-runtime files.

Patch artifact: `vendor/patches/xianyu-auto-reply/64c245-chg0018-chat-auth-convergence.patch`

Patch SHA256: `A83B43731408497BCC697B4D5F010C8BC7936057043D18F05A69D43619D2B2A8`

Patch base SHA: `64c245bc85ac56e34339fa056b0e291a16a3843b`.

Patch target SHA: local incremental diff only; no upstream target commit was created in `D:\xianyu-chg0018-t12-patchcheck`.

Patch clean apply checks:

- `git -C D:\xianyu-chg0018-t12-patchcheck apply --reverse --check D:\xianyu\vendor\patches\xianyu-auto-reply\64c245-chg0018-chat-auth-convergence.patch` -> passed.
- `git apply --numstat --unidiff-zero vendor\patches\xianyu-auto-reply\64c245-chg0018-chat-auth-convergence.patch` -> parsed cleanly from the governance repo.
- `PATCH_BYTE_EQUIVALENCE=true`; the vendor patch bytes match `git -C D:\xianyu-chg0018-t12-patchcheck diff --binary -- ...` for the six intended upstream files.

## Safety

No Cookie or Token value was printed in the evidence. The implementation logs only invalidation booleans and one-way fingerprints. Real messages sent: `0`. Real products published: `0`. QR scans performed by this validation: `0`.

## Live Auth Acceptance

Runtime baseline used an existing active account that already passed the authoritative Session lifecycle. No new QR scan was requested because the selected account returned `REAL_BROWSER_LOGIN_READY` through the existing WebSocket `/internal/session/health` path with `allow_renew=false`.

Selected account evidence is masked:

- Account id SHA256 prefix: `85fd9bf496fd`.
- DB Cookie present: `true`.
- DB Cookie fingerprint prefix before/after lifecycle health: matched.
- Canonical Profile template: `/app/browser_data/user_<account_id>`.
- Profile directory exists: `true`.
- Profile `Default` directory exists: `true`.
- Authoritative browser health: `REAL_BROWSER_LOGIN_READY=true`, `HUMAN_QR_REQUIRED=false`, `PLATFORM_VERIFICATION_REQUIRED=false`.
- `PROFILE_DB_COOKIE_CONVERGED=true`.

Read-only Chat acceptance on the same account:

- Existing path used: `ImSessionManager.get_or_connect()` followed by `GoofishImClient.get_conversations(limit=5)`.
- `CHAT_AUTH_READY=true`.
- `CHAT_CONNECTED=true`.
- Client auth fingerprint matched the latest DB Cookie fingerprint.
- Conversation list returned keys `hasMore`, `nextCursor`, and `userConvs`; 5 conversations were read.
- `CHAT_CONVERSATION_READ_READY=true`.
- `SECOND_QR_FOR_CHAT=0`.
- Real messages sent: `0`.

Read-only Publisher acceptance on the same account:

- Existing path used: `publish_single_item(..., account_id=<selected>, owner_id=<selected-owner>, preflight_only=True)`.
- Publisher used the canonical account Profile path through `initialize_account_profile()`.
- Browser/account lock acquired and released through the existing lock manager.
- Result: `success=true`, message `publish preflight ready`, failure reason `null`.
- `PUBLISH_AUTH_READY=true`.
- `PUBLISH_PREFLIGHT_READY=true`.
- `SECOND_QR_FOR_PUBLISH=0`.
- Real products published: `0`.
- The preflight stopped before image upload, title/description fill, category selection, and publish submit.

Unified QR gate acceptance:

- Chat disconnects, Chat Token cache miss/failure, Profile busy/missing, network errors, publish form timeout, and platform verification are not treated as `HUMAN_QR_REQUIRED` by this repair.
- Only the existing authoritative Session lifecycle is allowed to produce `HUMAN_QR_REQUIRED`.
- `AUTHORITATIVE_QR_GATE=true`.

Runtime drift check:

- Intended runtime-changed files: `backend-web/app/services/chat_new/im_session_manager.py`, `backend-web/app/services/chat_new/im_client.py`, `backend-web/app/api/routes/qr_login.py`, `backend-web/app/api/routes/shared_scan.py`.
- Runtime `common/utils/cookie_refresh.py` SHA256 matched the saved backup exactly after the corrected overlay.
- No Publisher file, Session lifecycle file, Scheduler file, Frontend file, database schema, or Browser Profile system was changed in this turn.
- `UNINTENDED_RUNTIME_DRIFT=false`.

Commit scope note:

- This evidence file and `vendor/patches/xianyu-auto-reply/64c245-chg0018-chat-auth-convergence.patch` are safe isolated artifacts for this auth convergence closure.
- `proposal.md`, `generated/PROJECT_STATE.json`, and `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch` were already dirty before this closure and are not part of this commit.
- `tasks.md` and `acceptance.md` also had pre-existing dirty governance hunks; they are intentionally left unstaged rather than mixing old governance edits into the auth convergence commit.
