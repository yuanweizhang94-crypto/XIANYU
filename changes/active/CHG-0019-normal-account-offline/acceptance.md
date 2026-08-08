# CHG-0019 Acceptance

Status: VERIFYING

Change ID: CHG-0019-normal-account-offline

## Acceptance

- CHG-0018 exists under `changes/suspended/CHG-0018-account-profile-publish-safety`, all four required files declare `SUSPENDED`, its production verification evidence remains valid, production auto-polish remains enabled/unchanged, and PR #26 remains Draft/Open/Unmerged.
- Exactly one active Change exists: `CHG-0019-normal-account-offline`.
- Root cause is fixed as `CURRENT_BACKEND_USES_WRONG_PC_SELLER_OFFSHELF_API`; this Change does not continue PC Seller COMMONPRO/member-id investigation.
- Public `POST /items/batch-offline` remains compatible.
- The default off-shelf execution uses existing XianyuPublisher/Playwright/Cookie/browser lifecycle and normal `www.goofish.com/item?id=<item_id>` detail pages.
- Old PC Seller batch-offline source is preserved and not used by the normal-account canary.
- Correct detail URL is generated from the exact platform item ID.
- Login/auth/verification state fails closed and triggers no automatic login or QR scan.
- An off-shelf action is allowed only when exactly one plausible visible enabled owner action is identified.
- Missing off-shelf control fails closed.
- Multiple plausible off-shelf controls fail closed with ambiguous-control classification.
- `删除`, `确认删除`, `永久删除`, or delete-containing owner/dialog contexts are never accepted as off-shelf actions.
- Confirmation is clicked only when the dialog is explicitly off-shelf semantics, contains no delete semantics, and has exactly one safe enabled confirmation action.
- Click completion alone never means success. Success requires target-specific post-action evidence: the exact target item URL must still match, and either a new success notice appears after the pre-action notice snapshot or the same captured owner-operation DOM location transitions from `下架` to exact visible `上架`/`重新上架`/`已下架` state.
- Whole-page `document.body.innerText` is never accepted as off-shelf success evidence. Unrelated/recommended/stale `已下架` text cannot confirm the target item, and `下架` control disappearance alone is insufficient.
- Batch processing records each item independently; one failure must not mark other items successful.
- Browser exceptions return failure, never success.
- Tests cover URL generation, unique/missing/multiple controls, delete exclusion, confirmation semantics, auth failure, success parsing, per-item batch result isolation, and browser exception handling.
- `python scripts/validate_change.py` and `python scripts/verify_repository.py` pass before production deployment.
- Deployment replaces only the backend component proven to own the route/publisher; MySQL, Redis, Scheduler, WebSocket, and Frontend are not restarted.
- Real canary is exactly ACCOUNT_ID `2221384086829`, LOCAL_ITEM_ID `49`, PLATFORM_ITEM_ID `1070515947040`; no other account/item product action is authorized.
- Before canary, session is healthy and detail page item ID/title plus owner context match the fixed target; price is auxiliary evidence and is not the sole identity gate.
- At most one real off-shelf target item is acted upon. No retry of an ambiguous/unknown real outcome is allowed.
- If UI success is explicit, one existing item synchronization/read-only refresh may run; no manual database or Redis status write is allowed.
- No product delete, publish, relist, edit, polish, Git commit, Git push, GitHub write, or PR #26 change occurs in this task.
- Explicit platform UI evidence (`已下架`, off-shelf success message, or equivalent state transition) is sufficient to establish canary success; no extra Owner App/Web confirmation is required when that evidence is clear.

## Canary success rule

`REAL_OFFSHELF_CANARY_SUCCESS=true` only when the target item matched, exactly one safe off-shelf action was used, any confirmation was explicitly safe, and the platform UI produced explicit off-shelf success/state-transition evidence. Post-sync confirmation is additional evidence and a stale local cache alone does not negate explicit platform success.

## Final canary acceptance evidence

