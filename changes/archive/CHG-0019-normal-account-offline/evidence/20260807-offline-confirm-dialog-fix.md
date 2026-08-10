# CHG-0019 Offline Confirm Dialog Fix Evidence

Status: IMPLEMENTING

Change ID: CHG-0019-normal-account-offline

## Scope

This evidence records a zero-product-action repair of the normal-Web off-shelf confirmation classifier after the canary returned `unsafe_or_ambiguous_offline_confirmation`.

REAL_PRODUCT_ACTIONS=0
REAL_OFFSHELF_UI_ACTIONS=0

## Previous canary evidence

- Existing backend/Playwright logs record the fail-closed classification but did not preserve the confirmation dialog title/body/button text.
- No saved screenshot, HTML snapshot, DOM dump, or prior temporary debug artifact containing the dialog text was found.
- `PREVIOUS_DIALOG_EVIDENCE_FOUND=false`.

## Official normal-Web bundle evidence

Read-only static inspection of `https://g.alicdn.com/idle-pc/xy-site/0.0.172/js/p_item-index.js` shows the seller `下架` control invokes the official confirm helper with:

- title: `确定要下架这个宝贝吗？`
- `closable: true`
- `onOk` calls `mtop.taobao.idle.item.downshelf`, version `2.0`, with the item ID
- successful completion shows `下架成功`

The same bundle's confirm-helper module (`38965`) defines default labels:

- `okText`: `确定`
- `cancelText`: `取消`
- both confirm and cancel controls are shown by default

The adjacent delete action is separately defined as:

- title: `确定要删除这个宝贝吗？`
- API: `com.taobao.idle.item.delete`
- success text: `删除成功`

This establishes that the action type is carried by the local dialog context while a safe positive control may be the generic `确定` label.

## Confirmed defect

The previous classifier already allowed `确定`/`确认`, but it used a broad dialog selector combining `[role='dialog']`, `.ant-modal-content`, `.ant-modal`, and substring class matches. One logical Ant Modal could therefore be counted through nested parent/child containers. It also searched `button, [role='button'], a, div, span`, allowing one semantic button label to be counted through nested elements.

ROOT_CAUSE=OFFSHELF_CONFIRM_DIALOG_CLASSIFIER_TOO_STRICT_OR_INCOMPLETE

## Minimal fix

- Prefer one visible semantic `[role='dialog']`; fall back to one visible `.ant-modal-content` only when no semantic dialog root exists.
- Inspect only the selected dialog's own text and controls; never use page-body text for confirmation classification.
- Require local off-shelf semantics and reject `删除`, `永久删除`, `注销`, `清空`, `编辑`, `发布`, or `上架` semantics.
- Search only semantic `button` / `[role='button']` controls inside the dialog.
- Accept exactly one positive control from `确定`, `确认`, `确认下架`, `确定下架`.
- Require a local `取消` or `关闭` escape action.
- Missing dialog, multiple dialogs, missing escape action, or multiple positive controls fail closed.

## Validation

- CHG-0019 targeted tests: 22 passed.
- Existing publish/Profile regression: 19 passed.
- No real product action was used to obtain or validate this evidence.
