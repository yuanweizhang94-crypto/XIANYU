# CHG-0034 Design

Change ID: CHG-0034-fixed-target-browser-ui
Status: ARCHIVED

## Execution Contract

User outcome: authorized Browser reliably loads and visually validates the fixed local XIANYU frontend at `http://127.0.0.1:19000/` across the required pages without platform actions or secret exposure.

Confirmed blocker: prior browser remained in stale SPA context; fresh document load, auth handoff, same-origin API/WebSocket and visible page state must be proven, and any XIANYU/COMPANY source drift must be classified.

Smallest success test: fixed target HTTP 200, nonblank fresh bundle, no fatal console errors, authorized API/WS visible, required account/item/chat/AI/service pages render with masked screenshots.

## Read-Only Phase Design

The current phase creates a real active Change and prepares a commander handoff. It must not control Browser or mutate any platform/runtime/source state.

Required evidence:

- `origin/main` equals `41b3a527a06d85d77d46bccba2780ff080504936`;
- CHG-0033 is archived on the baseline and CHG-0034 is the only active Change;
- active Change exists under `changes/active/CHG-0034-fixed-target-browser-ui`;
- `generated/PROJECT_STATE.json` identifies CHG-0034 and its next pending task;
- fixed target `http://127.0.0.1:19000/` returns HTTP 200 with no-cache or deterministic freshness headers recorded;
- frontend document and bundle are nonblank and hashable from source and runtime;
- backend API and WebSocket runtime surfaces are same-origin reachable or the exact pre-browser blocker is recorded;
- auth handoff contract is identified without printing secrets;
- required commander pages/routes are enumerated;
- any XIANYU or COMPANY source-vs-runtime drift is classified without modifying COMPANY source or installed proxy.

## Commander Handoff Design

Commander Browser validation, when later authorized by the commander, should use a fresh document load of the fixed target and collect masked screenshots only after confirming HTTP 200, nonblank bundle, no fatal console errors, authorized API visibility, and WebSocket visibility.

## Final Acceptance Design

The final acceptance record closes CHG-0034 as `PASS_WITH_NONFATAL_CHART_WARNINGS`. The controlled Browser path remains the existing upstream-native UI. CHG-0034 records only sanitized observations:

- fixed-target runtime and asset readiness;
- fresh Browser document load and pre-CAPTCHA clean console state;
- human-authorized Geetest slider interaction;
- post-third-party-captcha visible network timeout and one empty console error with no attributable app stack/text as a superseded chronological checkpoint;
- a user-available authenticated session, not an agent-created session;
- read-only validation of dashboard, accounts, selected-account detail, items, publish logs, online chat, auto reply, and scheduled tasks/service status;
- two nonfatal dashboard chart dimension warnings, no fatal console errors, and no business or platform mutation.

This closure does not patch frontend, backend, WebSocket, login, auth, CAPTCHA, sender, account, item, chat, auto-reply, or platform code. The rollback is removal of the CHG-0034 archived evidence/test record from a future revert commit; no runtime rollback is required.

## Upstream Capability Audit

Pinned upstream/local owners must be searched before any design expansion. The decision order remains: adopt upstream, configure upstream, patch upstream, wrap for operations, then build local exception only with explicit approval.

## Pinned Upstream Evidence

Pinned baseline: `origin/main` at `41b3a527a06d85d77d46bccba2780ff080504936`.

## Existing Local Implementation Search

Local searches are limited to archived CHG-0030 through CHG-0033 evidence, frontend source/build owners, nginx/proxy config, backend API routes, WebSocket/auth-sync contracts, and runtime metadata needed for readiness.

## Reuse Decision

Decision: WRAP_FOR_OPERATIONS

## Duplicate Implementation Risk

No duplicate frontend, API, WebSocket, auth, Browser, sender, or deployment path may be introduced.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the UI/API/WS/auth workflow but not this local freshness and commander-readiness proof.

## Approved Exception ADR

Not applicable.

## Component Owner

Existing deployed XIANYU frontend/backend/WebSocket/auth owners.

## Retirement Plan For Overlapping Local Code

No overlapping production code is added.
