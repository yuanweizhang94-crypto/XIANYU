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

`NO_GO_BLOCKER=HUMAN_BLOCKED_MATERIAL_DATA`

`REAL_PUBLISH_ACCEPTANCE=BLOCKED_HUMAN_MATERIAL_DATA`

`USER_PROVIDED_IDENTITY_BINDING=PASS`

`COMMANDER_DECISION=RESUME_NARROW_PREFLIGHT_NO_PUBLISH`

## Prior Durable-Label Discrepancy

The prior durable-table exact-label query found `exact_label_count=0` for the
approved label in `xy_accounts` fields and approved metadata keys. The commander
has now supplied direct project-owner authorization and an external sensitive
screenshot binding masked account `280***247` to the authorized account label
for this run. That external evidence supersedes the prior no-go identity
blocker for the purpose of resuming read-only preflight only.

## Commander Override State

`IDENTITY_UNIQUE=PASS_BY_PROJECT_OWNER_EXTERNAL_SCREENSHOT_ASSERTION_FOR_THIS_RUN`

`PUBLISH_INVOCATIONS=0`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_INVOCATIONS=0`

`BROWSER_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`DEPLOY_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

Publish and terminal durable readback remain not executed and are not passed.

## Resumed Narrow Preflight Decision

Identity binding for this run is accepted from direct project-owner assertion
plus external sensitive screenshot metadata, with only masked account
`280***247` recorded. The selected production account row exists exactly once
by masked binding, is `active`, has owner scope, cookie/session timestamps, no
disable reason, and read-only publish capability result `success=true` with
`account_invalid=false`.

Material `23` exists and is not already represented on the selected account:

```text
catalog_rows=0
catalog_distinct_items=0
duplicate_normalized_title_groups=0
duplicate_item_id_groups=0
publish_log_rows=37
publish_log_success_rows=9
publish_log_nonterminal_rows=0
normalized_duplicate_on_masked_account=0
publish_logs_for_material_on_masked_account=0
```

Material readiness fails closed:

```text
candidate_material_id=23
candidate_exists=true
title_non_placeholder=true
description_non_empty=true
description_chars=83
price_positive=true
price=2.90
stock_positive=true
stock=1
image_count=1
images_non_empty=true
category_present=true
sku_rows_present=false
specifications_present=false
delivery_method_present=true
delivery_method=express
shipping_method_present=true
shipping_method=free
address_present=false
obvious_risk_language=false
```

Final resumed checkpoint: `NO-GO`. Publish remains forbidden because the
selected material lacks required SKU rows and specifications. The earlier
address-specific failure was too strict: existing native batch publish hydrates
address through the existing publish-address owner.

## Replacement Candidate Selection

A narrow read-only candidate-selection pass queried the existing material
owner/source-of-truth only. Material `23` was excluded. The approved account was
used internally and is recorded only as masked `280***247`.

Selected-account readiness:

```text
sanitized_account_status_ok=true
account_status=FOUND
login_ready=true
account_enabled=true
account_online=true
platform_certification_required=false
profile_ready=null
publish_capability=true
```

Candidate-selection result:

```text
material_rows_examined=42
qualified_candidate_count=0
selected_candidate=NONE
catalog_rows=0
catalog_distinct_items=0
duplicate_normalized_title_groups=0
duplicate_item_id_groups=0
publish_log_rows=37
publish_log_success_rows=9
publish_log_nonterminal_rows=0
```

No existing material other than `23` already satisfied all required gates:
active/usable real material, non-placeholder title, nonempty description,
positive price and stock, at least one valid image, category, SKU rows,
specifications, supply-chain/address facts, no exact/normalized duplicate or
already represented item for the approved account, and no obvious
prohibited/infringing language. Final candidate-selection checkpoint:
`NO-GO`.

## Root Cause For No Qualifying Material

Upstream-first source inspection showed:

- pinned upstream `ProductMaterial` canonical model requires title,
  description, price, images, optional category/address fields, and does not
  define SKU/specification fields;
- deployed runtime extends the existing material owner with canonical
  `specifications` and `sku_rows` JSON fields;
- native batch publish resolves supply-chain/address evidence through
  `PublishAddressService.resolve_publish_address`, not only from material
  `address` or `address_expected_text`;
- direct publish payload treats SKU/specifications as optional platform inputs
  when both are absent, but if one is present the pair must be complete and
  coherent.

The user requirement for explicit SKU, specifications, and supply-chain/address
evidence remains stricter than platform minimums. The address requirement is
satisfied by existing owner data, but the SKU/specification requirement is not:

```text
material_23_spec_count=0
material_23_sku_count=0
material_23_sku_spec_coherent=false
material_23_successful_publish_logs=1
material_23_success_logs_with_resolved_address_id=1
material_23_success_logs_with_resolved_address_text=1
selected_owner_personal_publish_address_count=1
global_publish_address_count=155
material_rows_examined_excluding_23=42
sku_spec_valid_material_count_excluding_23=0
qualified_candidate_count_with_owner_address=0
```

Final root-cause result: `HUMAN_BLOCKED_MATERIAL_DATA`. The exact missing facts
are real SKU row data and matching specification definitions for at least one
existing non-duplicate material. No direct/manual database repair and no
fabricated values are allowed.

## Final Phase 1 Closure

`PRODUCTION_ACCEPTANCE=BLOCKED_HUMAN_MATERIAL_DATA`

`IDENTITY_BLOCKER_SUPERSEDED=true`

`USER_PROVIDED_IDENTITY_BINDING=PASS`

`FINAL_NO_GO_BLOCKER=HUMAN_BLOCKED_MATERIAL_DATA`

`MISSING_REQUIRED_FACTS=sku_rows,specifications`

`ADDRESS_OWNER_WORKS=true`

`PUBLISH_INVOCATIONS=0`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_INVOCATIONS=0`

`BROWSER_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`MATERIAL_MUTATION_COUNT=0`

`DEPLOY_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

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
