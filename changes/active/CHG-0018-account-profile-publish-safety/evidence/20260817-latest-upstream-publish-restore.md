# 2026-08-17 Latest upstream Publish restore

## Execution contract

- User outcome: restore actual latest upstream product publish as the normal production authority so `xianyu_publish_single -> Backend -> execute_single_publish -> capability detection -> direct/personal publisher -> mtop` works without the historical browser/Profile publish gate.
- Confirmed blocker: production `product_publish.py` filtered single and batch requests through `_filter_real_browser_ready_accounts()` and production publish services still routed normal publish through legacy `XianyuPublisher`/Playwright; the prior authorized Canary therefore stopped at `REAL_BROWSER_LOGIN_READY` before Publisher entry.
- Smallest success test: adopt the actual `origin/main@742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1` Publish surface, preserve strict selected-account/owner/Cookie/no-auto-retry/serial/success semantics, prove zero normal-publish browser-gate checks and zero Playwright starts in no-submit validation, deploy only Backend, then execute one actual platform-submit Canary through the formal Business Adapter to terminal SUCCESS or explicit platform FAILED.

## Authority and reuse

- Fresh remote `refs/heads/main`: `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.
- Fresh fetch advanced local upstream `origin/main` from `bf252be357f5e4261b04ce2b7419c5574aaf1b55` to `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.
- Upstream commit title: `完善商品发布`.
- Reuse decision: `ADOPT_UPSTREAM` for Publish-owned direct/personal/capability/category files; `PATCH_UPSTREAM` only for XIANYU safety/governance semantics that remain necessary and do not restore the browser owner; `WRAP_FOR_OPERATIONS` for the COMPANY_LOCAL_EXECUTION_TOOL status/serial Business Adapter.
- Duplicate-development risk: no second Publisher, Token owner, browser broker, category engine, retry engine, account fallback, queue, or table was added.
- Rollback: restore the pre-Publish-restore Backend source tar from the existing backup volume and revert only this task's Publish patch/status-adapter commits. No Cookie/Profile/account/product rollback is part of code rollback.

## Stale Browser gate evidence

Before recovery, production normal publish had:

- `backend-web/app/api/routes/product_publish.py`: `_filter_real_browser_ready_accounts()` on both single and batch publish; `REAL_BROWSER_LOGIN_READY` blocked entry to Publisher.
- `common/services/publish_execution_service.py`: normal single publish delegated to legacy `publish_single_item`.
- `backend-web/app/services/publish_execution_service.py`: batch publish created the legacy browser publisher.
- Production Canary before this recovery had already shown `REAL_BROWSER_LOGIN_READY=false`, `PUBLISH_EXECUTOR_ENTERED=false` and zero platform request.

Latest upstream has no normal single/batch `REAL_BROWSER_LOGIN_READY` gate. The latest execution owner is:

```text
execute_single_publish
-> detect_publish_account_capability
-> fish shop: XianyuDirectPublisher
-> personal seller: XianyuPersonalPublisher
-> mtop publish
-> item identity
-> Publish Log
-> authoritative item sync
```

Final invariant: `STALE_BROWSER_GATE_ACTIVE=false`, `NORMAL_PUBLISH_REQUIRES_BROWSER=false`.

## Adopted Publish dependency surface

The persistent patch records the exact `4c5e1ac5f532c7313365d70409ae115305de8a55 -> 742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1` Publish dependency delta across 19 upstream files, including the declared `opencv-python-headless>=4.10.0` dependency.

Patch:

`vendor/patches/xianyu-auto-reply/742fb58-chg0018-latest-upstream-publish-restore.patch`

Patch SHA256:

`28CEA82A473342DBE36964DB099F43CAC68A4E3748468BB42C01F585BF8E372D`

Manifest:

`vendor/patches/xianyu-auto-reply/742fb58-chg0018-latest-upstream-publish-restore.json`

The patch clean-applies with `git apply --check --whitespace=error-all` to the exact historical upstream base `4c5e1ac5...`.

## Material/schema compatibility

