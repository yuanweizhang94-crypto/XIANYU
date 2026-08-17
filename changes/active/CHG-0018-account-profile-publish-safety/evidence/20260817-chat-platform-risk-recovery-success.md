# 2026-08-17 Chat platform-risk recovery success

## Authority and scope

This evidence records the final successful production recovery of the upstream-native Chat path. It is a knowledge/persistence record only. It does not authorize or describe a new production deployment.

- Production runtime code base SHA: `7c4d2828f7b2c2e3f2dd6d79acfe2c9e321521ed`.
- Latest upstream authority used for Chat/QR comparison: `bf252be357f5e4261b04ce2b7419c5574aaf1b55`.
- Chat architecture: `LATEST_UPSTREAM_NATIVE`.
- QR semantics: upstream-native `QR success -> authoritative account/Cookie upsert -> Auto Reply WebSocket start/restart -> return success`.
- `QR_EAGER_CHAT_AUTH=false`.
- No production source change or deployment occurred during this final recovery canary.

No Cookie value, Token value, Authorization value, QR payload, challenge URL, customer message, password, API key, private key, or other credential is recorded here.

## Prior fresh cross-account platform evidence

Before the final recovery canary, two independent enabled accounts had already reached the latest-upstream Chat path and freshly reproduced platform validation rejection:

- `2214313339860`: expired Chat cache -> one Local Token attempt -> `FAIL_SYS_USER_VALIDATE` -> existing upstream bounded verification -> platform verification rejection.
- `2217936413500`: expired Chat cache -> one Local Token attempt -> `FAIL_SYS_USER_VALIDATE` -> existing upstream bounded verification -> platform verification rejection.

This proved the prior failure was not caused only by stale XIANYU PVR metadata on the first account. The old XIANYU PVR/readiness short-circuit had already been removed; the requests reached the real upstream Chat owner.

## Zero-auth quiet period

The last pre-recovery Chat authentication activity was observed at `2026-08-16 23:37:54 +08:00`.

The final canary Chat authentication began at approximately `2026-08-17 09:57:41 +08:00`.

Therefore the observed zero-Chat-auth quiet period before the canary was approximately `10h 19m 47s`.

During that quiet period there was no intentional Chat Connect, Local Token, CAPTCHA, Remote Token, QR scan, Cookie clear, or Profile deletion used as a recovery loop.

The quiet period itself did not prove the platform risk state had cleared. Only the single final canary below established recovery.

## Official QR canary

Target account: `2214313339860` only.

One existing upstream-native official QR login was generated and completed by the account owner.

Sanitized result:

- `QR_LOGIN_SUCCESS=true`.
- `ACCOUNT_ID_MATCH=true`.
- The authoritative account/Cookie record was updated through the existing QR owner.
- The existing Auto Reply WebSocket account task was restarted through the native QR continuation.
- `QR_EAGER_CHAT_AUTH=false`.
- QR success did not call Chat invalidation, Chat `get_or_connect`, Chat Token API, CAPTCHA, conversation list, publish preflight, or a Round2 auth-convergence loop.
- QR scans in this recovery: `1`.
- Cookie clears: `0`.
- Profile deletes: `0`.

## Final Chat lazy-connect canary

After QR success, one normal latest-upstream Chat lazy connect was executed for `2214313339860`.

Pre-connect Chat cache state: `EXPIRED`.

The real path was:

```text
user invokes Chat
-> cache-first lookup
-> expired cache
-> one Local Token owner call
-> FAIL_SYS_USER_VALIDATE
-> existing upstream bounded verification
-> first Baxia result 300
-> second bounded upstream verification attempt succeeds
-> existing upstream Token cache becomes valid
-> Token success
-> IM WebSocket connect/register success
-> conversation list success
```

Sanitized final result:

