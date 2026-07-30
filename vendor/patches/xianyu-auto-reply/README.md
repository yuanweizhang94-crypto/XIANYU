# Xianyu upstream patch artifacts

## CHG-0016 manual-only verification patch

- Base upstream repository: `zhinianboke/xianyu-auto-reply`
- Base pinned SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`
- Patch file: `bda1a85-manual-only-verification.patch`
- Patch SHA256: `76563EBC78AE0493175AC21EC6CC082C4B8E61FA45B9E34AA9BC0978475C25C2`
- Local patch worktree: `D:/xianyu-upstream-manual-chg0016`

## Runtime Boundary

The patch adds a default-off `CAPTCHA_MANUAL_ONLY` mode to the upstream captcha
orchestrator. When enabled it opens a visible local browser for the project
owner to complete the official verification page. It does not move the mouse,
type, click, drag, inject trajectories, call remote captcha services, create an
IM implementation, create a Token implementation, create a WebSocket
implementation, create a sender, or create a second automatic-reply executor.

The patch returns only allowed `x5*` Cookie delta fields and uses upstream
`merge_account_cookie_fields` for the automatic-reply Token path. It does not
persist verification URLs, print Cookie values, print Token values, or alter
online chat and automatic-reply Token cache ownership.
