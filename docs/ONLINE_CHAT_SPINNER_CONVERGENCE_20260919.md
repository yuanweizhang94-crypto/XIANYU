# XIANYU Online Chat account-status spinner convergence — 2026-09-19

## Result

ONLINE_CHAT_ACCOUNT_STATUS_SPINNER_CONVERGENCE=PASS

Production Runtime was repaired with a Frontend-only deployment. Backend, WebSocket, Scheduler, MySQL, Redis, account Session, Token, Cookie, QR/login state, and existing Chat connections were not restarted or refreshed.

## Authority at start

LOCAL_HEAD=334e1f75980e6fe72b9dca4729d12378b0669311

GITHUB_MAIN=334e1f75980e6fe72b9dca4729d12378b0669311

LOCAL_REMOTE_MATCH=true

Runtime images before this repair:

frontend = xianyu-chg0018-frontend:chatnew-account-cachefix-20260919-r1

backend = xianyu-chg0018-backend-web:desktop-recovery-20260910-r1

websocket = xianyu-chg0035-websocket:publish-session-fix-20260918-r1

scheduler = xianyu-chg0027-scheduler:desktop-recovery-20260910-r1

## Runtime baseline

Current XIANYU account-list rows: 13.

Active accounts: 10.

Native WebSocket instances: 10.

Native WebSocket connected: 9.

ChatNew / ImSessionManager connected: 9.

One active account remains legitimately LOGIN_REQUIRED / HUMAN_QR_REQUIRED.

Three account-list rows are disabled accounts.

No real account disconnect, Session refresh, QR login, Cookie refresh, account enabled-state mutation, Redis Session mutation, Backend restart, or WebSocket restart was performed by this repair.

## Live comparison proof

### Spinner account that is actually Chat-ready

ACCOUNT_ID=2221422775489

Native WebSocket:

running=true

ws_connected=true

token_ready=true

human_qr_required=false

platform_verification_required=false

ChatNew conversation read:

status=SUCCESS

Backend /chat-new/accounts response at the same production state:

connected=false

chat_state=SESSION_CHECKING

chat_reason=SESSION_CHECK_PENDING

session_state=SESSION_CHECK_PENDING

token_ready=true

connection_state=connected

runtime_connected=true

This is authoritative proof that UI_SPINNER != ACCOUNT_OFFLINE.

### Healthy connected comparison

ACCOUNT_ID=2221384086829

Native WS connected=true

Token ready=true

Chat conversations=SUCCESS

/chat-new/accounts:

connected=true

chat_state=READY

runtime_connected=true

### Real login-required comparison

ACCOUNT_ID=2221501265279

Native WS connected=false

token_ready=false

human_qr_required=true

Chat conversations=not connected

/chat-new/accounts:

connected=false

chat_state=LOGIN_REQUIRED

session_state=HUMAN_QR_REQUIRED

runtime_connected=false

The fixed UI preserves this terminal login-required state.

## Root cause

There were two independent convergence gaps in the current production Online Chat frontend.

### 1. Account list was loaded only once

The active production ChatNew bundle contained:

n.useEffect(() => { J() }, [])

for account-list startup and had no normal status polling loop.

Therefore a transient SESSION_CHECKING response could remain forever in React accounts[] even after the Backend later returned READY.

Request completion itself was not the issue: the fetch path already used try/finally. The missing behavior was post-startup status reconciliation.

### 2. Online Chat UI trusted stale Session-checking ahead of actual Chat runtime truth

Backend /chat-new/accounts can currently expose this combination:

runtime_connected=true

connected=false

chat_state=SESSION_CHECKING

when session_maintenance is still SESSION_CHECK_PENDING.

For the Online Chat page, ImSessionManager runtime connectivity is the relevant Chat authority. A connected Chat owner must not remain visually blocked by unrelated/stale Session checking unless the account has an explicit terminal login or platform-verification gate.

### 3. New QR-success accounts did not automatically enter ChatNew owner

The formal existing ChatNew owner has:

POST /api/v1/chat-new/connect/{account_id}

and ImSessionManager.get_or_connect(account_id).

A QR-success account can become Native WS connected + token_ready while runtime_connected for ChatNew is still false. Prior frontend behavior required a manual connect action.

No second Chat connection implementation was created.

## Frontend-only fix

Activated image:

xianyu-chg0018-frontend:chatnew-spinner-convergence-20260919-r1

Locked ChatNew chunk transformation:

BASE_SHA256=5a55733f22d0b18b56b1c2ffb7a02a4c55a8e3d8cfab39adb952ae1ea28bc79b

FIXED_SHA256=4345c358b1d7539b38ab0cff0d714b839632d248ba9bceac5f0f8b094aa303a1

Behavior:

