Run ID: CHG17-CATALOG-FALLBACK-OFFLINE-20260731T102708Z

Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
Verdict: LOCAL_ITEM_CATALOG_MISS

## Scope

This run continued the existing Draft PR #26 without creating a new Change, a
new PR, or merging the PR. It did not re-verify Token, Gemini, WebSocket, or
sender runtime behavior. No ACCOUNT-A websocket task was started and no message
was sent.

## Item Sync Logging Fix

Upstream candidate file:

- `common/utils/item_info_manager.py`

Raw logging of request headers, Cookie, signed params, request data, data value,
full response body, account ID, and user ID was removed from the candidate
patch. Replacement logs are structured and limited to request start, page
number, page size, resolved identity presence, HTTP status, ret classification,
response data key names, cardList count, parsed item count, saved item count,
duration availability, and error type.

Masked log test:

- Cookie printed: no
- `_m_h5_tk` printed: no
- sign printed: no
- Authorization printed: no
- full account identifier printed: no

## Offline Catalog Diagnosis

Only candidate MySQL, Redis, and backend-web were started. WebSocket and
ACCOUNT-A account task were not started. The upstream-native item list path was
called for page 1.

Masked result:

- cookie_user_identity_present: true
- stored_unb_present: true
- cookie_identity_matches_stored_unb: true
- API ret: success
- HTTP status: 200
- response data key names: `itemTopicList`, `needDecryptKeys`,
  `needDecryptKeysV2`, `nextPage`, `serverDecryptKeys`, `serverTime`,
  `topItem`, `totalCount`
- cardList present: false
- cardList count: 0
- other array field counts: all observed arrays were 0
- parsed items count: 0
- valid items count: 0
- skipped invalid items count: 0
- saved_count: 0
- candidate DB count for ACCOUNT-A: 0

Classification:

`ITEM_API_RETURNED_EMPTY`

## Reply Routing Fix

Upstream candidate file:

- `websocket/app/services/xianyu/auto_reply_service.py`

The previous `item_not_belong` branch treated a local catalog miss as a hard
reply stop. The candidate patch now records `item_catalog_missing=true` and
continues to account-level routing. When local catalog data is missing, the
candidate uses no item scope for keyword, AI, or default routing. This prevents
item-specific keyword/default/image/card/order/shipping/rating paths from being
selected by a locally unknown item while still allowing approved account-level
text keyword and Gemini paths after the CHG-0017 sender allowlist gate.

## Offline Tests

Candidate command:

`python tests/test_chg0017_reply_allowlist.py`

Result:

- tests passed: 18
- allowlist gate tests: passed
- catalog-missing global keyword fallback: passed
- catalog-missing AI fallback: passed
- catalog-missing item-specific keyword skip: passed
- catalog-missing item-specific default downgrade: passed
- known-catalog item scope preservation: passed
- catalog-missing safe log assertion: passed
- item sync safe log assertion: passed

## Patch Artifact

- patch file:
  `vendor/patches/xianyu-auto-reply/4c5e1ac-chg0017-reply-identity-allowlist.patch`
- SHA256:
  `4918E56416B2B0B1993801265BA09D876EACAEED73903A4E4FE44C68240C959A`
- clean apply check: passed
- patch target files:
  - `common/utils/item_info_manager.py`
  - `websocket/app/services/xianyu/auto_reply_service.py`
  - `tests/test_chg0017_reply_allowlist.py`

## Safety

- ACCOUNT-A websocket task started: no
- OWNER_TEST_ACCOUNT_B automatic reply task started: no
- platform messages sent: 0
- automatic replies sent: 0
- AI calls: 0
- item/order/refund/shipping/rating side effects: 0
- Cookie/Token/API key/UNB/full account ID/item ID/chat ID/message body recorded: no

## Next

T9/T10/T11 remain unchecked until the controlled live run proves the
upstream-native sender, account-level keyword, Gemini AI, cleanup, and reconnect
behavior under the CHG-0017 allowlist.
