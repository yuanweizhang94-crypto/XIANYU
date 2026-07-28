Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: IMPLEMENTING
# Acceptance

## Corrected CHG-0008 acceptance

- The previous adapter-heavy direction is explicitly corrected.
- No `app/xianyu_system/adapters/xianyu/` package exists.
- No fake adapter classes are implemented.
- Long-term anti-drift and duplicate-development guardrails are preserved.
- Product roadmap and upstream registry are simple fact sources, not a new governance product.
- Primary upstream is pinned to `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.
- Primary upstream license is AGPL-3.0.
- Reference upstream is pinned to `5ce38ab2c4236f7eaa65983ce5c2da1f2fbd09af`.
- Reference upstream license status is UNRESOLVED due absent LICENSE at pinned commit.
- Upstream code is not copied into `D:/xianyu`.
- Upstream code is not executed by this correction commit.
- Remote scripts and prebuilt images are not used by this correction commit.
- P0-P7 statuses are recorded truthfully.
- Without a dedicated test account and operator participation, real Xianyu verification remains blocked.
- Recommendation remains `INSUFFICIENT_EVIDENCE` until supervised pilot results exist.

## P0-P7 current status

- P0 system startup: NOT_STARTED, waiting for operator-approved local runtime setup.
- P1 manual scan login: BLOCKED, no dedicated supervised test account provided in this turn.
- P2 online state: BLOCKED by P1.
- P3 read-only message verification: BLOCKED by P1 and a second controlled test account/message source.
- P4 manually confirmed reply: BLOCKED by P3.
- P5 manually confirmed test listing: BLOCKED by P4 and explicit low-risk test listing assets.
- P6 test listing cleanup: BLOCKED by P5.
- P7 one-time schedule: BLOCKED by stable P5 and P6.

## Progress

Completed tasks: 5 / 9
Next task: T6 Execute local isolated P0 startup only after operator approves upstream runtime setup
