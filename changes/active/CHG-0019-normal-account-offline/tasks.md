# CHG-0019 Tasks

Status: VERIFYING

Change ID: CHG-0019-normal-account-offline

- [x] T1 Suspend CHG-0018 without production rollback, create CHG-0019 governance boundary, regenerate state, and validate exactly one active Change.
- [x] T2 Patch the existing normal-Web XianyuPublisher/off-shelf route with fail-closed unique-control and confirmation handling.
- [x] T3 Add and pass targeted normal-account off-shelf tests.
- [x] T4 Run `scripts/validate_change.py` and `scripts/verify_repository.py`.
- [x] T5 Build and replace only the backend component that serves `/items/batch-offline` and Playwright off-shelf.
- [x] T6 Run the owner-authorized single-item canary, perform one existing post-success item sync/read-only refresh, and stop before commit/push.

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
