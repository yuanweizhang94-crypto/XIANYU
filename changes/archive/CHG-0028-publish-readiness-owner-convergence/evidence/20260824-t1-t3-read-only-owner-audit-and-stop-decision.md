# CHG-0028 T1-T3 read-only owner audit and stop decision — 2026-08-24

Status: APPROVED

Change ID: CHG-0028-publish-readiness-owner-convergence

## Result

```text
T1_READ_ONLY_OWNER_AUDIT=PASS
T2_DETERMINISTIC_LAZY_PENDING_REPRODUCTION=PASS
T3_REUSE_DECISION=PATCH_UPSTREAM
T3_EXECUTION_DECISION=STOP
STOP_CONDITION_TRIGGERED=NEW_READINESS_WRITER_OR_CONSUMER_CONTRACT_CHANGE_REQUIRED
IMPLEMENTATION_AUTHORIZED=false
NEW_IMPLEMENTATION_ALLOWED=false
PRODUCTION_FREEZE=true
BROWSER_SCOPE_INCLUDED=false
```

The approved Publisher-only audit found an existing point-in-time native capability producer, but no existing transition that writes its result into the readiness contract consumed by the Accounts status path. Enabling the newer upstream route alone cannot make that consumer converge. Persisting the result would add a readiness writer, while polling the native MTOP probe from account status would change the existing read-only/polling contract and can invoke the established Cookie update path after token refresh. Both require a separate project-owner decision under the approved stop conditions.

No Publisher, Session, QR, WebSocket, Scheduler, COMPANY adapter, Browser, frontend, or production account state was modified.

## Authority and revision lock

| Authority | Exact revision / identity | Result |
| --- | --- | --- |
| XIANYU current GitHub main | `dc83ef23603c1725d3babcd8f89f54db0592f075` | CHG0027 merge/main authority |
| CHG0028 local audit start | `c77533ccd83aa6e97a7b8bf2008229e810505f2f` | clean |
| CHG0028 remote branch | `c77533ccd83aa6e97a7b8bf2008229e810505f2f` | fresh-fetch equality confirmed before T1 |
| CHG0028 merge base | `dc83ef23603c1725d3babcd8f89f54db0592f075` | main-based |
| production-source upstream pin | `bda1a859df63fa5f24e51398fa80a23490bb6dfc` | detached source comparison only |
| freshly fetched upstream main | `29dc831d4498f3174f0502c989a352ef59815553` | current comparison authority |
| upstream native capability introduction | `5984b483b5bfd6c852ef00c22291b1bf163022ee` | selected-account capability route/service/UI |

The pinned production-source upstream commit does not contain `publish_account_capability_service.py` or `product_publish_capability.py`. Fresh upstream main contains both. Production Runtime contains the capability service, normal Direct/Personal Publisher routing, and the Accounts readiness consumer, but it does not contain the newer `product_publish_capability.py` route registration.

## Runtime identity

| Component | Running image | Image ID | Publisher-readiness audit result |
| --- | --- | --- | --- |
| Backend | `xianyu-chg0027-backend-web:session-transient-classification-20260824-r1` | `sha256:fcada4935126e1b46360a560c76a1449e37f65d1344ae05cf5e37ddeeed6bf3e` | native capability service and consumer present; no readiness writer |
| WebSocket | `xianyu-chg0023-websocket:readiness-contract-20260822-r1` | `sha256:107b15563eb1cd3fae1d9e577f89ec9304a6ef8f8984aed486bacfe718ac6256` | Session/Cookie owner paths only; no Publisher readiness record or writer |
| Scheduler | `xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1` | `sha256:ab70f051e962a3138103de969e6976e13c923da86d9222eabf2b9223394331e8` | Session task consumers only; no Publisher readiness record or writer |

The production frontend and authorized Browser are outside CHG0028 and were not inspected as acceptance gates. Current upstream Product Publish source was inspected only to trace the native selected-account capability workflow.

