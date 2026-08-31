# CHG-0037 Final Runtime, Material 94 Category and Archive Closure Evidence

Date: 2026-08-31

## GitHub and source authority

- PR #55 merged successfully.
- Original dependency commit: `c3ca53e0db806de1fb087892f83980f420da5010`.
- Governance follow-up commit: `76d812101767e801a37264a4dcf7c3897da42124`.
- Merged/final source authority before this archive-only closure: `dc3c2d3956e5be09ebaaf61d62aea539b5d9d254`.
- Both CHG-0037 commits were proven ancestors of that main SHA.
- `BUSINESS_SOURCE_LOGIC_CHANGED=false`.

## Candidate and production Runtime acceptance

Accepted Backend image:

`xianyu-chg0018-backend-web:chg0037-cv2-dc3c2d3-20260831-r1`

Candidate image ID:

`sha256:22fcd85af7c0061eb22e54c47f8b9bb1396d6b01039af21153c916ec7a81940f`

Verified candidate and production facts:

- `CANDIDATE_SOURCE_SHA=dc3c2d3956e5be09ebaaf61d62aea539b5d9d254`.
- `CANDIDATE_CV2_IMPORT_PASS=true`.
- `CANDIDATE_CV2_VERSION=5.0.0`.
- `CANDIDATE_OPENCV_DISTRIBUTION_VERSION=5.0.0.93`.
- `CANDIDATE_PUBLISHER_IMPORT_PASS=true`.
- `CANDIDATE_SESSION_FORBIDDEN_PATTERN_COUNT=0`.
- `CANDIDATE_CANONICAL_COOKIE_FLOW=true`.
- Backend-only atomic replacement completed with rollback retained.
- `BACKEND_HEALTHY=true` and HTTP health returned 200.
- `RUNTIME_CV2_IMPORT_PASS=true`.
- `RUNTIME_CV2_VERSION=5.0.0`.
- `RUNTIME_OPENCV_DISTRIBUTION_VERSION=5.0.0.93`.
- `PRODUCTION_SESSION_FORBIDDEN_PATTERN_COUNT=0`.
- `PRODUCTION_CANONICAL_COOKIE_FLOW=true`.
- Frontend, WebSocket, Scheduler, MySQL and Redis container identities were preserved by the guarded Backend-only replacement.
- MySQL, Redis, Cookie, Session and Profile state were preserved.
- Account read-only smoke passed.
- Chat read-only route remained reachable; the existing disconnected IM state was not changed or reconnected.

## Material 94 category authority and compatibility

Material 94 business category is `其他会员账号充值`.

The category donor used for authoritative platform comparison was existing item `1078363546811`, owned by account `2219319284219`. Its stored title begins `PLUS订阅服务，官方正规渠道办理，个人号独享使用。`.

A fresh read-only Goofish editDetail readback returned:

- `catId=50025461`.
- `catName=其他会员账号充值`.
- `channelCatId=201419202`.
- channel/category label text `其他会员账号充值`.
- `tbCatId=123604002`.

A fresh XIANYU native category recommendation using canary account `2804730247` and the real Material 94 title/description returned ten candidates, of which two were complete. Complete candidate index 0 matched the donor exactly:

- `cat_id=50025461`.
- `cat_name=其他会员账号充值`.
- `channel_cat_id=201419202`.
- `channel_cat_name=其他会员账号充值`.
- `tb_cat_id=123604002`.

Therefore `CATEGORY_COMPATIBILITY_PROVEN=true` without guessing or caller-supplied category IDs.

## Formal Material category persistence

The current COMPANY remote-main formal tool contract includes `xianyu_material_category_apply`. The local ChatGPT connector schema was stale, but a direct MCP `tools/list` handshake against the existing COMPANY Proxy confirmed the running formal tool was present. No COMPANY source or runtime was modified.

Exactly one formal call was made:

- tool: `xianyu_material_category_apply`.
- account: `2804730247`.
- material: `94`.
- `candidate_index=0`.
- no title prefix.
- no caller-controlled category IDs.

The formal adapter returned `SUCCESS` and XIANYU Material readback then proved:

- `platform_category_id=50025461`.
- `platform_category_name=其他会员账号充值`.
- `platform_channel_category_id=201419202`.
- `platform_channel_category_name=其他会员账号充值`.
- `platform_tb_category_id=123604002`.
- `category_source=recommendation`.
- title remained `限时特价 PLUS会员订阅｜正规渠道｜稳定直充｜标价就是售价`.
- price remained `135.00`.
- image count remained `1`.

Only Material 94 category fields were targeted. Materials 95-103 were not changed.

## Persisted-category hard-blocked Runtime preflight

A second production Runtime dry-run used Material 94 as read directly from the database after category persistence. No in-memory category injection was performed.

Results:

- `IN_MEMORY_CATEGORY_INJECTION_USED=false`.
- `PERSISTED_CATEGORY_USED=true`.
- `RUNTIME_TRANSPORT_GUARD_INSTALLED=true`.
- `PLATFORM_WRITE_GUARD_ACTIVE=true`.
- local image preprocessing count `1`.
- address selection count `1`.
- Publisher module loaded successfully.
- `CV2_IMPORT_PASS=true` and `CV2_VERSION=5.0.0`.
- `PUBLISH_FLOW_REACHES_PLATFORM_BOUNDARY=true`.
- the item-create transport boundary was hard-blocked before a real platform publish request.
- `REAL_PLATFORM_REQUEST_BLOCKED=true`.
- `REAL_PUBLISH_HTTP_REQUEST_COUNT=0`.
- `REAL_ITEM_CREATE_COUNT=0`.
- batch success count `0` and failed count `1` by design.
- persisted dry-run PublishLog count `0` and SUCCESS log count `0`.
- `NO_FALSE_PUBLISH_SUCCESS=true`.
- `CV2_ERROR_REPRODUCED=false`.
- `SESSION_NAMEERROR_REPRODUCED=false`.
- the database session was rolled back.
- `MATERIAL_94_PERSISTED_CATEGORY_PREFLIGHT_PASS=true`.

The transport guards were process-scoped only and are not active in the production Backend process after the dry-run process exited.

## Safety invariants

- `REAL_XIANYU_PUBLISH_EXECUTED=false`.
- `MATERIALS_PUBLISHED_THIS_CHANGE=0`.
- `ITEMS_CREATED_THIS_CHANGE=0`.
- `AUTO_REPLY_CHANGED=false`.
- `MESSAGE_SENT=false`.
- `ORDER_CHANGED=false`.
- no QR login, face verification or verification bypass was performed.
- no Backend rebuild or replacement was performed during the category/archive reconciliation stage.

## Closure conclusion

T8 through T13 now have direct completed evidence. T14 is the archive/GitHub closure operation represented by the archive preparation branch and becomes operationally complete only when the archive PR is merged and main readback proves CHG-0037 is archived with no active Change.
