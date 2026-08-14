# CHG-0018 Single QR Consumer Convergence + Chat Read-only Diagnostic Purity

Date: 2026-08-14

## Execution contract

User outcome: One official QR login success for one account becomes the single auth-convergence trigger for Auto Reply, Chat, and Publish. Each consumer still reports its own real state. Account-list and strict Chat diagnostics remain non-mutating.

Confirmed blocker: Existing QR success persisted the authoritative account Cookie and invoked canonical Browser Session health plus WebSocket start/restart, but it did not orchestrate existing Chat invalidation/business reconnect, Publish preflight-only, bounded second-round Cookie rotation convergence, or repeated frontend business-capability refetch.

Smallest success test: Reuse the existing account upsert, Session lifecycle, WebSocket manager, ImSessionManager, token cache, Publisher preflight-only, business-capability serializer, and account UI. Add only bounded per-account orchestration and a non-mutating diagnostic mode on the existing Chat manager; prove one natural enabled HUMAN_QR_REQUIRED account can scan once and automatically re-evaluate all three consumers with no message and no product publish.

Reuse decision: PATCH_UPSTREAM.
Duplicate-development risk: LOW. No new Session owner, Chat service, Profile store, WebSocket manager, Scheduler, worker, queue, table, or Publisher is introduced.
Rollback: remove the QR-success orchestration call, strict Chat diagnostic method, and frontend post-login refetch timer while leaving all existing auth owners unchanged.

## Starting authority

- XIANYU branch: `feat/CHG-0018-account-profile-publish-safety`
- Starting formal commit: `97c32257c5f864e418cb1a6baf24fb3c06a9f2cc`
- Vendor Patch base: `64c245bc85ac56e34339fa056b0e291a16a3843b`
- Active change: `CHG-0018-account-profile-publish-safety`
- Active change status: `VERIFYING`
- `docs/AI_PROJECT_HANDOFF.md` is not present in the current checkout; no content was inferred for it.

## Current QR success convergence gaps confirmed before repair

`CURRENT_QR_SUCCESS_CONVERGENCE_GAPS=`

1. QR success wrote the existing authoritative DB Cookie but did not invoke one unified consumer-convergence owner.
2. Existing `ImSessionManager.invalidate_auth_consumers()` was not wired into QR success.
3. Existing Chat business `get_or_connect()` was not automatically re-run after QR success.
4. Existing Publisher `preflight_only` was not automatically re-run after canonical Browser readiness.
5. A legal Chat-auth Cookie rotation did not trigger one bounded second full convergence round.
6. Same-account login convergence did not have an explicit single-flight owner.
7. Frontend QR success performed only a single account refresh rather than bounded capability refetches.
8. `get_or_connect()` is a normal business-auth path and can legitimately refresh/persist Cookie, so it must not be used as a strict read-only health probe.

## Minimal implementation

- Added `AccountService.converge_existing_consumers_after_login()` as orchestration only.
- Per-account in-process lock enforces `MAX_AUTH_CONVERGENCE_PER_ACCOUNT=1`.
- `MAX_AUTH_CONVERGENCE_ROUNDS=2`.
- Duplicate already-converged QR callback for the same consumer-auth fingerprint returns `IDEMPOTENT_ALREADY_CONVERGED`.
- Round order reuses existing owners:
  1. authoritative DB account state already committed by existing QR upsert;
  2. existing auto-reply token-cache invalidation and existing Chat client/token invalidation, only on round 1;
  3. existing WebSocket Session `/internal/session/health` on canonical Profile;
  4. re-read the authoritative DB Cookie after Browser health because Browser health is itself an existing legitimate Cookie owner;
  5. existing WebSocket account start/restart + status using the latest authoritative Cookie;
  6. existing Chat business `get_or_connect()` + one conversation-list metadata read; no message send;
  7. if an auth-relevant Cookie field legally rotates, repeat exactly once;
  8. only after `REAL_BROWSER_LOGIN_READY`, run existing Publish `preflight_only` probe;
  9. record sanitized convergence summary and let existing business-capability serializer render the final independent states.
- Round 2 does not re-expire the just-established Auto Reply or Chat token cache. The existing WebSocket restart endpoint keeps its historical default `invalidate_token_cache=true`; only login-convergence round 2 passes `false` so the latest Cookie can be rebound without manufacturing another Token/Cookie rotation.
- Added `auth_convergence_fingerprint()` inside the existing Cookie utility. It canonicalizes field order and ignores only the runtime-proven Browser-health volatile fields `atpsida`, `sca`, and `tfstk`; these three changed on every Browser health while the Cookie key set and login state remained unchanged. Other authentication and verification Cookie changes remain part of the fingerprint.
- A third auth-relevant fingerprint change is fail-closed as `AUTH_CONVERGENCE_UNSTABLE` with no further loop.
- Disabled accounts fail closed before Auto Reply, Chat, or Publish convergence and retain all three business states as disabled.
- Existing `ImSessionManager.read_only_diagnostic()` mode reads stored Chat readiness, authoritative consumer-auth fingerprint, and existing client identity only. It does not call `get_or_connect`, mutate token cache, persist response Cookie, replace a client, or send a message.
- QR and shared-QR success both call the same orchestration owner.
- Account frontend displays “登录成功，正在恢复业务能力...” and performs bounded account refetch at 0/2/5/10 seconds without page reload.

## Offline verification before production