## Backend runtime source lock

| Runtime path | SHA256 | Git blob | Role |
| --- | --- | --- | --- |
| `/app/backend-web/app/api/routes/cookies.py` | `25405cab1ef1db5bbf7c9296d83f1201664c75f2a0651b90751d4b7804453ec1` | `034efa93831d04b6c67fca3ff70a396ee5d2a56c` | Accounts readiness consumer; exact CHG0027 accepted postimage |
| `/app/backend-web/app/services/publish_account_capability_service.py` | `702432eac538f4928927fb4a667b82d69b5cc6655e963e2baa01d79ea6685429` | `a7881c312add3d9da4fec41c059723b6a6692c69` | native point-in-time `preget` producer |
| `/app/common/services/xianyu_publish_service.py` | `a04961f1ae60e992560a19342f14e013e0ed4658c35b8240b0609767a80c5711` | `6e0fa5957e973aa075bf4361d347e4c4eac3ae42` | service loader and Direct/Personal routing |
| `/app/common/services/publish_execution_service.py` | `02943d7e3d76d1b567bc6cf2a776ad031ebf77d50ba51e99f36d60314847bf36` | `0c115aa44c13aa20fb6fc449e41f63ace3c77878` | normal publish execution consumer |
| `/app/common/utils/cookie_refresh.py` | `6a376efa08589bc91d53ad7f4c696c4a0acf453e5d5cf3ad40bd8f3754f9ba97` | `a2c560aa94fa7c612c8edd8b503701f9c0c54c92` | canonical Session/Cookie metadata writer; does not create Publisher readiness |

After line-ending normalization, the deployed `publish_account_capability_service.py` is byte-equivalent to freshly fetched upstream main: normalized SHA256 `f24c041f0631a00cedb7560b44eeea27899036c87b6c1e5d487ed9bb7d542372`.

## Existing producer and consumer ownership map

| Stage | Existing owner and path | Produced/consumed truth | Audit finding |
| --- | --- | --- | --- |
| Native Publisher capability probe | Backend `PublishAccountCapabilityService.detect` | calls `mtop.idle.pc.idleitem.preget`; returns success, account-invalid classification, seller type, SKU/inventory support, commission configuration, and latest Cookie | authoritative point-in-time capability evidence exists |
| Normal Publisher execution | `detect_publish_account_capability -> XianyuDirectPublisher / XianyuPersonalPublisher` | selected-account routing immediately before normal MTOP publish | existing owner remains correct; no Browser gate |
| Current upstream selected-account UI/API | GET `/product-publish/accounts/{account_id}/capability` plus `ProductPublish.tsx` account selection | keeps successful capability in frontend component state and prevents submit until it exists | exists on fresh upstream main only; does not emit or persist `READY` into Accounts status |
| Accounts readiness consumer | Backend `cookies.py::_build_business_capabilities` | reads `metadata_json.session_maintenance.consumers.publish`; only `state == READY` emits outward `READY` | deployed and deterministic; no producer writes its expected record |
| Session/Cookie metadata | Backend/WebSocket/Scheduler `set_session_maintenance_state` and `mark_cookie_update_session_pending` | writes canonical Session state and Cookie lineage | replacement record contains no Publisher consumer; QR success intentionally leaves Publisher lazy |
| COMPANY adapter | `xianyuAccountStatus` in `runtime/devspace_proxy/proxy.cjs` | reads sanitized account details and returns login/account booleans | thin consumer only; no Publisher readiness producer or duplicate business state |

Bounded source searches found `consumers` only in the Backend consumer and the explicit QR comment that Publisher consumers remain lazy. No `publish_auth_readiness`, `publish_preflight_active`, or Publisher consumer record exists in the WebSocket or Scheduler source trees.

## T2 deterministic reproduction

The deployed Backend function was invoked with synthetic in-memory account objects only. It made no HTTP, database, publish, QR, Browser, message, or account calls.

