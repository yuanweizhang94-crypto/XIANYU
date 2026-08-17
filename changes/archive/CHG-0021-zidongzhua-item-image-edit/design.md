# CHG-0021 Design

Status: ARCHIVED

Change ID: CHG-0021-zidongzhua-item-image-edit

## Architecture

Existing ownership remains unchanged:

`COMPANY thin adapter -> XIANYU product_publish route -> XianyuPersonalPublisher -> existing upload_publish_image + mtop_call -> Goofish official PC edit APIs`.

No new service, database table, worker, browser manager, Session owner, Cookie owner, Publisher, or media uploader is introduced.

## Platform edit state machine

1. Validate account/item ownership in XIANYU local catalog.
2. Validate replacement images are XIANYU-owned `/static/uploads/products/` files.
3. Detect current account publish capability and fail closed for unsupported fish-shop editing.
4. `editDetail(itemId)` reads the current platform payload.
5. Upload replacement image(s) through existing `upload_publish_image`.
6. Build an allowlisted edit payload from the current platform detail; replace only `imageInfoDOList`.
7. Submit `idleitem.edit` once with network retry disabled.
8. If the write response is unknown, return `UNKNOWN` and do not retry.
9. On explicit write success, call `editDetail(itemId)` again.
10. Compare the current image object(s) with the uploaded image object(s). Alibaba CDN scheme/path rewrites are normalized by object filename.
11. Return `SUCCESS` only after authoritative readback confirmation.

## Ownership and security

- `xianyu_mtop` continues to own signing, token refresh, Session/error classification, and credentials.
- `xianyu_publish_media` continues to own platform image upload.
- `XianyuPersonalPublisher` continues to own ordinary-seller payload semantics.
- Backend route accepts no Cookie, Token, authorization header, arbitrary endpoint, title, price, description, or category change.
- Platform verification/account-invalid results fail closed.
- The patch does not attempt CAPTCHA, slider, QR, face, or identity-verification bypass.

## Rollback

Remove the vendor patch / deployed incremental hunks and restart only the Backend. Existing publish, item sync, Session, WebSocket, Scheduler, database, and COMPANY infrastructure remain independent.