Latest direct/personal publishers require the current platform category contract, including `catId`, `channelCatId` and `tbCatId`. Production `xy_product_materials` was still on the older column set.

Only the upstream-owned `common/db/init_database.py` `xy_product_materials` column migration contract was used. The missing latest Material fields were added from that upstream definition; no independent schema/category system was invented. Existing data was retained.

Material `19` was then populated from current upstream platform category recommendation, not from a hardcoded virtual category. The selected platform candidate had a complete category contract and remained the formal Material used for the Canary.

## Backend deployment

A Backend-only overlay image was built from the established production Backend image with the latest Publish dependency surface and the upstream declared OpenCV dependency. All touched Python files passed `py_compile` inside the built image.

The existing Backend filesystem was backed up to the existing backup volume before overlay. The current Backend container identity, ports, network, mounts and restart policy were preserved.

Two generic compose `restart` attempts returned success without changing process `StartedAt`; they therefore were not accepted as deployment evidence. The existing COMPANY_LOCAL_EXECUTION_TOOL `restartMainBackendLifecycle` was then used. It strictly verified the allowlisted Main Backend identity, restarted exactly `xianyu_chg0017_backend_web`, observed `StartedAt` change from `2026-08-17T10:57:07.860008214Z` to `2026-08-17T15:31:49.321557077Z`, and restored Backend health to HTTP 200.

No WebSocket, Scheduler, MySQL, Redis or Frontend deployment was required.

Runtime source checks after the real process reload:

- `backend-web/app/api/routes/product_publish.py` matches latest upstream Publish route; `REAL_BROWSER_LOGIN_READY` count is zero.
- `common/services/publish_execution_service.py` matches latest capability-routed execution source.
- `XianyuDirectPublisher` and `XianyuPersonalPublisher` runtime files match latest upstream.
- Normal direct/personal publish does not start Playwright.

## No-submit validation

Fixed account: `2214313339860`.

Fixed Material: `19`.

The validation performed account lookup, authoritative owner scope, authoritative Cookie presence, Material validation, latest address resolution, capability detection, platform category recommendation and publisher-class selection without calling the final publish API.

Result:

- account lookup: PASS;
- owner scope: PASS;
- authoritative Cookie present: PASS;
- Material valid: PASS;
- address valid: PASS;
- capability detection: PASS;
- account type: personal seller (`is_fish_shop=false`);
- selected Publisher: `XianyuPersonalPublisher`;
- platform category candidates: 11;
- selected category: platform-selected complete category contract;
- `REAL_BROWSER_LOGIN_READY_CHECKS=0`;
- `PLAYWRIGHT_STARTS=0`;
- final publish API calls during no-submit validation: 0.

During native capability preget, upstream MTOP observed an expired `_m_h5_tk`, merged response Set-Cookie fields and wrote the refreshed authoritative Cookie through its existing owner. No Chat Token, Chat Connect or Chat CAPTCHA path was used.

## Canary sequencing and duplicate safety

One operation (`22f77da79d16`) was attempted while the new files were present but before the Backend Python process had actually reloaded. The old in-memory route returned the historical `REAL_BROWSER_LOGIN_READY` failure. That operation had:

- no batch id;
- `PUBLISH_EXECUTOR_ENTERED=false`;
- `GOOFISH_PUBLISH_REQUEST_SENT=false`;
- `PRODUCT_CREATED=false`.

It was never resubmitted. After the execution-tool status fix became live, the same operation correctly resolves to authoritative `FAILED` rather than `UNKNOWN`.

Because that stale-process operation never entered Publisher or sent a platform request, the later Canary below is the only actual platform-submit Canary in this recovery.

Before the actual platform Canary, the operation registry confirmed `ACTIVE_REAL_BATCH_EXECUTORS=0`.

## Real Canary result

Formal Business Adapter call only:

```text
xianyu_publish_single
-> XIANYU Backend /publish/batch
-> BATCH_SIZE=1
-> latest PublishExecutorService
-> execute_single_publish
-> detect_publish_account_capability
-> XianyuPersonalPublisher
-> platform MTOP
-> Publish Log
-> authoritative item sync
```

