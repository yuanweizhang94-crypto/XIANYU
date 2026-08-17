# XIANYU AI Project Handoff

Authority date: 2026-08-17 (Asia/Taipei / UTC+8)

This is the current authoritative AI/developer handoff for XIANYU runtime semantics that were proven during the Chat/QR/Token recovery. It supersedes older Chat/PVR/QR-convergence conclusions when they conflict with this file. It does **not** override the active Change acceptance boundary for unrelated publish/account work.

Never record or expose Cookie values, Token values, Authorization headers, passwords, API keys, private keys, QR payloads, raw challenge URLs, browser Profile contents, or real customer messages.

## Current authority

- `UPSTREAM_FIRST=true`.
- `PRODUCTION_RUNTIME_CODE_BASE_SHA=7c4d2828f7b2c2e3f2dd6d79acfe2c9e321521ed`.
- `LATEST_UPSTREAM_MAIN_SHA=742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.
- `CURRENT_CHAT_UPSTREAM_AUTHORITY_SHA=bf252be357f5e4261b04ce2b7419c5574aaf1b55`.
- `CURRENT_PUBLISH_UPSTREAM_AUTHORITY_SHA=742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.
- `CURRENT_CHAT_ARCHITECTURE=LATEST_UPSTREAM_NATIVE`.
- `CURRENT_CHAT_RECOVERY_STATUS=PROVEN_READY_ON_REAL_CANARY`.
- `QR_EAGER_CHAT_AUTH=false`.
- `AUTO_REPLY_AND_CHAT_INDEPENDENT=true`.
- `REMOTE_TOKEN_REQUIRED=false`.
- `PLATFORM_VERIFICATION_CAN_RECOVER_THROUGH_UPSTREAM_BOUNDED_PATH=true`.
- The repository SHA may advance for documentation/tests without changing the deployed production runtime. Never infer deployment from repository HEAD alone.

Authoritative final recovery evidence:

`changes/active/CHG-0018-account-profile-publish-safety/evidence/20260817-chat-platform-risk-recovery-success.md`

## Formal architecture rules

### 1. Upstream owns Chat / QR / Token / CAPTCHA semantics

Chat, QR login, Token acquisition and platform verification must remain latest-upstream-native unless a specifically proven defect requires the smallest auditable patch.

XIANYU must not introduce a second:

- Chat state machine;
- Token owner;
- Session owner;
- PVR lifecycle;
- verification lifecycle;
- QR convergence engine.

Use the decision order from `AGENTS.md`: `ADOPT_UPSTREAM -> CONFIGURE_UPSTREAM -> PATCH_UPSTREAM -> WRAP_FOR_OPERATIONS -> BUILD_LOCAL_EXCEPTION`.

### 2. Official QR login semantics

The authoritative QR success path is:

```text
QR SUCCESS
-> upsert authoritative account/Cookie
-> WebSocket Auto Reply start/restart
-> RETURN SUCCESS
```

The following sequence is forbidden after QR success:

```text
QR
-> Chat invalidation
-> Chat get_or_connect
-> Local Token
-> CAPTCHA
-> conversation list
-> Publish preflight
-> Round2 auth convergence
```

Permanent invariant: `QR_EAGER_CHAT_AUTH=false`.

QR is a login operation. It must not become a hidden pre-authentication operation for every downstream consumer.

### 3. Chat semantics are lazy and cache-first

The authoritative Chat path is:

```text
user actually opens/invokes Chat
-> cache-first
-> valid cache: reuse Token/device context
-> cache miss/expired: existing upstream get_or_connect
-> existing upstream Local Token owner if required
-> existing upstream bounded verification if required
-> IM connect/register
-> conversation list
```

Do not pre-connect all Chat accounts from QR, account-list rendering, background health checks, or stale readiness metadata.

### 4. Ordinary Chat/WebSocket disconnect means reconnect, not QR

A normal IM or Auto Reply WebSocket disconnect is a connection lifecycle event. The existing reconnect owner handles it.

Do not automatically escalate an ordinary disconnect to `QR_REQUIRED` or `HUMAN_QR_REQUIRED`.

### 5. Normal Token expiry remains a Token-owner responsibility

Normal Token expiry/cache expiry must be handled by the existing upstream Token owner.

Token expiry alone must not automatically become `HUMAN_QR_REQUIRED`.

### 6. QR is allowed only for authoritative login/session failure

`HUMAN_QR_REQUIRED` is valid only when authoritative login/session evidence proves that official login is genuinely required, for example explicit login/QR UI or another authoritative session failure owned by the existing Session lifecycle.

Cookie age, cache expiry, an ordinary disconnect, a stale PVR marker, or a generic Token risk response is not sufficient QR evidence by itself.

### 7. `FAIL_SYS_USER_VALIDATE` is platform verification, not QR-required evidence

`FAIL_SYS_USER_VALIDATE` means the current platform Token request requires risk/platform verification.

It must **not** be directly mapped to:

- `QR_REQUIRED`;
- `HUMAN_QR_REQUIRED`;
- automatic account re-login.