1. Account status is silently re-read every 5 seconds with no overlapping polling chain.
2. The normal manual account-list request still clears its loading state in finally.
3. runtime_connected=true is normalized to connected=true / READY for Online Chat, except explicit LOGIN_REQUIRED or PLATFORM_VERIFICATION_REQUIRED.
4. Disabled account rows normalize to DISABLED / 已禁用 and never display a checking spinner.
5. Native WS connected + token_ready + Chat owner missing invokes the existing Chat connect path at most once per account per page lifecycle.
6. Already Chat-connected accounts never invoke auto-connect.
7. LOGIN_REQUIRED, PLATFORM_VERIFICATION_REQUIRED, and SESSION_EXPIRED do not auto-connect.
8. Poll failures do not convert existing terminal state into a permanent checking spinner and silent polling does not spam error toasts.
9. The 2026-09-19 authoritative empty-conversation cache fix remains present unchanged.

The fix does not modify Auto Reply, Publisher, Session, Token, Cookie, Scheduler, database, item publishing, orders, or Chat message sending.

## Regression

Deterministic regression:

21 passed

Covered:

CASE_1 connected runtime + stale checking -> UI=已连接

CASE_2 already connected + account-list refresh -> remains 已连接

CASE_3 account states remain isolated

CASE_4 conversations=[] retains the 495a203 authoritative-cache behavior

CASE_5 HUMAN_QR / LOGIN_REQUIRED -> UI=需登录

CASE_6 error/timeout terminal states -> no infinite spinner

CASE_7 already Chat-connected -> no duplicate connect

CASE_8 Native WS ready + Chat owner missing -> at most one existing Chat connect

Disabled account + SESSION_CHECKING -> UI=已禁用

Exact Runtime replay from BASE_SHA256 to FIXED_SHA256=PASS.

Node syntax check=PASS.

git diff --check=PASS before commit.

## Production activation safety

Only Frontend container was recreated.

Backend container ID and StartedAt remained unchanged.

WebSocket container ID and StartedAt remained unchanged.

Scheduler container ID and StartedAt remained unchanged.

WEBSOCKET_RESTARTED=false

BACKEND_RESTARTED=false

REAL_ACCOUNT_DISCONNECTS=0

REAL_SESSION_REFRESHES=0

REAL_QR_LOGINS=0

## Production readback

Two separated post-activation Runtime reads initially returned the same protected baseline:

account_rows=13

active_count=10

native_connected=9/10

chat_connected=9/10

login_required=1

online_account_dropped=0

chat_connection_lost=0

A later live read captured account 2221422775489 as Backend SESSION_CHECKING while runtime_connected=true and Chat conversations still succeeded. This is the direct live spinner-but-usable case.

During the same repair window, account 2221501265279 independently transitioned from HUMAN_QR_REQUIRED to Native WebSocket ready:

native_ws_connected=true

token_ready=true

human_qr_required=false

platform_verification_required=false

At that point its Chat owner was still missing and the conversation API returned not connected. Exactly one existing formal Chat connect was invoked for that account through /chat-new/connect/{account_id}. No other account received a connect call. After one normal convergence interval, its conversation API returned SUCCESS.

This is the live production CASE_8 validation:

Native WS ready + Chat owner missing

→ one existing idempotent Chat connect

→ Chat owner connected

→ conversation read SUCCESS

Final production Runtime readback:

account_rows=13

active_count=10

native_connected=10/10

chat_runtime_connected=10/10

online_account_dropped=0

chat_connection_lost=0

session_changed_by_this_fix=0

The raw Backend account response can still expose stale SESSION_CHECKING for active accounts whose current Chat owner is already connected. The final live sample included 2221501265279, 2221422775489, and 1992416548 with runtime_connected=true while chat_state=SESSION_CHECKING. That Backend inconsistency does not require a Backend restart for this UI repair.

Feeding the exact current production /chat-new/accounts response through the activated Frontend resolver gives:

UI_CONNECTED=10

UI_LOGIN_REQUIRED=0

UI_DISABLED=3

UI_SPINNER=0

No current account is an auto-connect candidate after all ten active Chat owners are connected.

## Browser verification boundary

The user's existing Chrome did not expose the authorized CDP debugging endpoint during this repair, so direct DOM/local React-memory inspection was unavailable.

An isolated headless-browser attempt was stopped because credential injection into browser localStorage was blocked by the execution safety boundary. No bypass was attempted and the temporary process was removed.

Production verification therefore uses:
- the exact Backend API response consumed by the page;
- the exact activated production ChatNew bundle;
- deterministic state-machine projection against the live 13-row response;
- two Runtime readback cycles;
- unchanged Backend/WebSocket container identity.

After a normal page refresh/re-entry, the activated bundle is the served production asset and converges current Runtime truth within one 5-second polling cycle.

## Persistence

Exact replay owner:

scripts/patch_chatnew_spinner_convergence_20260919.py

Regression:

tests/unit/test_chatnew_spinner_convergence_20260919.py

The transformer fails closed unless its input exactly matches the locked production preimage SHA and verifies the exact fixed output SHA.

No Cookie, Token, Authorization value, password, QR payload, customer identifier, or customer message is persisted in this evidence.
