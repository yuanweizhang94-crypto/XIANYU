# CHG-0020 ZIDONGZHUA Fail-Closed Market Search

Status: ARCHIVED

Change ID: CHG-0020-zidongzhua-market-search

## Execution contract

User outcome: expose real Xianyu market search to the ZIDONGZHUA autonomous revenue workflow without creating a second search/session/browser system and without automatically solving or bypassing official platform verification.

## Upstream/local/runtime evidence

- Existing upstream capability: `common/services/xianyu_search_client.py` already owns Xianyu MTOP item search and `parse_search_item`.
- Existing Goofish Compass browser path was rejected for this use because its service invokes the existing slider verification handler.
- Existing listing-monitor task may rotate fallback accounts, so it cannot provide strict same-call fail-closed semantics.
- Production Backend already contains `XianyuSearchClient`; no new external dependency is required.

## Reuse decision

Decision: PATCH_UPSTREAM_EXISTING_ROUTE_ONLY.

The smallest change extends the existing Backend search router with `POST /search/market-items`, creates exactly one `XianyuSearchClient` for the requested account, sanitizes public listing output, and returns `PLATFORM_VERIFICATION_REQUIRED` immediately when validation/risk markers occur.

## Safety contract

- one account per call
- no account rotation after verification
- no SliderHandler / browser verification handler in this route
- no CAPTCHA/slider/QR/face bypass
- no Cookie/Token/password/profile data in response
- `view_count` remains unavailable when it cannot be obtained through the safe native search client
- verification or unknown search failure fails closed

## Production result

The route was loaded into the existing Backend only. OpenAPI confirmed `/api/v1/search/market-items`. Targeted safety tests passed 5/5. Real Phase 1 market searches completed without platform verification and supplied pricing / `want_count` evidence used by ZIDONGZHUA to choose its first four original Excel SKUs.
