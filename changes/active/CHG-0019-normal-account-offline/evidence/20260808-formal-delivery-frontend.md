# CHG-0019 Formal Delivery Frontend Verification

Date: 2026-08-08
Change: CHG-0019-normal-account-offline
Status: VERIFYING

## Delivery boundary

- BACKEND_REAL_CANARY=PASSED
- FRONTEND_LIVE_MUTATION_CANARY=NOT_REQUIRED
- NEW_REAL_PRODUCT_ACTIONS_DURING_UI_DELIVERY=0
- NEW_REAL_OFFSHELF_ACTIONS_DURING_UI_DELIVERY=0

The backend execution chain has already been proven by one controlled real canary on ACCOUNT_ID `2221384086829`, PLATFORM_ITEM_ID `1070515947040`, with explicit final platform state `已下架`. The frontend only calls the already-verified `POST /api/v1/items/batch-offline` contract. A second live mutation was intentionally not performed; frontend delivery was verified with unit/contract tests and a production read-only smoke test using intercepted synthetic data.

## Existing frontend audit

The existing product management page is `frontend/src/pages/items/Items.tsx` and the existing API wrapper is `frontend/src/api/items.ts`.

Before this delivery work:

- a checkbox-based selection model already existed;
- a batch `下架选中` entry already existed;
- `batchOfflineItems()` already called `/api/v1/items/batch-offline`;
- existing `ConfirmModal`, Toast, and `loadItems()` refresh infrastructure already existed;
- batch selection was already designed around an explicitly selected single account;
- no row-level single-item `下架` entry existed.

The existing batch/API path was reused. No second API client or alternate route was added.

## Backend contract

Current request schema is `{ cookie_id: string, item_ids: string[] }`.

Frontend consumes only `success`, `message`, and `data.results/suc_count/fail_count`. It does not consume or render `cookies_str` or credential material.

## Item status authority

`item_status` is present only in the raw platform list parser. `XYCatalogItem` does not persist/serialize it and the frontend `Item` type does not expose it. The real canary also proved local `-9` can remain unchanged after explicit platform success.

Therefore:

- `item_status == -9` is not treated as `已下架`;
- no synthetic database state was added;
- backend success is the operation evidence for the current request;
- the item list is refreshed after success;
- items that remain visible are marked `已下架` only in the current page session and cannot be submitted again;
- items that disappear from the refreshed list naturally leave the UI.

## Frontend implementation

- Added a row-level single-item `下架` action, visually distinct from `删除`.
- Single confirmation title: `确认下架商品？`.
- Single confirmation body: `确认将该商品从闲鱼下架吗？下架后不会删除商品。`.
- Confirmation button: `确认下架`; cancel performs no API call.
- Kept the existing single-account batch design and added fail-closed account consistency checks.
- Batch confirmation explicitly states the selected count and that off-shelf does not delete products.
- Empty selection cannot call the API.
- Per-item and batch in-flight locks prevent double submit.
- Single success shows `商品已成功下架` and refreshes the list.
- Batch full success shows the success count.
- Partial success shows `成功 X 个，失败 Y 个` and may include failed item IDs.
- Authentication/session failure shows `账号登录状态已失效，请先恢复登录。`.
- Verification-required failure shows a human-readable verification message.
- Internal stack traces and `cookies_str` are not rendered.
- Delete behavior was not changed.

## Frontend tests and build

`npm --prefix frontend run test:offline-ui`: 27/27 PASS, including a regression that requires the frontend container Healthcheck to use explicit IPv4 loopback `127.0.0.1`.

The tests cover the single entry, modal-before-call, cancel path, exact API path/payload, success message, refresh, per-item lock, duplicate protection, all failure, partial failure, auth failure, verification message, credential non-display, delete/offline separation, `item_status=-9` non-authority, empty batch, required account, multi-account rejection, already-offline rejection, deduplication, batch confirmation, batch lock, partial counts, and exception loading release.

`npm --prefix frontend run build`: PASS. TypeScript strict compilation and Vite production build passed.

`npm --prefix frontend run lint`: PASS. The upstream project had no ESLint configuration; a minimal configuration using already-installed parser/plugins was added without new dependencies. Existing unrelated React-Hooks dependency debt was not changed; strict type/unused checks remain enforced by the TypeScript build.