| Synthetic input | Deterministic outward Publish result |
| --- | --- |
| Session `REAL_BROWSER_LOGIN_READY`; no `consumers.publish` record | `RETRY_LATER`, reason `session_check_pending_no_active_check` |
| Same Session plus synthetic existing-contract `consumers.publish.state=READY` | `READY`, source `publish_auth_readiness` |
| Session `HUMAN_QR_REQUIRED` | `QR_REQUIRED`, source `canonical_browser_session` |

The native service was separately exercised with a mocked `mtop_call`:

- mocked native success returned seller/capability fields with `success=true`;
- mocked transient failure returned `success=false`, `account_invalid=false`;
- neither path touched Session metadata or produced `consumers.publish`.

This reproduces the exact missing transition without real Publisher or production mutation:

```text
detect_publish_account_capability success
-> MISSING TRANSITION
-> session_maintenance.consumers.publish.state=READY
-> cookies.py outward READY
```

CHG0027's accepted read-only matrix independently observed the production symptom: five enabled accounts with `REAL_BROWSER_LOGIN_READY`, Auto Reply `ONLINE`, Chat `SUCCESS`, and Publisher `LAZY_PENDING`.

## Why direct adoption or configuration is insufficient

1. Fresh upstream main's selected-account capability route is an ephemeral native probe. It does not update the deployed Accounts readiness contract.
2. The production Backend lacks that newer route, but activating the route alone still leaves `cookies.py` reading an unwritten `consumers.publish` record.
3. Calling `preget` from the Accounts four-second polling path is not the upstream-native selected-account workflow. It would fan out open-world MTOP calls and, after token refresh, can invoke the existing canonical Cookie update path.
4. Normal real publish already calls the probe, but real publish is not an acceptable readiness probe and is explicitly prohibited for CHG0028 acceptance.
5. QR must remain lazy and Browser-independent; it cannot become the Publisher readiness trigger.
6. No configuration connects the point-in-time result to the consumed state.

Therefore `ADOPT_UPSTREAM` and `CONFIGURE_UPSTREAM` do not satisfy the existing Accounts contract as-is. A `PATCH_UPSTREAM` continuation must choose one of two materially different contracts: add one lineage-aware readiness projection writer in the existing Backend owner, or retire/replace the global persisted readiness contract in favor of explicit selected-account on-demand capability. That choice is outside the approved no-new-writer/no-contract-expansion boundary.

## T3 decision

```text
REUSE_DECISION=PATCH_UPSTREAM
EXECUTION_DECISION=STOP
ADOPT_UPSTREAM_AS_IS=INSUFFICIENT
CONFIGURE_UPSTREAM=NOT_AVAILABLE
PATCH_UPSTREAM_WITHIN_APPROVED_BOUNDARY=false
NEW_OWNER_REQUIRED=false
NEW_READINESS_WRITER_OR_CONTRACT_DECISION_REQUIRED=true
BUILD_LOCAL_EXCEPTION_AUTHORIZED=false
T4_IMPLEMENTING_BLOCKED=true
NEXT_SINGLE_ACTION=STOP__RETURN_TO_PROJECT_OWNER_FOR_SEPARATE_BACKEND_READINESS_CONTRACT_DECISION
```

This stop is the accepted outcome defined by CHG0028. It does not reopen CHG0026 or CHG0027 and does not classify Publisher business execution as broken. The normal Direct/Personal Publisher remains production-validated and Browser-independent.

## Development precheck

