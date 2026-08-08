# CHG-0019 PR #28 review success-classification hardening

Status: VERIFYING

Change ID: CHG-0019-normal-account-offline

REVIEW_FINDING=GLOBAL_BODY_OFFLINE_SUCCESS_FALSE_POSITIVE_RISK
FIX=TARGET_SPECIFIC_POST_ACTION_SUCCESS_EVIDENCE

## Review boundary

- CHG-0019 predecessor: `44c8ae98ac576f9ab486fae473d56f26480b8868`.
- The predecessor is an ancestor of formal delivery commit `0573db0581eee71620a0260f7b639cd1b69a3401`.
- The true pre-review CHG-0019 delta is 2 commits / 28 files relative to that predecessor, rather than the unrelated `main..CHG-0019` historical range.
- Review-only stack base branch: `review-base/CHG-0019-predecessor-44c8ae9`, pushed at the exact predecessor commit.
- The stack-base branch is review infrastructure only. It does not reactivate CHG-0018 and must not be treated as a production branch.

## Finding

The verified normal-Web off-shelf path previously allowed `_wait_for_offline_ui_success()` to read `document.body.innerText` and accept broad page-level strings such as `已下架` / `下架成功`. That could theoretically confirm the target item from unrelated page regions such as recommendations, stale content, or other UI text.

## Hardening

The execution path remains the same; only post-action success classification is stricter.

- Global `document.body.innerText` is no longer used as off-shelf success evidence.
- Before the real action, visible explicit off-shelf success notices are snapshotted only from notice containers (`[role='alert']`, toast/message containers).
- After the action, a success notice counts only when its normalized occurrence count is greater than the pre-action snapshot, so stale pre-existing `下架成功` text cannot confirm the current transaction.
- The exact target detail-page `item_id` is rechecked before evaluating evidence and again immediately before returning success.
- The pre-action owner-operation DOM location is captured from the already validated unique `下架` control.
- Owner-context success requires the actionable `下架` control to be absent and the same captured owner-operation location to expose an exact visible reverse state of `上架`, `重新上架`, or `已下架`.
- `下架` disappearance alone is never sufficient.
- Login/verification state remains fail-closed.
- Cookie injection, detail URL, unique control resolution, delete isolation, confirmation dialog semantics, non-semantic confirm fallback, UI click count, batch route contract, and frontend API contract are unchanged.

## Regression evidence

Targeted Backend CHG-0019 tests: 47/47 PASS.

New review regressions include:

1. unrelated page-body `已下架` while target owner context still has `下架` -> FALSE;
2. recommendation text `商品已下架` while target still has `下架` -> FALSE;
3. stale pre-action `下架成功` notice with no new notice -> FALSE;
4. new post-action `下架成功` notice with exact target URL -> TRUE;
5. same target owner context: `下架` absent + `上架` -> TRUE;
6. same target owner context: `下架` absent + `已下架` -> TRUE;
7. `下架` absent without reverse state -> FALSE;
8. URL changes to another item despite success-like text -> FALSE;
9. login/verification page -> FALSE;
10. target owner context missing while page body contains `已下架` -> FALSE.

Existing publish/Profile regressions: 19/19 PASS.
Frontend offline UI tests: 27/27 PASS.
Frontend lint: PASS.
Frontend production build: PASS.

## Recovery artifact

Layered review-fix patch:

`vendor/patches/xianyu-auto-reply/4c5e1ac-chg0019-pr28-review-success-classification-hardening.patch`

Apply order:

1. CHG-0017 patch;
2. CHG-0018 patch;
3. CHG-0019 formal-delivery patch;
4. PR #28 review success-classification hardening patch.

Patch SHA256: `B4F9673CF486EC57FF235BAF97182066703FE6D2E4EE7910A3828AC769A1C912`.
Clean layered apply check: PASS.
Final Git blob equivalence: 2/2 target files match the hardened source snapshot.

## Safety

- `NEW_REAL_OFFSHELF_CANARY_REQUIRED=false`.
- No new real off-shelf transaction or other product action was executed.
- The prior controlled real-canary evidence remains valid because the click/confirmation execution path is unchanged and the independent post-action evidence already recorded explicit platform `已下架` state.
- No production container, database, Redis, account Session, or Xianyu login was changed.
- PR #26 is unrelated and must remain unchanged.

REAL_PRODUCT_ACTIONS=0
REAL_OFFSHELF_ACTIONS=0
CONTAINERS_CHANGED=0
