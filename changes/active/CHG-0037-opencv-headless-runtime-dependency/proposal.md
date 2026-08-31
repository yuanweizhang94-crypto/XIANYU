# CHG-0037 OpenCV Headless Runtime Dependency Persistence

Change ID: CHG-0037-opencv-headless-runtime-dependency
Status: APPROVED
Created: 2026-08-31
Owner task: xianyu_cv2_dependency_final_closure

## User Outcome

User outcome: persist the missing Backend OpenCV runtime dependency in canonical source governance, build and activate a Backend image that imports cv2, and prove Material 94 can traverse the production pre-platform publish path with the real platform transport hard-blocked.

Confirmed blocker: the accepted CHG-0036 production Backend image does not contain cv2 even though the pinned upstream Backend dependency authority includes OpenCV. The dependency was present in a historical formal publish image but was lost from later Runtime lineage/replay.

Smallest success test: a minimal vendor dependency patch pins `opencv-python-headless==5.0.0.93`, targeted source/regression gates pass, the final-main Backend candidate and production Backend both import cv2 version 5.0.0, and Material 94 reaches a hard-blocked platform boundary with zero real publish HTTP requests and zero item creation.

## Scope

`BUSINESS_SOURCE_LOGIC_CHANGED=false`

Allowed:
- isolated clean XIANYU worktree based on current `origin/main`;
- one dependency-only vendor patch for `backend-web/pyproject.toml`;
- dependency regression tests and sanitized Change/evidence updates;
- targeted tests, repository verification, diff check and secret scan;
- Git branch/PR/CI/merge closure;
- clean Backend candidate build and Backend-only replacement through the existing guarded lifecycle path;
- read-only account/chat smoke and hard-blocked Material 94 runtime dry-run.

Forbidden:
- modifying Publisher business logic, session/cookie flow, Material content, account state, Frontend, Scheduler, WebSocket, MySQL or Redis;
- real Xianyu publish, auto-reply configuration, message send or order mutation;
- direct mutation of a running container or `docker exec pip install`;
- copying old site-packages/venv, compose down, prune, volume deletion, secret exposure, force push, direct push to main.

## Development precheck

TASK_TYPE=REPAIR
FAILURE_REASON=Backend Runtime import chain fails with `ModuleNotFoundError: No module named 'cv2'` before platform publish transport.
RESPONSIBLE_LAYER=XIANYU Backend dependency/build persistence.
CURRENT_UPSTREAM_CAPABILITY=EXISTS; pinned and current upstream declare `opencv-python-headless>=4.10.0` in `backend-web/pyproject.toml` and Backend Dockerfile installs that dependency list.
CURRENT_LOCAL_CAPABILITY=PARTIAL; historical XIANYU formal evidence carried the upstream dependency delta, but current canonical vendor layering does not preserve an exact reproducible OpenCV runtime pin.
CURRENT_RUNTIME_CAPABILITY=MISSING; current production Backend does not import cv2.
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=No business function. Patch only the existing upstream Backend dependency declaration from a range to the historically proven exact package version.
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=There is no business-function defect; the missing runtime package must be made deterministic in the source-controlled dependency layer.
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=No new implementation is required. This Change is a minimal dependency persistence patch plus tests/evidence.

## Upstream capability audit

Pinned upstream `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1` and current upstream `d8c1a970304fdfb31fef549e07167d7ce82c0819` both declare `opencv-python-headless>=4.10.0` in `backend-web/pyproject.toml`. `backend-web/Dockerfile` extracts `[project].dependencies` from that file and installs them with pip. No second dependency owner is needed.

## Pinned upstream evidence

Pinned upstream SHA: `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.
Dependency authority: `backend-web/pyproject.toml`.
Build consumer: `backend-web/Dockerfile`.
Historical XIANYU source-fix commit: `4df4352ab0ee8dbf32c07e81acd75998e6b3b25d`.
Historical runtime image `xianyu-chg0018-backend-web:publish-upstream-742fb58-20260817` currently imports `cv2==5.0.0` with distribution `opencv-python-headless==5.0.0.93`.

## Existing local implementation search

Current XIANYU main contains CHG-0036 session regression guards and many runtime vendor patches, but does not contain the historical `742fb58-chg0018-latest-upstream-publish-restore.patch` that carried the original OpenCV dependency delta. Current production image `xianyu-chg0018-backend-web:chg0036-clean-replay-2df2087-20260830-r1` fails `import cv2`.

## Reuse decision

Decision: PATCH_UPSTREAM

The existing upstream dependency authority is retained. The only functional source delta is to pin its existing headless OpenCV requirement to the historically verified exact package build.

## Duplicate implementation risk

Low. No new Publisher, Session owner, dependency manager, service, route, worker or transport is introduced. Adding another runtime-only pip hotfix would create high drift risk and is forbidden.

## Why upstream cannot satisfy the requirement

Upstream's floating lower-bound dependency is correct functionally but does not by itself persist the exact historically verified package version through this project's local Runtime replay lineage. XIANYU needs one auditable pin artifact and regression guard so future clean builds cannot silently omit or resolve a different package.

## Approved exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not used.

## Component owner

Backend dependency declaration and installation remain owned by upstream `backend-web/pyproject.toml` plus `backend-web/Dockerfile`; XIANYU owns the minimal vendor pin and release/runtime proof.

## Retirement plan for overlapping local code

No overlapping production code is added. If upstream later pins an equivalent exact OpenCV build and the local pin becomes redundant, retire this vendor patch after clean-replay and runtime verification.
