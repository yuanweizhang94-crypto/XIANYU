# CHG-0026 Design

Status: ARCHIVED

Change ID: CHG-0026-qr-dual-mode-and-chat-connectivity-recovery

## Upstream capability audit

The existing upstream QR manager and AccountService remain the sole QR/account persistence owners. The existing WebSocket service remains Auto Reply connection owner. The existing `IMSessionManager` remains Online Chat owner.

## Pinned upstream evidence

`bda1a859df63fa5f24e51398fa80a23490bb6dfc`; paths listed in proposal.

## Existing local implementation search

CHG0025 recovery strictness and CHG0023 readiness contracts are retained. Current production adapters in `cookies.py` and `chat_new.py` are the only status surfaces to patch.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second QR manager, WebSocket manager, Chat session manager, readiness table, or reconnect daemon is allowed.

## Why upstream cannot satisfy the requirement

Native add-new QR lacks immutable recovery/add mode separation and cross-owner duplicate-identity fail-closed behavior; local readiness composition must also preserve newer CHG0023/25 safety contracts.

## Approved exception ADR

Not applicable.

## Component owner

Existing XIANYU QR route/AccountService, account status route, Chat route/IMSessionManager, and Frontend Accounts/Chat pages.

## Retirement plan for overlapping local code

No overlap is introduced; retire only the narrow compatibility logic when upstream supplies equivalent contracts.

## QR state machine

Server session metadata is fixed at create time:

```text
SESSION_OWNER[session_id]
SESSION_MODE[session_id] = RECOVERY_EXISTING | ADD_NEW_ACCOUNT
SESSION_TARGET_ACCOUNT[session_id] only for RECOVERY_EXISTING
QR_SESSION_MODE_IMMUTABLE=true
```

`RECOVERY_EXISTING` requires `target_account_id`, verifies owner before QR generation, validates scanned identity equals the target before any Account/Cookie/Session/WebSocket write, and never falls back or downgrades to add-new.

`ADD_NEW_ACCOUNT` requires no target. It binds the session to the authenticated XIANYU user. On success it preserves upstream same-owner semantics: scanned `unb` already owned by current user => update existing; no same-owner match => create new. If the scanned identity is already owned by a different XIANYU user, fail closed before Account/Cookie/WebSocket writes.

Status polling accepts only `session_id`; client cannot change mode/target. Expiry never regenerates automatically. Explicit refresh preserves original modal mode and target.

## Readiness precedence

Canonical blockers precede connection evidence:

```text
PLATFORM_VERIFICATION_REQUIRED
→ HUMAN_QR_REQUIRED / LOGIN_REQUIRED
→ SESSION_RENEW_FAILED / authoritative session-expired failure
→ WebSocket/Chat connection state
→ token readiness
→ healthy
```

A stale connected/token-ready WebSocket cannot make a canonical failed Session appear healthy. A Session renewal failure is not automatically converted into HUMAN_QR; only the existing authoritative owner may classify HQR.

## UI actions

Accounts top card restores `添加账号 -> 扫码登录` using `ADD_NEW_ACCOUNT`. Existing account rows show `扫码恢复` only for authoritative auth recovery. Connection-down but auth-valid state is shown as reconnect/connecting, not scan. Platform verification is displayed as its own blocker.

Online Chat account list receives authoritative `chat_state/chat_reason` from the existing Backend status composition. It may call the existing Chat connect owner only on explicit user reconnect/select when the authoritative auth state permits connection. It never creates QR.

## Production safety

No real QR create/scan is part of implementation or acceptance. No targeted account reconnect, password login, Session repair, Cookie refresh, Token API call, or Item Sync is allowed to make acceptance green. Wang and Zhou are judged from fresh canonical Session truth; when auth-valid, only the existing startup cached-token-only Chat lifecycle may rehydrate them. A real explicit platform challenge remains blocking. Background Scheduler/Session-owner activity is attributed separately from Chat lifecycle writes.

## Final startup convergence contract

`SESSION_CHECK_PENDING` is transitional authoritative truth and can never be overwritten by `WS_CONNECTED + TOKEN_READY` into ONLINE. Backend startup takes an initial canonical snapshot, waits a bounded read-only convergence window for pending accounts, and then performs at most one existing-owner runtime-only Chat attempt only for auth-valid accounts. HQR, PVR, fatal/expired Session, or still-unsettled accounts remain non-green without auth mutation.

R5 does not persist Chat runtime; it proves `CHAT_RUNTIME_PERSISTED=false` and `CHAT_RUNTIME_SELF_REHYDRATING=true`.
