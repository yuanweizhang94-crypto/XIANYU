# CHG-0031 Acceptance

Change ID: CHG-0031-controlled-real-publish-yilong
Status: ARCHIVED

## Required Phase 1 Acceptance

- CHG-0031 is the only active Change in the isolated worktree.
- The Change records the three-line execution contract:
  - User outcome: safely publish exactly one real sellable existing material through the existing unique upstream-native owner to the uniquely identified account labeled 艺龙 and keep it online.
  - Confirmed blocker: exact selected-account publish capability and one non-duplicate production-ready material must be proven; any trace/durable-truth gap must fail closed.
  - Smallest success test: one invocation, one platform item ACTIVE, local durable truth and remote/readback match, account item count +1, zero duplicate/extra items.
- `REAL_PUBLISH_ALLOWED=false` until the commander later sends exact `GO_FOR_REAL_PUBLISH`.
- `FRESH_ITEM_SYNC_INVOCATIONS=0`.
- No Cookie/Token/JWT/Authorization/password/API key/private key/Profile secret/customer content/full account ID is printed or committed.
- No publish, message, Browser, reconnect, QR, account edit, item edit, offline, delete, AI enablement, credential access, Fresh Item Sync, deploy, commit, or push occurs in this correction step.

## Current Gate State

`COMMANDER_GO_FOR_REAL_PUBLISH=false`

`REAL_PUBLISH_ALLOWED=false`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`REAL_PRODUCTS_PUBLISHED=0`

`PRODUCTION_MUTATION_COUNT=0`

`PREFLIGHT_T6_EXECUTED=true`

`EXACT_LABEL_COUNT_FOR_APPROVED_LABEL=0`

`EXACT_LABEL_REQUIRED_COUNT=1`

`MASKED_ACCOUNT_ROW_EXISTS=true`

`MASKED_ACCOUNT=280***247`

`MASKED_ACCOUNT_STATUS=active`

`MASKED_ACCOUNT_COOKIE_PRESENT=true`

`MASKED_ACCOUNT_LAST_LOGIN_PRESENT=true`

`MASKED_ACCOUNT_LAST_REFRESH_PRESENT=true`

`MASKED_ACCOUNT_NO_DISABLE_REASON=true`

`MASKED_ACCOUNT_NO_PLATFORM_RESTRICTION_LIKE=true`

`PUBLISH_CAPABILITY_ROUTE_PRESENT=true`

`PUBLISH_CAPABILITY_SELECTED_ACCOUNT_RESULT=UNKNOWN_NOT_CALLED_AFTER_LABEL_GATE_FAIL`

`CATALOG_ROWS=3`

`CATALOG_DISTINCT_ITEMS=3`

`CATALOG_ACTIVE_LIKE_ROWS=3`

`PUBLISH_LOG_ROWS=37`

`PUBLISH_LOG_SUCCESS_ROWS=9`

`PUBLISH_LOG_NONTERMINAL_ROWS=0`

`DUPLICATE_NORMALIZED_TITLE_GROUPS=0`

`DUPLICATE_ITEM_ID_GROUPS=0`

`CANDIDATE_MATERIAL_ID=23`

`CANDIDATE_TITLE=项目甘特图Excel模板｜任务负责人+进度+30天时间轴`

`CANDIDATE_PRICE=2.90`

`CANDIDATE_STOCK=1`

`CANDIDATE_IMAGE_COUNT=1`

`CANDIDATE_DESCRIPTION_CHARS=83`

`CANDIDATE_CATEGORY=office办公制作`

`CANDIDATE_SKU_ROWS_PRESENT=true`

`CANDIDATE_SPECIFICATIONS_PRESENT=true`

`CANDIDATE_DELIVERY_METHOD=express`

`CANDIDATE_SHIPPING_METHOD=free`

`CANDIDATE_NORMALIZED_DUPLICATE_ON_MASKED_ACCOUNT=false`

`CANDIDATE_OBVIOUS_RISK_LANGUAGE=false`

`CANDIDATE_PRIOR_SUCCESSFUL_PUBLISH_LOGS=1`

`CANDIDATE_ENABLED_DELIVERY_CARD_PRECEDENT=1`

`SERVICE_RESTART_COUNTS_ALL_ZERO=true`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`REAL_PUBLISH_INVOCATIONS=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`GO_RECOMMENDED=false`

`NO_GO_BLOCKER=APPROVED_LABEL_NOT_BOUND_IN_PRODUCTION_DURABLE_TRUTH`

`REAL_PUBLISH_ACCEPTANCE=BLOCKED_NO_IDENTITY_BINDING`

`COMMANDER_DECISION=NO-GO_FOR_REAL_PUBLISH`

## Preflight Decision

NO-GO. The approved account label gate fails closed because the exact durable-truth count for `艺龙` is `0`, while acceptance requires `1`. The masked account row `280***247` exists and looks session-ready in durable account fields, and candidate material `23` is complete and non-duplicate against the masked account, but real publish must not proceed until the approved label is durably bound to the selected account or another approved durable label source is identified.

## Final No-Go Closure

`IDENTITY_UNIQUE=FAIL`

`PUBLISH_INVOCATIONS=0`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_INVOCATIONS=0`

`BROWSER_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`DEPLOY_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

Publish and terminal durable readback were not executed and are not passed. The
only accepted Phase 1 outcome is the archived blocked/no-go evidence record.

## Upstream Capability Audit

Same as proposal.

## Pinned Upstream Evidence

Same as proposal.

## Existing Local Implementation Search

Same as proposal.

## Reuse Decision

Decision: ADOPT_UPSTREAM

## Duplicate Implementation Risk

No duplicate publish owner is accepted.

## Why Upstream Cannot Satisfy The Requirement

Upstream satisfies execution but not this pre-publish commander checkpoint.

## Approved Exception ADR

Not applicable.

## Component Owner

XIANYU native publish owner through Backend; COMPANY thin adapter only.

## Retirement Plan For Overlapping Local Code

No overlapping local code is introduced.