- Python compile: PASS for the final changed Backend/WebSocket Python modules.
- Focused cumulative CHG-0018 tests: `138 passed`.
- Frontend production-source build: PASS (`tsc && vite build`, 2686 modules transformed).
- Source `git diff --check`: PASS.
- New cumulative Vendor Patch file count: 33.
- Vendor Patch SHA256: `DE945281EAE91B56E74E3529B7CCA2DE0B5E4723C9D6898A67DC4BF9C7025A13`.
- Patch clean apply from exact base `64c245bc85ac56e34339fa056b0e291a16a3843b`: PASS.
- Focused tests after fresh patch apply: `138 passed`.
- `CONTENT_EQUIVALENCE_IGNORING_CRLF=PASS` for all 33 files.
- `PATCH_BYTE_EQUIVALENCE=CRLF_DIFF_ONLY` (one test file line-ending difference only).

## Safety boundary

- No product publish/relist/offline action is authorized by this repair.
- Publisher acceptance is `preflight_only` only.
- No customer or synthetic message may be sent.
- No platform verification, CAPTCHA, slider, face verification, device verification, QR requirement, or publish restriction is bypassed.
- Exactly one natural enabled account may be used for one official QR acceptance after deployment if its Browser Session is already naturally `HUMAN_QR_REQUIRED`.
- No batch QR acceptance.
- No private credentials, Cookie values, Token values, Authorization headers, QR payloads, private keys, customer messages, or browser Profile contents are recorded here.

## Production acceptance

- `SINGLE_QR_CONVERGENCE_SAMPLE=2214313339860`.
- Pre-acceptance authoritative Browser health: `HUMAN_QR_REQUIRED`, reason `LOGIN_OR_QR_UI_VISIBLE`.
- Before QR: Auto Reply `ONLINE`; Chat `RECOVERING`; Publish `CHECKING`.
- Strict read-only purity before QR:
  - account status API Cookie fingerprint unchanged;
  - account status API Chat token-cache metadata unchanged;
  - strict Chat diagnostic Cookie fingerprint unchanged;
  - strict Chat diagnostic token-cache metadata unchanged;
  - strict Chat diagnostic did not replace a client;
  - strict Chat diagnostic sent zero messages.
- Exactly one official QR scan was performed by the owner. Backend recorded official QR success at approximately 2026-08-14 13:08:09 (Asia/Shanghai/UTC+8). No second QR was requested or generated for acceptance.
- The QR success used the existing authoritative account upsert and therefore legitimately updated the account Cookie through the explicit login owner.
- Acceptance exposed one deployment-packaging omission: the first Backend overlay had not copied the already-patched `common/services/xianyu_publish_service.py`, so the newly added orchestration initially stopped on import. The same successful login event was resumed after adding that already-verified file; no second scan was needed.
- Acceptance then exposed a bounded-convergence defect: normal Chat auth and Browser health legitimately rotate Cookie fields, while round 2 was re-invalidating the same consumer caches. This manufactured repeated rotations. The final repair preserves newly established round-1 auth on round 2, adds the default-compatible WebSocket restart cache flag, re-reads DB Cookie after Browser health, and distinguishes auth-relevant rotation from the three Browser-health volatile fields.
- Runtime proof for the volatile-field classification: one Browser health kept the same 24 Cookie names and changed values only for `atpsida`, `sca`, and `tfstk`; no values were recorded in this evidence.
- Final bounded convergence result:
  - `AUTH_CONVERGENCE_TRIGGERED=true`;
  - `AUTH_CONVERGENCE_ROUNDS=2`;
  - round 1 contained one legitimate auth-relevant Cookie rotation from normal business auth;
  - round 2 had `fingerprint_changed=false`;
  - `BROWSER_SESSION_AFTER_QR=REAL_BROWSER_LOGIN_READY`;
  - Chat business auth converged to `READY`;
  - Publisher `preflight_only` executed and recorded `publish_preflight_ready`; the restriction probe state `NORMAL` means no official publish restriction signal, while the business capability is `READY`;
  - Auto Reply completed the existing asynchronous restart and final account state is `ONLINE`.
- Final account-page business capabilities from Backend authority:
  - Auto Reply: `ONLINE / 在线`;
  - Chat: `READY / 可用`;
  - Publish: `READY / 可用`.
- `COOKIE_WRITE_BY_EXPLICIT_LOGIN_FLOW=true` by the one QR login.
- `COOKIE_WRITE_BY_CHAT_BUSINESS_AUTH=true` through the existing normal Token/Cookie refresh owner.
- `COOKIE_WRITE_BY_READ_ONLY_ACCOUNT_API=false`.
- `COOKIE_WRITE_BY_STRICT_CHAT_DIAGNOSTIC=false`.
- `CHAT_SECOND_QR_REQUESTED=false`.
- Database side-effect counts since acceptance start: `xy_publish_logs=0`; `xy_auto_reply_message_logs=0`.
- `REAL_PRODUCTS_PUBLISHED=0`; `REAL_MESSAGES_SENT=0`.
- WebSocket final idle resource state: `PID1=docker-init`, `WEBSOCKET_ZOMBIES=0`, `CHROMIUM_PROCESS_COUNT_IDLE=0`, `PLAYWRIGHT_DRIVER_COUNT_IDLE=0`, `PIDS_IDLE=3`.
- WebSocket PID/zombie reaper therefore remains intact.
- Services changed/deployed for this acceptance: Backend, Frontend, and WebSocket. Scheduler, MySQL, and Redis source/runtime were not redeployed for this change; one Scheduler instance remains authoritative.
- No second Session system, Chat system, Profile system, WebSocket manager, Scheduler, Token store, Cookie store, queue, worker, table, or Publisher was created.
