# CHG-0025 Source Authority Reconciliation

Date: 2026-08-23 Asia/Taipei

SOURCE_AUTHORITY_RECONCILIATION=PASS
REAL_QR_CREATE_COUNT=0
REAL_QR_SCAN_COUNT=0
ADDITIONAL_ITEM_SYNC_INVOCATIONS=0

## Fresh XIANYU main

Fresh read-only SSH-over-443 `ls-remote`:

`0b752a7fb08456b88c5f8465f98cd8d9bc338ba1 refs/heads/main`

The ordinary HTTPS fetch path failed to connect; the SSH readback is the fresh remote authority. Main did not advance relative to the commander checkpoint.

## Historical 64c245 classification

Requested historical base reference:

`64c245bc85ac56e34339fa056b0e291a16a3843b`

The current primary upstream clone `D:/xianyu-upstream-pilot` does not expose this object through refs, reflogs, or fsck unreachable objects. The current XIANYU governance object database also does not contain it.

Exact historical worktrees remain on disk:

- `D:/xianyu-chg0018-chat-final-v2`
- `D:/xianyu-chg0018-chat-final-applycheck`
- `D:/xianyu-chg0018-t12-patchcheck`

Each reports `HEAD=64c245bc85ac56e34339fa056b0e291a16a3843b` and can read the exact base object/files.

Therefore:

`HISTORICAL_BASE_64C245_CLASSIFICATION=LOCAL_HISTORICAL_PATCH_BASE_WORKTREE_OBJECT`

`EXACT_BASE_OBJECT_RECOVERED=true`

`CONTENT_EQUIVALENT_BASE_USED=false`

No prune/gc/reset was performed.

## Exact Frontend production source preimages for CHG0025

Historical acceptance evidence identifies `D:/xianyu-chg0018-chat-final-v2` as the authoritative final source worktree and `D:/xianyu-chg0018-chat-final-applycheck` as the independent Fresh Apply worktree for cumulative patch:

`vendor/patches/xianyu-auto-reply/64c245-chg0018-chat-upstream-golden-path-cleanup.patch`

Recorded cumulative patch SHA256:

`ce55ef6d329dbb4ff982830e27f079c5af3d3c990569ba6e6b3c3a137f955346`

The patch bytes recovered from XIANYU Git history have that exact SHA256.

The three CHG0025-relevant Frontend postimages match exactly in both independent historical source worktrees:

| Path | Base SHA256 at 64c245 | Production source SHA256 |
|---|---|---|
| `frontend/src/api/accounts.ts` | `9740bb3348b27ffa851eaae71389d9c454057296d9aaca59b776799eef8c423d` | `71dcfde1ac53669261e4cbf19c781d3cd46f0c9ad69bfc0963240cd15b492268` |
| `frontend/src/pages/accounts/Accounts.tsx` | `d6ba4c261c3933419fe21110647aecfca2e2fe21f758871244feebe5c6448498` | `f31ece92d0d9570ea19477c29b1218bfd3b3e2aa365385ee20f9321af69fb5bf` |
| `frontend/src/types/index.ts` | `c45b17afe8059652a418cce1e8397867dfa6d9513f1af36b9b1e793fae6af061` | `71a0b5a41ed98ed773415d3f719822bbd31d3e02799dcfd357ce693404cf9087` |

## Source -> build -> current production artifact proof

Current production Frontend image:

`xianyu-chg0018-frontend:chat-upstream-golden-path-cleanup-20260815-r2`

Current production `index.html` references `index-Bo8JNRra.js` and `index-DSbQtSxR.css`; the Accounts lazy chunk is `Accounts-BoMMlrdD.js` and its shared API chunk is `accounts-DulStOuQ.js`.

The historical `.runtime_frontend_restore` artifacts retained under the authoritative final source worktree match the current production container byte-for-byte:

| Artifact | SHA256 |
|---|---|
| `assets/Accounts-BoMMlrdD.js` | `61ff4db1d7dd40f2b15c6e940c317502e8c04f993f2e142ffe01551968a6e681` |
| `assets/accounts-DulStOuQ.js` | `da31d9e632829e2dc4a68d74106027ae035205caef32bec3bd7790810c34ffb7` |
| `assets/index-Bo8JNRra.js` | `86f8d7b597ceafdcc20a36f59a4834a2f2932d05fa054a98410f9c529e714d6f` |
| `assets/index-DSbQtSxR.css` | `ce943d8848b339c7c2ae380a2d7f50ff3ad25dd53581421c4d8a9464699124f3` |

Thus the existing source -> cumulative patch/history -> accepted build artifact -> current production bundle lineage is proven without bundle reverse engineering.

`FRONTEND_SOURCE_AUTHORITY_MODEL=EXACT_HISTORICAL_FRESH_APPLY_PLUS_EXACT_CURRENT_BUNDLE_MATCH`

`FRONTEND_CURRENT_PRODUCTION_SOURCE_AUTHORITY_PROVEN=true`

## Backend QR route authority

Current accepted Backend container/image:

`xianyu_chg0017_backend_web`

`xianyu-chg0024-backend-web:item-sync-no-auth-recovery-20260823-r1`

Current runtime file:

`/app/backend-web/app/api/routes/qr_login.py`

SHA256:

`1d84ac624fc6ce6393d8b744f7c1d4b95cfa89c44f78b906fa0e9be70e7e2bd1`

`BACKEND_QR_ROUTE_PREIMAGE_AUTHORITY_PROVEN=true`

## Conclusion

The source-authority hard stop is cleared. CHG0025 may patch only the proven existing QR route and proven existing Frontend Accounts source while preserving existing Account/Cookie/Session/WebSocket owners.
