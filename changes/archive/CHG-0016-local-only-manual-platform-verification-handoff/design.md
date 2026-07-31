Change ID: CHG-0016-local-only-manual-platform-verification-handoff
Status: ARCHIVED
# Design

## Scope

This Change implements a local-only manual platform verification handoff as a default-off upstream patch plus a CHG-0009 operations wrapper.

The intended runtime owner split is:

- backend-web owns online chat.
- upstream websocket owns automatic reply and fixed-template reply.
- upstream account service owns Cookie merge.
- the manual handoff owns only local verification task lifecycle and owner-controlled handoff.

## Deployment topology questions

An executable Change must answer these before implementation:

1. Whether backend-web runs inside a container or on the Windows host.
2. Whether websocket runs inside a container.
3. Whether any browser started inside a container can be displayed to the project owner.
4. Whether the existing launcher can carry a one-time local task.
5. Whether a loopback-only local control channel already exists.
6. Whether safe browser process lifecycle management already exists.
7. How upstream account service safely merges Cookie fields.
8. How verification URL remains memory-only.
9. How the visible page is only available to the local owner.
10. How temporary browser profile deletion is guaranteed.

Do not assume a Docker container can directly open a Windows desktop browser.

Candidate owner evaluation order:

A. Reuse an existing Windows launcher for a one-time local helper.
B. Reuse an existing host-side operational wrapper.
C. Add the smallest auditable manual handoff hook to upstream.
D. Add a new local helper only as the last option.

## State machine

Required states:

- `IDLE`: no task exists; only authenticated owner may create one.
- `REQUESTING_VERIFICATION`: upstream native Token response produced an official verification URL; no URL is persisted.
- `READY_FOR_OWNER`: sanitized task exists; owner can open or cancel.
- `BROWSER_OPEN`: visible local browser is open at the official URL.
- `WAITING_FOR_OWNER`: program observes only close/redirect/expected Cookie appearance; no page interaction.
- `OWNER_CONFIRMED`: owner clicked "completed verification" in local UI.
- `VERIFYING_COOKIE_DELTA`: expected Cookie delta is read from the temporary browser profile.
- `COOKIE_MERGED`: allowed fields were merged through upstream account service.
- `TOKEN_REFRESH_PENDING`: native online-chat and automatic-reply Token refresh may each run once.
- `COMPLETED`: task closed; temporary browser profile removed.
- `CANCELLED`: owner cancelled; cleanup required.
- `EXPIRED`: TTL elapsed; cleanup required.
- `FAILED`: known failure; cleanup required.

Any unknown state is `FAIL_CLOSED`.

Each implemented state must document who can enter, who can exit, allowed operations, timeout, audit events, cleanup, and whether retry is allowed.

## Task initiation

Requirements:

- Only a logged-in user can actively click "start manual verification".
- User may operate only accounts they own.
- Admin delegation requires explicit audit.
- One account at a time.
- One task at a time.
- Account alias may be shown; Cookie must not be shown.
- Second confirmation is required.

## Verification URL

Requirements:

- Obtained only from upstream native Token response.
- Not stored in database.
- Not written to logs.
- Not written to files.
- Not written to Git.
- Not returned to remote clients.
- Memory-only.
- TTL maximum five minutes.
- Single use.
- Expiry cancels the task and must not refresh indefinitely.

## Browser behavior

Allowed program behavior:

- Open the official URL.
- Observe whether the page closes or redirects.
- Observe whether expected official Cookie fields appear.
- After owner clicks "completed verification", read the Cookie delta.
- Close browser after timeout/cancel/complete.

Forbidden program behavior:

- Mouse movement.
- Keyboard input.
- Click.
- Drag.
- Automation trajectory injection.
- Playwright `solve_slider`.
- DrissionPage solver.
- real_mouse.
- remote solver.
- Arbitrary URL navigation.

Browser requirements:

- Visible browser.
- Local owner performs the verification.
- Temporary isolated profile.
- Official verification host allowlist.
- Profile closed and deleted after completion.

## Live Defect Repair

Controlled owner validation exposed
`MANUAL_VERIFICATION_REPEATED_BROWSER_LAUNCH`.

Root causes:

- `AUTO_START_WEBSOCKET_NOT_DISABLED`.
- `EXISTING_X5_COOKIE_FALSE_SUCCESS`.
- `MANUAL_BROWSER_NOT_SINGLE_SHOT`.
- `MANUAL_LISTENER_LOGS_DISCARDED`.

Repair boundary:

- Keep CHG-0016 in `IMPLEMENTING`.
- Do not restart live validation until fake-browser, static, and repository
  tests pass and the repair PR is merged.
