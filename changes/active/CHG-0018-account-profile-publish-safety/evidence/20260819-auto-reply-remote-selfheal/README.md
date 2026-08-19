# 2026-08-19 Auto Reply remote-only self-heal

Decision: `PATCH_UPSTREAM`.

## Execution contract

- User outcome: when Auto Reply is offline but the authoritative Xianyu Session is still valid, the existing upstream remote Token interface must recover it automatically instead of leaving the account indefinitely offline in `PLATFORM_VERIFICATION_REQUIRED`.
- Confirmed blocker: the existing `CookieTokenManager.refresh_token()` returned immediately whenever `_auto_reply_platform_verification_required=true`, so a one-time local Token/CAPTCHA result could permanently suppress later remote fallback even when Publisher-equivalent safe MTOP still proved `AUTH_VALID`.
- Smallest success test: `AUTH_VALID -> low-frequency remote-only Token fallback -> cache -> clear PVR -> WebSocket reconnect`; `SESSION_EXPIRED -> no remote-only Token -> existing bounded Session renewal`; evidence-qualified `HUMAN_QR_REQUIRED -> stable QR wait with no reconnect/Token/CAPTCHA/password-login loop`.

## Implementation

Only the existing WebSocket Auto Reply owner is patched. No second Token service, Session service, Cookie owner, CAPTCHA solver, reconnect owner, API, table, worker, or scheduler is introduced.

1. `CookieTokenManager` adds a 180-second in-process gate for PVR remote recovery.
2. Before any PVR remote request, the current database Cookie is checked with Publisher-equivalent `safe_mtop_auth_probe`.
3. Only `AUTH_VALID` is allowed to call the already-existing `_try_remote_token_fallback`, which preserves its existing remote configuration, paid-fallback lock, and balance cooldown.
4. Remote response Cookies are ignored; the authoritative Cookie is never written by this recovery path.
5. On remote Token success, only the existing Token cache is updated, PVR metadata is cleared, and the same WebSocket owner reconnects normally.
6. `SESSION_EXPIRED` leaves Token-only recovery and re-enters the existing bounded Session renewal chain.
7. `UNKNOWN` fails closed and waits for the next low-frequency check.
8. Evidence-qualified `HUMAN_QR_REQUIRED` remains higher priority and never reaches the remote-only path.
9. PVR main-loop status polling is 60 seconds, while the external remote request remains gated to once per 180 seconds at most during continuous failure.

## Targeted validation

Runtime `py_compile`: PASS for `cookie_token_manager.py` and `xianyu_async.py`.

Isolated state-machine tests in the production WebSocket environment:

```text
TEST_AUTH_VALID_REMOTE_RECOVERY=PASS
TEST_REMOTE_FAILURE_RATE_LIMIT=PASS
TEST_SESSION_EXPIRED_NO_REMOTE=PASS
TEST_UNKNOWN_FAIL_CLOSED=PASS
```

Production WebSocket was reloaded only through the fixed allowlisted lifecycle command. Post-reload readback:

```text
2196106636 connected=True  token_state=success_from_cache  qr=False pvr=False reconnect=False
1034641456 connected=False token_state=human_qr_required qr=True  pvr=False reconnect=False
2219319284219 connected=False token_state=human_qr_required qr=True  pvr=False reconnect=False
2214313339860 connected=True token_state=success_from_cache
2217936413500 connected=True token_state=success_from_cache
2221501265279 connected=True token_state=success_from_cache
connection_stats total=6 connected=4
```

Healthy accounts returned from existing Token cache and normal heartbeats resumed. The two evidence-qualified QR accounts did not enter Token/CAPTCHA/password-login recovery after restart.

## Rebuildable artifact

- WebSocket image: `xianyu-chg0018-websocket:auth-cookie-closure-20260819-r3`
- Offline validation: `websocket:closure:HASH_MATCH files=18`, `PY_COMPILE_PASS`, `WRITER_INVENTORY_PASS missing_expected=0 unknown_direct=0`.
- `cookie_token_manager.py` SHA256: `2a727e3f32c8e392a5d59078f09ef75b50c2546a8065d504227aca1c9dfe32ec`
- `xianyu_async.py` SHA256: `33020bef42f85baea7d13c71b8bd0ae6f5e3fc6d4505905febc2189abd9e344c`
- Delta patch SHA256: `a4723e6596b171e3d241d060b28b805dc69a57ad2db6383516fa8a6a974457e9`

## Safety

- Authoritative Cookie writes from this new path: 0.
- QR actions: 0.
- CAPTCHA/slider actions introduced by this path: 0.
- Product publish/item mutation: 0.
- Customer messages sent: 0.
- Automatic payment: 0.
- Credentials or Token values persisted in evidence: 0.

## Repository verification note

- New targeted regression test: `4 passed`.
- Post-fix project-state/schema guard check: `2 passed`.
- Full `python scripts/verify_repository.py`: `649 passed / 14 failed / 1 warning`.
- The same 14 failures are the pre-existing latest-remote baseline: the corrupted/encoding-drifted `docs/AI_PROJECT_HANDOFF.md` regression invariant assertions, four historical locked patch byte-hash mismatches under the Windows checkout normalization, and the isolated-worktree Alembic path binding. This task does not modify those baseline files.
- No new failure remains attributable to this self-heal patch.
