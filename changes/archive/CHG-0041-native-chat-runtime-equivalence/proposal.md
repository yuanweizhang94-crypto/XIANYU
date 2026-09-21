# CHG-0041 Native Chat Runtime Equivalence

Change ID: CHG-0041-native-chat-runtime-equivalence
Status: ARCHIVED
Created: 2026-09-21
Owner task: account_enable_runtime_rehydration

## User Outcome

After an account is formally re-enabled, the already-existing Native WebSocket owner must be usable by Online Chat without a manual account restart, a second IM connection, or a full-stack restart.

## Production evidence

For enabled account 2219319284219, the formal account enable path called the existing WebSocket start owner at 2026-09-21 17:49:14. The Native owner was created immediately, matching registration ACK succeeded at 17:49:15, and message listening was ready at 17:49:16.

Starting at 17:49:20 the current Backend repeatedly called the shared-owner endpoints under /internal/accounts/2219319284219/chat/conversations and chat/messages. The running CHG0039 WebSocket image returned HTTP 404 because those routes were absent from that image.

The production-equivalent local WebSocket source already contains the Native Chat RPC methods and internal routes. The current CHG0039 runtime does not. Therefore the Native account runtime rehydration itself is already working; the remaining failure is WebSocket runtime baseline drift.

ROOT_CAUSE=WEBSOCKET_IMAGE_BASELINE_DRIFT_DROPPED_NATIVE_CHAT_RPC_WHILE_BACKEND_EXPECTS_SHARED_NATIVE_OWNER
FIRST_DIVERGENCE=ACCOUNT_ENABLE -> NATIVE_WS_START PASS -> TOKEN_READY PASS -> REGISTRATION_ACK PASS -> MESSAGE_LOOP_READY PASS -> BACKEND_NATIVE_CHAT_RPC -> WEBSOCKET_INTERNAL_ENDPOINT_404

## Scope

ALLOWED_CHANGE_SCOPE=current WebSocket Native owner Chat RPC methods and matching internal HTTP routes; deterministic tests; runtime-equivalence evidence; Change authority.
FORBIDDEN_CHANGE_SCOPE=Account enable handler, second WebSocket manager, second Chat manager, Scheduler, AutoReply rule engine, Publisher, catalog, reply configuration, CHG0038 registration semantics, CHG0039 invalidation semantics, CHG0040 QR Cookie enrichment.

## Development precheck

TASK_TYPE=REPAIR
FAILURE_REASON=current WebSocket production image is missing an already-existing local Native Chat RPC capability required by the current Backend shared-Native-owner architecture.
RESPONSIBLE_LAYER=XIANYU WebSocket runtime packaging/runtime equivalence.
CURRENT_UPSTREAM_CAPABILITY=MISSING_NATIVE_CHAT_RPC at pinned upstream origin/main fdc8eb039be771456ecfbbbe43fa26f57feb3947.
CURRENT_LOCAL_CAPABILITY=EXISTS in the production-equivalent recovery source.
CURRENT_RUNTIME_CAPABILITY=STALE_ONLY; CHG0039 runtime preserves CHG0038/CHG0039 but omits Native Chat RPC additions.
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=none; restore the existing local Native Chat RPC delta onto the current CHG0039 runtime preimage.
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=the current runtime image does not load the already-existing local RPC methods/routes.
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=No new implementation is allowed or required. This Change is runtime-equivalence restoration only.
NEW_IMPLEMENTATION_ALLOWED=false
FIX_CLASS=RUNTIME_EQUIVALENCE_RESTORATION

## Upstream capability audit

The public upstream is zhinianboke/xianyu-auto-reply. A fresh fetch attempt during this Change was blocked by a network connection reset. The locally fetched upstream origin/main fdc8eb039be771456ecfbbbe43fa26f57feb3947 was inspected directly and does not contain the Native Chat conversation/message internal routes used by the current local shared-owner Backend architecture.

## Pinned upstream evidence

UPSTREAM_REPOSITORY=zhinianboke/xianyu-auto-reply
UPSTREAM_COMMIT=fdc8eb039be771456ecfbbbe43fa26f57feb3947
UPSTREAM_FETCH_CURRENT_ATTEMPT=NETWORK_RESET
UPSTREAM_EQUIVALENT_FIX_EXISTS=false
UPSTREAM_GAP=no shared-Native Chat RPC route/method set matching current XIANYU Backend integration

## Existing local implementation search

The production-equivalent recovery source already contains:
- Native Chat bounded LWP request correlation on the existing XianyuAsync connection;
- conversation/history read methods;
- manual text/image/recall methods;
- matching internal HTTP routes that resolve the already-running account instance.

No second socket, Session owner, Token owner or Chat manager is needed.

## Why upstream cannot satisfy the requirement

The inspected upstream does not implement XIANYU's current local shared-Native Chat integration. Adopting upstream as-is would remove the local integration rather than restore the missing runtime capability.

## Approved exception ADR

Not applicable. This is PATCH_UPSTREAM against the current runtime overlay; no BUILD_LOCAL_EXCEPTION is requested.

## Reuse decision

Decision: PATCH_UPSTREAM

## Duplicate implementation risk

The restored methods use get_manager().instances and XianyuAsync.connection_manager.ws. They do not call websockets.connect and do not create another account worker or Chat lifecycle owner.

## Component owner

The existing XianyuAsync Native WebSocket instance remains the single upstream IM owner for Auto Reply and Online Chat. Backend remains a thin RPC consumer of that owner.

## Retirement plan for overlapping local code

Retire this local patch when upstream provides equivalent shared-Native Chat RPC behavior and XIANYU can adopt it without regressing CHG0038, CHG0039, CHG0040 or current production behavior.
