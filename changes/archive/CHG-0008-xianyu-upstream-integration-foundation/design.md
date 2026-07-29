Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: ARCHIVED
# Design

## Repository split

Main repository: `D:/xianyu` remains the long-term business core and governance fact source. Upstream pilot repository: `D:/xianyu-upstream-pilot` is a separate lab clone of `zhinianboke/xianyu-auto-reply` at pinned commit `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.

The upstream lab directory is not a submodule, is not a second remote of the main repository, and must not be vendored into `D:/xianyu`.

## Upstream priority

Primary upstream: `zhinianboke/xianyu-auto-reply`, pinned to `bda1a859df63fa5f24e51398fa80a23490bb6dfc`, license AGPL-3.0.

Reference upstream: `cv-cat/XianYuApis`, pinned to `5ce38ab2c4236f7eaa65983ce5c2da1f2fbd09af`, license status unresolved because LICENSE is absent at the pinned commit even though README badges claim MIT.

## Static audit result

Static audit found multiple high-risk areas in the primary upstream: remote deployment scripts, update scripts, Docker Compose defaults using prebuilt images, services binding to `0.0.0.0`, default database and Redis credentials that must be changed, Cookie/Token/session handling modules, CAPTCHA/slider/face-verification related modules, WebSocket services, and publishing/deletion services.

These findings do not reject the upstream. They require an isolated localhost-only pilot with explicit operator approval before any runtime execution.

## Isolation strategy

The pilot must use local source checkout only, bind service access to `127.0.0.1`, use independent MySQL/Redis data and credentials, avoid public ports, avoid remote update scripts, avoid prebuilt images unless provenance is separately approved, and avoid mounting `D:/xianyu` or browser profile directories.

## Credential and account boundary

A dedicated test account is required before P1-P7. It must not be a main operating account, must not hold high-value assets, and must be controlled by the user for manual scan login. Cookie, Token, Session, and browser state may only remain in the upstream pilot local data area and must never be written into `D:/xianyu`, Git, final reports, or chat.

## Stop conditions

Stop immediately on CAPTCHA, slider, face verification, device verification, risk-control prompts, unknown send/publish outcome, duplicate message, duplicate publish risk, public exposure requirement, unchangeable default credentials, Cookie log leakage, or any need to modify existing `D:/xianyu` business modules.

## P0 runtime evidence

P0 used Docker Desktop managed storage on the D drive. The accepted actual Docker Desktop WSL data location is `D:\Administrator\Documents\DockerDesktopWSL`. The previously planned empty directory `D:\DockerDesktopData` is not treated as the authoritative location and is not required for P0 acceptance.

Docker data migration preserved the existing Docker environment: containers, images, volumes, and networks remained intact. The unrelated `sub2api`, `sub2api-redis`, and `sub2api-postgres` services remained healthy after recovery. The isolated pilot environment recovered with `mysql`, `redis`, `backend-web`, and `frontend` services. WebSocket was added later only for the supervised online validation stage.

The P0 service exposure remains localhost-only: backend-web is bound to `127.0.0.1:18089`, frontend is bound to `127.0.0.1:19000`, and MySQL and Redis have no host port mappings. P0 did not start WebSocket, scheduler, crawler, promotion, updater, Playwright, Patchright, Chromium, or any browser process. It did not connect to real Xianyu and did not process Cookie, Token, Session, Profile, message sending, or item publishing.

## P1 supervised login evidence

P1 used the pinned upstream local source and the existing localhost-only pilot UI at `http://127.0.0.1:19000/accounts`. The real code path was `frontend` account management to `backend-web` QR login APIs. The QR image was generated locally by `backend-web` using the upstream QR login manager and was displayed only in the local browser UI.

The project owner manually scanned with a dedicated test account and completed the official mobile-side verification personally. No face data, identity document data, Cookie value, Token value, Session value, password, QR content, or complete account identifier is recorded in this repository, Git history, PR text, or chat.

P1 read-only result: account record created, login state success, credential stored in the local Pilot database, strict log heuristics did not find complete credential output, message listener was not running, automatic action logs remained empty, and no additional risk verification prompt remained visible after the owner completed the official mobile-side verification.

## P2-P6 supervised online evidence

P2 built and started `xianyu_pilot_websocket` from pinned local upstream source only. It is exposed only on `127.0.0.1:18090`; MySQL and Redis still have no host port mappings. The WebSocket health endpoint reported `running`, database connectivity reported `connected`, and connection statistics reported one total instance and one connected instance. A controlled stop/start recovery remained healthy.

P3 received a controlled inbound test message from a second owner-controlled account. The marker was recorded locally, but `process_status` stayed `skipped`, `reply_mode` stayed `none`, `reply_strategy` stayed `none`, no reply text was produced, and no non-empty send result was recorded.

P4 observed the project owner's manual reply from the official client. Local records increased to two message observations, both skipped with no reply text and no send result. This confirms observation without automated reply.

P5 used operator attestation for a manually published controlled test listing. The Pilot did not create publish logs, listing monitor rows, crawler rows, order rows, risk rows, automatic reply text, or non-empty send results.

P6 used operator attestation for cleanup by manually taking the test listing off sale. This was delisting, not deletion. The Pilot did not create delete, publish, listing monitor, crawler, order, risk, notification, or automatic message side effects.

P7 one-time schedule was not executed in CHG-0008. No scheduler, crawler, promotion, updater, or automatic platform action was started.

## Adoption boundary

The selected conclusion is `WRAP`. The pinned upstream can remain a supervised external Pilot reference for future wrapper design, but CHG-0008 does not copy upstream code, does not import upstream runtime into `D:/xianyu`, and does not authorize automatic live Xianyu operation. Any future wrapper or runtime adoption requires a separate active change with fresh owner authorization and explicit credential, operation, and platform-risk gates.

## Progress

Completed tasks: 9 / 9
Next task: null

## Post-merge archive record

CHG-0008 is archived after PR #9 merged into `main` through normal two-parent merge commit `e7a9205dfeafd8b5e0f617f1855ecc4a33d6441c`. Merged feature HEAD was `28220961586f4ea0008636d59635a39f6b44684d`.

The archived result preserves the supervised upstream Pilot evidence: P0 startup passed, P1 supervised login passed, P2 WebSocket online validation passed, P3 read-only message receiving passed, P4 manual reply observation passed, P5 manual test listing publication passed by operator attestation and side-effect audit, P6 cleanup passed as operator-delisted cleanup rather than deletion, and P7 one-time schedule was not executed.

The final recommendation remains `WRAP`. CHG-0008 did not copy upstream code into `D:/xianyu`, did not commit Cookie, Token, Session, browser Profile, account secrets, message bodies, or credential values, did not adopt the upstream runtime into the main repository, did not enable scheduler, crawler, promotion, updater, automatic reply, automatic delivery, automatic publishing, or automatic deletion, and did not create CHG-0009 before archive. The next separately authorized change may create CHG-0009-xianyu-upstream-wrapper-mvp from latest `main` to wrap only the narrow supervised upstream behavior proven by CHG-0008.