```text
DEVELOPMENT_PRECHECK
TASK_TYPE=REPAIR
FAILURE_REASON=ACCOUNTS_READINESS_CONSUMER_EXPECTS_UNWRITTEN_PUBLISH_RECORD
RESPONSIBLE_LAYER=XIANYU_BACKEND_EXISTING_PUBLISH_CAPABILITY_AND_ACCOUNT_STATUS_OWNERS
CURRENT_UPSTREAM_CAPABILITY=PARTIAL__POINT_IN_TIME_SELECTED_ACCOUNT_PRODUCER_EXISTS__NO_ACCOUNTS_STATE_TRANSITION
CURRENT_LOCAL_CAPABILITY=GOVERNANCE_ONLY__NO_PARALLEL_RUNTIME_OWNER
CURRENT_RUNTIME_CAPABILITY=PRODUCER_SERVICE_PLUS_CONSUMER_PRESENT__NO_READINESS_WRITER
CONFIGURATION_ISSUE=false
SESSION_OR_DATA_ISSUE=false
OFFICIAL_PLATFORM_LIMITATION=false
MINIMAL_EXISTING_FUNCTION_TO_CHANGE=BLOCKED_PENDING_OWNER_CHOICE_OF_PERSISTED_PROJECTION_VS_ON_DEMAND_CONTRACT
WHY_EXISTING_FUNCTION_CANNOT_BE_REUSED_AS_IS=PRODUCER_RESULT_IS_EPHEMERAL_AND_CONSUMER_REQUIRES_AN_UNWRITTEN_RECORD
WHY_NEW_IMPLEMENTATION_IS_REQUIRED=NOT_ESTABLISHED__SEPARATE_CONTRACT_DECISION_REQUIRED_FIRST
NEW_IMPLEMENTATION_ALLOWED=false
```

## Safety counters

```text
REAL_MESSAGES_SENT=0
REAL_PRODUCTS_PUBLISHED=0
REAL_PRODUCTS_MODIFIED=0
NEW_ITEM_SYNC_INVOCATION_COUNT=0
QR_LOGIN_INVOCATION_COUNT=0
MANUAL_RECONNECT_INVOCATION_COUNT=0
PRODUCTION_ACCOUNT_MUTATION_COUNT=0
PRODUCTION_CONTAINER_RESTART_OR_REPLACEMENT_COUNT=0
PRODUCTION_RUNTIME_CONFIGURATION_MUTATION_COUNT=0
COMPANY_SOURCE_MUTATION_COUNT=0
BROWSER_INVOCATION_COUNT=0
```

The synthetic Python imports initialized existing modules and emitted ordinary initialization logs only. No external capability probe, database operation, or production business operation was invoked.

## Governance verification

```text
CHG0028_ACCEPTANCE_TESTS=7/7_PASS
GENERATED_STATE_REGRESSION=9/9_PASS
RUFF_CHG0028=PASS
SECURITY_SCAN=PASS
DUPLICATE_CAPABILITY_VALIDATION=PASS
GIT_DIFF_CHECK=PASS
VALIDATE_CHANGE=PRE_EXISTING_BLOCKED__CHG0020_MISSING_ARCHIVED_DESIGN_AND_TASKS
VERIFY_REPOSITORY=PRE_EXISTING_BLOCKED__CHG0020_MISSING_ARCHIVED_DESIGN_AND_TASKS
NEW_CHG0028_VALIDATION_FAILURES=0
```

The repository-wide validation commands stop only on the already-recorded CHG0020 archive debt. This Change does not fabricate missing historical files or absorb that unrelated scope.

## Selected read-only audit IDs

```text
CHG0028_REMOTE_EQUALITY_AUDIT=d521cfcbfe0f
RUNTIME_CONTAINER_LIST_AUDIT=be761b16904b
BACKEND_RUNTIME_HASH_AUDIT=5aa0d0bf7489
BACKEND_WRITER_SEARCH_AUDIT=94f7f3a1a701
WEBSOCKET_WRITER_SEARCH_AUDIT=fceb3b1839e9
SCHEDULER_WRITER_SEARCH_AUDIT=d45719da773c
DETERMINISTIC_CONSUMER_REPRO_AUDIT=061d48bb74f3
MOCKED_NATIVE_PRODUCER_AUDIT=7b08871f95c2
```
