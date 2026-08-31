# CHG-0037 Design

Change ID: CHG-0037-opencv-headless-runtime-dependency
Status: APPROVED

## Execution contract

User outcome: restore deterministic cv2 availability in XIANYU Backend without changing Publisher business behavior.

Confirmed blocker: current production Backend lacks cv2 and fails during Publisher import before any platform request.

Smallest success test: exact source-controlled headless OpenCV pin, clean candidate import/version checks, Backend-only activation, and hard-blocked Material 94 pre-platform dry-run with zero platform writes.

## Dependency authority

`CURRENT_BACKEND_DEPENDENCY_AUTHORITY=upstream backend-web/pyproject.toml consumed by upstream backend-web/Dockerfile`

Pinned and current upstream both already contain:

`opencv-python-headless>=4.10.0`

The upstream Backend Dockerfile copies `backend-web` and extracts `[project].dependencies` from `/app/backend-web/pyproject.toml` into `/tmp/requirements.txt`, then runs pip install. Therefore the minimal deterministic source delta is:

`opencv-python-headless>=4.10.0 -> opencv-python-headless==5.0.0.93`

The XIANYU persistence artifact is:

`vendor/patches/xianyu-auto-reply/chg0037-opencv-headless-runtime-dependency.patch`

## Historical evidence

Historical source-fix commit `4df4352ab0ee8dbf32c07e81acd75998e6b3b25d` added the upstream publish-restore vendor artifact, whose dependency hunk added `opencv-python-headless>=4.10.0` to `backend-web/pyproject.toml`. That historical commit also contained unrelated publish/business/governance delta, so it must not be cherry-picked wholesale.

The immutable historical Backend image `xianyu-chg0018-backend-web:publish-upstream-742fb58-20260817` currently verifies:

- `cv2.__version__ == 5.0.0`
- `importlib.metadata.version('opencv-python-headless') == 5.0.0.93`

The current CHG-0036 production Backend verifies the negative condition: `ModuleNotFoundError: No module named 'cv2'`.

## Build and Runtime design

1. Apply the dependency-only patch against pinned upstream `742fb58...` in an isolated source worktree.
2. Preserve current runtime business-source lineage; do not alter Publisher/session/cookie behavior.
3. Build an immutable Backend candidate through a Docker build, never by mutating the running container.
4. Candidate must report the final XIANYU main SHA in image metadata and must pass:
   - `import cv2`
   - `cv2.__version__ == 5.0.0`
   - distribution `opencv-python-headless == 5.0.0.93`
   - `import common.services.xianyu_publish_video`
   - Publisher module/class import
   - forbidden session pattern count zero.
5. Record current Backend container/image/runtime configuration before replacement.
6. Replace Backend only through the existing protected lifecycle implementation; do not touch Frontend/WebSocket/Scheduler/MySQL/Redis.
7. Re-run health, account read-only smoke, chat read-only smoke, and production container cv2/session checks.
8. Execute Material 94 dry-run with transport hard-blocked before the real platform request boundary.

## Platform write guard

`PLATFORM_WRITE_GUARD_ACTIVE=true`

All source tests and dry-runs must stub/intercept the Publisher platform transport. A successful dry-run is a blocked failure/preflight result, never a publish SUCCESS. Required counters:

`REAL_PUBLISH_HTTP_REQUEST_COUNT=0`
`REAL_ITEM_CREATE_COUNT=0`

## Allowed change scope

- one dependency-only vendor patch;
- CHG-0037 tests;
- CHG-0037 governance/evidence;
- vendor README registration;
- generated state updates through repository scripts only.

## Forbidden change scope

- Publisher business logic;
- session/cookie flow;
- Material/account data;
- Frontend/WebSocket/Scheduler;
- MySQL/Redis;
- real publish or message/order writes;
- running-container package installation;
- old site-packages/venv copying.

## Upstream capability audit

Existing upstream dependency authority and Docker install path are sufficient.

## Pinned upstream evidence

`742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`, `backend-web/pyproject.toml`, `backend-web/Dockerfile`.

## Existing local implementation search

Historical formal OpenCV evidence exists, but the current runtime lineage omits cv2 and current XIANYU main lacks the old publish-restore dependency artifact.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

No second dependency/build owner is added; only the current authority is pinned.

## Why upstream cannot satisfy the requirement

The upstream range does not guarantee this project's exact proven package build or prevent local replay lineage from dropping it without a XIANYU regression artifact.

## Approved exception ADR

Not applicable.

## Component owner

Upstream Backend dependency/build files; XIANYU release governance and runtime activation.

## Retirement plan for overlapping local code

Retire the local pin if upstream later provides an equivalent exact pin and replacement is proven by clean replay plus production runtime verification.
