# CHG-0019 Non-semantic Confirm Control Fix

Date: 2026-08-08
Change: CHG-0019-normal-account-offline
Status: IMPLEMENTING

## Confirmed blocker

`LIVE_DIALOG_CONFIRM_CONTROLS_ARE_NON_SEMANTIC_FOR_CURRENT_SELECTOR`

The previous owner-authorized canary captured the live dialog-local text:

- `确定要下架这个宝贝吗？ 取消 确定`

The existing classifier selected the unique visible dialog correctly and validated the safe down-shelf semantics correctly, but searched controls only with `button, [role='button']`. The live `取消/确定` controls were not exposed through those semantic nodes, so the transaction failed closed before confirmation.

No live dialog or product action was opened or executed during this repair.

## Minimal fix

Business source changed only in `backend-web/app/services/xianyu_publisher.py`.

The existing semantic path remains first:

- `button, [role='button']`

If that path cannot resolve one positive action plus an escape action, a strict fallback runs only inside the already-selected unique visible dialog:

- selector: `button, [role='button'], div, span`
- normalized exact positive text only: `确定`, `确认`, `确定下架`, `确认下架`
- normalized exact escape text only: `取消`, `关闭`
- wrapper candidates are removed when a deeper visible exact-text child exists (leaf-most dedup)
- controls must be visible, enabled, have a positive-size bounding box, and `pointer-events != none`
- center-point `elementFromPoint()` must resolve within the same dialog to the candidate/descendant or an interactive ancestor within that dialog
- no handler search or parent climbing outside the selected dialog
- dangerous dialog semantics (`删除`, `永久删除`, `注销`, `清空`, `编辑`, `发布`, `上架`) remain fail-closed
- multiple positive controls remain fail-closed
- missing cancel/close escape remains fail-closed

The title `确定要下架这个宝贝吗？` cannot match `确定` because fallback matching is normalized exact text, not substring matching.

## Tests

CHG-0019 targeted tests: 37/37 PASS.

Added live-DOM regression variants include non-semantic div controls, span controls, div/span nesting leaf-most dedup, title exclusion, delete-dialog rejection, duplicate positive rejection, cancel requirement, background/outside-dialog isolation, hidden duplicate exclusion, semantic button and role-button compatibility, overlay obstruction rejection, missing down-shelf semantics rejection, and down-shelf/delete conflict rejection.

Existing publish/Profile regression: 19/19 PASS.

`python scripts/validate_change.py`: PASS.

`python scripts/verify_repository.py`: 590/590 PASS after using a short Windows pytest temp path; the first run had one unrelated Windows long-path copy failure and 589 tests passed.

## Deployment

Backend image: `xianyu-chg0019-backend-web:44c8ae9-nonsemantic-confirm`

Only `xianyu_chg0017_backend_web` was replaced. Health endpoint returned HTTP 200. Container readback confirmed the new exact-text helper, leaf-most helper, dialog-local fallback, `elementFromPoint` overlay check, and dangerous-semantic rejection are present.

Scheduler, WebSocket, Frontend, MySQL, and Redis were not restarted by this task.

## Real-action counters

- REAL_OFFSHELF_ROUTE_CALLS=0
- REAL_OFFSHELF_UI_ACTIONS=0
- REAL_PRODUCT_ACTIONS=0

This evidence is repair/deployment evidence only. It must not be treated as `REAL_OFFSHELF_VERIFIED`.