Canary account: `2214313339860`.

Canary operation: `726f0127565f`.

Canary batch: `6ce619b8-58b1-48fd-995a-44f2c5fd0684`.

Initial status was `SUBMITTED`. HTTP 200 / task submitted was not treated as success.

A read-only `xianyu_publish_status` follow-up returned terminal `SUCCESS` with:

- `PUBLISH_EXECUTOR_ENTERED=true`;
- `GOOFISH_PUBLISH_REQUEST_SENT=true`;
- `PUBLISH_NETWORK_REQUEST_SENT=true`;
- `PRODUCT_CREATED=true`;
- platform item id `1076024597942`;
- canonical item URL `https://www.goofish.com/item?id=1076024597942`;
- `AUTHORITATIVE_SYNC_CONFIRMED=true`;
- batch total `1`, success `1`, failed `0`, publishing `0`, pending `0`, finished `true`.

No second platform submit or second product was attempted.

Conclusion: `REAL_CANARY_SUCCESS=true`, `PUBLISH_READY=true`.

## Publish status semantics repair

The independent thin-adapter defect was owned by COMPANY_LOCAL_EXECUTION_TOOL. `xianyu_publish_status` previously downgraded a persisted `FAILED` operation with no `batch_id` to `UNKNOWN`.

The fix preserves terminal precedence:

1. strict local success evidence (`platform_item_id`, `item_url` or `AUTHORITATIVE_SYNC_CONFIRMED=true`);
2. persisted authoritative `FAILED`;
3. persisted `RUNNING` / `SUBMITTED`;
4. Backend batch/log evidence when a batch exists;
5. `UNKNOWN` only when no authoritative evidence exists.

Regression result: 4 status-specific tests passed; combined Business Adapter + status tests: 9/9 passed. Canonical proxy and runtime proxy SHA256 both equal `544f13196e2b42c47fb2392322bf4c3b3de40cc20888c6d8df4e8c4036118260`.

COMPANY_LOCAL_EXECUTION_TOOL persistence commit: `50c46238d9c06dab03c31c60164f2728e6a84202`; remote `main` equality verified.

## Regression validation

XIANYU targeted Publish authority regressions:

`20 passed`.

Full repository verification in the clean worktree, with the worktree `app` explicitly placed first on `PYTHONPATH`:

`654 passed, 1 warning`; repository verification passed.

The explicit worktree `PYTHONPATH` is required because this laptop also has the production checkout installed/importable at `D:/xianyu`; without the override, a worktree database-path test imports the production package instead of the worktree package. Three historical immutable patch hash tests also require Git blob line endings in a managed Windows worktree. Neither issue changes committed source.

Python compile for the new Publish regression test: PASS.

Frontend build: NOT_REQUIRED; no frontend source or contract was required by the formal Business Adapter Canary and no frontend source was changed in this recovery.

## Production invariants

- `LATEST_UPSTREAM_PUBLISH_IS_AUTHORITY=true`.
- `NORMAL_DIRECT_PUBLISH_REQUIRES_BROWSER=false`.
- `REAL_BROWSER_LOGIN_READY_IS_NOT_NORMAL_PUBLISH_GATE=true`.
- `OLD_BROWSER_PUBLISH_PATCH_IS_HISTORICAL_ONLY=true`.
- `PUBLISH_ACCOUNT_CAPABILITY_ROUTING_PRESERVED=true`.
- `STRICT_SELECTED_ACCOUNT=true`.
- `OWNER_SCOPE_PRESERVED=true`.
- `AUTHORITATIVE_COOKIE_ONLY=true`.
- `NO_AUTOMATIC_REAL_PUBLISH_RETRY=true`.
- `ACTIVE_REAL_BATCH_EXECUTORS_MAX=1`.
- `SUCCESS_SEMANTICS_STRICT=true`.
- Auto Reply remained six enabled accounts online during the controlled recovery checks.
- Chat files changed: 0.
- Chat Connect calls: 0.
- Chat Token calls: 0.

Status: VERIFYING / production Publish recovery proven; GitHub persistence is completed by the commit containing this evidence.
