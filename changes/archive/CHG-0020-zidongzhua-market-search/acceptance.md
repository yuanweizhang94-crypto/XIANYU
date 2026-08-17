# CHG-0020 Acceptance

- [x] Existing upstream `XianyuSearchClient` reused; no parallel search implementation.
- [x] Route is strict single-account per call.
- [x] Platform validation maps to `PLATFORM_VERIFICATION_REQUIRED` and stops.
- [x] No SliderHandler, automatic CAPTCHA/slider/QR/face handling, or account rotation in the route.
- [x] No raw_main or credentials exposed.
- [x] Targeted route safety tests: 5/5 PASS.
- [x] Python compile check: PASS.
- [x] Production OpenAPI route presence: PASS.
- [x] Vendor patch SHA256: `11663707335712BF39748460A44D932BC67384C9E11D0F2AB47CB3A00328800D`.
- [x] Strict vendor patch apply check on the CHG-0017 reconstructed upstream base: PASS.
- [x] Existing formal CHG-0017/0018/0019 patch artifacts do not modify `backend-web/app/api/routes/search.py`.
