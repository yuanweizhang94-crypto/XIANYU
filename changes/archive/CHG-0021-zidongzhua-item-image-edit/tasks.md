# CHG-0021 Tasks

Status: ARCHIVED

Change ID: CHG-0021-zidongzhua-item-image-edit

- [x] Inspect current upstream and official PC frontend existing-item edit capability.
- [x] Prove local `/items/{item_id}` is metadata-only and cannot satisfy the platform-edit outcome.
- [x] Extend existing `mtop_call` with a default-compatible no-network-retry option for side-effect writes.
- [x] Extend existing `XianyuPersonalPublisher` with read-only image status and image-only existing-item edit methods.
- [x] Add authoritative post-write `editDetail` readback and Alibaba CDN object-equivalence comparison.
- [x] Add Backend GET/POST item-image routes with account/item ownership and XIANYU static-path validation.
- [x] Add targeted tests for field preservation, UNKNOWN no-retry semantics, read-only status, and CDN normalization.
- [x] Compile changed Python files and pass diff checks.
- [x] Deploy incrementally over the existing production Backend without whole-file overwrite.
- [x] Update four existing ZIDONGZHUA listings in place and confirm 4/4 platform image readback.
- [x] Reuse upstream-native item synchronization for the one item missing from local catalog.
- [x] Generate and hash-lock the vendor patch and verify clean apply against upstream base.
- [x] Persist archived governance evidence and patch semantic tests in XIANYU.
