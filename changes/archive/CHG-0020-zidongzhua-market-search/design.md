# CHG-0020 Design

Status: ARCHIVED

Change ID: CHG-0020-zidongzhua-market-search

## Architecture

Existing ownership remains unchanged:

`ZIDONGZHUA -> COMPANY thin adapter -> XIANYU Backend existing search route -> XianyuSearchClient -> Xianyu MTOP search`.

The change reuses the existing upstream `common/services/xianyu_search_client.py` owner and the existing Backend search router. It does not create a second search client, Session owner, browser verifier, account-rotation worker, or CAPTCHA/slider handler.

## Fail-closed market-search flow

1. Accept one requested XIANYU account for the call.
2. Construct exactly one existing `XianyuSearchClient` for that account.
3. Execute the native item search through the existing Backend search owner.
4. Sanitize the result to public listing/business fields required by ZIDONGZHUA.
5. If validation/risk-control markers appear, stop and return `PLATFORM_VERIFICATION_REQUIRED`.
6. Do not rotate to another account after verification.
7. Do not invoke SliderHandler, browser verification, QR, face, CAPTCHA, or other verification bypass.
8. Unknown search failures fail closed rather than spawning a second execution path.

## Ownership and security

- XIANYU remains the business/search owner.
- COMPANY remains a thin operations bridge only.
- ZIDONGZHUA consumes sanitized market evidence and does not own search implementation.
- Cookie, Token, password, profile, authorization, and raw upstream payload secrets are not exposed.
- `view_count` remains unavailable when the safe native search path does not provide it.

## Rollback

Remove the CHG-0020 vendor patch / incremental Backend route change and restart only the Backend if runtime rollback is required. Existing Session, WebSocket, Publisher, Scheduler, COMPANY infrastructure, and ZIDONGZHUA decision state remain separate owners.