- `CHAT_CONNECT_COUNT=1`.
- `LOCAL_TOKEN_CALL_COUNT=1` at the Chat owner boundary.
- `LOCAL_TOKEN_RESULT=SUCCESS_AFTER_UPSTREAM_BOUNDED_VERIFICATION`.
- `CAPTCHA_DELEGATION_COUNT=1` at the Chat-to-existing-verification-owner boundary.
- First bounded platform verification attempt: Baxia status `300`.
- Second bounded attempt inside that same existing upstream verification operation: success.
- `CHAT_STATE=READY`.
- `CHAT_RUNTIME_CONNECTED=true`.
- `CONVERSATION_LIST_SUCCESS=true`.
- Conversation list returned successfully; no customer message contents are recorded.
- `PLATFORM_RISK_RECOVERED=true` for this canary.
- `REMOTE_TOKEN_CALLS=0`.
- Real messages sent: `0`.
- Real products published: `0`.

This successful result proves that a fresh `FAIL_SYS_USER_VALIDATE` is a platform verification/risk-control state, not evidence by itself that QR login is required. The existing upstream bounded verification path can recover without Remote Token and without creating a second Token/Session/verification owner.

## Auto Reply isolation result

After the Chat canary completed:

- `AUTO_REPLY_ONLINE_COUNT=6`.
- `AUTO_REPLY_ALL_ENABLED_ONLINE=true`.
- Chat authentication and bounded verification did not take the healthy Auto Reply fleet offline.
- No Token-refresh storm was introduced by the final canary.

Auto Reply and Chat remain independent consumers. A Chat Token/PVR failure must not destroy a healthy live Auto Reply Token or force a healthy Auto Reply WebSocket offline.

## Confirmed historical regression chain that must not return

### A. Token refresh storm

Historical production logs proved synchronized proactive maintenance generated hundreds of Token API calls per account over roughly 21 hours, approximately `325-426` requests per target account. Live WebSocket maintenance must not proactively refresh Token while an already-valid live Token is serving a connected/reconnecting Auto Reply WebSocket.

### B. QR eager Chat authentication

A XIANYU regression previously made QR success trigger Chat invalidation, Chat connect, Local Token, CAPTCHA, conversation read, publish preflight, and auth-convergence Round2. This was removed. QR success must remain upstream-native and must never eagerly authenticate Chat.

### C. Old XIANYU PVR gate

Historical Chat/PVR metadata previously short-circuited a fresh upstream Chat request. The local Chat readiness/PVR state machine was removed. Old PVR metadata must never block a new upstream-native lazy Chat request.

### D. Chat Round2 duplicate authentication

A prior QR/auth convergence path could perform another auth round after the first terminal platform-verification result. That duplicate convergence was removed and must not be restored.

### E. PVR marker cleared the live Auto Reply Token

A prior platform-verification marker could clear `current_token` even while Auto Reply WebSocket was healthy. That made a later ordinary disconnect unable to reconnect from the current Token. The live-token preservation fix is authoritative and must remain.

### F. WebSocket PID/zombie accumulation

The production WebSocket container requires an init reaper. The accepted invariant is `PID1=docker-init` with `zombies=0` under normal operation. The compose/runtime init-reaper configuration must not be removed.

## Final interpretation rules

- Normal Chat or Auto Reply WebSocket disconnect => reconnect through the existing owner; it is not QR-required evidence.
- Normal Token expiry => existing upstream Token owner handles it; expiry alone is not `HUMAN_QR_REQUIRED`.
- `FAIL_SYS_USER_VALIDATE` => platform verification/risk-control state; it must not be directly mapped to `QR_REQUIRED`.
- `HUMAN_QR_REQUIRED` is allowed only when authoritative login/session evidence proves that official login is actually required.
- Chat is lazy/cache-first. QR success does not pre-authenticate Chat.
- Healthy Auto Reply must survive Chat authentication failure.
- No second Chat state machine, Token owner, Session owner, PVR lifecycle, or verification lifecycle may be introduced.

## Related authoritative evidence

- `20260815-auto-reply-stability-consolidation.md` — Token-refresh storm root cause and live-token protections.
- `20260815-fresh-qr-chat-auth-trace-and-recovery.md` — duplicate auth/convergence findings.
- `20260816-restore-upstream-qr-login-semantics.md` — QR eager Chat convergence removal.
- `20260816-restore-latest-upstream-chat.md` — removal of old XIANYU Chat PVR/readiness state and restoration of latest-upstream Chat ownership.
- This file — final successful real canary proving Chat READY and conversation-list success.
