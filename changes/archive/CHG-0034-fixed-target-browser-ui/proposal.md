# CHG-0034 Fixed Target Browser UI

Change ID: CHG-0034-fixed-target-browser-ui
Status: ARCHIVED
Created: 2026-08-25
Owner task: chg0034_single_writer

## User Outcome

User outcome: authorized Browser reliably loads and visually validates the fixed local XIANYU frontend at `http://127.0.0.1:19000/` across the required pages without platform actions or secret exposure.

Confirmed blocker: prior browser remained in stale SPA context; fresh document load, auth handoff, same-origin API/WebSocket and visible page state must be proven, and any XIANYU/COMPANY source drift must be classified.

Smallest success test: fixed target HTTP 200, nonblank fresh bundle, no fatal console errors, authorized API/WS visible, required account/item/chat/AI/service pages render with masked screenshots.

## Scope

Allowed before commander Browser action:

- isolated worktree work under `D:/xianyu-worktrees/CHG-0034-fixed-target-browser-ui`;
- active Change governance/evidence creation and generated state via `python scripts/generate_state.py`;
- read-only inspection of prior CHG-0033 closure, frontend/backend/WS runtime state, source and runtime asset hashes, cache headers, nginx/API/WS/auth-sync contracts, and deterministic test/build commands;
- read-only discovery of the actual clean COMPANY source root/remote and dirty fingerprints if COMPANY source drift may be involved;
- readiness checkpoint for a separate commander-owned Browser action.

Forbidden before explicit later authorization:

- modifying `D:/xianyu` or any existing COMPANY dirty checkout;
- controlling Browser, Chrome, platform UI, QR, reconnect, sync, publish, send, AI enablement, account mutation, deployment, commit, or push;
- printing Cookie, Token, JWT, Authorization, API key, password, browser Profile secret, customer content, full account IDs, or unmasked screenshots;
- editing installed proxy/runtime files or COMPANY source.

## Current Gate State

`FIXED_TARGET_URL=http://127.0.0.1:19000/`

`COMMANDER_OWNS_BROWSER_ACTION=true`

`BROWSER_INVOCATIONS_ALLOWED=false`

`PLATFORM_ACTIONS_ALLOWED=false`

`DEPLOY_ALLOWED=false`

`COMMIT_ALLOWED=false`

`PUSH_ALLOWED=false`

`PRODUCTION_MUTATION_ALLOWED=false`

`SECRET_EXPOSURE_ALLOWED=false`

## Final Outcome

`FIXED_TARGET_BROWSER_UI_ACCEPTANCE=PASS_WITH_NONFATAL_CHART_WARNINGS`

`USER_AUTHENTICATED_SESSION_AVAILABLE=true`

`NO_BUSINESS_CODE_DEFECT_PROVEN=true`

`BUSINESS_RUNTIME_PATCHES=0`

`CAPTCHA_BYPASS_ATTEMPTS=0`

`SECOND_OWNER_CREATED=false`

The authorized Browser validation first proved a fresh, nonblank login document at `http://127.0.0.1:19000/` with title `闲鱼自动回复管理系统`. A third-party Geetest network-timeout checkpoint was observed within one human-authorized, unrefreshed CAPTCHA challenge; it remains chronological evidence and was not a credential failure. On 2026-08-26 the user made an authenticated session available in the existing Browser tab. Read-only validation then passed across dashboard, accounts, selected-account detail, items, publish logs, online chat, auto reply, and scheduled tasks/service status. Two nonfatal dashboard chart dimension warnings remained, with no fatal console errors and no business or platform write. No business/runtime code patch or second execution owner was required.

## Upstream Capability Audit

The required capability is operational validation of the already-deployed upstream-native XIANYU web UI and its same-origin API/WebSocket/auth handoff. CHG-0034 must inspect the upstream/local owner paths and runtime contracts before proposing any patch.

## Pinned Upstream Evidence

Pinned baseline for this Change is `origin/main` at `41b3a527a06d85d77d46bccba2780ff080504936`, containing CHG-0033 closure. Runtime/source readiness must record exact source paths, runtime image identifiers, asset hashes, and header/API/WS evidence discovered during read-only checks.

## Existing Local Implementation Search

Search is limited to archived CHG-0030 through CHG-0033 records, local frontend/backend/WS source owners, build artifacts, nginx/proxy config, auth-sync contracts, and installed runtime metadata needed to determine whether the deployed target already contains the fixed assets.

## Reuse Decision

Decision: WRAP_FOR_OPERATIONS

CHG-0034 does not create a new frontend, API, WebSocket owner, auth owner, Browser owner, or platform executor. It prepares an operations-only readiness checkpoint for the existing deployed target and commander-owned Browser validation.

## Duplicate Implementation Risk

Risk is low while the Change remains read-only and uses the existing deployed runtime. Risk becomes high if it creates a parallel frontend build owner, proxy, auth/session bridge, API/WS route owner, Browser automation owner, or platform action path.

## Why Upstream Cannot Satisfy The Requirement

Upstream supplies the UI/API/WS/auth workflow. It does not by itself prove this local fixed target is fresh in Browser, mapped to the current runtime assets, same-origin authorized, and visually ready for commander validation.

## Approved Exception ADR

Not applicable. `BUILD_LOCAL_EXCEPTION` is not authorized.

## Component Owner

The component owner remains the existing upstream-native XIANYU frontend/backend/WebSocket/auth deployment. CHG-0034 owns only read-only evidence and commander Browser handoff instructions.

## Retirement Plan For Overlapping Local Code

No overlapping production code is added.
