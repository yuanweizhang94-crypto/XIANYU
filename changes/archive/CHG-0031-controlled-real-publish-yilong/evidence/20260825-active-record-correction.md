# CHG-0031 Active Record Correction

Change ID: CHG-0031-controlled-real-publish-yilong
Status: ARCHIVED
Date: 2026-08-25

## Correction

The target worktree initially did not contain `changes/active/CHG-0031-controlled-real-publish-yilong/proposal.md`, and `git status` was clean. This evidence file records the correction in the actual isolated target worktree.

## Execution Contract

User outcome: safely publish exactly one real sellable existing material through the existing unique upstream-native owner to the uniquely identified account labeled 艺龙 and keep it online.

Confirmed blocker: exact selected-account publish capability and one non-duplicate production-ready material must be proven; any trace/durable-truth gap must fail closed.

Smallest success test: one invocation, one platform item ACTIVE, local durable truth and remote/readback match, account item count +1, zero duplicate/extra items.

## Safety Counters

`REAL_PUBLISH_INVOCATIONS=0`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`DEPLOY_INVOCATIONS=0`

`COMMIT_INVOCATIONS=0`

`PUSH_INVOCATIONS=0`

`PRODUCTION_DATABASE_PREFLIGHT_STOPPED=true`

## T6 Narrow Read-Only Preflight

Scope executed: production durable-truth reads and runtime metadata inspection only. No publish, Fresh Item Sync, deploy, restart, edit, offline, delete, message, Browser, QR, or credential access occurred.

### Account Label And Session

Exact approved-label query over discovered durable account label fields (`display_name`, `username`, `remark`, `metadata`) returned:

```text
exact_label_count=0
masked_bind_count=NULL
masked_account=NONE
```

The already masked account row was present:

```text
masked_row_count=1
masked_account=280***247
account_status=active
cookie_present=1
last_login_present=1
last_refresh_present=1
no_disable_reason=1
no_platform_restriction_like=1
```

Decision: `NO-GO`, because the exact label `艺龙` is not durably bound to the selected account in the discovered production account truth.

### Publish Capability Route

Runtime route inspection:

```text
product_publish_capability.py_exists=true
product_publish_capability.py_detect_publish_account_capability=true
product_publish.py_exists=true
product_publish.py_detect_publish_account_capability=true
product_publish.py_publish_batch=true
```

Selected-account publish capability was not called after the exact-label gate failed, so selected capability remains `UNKNOWN_NOT_CALLED_AFTER_LABEL_GATE_FAIL`.

### Current Local Catalog And Publish Baseline

No Fresh Item Sync was invoked.

```text
catalog_rows=3
catalog_distinct_items=3
catalog_active_like_rows=3
catalog_oldest_at=2026-08-20 01:49:44
catalog_newest_at=2026-08-25 14:24:27
publish_log_rows=37
publish_log_success_rows=9
publish_log_nonterminal_rows=0
publish_log_distinct_logged_items=9
publish_log_newest_at=2026-08-20 09:49:43
duplicate_normalized_title_groups=0
duplicate_normalized_title_rows=0
duplicate_item_id_groups=0
```

### Candidate Material

At most one material was inspected and selected as a possible candidate, subject to the account-label NO-GO blocker:

```text
material_id=23
title=项目甘特图Excel模板｜任务负责人+进度+30天时间轴
description_chars=83
price=2.90
stock=1
image_count=1
category=office办公制作
sku_rows_present=1
specifications_present=1
delivery_method=express
shipping_method=free
normalized_duplicate_on_masked_account=0
obvious_risk_language=0
successful_publish_logs=1
enabled_delivery_card_precedent=1
```

No obvious placeholder, prohibited, infringement, credential, or unverifiable-risk language was found by the narrow keyword screen.

### Owner, Idempotency, Durable Readback Contract

Only allowed later owner route:

```text
COMPANY xianyu_publish_single
-> XIANYU Backend /api/v1/product-publish/publish/batch
-> PublishExecutorService
-> execute_single_publish
-> detect_publish_account_capability
-> XianyuDirectPublisher / XianyuPersonalPublisher
-> MTOP publish
-> Publish Log
-> authoritative item sync/readback
```

If a later `GO_FOR_REAL_PUBLISH` is issued, use one deterministic idempotency key scoped to CHG-0031, the masked selected account, and material `23`; recover terminal status instead of retrying after UNKNOWN; require platform final ACTIVE state plus local durable truth/readback match and account item count +1.

