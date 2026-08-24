# CHG-0025 T5 Regression and Security Gates

Date: 2026-08-23 Asia/Taipei

CHG0025_FORMAL_TESTS=8/8_PASS
SECURITY_SCAN=PASS
DUPLICATE_CAPABILITY_VALIDATION=PASS
CHG0023_READINESS_REGRESSION=5/5_PASS
CHG0024_RELEVANT_REGRESSION=8/8_PASS
NEW_CHG0025_SPECIFIC_FAILURES=0
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0
ADDITIONAL_ITEM_SYNC_INVOCATIONS=0
TOTAL_NEW_T7_ITEM_SYNC_BUSINESS_INVOCATIONS=1

The first formal CHG0025 test run had one harness-only assertion error because it searched the entire unified patch and matched a deleted legacy line. The test was corrected to inspect added lines; source/postimage was not changed. The rerun passed 8/8.
