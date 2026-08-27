# CHG-0020 Tasks

Status: ARCHIVED

Change ID: CHG-0020-zidongzhua-market-search

- [x] Inspect existing upstream `XianyuSearchClient` and current Backend search ownership.
- [x] Reject browser/slider and fallback-account paths that cannot satisfy strict fail-closed same-call semantics.
- [x] Record `PATCH_UPSTREAM_EXISTING_ROUTE_ONLY` reuse decision and duplicate-development assessment.
- [x] Extend the existing Backend search router with the market-items route using exactly one requested account.
- [x] Sanitize public listing output and omit credentials/raw secret-bearing payloads.
- [x] Map platform validation/risk markers to `PLATFORM_VERIFICATION_REQUIRED` and stop without account rotation.
- [x] Keep SliderHandler/CAPTCHA/QR/face verification bypass outside the route.
- [x] Pass targeted route safety tests 5/5 and Python compile validation.
- [x] Verify production OpenAPI route presence.
- [x] Hash-lock the vendor patch and verify strict clean apply against the recorded reconstructed upstream base.
- [x] Confirm the patch does not overlap the formal CHG-0017/0018/0019 patch artifacts in the target search route.
- [x] Archive the Change after production market-search evidence was successfully consumed by ZIDONGZHUA.