### Service/Image/Restart Baseline

```text
backend=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2 restart=0
websocket=xianyu-chg0023-websocket:readiness-contract-20260822-r1 restart=0
scheduler=xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1 restart=0
frontend=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2 restart=0
mysql=mysql:8.0 restart=0
redis=redis:7.4-alpine restart=0
```

### Final T6 Decision

`GO_RECOMMENDED=SUPERSEDED_BY_COMMANDER_OVERRIDE_PENDING_RESUMED_PREFLIGHT`

`NO_GO_BLOCKER=CLEARED_FOR_THIS_RUN_BY_PROJECT_OWNER_EXTERNAL_BINDING`

Original commander decision: `NO-GO_FOR_REAL_PUBLISH`.

Override commander decision: `RESUME_NARROW_PREFLIGHT_NO_PUBLISH`.

`REAL_PUBLISH_ACCEPTANCE=PENDING_PREFLIGHT_AFTER_OWNER_BINDING`

`USER_PROVIDED_IDENTITY_BINDING=PASS`

`EXTERNAL_SENSITIVE_EVIDENCE_PATH=D:/Temp/codex-clipboard-5ae3b039-6bc0-4b76-ac50-c85220aaaeda.png`

`EXTERNAL_SENSITIVE_EVIDENCE_COMMITTED=false`

`EXTERNAL_SENSITIVE_EVIDENCE_HASH_RECORDED=false`

`FULL_ACCOUNT_ID_RECORDED=false`

`PUBLISH_INVOCATIONS=0`

`FRESH_ITEM_SYNC_INVOCATIONS=0`

`MESSAGE_SEND_INVOCATIONS=0`

`AI_INVOCATIONS=0`

`BROWSER_INVOCATIONS=0`

`ACCOUNT_MUTATION_COUNT=0`

`DEPLOY_INVOCATIONS=0`

`PRODUCTION_MUTATION_COUNT=0`

No production publish, deploy, Fresh Item Sync, message, AI, Browser, account
edit, item edit, offline, delete, reconnect, QR, credential access, or profile
mutation was performed. Publish terminal ACTIVE/readback/item-count +1
acceptance was not executed and is not claimed.

### T6 Identity Discrepancy Diagnosis

This section records only already-collected read-only evidence. No publish,
deploy, commit, push, credential read, account-label edit, Fresh Item Sync, or
production mutation was performed.

Authoritative production source semantics used for this diagnosis:

```text
backend_container=/xianyu_chg0017_backend_web
backend_image=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2
backend_restart_count=0
mysql_container=/xianyu_chg0017_mysql
mysql_image=mysql:8.0
mysql_restart_count=0
backend_environment=production
backend_mysql_host=xianyu_chg0017_mysql
backend_mysql_database=xianyu_pilot
authoritative_table=xianyu_pilot.xy_accounts
```

`xy_accounts` contains the candidate durable identity/display fields
`account_id`, `display_name`, `username`, `remark`, and `metadata`.
Backend account DTO/service mapping uses `xy_accounts.account_id` as the
selected account id and maps display/list remark from `xy_accounts.remark`;
the account lookup first resolves by exact `account_id`, then by `unb`.

For the single internally bound masked row `280***247`, the approved exact
Unicode string `艺龙` was not present in any inspected durable candidate label
field or approved metadata label key:

```text
target_rows_by_mask=1
approved_label_utf8_hex=E889BAE9BE99
approved_label_chars=2
display_exact=0
display_trim_exact=0
username_exact=0
username_trim_exact=0
remark_exact=0
remark_trim_exact=0
metadata_json_search_exact=0
metadata_contains_exact=0
metadata_key_display_name_present=0
metadata_key_nickname_present=0
metadata_key_name_present=0
metadata_key_label_present=0
metadata_key_remark_present=0
metadata_top_level_key_count=1
metadata_has_account_info=0
metadata_has_user_info=0
metadata_has_profile=0
metadata_has_business_capabilities=0
```

Exact-label count across the inspected durable account identity fields and
approved metadata label keys:

```text
exact_label_count=0
masked_bind_count=NULL
masked_account=NONE
```

