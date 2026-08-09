# CHG-0018 Final E2E UI Execution Contract

> Historical execution contract: the `polish.enabled=false` condition below applied to the UI verification stage only. Final production state is `polish.enabled=true`, with Vendor Patch SHA256 `94C8682263C17DBD416BE115534412E8EAC340E161AC5D24DAFDF202015FFDFD` and Scheduler image `xianyu-chg0018-scheduler:56d62e2-94c8682`; see `20260807-final-production-enable-closeout.md`.

User outcome: Account management must show the effective auto-polish state by combining account `auto_polish` with the existing system-level `polish` scheduled-task state.

Confirmed blocker: The account page currently renders only `account.auto_polish`, so an enabled account appears active even while the global `polish` task is disabled.

Smallest success test: Reuse `GET /api/v1/admin/scheduled-tasks`, fail closed on read errors, build the frontend successfully, deploy only Frontend, and confirm the production UI assets contain the global-pause and effective-state messages while Scheduler remains untouched and `polish.enabled=false`.
