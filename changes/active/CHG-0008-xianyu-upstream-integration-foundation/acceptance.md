Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: VERIFYING
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
- P0-P6 statuses are recorded truthfully.
- Dedicated test-account P1 login was performed only with operator participation and remains limited to local pilot evidence.
- P2-P6 were executed only after explicit operator approvals and manual owner actions.
- P7 one-time schedule was not executed in CHG-0008.
- Final recommendation is `WRAP`.

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
- Message listener: not started during P1.
- Scheduler: not started.
- Messages received during P1: none verified in this stage.
- Messages sent during P1: none.
- Listings published during P1: none.
- Listings deleted during P1: none.
- Automatic action occurred: false.

## P2 acceptance evidence

- P2 = PASSED.
- WebSocket service: `xianyu_pilot_websocket`.
- Source: pinned local upstream checkout only.
- Host binding: `127.0.0.1:18090`.
- Health: running.
- Database: connected.
- Registered instances: 1.
- Connected instances: 1.
- Controlled stop/start recovery: passed.
- Scheduler, crawler, promotion, updater: not running.
- Cookie / Token / Session values: not output.
- Platform risk verification: not observed after P1 completion.

## P3 acceptance evidence

- P3 = PASSED.
- Operator-controlled test message was received by the Pilot.
- Test marker row count: 1.
- Automatic reply process status: skipped.
- Reply mode: none.
- Reply strategy: none.
- Reply text produced: false.
- Non-empty send result: false.
- Orders created: 0.
- Risk-control logs: 0.

## P4 acceptance evidence

- P4 = PASSED.
- Project owner manually replied through the official client.
- Pilot observed the manual reply event.
- Total observed message rows: 2.
- Automatic reply process status: skipped for both rows.
- Reply mode: none for both rows.
- Reply strategy: none for both rows.
- Reply text produced: false.
- Non-empty send result: false.
- Orders created: 0.
- Risk-control logs: 0.

## P5 acceptance evidence

- P5 = PASSED.
- Project owner manually published one controlled test listing through the official client.
- This acceptance uses operator attestation plus local side-effect audit; the Pilot did not crawl or manage listing state.
- Publish logs created by Pilot: 0.
- Listing monitor rows: 0.
- Crawler rows: 0.
- Orders created: 0.
- Risk-control logs: 0.
- Automatic message output: false.

## P6 acceptance evidence

- P6 = PASSED as delisted cleanup, not deletion.
- Project owner manually took the controlled test listing off sale through the official client.
- The listing was not deleted.
- This acceptance uses operator attestation plus local side-effect audit; the Pilot did not delete, crawl, or manage listing state.
- Publish logs created by Pilot: 0.
- Listing monitor rows: 0.
- Crawler rows: 0.
- Orders created: 0.
- Risk-control logs: 0.
- Notification automation: 0.
- Automatic message output: false.

## P7 acceptance evidence

- P7 = NOT_EXECUTED.
- No one-time schedule was started.
- Scheduler, crawler, promotion, and updater remain outside the CHG-0008 runtime evidence.

## P0-P7 final status

- P0 system startup: PASSED, isolated localhost-only startup completed.
- P1 manual scan login: PASSED, supervised dedicated test-account QR login completed.
- P2 online state: PASSED, WebSocket registered and connected with controlled recovery.
- P3 read-only message verification: PASSED, inbound test marker observed and automatic reply skipped.
- P4 manually confirmed reply: PASSED, manual reply event observed and automatic reply skipped.
- P5 manually confirmed test listing: PASSED by operator attestation and side-effect audit.
- P6 test listing cleanup: PASSED as operator-delisted cleanup, not deletion.
- P7 one-time schedule: NOT_EXECUTED.

## Pilot conclusion

Final recommendation: `WRAP`.

The upstream is promising as an isolated supervised Pilot reference, but CHG-0008 does not adopt the upstream runtime into `D:/xianyu`. The next separately authorized change should wrap only the narrow behavior proven here, preserve local credential isolation, require explicit manual-operation gates, and continue to fail closed on platform risk, credential leakage, or uncertain send/publish/delete outcomes.

## Progress

Completed tasks: 9 / 9
Next task: null
