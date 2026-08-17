# CHG-0021 ZIDONGZHUA Existing Item Image Edit

Status: ARCHIVED

Change ID: CHG-0021-zidongzhua-item-image-edit

## Execution contract

User outcome: replace unattractive product images on already-published ZIDONGZHUA listings without deleting or republishing the listings and without changing title, price, category, description, or delivery data.

Confirmed blocker: XIANYU exposed publish and local item metadata update paths, but did not expose the Goofish platform's existing-item image edit path as an auditable operation.

Smallest success test: for one existing ordinary-seller item, upload a replacement image, submit the official PC item edit API once, then read the platform edit detail again and confirm the new image object while the existing item identity is unchanged.

## Upstream / official-path evidence

- Current upstream base inspected: `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`.
- The current Goofish PC publish frontend dynamically loads the official existing-item APIs `mtop.idle.pc.idleitem.editDetail` and `mtop.idle.pc.idleitem.edit`.
- Existing upstream `common/services/xianyu_mtop.py` owns MTOP signing/session handling.
- Existing upstream `common/services/xianyu_publish_media.py` owns image upload.
- Existing upstream `XianyuPersonalPublisher` owns ordinary-seller PC publish payload semantics.
- Existing XIANYU local `/items/{item_id}` updates only local catalog metadata and therefore was explicitly not used as evidence of a platform edit.

## Upstream capability audit

The upstream publish stack already provides MTOP signing/session handling, ordinary-seller publish payload ownership, product media upload, account capability detection, and item catalog synchronization. It does not expose an existing-item platform image edit operation even though the current official PC frontend exposes `idleitem.editDetail` and `idleitem.edit`.

## Pinned upstream evidence

Pinned source base for this patch: `742fb58a483d9c27d0bef75d7e3a10b4cfe24cc1`. Evidence paths: `common/services/xianyu_mtop.py`, `common/services/xianyu_publish_media.py`, `common/services/xianyu_publish_service.py`, `backend-web/app/services/xianyu_personal_publisher.py`, `backend-web/app/api/routes/product_publish.py`, and `common/services/item_service.py`. Official frontend runtime evidence identified `mtop.idle.pc.idleitem.editDetail` and `mtop.idle.pc.idleitem.edit` in the current PC publish bundle.

## Existing local implementation search

XIANYU local/runtime paths were checked for item update, edit, modify, published-image update, and the existing `/items/{item_id}` route. The local route changes only XIANYU catalog metadata and does not mutate the platform listing. No existing formal platform image-edit adapter was present.

## Reuse decision

Decision: PATCH_UPSTREAM

The patch extends the existing ordinary-seller publisher and publish router only. It does not add a second Publisher, browser manager, session owner, image uploader, signer, or item-sync implementation.

## Duplicate implementation risk

The primary risk is accidentally creating a second publisher/media/session execution path. The implementation therefore reuses the existing `XianyuPersonalPublisher`, `mtop_call`, `upload_publish_image`, account capability service, and XIANYU item ownership checks. COMPANY remains a thin transport only.

## Why upstream cannot satisfy the requirement

The upstream pieces required to perform the edit exist, but upstream does not wire them into a formal existing-item image edit operation. Without the minimal patch, the only available XIANYU item update route changes local metadata rather than the Goofish listing.

## Approved exception ADR

Not applicable. This is a minimal extension of existing upstream-owned services and routes, not a local exception runtime or parallel execution owner.

## Component owner

`XianyuPersonalPublisher` remains the ordinary-seller platform execution owner; `product_publish` remains the Backend route owner; `xianyu_mtop` and `xianyu_publish_media` remain the MTOP and image-upload owners.

## Retirement plan for overlapping local code

No overlapping owner is introduced. If upstream later ships an equivalent verified existing-item edit method/route, this patch and the COMPANY thin wrapper should be reviewed for retirement in favor of upstream.

## Safety contract

- the edit route accepts only account ID, existing item ID, and XIANYU-owned uploaded product image paths;
- title, price, category, description, credentials, raw platform endpoints, and arbitrary URLs are not accepted by the thin operation;
- existing item fields are loaded from `editDetail` and only `imageInfoDOList` is replaced;
- network-unknown writes use `retry_network_errors=False` and return `UNKNOWN` instead of blind retry;
- success requires authoritative `editDetail` readback after the write;
- Alibaba CDN scheme/path normalization is compared by the uploaded object filename so `imgextra` -> `bao/uploaded` rewrites do not create false UNKNOWN outcomes;
- platform verification/account invalid states remain fail-closed;
- current thin edit path supports ordinary-seller items only; fish-shop edit remains unsupported rather than guessed.

## Production result

Four existing ZIDONGZHUA listings were updated in place through the formal COMPANY -> XIANYU flow. No listing was deleted or republished. Final read-only `editDetail` checks returned the new image object for all four existing item IDs:

- `1077035060719`
- `1077035584051`
- `1076039705543`
- `1076024597942`

One catalog item was initially absent from XIANYU local item storage. The upstream-native `/api/v1/items/get-all-from-account` -> `ItemService.fetch_all_items_from_account` flow was reused to synchronize it; no parallel item crawler was built.
