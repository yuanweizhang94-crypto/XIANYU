Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: VERIFYING
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

The main repository records governance facts, upstream audit facts, deployment boundaries, and the P0-P6 supervised pilot evidence. It does not store Cookie material, does not copy upstream code, and does not create CHG-0009. P7 one-time schedule was not executed in CHG-0008.

## P0 isolated startup result

P0 is PASSED for localhost-only upstream startup evidence. Docker Desktop data was moved from the C drive to the D drive through Docker Desktop managed storage. The actual Docker Desktop WSL data location is `D:\Administrator\Documents\DockerDesktopWSL`.

The C drive free space increased from 8.15 GiB before the migration to 16.25 GiB after the migration. Docker containers, images, volumes, and networks were preserved. The isolated pilot runs MySQL, Redis, backend-web, frontend, and later the WebSocket service only after separate supervised authorization. The administrator default password has been replaced. Backend, frontend, and WebSocket are localhost-only. No remote scripts or prebuilt upstream application images were used.

## P1-P6 supervised pilot result

P1 manual scan login was executed only after explicit operator approval. The project owner used a dedicated supervised test account, completed the official mobile-side verification flow personally, and no verification data was collected or recorded by the repository. The login result is PASSED.

P2 WebSocket online validation is PASSED. The Pilot WebSocket service was built from pinned local upstream source, started as `xianyu_pilot_websocket`, bound only to `127.0.0.1:18090`, registered one connected instance, and recovered from one controlled stop/start cycle.

P3 read-only message receiving is PASSED. A project-owner controlled second account sent a test message. The Pilot recorded the inbound marker as local evidence while automatic reply remained skipped and no outgoing message occurred.

P4 manually confirmed reply is PASSED. The project owner replied manually in the official client. The Pilot observed the event as local evidence while automatic reply remained skipped and no outgoing automated message occurred.

P5 manually confirmed test listing is PASSED by operator attestation and side-effect audit. The project owner manually published one controlled test listing in the official client. The Pilot did not create publish logs, crawler rows, listing monitor rows, orders, or automatic message output.

P6 cleanup is PASSED as operator-delisted cleanup, not deletion. The project owner manually took the test listing off sale in the official client. The item was not deleted. The Pilot did not create delete, publish, crawler, listing monitor, order, risk, or automatic message side effects.

## Pilot conclusion

Final recommendation: `WRAP`.

The pinned upstream proved useful as an isolated supervised Pilot for login, online WebSocket connection, read-only message observation, manually confirmed reply observation, and manually published listing cleanup evidence. The main repository should not copy upstream code or immediately adopt upstream internals as the business runtime. Future work may define a narrow wrapper around observed upstream behavior only after a separately authorized change and must preserve localhost, credential, manual-operation, and fail-closed boundaries.

## Progress

Completed tasks: 9 / 9
Next task: null
Pilot status: P2_P6_PASSED_WITH_OPERATOR_DELISTED_CLEANUP
