# CHG-0021 Acceptance

Status: ARCHIVED

Change ID: CHG-0021-zidongzhua-item-image-edit

- [x] Current upstream and official PC frontend edit path inspected before implementation.
- [x] Existing `XianyuPersonalPublisher`, `mtop_call`, and `upload_publish_image` reused; no parallel Publisher/session/uploader created.
- [x] Platform edit uses `mtop.idle.pc.idleitem.editDetail` -> `mtop.idle.pc.idleitem.edit` -> authoritative `editDetail` readback.
- [x] Existing title, description, price, category, address, and other allowed edit fields are preserved from platform detail; only `imageInfoDOList` is replaced.
- [x] Write-network uncertainty is not blindly retried and returns `UNKNOWN`.
- [x] Alibaba CDN `imgextra` / `bao/uploaded` rewrites are compared by the same uploaded object filename.
- [x] Backend route accepts only XIANYU-owned `/static/uploads/products/` files and verifies item/account ownership.
- [x] Ordinary-seller-only boundary is explicit; unsupported fish-shop edit fails closed.
- [x] Targeted upstream item-image tests: 3/3 PASS.
- [x] Python compile check: PASS.
- [x] `git diff --check`: PASS.
- [x] Vendor patch SHA256: `C4BD334F9CAA4AC2BDE156440544D5C5A817B8E2665CB3E5A597F0135A3170B7`.
- [x] Vendor patch clean apply check against upstream base `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`: PASS.
- [x] Production final authoritative image status: 4/4 existing listings show the new image objects.
- [x] No listing delete or republish was used for the image refresh.