- Force host manual-listener startup to set `AUTO_START_WEBSOCKET=false`.
- Enforce process-wide one-shot manual browser launch state:
  `IDLE/RUNNING/SUCCEEDED/FAILED/TIMED_OUT/CANCELLED/CONSUMED`.
- Require exact new or changed `x5sec` after the page leaves the
  verification/punish state.
- Retry upstream native Token once after manual success. If the platform still
  requires verification, set `manual_verification_not_accepted` and fail closed
  without opening another browser.
- Store only sanitized local listener logs under the ignored path
  `D:/xianyu/.local/logs/CHG-0016-manual-listener.log`.

## Cookie merge

Requirements:

- Do not replace the entire account Cookie.
- Merge only new fields created by this browser task.
- Use upstream account service.
- Do not write directly to the database.
- Do not output values.
- Do not preserve browser Cookie files.
- Require account row ID and owner scope.
- Block wrong-account writes.
- Record field count only, not field contents.
- Fail if expected official verification Cookie fields are absent.

Initial allowlist must be based on upstream code evidence. Default candidates are `x5sec` and related `x5*` risk-control fields only. Do not expand to all Cookie fields without evidence.

## Token recovery

The handoff must not generate an IM Token.

After successful Cookie merge:

1. Close the manual verification task.
2. Let online chat run its native Token request once.
3. Let online chat write only its own `chat_{unb}` cache.
4. Let automatic reply run its native Token request once.
5. Let automatic reply write only its own `unb` cache.
6. Keep both caches isolated.
7. Do not copy Token values.
8. Do not send messages.

## API shape

Potential endpoints, subject to current repository API style:

- `POST /manual-verification/tasks`
- `GET /manual-verification/tasks/{opaque_id}`
- `POST /manual-verification/tasks/{opaque_id}/open`
- `POST /manual-verification/tasks/{opaque_id}/complete`
- `POST /manual-verification/tasks/{opaque_id}/cancel`

Constraints:

- Opaque random task ID.
- Account ID alone is not authorization.
- Owner scope.
- CSRF/auth.
- Loopback restriction for browser open.
- Rate limit.
- One active task per account.
- No raw URL response.
- No secret response.
- No arbitrary URL input.
- No user-provided Cookie input.
- Sanitized audit events.

## Minimal UI design

Possible entry points:

- Account management.
- Pending verification task in risk-control logs.

The UI may show:

- `ACCOUNT-A` or account remark.
- Verification type.
- Created time.
- Remaining TTL.
- Current state.
- "Open official verification page on this computer".
- "I completed verification".
- "Cancel".

The UI must not show:

- Cookie.
- Token.
- Device ID.
- Complete verification URL.
- Punish parameters.
- Raw platform response.

## Upstream capability audit

The design follows the upstream-first audit order now enforced by governance:

1. Product and upstream capability matrix.
2. Pinned upstream implementation.
3. Latest upstream changes.
4. Local history only after upstream insufficiency is proven.

## Pinned upstream evidence

See `evidence/upstream-audit.md`.

## Existing local implementation search

Local historical search found no reusable manual bridge. Existing local worker paths remain non-owners for live sending.

## Reuse decision

Decision: PATCH_UPSTREAM

The upstream patch is recorded at `vendor/patches/xianyu-auto-reply/bda1a85-manual-only-verification.patch`.
The local wrapper only manages the host process lifecycle for the patched upstream websocket listener.

## Duplicate implementation risk

The primary duplicate risk is introducing a second business executor while trying to solve a verification handoff problem. This design forbids creating IM, Token, WebSocket, sender, automatic reply, AI reply, or message receiving code.

## Why upstream cannot satisfy the requirement

Existing upstream paths automate the verification or call remote services. They do not provide the local owner-only manual handoff required by the CHG-0012 safety closeout.

## Approved exception ADR

Not applicable. No build exception is requested.

## Component owner

Manual handoff is an operations wrapper. Upstream remains the business runtime owner.

## Retirement plan for overlapping local code

Any future helper must be temporary, local-only, and retired or disabled if upstream later provides a native manual handoff.

## Blocked closeout

User outcome: Close CHG-0016 honestly after the approved owner-only platform
verification attempt was not accepted.
Confirmed blocker: The live manual verification ended with
`MANUAL_VERIFICATION_NOT_ACCEPTED`; no successful `x5sec` handoff was proven.
Smallest success test: Archive the Change with T12 blocked, T13 complete,
failure evidence preserved, generated state showing no active Change, and no
runtime or message side effects.

The closed design conclusion is that the manual handoff remains an
operations-only safety capability. It does not prove production automatic reply
delivery, AI reply, keyword reply, default reply, online-chat business matrix,
or customer messaging.
