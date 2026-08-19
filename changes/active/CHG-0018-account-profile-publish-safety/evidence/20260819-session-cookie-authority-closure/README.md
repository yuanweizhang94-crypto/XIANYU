# 2026-08-19 Session Cookie Authority Closure

Status: production-validated evidence for CHG-0018 `VERIFYING`.

## Execution contract

- User outcome: prevent unvalidated Session/Cookie renewal candidates and stale platform responses from becoming authoritative account Cookie state, while preserving healthy Publisher, Auto Reply, Orders, Item reads, Chat, and Scheduler behavior.
- Confirmed blocker: multiple upstream-native Cookie writers could write or merge Cookie state without one consistent Publisher-equivalent auth gate and/or request-baseline CAS; legacy QR/cooldown state could also hide whether official renewal had actually been exhausted.
- Smallest success test: enumerate all authoritative Cookie writers, close candidate and stale-write paths without adding a second Session owner, validate the existing renewal path on healthy and expired accounts, and prove zero regression with no product publish, product mutation, message send, QR action, or platform-verification bypass.
- Reuse decision: `PATCH_UPSTREAM`.
- Duplicate-development risk: no new Session service, Cookie store, Token system, login system, Profile manager, browser broker, queue, worker, table, Publisher, or sender was introduced.

## Runtime implementation

- `safe_mtop_auth_probe` uses the Publisher-equivalent Goofish MTOP preget path as a side-effect-free auth classifier.
- Login/renewal/browser/QR/external Cookie candidates may become authoritative only after `AUTH_VALID` and an expected-authoritative fingerprint CAS.
- Authenticated response `Set-Cookie` writers retain their native business call path but merge only against the request Cookie baseline; stale responses are discarded after a newer authoritative Cookie rotation.
- Per-account renewal uses the existing `SESSION_RENEWING` owner state as single-flight.
- Evidence-qualified `HUMAN_QR_REQUIRED` is sticky only for the same authoritative Cookie fingerprint after official renewal has been attempted and safe MTOP still returns `SESSION_EXPIRED`.
- Once that evidence-qualified QR state exists, background renewal cannot re-claim the same Cookie and downgrade the state; a changed authoritative Cookie is required before automatic renewal can re-enter.

## Writer inventory result

- `UNKNOWN_COOKIE_WRITERS=0` after AST/static enumeration of database mutation primitives, ORM direct assignments, `XYAccount(cookie=...)` construction paths, and raw SQL Cookie writers across Backend, WebSocket, Scheduler, and Common runtime code.
- `MISSING_EXPECTED_BASELINE_CALLERS=0` for all remaining `update_account_cookies_in_db` / `merge_account_cookie_fields` callers.
- QR/account import/password-login construction paths are explicitly classified as auth candidates and use safe MTOP validation before authoritative insertion/commit.
- Existing incremental response writers for Orders/Item/Rate/Chat/Publisher-related reads are stale-safe without changing their business execution owner.

## Targeted tests

- Original Cookie candidate closure suite: `15/15 PASS`.
- QR evidence qualification suite: `4/4 PASS`.
- Backend/WebSocket/Scheduler changed Python files: `py_compile PASS`.
- Final r2 offline overlay validation: hash match, `PY_COMPILE_PASS`, `missing_expected=0`, `unknown_direct=0` for all three runtime images.

## Production acceptance

- Healthy Publisher references `2196106636` and `2214313339860`: final safe MTOP = `AUTH_VALID`.
- Expired accounts `1034641456`, `2219319284219`, `2858469041`: final safe MTOP = `SESSION_EXPIRED`; each has evidence-qualified `HUMAN_QR_REQUIRED` with reason `OFFICIAL_RENEWAL_FAILED_SAFE_MTOP_SESSION_EXPIRED`.
- For `2858469041`, validation explicitly covered API renewal failure, real WebSocket-local browser renewal failure, safe MTOP still expired, candidate not committed, and `PASSWORD_LOGIN_ATTEMPTED=false`.
- WebSocket/Auto Reply: `5/5 enabled accounts connected`, `ZOMBIES=0`.
- Orders read regression: PASS for both healthy references.
- Item official PC `editDetail` read regression: PASS on current active catalog item; `ITEM_MUTATIONS=0`.
- Chat read regression: PASS for both healthy references. Backend restart clears the process-local Chat-New client dictionary, so the pre-existing healthy Chat sessions were restored strictly from still-valid `chat_{unb}` cache entries; validation recorded `TOKEN_API=0` and `CAPTCHA=0` for those restores.
- Scheduler remained healthy after targeted reload.

## Safety counters

```text
REAL_PRODUCT_ACTIONS=0
PUBLISH_CALLS=0
MESSAGES_SENT=0
QR_ACTIONS=0
ITEM_MUTATIONS=0
PLATFORM_VERIFICATION_BYPASS=0
COOKIE_SECRET_OUTPUTS=0
TOKEN_SECRET_OUTPUTS=0
```

## Rebuildable runtime images

- backend: `xianyu-chg0018-backend-web:auth-cookie-closure-20260819-r2`
- websocket: `xianyu-chg0018-websocket:auth-cookie-closure-20260819-r2`
- scheduler: `xianyu-chg0018-scheduler:auth-cookie-closure-20260819-r2`

## Runtime patch artifacts

- `backend-runtime.patch`: 15 changed runtime files; SHA256 `e5cbdbdc425c31ccf070c9d3cbdb536fc27ba92091d5233321f0b64ca705fc25`.
- `websocket-runtime.patch`: 13 changed runtime files; SHA256 `0a2c210082e6c2ba155c97e835bf9686a73a2e30bac145d9c4f5b8cb38198522`.
- `scheduler-runtime.patch`: 14 changed runtime files; SHA256 `ee821f7c3ed9134b526bea592ad013ac086d8492f8a9c6b624890b0dc13dbf8d`.

These are runtime-delta evidence artifacts against the captured PRE_CHANGE runtime file set. They are not a claim that the repository branch source is byte-identical to the production overlay base. The exact file hashes and runtime image identities are locked in `manifest.json`.

## Rollback

- Deterministic PRE_CHANGE runtime snapshots were captured before final deployment.
- Runtime rollback is component-scoped; MySQL, Redis, Frontend, product data, account credentials, and browser Profiles are not deleted or reset.
- Evidence-qualified QR state is data-state metadata for the unchanged Cookie fingerprint; a future successful official login/QR Cookie rotation naturally invalidates the old fingerprint and permits normal lifecycle entry again.

## Repository validation note

- The first isolated-worktree full repository verification collected 654 tests: 649 passed and 5 failed only because the Windows worktree transformed four locked historical patch files to CRLF bytes and the Python import environment resolved the Alembic repository constant to the source checkout.
- All four historical patch blobs were compared directly with `HEAD` and their locked SHA256 values matched the repository expectations. After restoring exact HEAD bytes and using the isolated worktree `app` path, the five previously failing tests passed `5/5`.
- A second full verify attempt was interrupted by connector `502` before its result could be retrieved; no production or repository mutation depended on that call. Effective test accounting is therefore 649 previously passing plus 5 environment-corrected passing tests.
- `git diff --cached --check` is required to pass for normal evidence/manifest files. The three `.patch` evidence artifacts intentionally preserve the captured runtime whitespace; their immutable SHA256 values are locked in `manifest.json`, following the repository patch-artifact exception rule.