- ACCOUNT_ID `2221384086829`, LOCAL_ITEM_ID `49`, PLATFORM_ITEM_ID `1070515947040` matched the authorized target.
- Session was healthy; no automatic recovery, QR scan, password action, Cookie renewal, or Token bootstrap was required.
- Owner context was confirmed and exactly one `下架` control existed before action; no already-off-shelf evidence existed.
- Exactly one route transaction was executed through `offline_items_normal_web`; old PC Seller API calls remained zero.
- The live Dialog text was `确定要下架这个宝贝吗？ 取消 确定`; local-only exact-text/leaf-most control resolution produced one safe `确定` confirmation and one `取消` escape control.
- The same authorized transaction performed the initial `下架` click and the single Dialog `确定` click.
- Route result and UI result were successful. Independent post-action page evidence showed `下架` absent and explicit `已下架` text.
- `PLATFORM_OFFSHELF_CONFIRMED=true` and `REAL_OFFSHELF_CANARY_SUCCESS=true`.
- One existing item synchronization completed successfully. Local cached status remained `-9`, which does not negate explicit platform success.
- No manual database/Redis write, other item/account product action, delete, publish, relist, edit, polish, Git push, GitHub write, or PR #26 change occurred during the real canary.

## Formal frontend delivery acceptance

- `BACKEND_REAL_CANARY=PASSED` and the explicit platform final state is `已下架` for the fixed authorized canary item.
- `FRONTEND_LIVE_MUTATION_CANARY=NOT_REQUIRED`: frontend delivery does not repeat a real product mutation because it only calls the already real-canary-verified Backend route.
- Product management reuses the pre-existing checkbox/batch-offline flow and the pre-existing `batchOfflineItems()` API wrapper; no duplicate API client or alternate off-shelf route exists.
- A row-level single-item `下架` entry exists and is visually/semantically separate from `删除`.
- Single-item confirmation explicitly says `下架后不会删除商品` and cancel performs no API call.
- Batch confirmation displays the selected count, requires a non-empty selection, preserves the existing explicit single-account selection rule, and rejects cross-account selection rather than merging accounts implicitly.
- Single and batch requests have in-flight locks so repeated clicks cannot create duplicate submissions.
- Full success, partial success, auth/session failure, verification-required failure, and request exception have human-readable UI feedback; no internal stack or `cookies_str` is rendered.
- Successful off-shelf responses refresh the list. If a successfully off-shelved item remains visible, current-page session state shows `已下架` and disables another off-shelf attempt.
- `item_status=-9` is never treated as an authoritative offline state; no database state is fabricated.
- Frontend unit/contract tests pass 27/27, including the explicit IPv4 container-health regression; lint passes, and TypeScript/Vite production build passes.
- Backend targeted tests remain 37/37 PASS and publish/Profile regressions remain 19/19 PASS after frontend work.
- Production frontend image `xianyu-chg0019-frontend:2b672d2-offline-ui-health` serves HTTP 200 and reports Docker Health `healthy`, while the verified Backend remains `xianyu-chg0019-backend-web:44c8ae9-nonsemantic-confirm` and healthy.
- Production read-only smoke uses actual deployed assets with synthetic intercepted data; row entry, confirmation, cancel, list load, zero page errors, zero sensitive render, and zero real `/items/batch-offline` forwarding are all verified.
- Mocked deployed-asset frontend-backend contract scenarios cover success, partial failure, auth failure, and server/network exception with correct payloads and zero real Backend forwarding.
- No new real product action or real off-shelf action occurs during frontend delivery.
- PR #28 review hardening changes only success classification, preserves the already real-canary-verified click/confirmation execution path, requires no new real canary, and passes 47/47 targeted Backend tests plus the existing 19/19 publish/Profile regressions and 27/27 Frontend tests.

IMPLEMENTATION_COMPLETE=true
BACKEND_REAL_CANARY_PASSED=true
FRONTEND_DELIVERY_VERIFIED=true
DELIVERY_READY=true
