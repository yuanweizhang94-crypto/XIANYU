# CHG-0019 Tasks

Status: ARCHIVED

Change ID: CHG-0019-normal-account-offline

- [x] T1 Suspend CHG-0018 without production rollback, create CHG-0019 governance boundary, regenerate state, and validate exactly one active Change.
- [x] T2 Patch the existing normal-Web XianyuPublisher/off-shelf route with fail-closed unique-control and confirmation handling.
- [x] T3 Add and pass targeted normal-account off-shelf tests.
- [x] T4 Run `scripts/validate_change.py` and `scripts/verify_repository.py`.
- [x] T5 Build and replace only the backend component that serves `/items/batch-offline` and Playwright off-shelf.
- [x] T6 Run the owner-authorized single-item canary, perform one existing post-success item sync/read-only refresh, and stop before commit/push.
- [x] T7 Reuse the existing product-management batch-offline UI/API path, add the missing single-item entry and fail-closed UI state handling, and pass 26 frontend contract tests, lint, and production build.
- [x] T8 Deploy only the formal frontend image, run production read-only smoke plus mocked frontend-backend contract scenarios, preserve the verified Backend unchanged, and record formal delivery evidence.
- [x] T9 Address PR #28 review findings by publishing the exact predecessor stack base and hardening off-shelf success classification to target-specific post-action evidence without changing the verified execution path or running a new real canary.

## T5 result

- Standard Backend image build was blocked by the configured Tsinghua pip mirror returning no FastAPI distribution; application dependencies were not changed.
- A Backend-only overlay image was built from the existing production Backend image and replaced only the three tested CHG-0019 runtime source files.
- Deployed image: `xianyu-chg0019-backend-web:44c8ae9-normal-offline`.
- Only `xianyu_chg0017_backend_web` was replaced. Scheduler, WebSocket, MySQL, Redis, and Frontend were not restarted.
- Runtime `/health` probe passed after the final replacement.

## T6 first canary attempt

- Fixed account/item preflight passed: current normal-Web Session healthy, exact item URL/title/price/account ownership matched, and exactly one safe `下架` control was found with no ambiguity.
- The single authorized canary entered the Playwright off-shelf execution path, but the route then raised a CHG-0019-local `NameError` because `suc_count`/`fail_count` were not assigned after the new normal-Web batch service returned.
- No retry was performed. A read-only post-attempt page check showed the target still has the unique `下架` and `删除` owner controls and no `上架`/`重新上架`, so explicit platform off-shelf success was not established.
- The route count defect was fixed, a regression test was added, targeted tests passed 11/11, existing publish/Profile regressions passed 19/19, and the corrected Backend image was redeployed without another product action.
- T6 remained incomplete at that point because the task permitted no second real canary attempt without fresh owner authorization.

## T6 final authorized canary result

- Final production Backend: `xianyu-chg0019-backend-web:44c8ae9-nonsemantic-confirm`.
- Read-only preflight passed for ACCOUNT_ID `2221384086829` / PLATFORM_ITEM_ID `1070515947040`: healthy Session, exact item ID/title, confirmed owner context, unique `下架`, no already-off-shelf evidence. Price `9.90` was recorded as auxiliary only.
- Exactly one `/items/batch-offline` transaction was executed. It used the normal-Web Playwright path and never called the old PC Seller batch-offline API.
- The unique `下架` control was clicked, then the local Dialog was read as `确定要下架这个宝贝吗？ 取消 确定`. The classifier resolved one safe `确定` plus one `取消`, with no dangerous semantics, and clicked the unique confirmation as part of the same authorized transaction.
- Route/UI result succeeded. Post-action read-only evidence showed the `下架` control absent and explicit `已下架` platform state. `REAL_OFFSHELF_CANARY_SUCCESS=true`.
- Exactly one existing item sync then completed successfully (`total_count=6`, `saved_count=6`). Local cached status remained `-9`; explicit platform evidence remains authoritative and no manual database/Redis status write was made.
- No other account/item product action, delete, publish, relist, edit, polish, Git commit, Git push, GitHub write, or PR #26 change occurred.
- Final evidence: `evidence/20260808-final-authorized-offline-end-to-end.md`.

## T7-T8 formal frontend delivery result

- Existing batch-offline entry and `batchOfflineItems()` API wrapper were reused; no duplicate route or API client was created.
- Added the missing row-level single-item off-shelf entry, explicit project confirmation, in-flight/double-submit protection, partial/auth failure feedback, success refresh, and page-session `已下架` protection without treating local `item_status=-9` as authority.
- Frontend tests passed 27/27, including the explicit IPv4 container-health regression; TypeScript/Vite build passed; frontend lint passed after adding the previously missing minimal ESLint configuration without new dependencies or unrelated hook refactors.
- Backend CHG-0019 targeted tests remained 37/37 PASS and publish/Profile regressions remained 19/19 PASS.
- Final formal frontend image `xianyu-chg0019-frontend:2b672d2-offline-ui-health` was deployed by replacing only the frontend container. It serves HTTP 200 and reports Docker Health `healthy`. Backend, MySQL, Redis, Scheduler, and WebSocket were not restarted.
- Production read-only smoke used the actual deployed assets with synthetic intercepted data: page/list/entry/dialog/cancel passed, JavaScript errors were zero, sensitive text was absent, and real `/items/batch-offline` forwarding was zero.
- Mocked deployed-asset contract scenarios for success, partial failure, auth failure, and network exception passed with zero real Backend forwarding.
- `BACKEND_REAL_CANARY=PASSED`; `FRONTEND_LIVE_MUTATION_CANARY=NOT_REQUIRED` because the mutation executor was already proven by the controlled real canary and this UI only calls the verified API.
- Formal delivery evidence: `evidence/20260808-formal-delivery-frontend.md`.

## T9 PR review hardening result

- Review predecessor `44c8ae98ac576f9ab486fae473d56f26480b8868` is an ancestor of formal delivery commit `0573db0581eee71620a0260f7b639cd1b69a3401`; the true pre-review CHG-0019 delta is 2 commits / 28 files.
- Review-only stack base `review-base/CHG-0019-predecessor-44c8ae9` was pushed at the exact predecessor commit; it is not a production or CHG-0018-reactivation branch.
- `_wait_for_offline_ui_success()` no longer accepts whole-page `document.body.innerText` as success evidence.
- Success now requires the exact target item URL plus either a new post-action success notice or a reverse state from the same captured owner-operation DOM location after the `下架` control disappears. Button disappearance alone is insufficient.
- Targeted Backend tests passed 47/47; publish/Profile regressions passed 19/19; Frontend tests remained 27/27 with lint/build PASS.
- Layered review-fix patch applies after the formal-delivery patch and reproduces the two hardened target files with 2/2 Git blob equivalence.
- No new real off-shelf action, product action, production deployment, container change, database/Redis write, or Xianyu login occurred.
- Review evidence: `evidence/20260808-pr28-review-success-classification-hardening.md`.

## Post-merge archive closeout

- PR #33 merged the current main-layered CHG-0019 delivery after exact-head review and CI.
- Post-merge `main` quality, tests, and security completed successfully.
- CHG-0019 is moved from `changes/active/` to `changes/archive/` and its governance status is `ARCHIVED`.
- No new real canary, product action, login, message, deployment, container change, database write, or Redis write was performed for this closeout.