The final real canary proved the upstream-native bounded verification path can recover from `FAIL_SYS_USER_VALIDATE` to Token success and Chat READY without Remote Token.

### 8. Auto Reply and Chat are independent consumers

A Chat Token failure or Chat PVR event must not destroy a healthy Auto Reply Token or force an already healthy Auto Reply WebSocket offline.

The live Auto Reply reconnect protection is authoritative: if a live Token is currently serving a connected WebSocket, marking platform verification must not clear that Token merely because another consumer failed authentication.

## Proven historical regressions — do not reintroduce

### A. Token refresh storm

Historical persistent production logs proved proactive maintenance generated approximately `325-426` Token API requests per target account over roughly 21 hours, with synchronized cross-account bursts.

The forbidden behavior is live WebSocket maintenance repeatedly calling the Token owner while an already-valid live Token is serving the connection.

Permanent rule: live WebSocket maintenance must not create proactive Token-refresh storms.

### B. QR eager Chat auth

A XIANYU regression previously changed QR success into a downstream auth fan-out: Chat invalidation, Chat connect, Local Token, CAPTCHA, conversation list, publish preflight and Round2 convergence.

That behavior was removed in `20260816-restore-upstream-qr-login-semantics.md` and must never return.

### C. Old XIANYU PVR gate

Old `session_maintenance.consumers.chat` / Chat readiness metadata could short-circuit a fresh upstream Chat request before `get_or_connect()` ran.

The XIANYU Chat readiness/PVR state machine was removed. Live latest-upstream Chat runtime is authoritative.

### D. Chat Round2 duplicate auth

The prior convergence path could perform another auth generation after a terminal platform-verification result. That duplicate Round2 behavior was removed.

A normal Chat call must have one upstream owner and bounded upstream retry semantics only.

### E. PVR marker clearing live Auto Reply Token

A previous PVR marker path cleared `current_token` while Auto Reply was still healthy. A later ordinary disconnect then could not reconnect directly and fell into full authentication/PVR.

The live-token preservation repair must remain.

### F. WebSocket PID/zombie accumulation

Production requires an init reaper for the WebSocket container.

Accepted invariant:

- `PID1=docker-init`;
- `zombies=0` under normal steady operation.

Do not remove the compose/runtime init reaper configuration.

## Final successful recovery fact

Target account: `2214313339860`.

Before the success canary, both `2214313339860` and `2217936413500` had independently reached latest-upstream Chat and freshly reproduced `FAIL_SYS_USER_VALIDATE` followed by platform-verification rejection. This established a cross-account platform result, not an old-PVR-only artifact.

After approximately `10h 19m 47s` with zero intentional Chat-auth activity:

1. one upstream-native official QR login succeeded for `2214313339860`;
2. account identity matched;
3. QR success updated the authoritative account/Cookie and restarted Auto Reply only;
4. QR did not eagerly authenticate Chat;
5. Chat cache was expired;
6. one Chat Connect was executed;
7. one Local Token owner call encountered `FAIL_SYS_USER_VALIDATE`;
8. the existing upstream bounded verification operation received Baxia `300` on its first internal attempt;
9. the second bounded attempt succeeded;
10. the existing upstream Token path became successful;
11. Chat reached READY and runtime connected;
12. conversation list succeeded;
13. Auto Reply remained `6/6 ONLINE`;
14. Remote Token calls were `0`;
15. Cookie clears were `0`;
16. Profile deletes were `0`;
17. real messages sent were `0`;
18. real products published were `0`.

Interpretation: platform verification had recovered for that canary. This is proof that `FAIL_SYS_USER_VALIDATE` can recover through the existing upstream bounded path and must not be converted to QR-required merely because the first Token request is challenged.

## Regression invariants

`REGRESSION_INVARIANT_01`
QR success must never eagerly authenticate Chat.

`REGRESSION_INVARIANT_02`
`FAIL_SYS_USER_VALIDATE` must never automatically become `QR_REQUIRED` or `HUMAN_QR_REQUIRED`.

`REGRESSION_INVARIANT_03`
Healthy Auto Reply must survive Chat authentication failure.

`REGRESSION_INVARIANT_04`
Live WebSocket maintenance must not cause a Token-refresh storm.

`REGRESSION_INVARIANT_05`
Chat uses upstream-native cache-first lazy connect.

`REGRESSION_INVARIANT_06`
Old XIANYU PVR metadata must never short-circuit a fresh upstream Chat request.

`REGRESSION_INVARIANT_07`
Only authoritative login/session failure may require QR.

`REGRESSION_INVARIANT_08`
No second Chat/Token/Session/PVR/verification owner may be introduced.

## Required regression coverage

The repository must permanently retain coverage for these behaviors:

- `TEST_QR_SUCCESS_DOES_NOT_CONNECT_CHAT`
- `TEST_QR_SUCCESS_DOES_NOT_CALL_TOKEN`
- `TEST_QR_SUCCESS_DOES_NOT_CALL_CAPTCHA`
- `TEST_QR_SUCCESS_DOES_NOT_RUN_PUBLISH_PREFLIGHT`
- `TEST_CHAT_CACHE_FIRST`
- `TEST_CHAT_CACHE_MISS_USES_UPSTREAM_TOKEN_OWNER`
- `TEST_FAIL_SYS_USER_VALIDATE_IS_NOT_QR_REQUIRED`
- `TEST_NORMAL_WS_DISCONNECT_DOES_NOT_REQUIRE_QR`
- `TEST_CHAT_PVR_DOES_NOT_DROP_HEALTHY_AUTO_REPLY`
- `TEST_LIVE_WS_MAINTENANCE_DOES_NOT_REFRESH_TOKEN`
- `TEST_CHAT_CONNECT_SINGLE_FLIGHT`
- `TEST_QR_NO_ROUND2_AUTH_CONVERGENCE`
- `TEST_DISABLED_ACCOUNT_ISOLATION`
- `TEST_WEBSOCKET_INIT_REAPER_CONFIGURATION`

These tests are regression guards. They must not be satisfied by reintroducing the removed XIANYU Chat/PVR/convergence state machine.

## Recovery decision guide for future operators

Use this order when Chat is not READY:

```text
1. Is Auto Reply healthy?
   -> preserve it; do not clear its live Token.

2. Is Chat already connected?
   -> reuse it.

3. User actually invokes Chat?
   -> cache-first lazy connect.

4. Cache expired/missing?
   -> let the existing upstream Token owner run.

5. FAIL_SYS_USER_VALIDATE?
   -> platform verification state; allow only existing bounded upstream behavior.
   -> do not label QR_REQUIRED from this fact alone.

6. Ordinary WS disconnect?
   -> reconnect; do not QR.

7. Only authoritative Session/Login failure?
   -> HUMAN_QR_REQUIRED is allowed.

8. QR success?
   -> upsert account/Cookie + Auto Reply start/restart + return success.
   -> Chat remains lazy until the user invokes it.
```

## Git/runtime identity rule

Two SHAs must always be distinguished:

- `PRODUCTION_RUNTIME_CODE_BASE_SHA`: the code actually deployed in production.
- `LATEST_REPOSITORY_DOCUMENTATION_SHA`: the Git commit containing the latest docs/tests/evidence.

A documentation/test commit must **not** be described as a production deployment. Until explicit deployment evidence says otherwise, the successful production runtime code base remains:

`7c4d2828f7b2c2e3f2dd6d79acfe2c9e321521ed`.

The latest repository documentation SHA is resolved from the current Git commit after the documentation/test commit is pushed and remote-SHA equality is verified.

## References

- `AGENTS.md`
- `docs/UPSTREAM_FIRST_POLICY.md`
- `changes/active/CHG-0018-account-profile-publish-safety/runtime_authority.json`
- `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260815-auto-reply-stability-consolidation.md`
- `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260815-fresh-qr-chat-auth-trace-and-recovery.md`
- `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260816-restore-upstream-qr-login-semantics.md`
- `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260816-restore-latest-upstream-chat.md`
- `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260817-chat-platform-risk-recovery-success.md`

## Publish authority update — 2026-08-17

The normal product-publish authority is now current upstream `origin/main@742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1` (`完善商品发布`).

Permanent Publish invariants:

- `LATEST_UPSTREAM_PUBLISH_IS_AUTHORITY=true`.
- `NORMAL_DIRECT_PUBLISH_REQUIRES_BROWSER=false`.
- `REAL_BROWSER_LOGIN_READY_IS_NOT_NORMAL_PUBLISH_GATE=true`.
- `OLD_BROWSER_PUBLISH_PATCH_IS_HISTORICAL_ONLY=true`.
- `PUBLISH_ACCOUNT_CAPABILITY_ROUTING_PRESERVED=true`.
- Normal single/batch publish must route `execute_single_publish -> detect_publish_account_capability -> XianyuDirectPublisher (fish shop) / XianyuPersonalPublisher (personal seller) -> mtop`.
- `XianyuPublisher`/Playwright may remain for legacy or other call sites, but it is not the owner of normal single/batch product publishing.
- `FAIL_SYS_USER_VALIDATE`, `RGV587`, punish/captcha/session errors from the publish MTOP owner are platform publish errors; they must not be converted to `REAL_BROWSER_LOGIN_READY=false`.
- Selected-account scope, owner scope, authoritative DB Cookie, serial real publishing, no automatic real-publish retry, duplicate safety, and strict SUCCESS evidence remain mandatory.
- `HTTP 200 / task submitted` is `SUBMITTED`, never `SUCCESS`. SUCCESS requires `platform_item_id`, `item_url`, or `AUTHORITATIVE_SYNC_CONFIRMED=true`.

Production recovery evidence: `changes/active/CHG-0018-account-profile-publish-safety/evidence/20260817-latest-upstream-publish-restore.md`.

The successful real Canary used account `2214313339860` and latest upstream personal-seller routing. It entered the latest upstream Publisher, issued one real platform publish request, returned a real item identity, and completed authoritative item sync while all six enabled Auto Reply accounts remained online.