The sanitized `app_xianyu_account_status` path is not an independent display
label authority. It accepts an account id, calls the backend read-only route
`/api/v1/cookies/details/paginated?page=1&page_size=1&account_id=...`, and
returns status booleans for the requested account. The inspected adapter output
shape does not prove that the display identity `艺龙` is durably bound to
`280***247`.

Identity conclusion:

```text
IDENTITY_UNIQUE=PASS_BY_PROJECT_OWNER_EXTERNAL_SCREENSHOT_ASSERTION_FOR_THIS_RUN
durable_table_note=approved exact label was not found in xianyu_pilot.xy_accounts durable label fields or inspected approved metadata label keys
override_source=direct project-owner assertion plus external sensitive screenshot, not committed and not hashed
```

### Resumed Read-Only Preflight After Commander Override

No production publish, deploy, commit, push, Fresh Item Sync, message, AI,
Browser, account mutation, item edit, offline, delete, QR, reconnect, or
credential logging occurred during the resumed preflight.

Identity binding:

```text
USER_PROVIDED_IDENTITY_BINDING=PASS
external_sensitive_evidence_path=D:/Temp/codex-clipboard-5ae3b039-6bc0-4b76-ac50-c85220aaaeda.png
external_sensitive_evidence_committed=false
external_sensitive_evidence_hash_recorded=false
full_account_id_recorded=false
masked_account=280***247
selected_mask_query_count=1
db=xianyu_pilot
status=active
owner_id_present=true
cookie_present=true
last_login_present=true
last_refresh_present=true
no_disable_reason=true
metadata_present=true
```

Read-only selected-account publish capability:

```text
capability_owner=common.services.xianyu_publish_service.detect_publish_account_capability
capability_success=true
account_invalid=false
is_fish_shop=false
support_sku_or_inventory=false
publish_capability=true
verification_false=not_explicitly_returned_by_capability_result
```

Current selected-account local baseline and duplicate state:

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

Candidate material `23` resumed validation:

