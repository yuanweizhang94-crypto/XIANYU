# CHG-0041 Design

Change ID: CHG-0041-native-chat-runtime-equivalence
Status: ARCHIVED

## State-machine conclusion

The formal enable lifecycle is already symmetric for the Native owner:

disabled
-> Account status enabled
-> Backend websocket_client.start_account
-> WebSocket CookieManager account task
-> XianyuAsync instance
-> Token ready
-> /reg matching ACK
-> message loop ready
-> Auto Reply owner ready

Production evidence for 2219319284219 completed this sequence in about two seconds.

The missing edge is:

Native owner ready
-> Backend Online Chat shared-owner RPC
-> current WebSocket image route 404

Therefore this Change must not add another enable reconciler or another Chat connection.

## Minimal behavior

Restore only the already-existing local Native Chat RPC surface onto the exact current CHG0039 production preimage:

1. Add Native Chat request models and internal routes to internal.py.
2. Resolve the existing CookieManager instance; fail closed when no Native owner exists.
3. Add bounded Chat LWP helpers to XianyuAsync using the existing connection_manager.ws and _pending_mid_futures correlation.
4. Preserve current CHG0038 registration ACK logic byte-for-byte outside the additions.
5. Preserve current CHG0039 token invalidation owner byte-for-byte.

## Runtime readiness semantics

SESSION_READY is derived from canonical Session truth.
TOKEN_READY comes from the Native WebSocket owner.
REGISTRATION_ACKED remains CHG0038 authority.
MESSAGE_LOOP_READY remains the Native owner message loop.
CHAT_READY means the Native owner RPC surface can execute on that same account connection; it is not a second Chat WebSocket owner.

HUMAN_QR_REQUIRED remains fail-closed.

## Idempotence

- Account enable continues to use existing start_account.
- CookieManager remains keyed by account_id and prevents duplicate account tasks.
- Chat RPC resolves the existing instance only.
- Repeated Chat reads create no worker and no second socket.
- Disabled accounts have no Native instance, so Chat RPC returns unavailable rather than starting one.

## Production activation

Only the WebSocket service image may change.
Backend, Frontend and Scheduler remain untouched.
The candidate image is built FROM the current production CHG0039 image and overlays only the two RPC files.

## Safety

No real send action is required for validation.
Conversation/history readback is sufficient to prove RPC availability.
No disabled account may be enabled for testing.
