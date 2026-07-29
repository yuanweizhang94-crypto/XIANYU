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
- The initial correction commit did not execute upstream code.
- P0 later executed only the isolated localhost upstream pilot startup path after operator approval.
- Remote scripts and prebuilt upstream application images are not used by this change.
- P0-P7 statuses are recorded truthfully.
- Dedicated test-account P1 login was performed only with operator participation and remains limited to local pilot evidence.
- Recommendation remains `INSUFFICIENT_EVIDENCE` until P2-P7 supervised pilot results exist.

## P0 acceptance evidence

- P0 = PASSED.
- Docker Desktop WSL data actual location: `D:\Administrator\Documents\DockerDesktopWSL`.
- Docker data migration result: Docker data successfully moved from C drive to D drive.
- C drive free before migration: 8.15 GiB.
- C drive free after migration: 16.25 GiB.
- Docker resources preserved: containers, images, volumes, and networks.
- Pilot services: mysql, redis, backend-web, frontend.
- Administrator default password: replaced.
- Network: localhost-only.
- Real Xianyu connection: not performed during P0.
- Cookie / Token / Session / Profile: not processed during P0.
- P1 manual scan login: PASSED after explicit operator approval.

## P1 acceptance evidence

- P1 = PASSED.
- Login method: supervised QR scan.
- Account type: dedicated test account controlled by the project owner.
- Operator action: project owner manually scanned and personally completed official mobile-side verification.
- Credential storage: local Pilot database only.
- Credential values: not recorded.
- Face or identity data: not collected, read, output, or recorded.
- Risk-control bypass: none.
- Additional risk verification after completion: none visible in the local UI.
- Message listener: not started.
- Scheduler: not started.
- Messages received: none verified in this stage.
- Messages sent: none.
- Listings published: none.
- Listings deleted: none.
- Automatic action occurred: false.
- Draft PR remains Draft; P2 is waiting for explicit operator approval.

## P0-P7 current status

- P0 system startup: PASSED, isolated localhost-only startup completed.
- P1 manual scan login: PASSED, supervised dedicated test-account QR login completed.
- P2 online state: WAITING_FOR_OPERATOR_APPROVAL.
- P3 read-only message verification: BLOCKED by P2 and a second controlled test account/message source.
- P4 manually confirmed reply: BLOCKED by P3.
- P5 manually confirmed test listing: BLOCKED by P4 and explicit low-risk test listing assets.
- P6 test listing cleanup: BLOCKED by P5.
- P7 one-time schedule: BLOCKED by stable P5 and P6.

## Progress

Completed tasks: 6 / 9
Next task: T7 Execute supervised account P1-P3 only with a dedicated test account
