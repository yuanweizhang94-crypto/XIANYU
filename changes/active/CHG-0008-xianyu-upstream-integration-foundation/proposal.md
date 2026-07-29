Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: IMPLEMENTING
# CHG-0008 Xianyu upstream pilot

## Direction correction record

The first CHG-0008 draft leaned toward building a clean-room offline adapter foundation before any live upstream pilot evidence existed. The project owner corrected that direction. CHG-0008 now prioritizes a pinned upstream pilot, static safety audit, isolated deployment plan, and supervised test-account checklist.

The repository must stop manufacturing large adapter abstractions without real validation input. `app/xianyu_system/adapters/xianyu/` is not created in this change. `FakeXianyuSessionAdapter`, `FakeXianyuMessageAdapter`, `FakeXianyuPublishAdapter`, complex maturity runtime, and large mapping DTO layers are explicitly deferred until real pilot results prove a specific local interface is necessary.

## Owner authorization

The project owner authorizes this correction and authorizes preserving the current Change ID instead of rewriting history or renaming the branch. No previous CHG-0008 commit exists; the correction is recorded in the first normal CHG-0008 commit.

## Corrected goal

Use pinned public upstream projects in an isolated local lab to determine whether the existing upstream can support a supervised, dedicated test-account path for:

1. system startup,
2. manual scan login,
3. online state,
4. read-only message receiving,
5. manually confirmed reply,
6. manually confirmed test listing,
7. test listing cleanup,
8. one-time schedule only after publish cleanup is proven.

## Current allowed state

The main repository records governance facts, upstream audit facts, deployment boundaries, and the P0-P7 checklist. It does not run live Xianyu, does not store Cookie material, does not copy upstream code, and does not create CHG-0009.

## P0 isolated startup result

P0 is PASSED for localhost-only upstream startup evidence. Docker Desktop data was moved from the C drive to the D drive through Docker Desktop managed storage. The actual Docker Desktop WSL data location is `D:\Administrator\Documents\DockerDesktopWSL`.

The C drive free space increased from 8.15 GiB before the migration to 16.25 GiB after the migration. Docker containers, images, volumes, and networks were preserved. The isolated pilot runs only MySQL, Redis, backend-web, and frontend. The administrator default password has been replaced. Backend and frontend are localhost-only. No real Xianyu connection, QR login, Cookie, Token, Session, Profile, message sending, item publishing, WebSocket, scheduler, crawler, Playwright, Patchright, Chromium, or browser process was executed for P0.

P1 manual scan login remains waiting for explicit operator approval and must not start without a separate authorization.

## Progress

Completed tasks: 6 / 9
Next task: T7 Execute supervised account P1-P3 only with a dedicated test account
Pilot status: WAITING_FOR_OPERATOR_APPROVED_P1_LOGIN
