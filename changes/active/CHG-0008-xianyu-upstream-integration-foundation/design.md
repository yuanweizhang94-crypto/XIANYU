Change ID: CHG-0008-xianyu-upstream-integration-foundation
Status: IMPLEMENTING
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

## Progress

Completed tasks: 5 / 9
Next task: T6 Execute local isolated P0 startup only after operator approves upstream runtime setup
