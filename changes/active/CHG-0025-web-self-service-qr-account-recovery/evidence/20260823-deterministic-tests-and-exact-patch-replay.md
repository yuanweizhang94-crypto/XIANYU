# CHG-0025 Deterministic Tests and Exact Patch Replay

Date: 2026-08-23 Asia/Taipei

BACKEND_DETERMINISTIC_TESTS=10/10_PASS
FRONTEND_DETERMINISTIC_TESTS=18/18_PASS
FRONTEND_TSC=PASS
FRONTEND_VITE_BUILD=PASS
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0
PASSWORD_LOGIN_ATTEMPTS=0
REAL_MESSAGES_SENT=0
ADDITIONAL_ITEM_SYNC_INVOCATIONS=0
TOTAL_NEW_T7_ITEM_SYNC_BUSINESS_INVOCATIONS=1

PATCH_PATH=vendor/patches/xianyu-auto-reply/chg0025-web-self-service-qr-account-recovery.patch
PATCH_SHA256=f3ecaf30603ec593521fcc84b0cce5dac92d0da45da0514ddcf8d577ab6fe8e8
PATCH_APPLY_CHECK=PASS
PATCH_CLEAN_APPLY=PASS
PATCH_REPLAY_POSTIMAGE_MATCH=true
NON_CHG0025_HUNKS=0

Preimages:
- backend QR route: `1d84ac624fc6ce6393d8b744f7c1d4b95cfa89c44f78b906fa0e9be70e7e2bd1`
- accounts API: `71dcfde1ac53669261e4cbf19c781d3cd46f0c9ad69bfc0963240cd15b492268`
- Accounts page: `f31ece92d0d9570ea19477c29b1218bfd3b3e2aa365385ee20f9321af69fb5bf`
- Frontend types: `71a0b5a41ed98ed773415d3f719822bbd31d3e02799dcfd357ce693404cf9087`

Postimages:
- backend QR route: `674381601ec3dcd7970a64e6ccb5a6ad72bcacb951a33f8c3d9867a097a96b4a`
- accounts API: `4de4bd8923faf1930832a9df2a60d91a87487f2ab89c942fa1ba27ba5b2b8777`
- Accounts page: `5b4c9c790c502790c4f0da759698ec218a7ed94aedd509da26a68418f1a0d8ef`
- Frontend types: `42b851df44745cbdaebf2376bdc2587b4b784ba4b7a7dffc2a71749b3bddc3cd`

The patch fixture used exact raw-byte production preimages with `core.autocrlf=false`. Clean replay produced exactly the four accepted postimage hashes. No historical cumulative Frontend patch was included.