## Backend regressions after frontend work

- CHG-0019 targeted backend tests: 37/37 PASS.
- Existing publish/Profile regression tests: 19/19 PASS.
- No CHG-0019 backend business source was changed during frontend delivery.

## Frontend production deployment

Final image: `xianyu-chg0019-frontend:2b672d2-offline-ui-health`.

Only `xianyu_chg0017_frontend` was replaced. Backend, MySQL, Redis, Scheduler, and WebSocket were not restarted.

The current production Backend container had previously been manually replaced and no longer carried the Compose `backend-web` DNS alias. A new nginx process therefore cannot resolve the historical upstream name unless the frontend container receives that alias locally. The deployed frontend container uses a frontend-side Docker link alias `xianyu_chg0017_backend_web:backend-web`; Backend networking/configuration was not changed.

Post-deployment:

- Frontend `http://127.0.0.1:19000/`: HTTP 200.
- Frontend Docker Health: `healthy`.
- Backend `http://127.0.0.1:28089/health`: HTTP 200.
- Previous frontend containers are retained stopped as rollback points.

The inherited Healthcheck initially used `http://localhost:80/`; BusyBox resolved it to IPv6 `::1` while nginx listened on IPv4, producing false `unhealthy` despite HTTP 200. The formal `docker/frontend/Dockerfile` now probes `http://127.0.0.1:80/`, and the final production image reports Docker Health `healthy`.

## Production read-only smoke

The actual deployed frontend assets were opened in Playwright. All `/api/v1/**` data was intercepted with synthetic account/item data. The smoke path opened the row-level `下架` confirmation and clicked only `取消`.

Result:

- page loaded: true;
- item list loaded: true;
- single-item off-shelf entry visible: true;
- confirmation opened: true;
- confirmation text explicitly distinguishes off-shelf from delete: true;
- cancel closed the dialog: true;
- real `/items/batch-offline` forwarding: 0;
- JavaScript page errors: 0;
- console errors: 0;
- rendered sensitive token/`cookies_str` text: false.

FRONTEND_PRODUCTION_SMOKE_PASSED=true.

## Mock frontend-backend contract integration

Using the same deployed assets, Playwright intercepted `POST /api/v1/items/batch-offline` so no request reached the real Backend.

Verified scenarios:

1. Single success: exactly one mocked POST with `{cookie_id: mock-account, item_ids: [mock-item-001]}`, success UI, list refresh, session `已下架` state.
2. Batch partial failure: exactly one mocked POST with two IDs, success 1/failure 1 feedback, list refresh.
3. Auth/session failure: exactly one mocked POST, `login_required` mapped to restore-login guidance.
4. Network/server exception: exactly one intercepted failed request, generic safe error, loading lock released.

All four scenarios had zero page errors and zero real Backend forwarding.

FRONTEND_BACKEND_CONTRACT_VERIFIED=true.

## Formal delivery source artifact

Formal incremental vendor patch:
`vendor/patches/xianyu-auto-reply/4c5e1ac-chg0019-normal-account-offline-formal-delivery.patch`

SHA256: `410308F81A2484C469694E8790E9C9C689DEDAEF5C73AB0D67DD3518D557C3CF`.

Restore order is CHG-0017 patch -> CHG-0018 patch -> CHG-0019 formal-delivery patch. Clean-base apply validation passed and final Git blob equivalence matched 11/11 target files, including the formal frontend Docker health check.

## Final repository validation

- `python scripts/validate_change.py`: PASS.
- `python scripts/verify_repository.py`: 590/590 PASS using the established short Windows pytest temp path to avoid unrelated long-path copy failures.
- Final frontend tests: 27/27 PASS.
- Final production frontend image: `xianyu-chg0019-frontend:2b672d2-offline-ui-health`, HTTP 200 and Docker Health `healthy`.
- Final production read-only smoke: PASS with real off-shelf route forwarding 0.

IMPLEMENTATION_COMPLETE=true
BACKEND_REAL_CANARY_PASSED=true
FRONTEND_DELIVERY_VERIFIED=true
DELIVERY_READY=true
