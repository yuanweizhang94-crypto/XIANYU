# CHG-0026 Proposal

Status: VERIFYING

Change ID: CHG-0026-qr-dual-mode-and-chat-connectivity-recovery

## User outcome

Restore two explicit QR workflows without weakening CHG0025 recovery safety, and make Accounts/Online Chat show the authoritative difference between authentication blockers and connection blockers. Wang must not be rescanned; Zhou must not be told to scan merely because Chat is disconnected.

## Confirmed blocker

1. CHG0025 intentionally removed the upstream unbound add-account QR entry while making existing-account recovery target-strict, so the upstream add-account QR workflow is no longer reachable from the Accounts UI.
2. Accounts readiness can report Auto Reply ONLINE from stale `connected+token_ready` even when canonical Session maintenance is `SESSION_RENEW_FAILED`.
3. `/chat-new/accounts` exposes only Chat-manager `connected` and omits canonical Session/HUMAN_QR/platform blockers, so refresh collapses distinct failures into generic disconnected state.

## Minimal intervention

Patch the existing upstream QR route with immutable server-side mode metadata, restore the existing add-account QR entry, preserve the CHG0025 recovery path unchanged in safety semantics, and enrich existing account/chat status adapters with canonical blocker precedence. Reuse the existing QR manager, AccountService, WebSocket owner, and Chat IMSessionManager.

## Smallest success test

Deterministically prove both QR modes are immutable and isolated, recovery mismatch remains pre-write fail-closed, add-new preserves same-owner update/create semantics while rejecting cross-owner identity reuse, and Chat/account status renders auth/session/connection truth without starting a new QR or second WebSocket owner.

## Stop condition

Stop on any need for real QR creation/scan, global account restart, Item Sync, new WebSocket/Chat owner, Cookie validation-core rewrite, Session schema change, or unknown side effect. Accidental same-image Backend restarts observed during acceptance are execution-discipline deviations, not authorization to repeat them; the affected acceptance generations are invalidated and recorded in final evidence.

## Upstream capability audit

Pinned upstream `zhinianboke/xianyu-auto-reply` already provides QR generation/status, add-account QR upsert, WebSocket start/restart, Online Chat `IMSessionManager`, and account status surfaces. The defect is local composition/regression, not missing owners.

## Pinned upstream evidence

Pinned checkout: `D:/xianyu-upstream-pilot` at `bda1a859df63fa5f24e51398fa80a23490bb6dfc`. Relevant paths: `backend-web/app/api/routes/qr_login.py`, `backend-web/app/services/account_service.py`, `backend-web/app/api/routes/chat_new.py`, `backend-web/app/services/chat_new/im_session_manager.py`, `frontend/src/pages/accounts/Accounts.tsx`, `frontend/src/pages/chat-new/ChatNew.tsx`. Native QR behavior is same-owner UPDATE_EXISTING by `unb`, otherwise CREATE_NEW.

## Existing local implementation search

Current production CHG0025 already has target-scoped recovery, identity pre-write guard, false-green prevention after recovery protocol success, account readiness aggregation, and latest-upstream Chat runtime. These owners will be patched, not duplicated.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

High if a second QR owner, WebSocket manager, Chat readiness truth, Session renewer, or add-account implementation is introduced. All are forbidden.

## Why upstream cannot satisfy the requirement

The pinned native add-account QR path exists, but directly restoring it would omit CHG0025 mode isolation and could create a second-owner duplicate identity when the scanned `unb` already belongs to another XIANYU user. The current local status composition also has post-upstream readiness contracts that need a minimal compatibility patch.

## Approved exception ADR

Not applicable; no `BUILD_LOCAL_EXCEPTION` is used.

## Component owner

Existing XIANYU upstream-derived Backend QR/Account/Chat routes and existing Frontend Accounts/Online Chat pages. WebSocket and Chat session execution owners remain unchanged.

## Retirement plan for overlapping local code

No parallel component is created. The dual-mode compatibility layer remains only while local CHG0025 strict recovery differs from upstream; if upstream gains equivalent immutable dual-mode safety, review this patch for retirement.

## Allowed change scope

- existing QR route and minimal AccountService ownership lookup if required
- existing account readiness/status adapter
- existing Chat accounts/status adapter
- existing Accounts QR UI/API/types
- existing Online Chat status UI/API/types
- deterministic tests, evidence, locked vendor patch and governance metadata

## Forbidden change scope

Item Sync, Publisher, Scheduler, Session DB schema, Cookie validation core, a second QR/WebSocket/Chat owner, global account restart, automatic QR creation/scan, password login, or unrelated governance debt repair.

## Final accepted correction chain

- R3: platform-verification status now requires account-scoped explicit evidence; stale persisted verification cannot override newer settled healthy Session truth.
- R4: bare `SESSION_CHECK_PENDING` outranks WebSocket/token green and renders as checking rather than false ONLINE/PVR/connection failure.
- R5: the existing `ImSessionManager` observes bounded startup Session convergence and performs exactly one cached-token-only `runtime_only=True` Chat rehydration when an initially transitional account becomes auth-valid; authoritative blockers remain skipped.
- No new QR/WebSocket/Chat/Session/Cookie/Token owner was introduced.
- Production acceptance completed with zero CHG0026 executor QR create/scan and zero Chat-lifecycle auth writes.
