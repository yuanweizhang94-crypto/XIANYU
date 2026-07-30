Change ID: CHG-0016-local-only-manual-platform-verification-handoff
Status: IMPLEMENTING
# Proposal

## Title

Local-only manual platform verification handoff

## Problem

When the upstream IM Token API returns an official platform verification requirement, the system needs a local, owner-controlled handoff flow. The owner must complete the official verification in a visible local browser, with no automated page interaction and no remote solver, then the system may safely return to upstream native Token refresh.

The problem is not automatic slider solving. The problem is the lack of a pure manual handoff that preserves current upstream ownership of online chat, automatic reply, fixed-template reply, Token acquisition, and message sending.

## Goal

Design a local-only manual verification handoff that:

- Uses official platform verification pages only.
- Requires an authenticated owner action and second confirmation.
- Opens a visible local browser for the owner to operate manually.
- Does not move, click, drag, type, or solve the page automatically.
- Keeps the verification URL in local memory only with a maximum five-minute TTL and single-use semantics.
- Reads only the minimal expected Cookie delta after owner confirmation.
- Merges allowed Cookie fields through the upstream account service.
- Returns to upstream native online-chat and automatic-reply Token refresh.
- Never creates a new IM implementation, Token API implementation, WebSocket implementation, sender, or automatic reply executor.

## Non-goals

- No second UI, IM, Token, WebSocket, sender, or automatic-reply executor.
- No automated platform verification interaction.
- No dependency, Docker service, migration, or runtime configuration.
- No login, relogin, scheduler start, CHG-0010 worker start, Patchright, DrissionPage, real_mouse, remote solving, automated click, automated drag, automated keyboard input, message send, item/order/refund/shipping/rating operation, or unapproved live platform validation.
- No AI reply design or implementation.

## Upstream capability audit

Pinned upstream and latest upstream were audited before this DRAFT:

- Pinned upstream has automated captcha solving paths.
- Pinned upstream has no manual-only verification mode for the IM Token `FAIL_SYS_USER_VALIDATE` path.
- Latest upstream has no manual-only verification mode.
- Upstream Issues and PRs related to slider, Token, and verification were reviewed.
- Local historical research found no reusable manual bridge.

This implementation must preserve upstream-first ownership and must not use repeated local development to make validation appear successful.

## Pinned upstream evidence

- Pinned upstream path: `D:/xianyu-upstream-pilot`.
- Pinned upstream repository: `zhinianboke/xianyu-auto-reply`.
- Pinned upstream SHA: `bda1a859df63fa5f24e51398fa80a23490bb6dfc`.
- Latest upstream observed during audit: `fbeea7a09e616e6739bebd871c2c4647207ceefc`.
- Pinned upstream automated paths include Playwright, DrissionPage, real_mouse, and remote solver patterns.
- Pinned upstream online-chat and automatic-reply Token paths remain separate and must remain separate.

## Existing local implementation search

Local history and documents were searched after upstream evidence:

- No reusable pure manual verification bridge was found.
- CHG-0009 wrapper remains operations/diagnostics.
- CHG-0010 local autoreply worker remains frozen/deprecated and must not become a sender.
- CHG-0012 is archived with `BLOCKED_BY_PLATFORM_VERIFICATION_GAP`.

## Reuse decision

Decision: PATCH_UPSTREAM

The executable solution is a small auditable upstream patch for a default-off manual-only verification mode. CHG-0009 remains a `WRAP_FOR_OPERATIONS` lifecycle wrapper for starting and stopping the patched upstream listener on the local Windows host. The handoff must not replace upstream online chat, automatic reply, Token acquisition, WebSocket, fixed reply, or sender ownership.

## Duplicate implementation risk

Duplicate risk is high if this work creates:

- A second IM protocol implementation.
- A second Token API client.
- A second WebSocket implementation.
- A second sender.
- A second automatic reply executor.
- A browser automation solver.
- A remote verification service.
- A local Cookie vault.
- A direct database writer for account Cookie.

The design must prevent all of those paths.

## Why upstream cannot satisfy the requirement

Pinned upstream and latest upstream do not provide a pure manual local handoff for the IM Token platform verification path. Existing upstream paths are automated or remote-solving oriented and are outside the current safety authorization.

## Approved exception ADR

Not applicable. This Change uses `PATCH_UPSTREAM`, not `BUILD_LOCAL_EXCEPTION`.

## Component owner

- Online chat remains backend-web.
- Automatic reply remains upstream websocket.
- Fixed reply remains upstream websocket.
- Manual handoff is an operations wrapper and is not a sender.
- Manual handoff never receives customer messages.
- Cookie merge must go through the upstream account service.

## Retirement plan for overlapping local code

CHG-0010 local worker remains `FREEZE_AND_DEPRECATE`. This Change must not restore it, extend it, or use it as a message executor. Any future implementation must retire or keep disabled any overlapping local helper once upstream provides an equivalent manual handoff.
