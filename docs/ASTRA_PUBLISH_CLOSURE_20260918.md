# XIANYU ASTRA Publish Closure — 2026-09-18

## Final business result

```text
TITLE=66 ASTRA 月卡 代充，袋充
PRICE=135
UNIQUE_MATERIALS=10
REAL_PUBLISH_OPERATIONS=18
SUCCESS_OPERATIONS=12
FAILED_OPERATIONS=6
UNKNOWN_OPERATIONS=0
```

All six failed operations are historical intermediate attempts with `PRODUCT_CREATED=false`. No UNKNOWN side effect remains.

## Publisher Session repair

Production WebSocket runtime:

```text
xianyu-chg0035-websocket:publish-session-fix-20260918-r1
```

Persisted source commit:

```text
ab7d6786903fcf1c755eb666b8b6d69fae05355f
```

The repair keeps the existing Session/Token/Publisher owners and closes two proven Runtime defects:

```text
renew_auth_valid
→ authoritative Cookie commit
→ clear persisted PVR marker
→ _clear_platform_verification_required()
→ last_token_refresh_status=success
```

and:

```text
OLD: instance.token_manager.trigger_refresh()
NEW: instance.refresh_token()
```

Targeted regression tests passed 6/6 and the persisted patch reproduces the activated Runtime source after canonical LF normalization.

## Fish Shop blocker resolution

Target account:

```text
ACCOUNT_ID=2196106636
IS_FISH_SHOP=true
```

Initial real publish of Material 109 failed at:

```text
API_NAME=mtop.idle.pc.backend.idleitem.publish
REQUEST_STAGE=final Fish Shop publish request; platform-internal shop-improve/pack-query prerequisite
RESPONSE_CODE=FAIL_BIZ_SHOP_IMPROVE_PACK_QUERY_EXP
RESPONSE_MESSAGE=亲，小闲鱼有点忙，请稍后重试哦
IS_AUTH_ERROR=false
IS_BUSINESS_TRANSIENT=true
IS_REQUIRED_PUBLISH_PREREQUISITE=true
```

Before retry, authoritative no-item proof was established:

```text
original batch=610efa94-d7f6-4e02-bf73-850c1f7dfa5d
operation status=FAILED
batch success=0
batch failed=1
publish_log.item_id=null
publish_log.item_url=null
current item sync total=0
local catalog count=0
PLATFORM_ITEM_CREATED=false
UNKNOWN_SIDE_EFFECT=false
```

Current upstream `6397dcf01defe5868d981b383a6aae74beb77513` contains no dedicated fix for this error and no separate no-write shop-improve pack-query endpoint. The current production Runtime is more complete than upstream in the Fish Shop publish path, so no Publisher code was changed.

A current account-scoped category recommendation/readback passed before the retry. One controlled real retry then succeeded:

```text
MATERIAL_ID=109
ACCOUNT_ID=2196106636
BATCH_ID=d7833cbe-5706-4409-ab8c-e0e2beba4586
FINAL_STATUS=SUCCESS
PLATFORM_ITEM_ID=1086172352322
ITEM_URL=https://www.goofish.com/item?id=1086172352322
PRODUCT_CREATED=true
AUTHORITATIVE_SYNC_CONFIRMED=true
```

Therefore the prior `FAIL_BIZ_SHOP_IMPROVE_PACK_QUERY_EXP` is classified as a platform-side transient business failure, not a Session, Token, QR, platform-verification, or local Publisher implementation defect.

## Final authoritative ASTRA items

Original ten-image publication set:

```text
astra_01 / material 108 / 2804730247 / 1083167591376
astra_02 / material 112 / 2214313339860 / 1085116561276
astra_03 / material 104 / 2804730247 / 1083167295431
astra_04 / material 105 / 2214313339860 / 1085115701625
astra_05 / material 109 / 2221422775489 / 1083167903144
astra_06 / material 106 / 2221422775489 / 1085115761716
astra_07 / material 110 / 2221384086829 / 1086139424625
astra_08 / material 113 / 2804730247 / 1083167911585
astra_09 / material 107 / 2221384086829 / 1086134168189
astra_10 / material 111 / 2214313339860 / 1086139280925
```

Additional post-repair Publisher verification items:

```text
material 108 / 1992416548 / 1086163872502
material 109 / 2196106636 / 1086172352322
```

## Remaining account boundaries

```text
2217936413500=HUMAN_QR_REQUIRED
2221501265279=HUMAN_QR_REQUIRED
2219319284219=FAIL_BIZ_USER_ERROR_USER_WAS_FORBIDDEN2
```

These account states do not block completion of the current ASTRA material set because the affected materials were already published through other proven Publisher-ready accounts.

No Cookie, Token, Authorization header, password, QR payload, or other credential material is stored in this document.
