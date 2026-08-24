# CHG-0025 Candidate Build and Frontend Runtime Preservation

Date: 2026-08-23 Asia/Taipei

T6_COMPLETE=true
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0

BACKEND_CANDIDATE=xianyu-chg0025-backend-web:web-self-service-qr-20260823-r1
BACKEND_CANDIDATE_IMAGE_ID=sha256:e50e217bd784d3dfbbd857b0f943aed9674c3a63ed02de053ff9dd013c1ef818
BACKEND_QR_ROUTE_POSTIMAGE_SHA256=674381601ec3dcd7970a64e6ccb5a6ad72bcacb951a33f8c3d9867a097a96b4a
BACKEND_BASE=xianyu-chg0024-backend-web:item-sync-no-auth-recovery-20260823-r1

FRONTEND_CANDIDATE=xianyu-chg0025-frontend:web-self-service-qr-20260823-r1
FRONTEND_CANDIDATE_IMAGE_ID=sha256:7dd999a6dbb6ee86cc3534e1def63f378ffd340ae20d159d3889b548f552b6c2
FRONTEND_BASE=xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2

The running Frontend contains later static hotfix artifacts beyond its base image, including an existing Orders import-map redirect. Replacing the whole freshly-built dist would regress unrelated runtime truth, so CHG0025 preserves the exact running static tree and overlays only a new account API compat chunk, a new Accounts page compat chunk, and one Accounts import-map entry. Existing Orders mapping remains byte-semantically preserved.

FRONTEND_COMPAT_API=accounts-CHG0025-b9434280163c.js
FRONTEND_COMPAT_API_SHA256=b9434280163ca78a61263860fabb42229c785699b427a831d2da845a2770757a
FRONTEND_COMPAT_PAGE=Accounts-CHG0025-3859a50c2210.js
FRONTEND_COMPAT_PAGE_SHA256=3859a50c22107e380dd5445468071ddbcf1b9eb03dea0b1146f6d74f89c207f9
FRONTEND_RUNTIME_INDEX_POSTIMAGE_SHA256=ce6b909ffe05da6b4e9af97f933f751f3bffa41a9df9b290a0abe9d855444e69
FRONTEND_STATIC_DIRECT_IMPORT_COUNT=23
FRONTEND_STATIC_MISSING_IMPORT_COUNT=0
ORDERS_IMPORTMAP_PRESERVED=true
WEBSOCKET_CANDIDATE_BUILT=false
SCHEDULER_CANDIDATE_BUILT=false
