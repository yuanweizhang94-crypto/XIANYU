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

`GO_RECOMMENDED=false`

`NO_GO_BLOCKER=APPROVED_LABEL_NOT_BOUND_IN_PRODUCTION_DURABLE_TRUTH`

Commander decision: `NO-GO_FOR_REAL_PUBLISH`.

`REAL_PUBLISH_ACCEPTANCE=BLOCKED_NO_IDENTITY_BINDING`

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
IDENTITY_UNIQUE=FAIL
failure_reason=approved exact label 艺龙 is not durably bound to the masked account row in xianyu_pilot.xy_accounts or inspected approved metadata label keys
earlier_audit_resolution=the earlier exact-label PASS was either based on a wrong field, an inferred/chat label, or an unprovided external source; it is not supported by the production durable-truth evidence inspected here
```