```text
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

Service/image/restart baseline:

```text
backend=xianyu-chg0030-backend-web:fresh-item-sync-canary-20260825-r2 restart=0
mysql=mysql:8.0 restart=0
redis=redis:7.4-alpine restart=0
websocket=xianyu-chg0023-websocket:readiness-contract-20260822-r1 restart=0
scheduler=xianyu-chg0027-scheduler:session-cooldown-lineage-20260824-r1 restart=0
frontend=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2 restart=0
```

Idempotency and durable readback plan if a later GO becomes legal after the
material blocker is repaired: exactly one invocation through
`xianyu_publish_single`, deterministic CHG-0031 idempotency key, recover
terminal status rather than retrying UNKNOWN, require platform item ACTIVE,
local durable truth/readback match, account item count +1 from baseline 0, and
zero duplicate/extra items.

Resumed checkpoint:

```text
GO_RECOMMENDED=false
NO_GO_BLOCKER=CANDIDATE_MATERIAL_MISSING_REQUIRED_SKU_SPECIFICATIONS_AND_SUPPLY_CHAIN_ADDRESS
REAL_PUBLISH_ACCEPTANCE=BLOCKED_MATERIAL_NOT_PRODUCTION_READY
PUBLISH_INVOCATIONS=0
FRESH_ITEM_SYNC_INVOCATIONS=0
MESSAGE_SEND_INVOCATIONS=0
AI_INVOCATIONS=0
BROWSER_INVOCATIONS=0
ACCOUNT_MUTATION_COUNT=0
DEPLOY_INVOCATIONS=0
PRODUCTION_MUTATION_COUNT=0
```

### Replacement Candidate Selection

No production publish, deploy, commit, push, Fresh Item Sync, message, AI,
Browser, account mutation, material mutation, item edit, offline, delete, QR,
reconnect, or credential logging occurred during this candidate-selection pass.

Sanitized selected-account readiness from the approved internally supplied
account id:

```text
masked_account=280***247
sanitized_account_status_ok=true
account_status=FOUND
login_ready=true
account_enabled=true
account_online=true
platform_certification_required=false
profile_ready=null
backend_auth_source_type=LOCAL_JSON_TOKEN_FILE
publish_capability=true
```

Existing material owner/source-of-truth query result:

```text
material_source=xy_product_materials
excluded_material_id=23
material_rows_examined=42
qualified_candidate_count=0
selected_candidate=NONE
```

Selected-account local baseline and duplicate guards for this selection:

```text
catalog_rows=0
catalog_distinct_items=0
duplicate_normalized_title_groups=0
duplicate_item_id_groups=0
publish_log_rows=37
publish_log_success_rows=9
publish_log_nonterminal_rows=0
```

Candidate-selection checkpoint:

```text
GO_RECOMMENDED=false
NO_GO_BLOCKER=NO_QUALIFYING_EXISTING_MATERIAL_WITH_REQUIRED_FIELDS
NO_QUALIFYING_MATERIAL_EXISTS=true
PUBLISH_INVOCATIONS=0
FRESH_ITEM_SYNC_INVOCATIONS=0
MESSAGE_SEND_INVOCATIONS=0
AI_INVOCATIONS=0
BROWSER_INVOCATIONS=0
ACCOUNT_MUTATION_COUNT=0
DEPLOY_INVOCATIONS=0
PRODUCTION_MUTATION_COUNT=0
```

### Root Cause For No Qualifying Existing Material

Upstream-first inspection:

```text
pinned_upstream_sha=bda1a859df63fa5f24e51398fa80a23490bb6dfc
pinned_upstream_product_material_fields=title,description,price,original_price,category,images,delivery_method,postage,address,brand,condition,remark
pinned_upstream_sku_spec_fields_present=false
runtime_material_owner=ProductMaterialService
runtime_sku_spec_fields=specifications,sku_rows
native_batch_publish_address_owner=PublishAddressService.resolve_publish_address
direct_payload_sku_spec_platform_minimum=optional_when_both_absent_but_required_to_be_coherent_if_present
user_requirement_sku_spec_supply_chain=explicit_required
```

Material `23` root-cause facts:

```text
material_23_spec_type=list
material_23_spec_count=0
material_23_sku_type=list
material_23_sku_count=0
material_23_sku_spec_coherent=false
material_23_sku_spec_reason=missing_specs_or_rows
material_23_material_address_present=false
material_23_platform_category_id_present=true
material_23_platform_category_name_present=true
material_23_platform_category_path_count=4
material_23_successful_publish_logs=1
material_23_success_logs_with_resolved_address_id=1
material_23_success_logs_with_resolved_address_text=1
```

Minimal successful historical material sample:

```text
historical_success_material_ids=30,3,4,5,31
historical_success_materials_all_spec_count=0
historical_success_materials_all_sku_count=0
historical_success_materials_all_sku_spec_coherent=false
historical_success_materials_all_material_address_present=false
historical_success_materials_all_success_logs_have_resolved_address=true
```

Existing address owner evidence:

```text
selected_owner_personal_publish_address_count=1
global_publish_address_count=155
address_owner_available=true
```

Replacement candidate recomputation with address satisfied by existing owner:

```text
material_rows_examined_excluding_23=42
sku_spec_valid_material_count_excluding_23=0
qualified_candidate_count_with_owner_address=0
failure_counts=category:5,represented:16,sku_spec:42
selected_candidate=NONE
```

Root-cause conclusion:

```text
ROOT_CAUSE=HUMAN_BLOCKED_MATERIAL_DATA
address_classifier_defect=true
address_classifier_defect_changes_decision=false
missing_required_facts=sku_rows,specifications
patch_upstream_required=false
reason_no_patch=existing owners already support SKU/spec JSON and address hydration; no authoritative SKU/spec source exists to hydrate missing material data without human material data entry
```

### Final Phase 1 Closure

Commander final decision: `NO-GO`.

```text
PRODUCTION_ACCEPTANCE=BLOCKED_HUMAN_MATERIAL_DATA
IDENTITY_BLOCKER_SUPERSEDED=true
USER_PROVIDED_IDENTITY_BINDING=PASS
FINAL_NO_GO_BLOCKER=HUMAN_BLOCKED_MATERIAL_DATA
MISSING_REQUIRED_FACTS=sku_rows,specifications
ADDRESS_OWNER_WORKS=true
PUBLISH_INVOCATIONS=0
FRESH_ITEM_SYNC_INVOCATIONS=0
MESSAGE_SEND_INVOCATIONS=0
AI_INVOCATIONS=0
BROWSER_INVOCATIONS=0
ACCOUNT_MUTATION_COUNT=0
MATERIAL_MUTATION_COUNT=0
DEPLOY_INVOCATIONS=0
PRODUCTION_MUTATION_COUNT=0
```
