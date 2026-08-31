# CHG-0037 Tasks

Change ID: CHG-0037-opencv-headless-runtime-dependency
Status: APPROVED

- [x] T1 Reconfirm XIANYU remote main, COMPANY remote main, dirty worktrees, current production Backend identity and current upstream authority.
- [x] T2 Audit historical cv2 source/runtime evidence and prove the dependency delta without cherry-picking unrelated historical work.
- [x] T3 Create isolated clean XIANYU and pinned-upstream worktrees.
- [x] T4 Define this executable dependency-only Change and platform-write guard.
- [x] T5 Persist the exact `opencv-python-headless==5.0.0.93` dependency vendor patch and vendor registry entry.
- [x] T6 Add and pass dependency declaration/artifact regression tests plus CHG-0036 session regression tests.
- [x] T7 Prove clean patch replay on pinned upstream and run targeted/repository/diff/secret gates.
- [ ] T8 Commit exact task files, push branch, create PR, require security/quality/tests PASS, merge, and prove fix ancestry on main.
- [ ] T9 Build an immutable Backend candidate from merged XIANYU main and verify cv2/package/Publisher/session gates before activation.
- [ ] T10 Record rollback/runtime configuration identity and replace Backend only through the existing protected lifecycle.
- [ ] T11 Verify production Backend health, cv2/package version, session guard, canonical cookie flow, account read-only smoke, and chat read-only smoke.
- [ ] T12 Run Material 94 hard-blocked production Runtime dry-run using account 2804730247 only if current read-only readiness remains passing.
- [ ] T13 Prove zero real publish HTTP requests/items and no false publish SUCCESS.
- [ ] T14 Archive the Change, regenerate project state, complete final GitHub closure, rebuild/relabel final-main Backend if required for exact source-SHA equality, and STOP without a real canary.

## Upstream capability audit

Existing upstream dependency authority and Docker install path are reused.

## Pinned upstream evidence

`742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`; current upstream `d8c1a970304fdfb31fef549e07167d7ce82c0819` retains the OpenCV headless dependency.

## Existing local implementation search

Historical formal image proves OpenCV works; current production image proves cv2 is absent. No business source repair is required.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

Only the existing dependency declaration is pinned; no duplicate owner is created.

## Why upstream cannot satisfy the requirement

A XIANYU-controlled exact pin and regression artifact are needed to make the local Runtime lineage deterministic.

## Approved exception ADR

Not applicable.

## Component owner

Upstream Backend dependency/build path, with XIANYU vendor/release governance.

## Retirement plan for overlapping local code

Remove the local pin only after an equivalent upstream exact pin is proven in clean build and production Runtime.
