# XIANYU Online Chat reconnect convergence follow-up — 2026-09-19

## Incident

Account 2217936413500 (周周22) was reported as disconnected in Online Chat, with no visible Chat conversations and no new Auto Reply activity.

Read-only Runtime evidence showed:

- account login remained valid;
- Native WebSocket had disconnected at 19:14:12 because of keepalive ping timeout;
- Native WebSocket automatically reconnected at 19:14:38 and registered at 19:14:39;
- token_ready=true;
- human_qr_required=false;
- platform_verification_required=false;
- ChatNew / ImSessionManager owner was missing until the existing chat connect route was called;
- product-level image+text default-reply configuration remained present;
- no post-reconnect inbound buyer message event was recorded in the Native WebSocket logs.

## Root cause

The previous 2026-09-19 spinner convergence fix introduced a defensive auto-connect latch:

autoChatOnce

That prevented duplicate Chat connects within one page lifetime, but it also prevented recovery after a later real disconnect/reconnect cycle:

initial Chat auto-connect succeeds
→ account_id is permanently recorded in autoChatOnce
→ Native WebSocket later drops
→ Native WebSocket self-recovers
→ Chat owner is missing
→ frontend sees the account but refuses another Chat connect because the account_id is already in autoChatOnce

This explains why Native WebSocket could recover while Online Chat remained unavailable.

## Fix

The one-shot latch is replaced by a cooldown-based reconnect guard:

autoChatRetryAt

Rules:

- connected=true: never connect again;
- runtime_connected=true: never connect again;
- Native WS not connected: do nothing;
- token not ready: do nothing;
- LOGIN_REQUIRED / PLATFORM_VERIFICATION_REQUIRED / SESSION_EXPIRED: do nothing;
- Chat owner missing while Native WS is connected and token-ready: call the existing /chat-new/connect/{account_id};
- in-flight Chat connect: do not duplicate;
- failed/missing Chat owner: allow another attempt only after 15 seconds;
- background recovery is silent and does not switch the user's selected account.

No second Chat owner or Chat protocol implementation was created.

## Runtime activation

FRONTEND_IMAGE=xianyu-chg0018-frontend:chatnew-reconnect-convergence-20260919-r1

BASE_CHATNEW_SHA256=4345c358b1d7539b38ab0cff0d714b839632d248ba9bceac5f0f8b094aa303a1

FIXED_CHATNEW_SHA256=326750c9383b392e58f6f864906359d2c7b2f6377519d698adf46852ca2c1d6e

Only the Frontend container was recreated. Backend and WebSocket container IDs, StartedAt values, and restart counts remained unchanged.

## Auto Reply

Auto Reply configuration was not lost. Account 2217936413500 retained enabled product-level replies with reply_image present, reply_content present, and reply_once=false for the newly published products.

The Native WebSocket source re-enters the async message loop after reconnect. Incoming messages continue through MessageHandler and AutoReplyService. No post-reconnect inbound buyer message event was present in logs during this incident, so there was no real message event available for an end-to-end Auto Reply send assertion.

A message arriving during the real 19:14:12–19:14:39 network outage can be missed by the live receive path and therefore have no Auto Reply activity row.

## Regression

Exact locked Runtime replay: PASS.

Combined Online Chat regression suites: 30 passed.

Reconnect policy unit cases include:

- already connected -> no reconnect;
- runtime-connected -> no reconnect;
- Native WS not ready -> no reconnect;
- terminal login states -> no reconnect;
- in-flight connect -> no duplicate;
- missing Chat owner -> reconnect after cooldown;
- repeated failure within cooldown -> blocked;
- later disconnect after a previous successful connect -> reconnect allowed again;
- previous spinner convergence fix preserved;
- previous authoritative empty-conversation cache fix preserved.

## Current account recovery

2217936413500 current state after repair:

LOGIN_READY=true
ACCOUNT_ONLINE=true
Native WS connected=true
ChatNew conversations=SUCCESS
Auto Reply configuration present=true

No Backend/WebSocket restart, QR login, account disable/enable mutation, or Session refresh was performed by this repair.
