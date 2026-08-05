# CHG-0018 Runtime Profile, Preflight, And Auto-Polish Evidence

Date: 2026-08-05

Target alias: `CANARY-A01`

## Owner Authorization

- Normal business-message log growth is not a blocker for this run.
- No synthetic test messages were sent.
- No products were created.
- No products were published.
- PR #26 was not changed.

## Frontend And Credential UI

- Frontend deployed: yes.
- WebSocket restarted by this deployment: no.
- Backend restarted by this deployment: no.
- MySQL or Redis rebuilt: no.
- UI password status: unconfigured credentials.
- Raw `login_password` accepted in ordinary account API response: no.
- Remark regression passed: yes.
- Credential content printed: no.

## Profile And Read-Only Preflight

- Profile created from authoritative database Cookie: yes.
- Profile healthy: yes.
- Manual verification required: no.
- Read-only publish preflight ready: yes.
- Preflight failure reason: null.
- Product form filled: no.
- Image uploaded: no.
- Publish clicked: no.

## Auto-Polish Root Cause

- Scheduler container before recovery: not running.
- Platform day before recovery: not ready.
- Root cause categories: `SCHEDULER_NOT_RUNNING`, `PLATFORM_DAY_NOT_READY`.
- Catalog synchronization path: upstream native fetch-items service.
- Catalog item count for target alias: 7.
- Cookie `_m_h5_tk` present: true.

## Auto-Polish Fix

- Fixed files in patch artifact:
  - `scheduler/app/services/scheduler/day_switch_task.py`
  - `scheduler/app/services/scheduler/polish_task.py`
  - `tests/test_chg0018_auto_polish_safety.py`
- Redis platform-day read failure fail-closed: yes.
- Platform-day update failure fail-closed: yes.
- Polish skipped until platform day ready: yes.
- Missing credentials avoid password login: yes.
- Missing credentials do not disable account: yes.
- Polish API response logging masked: yes.
- Token retry bounded: yes.
- Duplicate polish response treated as same-day success: yes.
- Canary account scope supported through existing polish service: yes.
- Canary max item limit supported through existing polish service: yes.

## Real Polish Canary

- Real polish canary executed: yes.
- Scope: target alias only.
- Max item count for explicit canary: 1.
- Explicit canary result: success.
- Explicit canary target log delta: 1.
- Explicit canary target success delta: 1.
- Explicit canary other-account polish delta: 0.
- Explicit canary password-login trigger count: 0.
- Explicit canary account-disabled result: false.
- Scheduler continued after canary: yes.
- Scheduler enabled tasks: `day_switch,fetch_items,polish`.
- Disabled scheduler task count: 18.
- Scheduler observed polish intervals: at least 2.
- Scheduler observed day-switch intervals: at least 2.
- Final target catalog count: 7.
- Final target polished count: 7.
- Final target unpolished count: 0.
- Other accounts polished during observation: 0.
- Other accounts with auto-polish enabled after setup: 0.
- `fetch_orders` executed: false.
- `dm_send` executed: false.
- `auto_order` executed: false.
- Password login triggered for target alias: false.
- Target account disabled: false.

## Runtime State

- Backend container: running and healthy.
- WebSocket container: running and healthy.
- Frontend container: running and healthy.
- Scheduler container: running.
- Scheduler health from container: HTTP 200.
- Single WebSocket executor observed: yes.
- Single Scheduler executor observed: yes.

## Patch And Validation

- Patch path: `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0018-account-profile-publish-safety.patch`.
- Patch SHA256: `F15F2161213EE7CD8B952D3DD475DEA18BA12F56570E332CE4711BD87D6350E2`.
- Patch clean apply: passed.
- Auto-polish targeted tests: 6 passed.
- CHG-0018 acceptance tests: 7 passed.
- CHG-0017 publish/AI regression tests: 58 passed.
- Frontend build: passed.
- Synthetic messages sent: 0.
- Products created: 0.
- Products published: 0.
- Sensitive data recorded: no.

## Rollback

- Disable `polish` in `xy_scheduled_tasks` to stop scheduled polishing.
- Set target account `auto_polish=false` through the existing account management path to stop target-account polishing.
- Stop the single scheduler container if scheduler rollback is required.
- Revert CHG-0018 patch artifact through Git if code rollback is required.

## Remaining Gate

Owner review is required before enabling auto-polish for any account other than `CANARY-A01`.
