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

## Progress

Completed tasks: 5 / 9
Next task: T6 Execute local isolated P0 startup only after operator approves upstream runtime setup
Pilot status: WAITING_FOR_OPERATOR_APPROVED_P0_SETUP
