Run ID: CHG17-CATALOG-DIRECTION-LIVE-20260731T095918Z-W9IU

Change ID: CHG-0017-upstream-native-auto-ai-delivery
Status: IMPLEMENTING
Verdict: ACCOUNT_A_ITEM_CATALOG_REQUIRED

## Standardized Direction Conclusion

`TEST_MESSAGE_DIRECTION_MISMATCH_AND_ITEM_CATALOG_MISS`

The previous skipped-row audit showed:

- records total: 5
- self_message: 4
- item_not_belong: 1
- EXPECTED_A_PLATFORM matches: 4
- EXPECTED_B_PLATFORM matches: 1
- EXPECTED_A_ACCOUNT matches: 0
- EXPECTED_B_ACCOUNT matches: 0

This proves that OWNER_TEST_ACCOUNT_B platform identity mapping is valid for at
least one real inbound record. The four self-message rows are ACCOUNT-A
self-message echoes and must not be interpreted as OWNER_TEST_ACCOUNT_B
identity parsing failures.

## Catalog Sync Attempt

Candidate management services were started without the websocket account task.
The upstream-native item catalog sync path was called for ACCOUNT-A.

Masked result:

- sync_success: true
- returned_items: 0
- saved_count: 0
- total_count: 0
- total_pages: 0
- candidate ACCOUNT-A catalog rows after sync: 0
- TEST_ITEM selected: no
- item ownership check proven: no

No item ID, title, account identifier, UNB, Cookie, Token, chat ID, or message
body is recorded in this evidence.

## Runtime Boundary

- websocket started: no
- ACCOUNT-A start count: 0
- OWNER_TEST_ACCOUNT_B automatic reply task: not started
- candidate online-chat send route used: no
- platform messages sent: 0
- automatic replies sent: 0
- AI calls: 0
- item mutation: 0
- order/refund/shipping/rating mutation: 0

## Cleanup

- candidate management runtime stopped: yes
- port 18090: closed
- port 8090: closed
- port 28090: closed
- port 28089: closed
- production gate enabled: no

## Result

T8 is complete based on prior successful Token/device/WebSocket evidence.
T9 remains blocked because no ACCOUNT-A TEST_ITEM could be proven in the
candidate catalog. Live keyword, Gemini AI, context, duplicate, stop, and
reconnect validation did not run.
